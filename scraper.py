from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv

def start_browser(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scrape_books(url, selectors, output_file="books.csv"):
    driver = start_browser()
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selectors["container"]))
    )

    books = driver.find_elements(By.CSS_SELECTOR, selectors["container"])

    data = []
    for book in books:
        title = book.find_element(By.CSS_SELECTOR, selectors["title"]).get_attribute("title")
        price = book.find_element(By.CSS_SELECTOR, selectors["price"]).text
        link = book.find_element(By.CSS_SELECTOR, selectors["link"]).get_attribute("href")
        data.append([title, price, link])

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Price", "Link"])
        writer.writerows(data)

    driver.quit()
    print(f"✅ Data saved to {output_file}")
