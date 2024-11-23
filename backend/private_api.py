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



