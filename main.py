import os
import asyncpg
import asyncio
import logging
from fastapi import FastAPI
from settings import Settings
from enum import Enum
from contextlib import asynccontextmanager


settings = Settings()
logging.basicConfig(format='%(asctime)s.%(msecs)03d - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def main():
    conn_1 = await asyncpg.connect(dsn=settings.database_dsn)
    logging.info('DB connection 1 has been established')

    conn_2 = await asyncpg.connect(dsn=settings.database_dsn)
    logging.info('DB connection 2 has been established')

    await conn_1.close()
    logging.info('DB connection 1 closed')

    await conn_2.close()
    logging.info('DB connection 2 closed')

    return {
        "status": "ok"
    }
