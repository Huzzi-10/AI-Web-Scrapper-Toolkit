# Library Files
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# User Input
search_query = input("Enter the product to search: ").strip()
max_items = int(input("How many products to scrape? ").strip())

# Initialize
base_url = "https://listado.mercadolibre.com.mx/"
search_url = f"{base_url}{search_query.replace(' ', '-')}"
headers = {'User-Agent': 'Mozilla/5.0'}

# as while loop is using so we initialize it with 0
data = []
items_scraped = 0
offset = 0

# Loop through pages
while items_scraped < max_items:
    url = f"{search_url}_Desde_{offset + 1}" if offset > 0 else search_url
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_cards = soup.select('div.ui-search-result__wrapper')

    if not product_cards:
        print("❌ No more products found.")
        break

    # Loop through products
    for product in product_cards:
        if items_scraped >= max_items:
            break

        # products selectors after website inspection
        title_tag = product.select_one('a.poly-component__title')
        price_tag = product.select_one('span.andes-money-amount__fraction')
        des_tag = product.select_one('h3.poly-component__title-wrapper')
        review_tag = product.select_one('div.poly-component__reviews')
        image_tag = product.select_one('img.poly-component__picture')

        # giving products data to varaible
        title = title_tag.text.strip() if title_tag else 'N/A'
        price = price_tag.text.strip() if price_tag else 'N/A'
        description = des_tag.text.strip() if des_tag else 'N/A'
        review = review_tag.text.strip() if review_tag else 'N/A'
        image = image_tag['src'] if image_tag and 'src' in image_tag.attrs else 'N/A'

        # columns Name
        data.append({
            'Product Title': title,
            'Price in Dollars': price,
            'Product Description': description,
            'Product Review': review,
            'Product Image': image,
        })
        items_scraped += 1

    offset += 50  # Usually 50 products per page
    time.sleep(1)  # Be polite, don't hammer the server

# Save to CSV and Excel
df = pd.DataFrame(data)

# path of user pc
csv_path = 'C:/Users/Huzaifa Asad/Desktop/scraped_data.csv'
excel_path = 'C:/Users/Huzaifa Asad/Desktop/scraped_data.xlsx'

# convert into excal and csv file
df.to_csv(csv_path, index=False)
df.to_excel(excel_path, index=False)

# statement after succesfull run of program
print(f"Scraping Done! {items_scraped} items saved to Desktop.")
