import asyncio
from typing import Dict, List

from bs4 import PageElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

from backend.db.models import Item
from backend.services.scrapers.utils.scraper_utils \
    import save_products_to_db, prepare_urls, process_items_for_db

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# List of IGA pages to scrape
# SITE_URL = "https://www.iga.net/en/online_grocery/browse?pageSize=24"
# URLS = [SITE_URL + f"&page={i}" for i in range(1, 1128)]

URLS_1 = [
    ("https://www.iga.net/en/online_grocery/instore_bakery", 41),
    ("https://www.iga.net/en/online_grocery/commercial_bakery", 14),
    ("https://www.iga.net/en/online_grocery/produce", 55),
    ("https://www.iga.net/en/online_grocery/home_meal_replacement", 33),
]

URLS_2 = [
    ("https://www.iga.net/en/online_grocery/produits_refrigeres", 56),
    ("https://www.iga.net/en/online_grocery/frozen_grocery", 44),
    ("https://www.iga.net/en/online_grocery/sushis", 9),
    ("https://www.iga.net/en/online_grocery/meat", 54),
]

URLS_3 = [
    ("https://www.iga.net/en/online_grocery/beverages", 81),
    ("https://www.iga.net/en/online_grocery/deli_and_cheese", 59),
    ("https://www.iga.net/en/online_grocery/seafood", 20),
]

URLS_4 = [
    ("https://www.iga.net/en/online_grocery/browse/Grocery/Snacks", 87)
]


def parse_product(product: PageElement) -> Dict[str, str]:
    name_tag = product.find("a", class_="js-ga-productname")
    name = name_tag.text.strip() if name_tag else "Name not found"

    brand_tag = product.find("div", class_="item-product__brand")
    brand = brand_tag.text.strip() if brand_tag else "No brand"

    link_tag = name_tag if name_tag else None
    product_link = "https://www.iga.net" + link_tag.get("href") if link_tag else None

    image_tag = product.find("img")
    image_url = image_tag.get("src") if image_tag else "Image not found"

    size_tag = product.find("div", class_="item-product__info")
    size = size_tag.text.strip() if size_tag else " "

    price_tag = product.find("span", class_="price text--strong")
    price = float(price_tag.text.strip().replace("$", "")) if price_tag else None

    return {
        "name": name,
        "brand": brand,
        "link": product_link,
        "image_url": image_url,
        "size": size,
        "price": price,
    }


async def scrape_page(url, driver) -> List[Item]:
    driver.get(url)
    items = []

    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "item-product"))
        )
        print(f"Page loaded successfully: {url}")

    except Exception as e:
        print(f"Error waiting for page to load: {e}")
        return []

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    all_products = soup.find_all("div", class_="grid__item")

    return process_items_for_db(1, all_products, parse_product)


async def scrape_iga(urls) -> None:
    """Gather SuperC products."""
    driver = webdriver.Chrome(options=chrome_options)  # Set up the WebDriver
    items = []

    try:
        for url in urls:
            result = await scrape_page(url, driver)
            items.extend(result)

        if items:
            save_products_to_db(items)
            print(f"Successfully saved {len(items)} products to the database.")

    except Exception as e:
        print(f"Error during update: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    # batch_1 = prepare_urls(URLS_1)
    # asyncio.run(scrape_iga(batch_1))
    link = prepare_urls("https://www.iga.net/en/online_grocery/instore_bakery", 2)
    asyncio.run(scrape_iga(link))
