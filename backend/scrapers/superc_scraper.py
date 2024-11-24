import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from backend.models import create_item, initialize_db  # Ensure correct import
import time

# URLs of the SuperC pages
DEMO_URLS = [
    "https://www.superc.ca/en/aisles/fruits-vegetables/fruits",
    "https://www.superc.ca/en/aisles/fruits-vegetables/vegetables",
    "https://www.superc.ca/en/aisles/meat-poultry/beef-veal",
]


async def save_product_to_db(name, brand, link, image_url, size, store, price):
    """Save product details to the database."""
    try:
        await create_item(name, brand, link, image_url, size, store, price)
        print(f"Saved: {name} from {store}")
    except Exception as e:
        print(f"Failed to save {name}: {e}")


def first_layer_parsing(url, driver):
    """
    Load a page with Selenium, parse the products, and return tasks to save them.
    """
    # Navigate to the page
    driver.get(url)

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

    # Get the rendered HTML
    html = driver.page_source

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all product tiles
    products = soup.find_all("div", class_="default-product-tile")

    tasks = []  # To store asyncio tasks
    for product in products:
        # Extract data for each product
        brand = product.get("data-product-brand", "Brand not found")
        name = product.get("data-product-name", "Name not found")

        url_tag = product.find("a", class_="product-details-link")
        product_url = "https://www.superc.ca" + url_tag.get("href") if url_tag else "URL not found"

        price_tag = product.find("span", class_="price-update")
        price = (
            float(price_tag.text.strip().replace("$", "")) if price_tag else None
        )  # Convert price to float

        size_tag = product.find("span", class_="head__unit-details")
        if size_tag:
            size = size_tag.text.strip()
        else:
            size_alt_tag = product.find("span", class_="unit-update")
            size = size_alt_tag.text.strip() if size_alt_tag else "None"

        image_tag = product.find("img", alt=True)
        image = image_tag.get("src") if image_tag else "Image not found"

        # Print product details
        print(f"Product Brand: {brand}")
        print(f"Product Name: {name}")
        print(f"Product Price: {price}")
        print(f"Product Size: {size}")
        print(f"Product URL: {product_url}")
        print(f"Product Image: {image}")
        print("-" * 50)

        # Create an asyncio task to save the product
        if name and product_url and price is not None:
            tasks.append(
                save_product_to_db(name, brand, product_url, image, size, "Super C", price)
            )

    return tasks


async def update_superc():
    """Update SuperC products."""
    await initialize_db()  # Ensure the database is initialized
    driver = webdriver.Chrome()  # Set up the WebDriver

    all_tasks = []
    try:
        for url in DEMO_URLS:
            tasks = first_layer_parsing(url, driver)
            all_tasks.extend(tasks)

        # Run all database save tasks
        if all_tasks:
            await asyncio.gather(*all_tasks)
    except Exception as e:
        print(f"Error during update: {e}")
    finally:
        driver.quit()  # Ensure the browser is closed


if __name__ == "__main__":
    asyncio.run(update_superc())
