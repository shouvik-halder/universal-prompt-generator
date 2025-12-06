from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.api import router
from src.db import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="Generation Service",
    description="Prompt generation service with platform-specific adapters",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.get("/")
async def root():
    return {
        "service": settings.service_name,
        "status": "running",
        "endpoints": ["/generate", "/platforms", "/intents", "/health", "/ready"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)