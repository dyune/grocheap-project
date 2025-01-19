import asyncio
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

from backend.services.scrapers.db_utils import create_db_item, save_products_to_db

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

DEMO_URLS = [
    "https://www.maxi.ca/en/food/fruits-vegetables/c/28000",
    "https://www.maxi.ca/en/food/meat/c/27998",
    "https://www.maxi.ca/en/food/natural-and-organic/dairy-and-eggs/c/59391",
]


def first_layer_parsing(url, driver):
    """Scrape the data from the page."""

    driver.get(url)

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "chakra-linkbox__overlay"))
        )
        print(f"Page loaded successfully: {url}")
        time.sleep(3)

    except Exception as e:
        print(f"Error waiting for content: {e}")

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div", class_="chakra-linkbox css-yxqevf")
    products = []

    # Scroll down to ensure all products are loaded (if the page has lazy loading)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait to allow additional products to load if needed

    for div in divs:
        try:
            name_tag = div.find("h3", class_="chakra-heading css-6qrhwc")
            name = name_tag.text.strip() if name_tag else None

            brand_tag = div.find("p", class_="chakra-text css-1ecdp9w")
            brand = brand_tag.text.strip() if brand_tag else "No brand"

            price_tag = div.find("span", attrs={"data-testid": "regular-price"})
            sale_price_tag = div.find("span", attrs={"data-testid": "sale-price"})

            if price_tag:
                price_text = price_tag.text
                price_match = re.search(r"\d+\.\d+", price_text)
                price = float(price_match.group()) if price_match else None

            elif sale_price_tag:
                price_text = sale_price_tag.text
                price_match = re.search(r"\d+\.\d+", price_text)
                price = float(price_match.group()) if price_match else None

            else:
                price = None

            a_tag = div.find("a", class_="chakra-linkbox__overlay css-1hnz6hu")
            link = "https://www.maxi.ca" + a_tag.get("href") if a_tag else None

            size_tag = div.find("p", attrs={"data-testid": "product-package-size"})
            size = size_tag.text.split(",")[0] if size_tag else None

            img_tag = div.find("img")
            image_url = img_tag.get("src") if img_tag else None

            if name and link and price is not None:
                db_item = create_db_item(
                    name,
                    brand,
                    link,
                    image_url,
                    size,
                    2,
                    price
                )
                if db_item:
                    products.append(db_item)

            else:
                print("Missing info: ", name, brand, link, size, price)

        except Exception as e:
            print(f"Parsing error, unable to save: {e}")

        finally:
            continue

    return products


async def update_maxi():
    """Update Maxi products."""

    driver = webdriver.Chrome(options=chrome_options)

    try:
        all_products = []

        for link in DEMO_URLS:
            products = first_layer_parsing(link, driver)
            all_products.extend(products)

        if all_products:
            await save_products_to_db(all_products)

    except Exception as e:
        print(f"Error updating Maxi: {e}")
        return False

    return True


if __name__ == "__main__":
    asyncio.run(update_maxi())
