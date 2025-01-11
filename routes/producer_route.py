from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List, Optional
from libs.database import get_db
from libs import crud
from libs.models import Producer
from libs.schemas import ProducerSchema, ProducerCreateSchema, ProducerUpdateSchema

router = APIRouter()

#--------------------------------------------------------------------------------------PRODUCER CRUD
@router.post("/", response_model=ProducerSchema)
def create_producer(producer: ProducerCreateSchema, db: Session = Depends(get_db)):
    """
    Создание производителя
    """
    return crud.create_producer(db=db, producer=producer)

@router.get("/", response_model=list[ProducerSchema])
def get_producers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение производителей
    """
    return crud.get_producers(db=db, skip=skip, limit=limit)

@router.get("/{producer_id}", response_model=ProducerSchema)
def get_producer(producer_id: int, db: Session = Depends(get_db)):
    """
    Получение производителей по ID
    """
    db_producer = crud.get_producer(db=db, producer_id=producer_id)
    if db_producer is None:
        raise HTTPException(status_code=404, detail="Producer not found")
    return db_producer

@router.put("/{producer_id}", response_model=ProducerSchema)
def update_producer(producer_id: int, producer: ProducerUpdateSchema, db: Session = Depends(get_db)):
    """
    Oбновление производителя
    """
    db_producer = crud.update_producer(db=db, producer_id=producer_id, producer=producer)
    if db_producer is None:
        raise HTTPException(status_code=404, detail="Producer not found")
    return db_producer

@router.delete("/{producer_id}", response_model=ProducerSchema)
def delete_producer(producer_id: int, db: Session = Depends(get_db)):
    """
    Удаление Производителя
    """
    db_producer = crud.delete_producer(db=db, producer_id=producer_id)
    if db_producer is None:
        raise HTTPException(status_code=404, detail="Producer not found")
    return db_producer

@router.get("/filter", response_model=List[ProducerSchema])
def filter_producers(
    name: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    warranty: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """
    SELECT WHERE для производителей
    """
    query = db.query(Producer)
    if name:
        query = query.filter(Producer.Name.ilike(f"%{name}%"))
    if country:
        query = query.filter(Producer.Country.ilike(f"%{country}%"))
    if warranty is not None:
        query = query.filter(Producer.Warranty == warranty)

    return query.all()

@router.put("/update", response_model=int)
def update_producers(
    field_name: str,
    new_value: str,
    filter_field: str = Query(..., description="Field to filter by"),
    filter_value: str = Query(..., description="Value to filter by"),
    db: Session = Depends(get_db),
):
    """
    Обновить выбранное поле для всех производителей, соответствующих фильтру.
    Возвращает количество обновлённых записей.
    """
    # Проверяем, существует ли поле в модели
    if not hasattr(Producer, field_name) or not hasattr(Producer, filter_field):
        raise HTTPException(status_code=400, detail="Invalid field name(s)")

    filter_condition = getattr(Producer, filter_field) == filter_value

    try:
        result = db.query(Producer).filter(filter_condition).update(
            {getattr(Producer, field_name): new_value},
            synchronize_session="fetch",
        )
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return result

@router.get("/group-by", response_model=dict)
def group_by_producers(
    group_by_field: str,
    db: Session = Depends(get_db),
):
    """
    Выполнить группировку производителей по указанному полю.
    Возвращает количество записей в каждой группе.
    """
    if not hasattr(Producer, group_by_field):
        raise HTTPException(status_code=400, detail="Invalid field name")

    group_by_column = getattr(Producer, group_by_field)

    query = (
        db.query(group_by_column, func.count(Producer.id))
        .group_by(group_by_column)
        .all()
    )

    # Форматируем результат
    result = {row[0]: row[1] for row in query}

    return result

