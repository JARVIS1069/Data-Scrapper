from flask import Flask, jsonify, send_file, render_template
import threading
import time
import csv
import os

from scraper import scrape_books  # Your Selenium scraping function

app = Flask(__name__)
scraping_status = {"status": "idle"}

CSV_FILE = "books.csv"

def run_scraper():
    global scraping_status
    scraping_status["status"] = "running"
    try:
        url = "http://books.toscrape.com/"
        selectors = {
            "container": "article.product_pod",
            "title": "h3 a",
            "price": "p.price_color",
            "link": "h3 a"
        }
        scrape_books(url, selectors)  # ✅ Now passing required arguments
        scraping_status["status"] = "done"
    except Exception as e:
        scraping_status["status"] = "error"
        print("Scraping error:", e)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start-scraping", methods=["POST"])
def start_scraping():
    if scraping_status["status"] == "running":
        return jsonify({"status": "already running"}), 400

    thread = threading.Thread(target=run_scraper)
    thread.start()
    return jsonify({"status": "started"})

@app.route("/status")
def status():
    return jsonify(scraping_status)

@app.route("/download")
def download():
    if os.path.exists(CSV_FILE):
        return send_file(CSV_FILE, as_attachment=True)
    return "CSV not found", 404

@app.route("/preview")
def preview():
    if not os.path.exists(CSV_FILE):
        return jsonify([])

    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return jsonify(rows[:5])  # Return only first 5 rows as preview

if __name__ == "__main__":
    app.run(debug=True)
