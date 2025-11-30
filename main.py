from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.v1.router import router as api_router
from app.auth.routers.auth_router import router as auth_router
from app.core.config import settings
from app.db.utils import connect_to_dbs, close_dbs
from contextlib import asynccontextmanager


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

# Include the API router with a prefix 
app.include_router(auth_router, prefix="/auth", tags=["authentication endpoints"])
app.include_router(api_router, prefix="/api/v1", tags=["Visibility Query"])

@app.get("/")
async def root():
    return {"message": f"Welcome to the Visibility API. Current Environment: {settings.ENVIRONMENT}"}