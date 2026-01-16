from fastapi import APIRouter, status, Depends
from backend.src.database.models import User
from backend.src.database.db import AsyncSession, get_session
from backend.src.service.auth_user import register_new_user, auth_user
from backend.src.api.schemas import UserCreate
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    new_user: UserCreate,
    session: AsyncSession = Depends(get_session)
): 
    return await register_new_user(session=session, user_create=new_user)


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login_user(
    credents: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    return await auth_user(credents=credents, session=session)
    
    