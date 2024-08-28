import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
import mimetypes

def fetch_images(query, num_images=500):
    url = f"https://www.bing.com/images/search?q={query.replace(' ', '+')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    img_urls = []
    for img_tag in soup.find_all("img"):
        img_url = img_tag.get("src")
        if img_url and not img_url.startswith("data:"):  # Skip data URLs
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

            # Determine the image format using PIL
            img = Image.open(BytesIO(img_data))
            img_format = img.format.lower()

            # If the format is not recognized, fall back to the content type method
            if img_format not in ['jpeg', 'png', 'gif']:
                content_type = requests.head(img_url).headers.get("content-type")
                img_format = mimetypes.guess_extension(content_type.split(";")[0]).lstrip(".")

            img.save(f"{directory}/{query}_{i}.{img_format}")
            print(f"Saved image {i+1} as {query}_{i}.{img_format}")
        except Exception as e:
            print(f"Could not save {img_url}: {e}")

if __name__ == "__main__":
    query = "cigar"
    fetch_images(query, num_images=500)
