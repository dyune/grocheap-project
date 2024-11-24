from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import asyncio
from backend.models import create_item, initialize_db

# List of IGA pages to scrape
DEMO_URLS = [
    "https://www.iga.net/en/online_grocery/aisles/fruits_and_vegetables",
    "https://www.iga.net/en/online_grocery/aisles/meat_and_seafood",
    "https://www.iga.net/en/online_grocery/aisles/dairy_and_eggs",
]


async def save_product_to_db(name, brand, link, image_url, size, store, price):
    """Save product details to the database."""
    if name and link and price is not None:
        try:
            await create_item(name, brand, link, image_url, size, store, price)
            print(f"Saved: {name} from {store} at ${price}")
        except Exception as e:
            print(f"Failed to save {name}: {e}")
    else:
        print(f"Invalid product data: {name}, {brand}, {link}, {image_url}, {size}, {price}")


def parse_product(product):
    """Parse individual product details from the HTML."""
    # Product name
    name_tag = product.find("a", class_="js-ga-productname")
    name = name_tag.text.strip() if name_tag else "Name not found"

    # Brand
    brand_tag = product.find("div", class_="item-product__brand")
    brand = brand_tag.text.strip() if brand_tag else "Brand not found"

    # Product URL
    link_tag = name_tag.find("a") if name_tag else None
    link = "https://www.iga.net" + link_tag.get("href") if link_tag else None

    # Image URL
    image_tag = product.find("img")
    image_url = image_tag.get("src") if image_tag else "Image not found"

    # Size
    size_tag = product.find("div", class_="item-product__info")
    size = size_tag.text.strip() if size_tag else "Size not found"

    # Price
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


def scrape_page(url, driver):
    """Scrape a single IGA page using Selenium and BeautifulSoup."""
    driver.get(url)

    # Wait for the page to load fully
    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "grid"))
        )
        print(f"Page loaded successfully: {url}")
    except Exception as e:
        print(f"Error waiting for page to load: {e}")
        return []

    # Scroll to load more products if needed
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "grid"))
    )

    # Parse the page content
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    product_containers = soup.find_all("div", class_="grid__item")

    # Extract product details
    products = []
    for product in product_containers:
        try:
            product_data = parse_product(product)
            if product_data["name"] and product_data["price"] is not None:
                products.append(product_data)
        except Exception as e:
            print(f"Failed to parse product: {e}")

    return products


async def update_iga():
    """Scrape IGA pages and save product data."""
    await initialize_db()
    driver = webdriver.Chrome()

    try:
        all_products = []
        for url in DEMO_URLS:
            products = scrape_page(url, driver)
            all_products.extend(products)

        # Save all products to the database
        tasks = [
            save_product_to_db(
                product["name"],
                product["brand"],
                product["link"],
                product["image_url"],
                product["size"],
                "IGA",
                product["price"],
            )
            for product in all_products
        ]
        if tasks:
            await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    asyncio.run(update_iga())
