from fastapi import HTTPException, status
from backend.src.database.db import AsyncSession
from backend.src.database.models import Section, UserCourses, User, Lesson
from sqlalchemy import select, exists
from sqlalchemy.orm import selectinload


async def get_lessons_by_section(
        session: AsyncSession,
        section_id: int,
        user: User
):
    result = await session.execute(
        select(Section).where(Section.id == section_id)
    )

    section = result.scalar_one_or_none()

    if not section: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bölüm bulunamadı."
        )
    
    is_enrolled = await session.scalar(
        select(
            exists().where(
                (UserCourses.user_id == user.id) &
                (UserCourses.course_id == section.course_id)
            )
        )
    )

    if not is_enrolled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kursa kayıtlı değilseniz bölümleri göremezsiniz."
        )
    
    result = await session.execute(
        select(Lesson)
        .where(Lesson.section_id == section_id)
        .order_by(Lesson.position)
    )

    return result.scalars().all()
