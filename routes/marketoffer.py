from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from libs.database import get_db
from libs.models import MarketOffer
from libs.schemas import MarketOfferSchema
from datetime import datetime

router = APIRouter()

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

