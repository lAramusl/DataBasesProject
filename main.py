import libs.models as modl
import libs.schemas as sch
from libs.database import get_db, engine, Base
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from routes import laptop_route, marketoffer_route, producer_route
import libs.crud as crud

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(producer_route.router, prefix="/producers", tags=["Producers"])

app.include_router(laptop_route.router, prefix="/laptops", tags=["Laptops"])

app.include_router(marketoffer_route.router, prefix="/marketoffers", tags=["Marketoffers"])

