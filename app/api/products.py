from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .. import crud, schemas
from fastapi_cache.decorator import cache
from typing import List

router = APIRouter()


@router.get("/products/", response_model=List[schemas.ProductOut])
@cache(expire=60)
async def get_all_products(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_products(db)
