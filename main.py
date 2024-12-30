import psycopg2
import sqlalchemy
from fastapi import FastAPI


app = FastAPI()

@app.get('/')
def read_root():
    return {"hello" : "world"}
    
    
@app.get('/pcs')
def read_root():
    return {"hello" : "world"}