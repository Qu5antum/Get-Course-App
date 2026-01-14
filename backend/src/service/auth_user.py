from backend.src.database.db import AsyncSession
from backend.src.api.schemas import UserCreate
from backend.src.database.models import User
from fastapi import HTTPException, status
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from backend.src.core.jwt_token import create_jwt_token


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


async def auth_user(credents: OAuth2PasswordRequestForm, session: AsyncSession):
    result = await session.execute(
        select(User)
        .where(User.username == credents.username)
    )

    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kullanıcı bulunamadı."
        )
    
    if user.password != credents.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yanlış şifre."
        )
    
    token = await create_jwt_token({"sub": str(user.id)})
    return {"access_token": token,
            "token_type": "bearer"}




    
    