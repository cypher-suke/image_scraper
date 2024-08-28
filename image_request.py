import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO

def fetch_images(query, num_images=100):
    url = f"https://www.example.com/search?q={query.replace(' ', '+')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    img_urls = []
    for img_tag in soup.find_all("img"):
        img_url = img_tag.get("src")
        if img_url:
            img_url = urljoin(url, img_url)
            img_urls.append(img_url)
        if len(img_urls) >= num_images:
            break

    save_images(img_urls, query)

def save_images(img_urls, query):
    directory = f"images/{query}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i, img_url in enumerate(img_urls):
        try:
            img_data = requests.get(img_url).content
            img = Image.open(BytesIO(img_data))
            img_format = img.format.lower()
            img.save(f"{directory}/{query}_{i}.{img_format}")
        except Exception as e:
            print(f"Could not save {img_url}: {e}")

if __name__ == "__main__":
    query = "puppies"
    fetch_images(query, num_images=100)
