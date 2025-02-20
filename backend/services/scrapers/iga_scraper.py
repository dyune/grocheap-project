import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import asyncio
from selenium.webdriver.chrome.options import Options
import xml.etree.ElementTree as ET

from backend.services.scrapers.scraper_utils import create_db_item, save_products_to_db

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# List of IGA pages to scrape
SITE_URL = "https://www.iga.net/en/online_grocery/browse?pageSize=24"

URLS = [SITE_URL + f"&page={i}" for i in range(1, 1128)]


def parse_product(product):
    name_tag = product.find("a", class_="js-ga-productname")
    name = name_tag.text.strip() if name_tag else "Name not found"

    brand_tag = product.find("div", class_="item-product__brand")
    brand = brand_tag.text.strip() if brand_tag else "No brand"

    link_tag = name_tag if name_tag else None
    link = "https://www.iga.net" + link_tag.get("href") if link_tag else None

    image_tag = product.find("img")
    image_url = image_tag.get("src") if image_tag else "Image not found"

    size_tag = product.find("div", class_="item-product__info")
    size = size_tag.text.strip() if size_tag else " "

    price_tag = product.find("span", class_="price text--strong")
    price = float(price_tag.text.strip().replace("$", "")) if price_tag else None

    return {
        "name": name,
        "brand": brand,
        "link": link,
        "image_url": image_url,
        "size": size,
        "price": price,
    }


async def scrape_page(url, driver):
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

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "grid"))
    )

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    all_products = soup.find_all("div", class_="grid__item")

    try:
        for product in all_products:
            product_data = parse_product(product)

            if product_data["name"] and product_data["price"] and product_data["link"] is not None:
                db_item = create_db_item(
                    product_data["name"],
                    product_data["brand"],
                    product_data["link"],
                    product_data["image_url"],
                    product_data["size"],
                    3,
                    product_data["price"],
                )
                if db_item:
                    items.append(db_item)

            else:
                print(f"Product {product_data['name']} was missing essential information and could not be saved")

    except Exception as e:
        print(f"Failed to scrape: {e}")
        return None

    return items


async def update_iga(urls):
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
    print(URLS)
    asyncio.run(update_iga(URLS))
