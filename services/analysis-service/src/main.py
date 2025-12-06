from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.api import router

app = FastAPI(
    title="Analysis Service",
    description="NLU service for intent classification, entity extraction, and assumption generation",
    version="1.0.0",
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
        "endpoints": ["/analyze", "/health", "/ready"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)