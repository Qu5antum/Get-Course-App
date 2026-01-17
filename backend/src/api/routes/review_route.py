from fastapi import APIRouter, status, Depends
from backend.src.database.db import AsyncSession, get_session
from backend.src.api.dependency import get_current_user
from backend.src.service.review import new_review_by_user
from backend.src.api.schemas import ReviewCreate
from backend.src.database.models import User


router = APIRouter(
    prefix="/review",
    tags=["reviews"]
)


@router.post("/", status_code=status.HTTP_200_OK)
async def new_review(
    course_id: int,
    data: ReviewCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await new_review_by_user(
        session=session,
        course_id=course_id,
        data=data,
        user=user
    )