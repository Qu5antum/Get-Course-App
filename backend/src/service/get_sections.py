from fastapi import HTTPException, status
from backend.src.database.db import AsyncSession
from backend.src.database.models import Section, Course, UserCourses, User
from sqlalchemy import select, exists
from sqlalchemy.orm import selectinload


async def get_section_by_course(
        session: AsyncSession,
        course_id: int,
        user: User
): 
    course = await session.get(Course, course_id)

    if not course: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kurs bulunamadı."
        )
    
    is_enrolled = await session.scalar(
        select(
            exists().where(
                (UserCourses.user_id == user.id) &
                (UserCourses.course_id == course_id)
            )
        )
    )

    if not is_enrolled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kursa kayıtlı değilseniz bölümleri göremezsiniz."
        )
    
    result = await session.execute(
        select(Section)
        .where(Section.course_id == course_id)
        .order_by(Section.id)
    )

    return result.scalars().all()


    
    

    

    


    

    
