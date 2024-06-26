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


@app.get("/1")
async def main():
    conn_1 = await asyncpg.connect(dsn=settings.database_dsn)
    logging.info('DB connection 1 has been established')

    async with conn_1.transaction():
        await conn_1.execute("INSERT INTO values (number) VALUES (2)")
        await conn_1.execute(
            """UPDATE values
            SET number = 3
            WHERE id = 1;"""
        )
        await conn_1.execute("INSERT INTO values (number) VALUES (3)")
        await conn_1.execute(
            """UPDATE values
            SET number = 3
            WHERE id = 2;"""
        )
        await asyncio.sleep(5)
        await conn_1.execute("DELETE FROM values WHERE id = 1")
        await conn_1.execute("INSERT INTO values (number) VALUES (4)")
        await conn_1.execute(
            """UPDATE values
            SET number = 5
            WHERE id = 2;"""
        )
        
    await conn_1.close()
    logging.info('DB connection 1 closed')

    return {
        "status": "ok"
    }


@app.get("/2")
async def main():
    conn_2 = await asyncpg.connect(dsn=settings.database_dsn)
    logging.info('DB connection 2 has been established')

    async with conn_2.transaction():
        await conn_2.execute("INSERT INTO values (number) VALUES (2)")
        await conn_2.execute(
            """UPDATE values
            SET number = 3
            WHERE id = 2;"""
        )
        await conn_2.execute("INSERT INTO values (number) VALUES (5)")
        await conn_2.execute(
            """UPDATE values
            SET number = 3
            WHERE id = 1;"""
        )
        await conn_2.execute("DELETE FROM values WHERE id = 1")
        await conn_2.execute("INSERT INTO values (number) VALUES (4)")
        await conn_2.execute(
            """UPDATE values
            SET number = 5
            WHERE id = 2;"""
        )

    await conn_2.close()
    logging.info('DB connection 2 closed')

    return {
        "status": "ok"
    }
