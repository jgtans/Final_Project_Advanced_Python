from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


def init_cache():
    # Используем in-memory кеширование для сложных запросов
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
