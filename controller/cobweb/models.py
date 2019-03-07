from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Model = declarative_base()


class Apartment(Model):
    __tablename__ = 'apartment'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    owners = relationship('Ownership')


class Producer(Model):
    __tablename__ = 'producer'

    id = Column(Integer, primary_key=True)
    # Lifetime / ammortization period in years
    lifetime = Column(Integer, default=25, nullable=False)
    power = Column(Float, default=30000, nullable=False)

    owners = relationship("Ownership")


class Production(Model):
    __tablename__ = 'production'

    id = Column(Integer, primary_key=True)
    energy = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    time = Column(DateTime, nullable=False)

    producer_id = Column(Integer, ForeignKey('producer.id'), nullable=False)
    producer = relationship('Producer', backref='production')


class ElectricityPrice(Model):
    __tablename__ = 'electricity_price'

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    time = Column(DateTime, nullable=False)


class Ownership(Model):
    __tablename__ = 'ownership'

    apartment_id = Column(Integer, ForeignKey('apartment.id'), primary_key=True)
    apartment = relationship('Apartment')

    producer_id = Column(Integer, ForeignKey('producer.id'), primary_key=True)
    producer = relationship('Producer')

    percentage = Column(Float, nullable=False)


class Storage(Model):
    __tablename__ = 'storage'

    id = Column(Integer, primary_key=True)
    max_capacity = Column(Float, nullable=False)
    capacity = Column(Float, default=0, nullable=False)
    price = Column(Float, default=0, nullable=False)
    source = Column(String(63), default='external', nullable=False)
    available = Column(Boolean, default=True, nullable=False)

    apartment_id = Column(Integer, ForeignKey('apartment.id'), nullable=False)
    apartment = relationship('Apartment', backref='storages')


class Charge(Model):
    __tablename__ = 'charge'

    id = Column(Integer, primary_key=True)

    storage_id = Column(Integer, ForeignKey('storage.id'), nullable=False)
    storage = relationship('Storage', backref='pings')

    capacity = Column(Float, nullable=False)
    time = Column(DateTime, nullable=False)


class Constraint(Model):
    __tablename__ = 'constraint'

    id = Column(Integer, primary_key=True)
    capacity = Column(Float, nullable=False)
    time = Column(DateTime, nullable=False)


class Consumption(Model):
    __tablename__ = 'consumption'

    id = Column(Integer, primary_key=True)
    energy = Column(Float, nullable=False)
    origin = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    time = Column(DateTime, nullable=False)

    apartment_id = Column(Integer, ForeignKey('apartment.id'), nullable=False)
    apartment = relationship('Apartment', backref='consumptions')
