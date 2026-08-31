"""
8주차 연습 — pandas

사용법:
    pip install pandas
    python week8_practice.py

이번 주는 특별합니다. 연습용 가짜 데이터가 아니라
6주차에 직접 모으신 books.csv를 분석하게 됩니다.

    이 폴더에 books.csv가 있으면 → 그걸로 채점합니다.
    없으면 → sample_books.csv를 자동으로 만들어서 대신 씁니다.
             (본인 books.csv를 나중에 이 폴더에 넣고 다시 돌려보세요)

pandas 감 잡기:
    NumPy 배열이 '숫자 뭉치'였다면, pandas의 DataFrame은 '표'입니다.
    엑셀 스프레드시트를 코드로 다룬다고 생각하시면 됩니다.
    df["price"]  ->  price 열 전체를 한 번에 꺼냅니다. (2주차 딕셔너리 접근과 비슷한 감각)
"""

import os
import pandas as pd


CSV_PATH = "books.csv" if os.path.exists("books.csv") else "sample_books.csv"


# ─────────────────────────────────────────────
# 문제 1. CSV 읽기와 첫인상
# ─────────────────────────────────────────────

def load_books(path):
    """CSV 파일을 읽어 DataFrame으로 돌려주세요.

    힌트: pd.read_csv(path, encoding="utf-8-sig")
          encoding을 안 맞추면 첫 번째 열 이름 앞에 이상한 문자가 붙습니다.
          (6주차에 utf-8-sig로 저장했던 것, 기억나시나요?)
    """
    return pd.read_csv(path, encoding="utf-8-sig")


# ─────────────────────────────────────────────
# 문제 2. 기초 통계
# ─────────────────────────────────────────────

def price_stats(df):
    """price 열의 개수·평균·최솟값·최댓값을 딕셔너리로 돌려주세요.
    평균은 소수 둘째 자리까지 반올림.

    돌려줄 모양: {"count": 30, "mean": 34.5, "min": 10.2, "max": 59.8}

    힌트: df["price"].count() / .mean() / .min() / .max()
          NumPy 배열의 .sum(), .mean()과 같은 느낌입니다 — 열 하나가 배열이라고 보면 됩니다.
    """
    return {
        "count": df["price"].count(),
        "mean": round(df["price"].mean(), 2),
        "min": df["price"].min(),
        "max": df["price"].max(),
    }
    pass


# ─────────────────────────────────────────────
# 문제 3. 정렬과 상위 n개  ← 7주차 row_sums처럼, 이번엔 '표'에서
# ─────────────────────────────────────────────

def top_n_expensive(df, n):
    """가격이 비싼 순서로 상위 n개의 '제목'만 리스트로 돌려주세요.

    힌트: df.sort_values("price", ascending=False) 로 비싼 순 정렬
          그다음 ["title"] 로 제목 열만 꺼내고
          .head(n) 으로 위에서 n개
          .tolist() 로 파이썬 리스트로 바꾸기
          네 단계를 이어붙이면 한 줄이 됩니다.
    """
    df = df.sort_values("price", ascending=False)
    return df["title"].head(n).tolist()


# ─────────────────────────────────────────────
# 문제 4. 그룹별 세기  ← 2주차 딕셔너리 세기가 한 줄이 됩니다
# ─────────────────────────────────────────────

def rating_counts(df):
    """평점(rank)별로 몇 권씩 있는지 {평점: 권수} 딕셔너리로 돌려주세요.
    평점 오름차순으로.

    예: {1: 4, 2: 3, 3: 10, 4: 8, 5: 5}

    힌트: df["rank"].value_counts() 가 거의 다 해줍니다.
          .sort_index() 로 평점 순서로 정렬하고
          {int(k): int(v) for k, v in ....items()} 로 딕셔너리로 바꾸세요.
          (int()로 안 감싸면 NumPy 정수 타입이 나와서 비교에서 어긋날 수 있습니다)

    2주차에 여러 줄로 만들었던 count_words를 떠올려보세요.
    pandas에서는 이게 전부 한 줄입니다 — 그 여러 줄이 '왜' 필요했는지 이해했다면
    이 한 줄이 무슨 일을 하는지도 바로 그려질 겁니다.
    """
    df = df["rank"].value_counts().sort_index()
    return df.to_dict()


# ─────────────────────────────────────────────
# 문제 5. 조건 필터링
# ─────────────────────────────────────────────

def filter_by_rating(df, min_rating):
    """평점이 min_rating 이상인 책들만 골라 DataFrame으로 돌려주세요.

    힌트: df[df["rank"] >= min_rating]
          안쪽 df["rank"] >= min_rating 은 True/False로 된 열입니다.
          그걸로 df[...] 를 감싸면 True인 행만 남습니다.
          이 패턴이 pandas에서 가장 많이 쓰입니다 — '조건 → 마스크 → 필터링'.
    """
    return df[df["rank"] >= min_rating]


# ─────────────────────────────────────────────
# 문제 6. 새 열 만들기
# ─────────────────────────────────────────────

def price_tier(price):
    """가격 하나를 받아 등급 문자열을 돌려주는 평범한 함수입니다. (pandas 아님)

    20 미만 -> "저가",  40 미만 -> "중가",  그 외 -> "고가"
    """
    if price < 20:
        return "저가"
    elif price < 40:
        return "중가"
    else:
        return "고가"


