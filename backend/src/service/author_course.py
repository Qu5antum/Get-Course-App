from backend.src.database.db import AsyncSession
from backend.src.database.models import Course, Section, Lesson
from fastapi import HTTPException, status
from backend.src.database.models import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def create_new_course(
        session: AsyncSession,
        author: str,
        create_course: str,
):
    course = Course(
        title=create_course.title,
        description=create_course.description,
        image_url=create_course.image_url,
        author=author
    )

    session.add(course)
    await session.commit()
    await session.refresh(course)

    return course


async def create_new_section_by_course(
        session: AsyncSession,
        course_id: int,
        create_section: str,
        author: User
):
    course = await session.get(Course, course_id)

    if not course: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kurs bulanamdı."
        )
    
    if course.author_id != author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yasaklı."
        )
    
    section = Section(
        title=create_section.title,
        course=course
    )

    session.add(section)
    await session.commit()
    await session.refresh(section)

    return section


async def create_new_lesson_by_section(
        session: AsyncSession,
        section_id: int,
        create_lesson: str,
        author: str
):
    result = await session.execute(
        select(Section)
        .options(selectinload(Section.course))
        .where(Section.id == section_id)
    )
    section = result.scalar_one_or_none()

    if not section: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bölüm bulanamadı."
        )
    
    course = section.course
    
    if course.author_id != author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yasaklı."
        )
    
    lesson = Lesson(
        description=create_lesson.description,
        section=section, 
    )

    session.add(lesson)
    await session.commit()
    await session.refresh(lesson)

    return lesson





