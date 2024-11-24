from superc_scraper import update_prices, scrape_iga, scrape_super_c, scrape_maxi
from fastapi import FastAPI, HTTPException
from models import *

app = FastAPI()


@app.get("/init/stores")
async def start_stores():
    try:
        await create_store("IGA", "https://www.iga.net")
        await create_store("Super C", "https://www.superc.ca/en")
        await create_store("Maxi", "https://www.maxi.ca/en")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "ok"}



@app.get("/scrape/{store_name}")
async def scrape_store(store_name: str):
    """Trigger scraper for a specific store."""
    try:
        if store_name.lower() == "iga":
            await update_prices("IGA", scrape_iga)
        elif store_name.lower() == "super c":
            await update_prices("Super C", scrape_super_c)
        elif store_name.lower() == "maxi":
            await update_prices("Maxi", scrape_maxi)
        else:
            raise HTTPException(status_code=404,
                                detail=f"No scraper available for {store_name}.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "ok", "store": store_name}
