from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    id: int
    name: str
    brand: Optional[str] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    price: Optional[float] = None
    stock: Optional[int] = None

    class Config:
        orm_mode = True   # чтобы работало с SQLAlchemy-моделями