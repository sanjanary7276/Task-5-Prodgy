#!/usr/bin/env python3
"""
Demo script for testing the E-commerce Scraper
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scraper import EcommerceScraper

def demo_books_to_scrape():
    """Demo using books.toscrape.com (a website designed for scraping practice)"""
    print("📚 Demo: Scraping books.toscrape.com")
    
    url = "http://books.toscrape.com/"
    scraper = EcommerceScraper(url, delay=0.5)
    
    # Scrape first 3 pages as demo
    products = scraper.scrape_and_save(max_pages=3, output_format='both')
    
    print(f"✅ Demo completed! Scraped {len(products)} books")
    return products

def demo_custom_site():
    """Demo with a custom URL"""
    url = input("Enter the e-commerce website URL to scrape: ")
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    max_pages = int(input("Enter maximum pages to scrape (default 5): ") or "5")
    
    scraper = EcommerceScraper(url)
    products = scraper.scrape_and_save(max_pages=max_pages)
    
    print(f"✅ Scraped {len(products)} products")
    return products

if __name__ == "__main__":
    print("🎯 E-commerce Scraper Demo")
    print("1. Demo with books.toscrape.com (recommended for testing)")
    print("2. Custom URL")
    
    choice = input("Choose demo (1 or 2): ").strip()
    
    if choice == "1":
        demo_books_to_scrape()
    elif choice == "2":
        demo_custom_site()
    else:
        print("❌ Invalid choice")
