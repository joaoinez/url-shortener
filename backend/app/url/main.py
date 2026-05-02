from fastapi import APIRouter

from app.url import generate, redirect

url_router = APIRouter(tags=["URL"])

url_router.include_router(generate.router)
url_router.include_router(redirect.router)
