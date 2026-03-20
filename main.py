#!/usr/bin/env python3
"""
E-commerce Web Scraper - Main Entry Point
"""

import argparse
import sys
from src.scraper import EcommerceScraper

def main():
    parser = argparse.ArgumentParser(description='E-commerce Web Scraper')
    parser.add_argument('url', help='URL of the e-commerce website to scrape')
    parser.add_argument('--pages', type=int, default=10, help='Maximum number of pages to scrape (default: 10)')
    parser.add_argument('--format', choices=['csv', 'json', 'both'], default='csv', 
                       help='Output format (default: csv)')
    parser.add_argument('--retries', type=int, default=3, help='Maximum retry attempts (default: 3)')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--filter-price', type=float, help='Filter products below this price')
    
    args = parser.parse_args()
    
    print(f"🚀 Starting E-commerce Scraper")
    print(f"📡 Target URL: {args.url}")
    print(f"📄 Max pages: {args.pages}")
    print(f"💾 Output format: {args.format}")
    print(f"⏱️  Delay: {args.delay}s")
    print("-" * 50)
    
    try:
        # Initialize scraper
        scraper = EcommerceScraper(
            base_url=args.url,
            max_retries=args.retries,
            delay=args.delay
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
                print(f"\n💰 Filtered {len(filtered_products)} products below ${args.filter_price}")
                if args.format in ['csv', 'both']:
                    scraper.save_to_csv(filtered_products, 'products_filtered.csv')
                if args.format in ['json', 'both']:
                    scraper.save_to_json(filtered_products, 'products_filtered.json')
        
        # Display summary
        print(f"\n✅ Scraping completed!")
        print(f"📊 Total products scraped: {len(products)}")
        
        if products:
            print("\n📋 Sample products:")
            for i, product in enumerate(products[:3], 1):
                print(f"{i}. {product['name'][:50]}... - ${product['price']}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
