from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import uvicorn
import psutil
import os
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
import time
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator:
    redis = aioredis.from_url(os.getenv("REDIS_URL"))
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)

ret = 0
@cache(namespace="test", expire=1)
async def get_ret():
    global ret
    ret = ret + 1
    return ret


@app.get("/index")
@cache(namespace="test", expire=10)
async def index():
    time.sleep(5)
    return {"ret": await get_ret()}

@cache()
async def get_cache():
    return 1


@app.get("/")
@cache(expire=60)
async def index():
    time.sleep(10)
    return dict(hello="world")

if __name__ == "__main__":
    
    print(psutil.cpu_count(logical=False))
    uvicorn.run(
        app="reara:app", 
        host=os.getenv("APP_HOST"), 
        port=int(os.getenv("APP_PORT")),
        workers=psutil.cpu_count(logical=False)
    )