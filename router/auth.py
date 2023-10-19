from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette import status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate
from database import get_db

router = APIRouter()

bcrypt = CryptContext(schemes=["bcrypt"])

DBDependency = Annotated[Session, Depends(get_db)]


@router.get("/auth")
async def get_user():
    """
    Auth User
    """
    return {"user": "authenticated"}


@router.post("/users")
async def create_user(new_user: UserCreate, db: DBDependency):
    """
    Create user
    """
    user = User(
        username=new_user.username,
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        role=new_user.role,
        is_active=True,
        hashed_password=bcrypt.hash(new_user.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"status": "Success"}
    )
