from fastapi import APIRouter, status, Depends
from backend.src.database.db import AsyncSession, get_session
from backend.src.api.dependency import get_current_user
from backend.src.service.course import create_new_course, update_course_by_course_id
from backend.src.service.section import create_new_section_by_course, update_section_by_section_id
from backend.src.service.lesson import create_new_lesson_by_section
from backend.src.api.schemas import CourseCreate, SectionCreate, LessonCreate, CourseUpdate
from backend.src.database.models import User


router = APIRouter(
    prefix="/new_course",
    tags=["new_courses"]
)


@router.post("/courses", status_code=status.HTTP_201_CREATED)
async def create_course(
    data: CourseCreate,
    author: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await create_new_course(
        session=session, 
        author=author, 
        data=data
    )


@router.post("/courses/{course_id}", status_code=status.HTTP_201_CREATED)
async def update_course(
    course_id: int,
    data: CourseUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await update_course_by_course_id(session=session, course_id=course_id, data=data, author=user)


@router.post("/courses/{course_id}/sections", status_code=status.HTTP_201_CREATED)
async def create_section(
    course_id: int,
    data: SectionCreate,
    author: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await create_new_section_by_course(
        session=session, 
        course_id=course_id, 
        data=data, 
        author=author
    )


@router.post("/sections/{section_id}/lessons", status_code=status.HTTP_201_CREATED)
async def create_lesson(
    section_id: int,
    data: LessonCreate,
    author: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await create_new_lesson_by_section(
        session=session,
        section_id=section_id,
        data=data,
        author=author
    )


    