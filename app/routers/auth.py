from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    - Checks if username/email already exists
    - Hashes the password before saving
    """
    # Check for duplicate username
    if db.query(models.User).filter(models.User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Check for duplicate email
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user with hashed password
    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)     # refresh to get the auto-generated id
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Login with username + password. Returns a JWT access token.
    Use this token in the Authorization header: Bearer <token>
    """
    user = db.query(models.User).filter(
        models.User.username == credentials.username
    ).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
