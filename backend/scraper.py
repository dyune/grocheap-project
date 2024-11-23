from datetime import datetime
import aiohttp
import requests
from bs4 import BeautifulSoup
from models import fetch_all_items, fetch_all_stores, create_price

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


async def scrape_iga():
    """Scrape IGA's website for items and prices."""
    items = []
    async with aiohttp.ClientSession() as session:
        async with session.get(STORE_URLS["IGA"]) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            # Example: Replace with IGA's specific selectors
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


async def scrape_super_c():
    """Scraper for Super C store."""
    url = "https://www.superc.ca/en"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Example scraping logic (adjust based on Super C's structure):
    prices = []
    for product in soup.select(".product-class"):  # Replace with actual class
        name = product.select_one(
            ".product-name-class").text.strip()  # Replace with actual class
        price = float(
            product.select_one(".price-class").text.strip().replace("$",
                                                                    ""))  # Replace with actual class
        link = url + product.select_one("a")[
            "href"]  # Replace with actual structure
        prices.append({"name": name, "price": price, "url": link})

    return prices


async def scrape_maxi():
    """Scraper for Maxi store."""
    url = "https://www.maxi.ca/en"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Example scraping logic (adjust based on Maxi's structure):
    prices = []
    for product in soup.select(".product-class"):  # Replace with actual class
        name = product.select_one(
            ".product-name-class").text.strip()  # Replace with actual class
        price = float(
            product.select_one(".price-class").text.strip().replace("$",
                                                                    ""))  # Replace with actual class
        link = url + product.select_one("a")[
            "href"]  # Replace with actual structure
        prices.append({"name": name, "price": price, "url": link})

    return prices


async def update_prices(store_name, scraper_function):
    """Fetch items and update prices using the scraper."""
    stores = await fetch_all_stores()
    items = await fetch_all_items()

    # Find the store ID
    store_id = next(
        (store["id"] for store in stores if store["name"] == store_name), None)
    if store_id is None:
        raise ValueError(f"Store '{store_name}' not found in the database.")

    # Scrape data
    scraped_data = await scraper_function()

    # Update prices in the database
    for product in scraped_data:
        item = next(
            (item for item in items if item["name"] == product["name"]), None)
        if item:
            await create_price(store_id, item["id"], product["price"],
                               product["url"])


