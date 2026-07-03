import httpx
import asyncio
from sqlalchemy import select
from ..database import async_session
from .. import models


async def fetch_products_page(skip: int, limit: int):
    url = f"https://dummyjson.com/products?limit={limit}&skip={skip}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json().get("products", [])


async def fetch_all_products():
    tasks = [
        fetch_products_page(0, 50),
        fetch_products_page(50, 50),
        fetch_products_page(100, 50),
        fetch_products_page(150, 50)
    ]
    results = await asyncio.gather(*tasks)
    products = []
    for res in results:
        products.extend(res)
    return products


async def load_data_to_db():
    products_data = await fetch_all_products()
    
    async with async_session() as session:
        for p_data in products_data:
            result = await session.execute(select(models.Category).where(models.Category.name == p_data["category"]))
            category = result.scalars().first()
            if not category:
                category = models.Category(name=p_data["category"])
                session.add(category)
                await session.flush()
            
            brand_name = p_data.get("brand", "Unknown")
            result = await session.execute(select(models.Brand).where(models.Brand.name == brand_name))
            brand = result.scalars().first()
            if not brand:
                brand = models.Brand(name=brand_name)
                session.add(brand)
                await session.flush()
            
            result = await session.execute(select(models.Product).where(models.Product.sku == p_data["sku"]))
            existing_product = result.scalars().first()
            
            if not existing_product:
                db_product = models.Product(
                    sku=p_data["sku"],
                    title=p_data["title"],
                    description=p_data["description"],
                    price=p_data["price"],
                    brand_id=brand.id,
                    category_id=category.id
                )
                session.add(db_product)
                await session.flush()
                
                for r_data in p_data.get("reviews", []):
                    review = models.Review(
                        product_id=db_product.id,
                        rating=r_data.get("rating", 0),
                        comment=r_data.get("comment", ""),
                        reviewer_name=r_data.get("reviewerName", "")
                    )
                    session.add(review)
                await session.commit()
