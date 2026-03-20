import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from fake_useragent import UserAgent
from urllib.parse import urljoin, urlparse
import re
from typing import List, Dict, Optional
from tqdm import tqdm

class EcommerceScraper:
    def __init__(self, base_url: str, max_retries: int = 3, delay: float = 1.0):
        self.base_url = base_url
        self.max_retries = max_retries
        self.delay = delay
        self.session = requests.Session()
        self.ua = UserAgent()
        self.session.headers.update({'User-Agent': self.ua.random})
        self.products = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def make_request(self, url: str) -> Optional[BeautifulSoup]:
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"Requesting: {url} (Attempt {attempt + 1})")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                self.logger.info(f"Successfully fetched: {url}")
                return soup
                
            except requests.RequestException as e:
                self.logger.warning(f"Request failed for {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay * (attempt + 1))
                else:
                    self.logger.error(f"Max retries reached for {url}")
                    return None

    def extract_product_info(self, product_element, base_url: str) -> Dict[str, str]:
        product = {
            'name': '',
            'price': '',
            'rating': '',
            'link': ''
        }
        
        try:
            # Extract product name (common selectors)
            name_selectors = ['h3 a', 'h2 a', '.product-title a', '.title a', 'a[title]']
            for selector in name_selectors:
                name_elem = product_element.select_one(selector)
                if name_elem:
                    product['name'] = name_elem.get_text(strip=True) or name_elem.get('title', '').strip()
                    break
            
            # Extract price (common selectors)
            price_selectors = ['.price', '.product-price', '.current-price', '[data-price]', '.price-current']
            for selector in price_selectors:
                price_elem = product_element.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    # Clean price text (remove currency symbols, etc.)
                    price_text = re.sub(r'[^\d.,]', '', price_text)
                    product['price'] = price_text
                    break
            
            # Extract rating (common selectors)
            rating_selectors = ['.rating', '.star-rating', '[data-rating]', '.review-rating']
            for selector in rating_selectors:
                rating_elem = product_element.select_one(selector)
                if rating_elem:
                    rating_text = rating_elem.get_text(strip=True)
                    # Extract numeric rating
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        product['rating'] = rating_match.group(1)
                    break
            
            # Extract product link
            link_elem = product_element.select_one('a[href]')
            if link_elem:
                href = link_elem.get('href', '')
                product['link'] = urljoin(base_url, href)
            
            # Log if any field is missing
            missing_fields = [k for k, v in product.items() if not v]
            if missing_fields:
                self.logger.debug(f"Missing fields for product: {missing_fields}")
                
        except Exception as e:
            self.logger.error(f"Error extracting product info: {e}")
        
        return product

    def extract_books_to_scrape_info(self, product_element, base_url: str) -> Dict[str, str]:
        """Specialized extractor for books.toscrape.com"""
        product = {
            'name': '',
            'price': '',
            'rating': '',
            'link': ''
        }
        
        try:
            # Extract product name
            name_elem = product_element.select_one('h3 a')
            if name_elem:
                product['name'] = name_elem.get('title', '').strip()
                href = name_elem.get('href', '')
                product['link'] = urljoin(base_url, href)
            
            # Extract price
            price_elem = product_element.select_one('.price_color')
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                # Remove £ symbol and clean
                price_text = re.sub(r'[^\d.,]', '', price_text)
                product['price'] = price_text
            
            # Extract rating (star rating)
            rating_elem = product_element.select_one('p.star-rating')
            if rating_elem:
                rating_class = rating_elem.get('class', [])
                # Look for rating classes like 'star-rating Three', 'star-rating Four', etc.
                for cls in rating_class:
                    if cls.lower() in ['one', 'two', 'three', 'four', 'five']:
                        rating_map = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5'}
                        product['rating'] = rating_map.get(cls.lower(), '')
                        break
            
            # Log if any field is missing
            missing_fields = [k for k, v in product.items() if not v]
            if missing_fields:
                self.logger.debug(f"Missing fields for book: {missing_fields}")
                
        except Exception as e:
            self.logger.error(f"Error extracting book info: {e}")
        
        return product

    def scrape_page(self, url: str) -> List[Dict[str, str]]:
        soup = self.make_request(url)
        if not soup:
            return []
        
        products = []
        
        # Special handling for books.toscrape.com
        if 'books.toscrape.com' in url:
            product_elements = soup.select('article.product_pod')
            if product_elements:
                self.logger.info(f"Found {len(product_elements)} books using books.toscrape.com selector")
                for element in product_elements:
                    product = self.extract_books_to_scrape_info(element, self.base_url)
                    if product['name']:
                        products.append(product)
                return products
        
        # Common product container selectors for other sites
        product_selectors = [
            '.product', '.product-item', '.item', '.book', 
            '[data-product]', '.product-card', '.listing-item'
        ]
        
        product_elements = []
        for selector in product_selectors:
            elements = soup.select(selector)
            if elements:
                product_elements = elements
                self.logger.info(f"Found {len(elements)} products using selector: {selector}")
                break
        
        if not product_elements:
            self.logger.warning("No products found on the page")
            return []
        
        for element in product_elements:
            product = self.extract_product_info(element, self.base_url)
            if product['name']:  # Only add if we have at least a name
                products.append(product)
        
        return products

    def find_next_page(self, soup, current_url: str) -> Optional[str]:
        # Special handling for books.toscrape.com
        if 'books.toscrape.com' in current_url:
            next_elem = soup.select_one('li.next a')
            if next_elem:
                href = next_elem.get('href')
                if href:
                    return urljoin(current_url, href)
        
        # Common next page selectors
        next_selectors = [
            '.next a', '.pagination-next a', '[rel="next"]',
            '.next-page a', '.page-next a'
        ]
        
        for selector in next_selectors:
            next_elem = soup.select_one(selector)
            if next_elem:
                href = next_elem.get('href')
                if href:
                    return urljoin(current_url, href)
        
        return None

    def scrape_all_pages(self, max_pages: int = 10) -> List[Dict[str, str]]:
        current_url = self.base_url
        page_count = 0
        all_products = []
        
        with tqdm(desc="Scraping pages", unit="page") as pbar:
            while current_url and page_count < max_pages:
                self.logger.info(f"Scraping page {page_count + 1}: {current_url}")
                
                products = self.scrape_page(current_url)
                all_products.extend(products)
                
                # Update progress bar with product count
                pbar.set_description(f"Scraping pages (Products: {len(all_products)})")
                pbar.update(1)
                
                # Find next page
                soup = self.make_request(current_url)
                if soup:
                    next_url = self.find_next_page(soup, current_url)
                    if next_url and next_url != current_url:
                        current_url = next_url
                        page_count += 1
                        time.sleep(self.delay)  # Be respectful to the server
                    else:
                        self.logger.info("No more pages found")
                        break
                else:
                    self.logger.error("Failed to fetch page for pagination")
                    break
        
        self.logger.info(f"Total products scraped: {len(all_products)}")
        return all_products

    def save_to_csv(self, products: List[Dict[str, str]], filename: str = 'products.csv'):
        if not products:
            self.logger.warning("No products to save")
            return
        
        df = pd.DataFrame(products)
        df.to_csv(filename, index=False, encoding='utf-8')
        self.logger.info(f"Saved {len(products)} products to {filename}")

    def save_to_json(self, products: List[Dict[str, str]], filename: str = 'products.json'):
        if not products:
            self.logger.warning("No products to save")
            return
        
        df = pd.DataFrame(products)
        df.to_json(filename, orient='records', indent=2, force_ascii=False)
        self.logger.info(f"Saved {len(products)} products to {filename}")

    def scrape_and_save(self, max_pages: int = 10, output_format: str = 'csv'):
        self.logger.info(f"Starting scrape of {self.base_url}")
        
        products = self.scrape_all_pages(max_pages)
        
        if products:
            if output_format.lower() == 'csv':
                self.save_to_csv(products)
            elif output_format.lower() == 'json':
                self.save_to_json(products)
            else:
                self.save_to_csv(products)
                self.save_to_json(products)
        else:
            self.logger.warning("No products were scraped")
        
        return products
