from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from libs.database import get_db
from libs.models import Laptop
from libs.schemas import LaptopSchema
from sqlalchemy import Integer, Float

router = APIRouter()

@router.get("/filter", response_model=List[LaptopSchema])
def filter_laptops(
    model: Optional[str] = Query(None),
    cpu: Optional[str] = Query(None),
    min_ram: Optional[int] = Query(None),
    max_screensize: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Laptop)
    if model:
        query = query.filter(Laptop.model.ilike(f"%{model}%"))
    if cpu:
        query = query.filter(Laptop.cpu.ilike(f"%{cpu}%"))
    if min_ram:
        query = query.filter(Laptop.ram.cast(Integer) >= min_ram)
    if max_screensize:
        query = query.filter(Laptop.screensize.cast(Float) <= max_screensize)

    return query.all()