import asyncio
import random
import time
import tracemalloc

from fake_useragent import UserAgent
from typing import List
from bs4 import BeautifulSoup, PageElement
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from backend.db.models import Item
from backend.services.scrapers.utils.scraper_utils \
    import save_products_to_db, parse_unit_price, prepare_urls, process_items_for_db

# Configure Chrome for headless mode
ua = UserAgent()
chrome_options = Options()
chrome_options.add_argument(f"user-agent={ua.random}")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")


TEST = [
    ("https://www.superc.ca/en/aisles/fruits-vegetables", 2),
]

# URLs of the SuperC pages
BATCH_1 = [
    ("https://www.superc.ca/en/aisles/fruits-vegetables", 21),
    ("https://www.superc.ca/en/aisles/dairy-eggs", 31),
    ("https://www.superc.ca/en/aisles/pantry", 85),
    ("https://www.superc.ca/en/aisles/cooked-meals", 2),
    ("https://www.superc.ca/en/aisles/value-pack", 16),
    ("https://www.superc.ca/en/aisles/beverages", 36),
]

BATCH_2 = [
    ("https://www.superc.ca/en/aisles/beer-wine", 17),
    ("https://www.superc.ca/en/aisles/meat-poultry", 13),
    ("https://www.superc.ca/en/aisles/vegan-vegetarian-food", 13),
    ("https://www.superc.ca/en/aisles/organic-groceries", 10),
    ("https://www.superc.ca/en/aisles/snacks", 49),
    ("https://www.superc.ca/en/aisles/frozen", 29),
    ("https://www.superc.ca/en/aisles/bread-bakery-products", 14),
    ("https://www.superc.ca/en/aisles/deli-prepared-meals", 18),
    ("https://www.superc.ca/en/aisles/fish-seafood", 5),
    ("https://www.superc.ca/en/aisles/world-cuisine", 8),
]


def parse_product(product: PageElement):
    brand = product.get("data-product-brand", "No brand")
    name = product.get("data-product-name", None)

    link_tag = product.find("a", class_="product-details-link")
    product_link = "https://www.superc.ca" + link_tag.get("href") if link_tag else None

    # TODO: Implement better product price tag sanitizing
    price_tag = product.find("span", class_="price-update")
    try:
        price = (float(price_tag.text.strip().replace("$", "")) if price_tag else None)
    except ValueError:
        price = parse_unit_price(price_tag.text)
        if not price:
            price = None

    size_tag = product.find("span", class_="head__unit-details")
    if size_tag:
        size = size_tag.text.strip()
    else:
        size_alt_tag = product.find("span", class_="unit-update")
        size = size_alt_tag.text.strip() if size_alt_tag else None

    image_tag = product.find("img", alt=True)
    image_url = image_tag.get("src") if image_tag else None

    return {
        "name": name,
        "brand": brand,
        "link": product_link,
        "image_url": image_url,
        "size": size,
        "price": price,
    }


async def scrape_page(url, driver) -> List[Item]:
    """
    Load a page with Selenium, parse the products, and return tasks to save them.
    """

    # Navigate to the page
    driver.get(url)
    items = []

    # Wait for the page to load fully
    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "default-product-tile"))
        )
        print(f"Page loaded successfully: {url}")

    except Exception as e:
        print(f"Error waiting for page to load: {e}")
        return []

    # Scroll down to ensure all products are loaded (if the page has lazy loading)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait to allow additional products to load if needed

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    all_products = soup.find_all("div", class_="default-product-tile")

    return process_items_for_db(3, all_products, parse_product)


async def batch_insert_superc(urls):
    """Gather SuperC products."""
    driver = webdriver.Chrome(options=chrome_options)  # Set up the WebDriver
    items = []

    try:
        for url in urls:
            delay = random.uniform(2, 5)  # Timeout to prevent being spotted as bot
            time.sleep(delay)
            result = await scrape_page(url, driver)
            print(f'Found {len(result)} products.')
            items.extend(result)

        if items:
            print(f"Saved these following items: {save_products_to_db(items)}")

    except Exception as e:
        print(f"Error during update, could not save: {e}")

    finally:
        driver.quit()  # Ensure the browser is closed


if __name__ == "__main__":
    tracemalloc.start()
    # links_1 = prepare_urls(BATCH_1)
    links_2 = prepare_urls(BATCH_2)

    asyncio.run(batch_insert_superc(links_2))
    # asyncio.run(batch_insert_superc(links_2))
