from typing import Annotated
from fastapi import Depends, APIRouter, Path, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Todo
from schemas import TodoCreate


router = APIRouter(tags=["Todos API"])

DBDependency = Annotated[Session, Depends(get_db)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_todos(db: DBDependency):
    """
    Get Todos
    """
    return db.query(Todo).all()


@router.get("/todos/{todo_id}")
async def get_todo_by_id(db: DBDependency, todo_id: int = Path(gt=0)):
    """
    Get Todo By ID
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is not None:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=jsonable_encoder(todo)
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Todo with {todo_id} not found"},
        )


@router.post("/todos")
async def create_todo(db: DBDependency, todo_request: TodoCreate):
    """
    Create todo item
    """
    todo = Todo(**todo_request.model_dump())

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return JSONResponse(
        status_code=201,
        content=jsonable_encoder(todo),
    )


@router.put("/todos/{todo_id}")
async def update_todo(
    db: DBDependency, todo_request: TodoCreate, todo_id: int = Path(gt=0)
):
    """
    Update todo item
    """
    # get todo by id
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

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
async def delete_todo(db: DBDependency, todo_id: int = Path(gt=0)):
    """
    Delete todo item
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Todo with {todo_id} not found"},
        )
    else:
        db.query(Todo).filter(Todo.id == todo_id).delete()
        db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"status": "Deleted Successfully"}
    )
