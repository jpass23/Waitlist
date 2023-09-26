from pydantic import BaseModel
from datetime import datetime

class FetchResponse(BaseModel):
    count: int
    last: None
    items: list

class Customer(BaseModel):
    name: str
    number: int
    #timeAdded: datetime
    def toDict(self):
        return {"name": self.name, "number": self.number} #, "timeAdded": self.timeAdded.strftime("%Y-%m-%d %H:%M:%S")}
    
    @classmethod
    def fromDict(self, d: dict):
        return Customer(name=d["name"], number=d["number"])