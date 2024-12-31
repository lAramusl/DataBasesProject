from sqlalchemy import Column, Integer, String, Float, VARCHAR, DateTime, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Laptop(Base):
    __tablename__ = "Laptop"
    id = Column(Integer, primary_key=True, index=True)
    Model = Column(VARCHAR(20), nullable=False)
    CPU = Column(VARCHAR(20), nullable=False)
    GPU = Column(VARCHAR(20), nullable=False)
    RAM = Column(VARCHAR(20), nullable=False)
    ScreenSize = Column(VARCHAR(10), nullable=False)
    Matrix = Column(VARCHAR(10), nullable=False)

class Producer(Base):
    __tablename__ = "Producer"
    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)
    Country = Column(String, nullable=False)
    Placement = Column(String, nullable=True)
    Warranty = Column(BOOLEAN, nullable=True)

class MarketOffer(Base):
    __tablename__ = "MarketOffer"
    id = Column(Integer, primary_key=True, index=True)
    LaptopID = Column(Integer, nullable=False)#add foreign key thing
    ProducerID = Column(Integer, nullable=False)#add foreign key thing
    Price = Column(Float, nullable=False)
    Date = Column(DateTime, nullable=False)
