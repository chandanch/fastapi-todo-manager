from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from starlette import status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate
from database import get_db

router = APIRouter()

bcrypt = CryptContext(schemes=["bcrypt"])

DBDependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt.verify(password, user.hashed_password):
        return False
    else:
        return True


@router.post("/auth")
async def authenticate(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DBDependency
):
    """
    Auth User
    """
    is_valid_user = authenticate_user(form_data.username, form_data.password, db)

    if is_valid_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"status": "Success"}
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "invalid credentials"},
        )

    return {"user": form_data}


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
