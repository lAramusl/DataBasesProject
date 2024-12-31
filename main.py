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

#LAPTOP CRUD
@app.post("/laptop/", response_model=sch.LaptopSchema)
def create_laptop(laptop: sch.LaptopCreateSchema, db: Session = Depends(get_db)):
    return crud.create_laptop(db=db, laptop=laptop)

@app.get("/laptops/", response_model=list[sch.LaptopSchema])
def get_laptops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_laptops(db=db, skip=skip, limit=limit)

@app.get("/laptop/{laptop_id}", response_model=sch.LaptopSchema)
def get_laptop(laptop_id: int, db: Session = Depends(get_db)):
    db_laptop = crud.find_laptop(db=db, laptop_id=laptop_id)
    if db_laptop is None:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return db_laptop

@app.put('/laptop/{laptop_id}', response_model=sch.LaptopSchema)
def update_laptop(laptop_id: int, laptop: sch.LaptopSchema, db: Session = Depends(get_db)):
    db_laptop = crud.update_laptop(db=db, laptop_id=laptop_id, laptop=laptop)

    if db_laptop is None:
        raise HTTPException(status_code=404, detail="laptop not found")
    
    return db_laptop

@app.delete("/laptop/{laptop_id}", response_model=sch.LaptopSchema)
def delete_laptop(laptop_id: int, db: Session = Depends(get_db)):
    db_laptop = crud.delete_laptop(db=db, laptop_id=laptop_id)
    if db_laptop is None:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return db_laptop