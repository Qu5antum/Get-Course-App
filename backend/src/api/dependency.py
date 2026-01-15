from fastapi import Depends, HTTPException, status
from backend.src.database.db import get_session, AsyncSession
from sqlalchemy import select
from backend.src.database.models import User
from backend.src.core.jwt_token import get_user_from_token


async def get_current_user(
        user_id: int = Depends(get_user_from_token),
        session : AsyncSession = Depends(get_session)
)-> User:
    user = await session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Kullanıcı bulunamadı."
        )
    return user