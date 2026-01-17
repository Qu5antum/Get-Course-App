from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from backend.src.database.db import AsyncSession
from backend.src.database.models import User, Section, Lesson



async def create_new_lesson_by_section(
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
            detail="Bölüm bulanamadı."
        )

    if section.course.author_id != author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yasaklı."
        )
    
    lesson = Lesson(
        description=data.description,
        position=data.position,
        section=section, 
    )

    session.add(lesson)
    await session.commit()
    await session.refresh(lesson)

    return lesson


async def update_lesson_by_lesson_id(
        session: AsyncSession,
        lesson_id: int,
        data: str,
        author: User
):
    result = await session.execute(
        select(Lesson)
        .options(
            selectinload(Lesson.section)
            .selectinload(Section.course)
        )
        .where(Lesson.id == lesson_id)
    )

    lesson = result.scalar_one_or_none()

    if not lesson: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ders bulanamadı."
        )
    
    if lesson.section.course.author_id != author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yasaklı."
        )
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(lesson, field, value)

    await session.commit()
    await session.refresh(lesson)


    return {"detail": "Değişiklikler kaydedildi."}



async def delete_lesson_by_id(
        session: AsyncSession,
        lesson_id: int,
        author: User
):
    result = await session.execute(
        select(Lesson)
        .options(
            selectinload(Lesson.section)
            .selectinload(Section.course)
        )
        .where(Lesson.id == lesson_id)
    )

    lesson = result.scalar_one_or_none()

    if not lesson: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ders bulanamadı."
        )
    
    if lesson.section.course.author_id != author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yasaklı."
        )
    
    await session.delete(lesson)
    await session.commit()

    return {"detail": "Ders başarıyla silindi."}
    

    