from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up Selenium WebDriver
driver = webdriver.Chrome()

# Navigate to the URL
url = "https://www.maxi.ca/en/food/fish-seafood/c/27999"  # Replace with your URL
driver.get(url)

# Wait for the content to load (adjust the selector for a visible element on the page)
try:
    WebDriverWait(driver, 10).until(
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
