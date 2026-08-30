import requests
import time
from bs4 import BeautifulSoup

class Book:
    def __init__(self, title, link, price, rank):
        self.title = title
        self.link = link
        self.price = price
        self.rank = rank
    
    def as_row(self):
        return {
            "title" : self.title,
            "link" : self.link,
            "price" : self.price,
            "rank" : self.rank
        }

class BookCollector:
    def __init__(self):
        self.books = []
    
    def add(self, book):
        self.books.append(book)
    
    def average_price(self):
        return round(sum((b.price for b in self.books)) / len(self.books), 2)

    def max_price(self):
        return max(b.price for b in self.books)

    def rank_counts(self):
        result = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0}
        for b in self.books:
            result[b.rank] += 1
        return result
    
    def save_csv(self, path):
        import csv
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "link", "price", "rank"])
            writer.writeheader()
            writer.writerows(b.as_row() for b in self.books)

RATING_WORDS = {"One" : 1, "Two" : 2, "Three" : 3, "Four" : 4, "Five" : 5}
def main():
    collector = BookCollector()
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
            collector.add(Book(title, link, price, rank))
        time.sleep(1)
    
    print(collector.average_price())
    print(collector.max_price())
    print(collector.rank_counts())
    collector.save_csv("books.csv")

if __name__ == "__main__":
    main()
