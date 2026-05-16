from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ─────────────────────────────────────────
#  USER SCHEMAS
# ─────────────────────────────────────────

class UserCreate(BaseModel):
    """What the client sends when registering"""
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")
    email:    EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., min_length=6, example="secret123")


class UserResponse(BaseModel):
    """What we send back (never expose password!)"""
    id:       int
    username: str
    email:    str
    is_active: bool

    class Config:
        from_attributes = True    # lets Pydantic read SQLAlchemy objects


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"


# ─────────────────────────────────────────
#  BOOK SCHEMAS
# ─────────────────────────────────────────

class BookCreate(BaseModel):
    """What the client sends to add a book"""
    title:   str   = Field(..., min_length=1, example="The Pragmatic Programmer")
    author:  str   = Field(..., example="David Thomas")
    genre:   Optional[str]  = Field(None, example="Technology")
    year:    Optional[int]  = Field(None, example=2019)
    rating:  Optional[float] = Field(None, ge=1.0, le=5.0, example=4.5)
    is_read: bool  = Field(False, example=False)


class BookUpdate(BaseModel):
    """All fields optional for partial updates (PATCH)"""
    title:   Optional[str]   = None
    author:  Optional[str]   = None
    genre:   Optional[str]   = None
    year:    Optional[int]   = None
    rating:  Optional[float] = Field(None, ge=1.0, le=5.0)
    is_read: Optional[bool]  = None


class BookResponse(BaseModel):
    """What we send back after creating / fetching a book"""
    id:         int
    title:      str
    author:     str
    genre:      Optional[str]
    year:       Optional[int]
    rating:     Optional[float]
    is_read:    bool
    created_at: datetime
    owner_id:   int

    class Config:
        from_attributes = True
