from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.proxy import router


app = FastAPI(title="API Gateway")

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"])

@app.get("/health")
async def health():
    return {"status": "OK"}

app.include_router(router)