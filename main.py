from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.v1.router import router as api_router
from app.auth.routers.auth_router import router as auth_router
from app.core.config import settings
from app.db.utils import connect_to_dbs, close_dbs
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware


# load .env 
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic here
    await connect_to_dbs()
    # e.g. connect to DB, load resources, initialize things
    yield
    # shutdown logic here
    await close_dbs()
    # e.g. close DB, clean up resources

app = FastAPI(
    lifespan=lifespan,
    title="Elelem Visibility Backend",
    description=f"GenAI Visibility Scoring API | Environment: {settings.ENVIRONMENT}",
    version="1.0.0",
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add your production frontend domain here when deploying, e.g., "https://yourapp.com"
]

app.add_middleware(
    CORSMiddleware,
    # Allow all origins for now, but uncomment 'allow_origins' below for production
    allow_origins=origins,
    # allow_origins=origins, # Use this in production
    
    # Allow credentials (necessary for cookies/JWT in HTTP-only cookies)
    allow_credentials=True, 
    
    # Allow specific HTTP methods (POST, GET, OPTIONS are standard)
    allow_methods=["*"], 
    
    # Allow specific headers (necessary for Content-Type, Authorization, etc.)
    allow_headers=["*"], 
)

# Include the API router with a prefix 
app.include_router(auth_router, prefix="/auth", tags=["authentication endpoints"])
app.include_router(api_router, prefix="/api/v1", tags=["Visibility Query"])

@app.get("/")
async def root():
    return {"message": f"Welcome to the Visibility API. Current Environment: {settings.ENVIRONMENT}"}