from fastapi import APIRouter, status, Depends
from backend.src.database.db import AsyncSession, get_session
from backend.src.api.dependency import get_current_user
from backend.src.service.author_course import create_new_course, create_new_section_by_course, create_new_lesson_by_section
from backend.src.api.schemas import CourseCreate, SectionCreate, LessonCreate
from backend.src.database.models import User


router = APIRouter(
    prefix="/new_course",
    tags=["new_courses"]
)


@router.post("/courses", status_code=status.HTTP_201_CREATED)
async def create_course(
    create_course: CourseCreate,
    author: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await create_new_course(
        session=session, 
        author=author, 
        create_course=create_course
    )


@router.post("/courses/{course_id}/sections", status_code=status.HTTP_201_CREATED)
async def create_section(
    course_id: int,
    create_section: SectionCreate,
    author: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await create_new_section_by_course(
        session=session, 
        course_id=course_id, 
        create_section=create_section, 
        author=author
    )


@router.post("/sections/{section_id}/lessons", status_code=status.HTTP_201_CREATED)
async def create_lesson(
    section_id: int,
    create_lesson: LessonCreate,
    author: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await create_new_lesson_by_section(
        session=session,
        section_id=section_id,
        create_lesson=create_lesson,
        author=author
    )


    