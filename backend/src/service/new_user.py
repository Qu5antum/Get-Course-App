from backend.src.database.db import AsyncSession
from backend.src.api.schemas import UserCreate
from backend.src.database.models import User
from fastapi import HTTPException, status
from sqlalchemy import select


async def register_user(
        session: AsyncSession,
        user_create: UserCreate
):
    result = await session.execute(
        select(User)
        .where(User.username == user_create.username)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kullanıcı adı zaten mevcut."
        )
    
    new_user = User(
        username = user_create.username,
        email = user_create.email,
        password = user_create.password
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {"message": "Kayıt başarılı."}





    
    