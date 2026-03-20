#!/usr/bin/env python3
"""
E-commerce Web Scraper - Main Entry Point
"""

import argparse
import sys
from src.scraper import EcommerceScraper

try:
    # Ensure emoji/Unicode output works reliably on Windows terminals.
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

def main():
    parser = argparse.ArgumentParser(description='E-commerce Web Scraper')
    parser.add_argument('url', help='URL of the e-commerce website to scrape')
    parser.add_argument('--pages', type=int, default=10, help='Maximum number of pages to scrape (default: 10)')
    parser.add_argument('--format', choices=['csv', 'json', 'both'], default='csv', 
                       help='Output format (default: csv)')
    parser.add_argument('--retries', type=int, default=3, help='Maximum retry attempts (default: 3)')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--filter-price', type=float, help='Filter products below this price')
    parser.add_argument('--cache-dir', type=str, default=None, help='Optional disk cache directory')
    parser.add_argument('--cache-ttl', type=int, default=3600, help='Cache TTL in seconds (default: 3600)')
    
    args = parser.parse_args()
    
    print("Starting E-commerce Scraper")
    print(f"Target URL: {args.url}")
    print(f"Max pages: {args.pages}")
    print(f"Output format: {args.format}")
    print(f"Delay: {args.delay}s")
    print("-" * 50)
    
    try:
        # Initialize scraper
        scraper = EcommerceScraper(
            base_url=args.url,
            max_retries=args.retries,
            delay=args.delay,
            cache_dir=args.cache_dir,
            cache_ttl_seconds=args.cache_ttl if args.cache_dir else None,
        )
        
        # Scrape and save
        products = scraper.scrape_and_save(
            max_pages=args.pages,
            output_format=args.format
        )
        
        # Apply price filter if specified
        if args.filter_price and products:
            filtered_products = []
            for product in products:
                try:
                    price = float(product['price'].replace(',', '.'))
                    if price < args.filter_price:
                        filtered_products.append(product)
                except (ValueError, AttributeError):
                    continue
            
            if filtered_products:
                print(f"\nFiltered {len(filtered_products)} products below ${args.filter_price}")
                if args.format in ['csv', 'both']:
                    scraper.save_to_csv(filtered_products, 'products_filtered.csv')
                if args.format in ['json', 'both']:
                    scraper.save_to_json(filtered_products, 'products_filtered.json')
        
        # Display summary
        print("\nScraping completed!")
        print(f"Total products scraped: {len(products)}")
        
        if products:
            print("\nSample products:")
            for i, product in enumerate(products[:3], 1):
                print(f"{i}. {product['name'][:50]}... - ${product['price']}")
        
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
