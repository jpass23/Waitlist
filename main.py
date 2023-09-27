from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Union
from deta import Deta
from models import FetchResponse, Customer
from math import *
from datetime import datetime

db_key = "b0pmrzzf4gc_EECpB8NVp9SexAHjntA89mA6zwuH4qqW"

deta = Deta(db_key)

db = deta.Base("customer")
queue = deta.Base("queue")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def myHash(cust: Customer) -> str:
    return str(floor(abs(hash(cust.name)/(10**7))) + floor(abs(hash(cust.number)/(10**4))))

@app.get("/join-waitlist", response_class=HTMLResponse)
def render_join_page(request: Request):
    return templates.TemplateResponse("join.html", {"request": request})

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/customers")
def get_customers() -> list[Customer]:
    keys = get_queue()
    customers = []
    for key in keys:
        customers.append(get_customer_for_key(key))
    return customers

@app.get("/queue")
def get_queue() -> list[int]:
    return queue.get("0")["list"]

@app.get("/customer")
def get_customer_for_key(key: str) -> Union[Customer, None]:
    customer: Customer = db.get(key)
    return customer

@app.get("/next-customer") #Shows next customer without removing them from queue
def get_next_customer() -> Union[Customer, None]:
    currentQueue = queue.get("0")["list"]
    nextCustKey = currentQueue[0]
    customer: Customer = db.get(nextCustKey)
    return customer

@app.get("/advance-queue") #Actually advances the queue by removing and returning the next customer
def advance_queue(): #-> Union[Customer, None]:
    currentQueue = queue.get("0")["list"]
    nextCustKey = currentQueue.pop(0)
    queue.put({"list" :currentQueue}, "0")
    customer: Customer = db.get(nextCustKey)
    db.delete(nextCustKey)
    return RedirectResponse("https://waitlist-1-c5006775.deta.app/waitlist/3014707") #'https://waitlist-1-c5006775.deta.app/waitlist/3014707'

@app.get("/add", response_class=HTMLResponse)
def add_customer(request: Request, name: str, number: int) -> Customer:
    customer: Customer = Customer(name=name, number=number)
    key = myHash(customer)
    currentQueue: list = queue.get("0")["list"]
    if key in currentQueue:
        pass
    else:
        currentQueue.append(key)
    queue.put({"list" :currentQueue}, "0")
    db.put(customer.toDict(), key) #, expire_in=43200) #Expires in 12 hours
    return templates.TemplateResponse("position.html", {"request": request, "name": name, "number": number})

@app.get("/tablesize")
def get_num_customers() -> int:
    table: FetchResponse = db.fetch()
    return table.count

@app.get("/delete")
def delete_customer_for_key(request: Request, name: str, number: int, admin: bool = False):
    try:
        customer: Customer = Customer(name=name, number=number)
        db.delete(myHash(customer))
        currentQueue = queue.get("0")["list"]
        currentQueue.remove(myHash(customer))
        queue.put({"list" : currentQueue}, "0")
        if admin:
            return RedirectResponse("https://waitlist-1-c5006775.deta.app/waitlist/3014707") #'https://waitlist-1-c5006775.deta.app/waitlist/3014707'
        else:
            return templates.TemplateResponse("deleted.html", {"request": request, "name": name, "number": number})
    except ValueError:
        return False

@app.get("/clear-all")
def clearDB():
    customers = get_customers()
    for customerDict in customers:
        db.delete(customerDict["key"]) #Removes everyone from the customer db
    queue.put({"list": []}, "0") #Clears the queue

    if get_num_customers() == 0:
        return RedirectResponse("https://waitlist-1-c5006775.deta.app/waitlist/3014707") #'https://waitlist-1-c5006775.deta.app/waitlist/3014707'
    return False

@app.get("/position")
def get_position(name: str, number: int) -> Union[int, None]:
    queue = get_queue()
    try:
        return queue.index(myHash(Customer(name=name, number=number))) + 1
    except ValueError:
        return None

@app.get("/waitlist/3014707", response_class=HTMLResponse)
def waitlist(request: Request):
    return templates.TemplateResponse("waitlist.html", {"request": request})