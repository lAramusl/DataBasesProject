import libs.models as modl
import libs.schemas as sch
from libs.database import get_db, engine, Base
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import libs.crud as crud

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get('/')
def read_root():
    return {"hello" : "world"}
    
    
@app.get('/laptop')
def read_root(db: Session = Depends(get_db)):
    return db.query(modl.Laptop).all()

@app.post('/laptop/')
def create_laptop(laptop: sch.LaptopCreateSchema, db: Session = Depends(get_db)):
    return crud.create_laptop(db=db, laptop=laptop)