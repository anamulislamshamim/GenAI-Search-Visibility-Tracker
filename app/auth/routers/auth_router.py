from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.responses import JSONResponse
from app.auth.models.auth_models import LoginPayload, UserInDB
from app.db.mongodb.user_storage import get_user_by_email, create_user
from app.auth.core.utils import verify_password, create_access_token
from app.core.config import settings
from datetime import timedelta
from app.middlewares.auth_middleware import get_current_user


router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: LoginPayload):
    """
    Handles new user registration by checking for existing users and securely
    hashing and storing the new user's credentials in MongoDB.
    """
    # Attempt to create the user
    new_user = await create_user(user_data.email, user_data.password)
    
    if new_user is None:
        # User already exists (handled by the create_user function)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists."
        )
        
    # Registration successful
    return {"message": "User successfully registered.", "email": new_user.email}

@router.post("/login")
async def login_for_access_token(
    form_data: LoginPayload, 
    response: Response
):
    """
    Authenticates a user via email and password, returning a secure HTTP-only cookie
    containing the JWT access token.
    """
    # 1. Look up user by email
    user = await get_user_by_email(form_data.email)
    
    # 2. Authentication check
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Create the JWT token
    access_token = create_access_token(data={"email": user.email})
    
    # 4. Set the secure, HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        # Set max-age for persistence (e.g., 24 hours)
        max_age=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds(), 
        httponly=True,
        # Ensure 'secure=True' is used in production (settings.ENVIRONMENT check is best)
        secure=settings.ENVIRONMENT != "development", 
        samesite="lax" # 'strict' can cause issues with external links; 'lax' is safer default
    )
    
    # 5. Return a successful JSON response
    # We return a standard dict/Token model, and FastAPI handles serialization.
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(response: Response):
    """
    Logs out the user by clearing the access_token cookie.
    """
    try:
        get_current_user()
        response.delete_cookie(
            key="access_token",
            httponly=True,
            secure=settings.ENVIRONMENT != "development",
            samesite="lax"
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized attempt!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"message": "Logged out successfully"}

@router.get("/me")
async def verify_cookie():
    try:
        get_current_user()
        return {"status": True}
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Cookie!",
            headers={"WWW-Authenticate": "Bearer"},
        )