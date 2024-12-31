from sqlalchemy.orm import Session
import libs.models as modl
import libs.schemas as sch

def create_laptop(db: Session, laptop: sch.LaptopCreateSchema):
    db_laptop = modl.Laptop(
        model=laptop.Model,
        cpu=laptop.CPU,
        gpu=laptop.GPU,
        ram=laptop.RAM,
        screensize=laptop.ScreenSize,
        matrix=laptop.Matrix
    )
    db.add(db_laptop)
    db.commit()
    db.refresh(db_laptop)
    return db_laptop

def get_laptops(db: Session, skip: int = 0, limit: int = 100):
    return db.query(modl.Laptop).offset(skip).limit(limit).all()

def get_laptop(db: Session, laptop_id: int):
    return db.query(modl.Laptop).filter(modl.Laptop.id == laptop_id).first()

def update_laptop(db: Session, laptop_id: int, laptop: sch.LaptopSchema):
    db_laptop = db.query(modl.Laptop).filter(modl.Laptop.id == laptop_id).first()
    if db_laptop:
        db_laptop.Model = laptop.Model if laptop.Model else db_laptop.Model
        db_laptop.CPU = laptop.CPU if laptop.CPU else db_laptop.CPU
        db_laptop.GPU = laptop.GPU if laptop.GPU else db_laptop.GPU
        db_laptop.RAM = laptop.RAM if laptop.RAM else db_laptop.RAM
        db_laptop.ScreenSize = laptop.ScreenSize if laptop.ScreenSize else db_laptop.ScreenSize
        db_laptop.Matrix = laptop.Matrix if laptop.Matrix else db_laptop.Matrix
        
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
