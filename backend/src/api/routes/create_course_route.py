from fastapi import APIRouter, status, Depends
from backend.src.database.db import AsyncSession, get_session
from backend.src.api.dependency import get_current_user
from backend.src.service.course import create_new_course, update_course_by_course_id, delete_course_by_id
from backend.src.service.section import create_new_section_by_course, update_section_by_section_id, delete_section_by_id
from backend.src.service.lesson import create_new_lesson_by_section, update_lesson_by_lesson_id, delete_lesson_by_id
from backend.src.api.schemas import CourseCreate, SectionCreate, LessonCreate, CourseUpdate, SectionUpdate, LessonUpdate
from backend.src.database.models import User


router = APIRouter(
    prefix="/new_course",
    tags=["new_courses"]
)


@router.post("/courses", status_code=status.HTTP_201_CREATED)
async def create_course(
    title: str,
    description: str,
    image_url: str | None = None,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await create_new_course(
        session=session, 
        author=user, 
        title=title,
        description=description,
        image_url=image_url
    )


@router.put("/courses/{course_id}", status_code=status.HTTP_200_OK)
async def update_course(
    course_id: int,
    data: CourseUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await update_course_by_course_id(session=session, course_id=course_id, data=data, author=user)


@router.delete("/courses/{course_id}", status_code=status.HTTP_200_OK)
async def delete_course(
    course_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await delete_course_by_id(session=session, course_id=course_id, author=user)


@router.post("/courses/{course_id}/sections", status_code=status.HTTP_201_CREATED)
async def create_section(
    course_id: int,
    data: SectionCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await create_new_section_by_course(
        session=session, 
        course_id=course_id, 
        data=data, 
        author=user
    )


@router.put("/sections/{section_id}", status_code=status.HTTP_200_OK)
async def update_section(
    section_id: int,
    data: SectionUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await update_section_by_section_id(session=session, section_id=section_id, data=data, author=user)


@router.delete("/sections/{section_id}", status_code=status.HTTP_200_OK)
async def delete_section(
    section_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await delete_section_by_id(session=session, section_id=section_id, author=user)


@router.post("/sections/{section_id}/lessons", status_code=status.HTTP_201_CREATED)
async def create_lesson(
    section_id: int,
    data: LessonCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await create_new_lesson_by_section(
        session=session,
        section_id=section_id,
        data=data,
        author=user
    )

@router.put("/lessons/{lesson_id}", status_code=status.HTTP_200_OK)
async def update_lesson(
    lesson_id: int,
    data: LessonUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await update_lesson_by_lesson_id(session=session, lesson_id=lesson_id, data=data, author=user)


@router.delete("/lessons/{lesson_id}", status_code=status.HTTP_200_OK)
async def delete_lesson(
    lesson_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await delete_lesson_by_id(session=session, lesson_id=lesson_id, author=user)

    