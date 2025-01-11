from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from libs.database import get_db
from libs.models import Laptop, MarketOffer
from libs.schemas import LaptopSchema, MarketOfferSchema
from sqlalchemy import Integer, Float
from sqlalchemy.sql import func

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

@router.get("/laptops-with-market-offers", response_model=List[dict])
def get_laptops_with_market_offers(db: Session = Depends(get_db)):
    """
    Получить список ноутбуков с их рыночными предложениями (JOIN Laptop и MarketOffer).
    """
    query = db.query(Laptop, MarketOffer).join(MarketOffer, Laptop.id == MarketOffer.laptopid).all()

    return [
        {
            "laptop": {
                "id": laptop.id,
                "model": laptop.Model,
                "cpu": laptop.CPU,
                "gpu": laptop.GPU,
                "ram": laptop.RAM,
                "screensize": laptop.ScreenSize,
                "matrix": laptop.Matrix,
            },
            "market_offer": {
                "id": offer.id,
                "producer_id": offer.producerid,
                "price": offer.price,
                "date": offer.date,
            },
        }
        for laptop, offer in query
    ]

@router.put("/update-laptop/{laptop_id}")
def update_laptop_field(
    laptop_id: int,
    field: str,
    value: any,
    db: Session = Depends(get_db),
):
    """
    Обновить указанное поле ноутбука.
    :param laptop_id: ID ноутбука для обновления.
    :param field: Название поля, которое нужно обновить.
    :param value: Новое значение.
    """
    laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")

    if not hasattr(Laptop, field):
        raise HTTPException(status_code=400, detail=f"Field '{field}' does not exist in Laptop")

    setattr(laptop, field, value)
    db.commit()
    db.refresh(laptop)

    return {"detail": f"Laptop with ID {laptop_id} updated successfully"}


@router.get("/group-by")
def group_by_field(
    group_field: str = Query(..., description="Поле для группировки (например, CPU, GPU, RAM, ScreenSize)"),
    aggregate_field: str = Query(..., description="Поле для агрегатной функции (например, RAM, Price)"),
    aggregate_function: str = Query("avg", description="Агрегатная функция (avg, sum, min, max)"),
    db: Session = Depends(get_db),
):
    """
    Группировка данных по выбранному полю с применением агрегатной функции.
    :param group_field: Поле, по которому нужно группировать.
    :param aggregate_field: Поле, к которому применяется агрегатная функция.
    :param aggregate_function: Агрегатная функция (avg, sum, min, max).
    """
    # Проверка существования полей в модели
    if not hasattr(Laptop, group_field):
        raise HTTPException(status_code=400, detail=f"Field '{group_field}' does not exist in Laptop")
    if not hasattr(Laptop, aggregate_field):
        raise HTTPException(status_code=400, detail=f"Field '{aggregate_field}' does not exist in Laptop")

    # Определение агрегатной функции
    aggregate_functions = {
        "avg": func.avg,
        "sum": func.sum,
        "min": func.min,
        "max": func.max,
    }

    if aggregate_function not in aggregate_functions:
        raise HTTPException(
            status_code=400, detail=f"Unsupported aggregate function '{aggregate_function}'. Choose from avg, sum, min, max."
        )

    func_to_apply = aggregate_functions[aggregate_function]

    # Выполнение запроса
    query = (
        db.query(
            getattr(Laptop, group_field).label("group_value"),
            func_to_apply(getattr(Laptop, aggregate_field)).label("aggregate_result"),
        )
        .group_by(getattr(Laptop, group_field))
        .all()
    )

    result =  [
        {"group_value": row.group_value, "aggregate_result": row.aggregate_result}
        for row in query]

    return


