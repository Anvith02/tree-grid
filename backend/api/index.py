from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.main import app as fastapi_app

# This is needed for Vercel to properly detect the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the FastAPI app
app.mount("/", fastapi_app)

# This is needed for Vercel to properly detect the ASGI app
api = app
