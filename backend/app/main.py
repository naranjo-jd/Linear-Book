"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import problems, submissions, health

app = FastAPI(
    title="Linear Algebra Interactive Book API",
    description="Backend for interactive problem solving and solution verification",
    version="0.1.0"
)

# CORS — en desarrollo se permiten todos los orígenes locales.
# En producción reemplazar con el dominio real, ej. ["https://mi-sitio.com"].
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
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
