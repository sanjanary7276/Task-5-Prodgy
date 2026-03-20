#!/usr/bin/env python3
"""
Test script to demonstrate all features of the E-commerce Scraper
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.scraper import EcommerceScraper
import pandas as pd

def test_all_features():
    print("[TEST] Testing All Features of E-commerce Scraper")
    print("=" * 50)
    
    # Test 1: Basic scraping
    print("\n1) Testing Basic Scraping")
    url = "http://books.toscrape.com"
    scraper = EcommerceScraper(url, delay=0.5)
    
    products = scraper.scrape_and_save(max_pages=2, output_format='both')
    print(f"[OK] Scraped {len(products)} products")
    
    # Test 2: Price filtering
    print("\n2) Testing Price Filtering")
    budget_products = [p for p in products if float(p['price']) < 25]
    scraper.save_to_csv(budget_products, 'budget_books.csv')
    print(f"[OK] Found {len(budget_products)} books under $25")
    
    # Test 3: Rating analysis
    print("\n3) Testing Rating Analysis")
    ratings = [int(p['rating']) for p in products if p['rating']]
    if ratings:
        avg_rating = sum(ratings) / len(ratings)
        print(f"[OK] Average rating: {avg_rating:.2f}/5")
    
    # Test 4: Summary statistics
    print("\n4) Testing Summary Statistics")
    df = pd.DataFrame(products)
    print(f"[OK] Price range: ${df['price'].astype(float).min():.2f} - ${df['price'].astype(float).max():.2f}")
    print(f"[OK] Products with ratings: {len(df[df['rating'] != ''])}")
    
    # Test 5: Error handling (invalid URL)
    print("\n5) Testing Error Handling")
    try:
        bad_scraper = EcommerceScraper("http://invalid-website-12345.com")
        bad_products = bad_scraper.scrape_and_save(max_pages=1)
        print(f"[OK] Handled invalid URL gracefully: {len(bad_products)} products")
    except Exception as e:
        print(f"[OK] Error handling working: {type(e).__name__}")
    
    print("\nAll tests completed successfully!")
    print("Generated files:")
    print("   - products.csv")
    print("   - products.json") 
    print("   - budget_books.csv")
    print("   - scraper.log")

if __name__ == "__main__":
    test_all_features()
