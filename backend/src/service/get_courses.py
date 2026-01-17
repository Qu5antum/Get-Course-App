from backend.src.database.db import AsyncSession
from sqlalchemy import select
from backend.src.database.models import Course, User, UserCourses
from fastapi import HTTPException, status



async def search_course_by_title(
        session: AsyncSession,
        title: str
):
    if title:
        result = await session.execute(
            select(Course)
            .where(Course.title.ilike(f"%{title}%"))
            .order_by(Course.title)
            .limit(20)
        )
    else:
        result = await session.execute(
            select(Course)
        )

    return result.scalars().all()



async def add_course_by_user(
        session: AsyncSession,
        course_id: int,
        user: User
):
    existing_course = await session.get(Course, course_id)

    if not existing_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kurs bulunamadı."
        )
    
    result = await session.execute(
        select(UserCourses)
        .where(
            UserCourses.user_id == user.id,
            UserCourses.course_id == course_id
        )
    )

    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kursa zaten kayıtlısınız."
        )
    
    enrollment = UserCourses(
        user_id=user.id,
        course_id=course_id,
    )

    session.add(enrollment)
    await session.commit()

    return {"detail": "Kursa başarıyla kayıt oldunuz."}



async def user_courses(
        session: AsyncSession,
        user: User
):
    result = await session.execute(
        select(Course)
        .join(UserCourses, UserCourses.course_id == Course.id)
        .where(UserCourses.user_id == user.id)
    )

    return result.scalars().all()

