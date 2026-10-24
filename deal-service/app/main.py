import asyncio
import json

from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
from vkbottle import API

from app.config import settings
from app.database.config import TORTOISE_ORM
from app.api.endpoints import router
from app.utils.services import send_vk_notification_employes

from contextlib import asynccontextmanager
from tortoise.contrib.fastapi import register_tortoise


@asynccontextmanager
async def lifespan(_: FastAPI):
    vk_api = API(token=settings.vk_token)
    kafka_task = asyncio.create_task(kafka_start(vk_api))

    yield

    kafka_task.cancel()
    try:
        await kafka_task
    except asyncio.CancelledError:
        print("[x] kafka_task failed!")


async def kafka_start(vk_api: API):

    consumer = AIOKafkaConsumer("orders.created",
        bootstrap_servers='kafka:9092',
        auto_offset_reset="earliest",
        group_id="orders",
        retry_backoff_ms=1000,
        request_timeout_ms=40000,
        session_timeout_ms=45000,
        heartbeat_interval_ms=3000,
        max_poll_interval_ms=300000,
        metadata_max_age_ms=30000,
        enable_auto_commit=False)

    try:
        await consumer.start()
        
        async for msg in consumer:
            print("[!] Consumed: ", msg.topic, msg.offset, msg.partition, msg.value, msg.timestamp, flush=True)

            data = json.loads(msg.value) # type: ignore

            template = f"🛒 Номер заказа: {data["id"]}\n🆔 ID пользователя: {data["payload"]["user_id"]}\n📦 Состав заказа:\n" + "\n".join([f"- 🛍️ {i["product_title"]}, 💰 {i["product_price"]}" for i in data["products"]])
        
            await send_vk_notification_employes(vk_api, template.strip())
            await consumer.commit()

    except Exception as e:
        print("[Deal-Service | Consumer]: ", e)
        await asyncio.sleep(5) 

    finally:
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