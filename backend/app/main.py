"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import problems, submissions, health

app = FastAPI(
    title="Linear Algebra Interactive Book API",
    description="Backend for interactive problem solving and solution verification",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(problems.router, prefix="/api/v1", tags=["problems"])
app.include_router(submissions.router, prefix="/api/v1", tags=["submissions"])

@app.get("/")
async def root():
    return {
        "message": "Linear Algebra Interactive Book API",
        "version": "0.1.0",
        "docs": "/docs"
    }
