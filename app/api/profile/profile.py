from fastapi import APIRouter

from app.api.profile import courses, solutions


router = APIRouter()

router.include_router(courses.router, prefix='/courses')
router.include_router(solutions.router, prefix='/solutions')