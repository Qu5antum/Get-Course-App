from fastapi import HTTPException, status
from sqlalchemy import select, exists, func
from sqlalchemy.orm import selectinload
from backend.src.database.db import AsyncSession
from backend.src.database.models import User, Lesson, UserCourses, UserLessonProgress, Section


async def mark_lesson_completed(
        session: AsyncSession,
        lesson_id: int,
        user: User
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
            detail="Ders bulunamadı."
        )
    
    is_enrolled = await session.scalar(
        select(
            exists().where(
                (UserCourses.user_id == user.id) &
                (UserCourses.course_id == lesson.section.course_id)
            )
        )
    )

    if not is_enrolled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kursa kayıtlı değilsiniz."
        )
    

    exists_progress = await session.get(
        UserLessonProgress,
        (user.id, lesson_id)
    )

    if exists_progress:
        return {"detail": "Ders zaten tamamlandı."}
    
    progress = UserLessonProgress(
        user_id=user.id,
        lesson_id=lesson_id
    )

    session.add(progress)
    await session.commit()

    return {"detail": "Ders tamamlandı olarak işaretlendi."}



async def user_course_progress(
        session: AsyncSession,
        course_id: int,
        user: User
):
    total = await session.scalar(
        select(func.count(Lesson.id))
        .join(Section)
        .where(Section.course_id == course_id)
    )

    completed = await session.scalar(
        select(func.count(UserLessonProgress.lesson_id))
        .join(Lesson)
        .join(Section)
        .where(
            Section.course_id == course_id,
            UserLessonProgress.user_id == user.id
        )
    )

    return {
        "completed": completed,
        "total": total,
        "percent": round((completed / total) * 100, 2) if total else 0
    }