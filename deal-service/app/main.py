from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer

from app.database.config import TORTOISE_ORM
from app.api.endpoints import router

from contextlib import asynccontextmanager
from tortoise.contrib.fastapi import register_tortoise


@asynccontextmanager
async def lifespan(app: FastAPI):

    consumer = AIOKafkaConsumer("order.created",
        bootstrap_servers='kafka:9092',
        group_id="orders",
        auto_offset_reset="earliest")

    await consumer.start()

    print("[X] Консьюмер запущен, слушаем...")
    async for msg in consumer:
        print("[!] Consumed: ", msg.topic, msg.value, flush=True)
        # тут допустим отправка уведомления сотруднику о созданном заказе

    yield

    await consumer.stop()

app = FastAPI(title="Deal Service", lifespan=lifespan)

@app.get("/health")
async def healthcheck():
    return {"message": "OK"}


app.include_router(router)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True
)