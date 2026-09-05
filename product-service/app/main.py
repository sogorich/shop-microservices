from fastapi import FastAPI
from config import settings

from api.endpoints import router


app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
    summary=settings.summary,
)


@app.get("/health", tags=["Проверка состояния"])
async def health():
    return {"message": "Microservice \"product-service\" is ready!"}


app.include_router(router)