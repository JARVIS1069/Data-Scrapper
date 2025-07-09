from scraper import scrape_books

url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

selectors = {
    "container": "article.product_pod",
    "title": "h3 a",
    "price": "div.product_price p.price_color",
    "link": "h3 a"
}

scrape_books(url, selectors)
