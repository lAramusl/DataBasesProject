import libs.models as modl
from libs.database import get_db, engine, Base
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get('/')
def read_root():
    return {"hello" : "world"}
    
    
@app.get('/Laptop')
def read_root(db: Session = Depends(get_db)):
    return db.query(modl.Laptop).all()