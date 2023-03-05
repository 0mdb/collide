from fastapi import APIRouter

from app.api.api_v1.endpoints import forcegraph

api_router = APIRouter()

api_router.include_router(forcegraph.router, prefix="/forcegraph", tags=["forcegraph"])

