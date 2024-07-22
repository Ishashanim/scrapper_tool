from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.future import select
from .settings import Settings

settings = Settings()

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product_title = Column(String, unique=True, index=True)
    product_price = Column(Float)
    path_to_image = Column(String)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_db_and_tables():
    Base.metadata.create_all(bind=engine)