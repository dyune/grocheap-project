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

from db_utils import save_product_to_db, create_db_item, save_products_to_db

# Configure Chrome for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# URLs of the SuperC pages
DEMO_URLS = [
    ("https://www.superc.ca/en/aisles/fruits-vegetables", 21),
    ("https://www.superc.ca/en/aisles/dairy-eggs", 31),
    ("https://www.superc.ca/en/aisles/pantry", 85),
    ("https://www.superc.ca/en/aisles/meat-poultry", 13)
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
    db_products = []

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
    products = soup.find_all("div", class_="default-product-tile")

    for product in products:
        try:
            brand = product.get("data-product-brand", "No brand")
            name = product.get("data-product-name", None)

            url_tag = product.find("a", class_="product-details-link")
            product_url = "https://www.superc.ca" + url_tag.get("href") if url_tag else "URL not found"

            # TODO: Implement better sanitizing
            price_tag = product.find("span", class_="price-update")
            price = (
                float(price_tag.text.strip().replace("$", "")) if price_tag else None
            )  # Convert price to float
            # print(price)

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
                db_item = create_db_item(
                    name,
                    brand,
                    product_url,
                    image,
                    size,
                    1,
                    price,
                )
                if db_item:
                    db_products.append(db_item)

        except Exception as e:
            print(f"Parsing error, unable to save: {e}")

        finally:
            continue

    return db_products


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


async def batch_insert_superc(urls):
    """Gather SuperC products."""
    driver = webdriver.Chrome(options=chrome_options)  # Set up the WebDriver
    items = []

    try:
        print(DEMO_URLS)
        for url in urls:
            result = await first_layer_parsing(url, driver)
            items.extend(result)
            print(items)

        if items:
            await save_products_to_db(items)
            print(f"Successfully saved {len(items)} products to the database.")

    except Exception as e:
        print(f"Error during update: {e}")

    finally:
        driver.quit()  # Ensure the browser is closed


if __name__ == "__main__":
    tracemalloc.start()
    urls = []
    for elem in DEMO_URLS:
        urls.extend(
            iterate_through_pages(elem[0], elem[1])
        )
    print(urls)
    print(urls)
    asyncio.run(batch_insert_superc(urls))
