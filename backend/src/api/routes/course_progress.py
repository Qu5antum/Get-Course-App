from fastapi import APIRouter, status, Depends
from backend.src.database.db import AsyncSession, get_session
from backend.src.api.dependency import get_current_user
from backend.src.database.models import User
from backend.src.service.lesson_progress import mark_lesson_completed, user_course_progress


router = APIRouter(
    prefix="/progress",
    tags=["progresses"]
)


@router.post("/lessons/{lesson_id}/complete", status_code=status.HTTP_201_CREATED)
async def complete_lesson(
    lesson_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await mark_lesson_completed(
        session=session,
        lesson_id=lesson_id,
        user=user
    )


@router.get("/course/{course_id}/complete", status_code=status.HTTP_200_OK)
async def course_progress(
    course_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await user_course_progress(
        session=session,
        course_id=course_id,
        user=user
    )