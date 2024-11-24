from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Headers to simulate a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

# URL of the Super C search page
URL = "https://www.superc.ca/en/aisles/baby/food-formula/cereal/multigrain-oatmeal-with-fruit-baby-cereal/p/065000138160"

# Fetch the webpage
webpage = requests.get(URL, headers=HEADERS)

# Print the entire HTML of the page
print("Entire HTML Content:\n")
# Parse the webpage with BeautifulSoup
soup = BeautifulSoup(webpage.content, "html")
print(soup)  # Prettifies the output for better readability
# Find all product links that contain 'data-main-price' attribute
links = soup.find("h1", attrs={'class':'pi--title'})

print(links)
# List to store extracted data
list_links = []






#
# # # Scrape IGA (asynchronous)
# # async def scrape_iga(search_term):
# #
# #
# #
# # # Scrape Super C (asynchronous)
# # async def scrape_super_c(search_term):
# #
# #
# #
# # # Scrape Maxi (asynchronous)
# # async def scrape_maxi(search_term):
# #
# #
# #
# # # Update prices in the database
# # async def update_prices(store_name, scraper_function, search_term):
# #
# #
# #
# #
# # def main():
# #
# #
# #
# # if __name__ == "__main__":
# #     main()


