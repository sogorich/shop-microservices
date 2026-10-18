from fastapi import FastAPI
from aiokafka import AIOKafkaProducer
from contextlib import asynccontextmanager

from app.api.endpoints import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092',
        enable_idempotence=True
    )
    
    await producer.start()

    print("[x] Продюсер запущен", flush=True)
    app.state.kafka_producer = producer

    yield

    await producer.stop()


app = FastAPI(
    title="Order service",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"msg": "OK"}


app.include_router(router)