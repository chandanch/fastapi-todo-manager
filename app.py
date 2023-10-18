"""
App
"""
from typing import Annotated

from fastapi import Depends, FastAPI, Path, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException
from sqlalchemy.orm import Session


from database import get_db
from models import Todo
from schemas import TodoCreate


app = FastAPI()


DBDependency = Annotated[Session, Depends(get_db)]


@app.get("/healthcheck")
async def health_check():
    """
    Health Check
    """
    return {"status": "OK", "message": "Up & Running!"}


@app.get("/todos", status_code=status.HTTP_200_OK)
async def get_todos(db: DBDependency):
    """
    Get Todos
    """
    return db.query(Todo).all()


@app.get("/todos/{todo_id}")
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


@app.post("/todos")
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


@app.put("/todos/{todo_id}")
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
