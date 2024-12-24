import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import jobsRoutes

# Make sure all models are created
def create_tables():
    Base.metadata.create_all(bind=engine)

# Call it when app starts
create_tables()

app = FastAPI(title="FastAPI App")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(jobsRoutes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)