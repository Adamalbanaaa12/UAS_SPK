from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Motor(Base):
    __tablename__ = 'motor'
    id = Column(Integer, primary_key=True)
    nmotor = Column(String(50))
    volume = Column(String(50)) 
    tangki = Column(String(50))
    daya = Column(String(10))
    torsi = Column(String(20))
    harga = Column(String(20))

    def __repr__(self):
        return f"motor(id={self.id!r}, brand={self.brand!r}"
