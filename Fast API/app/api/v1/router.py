from fastapi import APIRouter, Depends

from app.api.v1.endpoints import user


api_router = APIRouter()
api_router.include_router(user.router, prefix="/public", tags=["Public"])
