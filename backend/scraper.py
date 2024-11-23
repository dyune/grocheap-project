from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup

from models import fetch_all_items, fetch_all_stores, create_price

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
STORE_URLS = {
    "IGA": "https://www.iga.net/en/search?search-bar=",  # IGA URL for search
    "Super C": "https://www.superc.ca/en",  # Example URL for Super C
    "Maxi": "https://www.maxi.ca/en",  # Example URL for Maxi
}


# Scrape IGA (asynchronous)
async def scrape_iga(search_term):
    """Scrape IGA's website for items and prices."""
    items = []
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{STORE_URLS['IGA']}{search_term}") as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            # Scrape IGA products (replace with actual selectors)
            products = soup.find_all("div", class_="product-card")
            for product in products:
                name = product.find("h2", class_="product-name").text.strip()
                price = product.find("span", class_="product-price").text.strip()
                url = product.find("a", class_="product-link")["href"]

                items.append({
                    "name": name,
                    "price": float(price.replace("$", "").strip()),
                    "url": url,
                    "last_updated": datetime.now()
                })
    return items


# Scrape Super C (asynchronous)
async def scrape_super_c(search_term):
    """Scraper for Super C store."""
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{STORE_URLS['Super C']}/en/search?search-bar={search_term}") as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            # Example scraping logic (adjust based on Super C's structure):
            prices = []
            for product in soup.select(
                    ".product-class"):  # Replace with actual class
                name = product.select_one(
                    ".product-name-class").text.strip()  # Replace with actual class
                price = float(
                    product.select_one(".price-class").text.strip().replace(
                        "$", ""))  # Replace with actual class
                link = STORE_URLS['Super C'] + product.select_one("a")[
                    "href"]  # Replace with actual structure
                prices.append({"name": name, "price": price, "url": link})

    return prices


# Scrape Maxi (asynchronous)
async def scrape_maxi(search_term):
    """Scraper for Maxi store."""
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{STORE_URLS['Maxi']}/en/search?search-bar={search_term}") as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            # Example scraping logic (adjust based on Maxi's structure):
            prices = []
            for product in soup.select(
                    ".product-class"):  # Replace with actual class
                name = product.select_one(
                    ".product-name-class").text.strip()  # Replace with actual class
                price = float(
                    product.select_one(".price-class").text.strip().replace(
                        "$", ""))  # Replace with actual class
                link = STORE_URLS['Maxi'] + product.select_one("a")[
                    "href"]  # Replace with actual structure
                prices.append({"name": name, "price": price, "url": link})

    return prices


# Update prices in the database
async def update_prices(store_name, scraper_function, search_term):
    """Fetch items and update prices using the scraper."""
    stores = await fetch_all_stores()
    items = await fetch_all_items()

    # Find the store ID
    store_id = next(
        (store["id"] for store in stores if store["name"] == store_name), None)
    if store_id is None:
        raise ValueError(f"Store '{store_name}' not found in the database.")

    # Scrape data
    scraped_data = await scraper_function(search_term)

    # Update prices in the database
    for product in scraped_data:
        item = next(
            (item for item in items if item["name"] == product["name"]), None)
        if item:
            await create_price(store_id, item["id"], product["price"],
                               product["url"])


# run_scraper.py
import asyncio


def main():
    search_term = "milk"  # Or any item you want to search for
    asyncio.run(
        update_prices("Maxi", scrape_maxi, search_term))  # Example for Maxi
    asyncio.run(update_prices("Super C", scrape_super_c,
                              search_term))  # Example for Super C
    asyncio.run(
        update_prices("IGA", scrape_iga, search_term))  # Example for IGA


if __name__ == "__main__":
    main()
