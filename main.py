from libs.database import engine, Base
from fastapi import FastAPI
from routes import laptop_route, marketoffer_route, producer_route

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(producer_route.router, prefix="/producers", tags=["Producers"])

app.include_router(laptop_route.router, prefix="/laptops", tags=["Laptops"])

app.include_router(marketoffer_route.router, prefix="/marketoffers", tags=["Marketoffers"])

