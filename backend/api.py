from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.main import app as main_app

# Create a new FastAPI instance
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your main app's router
app.include_router(main_app.router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Tree Grid API"}

# This is needed for Vercel to find the app
handler = app