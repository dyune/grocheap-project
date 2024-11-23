import requests
from bs4 import BeautifulSoup
import json


class Scraper:
    def __init__(self, base_url):
        """
        Initialize the Scraper with a base URL.
        """
        self.base_url = base_url

    def fetch_page(self, url):
        """
        Fetch a webpage's HTML content.
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

    def parse_page(self, html_content):
        """
        Parse HTML content and extract product data.
        """
        soup = BeautifulSoup(html_content, "html.parser")

        # Example: Customize this to match the target website's structure
        product_elements = soup.find_all("div", class_="product-card")
        products = []
        for product in product_elements:
            try:
                name = product.find("span", class_="product-name").text.strip()
                price = (
                    product.find("span", class_="product-price")
                    .text.strip()
                    .replace("$", "")
                )
                products.append({"name": name, "price": float(price)})
            except AttributeError:
                # Skip products missing name or price
                continue

        return products

    def scrape(self, path):
        """
        Orchestrates the scraping process for a specific URL path.
        """
        url = f"{self.base_url}/{path}"
        print(f"Scraping URL: {url}")

        html_content = self.fetch_page(url)
        if html_content:
            data = self.parse_page(html_content)
            return data
        else:
            return None

    def save_to_file(self, data, filename="products.json"):
        """
        Save scraped data to a JSON file.
        """
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")


# Example usage
if __name__ == "__main__":
    # Update the base URL to match the target grocery store
    base_url = "https://example-grocery-store.com"
    scraper = Scraper(base_url)

    # Update the path to match the specific page you're scraping
    data = scraper.scrape("search?q=milk")

    if data:
        scraper.save_to_file(data)
        print(f"Scraped {len(data)} products.")
    else:
        print("No data scraped.")
