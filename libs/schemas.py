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
    color: str #added with alembic to db

    class Config:
        orm_mode = True

class LaptopCreateSchema(BaseModel):
    model: str
    cpu: str
    gpu: str
    ram: str
    screensize: str
    matrix: str

class LaptopUpdateSchema(BaseModel):
    model: Optional[str] = None
    cpu: Optional[str] = None
    gpu: Optional[str] = None
    ram: Optional[str] = None
    screensize: Optional[str] = None
    matrix: Optional[str] = None

    class Config:
        orm_mode = True

#PRODUCERS
class ProducerSchema(BaseModel):
    id: int
    name: str
    country: str
    placement: Optional[str]
    warranty: Optional[bool]

    class Config:
        orm_mode = True

class ProducerCreateSchema(BaseModel):
    name: str
    country: str
    placement: Optional[str]
    warranty: Optional[bool]

class ProducerUpdateSchema(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    placement: Optional[str] = None
    warranty: Optional[bool] = None

    class Config:
        orm_mode = True

#MARKET_OFFERS
class MarketOfferSchema(BaseModel):
    id: int
    laptopid: int
    producerid: int
    price: float
    date: datetime

    class Config:
        orm_mode = True

class MarketOfferCreateSchema(BaseModel):
    laptopid: int
    producerid: int
    price: float
    date: datetime

class MarketOfferUpdateSchema(BaseModel):
    laptopid: Optional[int] = None
    producerid: Optional[int] = None
    price: Optional[float] = None
    date: Optional[datetime] = None

    class Config:
        orm_mode = True