from fastapi import APIRouter
from .assessment.endpoint import router as assessment_router


central_router = APIRouter()
central_router.include_router(router=assessment_router)


