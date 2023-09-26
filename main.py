from fastapi import FastAPI
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

def myHash(cust: Customer) -> str:
    return str(floor(abs(hash(cust.name)/(10**7))) + floor(abs(hash(cust.number)/(10**4))))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/customers")
def get_customers() -> list[Customer]:
    table: FetchResponse = db.fetch()
    return table.items

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
def advance_queue() -> Union[Customer, None]:
    currentQueue = queue.get("0")["list"]
    nextCustKey = currentQueue.pop(0)
    queue.put({"list" :currentQueue}, "0")
    customer: Customer = db.get(nextCustKey)
    db.delete(nextCustKey)
    return customer

@app.get("/add")
def add_customer(name: str, number: int) -> Customer:
    customer: Customer = Customer(name=name, number=number)
    key = myHash(customer)
    currentQueue = queue.get("0")["list"]
    currentQueue.append(key)
    queue.put({"list" :currentQueue}, "0")
    return db.put(customer.toDict(), key) #, expire_in=43200) #Expires in 12 hours


@app.get("/tablesize")
def get_num_customers() -> int:
    table: FetchResponse = db.fetch()
    return table.count

@app.get("/delete")
def delete_customer_for_key(name: str, number: int) -> bool:
    try:
        customer: Customer = Customer(name=name, number=number)
        db.delete(myHash(customer))
        currentQueue = queue.get("0")["list"]
        currentQueue.remove(myHash(customer))
        queue.put({"list" : currentQueue}, "0")
        return True
    except ValueError:
        return False

@app.get("/clear-all")
def clearDB() -> bool:
    customers = get_customers()
    for customerDict in customers:
        db.delete(customerDict["key"]) #Removes everyone from the customer db
    queue.put({"list": []}, "0") #Clears the queue

    if get_num_customers() == 0:
        return True
    return False