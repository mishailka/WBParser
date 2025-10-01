from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal, Product
from schemas import ProductBase

app = FastAPI(title="Wildberries Parser API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products", response_model=List[ProductBase])
def get_products(name: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Product)
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    return query.all()
