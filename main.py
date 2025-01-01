import libs.models as modl
import libs.schemas as sch
from libs.database import get_db, engine, Base
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import libs.crud as crud

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get('/')
def read_root():
    return {"hello" : "world"}

#--------------------------------------------------------------------------------LAPTOP 
@app.post("/laptops/", response_model=sch.LaptopSchema)
def create_laptop(laptop: sch.LaptopCreateSchema, db: Session = Depends(get_db)):
    return crud.create_laptop(db=db, laptop=laptop)

@app.get("/laptops/", response_model=list[sch.LaptopSchema])
def get_laptops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_laptops(db=db, skip=skip, limit=limit)

@app.get("/laptops/{laptop_id}", response_model=sch.LaptopSchema)
def get_laptop(laptop_id: int, db: Session = Depends(get_db)):
    db_laptop = crud.find_laptop(db=db, laptop_id=laptop_id)
    if db_laptop is None:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return db_laptop

@app.put('/laptops/{laptop_id}', response_model=sch.LaptopSchema)
def update_laptop(laptop_id: int, laptop: sch.LaptopSchema, db: Session = Depends(get_db)):
    db_laptop = crud.update_laptop(db=db, laptop_id=laptop_id, laptop=laptop)

    if db_laptop is None:
        raise HTTPException(status_code=404, detail="laptop not found")
    
    return db_laptop

@app.delete("/laptops/{laptop_id}", response_model=sch.LaptopSchema)
def delete_laptop(laptop_id: int, db: Session = Depends(get_db)):
    db_laptop = crud.delete_laptop(db=db, laptop_id=laptop_id)
    if db_laptop is None:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return db_laptop

#--------------------------------------------------------------------------------------PRODUCER
@app.post("/producers/", response_model=sch.ProducerSchema)
def create_producer(producer: sch.ProducerCreateSchema, db: Session = Depends(get_db)):
    return crud.create_producer(db=db, producer=producer)

@app.get("/producers/", response_model=list[sch.ProducerSchema])
def get_producers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_producers(db=db, skip=skip, limit=limit)

@app.get("/producers/{producer_id}", response_model=sch.ProducerSchema)
def get_producer(producer_id: int, db: Session = Depends(get_db)):
    db_producer = crud.get_producer(db=db, producer_id=producer_id)
    if db_producer is None:
        raise HTTPException(status_code=404, detail="Producer not found")
    return db_producer

@app.put("/producers/{producer_id}", response_model=sch.ProducerSchema)
def update_producer(producer_id: int, producer: sch.ProducerUpdateSchema, db: Session = Depends(get_db)):
    db_producer = crud.update_producer(db=db, producer_id=producer_id, producer=producer)
    if db_producer is None:
        raise HTTPException(status_code=404, detail="Producer not found")
    return db_producer

@app.delete("/producers/{producer_id}", response_model=sch.ProducerSchema)
def delete_producer(producer_id: int, db: Session = Depends(get_db)):
    db_producer = crud.delete_producer(db=db, producer_id=producer_id)
    if db_producer is None:
        raise HTTPException(status_code=404, detail="Producer not found")
    return db_producer

#-----------------------------------------------------------------------------------------------MARKET_OFFER
@app.post("/marketoffers/", response_model=sch.MarketOfferSchema)
def create_market_offer(market_offer: sch.MarketOfferCreateSchema, db: Session = Depends(get_db)):
    return crud.create_market_offer(db=db, market_offer=market_offer)

@app.get("/marketoffers/", response_model=list[sch.MarketOfferSchema])
def get_market_offers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_market_offers(db=db, skip=skip, limit=limit)

@app.get("/marketoffers/{market_offer_id}", response_model=sch.MarketOfferSchema)
def get_market_offer(market_offer_id: int, db: Session = Depends(get_db)):
    db_market_offer = crud.get_market_offer(db=db, market_offer_id=market_offer_id)
    if db_market_offer is None:
        raise HTTPException(status_code=404, detail="MarketOffer not found")
    return db_market_offer

@app.put("/marketoffers/{market_offer_id}", response_model=sch.MarketOfferSchema)
def update_market_offer(market_offer_id: int, market_offer: sch.MarketOfferUpdateSchema, db: Session = Depends(get_db)):
    db_market_offer = crud.update_market_offer(db=db, market_offer_id=market_offer_id, market_offer=market_offer)
    if db_market_offer is None:
        raise HTTPException(status_code=404, detail="MarketOffer not found")
    return db_market_offer

@app.delete("/marketoffers/{market_offer_id}", response_model=sch.MarketOfferSchema)
def delete_market_offer(market_offer_id: int, db: Session = Depends(get_db)):
    db_market_offer = crud.delete_market_offer(db=db, market_offer_id=market_offer_id)
    if db_market_offer is None:
        raise HTTPException(status_code=404, detail="MarketOffer not found")
    return db_market_offer