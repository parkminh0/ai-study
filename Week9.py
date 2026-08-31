"""
9주차 연습 — pandas 심화: merge · groupby · 날짜 · pivot_table

준비:
    python make_sample_books.py     (books.csv가 없다면)
    python make_sales_data.py       (book_sales.csv 생성)

사용법:
    python week9_practice.py

이번 주의 그림:

    books.csv       제목 | 링크 | 가격 | 평점       ← 책 목록 (책 한 권당 한 줄)
    book_sales.csv  제목 | 날짜 | 수량             ← 판매 기록 (거래 한 건당 한 줄)
                          │
                          └─ merge(제목 기준) ─→  하나의 큰 표
                                                   └─ groupby로 요약
                                                   └─ pivot_table로 교차표

8주차에는 표 하나만 다뤘습니다. 현실의 데이터는 거의 항상 여러 파일로 나뉘어 있고,
그걸 합치는 게 분석의 첫 단계입니다.
"""

import os
import pandas as pd


BOOKS_PATH = "books.csv" if os.path.exists("books.csv") else "sample_books.csv"
SALES_PATH = "book_sales.csv"


# ─────────────────────────────────────────────
# 문제 1. 날짜를 진짜 날짜로 만들기
# ─────────────────────────────────────────────

def load_sales(path):
    """판매 기록 CSV를 읽되, date 열을 '진짜 날짜 타입'으로 바꿔서 돌려주세요.

    CSV에서 읽으면 date는 "2026-03-14" 같은 그냥 문자열입니다.
    문자열인 상태로는 '3월만 뽑기', '월별로 묶기' 같은 걸 할 수 없습니다.

    힌트:
        df = pd.read_csv(path, encoding="utf-8-sig")
        df["date"] = pd.to_datetime(df["date"])
        return df

    to_datetime을 거치고 나면 df["date"].dt.year, .dt.month 처럼
    .dt 으로 날짜의 부품을 꺼낼 수 있게 됩니다.
    (문자열 열에 .str 이 붙는 것과 같은 구조입니다)
    """
    df = pd.read_csv(path, encoding="utf-8-sig")
    df["date"] = pd.to_datetime(df["date"])
    return df


# ─────────────────────────────────────────────
# 문제 2. 두 표 합치기 (merge)  ★ 이번 주 핵심
# ─────────────────────────────────────────────

def merge_books_sales(books, sales):
    """책 목록과 판매 기록을 'title' 기준으로 합쳐서 돌려주세요.

    books:  title | link | price | rank      (책 30종)
    sales:  title | date | quantity          (거래 300건)
    결과:   title | link | price | rank | date | quantity   (거래 300건)

    판매 기록 한 줄마다, 그 책의 가격·평점 정보가 옆에 따라붙습니다.
    이래야 "평점 5점짜리 책이 총 얼마어치 팔렸나" 같은 질문에 답할 수 있습니다.

    힌트: pd.merge(books, sales, on="title")

    엑셀의 VLOOKUP과 같은 일입니다. SQL을 아신다면 JOIN이고요.
    """
    return pd.merge(books, sales, on="title")


# ─────────────────────────────────────────────
# 문제 3. 열끼리 계산해서 새 열 만들기
# ─────────────────────────────────────────────

def add_revenue(merged):
    """merged를 복사해서 revenue(매출) 열을 추가해 돌려주세요.
    매출 = 가격 × 수량

    힌트: merged["price"] * merged["quantity"]
          열 곱하기 열이 각 줄끼리 알아서 곱해집니다.
          7주차 NumPy 브로드캐스팅과 똑같은 원리입니다 — 표에서도 그대로 통합니다.

    (8주차 add_tier_column처럼 원본은 건드리지 말고 .copy() 먼저)
    """
    merged = merged.copy()
    merged["revenue"] = merged["price"] * merged["quantity"]
    return merged


# ─────────────────────────────────────────────
# 문제 4. groupby로 요약하기  ★ 이번 주 핵심
# ─────────────────────────────────────────────

def revenue_by_rating(merged):
    """평점별 총 매출을 {평점: 매출} 딕셔너리로 돌려주세요.
    평점 오름차순, 매출은 소수 둘째 자리 반올림.

    예: {1: 1520.5, 2: 980.25, 3: 4210.0, 4: 3300.75, 5: 2100.4}

    힌트: merged.groupby("rank")["revenue"].sum()
          "rank로 묶어서 / revenue 열을 / 더해라" — 영어 문장처럼 읽힙니다.
          .sort_index() 로 평점 순 정렬하고
          {int(k): round(float(v), 2) for k, v in ....items()} 로 변환하세요.

    8주차 value_counts()는 '개수'만 셌습니다.
    groupby는 개수뿐 아니라 합계·평균·최댓값 등 뭐든 계산할 수 있습니다.
    """
    merged = merged.copy().groupby("rank")["revenue"].sum().sort_index()
    return {int(k) : round(float(v), 2) for k, v in merged.items()}


