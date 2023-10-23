"""
Pydantic Schemas
"""

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    """
    Create Todo Request Schema
    """

    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    is_complete: bool


class UserCreate(BaseModel):
    """
    Create User Request Schema
    """

    username: str = Field(min_length=3)
    email: str
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    password: str
    role: str = Field(min_length=3)


class AuthResponse(BaseModel):
    """
    Auth Response Schema
    """

    access_token: str
    token_type: str
