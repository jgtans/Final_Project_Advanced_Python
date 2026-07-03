from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .. import crud, schemas
from fastapi_cache.decorator import cache
from typing import List

router = APIRouter()


@router.get("/brands/", response_model=List[schemas.BrandOut])
@cache(expire=60)
async def get_all_brands(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_brands(db)


@router.get("/brand/{brand_name}", response_model=List[schemas.ProductOut])
@cache(expire=60)
async def get_products_by_brand(brand_name: str, db: AsyncSession = Depends(get_db)):
    return await crud.get_products_by_brand(db, brand_name)