# ─────────────────────────────────────────────
# 문제 5. 날짜에서 '월' 뽑아내기
# ─────────────────────────────────────────────

def add_month(merged):
    """merged를 복사해서 month 열("2026-03" 형태 문자열)을 추가해 돌려주세요.

    힌트: merged["date"].dt.strftime("%Y-%m")
          %Y는 네 자리 연도, %m은 두 자리 월입니다.

    왜 "2026-03" 같은 문자열로 만드나요?
    "3"만 뽑으면 2026년 3월과 2027년 3월이 섞여버립니다.
    연도까지 붙여야 시간 순서대로 정렬도 됩니다. (문자열이라도 이 형식은 순서가 맞습니다)
    """
    merged = merged.copy()
    merged["month"] = merged["date"].dt.strftime("%Y-%m")
    return merged


def monthly_quantity(merged):
    """월별 총 판매 수량을 {"2026-01": 120, ...} 딕셔너리로 돌려주세요.
    월 오름차순.

    힌트: month 열이 이미 있다고 가정하고 groupby("month")["quantity"].sum()
    """
    return merged.groupby("month")["quantity"].sum().sort_index().to_dict()

def best_month(merged):
    """가장 많이 팔린 달을 "2026-03" 같은 문자열로 돌려주세요.

    힌트: groupby한 결과에 .idxmax() 를 쓰면
          '가장 큰 값' 이 아니라 '가장 큰 값의 이름표(인덱스)' 가 나옵니다.
          max() 와 idxmax() 의 차이를 꼭 구분해두세요 — 자주 헷갈립니다.
    """
    return merged.copy().groupby("month")["quantity"].sum().idxmax()


# ─────────────────────────────────────────────
# 문제 6. pivot_table — 두 방향으로 동시에 묶기
# ─────────────────────────────────────────────

def rating_month_pivot(merged):
    """행은 평점(rank), 열은 월(month), 값은 판매수량 합계인 교차표를 돌려주세요.
    데이터가 없는 칸은 0으로.

    결과 모양:
        month    2026-01  2026-02  2026-03 ...
        rank
        1             12       8       15
        2              5      20        9
        ...

    힌트:
        pd.pivot_table(merged, index="rank", columns="month",
                       values="quantity", aggfunc="sum", fill_value=0)

    groupby가 한 방향으로 묶는 거라면, pivot_table은 두 방향으로 동시에 묶습니다.
    엑셀의 '피벗 테이블'과 정확히 같은 개념입니다.
    """
    return pd.pivot_table(merged, index="rank", columns="month", values="quantity", aggfunc="sum", fill_value=0)


# ═════════════════════════════════════════════
# 아래는 채점기입니다. 고치지 마세요.
# ═════════════════════════════════════════════

def _val(fn):
    try:
        return fn()
    except Exception as e:
        return f"<에러: {type(e).__name__}: {e}>"


def _check(name, got, want):
    ok = got == want
    print(f"  {'✅' if ok else '❌'} {name}")
    if not ok:
        print(f"       기대한 값: {want!r}")
        print(f"       나온 값  : {got!r}")
    return ok


def _report(ok, name, detail=""):
    print(f"  {'✅' if ok else '❌'} {name}")
    if not ok and detail:
        print(f"       {detail}")
    return ok


