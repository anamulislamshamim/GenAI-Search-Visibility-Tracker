import datetime
from typing import Optional, Any
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.core.config import settings


# Uses a safe default, but MUST be loaded from .env in production
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Password Hashing Functions ---

def hash_password(password: str) -> str:
    # Truncate to the first 72 bytes/characters
    safe_password = password[:72]
    return pwd_context.hash(safe_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Truncate to the first 72 bytes/characters before verification
    safe_password = plain_password[:72]
    return pwd_context.verify(safe_password, hashed_password)


# --- JWT Token Functions ---
def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        # Default expiration
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire, "sub": to_encode.pop('email')})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict[str, Any]]:
    """Decodes and validates a JWT access token."""
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if the token is valid (not expired)
        if datetime.datetime.fromtimestamp(payload.get("exp"), tz=datetime.timezone.utc) < datetime.datetime.now(datetime.timezone.utc):
             return None # Token expired
             
        # Return the subject (user identifier)
        return payload

    except JWTError:
        return None # Invalid token structure or signature