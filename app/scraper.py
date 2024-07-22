import os
import json
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from .products import ProductCreate

class Scraper:
    def __init__(self, base_url: str, pages: int, proxy: Optional[str] = None):
        self.base_url = base_url
        self.pages = pages
        self.proxy = proxy

    def fetch_page(self, url: str) -> requests.Response:
        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
        retries = 3
        for attempt in range(retries):
            try:
                response = requests.get(url, proxies=proxies)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print(f"Error fetching page {url} (Attempt {attempt + 1}/{retries}): {e}")
                time.sleep(5)
        raise Exception(f"Failed to fetch page {url} after {retries} retries")

    def scrape(self) -> List[ProductCreate]:
        products = []
        for page in range(1, self.pages + 1):
            url = f"{self.base_url}/page/{page}"
            try:
                response = self.fetch_page(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                for item in soup.select(".product"):
                    name = item.select_one(".woo-loop-product__title").get_text(strip=True)
                    price = item.select_one(".amount").get_text(strip=True)
                    image_url = item.select_one(".mf-product-thumbnail").find("img")["data-lazy-src"]
                    products.append(ProductCreate(
                        product_title = name,
                        product_price = float(price.replace('₹', '')),
                        path_to_image = image_url
                    ))
            except Exception as e:
                print(f"Skipping page {page} due to error: {e}")
        return products


    def save_to_json(self, data: List[ProductCreate], filename: str = "products.json"):
        with open(filename, "w") as file:
            json.dump([product.model_dump() for product in data], file, indent=4)
