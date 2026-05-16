from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])


# ── CREATE ────────────────────────────────────────────────────────────────────

@router.post("/", response_model=schemas.BookResponse, status_code=201)
def add_book(
    book_data: schemas.BookCreate,
    db:   Session      = Depends(get_db),
    user: models.User  = Depends(get_current_user)   # 🔒 protected route
):
    """Add a new book to your library. Requires login."""
    new_book = models.Book(**book_data.dict(), owner_id=user.id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


# ── READ ALL (with search & filter) ──────────────────────────────────────────

@router.get("/", response_model=List[schemas.BookResponse])
def get_books(
    search:  Optional[str]  = Query(None, description="Search by title or author"),
    genre:   Optional[str]  = Query(None, description="Filter by genre"),
    is_read: Optional[bool] = Query(None, description="Filter by read status"),
    skip:    int = Query(0,  ge=0,  description="Pagination offset"),
    limit:   int = Query(10, ge=1, le=100, description="Items per page"),
    db:      Session     = Depends(get_db),
    user:    models.User = Depends(get_current_user)
):
    """
    Get all your books. Supports:
    - ?search=python     → search title or author
    - ?genre=Technology  → filter by genre
    - ?is_read=true      → filter by read status
    - ?skip=0&limit=10   → pagination
    """
    query = db.query(models.Book).filter(models.Book.owner_id == user.id)

    if search:
        query = query.filter(
            models.Book.title.ilike(f"%{search}%") |
            models.Book.author.ilike(f"%{search}%")
        )
    if genre:
        query = query.filter(models.Book.genre.ilike(f"%{genre}%"))
    if is_read is not None:
        query = query.filter(models.Book.is_read == is_read)

    return query.offset(skip).limit(limit).all()


# ── READ ONE ──────────────────────────────────────────────────────────────────

@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(
    book_id: int,
    db:   Session     = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """Get a single book by its ID."""
    book = db.query(models.Book).filter(
        models.Book.id == book_id,
        models.Book.owner_id == user.id
    ).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# ── UPDATE (partial) ──────────────────────────────────────────────────────────

@router.patch("/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id:   int,
    book_data: schemas.BookUpdate,
    db:   Session     = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """
    Update any fields of a book. Only send the fields you want to change.
    Example: {"is_read": true, "rating": 4.5}
    """
    book = db.query(models.Book).filter(
        models.Book.id == book_id,
        models.Book.owner_id == user.id
    ).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Only update fields that were actually sent
    update_data = book_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


# ── DELETE ────────────────────────────────────────────────────────────────────

@router.delete("/{book_id}", status_code=204)
def delete_book(
    book_id: int,
    db:   Session     = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """Delete a book from your library."""
    book = db.query(models.Book).filter(
        models.Book.id == book_id,
        models.Book.owner_id == user.id
    ).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return   # 204 No Content — no body needed


# ── STATS ─────────────────────────────────────────────────────────────────────

@router.get("/stats/summary")
def get_stats(
    db:   Session     = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """Get a quick summary of your library."""
    books = db.query(models.Book).filter(models.Book.owner_id == user.id).all()
    if not books:
        return {"message": "No books in your library yet!"}

    ratings = [b.rating for b in books if b.rating]
    return {
        "total_books":   len(books),
        "books_read":    sum(1 for b in books if b.is_read),
        "books_unread":  sum(1 for b in books if not b.is_read),
        "average_rating": round(sum(ratings) / len(ratings), 2) if ratings else None,
        "genres":        list(set(b.genre for b in books if b.genre))
    }
