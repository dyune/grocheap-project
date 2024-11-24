import asyncio
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from backend.models import create_item, initialize_db  # Ensure correct import

DEMO_URLS = [
    "https://www.maxi.ca/en/food/fruits-vegetables/c/28000",
    "https://www.maxi.ca/en/food/meat/c/27998",
    "https://www.maxi.ca/en/food/natural-and-organic/dairy-and-eggs/c/59391",
]


async def save_product_to_db(name, brand, link, image_url, size, store, price):
    """Save product details to the database."""
    try:
        await create_item(name, brand, link, image_url, size, store, price)
        print(f"Saved: {name} from {store} at ${price}")
    except Exception as e:
        print(f"Failed to save {name}: {e}")


def first_layer_parsing(url):
    """Scrape the data from the page."""
    driver = webdriver.Chrome()

    # Navigate to the URL
    driver.get(url)

    # Wait for the content to load
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "chakra-linkbox__overlay"))
        )
        print("Content loaded successfully.")
    except Exception as e:
        print(f"Error waiting for content: {e}")

    # Get the fully rendered HTML
    html = driver.page_source

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    # Find all product containers
    divs = soup.find_all("div", class_="chakra-linkbox css-yxqevf")
    tasks = []  # To store asyncio tasks
    if divs:
        for div in divs:
            # Extract product details
            name_tag = div.find("h3", class_="chakra-heading css-6qrhwc")
            name = name_tag.text.strip() if name_tag else None

            brand_tag = div.find("p", class_="chakra-text css-1ecdp9w")
            brand = brand_tag.text.strip() if brand_tag else None

            price_tag = div.find("span", attrs={"data-testid": "regular-price"})
            if price_tag:
                price_text = price_tag.text
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
                # Create an asyncio task to save the product
                tasks.append(save_product_to_db(name, brand, link, image_url, size, "Maxi", price))
            else:
                print("Missing essential product information, skipping: " + name)

    else:
        print("No product containers found.")

    # Close the browser
    driver.quit()

    return tasks  # Return the list of asyncio tasks


async def update_maxi():
    """Update Maxi products."""
    try:
        await initialize_db()  # Ensure the database is initialized
        all_tasks = []
        for link in DEMO_URLS:
            tasks = first_layer_parsing(link)
            all_tasks.extend(tasks)

        # Run all database save tasks
        if all_tasks:
            await asyncio.gather(*all_tasks)
    except Exception as e:
        print(f"Error updating Maxi: {e}")
        return False
    return True


if __name__ == "__main__":
    asyncio.run(update_maxi())
