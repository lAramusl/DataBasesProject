from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from libs.database import get_db
from libs.models import MarketOffer
from libs.schemas import MarketOfferSchema, MarketOfferCreateSchema, MarketOfferUpdateSchema
from libs import crud
from datetime import datetime

router = APIRouter()

#-----------------------------------------------------------------------------------------------MARKET_OFFER CRUD
@router.post("/", response_model=MarketOfferSchema)
def create_market_offer(market_offer: MarketOfferCreateSchema, db: Session = Depends(get_db)):
    return crud.create_market_offer(db=db, market_offer=market_offer)

@router.get("/", response_model=list[MarketOfferSchema])
def get_market_offers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_market_offers(db=db, skip=skip, limit=limit)

@router.get("/{market_offer_id}", response_model=MarketOfferSchema)
def get_market_offer(market_offer_id: int, db: Session = Depends(get_db)):
    db_market_offer = crud.get_market_offer(db=db, market_offer_id=market_offer_id)
    if db_market_offer is None:
        raise HTTPException(status_code=404, detail="MarketOffer not found")
    return db_market_offer

@router.put("/{market_offer_id}", response_model=MarketOfferSchema)
def update_market_offer(market_offer_id: int, market_offer: MarketOfferUpdateSchema, db: Session = Depends(get_db)):
    db_market_offer = crud.update_market_offer(db=db, market_offer_id=market_offer_id, market_offer=market_offer)
    if db_market_offer is None:
        raise HTTPException(status_code=404, detail="MarketOffer not found")
    return db_market_offer

@router.delete("/{market_offer_id}", response_model=MarketOfferSchema)
def delete_market_offer(market_offer_id: int, db: Session = Depends(get_db)):
    db_market_offer = crud.delete_market_offer(db=db, market_offer_id=market_offer_id)
    if db_market_offer is None:
        raise HTTPException(status_code=404, detail="MarketOffer not found")
    return db_market_offer

@router.get("/filter", response_model=List[MarketOfferSchema])
def filter_market_offers(
    laptop_id: Optional[int] = None,
    producer_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    query = db.query(MarketOffer)

    if laptop_id:
        query = query.filter(MarketOffer.laptopid == laptop_id)
    if producer_id:
        query = query.filter(MarketOffer.producerid == producer_id)
    if min_price:
        query = query.filter(MarketOffer.price >= min_price)
    if max_price:
        query = query.filter(MarketOffer.price <= max_price)
    if start_date:
        query = query.filter(MarketOffer.date >= start_date)
    if end_date:
        query = query.filter(MarketOffer.date <= end_date)

    return query.all()

