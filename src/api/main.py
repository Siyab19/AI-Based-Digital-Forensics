
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routes.statistics import router as statistics_router

from fastapi.middleware.cors import CORSMiddleware

from src.api.database import (
    connect_to_neo4j,
    close_neo4j_connection
)
from src.api.routes.investigations import router as investigations_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the Neo4j connection during the API lifecycle."""

    connect_to_neo4j()

    yield

    close_neo4j_connection()


app = FastAPI(
    title="AI-Based Digital Forensics API",
    description=(
        "Backend API for digital forensic evidence "
        "correlation and investigation."
    ),
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(investigations_router)
app.include_router(statistics_router)


@app.get("/")
def root():
    return {
        "message": "AI-Based Digital Forensics API is running!",
        "status": "active"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }
