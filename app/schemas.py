from pydantic import BaseModel
from typing import List


class ReviewOut(BaseModel):
    id: int
    rating: float
    comment: str
    reviewer_name: str
    
    class Config:
        from_attributes = True


class BrandOut(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True


class CategoryOut(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True


class ProductOut(BaseModel):
    id: int
    sku: str
    title: str
    description: str
    price: float
    brand: BrandOut
    category: CategoryOut
    reviews: List[ReviewOut] = []
    
    class Config:
        from_attributes = True
