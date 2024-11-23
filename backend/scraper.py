import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup
from lxml import etree


# Base Scraper Class
class BaseScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_page(self, url):
        """
        Fetch the HTML or XML content of a page.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}: {response.status_code}")
            return None


# Store-Specific Scrapers
class MaxiScraper(BaseScraper):
    def parse_xml(self, xml_content):
        """
        Parse Maxi's XML content to extract product descriptions.
        """
        root = ET.fromstring(xml_content)
        products = []
        for product in root.findall(".//product"):
            try:
                name = product.find("name").text
                description = product.find("description").text
                products.append({"name": name, "description": description})
            except AttributeError:
                continue
        return products


class SuperCScraper(BaseScraper):
    def parse_xml(self, xml_content):
        """
        Parse Super C's XML content to extract product descriptions.
        """
        root = etree.fromstring(xml_content)
        products = []
        for product in root.xpath("//product"):
            try:
                name = product.xpath("name/text()")[0]
                description = product.xpath("description/text()")[0]
                products.append({"name": name, "description": description})
            except IndexError:
                continue
        return products


class IGAScraper(BaseScraper):
    def parse_xml(self, xml_content):
        """
        Parse IGA's XML content to extract product descriptions.
        """
        soup = BeautifulSoup(xml_content, "xml")  # Use BeautifulSoup for XML
        products = []
        product_elements = soup.find_all("product")
        for product in product_elements:
            try:
                name = product.find("name").text
                description = product.find("description").text
                products.append({"name": name, "description": description})
            except AttributeError:
                continue
        return products


# Scraper Function
def scraper(store_name, query):
    """
    Scraper function that selects the scraper for a store, fetches data,
    and applies an XML filter to extract product descriptions.
    """
    scrapers = {
        "Maxi": MaxiScraper(base_url="https://www.maxi.ca"),
        "SuperC": SuperCScraper(base_url="https://www.superc.ca"),
        "IGA": IGAScraper(base_url="https://www.iga.net"),
    }

    # Select the scraper
    if store_name not in scrapers:
        raise ValueError(f"Unsupported store: {store_name}")

    scraper = scrapers[store_name]

    # Generate the path for the query
    path = f"search?q={query}"

    # Fetch and parse data
    print(f"Scraping data for {query} from {store_name}...")
    xml_content = scraper.fetch_page(f"{scraper.base_url}/{path}")
    if not xml_content:
        print("No content fetched.")
        return []

    # Apply the XML filter
    return scraper.parse_xml(xml_content)


# Example Usage
if __name__ == "__main__":
    store = "Maxi"  # Change to "SuperC" or "IGA" as needed
    query = "milk"

    try:
        products = scraper(store, query)
        if products:
            print(f"Scraped {len(products)} products from {store}:")
            for product in products:
                print(product)
        else:
            print(f"No products found for {query} at {store}.")
    except ValueError as e:
        print(e)

print(requests.__version__)
