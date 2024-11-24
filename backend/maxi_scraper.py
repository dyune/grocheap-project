from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

DEMO_URLS = [
    "https://www.maxi.ca/en/food/fruits-vegetables/c/28000",
    "https://www.maxi.ca/en/food/meat/c/27998",
    "https://www.maxi.ca/en/food/natural-and-organic/dairy-and-eggs/c/59391"
]


def first_layer_parsing(url):
    driver = webdriver.Chrome()

    # Navigate to the URL
    driver.get(url)

    # Wait for the content to load (adjust the selector for a visible element on the page)
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

    # Find all anchor tags with the specified class
    anchors = soup.find_all("a", class_="chakra-linkbox__overlay")
    if anchors:
        print(f"Found {len(anchors)} anchor tags:")
        for anchor in anchors:
            print(anchor.get("href"))
    else:
        print("No anchor tags found with the specified class.")

    # Close the browser
    driver.quit()


for link in DEMO_URLS:
    first_layer_parsing(link)
