from fastapi import APIRouter
from models import User
from schemas import UserCreate

router = APIRouter()


@router.get("/auth")
async def get_user():
    """
    Auth User
    """
    return {"user": "authenticated"}


@router.post("/users")
async def create_user(new_user: UserCreate):
    """
    Create user
    """
    create_user_model = User(
        username=new_user.username,
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        role=new_user.role,
        is_active=True,
        hashed_password=new_user.password,
    )

    return create_user_model
