from sqlalchemy import BigInteger, Column, Float, Integer, String, ForeignKey, DateTime, Boolean, Date, Time
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

Base = declarative_base()


class hospitals(Base):
    __tablename__ = 'hospitals'
    id = Column(Integer, primary_key=True)
    hospital = Column(String(500), nullable=False)
    contact_number=Column(String(100),default=None)
    address = Column(String(500), nullable=False)
    status = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


class facilities(Base):
    __tablename__ = 'facilities'
    id = Column(Integer, primary_key=True)
    hospital_id=Column(Integer, ForeignKey("hospitals.id"))
    facility=Column(String(200), nullable=False)
    price=Column(String(200),nullable=False)
    status = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    hospitals = relationship("Hospitals")


DATABASE_URI = "mysql+pymysql://root:14july1998$@localhost/tri-city"

engine = create_engine(
    DATABASE_URI
)

