from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from . import models


async def get_products_by_category(db: AsyncSession, category_name: str):
    result = await db.execute(
        select(models.Product)
        .join(models.Category)
        .options(selectinload(models.Product.brand), selectinload(models.Product.category), selectinload(models.Product.reviews))
        .where(models.Category.name == category_name)
    )
    return result.scalars().all()


async def get_all_brands(db: AsyncSession):
    result = await db.execute(select(models.Brand))
    return result.scalars().all()


async def get_products_by_brand(db: AsyncSession, brand_name: str):
    result = await db.execute(
        select(models.Product)
        .join(models.Brand)
        .options(selectinload(models.Product.brand), selectinload(models.Product.category), selectinload(models.Product.reviews))
        .where(models.Brand.name == brand_name)
    )
    return result.scalars().all()


async def get_all_products(db: AsyncSession):
    result = await db.execute(
        select(models.Product).options(
            selectinload(models.Product.brand), 
            selectinload(models.Product.category), 
            selectinload(models.Product.reviews)
        )
    )
    return result.scalars().all()
