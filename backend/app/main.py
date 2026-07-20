from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db
from app.core.logging import setup_logging
from app.routers import infrastructure, deployment, monitoring, logs, ai


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    await init_db()
    yield


app = FastAPI(
    title="Enterprise IDP",
    description="Internal Developer Platform API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(infrastructure.router)
app.include_router(deployment.router)
app.include_router(monitoring.router)
app.include_router(logs.router)
app.include_router(ai.router)


@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "enterprise-idp"}
