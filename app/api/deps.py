from typing import Optional

from fastapi import HTTPException, Header, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.core.config import settings
from app.services.auth import decode_access_token
from app.crud import crud_user

def get_current_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Header(None)
) -> User:
    """Get current user from the token."""
    if not token:
        raise HTTPException(status_code=400, detail="Token not provided")

    try:
        payload = decode_access_token(data=token)
        user = crud_user.get_by_email(db, email=payload["sub"])
        
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        return user
        
    except JWTError as e:
        raise HTTPException(status_code=400, detail="Token is invalid or has expired")

def get_db_session():
    """Get a database session. This can be a generator that yields a session and closes it after usage."""
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

# Other dependencies can be added as needed, such as caching.
