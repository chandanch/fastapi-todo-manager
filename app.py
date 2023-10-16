"""
App
"""

from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

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
