from fastapi import FastAPI
from src.api.endpoints import router as api_router

app = FastAPI(title="SimpliRoute Micro-Engine", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
