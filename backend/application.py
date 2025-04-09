from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import search
from backend.db.session import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],        # Allow all HTTP methods
    allow_headers=["*"],        # Allow all headers
)

app.include_router(search.router)


@app.on_event("startup")
async def startup():
    try:
        init_db()
    except Exception as e:
        print(f"Error: {e}")




