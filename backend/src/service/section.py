from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from backend.src.database.db import AsyncSession
from backend.src.database.models import User, Course, Section



async def create_new_section_by_course(
        session: AsyncSession,
        course_id: int,
        data: str,
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
        title=data.title,
        course=course
    )

    session.add(section)
    await session.commit()
    await session.refresh(section)

    return section



async def update_section_by_section_id(
        session: AsyncSession,
        section_id: int,
        data: str,
        author: User
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
            detail="Bölüm bulanamdı."
        )
    
    if section.course.author_id != author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yasaklı."
        )
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(section, field, value)

    await session.commit()
    await session.refresh(section)

    return {"detail": "Değişiklikler kaydedildi"}
