from sqlalchemy import Column, Integer, String, Float, VARCHAR, DateTime, BOOLEAN, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

#WRITE EVERYTHING IN LOWERCASE
class Laptop(Base):
    __tablename__ = "laptop"
    id = Column(Integer, primary_key=True, index=True)
    model = Column(VARCHAR(20), nullable=False)
    cpu = Column(VARCHAR(20), nullable=False)
    gpu = Column(VARCHAR(20), nullable=False)
    ram = Column(VARCHAR(20), nullable=False)
    screensize = Column(VARCHAR(10), nullable=False)
    matrix = Column(VARCHAR(10), nullable=False)

    market_offers = relationship("MarketOffer", back_populates="laptop", foreign_keys="MarketOffer.laptopid")


class Producer(Base):
    __tablename__ = "producer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    placement = Column(String, nullable=True)
    warranty = Column(BOOLEAN, nullable=True)

    market_offers = relationship("MarketOffer", back_populates="producer", foreign_keys="MarketOffer.producerid")


class MarketOffer(Base):
    __tablename__ = "marketoffer"
    id = Column(Integer, primary_key=True, index=True)
    laptopid = Column(Integer, ForeignKey("laptop.id"), nullable=False)  # Обратите внимание на регистр
    producerid = Column(Integer, ForeignKey("producer.id"), nullable=False)  # Обратите внимание на регистр
    price = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)

    laptop = relationship("Laptop", back_populates="market_offers")
    producer = relationship("Producer", back_populates="market_offers")
