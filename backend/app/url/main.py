from fastapi import APIRouter

from app.url import generate_url, redirect

url_router = APIRouter(tags=["URL"])

url_router.include_router(generate_url.router)
url_router.include_router(redirect.router)
