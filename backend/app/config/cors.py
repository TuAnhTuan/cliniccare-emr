import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Comma-separated list of origins allowed to call this API from a browser,
# e.g. "http://localhost:3000,https://cliniccare.example.com"
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]


def configure_cors(app: FastAPI) -> None:
    """Allow the frontend to call this API directly from the browser
    (client-side search/submit requests, as opposed to server-side SSR fetches)."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )
