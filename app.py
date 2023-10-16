"""
App
"""

from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException

from database import get_db
from models import Todo

app = FastAPI()


DBDependency = Annotated[Session, Depends(get_db)]


@app.get("/healthcheck")
async def health_check():
    """
    Health Check
    """
    return {"status": "OK", "message": "Up & Running!"}


@app.get("/todos")
async def get_todos(db: DBDependency):
    """
    Get Todos
    """
    return db.query(Todo).all()


@app.get("/todos/{todo_id}")
async def get_todo_by_id(db: DBDependency, todo_id: int):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is not None:
        return JSONResponse(status_code=200, content=jsonable_encoder(todo))
    else:
        raise HTTPException(
            status_code=404, detail={"error": f"Todo with {todo_id} not found"}
        )
