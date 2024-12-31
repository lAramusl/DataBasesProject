from sqlalchemy.orm import Session
import libs.models as modl
import libs.schemas as sch

def create_laptop(db: Session, laptop: sch.LaptopCreateSchema):
    db_laptop = modl.Laptop(
        model=laptop.model,
        cpu=laptop.cpu,
        gpu=laptop.gpu,
        ram=laptop.ram,
        screensize=laptop.screensize,
        matrix=laptop.matrix
    )
    db.add(db_laptop)
    db.commit()
    db.refresh(db_laptop)
    return db_laptop

def get_laptops(db: Session, skip: int = 0, limit: int = 100):
    return db.query(modl.Laptop).offset(skip).limit(limit).all()

def find_laptop(db: Session, laptop_id: int):
    return db.query(modl.Laptop).filter(modl.Laptop.id == laptop_id).first()

def update_laptop(db: Session, laptop_id: int, laptop: sch.LaptopSchema):
    db_laptop = db.query(modl.Laptop).filter(modl.Laptop.id == laptop_id).first()
    if db_laptop:
        db_laptop.model = laptop.model if laptop.model else db_laptop.model
        db_laptop.cpu = laptop.cpu if laptop.cpu else db_laptop.cpu
        db_laptop.gpu = laptop.gpu if laptop.gpu else db_laptop.gpu
        db_laptop.ram = laptop.ram if laptop.ram else db_laptop.ram
        db_laptop.screensize = laptop.screensize if laptop.screensize else db_laptop.screensize
        db_laptop.matrix = laptop.matrix if laptop.matrix else db_laptop.matrix
        db.commit()
        db.refresh(db_laptop)
        return db_laptop
    return None

def delete_laptop(db: Session, laptop_id: int):
    db_laptop = db.query(modl.Laptop).filter(modl.Laptop.id == laptop_id).first()
    if db_laptop:
        db.delete(db_laptop)
        db.commit()
        return db_laptop
    return None
