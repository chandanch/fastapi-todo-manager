"""
Todo Routes
"""

from typing import Annotated
from fastapi import Depends, APIRouter, Path, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Todo
from schemas import TodoCreate
from .auth import get_user_info


router = APIRouter(tags=["Todos API"])

DBDependency = Annotated[Session, Depends(get_db)]

UserInfoDependency = Annotated[dict, Depends(get_user_info)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_todos(user: UserInfoDependency, db: DBDependency):
    """
    Get Todos
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "Authentication Failed"},
        )
    return db.query(Todo).filter(Todo.owner_id == user.get("id")).all()


@router.get("/todos/{todo_id}")
async def get_todo_by_id(
    user: UserInfoDependency, db: DBDependency, todo_id: int = Path(gt=0)
):
    """
    Get Todo By ID
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "Authentication Failed"},
        )
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .filter(Todo.owner_id == user.get("id"))
        .first()
    )
    if todo is not None:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=jsonable_encoder(todo)
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": f"Todo with {todo_id} not found"},
    )


@router.post("/todos")
async def create_todo(
    user: UserInfoDependency, db: DBDependency, todo_request: TodoCreate
):
    """
    Create todo item
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "Authentication Failed"},
        )
    print(user)
    todo = Todo(**todo_request.model_dump(), owner_id=user.get("id"))

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return JSONResponse(
        status_code=201,
        content=jsonable_encoder(todo),
    )


@router.put("/todos/{todo_id}")
async def update_todo(
    user: UserInfoDependency,
    db: DBDependency,
    todo_request: TodoCreate,
    todo_id: int = Path(gt=0),
):
    """
    Update todo item
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "Authentication Failed"},
        )
    # get todo by id
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .filter(Todo.owner_id == user.get("id"))
        .first()
    )

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Todo with {todo_id} not found"},
        )

    # Update data
    todo.description = todo_request.description
    todo.title = todo_request.title
    todo.priority = todo_request.priority
    todo.is_complete = todo_request.is_complete

    db.add(todo)
    db.commit()

    return JSONResponse(status_code=200, content={"status": "Updated Todo"})


@router.delete("/todos/{todo_id}")
async def delete_todo(
    user: UserInfoDependency, db: DBDependency, todo_id: int = Path(gt=0)
):
    """
    Delete todo item
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "Authentication Failed"},
        )
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .filter(Todo.owner_id == user.get("id"))
        .first()
    )

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Todo with {todo_id} not found"},
        )

    db.query(Todo).filter(Todo.id == todo_id).filter(
        Todo.owner_id == user.get("id")
    ).delete()
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"status": "Deleted Successfully"}
    )
