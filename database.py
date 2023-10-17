"""
Database initializer and session manager
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# create_engine:
# create_engine is a function from SQLAlchemy that creates an instance of an SQLAlchemy Engine. The engine represents the interface to the database. It's responsible for managing connections, transactions, and the overall communication between your Python application and the database.

# Parameters:

# DATABASE_URL: This is the URL or connection string for the database. The format depends on the type of database you're connecting to (SQLite, PostgreSQL, MySQL, etc.).

# sessionmaker:
# sessionmaker is a factory for creating new SQLAlchemy Session instances.
# A Session is a high-level interface to the database, providing methods to query and interact with the database.
# The sessionmaker configures how sessions will behave, including settings for autocommit, autoflush, and the database bind.

# Parameters:

# autocommit: If True, the session will automatically commit transactions. Setting it to False means you need to call commit() explicitly.
# autoflush: If True, the session will automatically flush changes to the database before any query. Setting it to False means you need to call flush() explicitly.
# bind: The bind parameter is optional and allows you to specify the SQLAlchemy Engine to be used for this session.
# SessionLocal:
# SessionLocal is an instance of the session factory created by sessionmaker. It's typically used in your application to create new sessions when needed. This instance will have the specified behavior defined by sessionmaker.

# Base:
# Base is a declarative base class provided by SQLAlchemy. It's used as a base class for your model classes.
# By subclassing Base, your model classes inherit useful attributes and methods for interacting with the database.


SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

db_engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autoflush=True, bind=db_engine, autocommit=False)

Base = declarative_base()


def get_db():
    """
    Get DB Session and yeild the db session
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
