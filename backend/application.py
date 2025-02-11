from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.services.scrapers.superc_scraper import batch_insert_superc, prepare_urls, ALL_URLS
from backend.db import crud, associations
from backend.db.session import init_db

app = FastAPI(
    prefix="/api"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(crud.router)
app.include_router(associations.router)


@app.on_event("startup")
async def startup():
    init_db()


@app.post("/scrape/super-c")
async def scrape_super_c():
    await batch_insert_superc(prepare_urls(ALL_URLS))
