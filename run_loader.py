import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.services.dummyjson_loader import load_data_to_db


if __name__ == "__main__":
    print("Starting data loading from DummyJSON...")
    asyncio.run(load_data_to_db())
    print("Data loading completed!")
