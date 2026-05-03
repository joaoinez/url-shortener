import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies import get_settings, lifespan
from app.docs import docs_router
from app.url.main import url_router

settings = get_settings()

app = FastAPI(
    lifespan=lifespan,
    openapi_prefix="/api" if os.environ.get("APP_ENV") == "production" else "",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docs_router)
app.include_router(url_router)
