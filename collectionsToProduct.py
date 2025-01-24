import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random
import os
from fake_useragent import UserAgent

with open("collections.json", "r", encoding="utf-8") as json_file:
    categories = json.load(json_file)

ua = UserAgent()

output_file = "products.json"

# Initialize JSON file if it doesn't exist
if not os.path.exists(output_file):
    with open(output_file, "w") as file:
        json.dump([], file)  # Start with an empty JSON array

def clean_price(price_str):
    cleaned_str = re.sub(r"[^\d,]", "", price_str)  # Remove non-numeric characters
    cleaned_str = cleaned_str.replace(",", "")      # Remove commas
    return int(cleaned_str) if cleaned_str else 0   # Convert to integer

# Function to append data to JSON file
def append_to_json_file(file_path, data):
    # Read existing content
    with open(file_path, "r", encoding="utf-8") as file:
        existing_data = json.load(file)

    # Append new data
    existing_data.extend(data)

    # Write back to the file with utf-8 encoding
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)

def scrape_category(category):
    base_url = category["link"]
    total_products = category["amount"]
    scraped_products = 0
    page = 1
    products = []

    while scraped_products < total_products:
        paginated_url = f"{base_url}?page={page}"
        headers = {"User-Agent": ua.random}
        print(f"Scraping: {paginated_url}")

        response = requests.get(paginated_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch {paginated_url}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        product_elements = soup.select(".product-card")

        for product in product_elements:
            raw_price = product.select_one(".price__regular").text.strip() if product.select_one(".price__regular") else "0"
            raw_discount = product.select_one(".price__sale").text.strip() if product.select_one(".price__sale") else "0"

            product_info = {
                "title": product.select_one(".product-card__heading").text.strip() if product.select_one(".product-card__heading") else "Unknown",
                "price": clean_price(raw_price),
                "discount": clean_price(raw_discount),
                "link": f"https://sample.xx{product.select_one('.product-card__image')['href']}" if product.select_one(".product-card__image") else "Unknown",
                "img": f"https:{product.select_one('.image-show--fadein')['src']}" if product.select_one(".image-show--fadein") else "Unknown",
                "category": category["title"]
            }
            products.append(product_info)

        scraped_products += len(product_elements)
        print(f"Scraped {scraped_products} / {total_products} products from {category['title']}.")

        if len(product_elements) < 20 or not product_elements:
             print("No more products in this page")
             break


        page +=1
        time.sleep(random.uniform(15, 30))



    return products

for category in categories:
    category_products = scrape_category(category)
    append_to_json_file(output_file, category_products)
    print(f"Finished scraping {category['title']}, found {len(category_products)} products.")