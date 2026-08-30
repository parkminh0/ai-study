import requests
import time
import csv
from bs4 import BeautifulSoup

books_data = []
RATING_WORDS = {"One" : 1, "Two" : 2, "Three" : 3, "Four" : 4, "Five" : 5}

def price_avg(info):
    price = 0
    for v in info:
        for key, value in v.items():
            if key == "price":
                price += value
    return round(price / len(info), 2)

def price_max(info):
    price = 0
    for v in info:
        for key, value in v.items():
            if key == "price" and price < value:
                price = value
    return price

def rank_counts(info):
    result = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0}
    for v in info:
        for key, value in v.items():
            if key == "rank":
                result[value] += 1
    return result

for i in range(1, 6):
    try:
        r = requests.get(f'https://books.toscrape.com/catalogue/page-{i}.html', timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"{i}페이지 건너뜀: {e}")
        continue

    soup = BeautifulSoup(r.text, 'html.parser')
    books = soup.findAll('article', class_="product_pod")
    for book in books:
        title = book.h3.a["title"]
        link = book.h3.a["href"]
        price = float(book.find("p", class_="price_color").get_text().replace("£", "").replace("Â", "").strip())
        rank = RATING_WORDS[book.find("p", class_="star-rating").get("class")[1]]
        books_data.append({
            "title" : title,
            "link" : link,
            "price" : price,
            "rank" : rank
        })
    time.sleep(1)

print(price_avg(books_data))
print(price_max(books_data))
print(rank_counts(books_data))

FIELDS = ["title", "link", "price", "rank"]

with open("books.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(books_data)