def main():
    print("\n9주차 연습 채점\n" + "─" * 52)

    if not os.path.exists(SALES_PATH):
        print(f"\n{SALES_PATH} 가 없습니다. 먼저 이걸 돌리세요:")
        print("    python make_sales_data.py\n")
        return

    books = pd.read_csv(BOOKS_PATH, encoding="utf-8-sig")
    print(f"대상: {BOOKS_PATH} ({len(books)}종) + {SALES_PATH}")
    results = []

    print("\n[문제 1] 날짜 변환")
    sales = _val(lambda: load_sales(SALES_PATH))
    ok = isinstance(sales, pd.DataFrame) and pd.api.types.is_datetime64_any_dtype(sales.get("date"))
    results.append(_report(
        ok, "load_sales — date 열이 datetime 타입",
        f"date 열의 타입이 아직 문자열입니다: {sales!r}"[:200]))
    if not ok:
        print("\n1번을 먼저 해결해야 나머지를 채점할 수 있습니다.\n")
        return

    print("\n[문제 2] merge")
    merged = _val(lambda: merge_books_sales(books, sales))
    expect = pd.merge(books, sales, on="title")
    ok = isinstance(merged, pd.DataFrame) and len(merged) == len(expect) \
        and {"price", "rank", "date", "quantity"} <= set(merged.columns)
    results.append(_report(
        ok, f"merge_books_sales — {len(expect)}행, 양쪽 열이 모두 있어야 함",
        f"나온 결과: {type(merged).__name__}, "
        f"{len(merged) if isinstance(merged, pd.DataFrame) else '?'}행"))
    if not ok:
        print("\n2번을 먼저 해결해야 나머지를 채점할 수 있습니다.\n")
        return

    print("\n[문제 3] 새 열 계산")
    rev = _val(lambda: add_revenue(merged))
    ok = isinstance(rev, pd.DataFrame) and "revenue" in rev.columns \
        and "revenue" not in merged.columns \
        and abs(float(rev["revenue"].sum())
                - float((expect["price"] * expect["quantity"]).sum())) < 0.01
    results.append(_report(ok, "add_revenue — revenue 열 추가, 원본 보존"))
    if not ok:
        rev = expect.copy()
        rev["revenue"] = rev["price"] * rev["quantity"]

    print("\n[문제 4] groupby 요약")
    exp_rev = expect.copy()
    exp_rev["revenue"] = exp_rev["price"] * exp_rev["quantity"]
    want_rbr = {int(k): round(float(v), 2)
                for k, v in exp_rev.groupby("rank")["revenue"].sum().sort_index().items()}
    results.append(_check("revenue_by_rating(merged)", _val(lambda: revenue_by_rating(rev)), want_rbr))

    print("\n[문제 5] 날짜에서 월 뽑기")
    withm = _val(lambda: add_month(rev))
    ok = isinstance(withm, pd.DataFrame) and "month" in withm.columns \
        and str(withm["month"].iloc[0]).count("-") == 1 and len(str(withm["month"].iloc[0])) == 7
    results.append(_report(
        ok, 'add_month — "2026-03" 형태의 month 열',
        f'첫 값이 "2026-03" 형태가 아닙니다: '
        f'{withm["month"].iloc[0] if isinstance(withm, pd.DataFrame) and "month" in withm.columns else withm!r}'))
    if not ok:
        withm = rev.copy()
        withm["month"] = withm["date"].dt.strftime("%Y-%m")

    exp_m = exp_rev.copy()
    exp_m["month"] = exp_m["date"].dt.strftime("%Y-%m")
    want_mq = {str(k): int(v)
               for k, v in exp_m.groupby("month")["quantity"].sum().sort_index().items()}
    results.append(_check("monthly_quantity(merged)", _val(lambda: monthly_quantity(withm)), want_mq))
    results.append(_check("best_month(merged)", _val(lambda: best_month(withm)),
                          str(exp_m.groupby("month")["quantity"].sum().idxmax())))

    print("\n[문제 6] pivot_table")
    piv = _val(lambda: rating_month_pivot(withm))
    want_piv = pd.pivot_table(exp_m, index="rank", columns="month",
                              values="quantity", aggfunc="sum", fill_value=0)
    ok = isinstance(piv, pd.DataFrame) and piv.shape == want_piv.shape \
        and int(piv.to_numpy().sum()) == int(want_piv.to_numpy().sum())
    results.append(_report(
        ok, f"rating_month_pivot — {want_piv.shape[0]}행 × {want_piv.shape[1]}열 교차표",
        f"나온 모양: {piv.shape if isinstance(piv, pd.DataFrame) else piv!r}"))

    passed = sum(1 for r in results if r)
    total = len(results)
    print("\n" + "─" * 52)
    print(f"{passed} / {total} 통과")

    if passed == total:
        print("\n전부 통과했습니다. 실제로 만들어진 교차표를 보여드릴게요:\n")
        print(want_piv.to_string())
        print("""
이 표 하나에 "어떤 평점의 책이 어느 달에 얼마나 팔렸나"가 전부 들어 있습니다.
merge로 흩어진 데이터를 모으고, groupby로 요약하고, pivot으로 두 방향에서 본 결과입니다.

이 세 가지가 데이터 분석 업무의 절반입니다.
10주차에는 이 표를 그래프로 그려서 눈으로 봅니다.

  git add . && git commit -m "9주차 pandas 심화" && git push
""")
    else:
        print("\n❌ 항목을 확인하세요. 앞 문제가 틀리면 뒤 문제는 정답 데이터로 대신 채점합니다.\n")


if __name__ == "__main__":
    main()