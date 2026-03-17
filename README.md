# E-commerce Product Scraper

This project contains web scrapers for extracting product data from multiple e-commerce platforms.

## Features
- Scrape product title, price, description, reviews, and images
- Supports:
  - MercadoLibre
  - Alibaba
- Saves data in CSV and Excel formats

## Technologies Used
- Python
- BeautifulSoup
- Selenium
- Pandas

## How to Run

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run scraper
python mercadolibre_scraper.py
python alibaba_scraper.py

## Output
Scraped data is saved in CSV/Excel format.

## Note
Alibaba scraper may require manual CAPTCHA solving.
