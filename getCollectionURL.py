import requests
from bs4 import
import json
import re

# URL to scrape
url = "https://sample.xx/collections/"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the webpage content
    soup = BeautifulSoup(response.text, "html.parser")

    collections = soup.select(".collection-list-type2")

    data = []

    for element in collections:
        link = element.get("href", "")

        title_el = element.select_one(".h5")
        title = title_el.text.strip() if title_el else ""

        amount_el = element.select_one(".body2")
        amount_txt = amount_el.text.strip() if amount_el else ""

        amount_match = re.search(r"\d+", amount_txt)
        amount = int(amount_match.group()) if amount_match else 0

        data.append({"link": 'https://sample.xx'+link, "title": title, "amount": amount})
        print(f"link: https://sample.xx{link}, title: {title}, amount: {amount}")
    with open("collections.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")