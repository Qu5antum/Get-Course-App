from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.src.database.db import Base
from sqlalchemy import ForeignKey, DateTime, func
from datetime import datetime



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    courses: Mapped[list["Course"]] = relationship(
        secondary="user_courses",
        back_populates="users"
    )

    created_courses: Mapped[list["Course"]] = relationship(
        back_populates="author"
    )
    
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )



class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    image_url: Mapped[str | None] = mapped_column(
        nullable=True
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
    )

    author: Mapped["User"] = relationship(
        back_populates="created_courses"
    )

    users: Mapped[list["User"]] = relationship(
        secondary="user_courses",
        back_populates="courses"
    )

    sections: Mapped[list["Section"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan"
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan"
    )



class UserCourses(Base):
    __tablename__ = "user_courses"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'), primary_key=True)

    completed: Mapped[bool] = mapped_column(default=False)
    
    completed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
    )



class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    comment: Mapped[str] = mapped_column(nullable=False) 
    rate: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))

    user: Mapped["User"] = relationship(back_populates="reviews")
    course: Mapped["Course"] = relationship(back_populates="reviews")


class Section(Base):
    __tablename__ = "sections"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    title: Mapped[str] = mapped_column(nullable=False)

    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="sections")

    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan"
    )


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)

    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id"))
    section: Mapped["Section"] = relationship(back_populates="lessons")
