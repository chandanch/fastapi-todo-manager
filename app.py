"""
App
"""

from fastapi import FastAPI
from database import db_engine
import models

app = FastAPI()

# create database and tables
models.Base.metadata.create_all(db_engine)


@app.get("/healthcheck")
async def health_check():
    """
    Health Check
    """
    return {"status": "OK", "message": "Up & Running!"}
