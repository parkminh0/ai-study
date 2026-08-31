"""
9주차용 판매 기록 데이터를 만듭니다.

books.csv(또는 sample_books.csv)에 있는 책 제목을 가져와서,
각 책이 언제 몇 권 팔렸는지 가짜 판매 기록을 생성합니다.

    books.csv        제목 | 링크 | 가격 | 평점        ← 책 '목록' (책 한 권당 한 줄)
    book_sales.csv   제목 | 날짜 | 수량              ← 판매 '기록' (거래 한 건당 한 줄)

이렇게 성격이 다른 두 표를 하나로 합치는 게 9주차의 핵심입니다.
현실의 데이터는 거의 항상 이렇게 여러 파일에 나뉘어 있습니다.
"""

import csv
import os
import random
from datetime import date, timedelta

random.seed(42)

SOURCE = "books.csv" if os.path.exists("books.csv") else "sample_books.csv"

if not os.path.exists(SOURCE):
    raise SystemExit(
        "books.csv도 sample_books.csv도 없습니다.\n"
        "먼저 python make_sample_books.py 를 돌리거나, 6주차 books.csv를 이 폴더에 두세요."
    )

with open(SOURCE, "r", encoding="utf-8-sig") as f:
    titles = [row["title"] for row in csv.DictReader(f)]

# 너무 커지지 않게 앞쪽 40권만 사용
titles = titles[:40]

START = date(2026, 1, 1)
rows = []

for title in titles:
    # 책마다 3~12건의 판매 기록을 만듭니다 (모든 책이 골고루 팔리진 않습니다)
    for _ in range(random.randint(3, 12)):
        sold_on = START + timedelta(days=random.randint(0, 179))  # 2026-01-01 ~ 6월 말
        rows.append({
            "title": title,
            "date": sold_on.isoformat(),      # "2026-03-14" 같은 문자열로 저장됩니다
            "quantity": random.randint(1, 5),
        })

rows.sort(key=lambda r: r["date"])

with open("book_sales.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["title", "date", "quantity"])
    w.writeheader()
    w.writerows(rows)

print(f"book_sales.csv 생성 완료 — {SOURCE}의 책 {len(titles)}종, 판매 기록 {len(rows)}건")
print("날짜는 문자열로 저장되어 있습니다. 이걸 진짜 날짜로 바꾸는 게 9주차 문제 중 하나입니다.")