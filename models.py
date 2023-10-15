from sqlalchemy import Column, Integer, String, Boolean
from database import Base


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
