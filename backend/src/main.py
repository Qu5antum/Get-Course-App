from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.core.config import settings
from backend.src.database.db import init_models
from backend.src.api.routes.user_route import router as user_route
from backend.src.api.routes.create_course_route import router as create_course_route
from backend.src.api.routes.get_course_route import router as course_route
from backend.src.api.routes.review_route import router as review_route
from backend.src.api.routes.course_progress import router as progress_route
import asyncio
import uvicorn


app = FastAPI(
    title = settings.app_name,
    debug=settings.debug,
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors_origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


app.include_router(user_route)
app.include_router(course_route)
app.include_router(progress_route)
app.include_router(review_route)
app.include_router(create_course_route)


if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run(
        "backend.src.main:app", host="127.0.0.1", port=8000, reload=True
)