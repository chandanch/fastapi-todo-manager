"""
Healthcheck routes
"""

from fastapi import APIRouter

router = APIRouter(tags=["Ping API"])


@router.get("/healthcheck")
async def health_check():
    """
    Health Check
    """
    return {"status": "OK", "message": "Up & Running!"}
