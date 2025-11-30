from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.v1.router import router as api_router
from app.core.config import settings
from app.db.utils import connect_to_dbs, close_dbs


# load .env 
load_dotenv()

app = FastAPI(
    title="Elelem Visibility Backend",
    description=f"GenAI Visibility Scoring API | Environment: {settings.ENVIRONMENT}",
    version="1.0.0",
)


@app.lifespan("startup")
async def startup_event():
    await connect_to_dbs()

@app.lifespan("shutdown")
async def shutdown_event():
    await close_dbs()

# Include the API router with a prefix 
app.include_router(api_router, prefix="/api/v1", tags=["Visibility Query"])

@app.get("/")
async def root():
    return {"message": f"Welcome to the Visibility API. Current Environment: {settings.ENVIRONMENT}"}