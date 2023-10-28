from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database import get_db
from sqlalchemy.orm import Session

from .auth import get_user_info, authorize_request
from models import Todo

router = APIRouter(prefix="/auth", tags=["Admin API"])


UserInfoDependency = Annotated[dict, Depends(get_user_info)]

AuthorizeUserDependency = Annotated[bool, Depends(authorize_request)]

DBDependency = Annotated[Session, Depends(get_db)]


@router.get("/todos")
async def get_todos_admin(
    user: UserInfoDependency, aut: AuthorizeUserDependency, db: DBDependency
):
    print(user, aut)
    todos = db.query(Todo).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(todos))
