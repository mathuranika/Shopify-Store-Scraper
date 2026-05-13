# Shopify Store Scraper

A comprehensive tool for scraping and extracting product information from Shopify-powered e-commerce stores. This project is designed to help developers, analysts, and e-commerce professionals collect structured data such as product titles, prices, images, descriptions, and inventory details from Shopify storefronts.

## Features

- **Automated scraping** of publicly accessible Shopify product listings
- Extraction of key product information:
  - Titles
  - Prices
  - Images
  - Descriptions
  - Inventory status
  - Variants and options
- Flexible output formats (e.g., CSV, JSON)
- Easy configuration for scraping multiple stores or custom domains
- Supports pagination and large inventories
- User-friendly CLI or API integration (customize as needed)
- Error handling and store-access failover

## Installation

Clone the repository:

```bash
git clone https://github.com/mathuranika/Shopify-Store-Scraper.git
cd Shopify-Store-Scraper
```

**(Optional)** Install dependencies if applicable (e.g., via `pip`, `npm`, etc.):

```bash
# For Python projects
pip install -r requirements.txt

# For Node.js projects
npm install
```

## Usage

```bash
# Basic example (customize based on your actual interface)
python scraper.py --store_url https://examplestore.myshopify.com --output products.csv
```

Replace `scraper.py` and arguments above with your  main script and preferred options.

#### Common arguments

| Argument        | Description                                  | Example                                   |
|-----------------|----------------------------------------------|-------------------------------------------|
| `--store_url`   | Shopify store front URL to scrape            | `https://examplestore.myshopify.com`      |
| `--output`      | Output file name + format (csv/json)         | `products.csv` or `products.json`         |
| `--all-products`| Scrape every product in store                |                                           |
| `--delay`       | Delay between requests (seconds)             | `2`                                       |
| ...             | ...                                          | ...                                       |

See the [`examples/`](./examples) folder or the script’s help output for advanced usage.

## Output

Scraped data can include:

- Product Title
- Price
- Description
- Product URL
- Image URLs
- Inventory Quantity
- Variant options

## Example

```json
[
  {
    "title": "Basic T-Shirt",
    "price": "19.99",
    "description": "A comfortable cotton t-shirt.",
    "url": "https://examplestore.myshopify.com/products/basic-t-shirt",
    "images": [
      "https://cdn.shopify.com/s/files/1/1234/5678/products/tshirt1.jpg"
    ],
    "variants": [
      {"option": "Size", "value": "M"}
    ],
    "inventory_quantity": 50
  }
]
```

## Contributing

Contributions welcome! Please [open an issue](https://github.com/mathuranika/Shopify-Store-Scraper/issues) or submit a pull request for improvements, bug fixes, or new features.

1. Fork the repo
2. Make changes in a feature branch
3. Add tests (if applicable)
4. Open a PR describing your changes

## Disclaimer

- This tool is for educational and research purposes only.
- Scraping websites must comply with their Terms of Service and applicable laws.
- Respect robots.txt and usage limits; do not overload target stores.

## License

MIT License. See [LICENSE](./LICENSE) for details.

---

*Created by [mathuranika](https://github.com/mathuranika)*
