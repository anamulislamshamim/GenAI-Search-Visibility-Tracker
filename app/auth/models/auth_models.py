from pydantic import BaseModel, Field
from typing import Optional

class Token(BaseModel):
    """Model for the token payload (claims stored in the JWT)."""
    # The subject of the token (e.g., user ID or email)
    sub: str = Field(..., description="Subject of the token (user identifier)")
    # Optional: Token expiration time (Unix timestamp)
    exp: Optional[int] = Field(None, description="Expiration time of the token")

class LoginPayload(BaseModel):
    """Model for the data received at the /login endpoint."""
    email: str = Field(..., example="user@example.com")
    password: str = Field(..., example="secure_password_123")

class UserInDB(BaseModel):
    """Model for a User document stored in MongoDB."""
    email: str = Field(..., example="user@example.com", unique=True)
    hashed_password: str = Field(..., description="Bcrypt hashed password.")