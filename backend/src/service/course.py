from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from backend.src.database.db import AsyncSession
from backend.src.database.models import Course, Section, Lesson
from backend.src.database.models import User



async def create_new_course(
        session: AsyncSession,
        author: User,
        data: str,
):
    course = Course(
        title=data.title,
        description=data.description,
        image_url=data.image_url,
        author=author
    )

    session.add(course)
    await session.commit()
    await session.refresh(course)

    return course


async def update_course_by_course_id(
        session: AsyncSession,
        course_id: int,
        data: str,
        author: User,
):
    course = await session.get(Course, course_id)

    if not course: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kurs bulunamadı."
        )
    
    if course.author_id != author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yasaklı."
        )

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(course, field, value)

    await session.commit()
    await session.refresh(course)

    return {"detail": "Değişiklikler kaydedildi."}

    
    
async def delete_course_by_id(
        session: AsyncSession,
        course_id: int,
        author: User
):
    course = await session.get(Course, course_id)

    if not course: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kurs bulunamadı."
        )
    
    if course.author_id != author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yasaklı."
        )
    
    await session.delete(course)
    await session.commit()
    
    return {"detail": "Kurs başarıyla silindi."}
    

    





