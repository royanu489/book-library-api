from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file will be created in the project root
DATABASE_URL = "sqlite:///./library.db"

# connect_args is needed only for SQLite (allows multi-threading)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Each request gets its own DB session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All models will inherit from this Base
Base = declarative_base()


# Dependency — used in routes to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db          # give the session to the route
    finally:
        db.close()        # always close it after the request
