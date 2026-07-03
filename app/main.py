from fastapi import FastAPI
from .database import engine, Base
from .api import categories, brands, products
from .services.cache import init_cache
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Автоматическое создание таблиц, если их нет
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    init_cache()
    yield


app = FastAPI(title="Wildberries Catalog API", lifespan=lifespan)

app.include_router(categories.router, tags=["Categories"])
app.include_router(brands.router, tags=["Brands"])
app.include_router(products.router, tags=["Products"])


@app.get("/")
async def root():
    return {"message": "Welcome to Wildberries Catalog API. Visit /docs for API documentation."}
