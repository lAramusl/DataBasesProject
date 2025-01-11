from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
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

@router.put("/producers/update", response_model=int)
def update_producers(
    field_name: str,
    new_value: str,
    filter_field: str = Query(..., description="Field to filter producers by"),
    filter_value: str = Query(..., description="Value to filter producers by"),
    db: Session = Depends(get_db),
):
    """
    Обновить выбранное поле для всех производителей, соответствующих фильтру.
    Возвращает количество обновлённых записей.
    """
    # Проверяем, существует ли поле в модели
    if not hasattr(Producer, field_name) or not hasattr(Producer, filter_field):
        raise HTTPException(status_code=400, detail="Invalid field name(s)")

    # Формируем условие WHERE
    filter_condition = getattr(Producer, filter_field) == filter_value

    # Выполняем обновление
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

@router.get("/producers/group-by", response_model=dict)
def group_by_producers(
    group_by_field: str,
    db: Session = Depends(get_db),
):
    """
    Выполнить группировку производителей по указанному полю.
    Возвращает количество записей в каждой группе.
    """
    # Проверяем, существует ли поле в модели
    if not hasattr(Producer, group_by_field):
        raise HTTPException(status_code=400, detail="Invalid field name")

    # Получаем поле для группировки
    group_by_column = getattr(Producer, group_by_field)

    # Выполняем группировку
    query = (
        db.query(group_by_column, func.count(Producer.id))
        .group_by(group_by_column)
        .all()
    )

    # Форматируем результат
    result = {row[0]: row[1] for row in query}

    return result

