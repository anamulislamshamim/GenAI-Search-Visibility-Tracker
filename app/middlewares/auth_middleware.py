from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2
from jose import JWTError
from typing import Optional
from app.auth.core.utils import decode_access_token


# We extend OAuth2 to handle token extraction from a cookie instead of headers
# The 'scheme' instance is primarily used for dependency injection signature
oauth2_scheme = OAuth2() 

def get_token_from_cookie(request: Request) -> Optional[str]:
    """
    Extracts the JWT token from the 'access_token' HTTP-only cookie.
    """
    token = request.cookies.get("access_token")
    if token:
        # The token is stored as "Bearer <JWT>", so we split and return just the JWT
        try:
            scheme, token_string = token.split()
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme in cookie.",
                )
            return token_string
        except ValueError:
            # Handle cases where the cookie value is malformed (e.g., just the JWT without "Bearer ")
            return token # Return the whole thing, let the decoder fail it if necessary

    return None


async def get_current_user(token: Optional[str] = Depends(get_token_from_cookie)):
    """
    A FastAPI dependency that requires a valid JWT cookie.
    
    Raises:
        HTTPException 401: If the token is missing, invalid, or expired.
    
    Returns:
        str: The email (subject) of the authenticated user.
    """
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Access token cookie is missing.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token subject (email) missing.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # NOTE: In a real app, you would now fetch the user from the DB 
        # (e.g., get_user_by_email) to ensure the user still exists and is active.
        return email
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials or token expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )