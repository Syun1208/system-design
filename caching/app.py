from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import uvicorn
import psutil
import os
import time

from celery_worker import check_prime, celery_app
from dotenv import load_dotenv
from redis import Redis
from redis.lock import Lock as RedisLock

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:
    redis_instance = Redis.from_url(os.getenv("REDIS_URL"))
    response = redis_instance.ping()
    if response:
        print("Connected to Redis!")
    app.state.redis_instance =redis_instance
    yield
    redis_instance.close()

app = FastAPI(
    title='Sytem Design [Series 1]: Caching',
    lifespan=lifespan
)  


@app.post('/prime')
async def prime(request: Request) -> JSONResponse:
  
    request_data = await request.json()
    task_id = request_data["task_id"]
    print(task_id)
    time_execution = app.state.redis_instance.get(task_id)
    if time_execution is None or celery_app.AsyncResult(time_execution).ready():

        # task = check_prime.delay(request_data["time_delay"])
        time.sleep(request_data["time_delay"])
        time_execution = 424525
        app.state.redis_instance.set(task_id, time_execution)
        return JSONResponse(
            content=jsonable_encoder({
                "task_id": task_id,
                "time_execution": time_execution
            })
        )
    else:
        return JSONResponse(
            content=jsonable_encoder({
                "task_id": task_id,
                "time_execution": time_execution
            })
        )



if __name__ == "__main__":
    
    print(psutil.cpu_count(logical=False))
    uvicorn.run(
        app="app:app", 
        host=os.getenv("APP_HOST"), 
        port=int(os.getenv("APP_PORT")),
        workers=psutil.cpu_count(logical=False)
    )