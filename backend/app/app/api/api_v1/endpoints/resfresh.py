from typing import Any, List
from fastapi import APIRouter, Depends, Response
from app.core.users import auth_backend, get_jwt_strategy, JWTStrategy, fastapi_users

router = APIRouter()


@router.post("/jwt/refresh", tags=["auth"])
async def refresh_jwt(
    response: Response,
    jwt_strategy: JWTStrategy = Depends(get_jwt_strategy),
    user=Depends(fastapi_users.current_user(active=True)),
):
    return await auth_backend.login(jwt_strategy, user, response)
