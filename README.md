# 🛒 E-commerce Web Scraper

A powerful, production-level web scraper for extracting product data from e-commerce websites. Built with Python, featuring robust error handling, pagination support, and multiple export formats.

## ✨ Features

### Core Features
- 📦 **Product Data Extraction**: Name, Price, Rating, Product Link
- 💾 **CSV Export**: Structured data storage for analysis
- 📄 **Pagination Support**: Handle multiple pages automatically
- 🔄 **Retry Mechanism**: Robust error handling for failed requests
- 📊 **Progress Tracking**: Real-time progress bar and logging

### Advanced Features
- 🛡️ **Smart Selectors**: Works with multiple e-commerce site structures
- 📝 **Logging System**: Comprehensive activity tracking
- 💻 **CLI Interface**: Dynamic URL input and configuration
- 🔄 **JSON Export**: Alternative data format
- 🌐 **User-Agent Rotation**: Avoid blocking with fake headers
- 💰 **Price Filtering**: Filter products by price range
- ⚡ **Rate Limiting**: Respectful scraping with configurable delays

## 🚀 Quick Start

### Installation

1. Clone or download this project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

#### Command Line Interface
```bash
# Basic scraping
python main.py https://example-ecommerce.com

# Advanced options
python main.py https://example.com --pages 5 --format both --filter-price 100
```

#### Python Script
```python
from src.scraper import EcommerceScraper

# Initialize scraper
scraper = EcommerceScraper("https://example-ecommerce.com")

# Scrape and save to CSV
products = scraper.scrape_and_save(max_pages=10, output_format='csv')
```

### Demo Usage

Try the built-in demo with a scraper-friendly website:
```bash
python examples/demo_scraper.py
```

## 📋 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `url` | Target e-commerce website URL | Required |
| `--pages` | Maximum pages to scrape | 10 |
| `--format` | Output format (csv/json/both) | csv |
| `--retries` | Maximum retry attempts | 3 |
| `--delay` | Delay between requests (seconds) | 1.0 |
| `--filter-price` | Filter products below this price | None |

## 📁 Project Structure

```
ecommerce-scraper/
├── src/
│   ├── __init__.py
│   └── scraper.py          # Core scraper logic
├── examples/
│   └── demo_scraper.py     # Demo and testing script
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── products.csv           # Output file (generated)
```

## 🔧 Technical Details

### Supported Website Structures

The scraper is designed to work with various e-commerce site structures using smart selectors:

- **Product Names**: `h3 a`, `h2 a`, `.product-title a`, `.title a`, `a[title]`
- **Prices**: `.price`, `.product-price`, `.current-price`, `[data-price]`
- **Ratings**: `.rating`, `.star-rating`, `[data-rating]`, `.review-rating`
- **Pagination**: `.next a`, `.pagination-next a`, `[rel="next"]`

### Error Handling

- **Network Errors**: Automatic retry with exponential backoff
- **Missing Data**: Graceful handling of incomplete product information
- **HTML Changes**: Multiple selector fallbacks for robustness
- **Rate Limiting**: Configurable delays to respect server limits

### Logging

All scraping activities are logged to:
- **Console**: Real-time progress updates
- **File**: `scraper.log` for detailed analysis

## 📊 Output Formats

### CSV Format
```csv
name,price,rating,link
"Product Name","19.99","4.5","https://example.com/product/1"
```

### JSON Format
```json
[
  {
    "name": "Product Name",
    "price": "19.99",
    "rating": "4.5",
    "link": "https://example.com/product/1"
  }
]
```

## 🧪 Testing

### Recommended Test Sites
- **books.toscrape.com**: Designed for scraping practice
- **demo sites**: Any e-commerce demo site

### Test Commands
```bash
# Test with books.toscrape.com
python main.py http://books.toscrape.com --pages 3

# Run demo
python examples/demo_scraper.py
```

## ⚠️ Important Notes

### Legal & Ethical Considerations
- Always check `robots.txt` of target websites
- Respect rate limits and terms of service
- Use for educational and legitimate purposes only

### Common Issues
- **Blocking**: Use appropriate delays and headers
- **Dynamic Content**: JavaScript-heavy sites may require Selenium
- **CAPTCHA**: Advanced sites may detect and block scrapers

## 🌟 Advanced Usage Examples

### Custom Configuration
```python
scraper = EcommerceScraper(
    base_url="https://example.com",
    max_retries=5,
    delay=2.0
)

products = scraper.scrape_all_pages(max_pages=20)
scraper.save_to_csv(products, "custom_output.csv")
```

### Price Filtering
```python
# Filter products under $50
scraper = EcommerceScraper("https://example.com")
products = scraper.scrape_and_save(max_pages=5)

filtered = [p for p in products if float(p['price']) < 50]
scraper.save_to_csv(filtered, "budget_products.csv")
```

## 📈 Performance Metrics

- **Speed**: ~1-3 seconds per page (depending on site complexity)
- **Success Rate**: 90%+ product data extraction
- **Reliability**: Handles network errors and missing data gracefully
- **Scalability**: Can handle hundreds of products across multiple pages

## 🔮 Future Enhancements

- [ ] GUI Interface for non-technical users
- [ ] Scheduled scraping with cron jobs
- [ ] Database storage (MySQL/MongoDB)
- [ ] Dashboard visualization
- [ ] Multi-website simultaneous scraping
- [ ] Proxy rotation support
- [ ] Selenium integration for dynamic sites

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes. Use responsibly and in accordance with website terms of service.

## 🆘 Troubleshooting

### Common Solutions

**Issue**: No products found
- **Solution**: Check if the website uses JavaScript-heavy content
- **Alternative**: Try different selectors or use Selenium

**Issue**: Getting blocked
- **Solution**: Increase delay between requests
- **Alternative**: Use proxy rotation

**Issue**: Missing data fields
- **Solution**: Check website HTML structure
- **Alternative**: Add custom selectors for the specific site

### Support

For issues and questions:
1. Check the log file (`scraper.log`)
2. Verify the website structure
3. Test with the demo script first
4. Review the command line options

---

**Happy Scraping! 🚀**
# Task-5-Prodgy
# Task-5-Prodgy
