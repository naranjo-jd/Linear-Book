#!/usr/bin/env python
"""Run the FastAPI application."""

import uvicorn
from app.config import settings
from app.db import init_db

if __name__ == "__main__":
    init_db()
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
