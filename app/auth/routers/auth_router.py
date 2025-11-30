from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from app.auth.models.auth_models import LoginPayload, UserInDB
from app.db.mongodb.user_storage import get_user_by_email, create_user
from app.auth.core.utils import verify_password, create_access_token


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
async def login_for_access_token(response: JSONResponse, form_data: LoginPayload = Depends()):
    """
    Authenticates a user via email and password, returning a secure HTTP-only cookie
    containing the JWT access token.
    """
    user = await get_user_by_email(form_data.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify the password against the stored hash
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Create the JWT token
    access_token = create_access_token(data={"email": user.email})
    
    # Successful login response
    response_content = {"message": "Login successful"}
    response = JSONResponse(content=response_content)
    
    # Set the secure, HTTP-only cookie
    # httponly=True: Prevents JavaScript access (XSS defense)
    # secure=True: Ensures cookie is only sent over HTTPS (production requirement)
    # samesite="strict": Protects against CSRF (Cross-Site Request Forgery)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True, 
        samesite="strict" 
    )
    
    return response