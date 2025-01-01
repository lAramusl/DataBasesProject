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

def update_laptop(db: Session, laptop_id: int, laptop: sch.LaptopUpdateSchema):
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


def create_producer(db: Session, producer: sch.ProducerCreateSchema):
    db_producer = modl.Producer(
        name=producer.name,
        country=producer.country,
        placement=producer.placement,
        warranty=producer.warranty
    )
    db.add(db_producer)
    db.commit()
    db.refresh(db_producer)
    return db_producer


def get_producers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(modl.Producer).offset(skip).limit(limit).all()

def get_producer(db: Session, producer_id: int):
    return db.query(modl.Producer).filter(modl.Producer.id == producer_id).first()

def update_producer(db: Session, producer_id: int, producer: sch.ProducerUpdateSchema):
    db_producer = db.query(modl.Producer).filter(modl.Producer.id == producer_id).first()
    if db_producer:
        db_producer.name = producer.name if producer.name else db_producer.name
        db_producer.country = producer.country if producer.country else db_producer.country
        db_producer.placement = producer.placement if producer.placement else db_producer.placement
        db_producer.warranty = producer.warranty if producer.warranty is not None else db_producer.warranty

        db.commit()
        db.refresh(db_producer)
        return db_producer
    return None

# Delete a producer
def delete_producer(db: Session, producer_id: int):
    db_producer = db.query(modl.Producer).filter(modl.Producer.id == producer_id).first()
    if db_producer:
        db.delete(db_producer)
        db.commit()
        return db_producer
    return None


# --- CRUD для MarketOffer ---

# Create a new market offer
def create_market_offer(db: Session, market_offer: sch.MarketOfferCreateSchema):
    db_market_offer = modl.MarketOffer(
        laptopid=market_offer.laptopid,
        producerid=market_offer.producerid,
        price=market_offer.price,
        date=market_offer.date
    )
    db.add(db_market_offer)
    db.commit()
    db.refresh(db_market_offer)
    return db_market_offer

# Get all market offers
def get_market_offers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(modl.MarketOffer).offset(skip).limit(limit).all()

# Get a market offer by ID
def get_market_offer(db: Session, market_offer_id: int):
    return db.query(modl.MarketOffer).filter(modl.MarketOffer.id == market_offer_id).first()

# Update a market offer
def update_market_offer(db: Session, market_offer_id: int, market_offer: sch.MarketOfferUpdateSchema):
    db_market_offer = db.query(modl.MarketOffer).filter(modl.MarketOffer.id == market_offer_id).first()
    if db_market_offer:
        db_market_offer.laptopid = market_offer.laptopid if market_offer.laptopid else db_market_offer.laptopid
        db_market_offer.producerid = market_offer.producerid if market_offer.producerid else db_market_offer.producerid
        db_market_offer.price = market_offer.price if market_offer.price else db_market_offer.price
        db_market_offer.date = market_offer.date if market_offer.date else db_market_offer.date

        db.commit()
        db.refresh(db_market_offer)
        return db_market_offer
    return None

# Delete a market offer
def delete_market_offer(db: Session, market_offer_id: int):
    db_market_offer = db.query(modl.MarketOffer).filter(modl.MarketOffer.id == market_offer_id).first()
    if db_market_offer:
        db.delete(db_market_offer)
        db.commit()
        return db_market_offer
    return None
