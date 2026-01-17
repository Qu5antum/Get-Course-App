from fastapi import HTTPException, status
from sqlalchemy import select, exists
from backend.src.database.db import AsyncSession
from backend.src.database.models import User, Course, Review, UserCourses

async def new_review_by_user(
        session: AsyncSession,
        course_id: int,
        data: str,
        user: User
):
    result = await session.execute(
        select(Course)
        .where(Course.id == course_id)
    )
    
    course = result.scalar_one_or_none()

    if not course: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kurs bulunamadı."
        )
    
    if course.author_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kursun yazarı sizsiniz, onu değerlendiremezsiniz."
        )

    is_enrolled = await session.scalar(
        select(
            exists().where(
                (UserCourses.user_id == user.id) &
                (UserCourses.course_id == course.id)
            )
        )
    )

    if not is_enrolled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kursa kayıtlı değilseniz yorum yapamazsınız."
        )
    
    
    existing_review = await session.execute(
        select(Review)
        .where(
            Review.user_id == user.id,
            Review.course_id == course_id
        )
    )

    if existing_review.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu kurs için zaten bir yorum yaptınız."
        )
    
    new_review = Review(
        comment=data.comment,
        rate=data.rate,
        user=user,
        course=course
    )

    session.add(new_review)
    await session.commit()
    await session.refresh(new_review)

    return {"detail": "Yorum eklendi."}

