from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#LAPTOPS
class LaptopSchema(BaseModel):
    id: int
    model: str
    cpu: str
    gpu: str
    ram: str
    screensize: str
    matrix: str

    class Config:
        orm_mode = True

class LaptopCreateSchema(BaseModel):
    model: str
    cpu: str
    gpu: str
    ram: str
    screensize: str
    matrix: str


#PRODUCERS
class ProducerSchema(BaseModel):
    id: int
    Name: str
    Country: str
    Placement: Optional[str]
    Warranty: Optional[bool]

    class Config:
        orm_mode = True

class ProducerCreateSchema(BaseModel):
    Name: str
    Country: str
    Placement: Optional[str]
    Warranty: Optional[bool]


#MARKET_OFFERS
class MarketOfferSchema(BaseModel):
    id: int
    LaptopID: int
    ProducerID: int
    Price: float
    Date: datetime

    class Config:
        orm_mode = True

class MarketOfferCreateSchema(BaseModel):
    LaptopID: int
    ProducerID: int
    Price: float
    Date: datetime
