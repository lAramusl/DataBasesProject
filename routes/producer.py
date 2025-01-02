from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from libs.database import get_db
from libs.models import Producer
from libs.schemas import ProducerSchema

router = APIRouter()

@router.get("/filter", response_model=List[ProducerSchema])
def filter_producers(
    name: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    warranty: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    
    query = db.query(Producer)
    if name:
        query = query.filter(Producer.Name.ilike(f"%{name}%"))
    if country:
        query = query.filter(Producer.Country.ilike(f"%{country}%"))
    if warranty is not None:
        query = query.filter(Producer.Warranty == warranty)

    return query.all()
