from fastapi import FastAPI

from app.database.config import TORTOISE_ORM
from app.api.endpoints import router

from tortoise.contrib.fastapi import register_tortoise


app = FastAPI(title="Deal Service")


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

