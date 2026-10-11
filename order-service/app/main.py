from fastapi import FastAPI
from app.api.endpoints import router


app = FastAPI(title="Order service")


@app.get("/health")
async def health_check():
    return {"msg": "OK"}


app.include_router(router)