def add_tier_column(df):
    """df를 복사해서 price_tier를 적용한 'tier' 열을 추가해 돌려주세요.
    (원본 df는 건드리지 않습니다)

    힌트: df = df.copy()                      원본 보호
          df["tier"] = df["price"].apply(price_tier)
          .apply() 는 열의 값 하나하나에 함수를 적용합니다.
          2주차의 for문이 여기서는 apply 한 줄로 바뀝니다.
    """
    df = df.copy()
    df["tier"] = df["price"].apply(price_tier)
    return df


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


def _ensure_data():
    if not os.path.exists(CSV_PATH):
        os.system("python make_sample_books.py")


def main():
    print("\n8주차 연습 채점\n" + "─" * 46)
    _ensure_data()
    is_own_data = CSV_PATH == "books.csv"
    print(f"대상 파일: {CSV_PATH}" + (" (본인이 직접 모은 데이터입니다)" if is_own_data else " (예시 데이터)"))
    results = []

    print("\n[문제 1] 읽기")
    df = _val(lambda: load_books(CSV_PATH))
    ok = isinstance(df, pd.DataFrame) and set(df.columns) >= {"title", "price", "rank"}
    print(f"  {'✅' if ok else '❌'} load_books({CSV_PATH!r})" +
          ("" if ok else f"\n       DataFrame이 아니거나 필요한 열이 없습니다: {df!r}"))
    results.append(ok)
    if not ok:
        print("\n1번 문제가 안 풀리면 나머지는 채점할 수 없습니다. 여기부터 고쳐주세요.\n")
        return

    print("\n[문제 2] 기초 통계")
    stats = _val(lambda: price_stats(df))
    if isinstance(stats, dict):
        results.append(_check("price_stats 의 count", stats.get("count"), int(df["price"].count())))
        results.append(_check("price_stats 의 mean (소수 2자리)", stats.get("mean"),
                              round(float(df["price"].mean()), 2)))
        results.append(_check("price_stats 의 min", stats.get("min"), round(float(df["price"].min()), 2)))
        results.append(_check("price_stats 의 max", stats.get("max"), round(float(df["price"].max()), 2)))
    else:
        print(f"  ❌ price_stats가 딕셔너리를 안 돌려줍니다: {stats!r}")
        results += [False] * 4

    print("\n[문제 3] 정렬 상위 n개")
    top3 = _val(lambda: top_n_expensive(df, 3))
    expect_top3 = df.sort_values("price", ascending=False)["title"].head(3).tolist()
    results.append(_check("top_n_expensive(df, 3)", top3, expect_top3))

    print("\n[문제 4] 그룹별 세기")
    rc = _val(lambda: rating_counts(df))
    expect_rc = {int(k): int(v) for k, v in df["rank"].value_counts().sort_index().items()}
    results.append(_check("rating_counts(df)", rc, expect_rc))

    print("\n[문제 5] 조건 필터링")
    filtered = _val(lambda: filter_by_rating(df, 4))
    ok = isinstance(filtered, pd.DataFrame) and len(filtered) == len(df[df["rank"] >= 4]) \
         and filtered["rank"].min() >= 4 if len(filtered) else True
    print(f"  {'✅' if ok else '❌'} filter_by_rating(df, 4) — 평점 4 이상만 {len(df[df['rank']>=4])}건 남아야 함" +
          ("" if ok else f" (실제 {len(filtered) if isinstance(filtered, pd.DataFrame) else filtered}건)"))
    results.append(bool(ok))

    print("\n[문제 6] 새 열 만들기")
    results.append(_check('price_tier(15)', _val(lambda: price_tier(15)), "저가"))
    results.append(_check('price_tier(25)', _val(lambda: price_tier(25)), "중가"))
    results.append(_check('price_tier(50)', _val(lambda: price_tier(50)), "고가"))
    tiered = _val(lambda: add_tier_column(df))
    ok = isinstance(tiered, pd.DataFrame) and "tier" in tiered.columns and "tier" not in df.columns
    print(f"  {'✅' if ok else '❌'} add_tier_column(df) — 'tier' 열이 새로 생기고 원본 df는 안 바뀌어야 함")
    results.append(bool(ok))

    passed = sum(1 for r in results if r)
    total = len(results)
    print("\n" + "─" * 46)
    print(f"{passed} / {total} 통과")

    if passed == total:
        print(f"""
전부 통과했습니다.

이제 파일 맨 아래 EDA_QUESTIONS.md 를 열어서,
본인이 직접 궁금한 질문 5개를 만들고 pandas로 답해보세요.
그게 2단계 완료 기준입니다 — 정답이 정해진 문제가 아니라
'내가 궁금한 걸 데이터로 확인'하는 연습입니다.
""" + ("" if is_own_data else """
지금은 sample_books.csv로 채점했습니다.
본인의 진짜 books.csv를 이 폴더에 넣고 다시 돌리면
같은 코드가 진짜 데이터에서도 통과하는지 확인할 수 있습니다.
"""))
    else:
        print("\n❌ 항목의 '기대한 값'과 '나온 값'을 비교해보세요.")
    print()


if __name__ == "__main__":
    main()