"""
Auth Routes
"""

from typing import Annotated
from datetime import timedelta, datetime


from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from starlette import status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from models import User
from schemas import UserCreate, AuthResponse
from database import get_db

router = APIRouter()

bcrypt = CryptContext(schemes=["bcrypt"])

DBDependency = Annotated[Session, Depends(get_db)]

JWT_KEY = "weneqweqwuhu3hhu32erh3rf32fh"

JWT_SIGN_ALG = "HS256"

oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth")


def authenticate_user(username: str, password: str, db):
    """
    authenticate user and check user existence
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt.verify(password, user.hashed_password):
        return False
    else:
        return user


def generate_token(user: User, time_delta: timedelta):
    """
    Generate JWT token
    """
    token_payload = {
        "username": user.username,
        "role": user.role,
        "sub": user.username,
        "aud": "todomanager",
        "exp": datetime.utcnow() + time_delta,
    }

    return jwt.encode(
        token_payload,
        algorithm=JWT_SIGN_ALG,
        key=JWT_KEY,
    )


async def verify_token(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token, key=JWT_KEY, algorithms=[JWT_SIGN_ALG])
        username: str = payload.get("username")
        role: str = payload.get("role")

        if username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"msg": "Invalid token"},
            )
        else:
            return {"username": username, "role": role}
    except JWTError as exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "Invalid token"}
        ) from exp


@router.post("/auth", response_model=AuthResponse)
async def authenticate(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DBDependency
):
    """
    Auth User
    """
    user = authenticate_user(form_data.username, form_data.password, db)

    if user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": generate_token(user, timedelta(minutes=60)),
                "token_type": "Bearer",
            },
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"msg": "invalid credentials"},
    )


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
