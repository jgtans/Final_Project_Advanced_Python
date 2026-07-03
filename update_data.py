import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.services.wildberries_loader import load_data_to_db


if __name__ == "__main__":
    print("🚀 Начинаем асинхронную загрузку данных с Wildberries...")
    asyncio.run(load_data_to_db())
    print("✅ Данные успешно загружены и сохранены в БД!")
