from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base, db_engine


class User(Base):
    """
    User Table
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String, nullable=True)


class Todo(Base):
    """
    Class for todos
    """

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    is_complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String, nullable=True)
    todo_type = Column(String, nullable=True)


# create database and tables
Base.metadata.create_all(db_engine)
