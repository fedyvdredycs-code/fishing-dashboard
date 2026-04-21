from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./fishing.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    records = relationship("FishingRecord", back_populates="owner", cascade="all, delete-orphan")

class FishingRecord(Base):
    __tablename__ = "fishing_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String(20), nullable=False)
    time = Column(String(10), default="")
    location = Column(String(200), nullable=False)
    weather = Column(String(20), nullable=False)
    temp = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    wind = Column(String(100), default="")
    water_temp = Column(Float, nullable=True)
    water_level = Column(String(20), default="")
    method = Column(String(50), default="")
    bait = Column(String(200), default="")
    rating = Column(Integer, nullable=True)
    notes = Column(Text, default="")
    catches_json = Column(Text, default="[]")
    total_weight = Column(Float, default=0)
    total_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="records")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
