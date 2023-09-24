from fastapi import FastAPI
from deta import Deta

db_key = "b0pmrzzf4gc_EECpB8NVp9SexAHjntA89mA6zwuH4qqW"


deta = Deta(db_key)

db = deta.Base("customer")

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
def get_user():
    user = db.get("h7vk203u50z8")
    return user