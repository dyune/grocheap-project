import asyncio
import time
import tracemalloc
from typing import List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from db_utils import save_product_to_db

# Configure Chrome for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# URLs of the SuperC pages
DEMO_URLS = [
    "https://www.superc.ca/en/aisles/fruits-vegetables/fruits",
    "https://www.superc.ca/en/aisles/fruits-vegetables/vegetables",
    "https://www.superc.ca/en/aisles/meat-poultry/beef-veal",
]


def iterate_through_pages(link: str, max_pages: int) -> List[str]:
    index = 1
    pages = []
    while index <= max_pages:
        if index == 1:
            pages.append(link)
        else:
            paginated_link = link + f"-page-{index}"
            pages.append(paginated_link)
        index += 1
    return pages


async def first_layer_parsing(url, driver):
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
        return []  # Return an empty list of async tasks to do.

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
        try:
            # Extract data for each product
            brand = product.get("data-product-brand", "No brand")
            name = product.get("data-product-name", None)

            url_tag = product.find("a", class_="product-details-link")
            product_url = "https://www.superc.ca" + url_tag.get("href") if url_tag else "URL not found"

            price_tag = product.find("span", class_="price-update")
            price = (
                float(price_tag.text.strip().replace("$", "")) if price_tag else None
            )  # Convert price to float
            print(price)

            size_tag = product.find("span", class_="head__unit-details")
            if size_tag:
                size = size_tag.text.strip()
            else:
                size_alt_tag = product.find("span", class_="unit-update")
                size = size_alt_tag.text.strip() if size_alt_tag else "None"

            image_tag = product.find("img", alt=True)
            image = image_tag.get("src") if image_tag else "Image not found"

            # Print product details
            # print(f"Product Brand: {brand}")
            # print(f"Product Name: {name}")
            # print(f"Product Price: {price}")
            # print(f"Product Size: {size}")
            # print(f"Product URL: {product_url}")
            # print(f"Product Image: {image}")
            # print("-" * 50)

            # Create an asyncio task to save the product
            if name and product_url and price is not None:
                tasks.append(
                    save_product_to_db(
                        name,
                        brand,
                        product_url,
                        image,
                        size,
                        1,
                        price,
                    )
                )

        except Exception as e:
            print(f"Parsing error, unable to save: {e}")

        finally:
            continue

    return tasks


async def gather_superc():
    """Gather SuperC products."""
    driver = webdriver.Chrome(options=chrome_options)  # Set up the WebDriver
    all_tasks = []

    try:
        print(DEMO_URLS)
        for url in DEMO_URLS:
            print(tracemalloc.take_snapshot())
            tasks = await first_layer_parsing(url, driver)
            all_tasks.extend(tasks)

        # Run all database save tasks
        if all_tasks:
            await asyncio.gather(*all_tasks)

    except Exception as e:
        print(f"Error during update: {e}")

    finally:
        driver.quit()  # Ensure the browser is closed


async def update_superc():
    pass


if __name__ == "__main__":
    tracemalloc.start()
    ls = iterate_through_pages("https://www.superc.ca/en/aisles/fruits-vegetables", 21)
    print(ls)
    DEMO_URLS += ls
    asyncio.run(gather_superc())
