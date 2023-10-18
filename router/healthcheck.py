from fastapi import APIRouter

router = APIRouter()


@router.get("/healthcheck")
async def health_check():
    """
    Health Check
    """
    return {"status": "OK", "message": "Up & Running!"}
