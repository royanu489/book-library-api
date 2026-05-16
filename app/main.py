from fastapi import FastAPI
from app.database import engine, Base
from app.routers import books, auth

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="📚 Book Library API",
    description="A REST API to manage your personal book library. Built with FastAPI + SQLite.",
    version="1.0.0"
)

# Include routers (groups of related endpoints)
app.include_router(auth.router)
app.include_router(books.router)


@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the Book Library API! 📚",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth/register | /auth/login",
            "books": "/books"
        }
    }
