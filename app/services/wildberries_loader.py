import httpx
import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import async_session
from .. import models


async def fetch_wildberries_data():
    """Загрузка данных с Wildberries через публичные API"""
    
    # Используем публичные данные и заглушки для демонстрации
    # В реальном проекте нужен ключ API Wildberries
    
    # Пример структуры данных (для демонстрации)
    wildberries_data = {
        "categories": [
            {"id": 1, "name": "Одежда"},
            {"id": 2, "name": "Обувь"},
            {"id": 3, "name": "Аксессуары"},
            {"id": 4, "name": "Красота"},
            {"id": 5, "name": "Техника"}
        ],
        "brands": [
            {"id": 1, "name": "Zara"},
            {"id": 2, "name": "H&M"},
            {"id": 3, "name": "Nike"},
            {"id": 4, "name": "Adidas"},
            {"id": 5, "name": "Apple"},
            {"id": 6, "name": "Samsung"},
            {"id": 7, "name": "LG"},
            {"id": 8, "name": "Sony"}
        ],
        "products": [
            {
                "sku": "1234567",
                "name": "Футболка Zara",
                "description": "Мужская хлопковая футболка",
                "price": 1500.0,
                "category": "Одежда",
                "brand": "Zara",
                "reviews": [
                    {"rating": 4.5, "comment": "Хорошее качество", "author": "Иван"},
                    {"rating": 5.0, "comment": "Отлично!", "author": "Петр"}
                ]
            },
            {
                "sku": "7654321",
                "name": "Кроссовки Nike",
                "description": "Спортивные кроссовки для бега",
                "price": 8500.0,
                "category": "Обувь",
                "brand": "Nike",
                "reviews": [
                    {"rating": 4.8, "comment": "Удобные", "author": "Анна"}
                ]
            },
            {
                "sku": "9876543",
                "name": "iPhone 15",
                "description": "Смартфон Apple с A17 Pro",
                "price": 89990.0,
                "category": "Техника",
                "brand": "Apple",
                "reviews": [
                    {"rating": 4.9, "comment": "Лучший смартфон", "author": "Максим"}
                ]
            },
            {
                "sku": "2345678",
                "name": "Samsung Galaxy S24",
                "description": "Флагманский смартфон Samsung",
                "price": 79990.0,
                "category": "Техника",
                "brand": "Samsung",
                "reviews": [
                    {"rating": 4.7, "comment": "Отличный экран", "author": "Ольга"}
                ]
            },
            {
                "sku": "3456789",
                "name": "Платье Zara",
                "description": "Вечернее платье",
                "price": 3500.0,
                "category": "Одежда",
                "brand": "Zara",
                "reviews": []
            },
            {
                "sku": "4567890",
                "name": "Кроссовки Adidas",
                "description": "Кроссовки для тренировок",
                "price": 6500.0,
                "category": "Обувь",
                "brand": "Adidas",
                "reviews": [
                    {"rating": 4.6, "comment": "Неплохо", "author": "Дмитрий"}
                ]
            },
            {
                "sku": "5678901",
                "name": "Краска для волос",
                "description": "Профессиональная краска",
                "price": 450.0,
                "category": "Красота",
                "brand": "Loreal",
                "reviews": [
                    {"rating": 4.2, "comment": "Хороший оттенок", "author": "Елена"}
                ]
            },
            {
                "sku": "6789012",
                "name": "Помада",
                "description": "Матовая помада",
                "price": 890.0,
                "category": "Красота",
                "brand": "Maybelline",
                "reviews": [
                    {"rating": 4.4, "comment": "Любимый цвет", "author": "Светлана"}
                ]
            }
        ]
    }
    
    return wildberries_data


async def load_data_to_db():
    """Загрузка данных Wildberries в БД"""
    print("🚀 Начинаем загрузку данных с Wildberries...")
    
    products_data = await fetch_wildberries_data()
    
    async with async_session() as session:
        # 1. Загрузка категорий
        for cat_data in products_data["categories"]:
            result = await session.execute(
                select(models.Category).where(models.Category.name == cat_data["name"])
            )
            category = result.scalars().first()
            if not category:
                category = models.Category(name=cat_data["name"])
                session.add(category)
                await session.flush()
        
        # 2. Загрузка брендов
        for brand_data in products_data["brands"]:
            result = await session.execute(
                select(models.Brand).where(models.Brand.name == brand_data["name"])
            )
            brand = result.scalars().first()
            if not brand:
                brand = models.Brand(name=brand_data["name"])
                session.add(brand)
                await session.flush()
        
        # 3. Загрузка товаров
        for prod_data in products_data["products"]:
            result = await session.execute(
                select(models.Product).where(models.Product.sku == prod_data["sku"])
            )
            existing_product = result.scalars().first()
            
            if not existing_product:
                # Получаем категорию
                result = await session.execute(
                    select(models.Category).where(models.Category.name == prod_data.get("category", "Other"))
                )
                category = result.scalars().first()
                
                # Получаем бренд
                result = await session.execute(
                    select(models.Brand).where(models.Brand.name == prod_data.get("brand", "Unknown"))
                )
                brand = result.scalars().first()
                
                db_product = models.Product(
                    sku=prod_data["sku"],
                    title=prod_data["name"],
                    description=prod_data.get("description", ""),
                    price=prod_data["price"],
                    brand_id=brand.id if brand else None,
                    category_id=category.id if category else None
                )
                session.add(db_product)
                await session.flush()
                
                # Добавляем отзывы
                for review in prod_data.get("reviews", []):
                    review_obj = models.Review(
                        product_id=db_product.id,
                        rating=review.get("rating", 0),
                        comment=review.get("comment", ""),
                        reviewer_name=review.get("author", "")
                    )
                    session.add(review_obj)
        
        await session.commit()
    
    print(f"✅ Загружено {len(products_data['products'])} товаров с Wildberries!")
