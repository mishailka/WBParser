import json
import requests
from fastapi import FastAPI, Query
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/wb_db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    wb_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    brand = Column(String, nullable=True)
    price = Column(Float, nullable=False, default=0)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, default=0)
    stock = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)



app = FastAPI(title="WB Products API")

@app.get("/products")
def get_products(name: str | None = Query(None)):
    db = SessionLocal()
    query = db.query(Product)
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    results = query.limit(50).all()
    db.close()
    return [
        {
            "id": p.id,
            "wb_id": p.wb_id,
            "name": p.name,
            "brand": p.brand,
            "price": p.price,
            "rating": p.rating,
            "reviews_count": p.reviews_count,
            "stock": p.stock
        }
        for p in results
    ]
