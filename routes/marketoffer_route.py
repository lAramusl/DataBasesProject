from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from libs.database import get_db
from libs.models import MarketOffer
from libs.schemas import MarketOfferSchema, MarketOfferCreateSchema, MarketOfferUpdateSchema
from libs import crud
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
    skip: int = 0,
    limit: int = 100
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

    return query.offset(skip).limit(limit).all()

@router.put("/update", response_model=int)
def update_offers(
    field_name: str,
    new_value: str,
    filter_field: str = Query(..., description="Field to filter Marketoffers by"),
    filter_value: str = Query(..., description="Value to filter Marketoffers by"),
    db: Session = Depends(get_db),
):
    """
    Обновить выбранное поле для всех предложений, соответствующих фильтру.
    Возвращает количество обновлённых записей.
    """
    # Проверяем, существует ли поле в модели
    if not hasattr(MarketOffer, field_name) or not hasattr(MarketOffer, filter_field):
        raise HTTPException(status_code=400, detail="Invalid field name(s)")

    filter_condition = getattr(MarketOffer, filter_field) == filter_value

    try:
        result = db.query(MarketOffer).filter(filter_condition).update(
            {getattr(MarketOffer, field_name): new_value},
            synchronize_session="fetch",
        )
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return result

@router.get("/", response_model=list[MarketOfferSchema])
def get_market_offers(
    skip: int = 0, 
    limit: int = 100, 
    sort_by: Optional[str] = Query(None),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    Получение рыночных предложений с возможностью сортировки
    """
    query = db.query(MarketOffer)

    if sort_by:
        if hasattr(MarketOffer, sort_by):
            column = getattr(MarketOffer, sort_by)
            if order == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
        else:
            raise HTTPException(status_code=400, detail=f"Invalid sort field '{sort_by}'")

    return query.offset(skip).limit(limit).all()

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