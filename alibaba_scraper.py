import undetected_chromedriver as uc
import time

options = uc.ChromeOptions()
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
driver = uc.Chrome(options=options)

driver.get("https://www.alibaba.com/trade/search?SearchText=your+product")
time.sleep(10)  # Wait and solve CAPTCHA manually if it appears

# Continue scraping after CAPTCHA solved manually or with 3rd-party service

driver.quit()
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Path to Brave browser executable
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Update if needed

# Set up Selenium with Brave
chrome_options = Options()
chrome_options.binary_location = brave_path
chrome_options.add_argument("--start-maximized")  # Optional: start maximized
# chrome_options.add_argument("--headless")  # Uncomment for headless mode

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

search_query = input("Enter the product you want to search for: ")
search_url = f"https://www.alibaba.com/trade/search?SearchText={search_query.replace(' ', '+')}"

driver.get(search_url)
time.sleep(5)  # Wait for the page to load

product_data_list = []

# Scrape the first 3 pages
for page in range(1, 4):
    print(f"Scraping page {page}...")
    time.sleep(3)  # Wait for content to load

    products = driver.find_elements(By.CSS_SELECTOR, "div.search-card-info__wrapper")
    for product in products:
        try:
            name = product.find_element(By.CSS_SELECTOR, ".search-card-e-title a span").text.strip()
        except:
            name = ""
        try:
            price = product.find_element(By.CSS_SELECTOR, ".search-card-e-price-main").text.strip()
        except:
            price = ""
        try:
            description = product.find_element(By.CSS_SELECTOR, ".search-card-e-sell-point").text.strip()
        except:
            description = ""
        try:
            moq = product.find_element(By.CSS_SELECTOR, ".search-card-m-sale-features__item").text.strip()
        except:
            moq = ""
        try:
            rating = product.find_element(By.CSS_SELECTOR, ".search-card-e-review strong").text.strip()
        except:
            rating = ""

        product_data_list.append({
            "Product Name": name,
            "Price": price,
            "Description": description,
            "MOQ": moq,
            "Rating": rating
        })

    # Go to next page if exists
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "button.pagination-item")
        driver.execute_script("arguments[0].click();", next_button)
    except:
        print("No more pages or next button not found.")
        break

driver.quit()

# Save to Excel
df = pd.DataFrame(product_data_list)
excel_filename = f"{search_query.replace(' ', '_')}_alibaba.xlsx"
df.to_excel(excel_filename, index=False)
print(f"Scraped data saved to {excel_filename}")
