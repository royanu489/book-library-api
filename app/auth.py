from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

# ── Security config ───────────────────────────────────────────────────────────
SECRET_KEY  = "your-secret-key-change-this-in-production"  # ← change in prod!
ALGORITHM   = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 24     # token lives for 24 hours

# ── Password hashing ──────────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    """Turn plain text password into a secure hash"""
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    """Check if a plain password matches its hash"""
    return pwd_context.verify(plain, hashed)

# ── JWT tokens ────────────────────────────────────────────────────────────────
def create_access_token(data: dict) -> str:
    """Create a JWT token with an expiry time"""
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# ── Current user dependency ───────────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db:    Session = Depends(get_db)
) -> models.User:
    """
    Decode the JWT from the Authorization header and return the logged-in user.
    This is used as a dependency in protected routes.
    """
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload  = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_error
    except JWTError:
        raise credentials_error

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_error
    return user
