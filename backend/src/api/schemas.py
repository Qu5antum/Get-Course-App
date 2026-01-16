from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class CourseCreate(BaseModel):
    title: str = Field(min_length=5, max_length=75)
    description: str = Field(min_length=10)
    image_url: str | None = None


class SectionCreate(BaseModel):
    title: str


class LessonCreate(BaseModel):
    description: str


class CourseOut(BaseModel):
    id: int
    title: str
    description: str
    image_url: str | None

    class Config:
        from_attributes = True