from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from libs.database import get_db
from libs.models import Laptop, MarketOffer
from libs.schemas import LaptopSchema, LaptopCreateSchema, LaptopUpdateSchema
from libs import crud
from sqlalchemy import Integer, Float
from sqlalchemy.sql import func

router = APIRouter()

@router.get("/filter", response_model=List[LaptopSchema])
def filter_laptops(
    model: Optional[str] = Query(None),
    cpu: Optional[str] = Query(None),
    ram: Optional[str] = Query(None),
    max_screensize: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    '''
    SELECT WHERE запрос для Ноутбуков
    '''
    query = db.query(Laptop)
    if model:
        query = query.filter(Laptop.model.ilike(f"%{model}%"))
    if cpu:
        query = query.filter(Laptop.cpu.ilike(f"%{cpu}%"))
    if ram:
        query = query.filter(Laptop.ram.ilike(f"%{ram}%"))
    if max_screensize:
        query = query.filter(Laptop.screensize.cast(Float) <= max_screensize)

    return query.all()

@router.get("/laptops-with-market-offers", response_model=List[dict])
def get_laptops_with_market_offers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список ноутбуков с их рыночными предложениями (JOIN Laptop и MarketOffer).
    """
    query = db.query(Laptop, MarketOffer).join(MarketOffer, Laptop.id == MarketOffer.laptopid).all()

    return [
        {
            "laptop": {
                "id": laptop.id,
                "model": laptop.model,
                "cpu": laptop.cpu,
                "gpu": laptop.gpu,
                "ram": laptop.ram,
                "screensize": laptop.screensize,
                "matrix": laptop.matrix,
                "color": laptop.color,
                "extra_info": laptop.extra_info
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

@router.put("/update", response_model=int)
def update_laptops(
    field_name: str,
    new_value: str,
    filter_field: str = Query(..., description="Field to filter laptops by"),
    filter_value: str = Query(..., description="Value to filter laptops by"),
    db: Session = Depends(get_db),
    skip: int = 0, 
    limit: int = 100,
):
    """
    Обновить выбранное поле для всех ноутбуков, соответствующих фильтру.
    Возвращает количество обновлённых записей.
    """
    # Проверяем, существует ли поле в модели
    if not hasattr(Laptop, field_name) or not hasattr(Laptop, filter_field):
        raise HTTPException(status_code=400, detail="Invalid field name(s)")

    filter_condition = getattr(Laptop, filter_field).ilike(f"%{filter_value}%")

    try:
        result = db.query(Laptop).filter(filter_condition).update(
            {getattr(Laptop, field_name): new_value},
            synchronize_session="fetch",
        )
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return result

@router.get("/group-by")
def group_by_field(
    group_field: str = Query(..., description="Поле для группировки (например, CPU, GPU, RAM, ScreenSize)"),
    db: Session = Depends(get_db),
):
    """
    Группировка данных по выбранному полю с применением агрегатной функции.
    :param group_field: Поле, по которому нужно группировать.
    :param aggregate_field: Поле, к которому применяется агрегатная функция.
    :param aggregate_function: Агрегатная функция (avg, sum, min, max).
    """
    # Проверка существования полей в модели
    group_field = group_field.lower()
    if not hasattr(Laptop, group_field):
        raise HTTPException(status_code=400, detail=f"Field '{group_field}' does not exist in Laptop")

    # Определение агрегатной функции

    # Выполнение запроса
    query = db.query(Laptop).group_by(Laptop.id, group_field)
    result = query.all()

    return result

@router.get("/", response_model=list[LaptopSchema])
def get_laptops(
    skip: int = 0, 
    limit: int = 100, 
    sort_by: Optional[str] = Query(None),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    Получение ноутбуков с возможностью сортировки
    """
    query = db.query(Laptop)

    if sort_by:
        if hasattr(Laptop, sort_by):
            column = getattr(Laptop, sort_by)
            if order == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
        else:
            raise HTTPException(status_code=400, detail=f"Invalid sort field '{sort_by}'")

    return query.offset(skip).limit(limit).all()

@router.get("/search-json", response_model=List[LaptopSchema])
def search_laptops_by_json(
    key: str, value: str, db: Session = Depends(get_db)
):
    """
    Поиск ноутбуков по ключу и значению в extra_info (JSON).
    """
    query = db.query(Laptop).filter(Laptop.extra_info[key].astext == value)
    result = query.all()
    if not result:
        raise HTTPException(status_code=404, detail="No laptops found")
    return result

#--------------------------------------------------------------------------------LAPTOP CRUD
@router.post("/", response_model=LaptopSchema)
def create_laptop(laptop: LaptopCreateSchema, db: Session = Depends(get_db)):
    '''
    Создание нового Ноутбука
    '''
    return crud.create_laptop(db=db, laptop=laptop)

@router.get("/", response_model=list[LaptopSchema])
def get_laptops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    '''
    Получение ноутбуков
    '''
    return crud.get_laptops(db=db, skip=skip, limit=limit)

@router.get("/{laptop_id}", response_model=LaptopSchema)
def get_laptop(laptop_id: int, db: Session = Depends(get_db)):
    '''
    Получение Ноутбука по ID
    '''
    db_laptop = crud.find_laptop(db=db, laptop_id=laptop_id)
    if db_laptop is None:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return db_laptop

@router.put('/{laptop_id}', response_model=LaptopUpdateSchema)
def update_laptop(laptop_id: int, laptop: LaptopUpdateSchema, db: Session = Depends(get_db)):
    """
    Обновление полей ноутбука
    """
    db_laptop = crud.update_laptop(db=db, laptop_id=laptop_id, laptop=laptop)

    if db_laptop is None:
        raise HTTPException(status_code=404, detail="laptop not found")
    
    return db_laptop

@router.delete("/{laptop_id}", response_model=LaptopSchema)
def delete_laptop(laptop_id: int, db: Session = Depends(get_db)):
    '''
    Удаление ноутбука по ID
    '''
    try:
        db_laptop = crud.delete_laptop(db=db, laptop_id=laptop_id)
    except:
        raise HTTPException(status_code=500, detail="Laptop is connected to another table")
    if db_laptop is None:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return db_laptop