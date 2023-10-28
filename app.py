"""
App
"""
from fastapi import FastAPI
from dotenv import load_dotenv

from router import auth, healthcheck, todo, admin

load_dotenv()


app = FastAPI(
    title="Todo Manager",
    description="Todo API helps you manage awesome todos. 🚀",
    version="1.1.0",
    contact={"name": "chandanch"},
    summary="Manage Todos Easily",
)


app.include_router(router=auth.router)
app.include_router(router=healthcheck.router)
app.include_router(router=todo.router)
app.include_router(router=admin.router)
