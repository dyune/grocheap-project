import asyncio
import random
import re
import time
import requests
import xml.etree.ElementTree as ET

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from backend.services.scrapers.scraper_utils import create_db_item, save_products_to_db

ua = UserAgent()
chrome_options = Options()
chrome_options.add_argument(f"user-agent={ua.random}")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")


SITEMAP_URL = 'https://www.maxi.ca/sitemap.xml'


def fetch_all_root():
    response = requests.get(SITEMAP_URL)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        l3_links = []

        for url in root.findall('ns:url', namespaces):
            loc = url.find('ns:loc', namespaces).text

            if (loc.startswith('https://www.maxi.ca/en/food/')
            ) and '/c/' in loc and '?navid=flyout-L3-' in loc:
                l3_links.append(loc)

        return l3_links

    else:
        print(f"Failed to retrieve the sitemap: HTTP {response.status_code}")


def open_page(url, driver):

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
    return html


def open_root(url, driver):
    html = open_page(url, driver)
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find('nav', {'aria-label': 'Pagination'})

    if pagination is None:
        return [url]

    page_links = pagination.find_all('a', {'aria-label': lambda x: x and x.startswith('Page')})
    print(page_links)
    page_numbers = [int(link.text) for link in page_links]
    max_page = max(page_numbers)

    base_url = url + "&page={}"
    page_urls = [base_url.format(page) for page in range(1, max_page + 1)]

    for url in page_urls:
        print(url)

    return page_urls


def first_layer_parsing(url, driver):
    """Scrape the data from the page."""

    links = open_root(url, driver)
    products = []

    for lnk in links:
        html = open_page(lnk, driver)
        soup = BeautifulSoup(html, "html.parser")
        divs = soup.find_all('div', {'class': 'chakra-linkbox css-yxqevf'})
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

        for link in fetch_all_root():
            products = first_layer_parsing(link, driver)
            all_products.extend(products)

        if all_products:
            save_products_to_db(all_products)

    except Exception as e:
        print(f"Error updating Maxi: {e}")
        return False

    return True


if __name__ == "__main__":
    asyncio.run(update_maxi())
