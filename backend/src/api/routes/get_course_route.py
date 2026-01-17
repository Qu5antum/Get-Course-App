from backend.src.database.db import AsyncSession, get_session
from fastapi import Depends, APIRouter, status
from backend.src.api.dependency import get_current_user
from backend.src.database.models import User
from backend.src.service.get_courses import add_course_by_user,search_course_by_title, user_courses
from backend.src.api.schemas import CourseOut


router = APIRouter(
    prefix="/courses",
    tags=["get_courses"]
)


@router.post("/{courses_id}/enroll", status_code=status.HTTP_201_CREATED)
async def add_course(
    course_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await add_course_by_user(session=session, course_id=course_id, user=user)



@router.get("/search", response_model=list[CourseOut], status_code=status.HTTP_201_CREATED)
async def search_course(
    title: str | None = None,
    session: AsyncSession = Depends(get_session)
):
    return await search_course_by_title(session=session, title=title)


@router.get("/user_courses", response_model=list[CourseOut], status_code=status.HTTP_201_CREATED)
async def get_user_courses(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await user_courses(session=session, user=user)
    
