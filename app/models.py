from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    """Stores registered users"""
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email    = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)           # hashed password
    is_active = Column(Boolean, default=True)

    # One user can have many books
    books = relationship("Book", back_populates="owner")


class Book(Base):
    """Stores books added by users"""
    __tablename__ = "books"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String, index=True, nullable=False)
    author      = Column(String, nullable=False)
    genre       = Column(String, nullable=True)
    year        = Column(Integer, nullable=True)
    rating      = Column(Float, nullable=True)          # 1.0 – 5.0
    is_read     = Column(Boolean, default=False)
    created_at  = Column(DateTime, default=datetime.utcnow)

    # Foreign key links book → user
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner    = relationship("User", back_populates="books")
