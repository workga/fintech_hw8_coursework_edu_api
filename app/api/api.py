from fastapi import APIRouter

from app.api.admin import admin
from app.api.auth import auth
from app.api.courses import courses
from app.api.profile import profile


api_router = APIRouter()

api_router.include_router(admin.router, prefix='/admin')
api_router.include_router(auth.router, prefix='/auth')
api_router.include_router(courses.router, prefix='/courses')
api_router.include_router(profile.router, prefix='/profile')
