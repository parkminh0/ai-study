"""
10주차 연습 — 시각화 (matplotlib · seaborn)

준비:
    pip install matplotlib seaborn
    python make_sample_books.py     (books.csv가 없다면)
    python make_sales_data.py

사용법:
    python week10_practice.py

이번 주는 채점 방식이 다릅니다.
그래프가 '예쁜지'는 채점할 수 없습니다. 대신 **틀린 그래프**를 잡아냅니다:
    - 제목·축 라벨이 없는가          (라벨 없는 그래프는 읽을 수 없습니다)
    - 데이터의 job에 맞는 형태인가   (추세엔 선, 크기 비교엔 막대, 분포엔 히스토그램)
    - 색을 역할에 맞게 썼는가        (양=한 색 진하기, 양극=두 색+중간 회색)

각 함수는 matplotlib Figure를 돌려주면 됩니다.
전부 통과하면 PNG 5장이 저장되니 직접 열어보세요.

━━ 형태 고르기: 데이터가 하는 일이 형태를 정합니다 ━━
    시간에 따른 추세      →  선 그래프
    크기 비교            →  막대 그래프
    분포(퍼짐)           →  히스토그램
    두 값의 관계         →  산점도
    격자 형태의 크기 비교  →  히트맵
"""

import colorsys
import os

import matplotlib
matplotlib.use("Agg")          # 창을 안 띄우고 파일로만 저장 (채점용)
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from viz_style import apply_style, clean_axes, PRIMARY, BLUE_RAMP

apply_style()


# ─────────────────────────────────────────────
# 문제 1. 선 그래프 — 시간에 따른 추세
# ─────────────────────────────────────────────

def monthly_line(monthly):
    """월별 판매 수량을 선 그래프로 그려 Figure를 돌려주세요.

    monthly는 {"2026-01": 105, "2026-02": 96, ...} 형태의 딕셔너리입니다.

    반드시 넣을 것: 제목, x축 라벨, y축 라벨
        라벨 없는 그래프는 본인만 알아볼 수 있습니다.
        "판매 수량"이 아니라 "판매 수량 (권)"처럼 단위까지 쓰면 더 좋습니다.

    힌트:
        fig, ax = plt.subplots()
        ax.plot(list(monthly.keys()), list(monthly.values()), color=PRIMARY, marker="o")
        ax.set_title("...")
        ax.set_xlabel("...")
        ax.set_ylabel("...")
        clean_axes(ax)          # 위/오른쪽 테두리 제거
        fig.tight_layout()
        return fig
    """
    fig, ax = plt.subplots()
    ax.plot(list(monthly.keys()), list(monthly.values()), color=PRIMARY, marker="o")
    ax.set_title("월별 판매 수량")
    ax.set_xlabel("년-월")
    ax.set_ylabel("판매 수량")
    clean_axes(ax)          # 위/오른쪽 테두리 제거
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────
# 문제 2. 막대 그래프 — 크기 비교
# ─────────────────────────────────────────────

def revenue_bar(revenue):
    """평점별 총 매출을 막대 그래프로 그려 Figure를 돌려주세요.

    revenue는 {1: 1520.5, 2: 980.25, ...} 형태입니다.

    색에 대하여:
        평점 1~5는 '순서가 있는' 값입니다. 이런 경우엔 한 가지 색의
        진하기를 순서대로 쓰는 게 좋습니다 (BLUE_RAMP를 순서대로).

        주의: 순서 없는 항목(책 제목, 팀 이름 등)에는 이렇게 하면 안 됩니다.
              막대 길이가 이미 크기를 보여주는데 색까지 크기를 나타내면
              색이라는 정보 채널을 낭비하는 셈입니다. 그럴 땐 전부 한 색으로.

    힌트:
        ax.bar([str(r) for r in revenue.keys()], list(revenue.values()),
               color=BLUE_RAMP, width=0.7)
        x축은 숫자가 아니라 '항목'이므로 문자열로 바꿔주는 게 안전합니다.
    """
    fig, ax = plt.subplots()
    ax.bar([str(r) for r in revenue.keys()], list(revenue.values()), color=BLUE_RAMP, width=0.7)
    ax.set_title("평점별 총 매출")
    ax.set_xlabel("평점")
    ax.set_ylabel("매출")
    clean_axes(ax)          # 위/오른쪽 테두리 제거
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────
# 문제 3. 산점도 — 두 값의 관계
# ─────────────────────────────────────────────

def price_quantity_scatter(merged):
    """가격(x)과 판매 수량(y)의 관계를 산점도로 그려 Figure를 돌려주세요.

    힌트:
        ax.scatter(merged["price"], merged["quantity"], color=PRIMARY,
                   alpha=0.6, s=40, edgecolors="white", linewidths=1.5)

        alpha(투명도)와 흰 테두리를 주는 이유: 점이 겹칠 때 몇 개가 겹쳤는지
        보이게 하려고요. 불투명한 점만 찍으면 100개가 겹쳐도 1개처럼 보입니다.
    """
    fig, ax = plt.subplots()
    ax.scatter(merged["price"], merged["quantity"], color=PRIMARY,
                   alpha=0.6, s=40, edgecolors="white", linewidths=1.5)
    ax.set_title("가격과 판매수량의 관계")
    ax.set_xlabel("가격")
    ax.set_ylabel("판매 수량")
    clean_axes(ax)          # 위/오른쪽 테두리 제거
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────
# 문제 4. 히스토그램 — 분포
# ─────────────────────────────────────────────

def price_histogram(books):
    """책 가격의 분포를 히스토그램으로 그려 Figure를 돌려주세요.

    막대 그래프와 헷갈리기 쉽습니다:
        막대 그래프  — 항목별 값 (평점 1은 얼마, 평점 2는 얼마)
        히스토그램   — 값의 분포 (10~20파운드 책이 몇 권, 20~30파운드가 몇 권)
        히스토그램의 x축은 '구간'이지 '항목'이 아닙니다.

    힌트:
        ax.hist(books["price"], bins=12, color=PRIMARY,
                edgecolor="white", linewidth=1.2)
        bins는 구간을 몇 개로 나눌지입니다. 바꿔가며 그려보세요 —
        너무 적으면 뭉개지고, 너무 많으면 들쭉날쭉해집니다.
    """
    fig, ax = plt.subplots()
    ax.hist(books["price"], bins=12, color=PRIMARY,
                edgecolor="white", linewidth=1.2)
    ax.set_title("책 가격의 분포")
    ax.set_xlabel("가격")
    ax.set_ylabel("수량")
    clean_axes(ax)          # 위/오른쪽 테두리 제거
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────
# 문제 5. 히트맵 — 상관관계  ★ 색을 제대로 써야 하는 문제
# ─────────────────────────────────────────────

def correlation_heatmap(merged):
    """price, rank, quantity, revenue 네 열의 상관관계를 히트맵으로 그려주세요.

    상관계수는 -1 ~ +1 사이입니다. 이런 데이터는 '양극(diverging)' 데이터입니다:
        +1  강한 양의 관계   (하나가 커지면 다른 것도 커짐)
         0  관계 없음
        -1  강한 음의 관계   (하나가 커지면 다른 것은 작아짐)

    색 규칙 — 이번 주에서 가장 중요합니다:
        양극 데이터는 **반대되는 두 색 + 가운데는 회색**으로 칠합니다.
        0이 '아무것도 아님'으로 읽혀야 하니까 가운데에 색이 있으면 안 됩니다.
        빨강↔파랑은 따뜻함/차가움이라 반대로 읽힙니다. 좋습니다.
        파랑↔하늘색은 둘 다 차가워서 안 됩니다.
        무지개색은 절대 쓰지 마세요.

        그리고 vmin=-1, vmax=1, center=0 을 반드시 지정하세요.
        안 그러면 데이터 범위에 맞춰 색이 자동 조정돼서,
        상관계수 0.1짜리가 새빨갛게 나오는 거짓말이 됩니다.

    힌트:
        cols = ["price", "rank", "quantity", "revenue"]
        corr = merged[cols].corr()
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(corr, ax=ax, cmap="RdBu_r", vmin=-1, vmax=1, center=0,
                    annot=True, fmt=".2f", square=True,
                    linewidths=2, linecolor="white",
                    cbar_kws={"label": "상관계수"})
        ax.set_title("...")
    """
    cols = ["price", "rank", "quantity", "revenue"]
    corr = merged[cols].corr()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(corr, ax=ax, cmap="RdBu_r", vmin=-1, vmax=1, center=0,
                annot=True, fmt=".2f", square=True,
                linewidths=2, linecolor="white",
                cbar_kws={"label": "상관계수"})
    ax.set_title("상관관계 히트맵")
    clean_axes(ax)          # 위/오른쪽 테두리 제거
    fig.tight_layout()
    return fig


# ═════════════════════════════════════════════
# 아래는 채점기입니다. 고치지 마세요.
# ═════════════════════════════════════════════

def _val(fn):
    try:
        return fn()
    except Exception as e:
        return f"<에러: {type(e).__name__}: {e}>"


def _report(ok, name, detail=""):
    print(f"  {'✅' if ok else '❌'} {name}")
    if not ok and detail:
        for line in str(detail).split("\n"):
            print(f"       {line}")
    return bool(ok)


def _check_labels(fig, results, label, need_xy=True):
    """제목·축 라벨이 있는지 검사합니다. 모든 그래프의 기본 요건입니다."""
    if not isinstance(fig, plt.Figure):
        results.append(_report(False, f"{label} — Figure를 돌려줘야 합니다", f"돌려준 것: {fig!r}"))
        return None
    ax = fig.axes[0]
    results.append(_report(bool(ax.get_title().strip()), f"{label} — 제목이 있음",
                           "ax.set_title(...) 을 넣으세요"))
    if need_xy:
        results.append(_report(bool(ax.get_xlabel().strip()), f"{label} — x축 라벨이 있음",
                               "ax.set_xlabel(...) 을 넣으세요"))
        results.append(_report(bool(ax.get_ylabel().strip()), f"{label} — y축 라벨이 있음",
                               "ax.set_ylabel(...) 을 넣으세요"))
    return ax


def main():
    print("\n10주차 연습 채점\n" + "─" * 52)

    books_path = "books.csv" if os.path.exists("books.csv") else "sample_books.csv"
    if not os.path.exists("book_sales.csv"):
        print("\nbook_sales.csv 가 없습니다. python make_sales_data.py 를 먼저 돌리세요.\n")
        return

    books = pd.read_csv(books_path, encoding="utf-8-sig")
    sales = pd.read_csv("book_sales.csv", encoding="utf-8-sig")
    sales["date"] = pd.to_datetime(sales["date"])
    merged = pd.merge(books, sales, on="title")
    merged["revenue"] = merged["price"] * merged["quantity"]
    merged["month"] = merged["date"].dt.strftime("%Y-%m")

    monthly = {str(k): int(v) for k, v in
               merged.groupby("month")["quantity"].sum().sort_index().items()}
    revenue = {int(k): round(float(v), 2) for k, v in
               merged.groupby("rank")["revenue"].sum().sort_index().items()}

    print(f"대상: {books_path} + book_sales.csv ({len(merged)}행)")
    results = []
    saved = []

    print("\n[문제 1] 선 그래프")
    fig = _val(lambda: monthly_line(monthly))
    ax = _check_labels(fig, results, "monthly_line")
    if ax is not None:
        results.append(_report(len(ax.lines) >= 1, "monthly_line — 선(line)이 그려짐",
                               "ax.plot() 을 쓰세요. 추세에는 선 그래프입니다."))
        if ax.lines:
            got = list(ax.lines[0].get_ydata())
            results.append(_report(got == [float(v) for v in monthly.values()],
                                   "monthly_line — 월별 수량이 정확히 그려짐",
                                   f"기대: {list(monthly.values())}\n나온 값: {got}"))
        saved.append(("chart_1_line.png", fig))

    print("\n[문제 2] 막대 그래프")
    fig = _val(lambda: revenue_bar(revenue))
    ax = _check_labels(fig, results, "revenue_bar")
    if ax is not None:
        bars = [p for p in ax.patches]
        results.append(_report(len(bars) == len(revenue),
                               f"revenue_bar — 막대 {len(revenue)}개",
                               f"막대가 {len(bars)}개입니다. ax.bar() 를 쓰세요."))
        if bars:
            heights = sorted(round(b.get_height(), 2) for b in bars)
            want = sorted(round(v, 2) for v in revenue.values())
            results.append(_report(heights == want, "revenue_bar — 막대 높이가 매출과 일치",
                                   f"기대: {want}\n나온 값: {heights}"))
        saved.append(("chart_2_bar.png", fig))

    print("\n[문제 3] 산점도")
    fig = _val(lambda: price_quantity_scatter(merged))
    ax = _check_labels(fig, results, "price_quantity_scatter")
    if ax is not None:
        results.append(_report(len(ax.collections) >= 1,
                               "price_quantity_scatter — 산점도가 그려짐",
                               "ax.scatter() 를 쓰세요. 두 값의 관계에는 산점도입니다."))
        if ax.collections:
            n_points = len(ax.collections[0].get_offsets())
            results.append(_report(n_points == len(merged),
                                   f"price_quantity_scatter — 점 {len(merged)}개",
                                   f"점이 {n_points}개입니다. merged 전체를 넣으셨나요?"))
        saved.append(("chart_3_scatter.png", fig))

    print("\n[문제 4] 히스토그램")
    fig = _val(lambda: price_histogram(books))
    ax = _check_labels(fig, results, "price_histogram")
    if ax is not None:
        results.append(_report(len(ax.patches) >= 5,
                               "price_histogram — 구간 막대가 5개 이상",
                               "ax.hist() 를 쓰세요. bins로 구간 수를 정합니다."))
        total = sum(p.get_height() for p in ax.patches)
        results.append(_report(abs(total - len(books)) < 0.5,
                               f"price_histogram — 전체 개수 합이 {len(books)}권",
                               f"막대 높이의 합이 {total}입니다. 모든 책이 들어갔나요?"))
        saved.append(("chart_4_hist.png", fig))

    print("\n[문제 5] 히트맵")
    fig = _val(lambda: correlation_heatmap(merged))
    ax = _check_labels(fig, results, "correlation_heatmap", need_xy=False)
    if ax is not None:
        mesh = ax.collections[0] if ax.collections else None
        results.append(_report(mesh is not None, "correlation_heatmap — 히트맵이 그려짐",
                               "sns.heatmap(...) 을 쓰세요."))
        if mesh is not None:
            lo, hi = mesh.get_clim()
            results.append(_report(
                abs(lo + 1) < 0.01 and abs(hi - 1) < 0.01,
                "correlation_heatmap — 색 범위가 -1 ~ +1 로 고정됨",
                f"현재 범위: {lo:.2f} ~ {hi:.2f}\n"
                "vmin=-1, vmax=1, center=0 을 지정하세요.\n"
                "고정하지 않으면 상관계수 0.1짜리가 새빨갛게 나옵니다 — 거짓말하는 그래프입니다."))
            # cmap 이름이 아니라 '실제 색'을 검사합니다.
            # (seaborn이 이름을 from_list로 바꿔버리기 때문에 이름 검사는 못 씁니다)
            cmap = mesh.get_cmap()
            lo_c, mid_c, hi_c = cmap(0.0)[:3], cmap(0.5)[:3], cmap(1.0)[:3]
            mid_sat = colorsys.rgb_to_hsv(*mid_c)[1]
            h_lo = colorsys.rgb_to_hsv(*lo_c)[0]
            h_hi = colorsys.rgb_to_hsv(*hi_c)[0]
            hue_gap = min(abs(h_lo - h_hi), 1 - abs(h_lo - h_hi))
            results.append(_report(
                mid_sat < 0.30 and hue_gap > 0.15,
                f"correlation_heatmap — 양극(diverging) 색 (가운데 채도 {mid_sat:.2f}, "
                f"양끝 색상차 {hue_gap:.2f})",
                "상관계수는 -1~+1의 양극 데이터입니다. 색이 두 조건을 만족해야 합니다:\n"
                "  1) 가운데(0)가 무채색이어야 함 — 0은 '아무것도 아님'으로 읽혀야 합니다\n"
                "  2) 양끝이 반대되는 두 색이어야 함 — 빨강↔파랑 같은 따뜻/차가움\n"
                "RdBu_r, coolwarm, vlag 등이 맞습니다.\n"
                "viridis·Blues 같은 한 방향 색이나 무지개색(jet, rainbow)은 안 됩니다."))
        saved.append(("chart_5_heatmap.png", fig))

    passed = sum(1 for r in results if r)
    total = len(results)
    print("\n" + "─" * 52)
    print(f"{passed} / {total} 통과")

    for name, f in saved:
        try:
            f.savefig(name, bbox_inches="tight")
        except Exception:
            pass
    if saved:
        print(f"\n그림 {len(saved)}장을 저장했습니다: {', '.join(n for n, _ in saved)}")
        print("파일을 열어서 직접 눈으로 확인하세요. 채점기는 색과 라벨만 보지, 겹친 글자는 못 봅니다.")

    if passed == total:
        print("""
전부 통과했습니다.

이제 완료 기준입니다: **본인 데이터로 흥미로운 그래프 4개**를 그리세요.
여기 있는 5개를 그대로 쓰지 말고, 8주차 EDA_QUESTIONS.md 에서 던졌던
질문 중 '그림으로 보면 더 잘 보일 것 같은' 걸 골라 그려보세요.

그래프를 그리기 전에 매번 물어보세요:
    "이 그림에서 독자가 무엇을 읽어내야 하지?"
그 답이 형태를 정해줍니다. 예쁜 그래프가 아니라 답이 보이는 그래프가 목표입니다.

  git add . && git commit -m "10주차 시각화" && git push
""")
    else:
        print("\n❌ 항목을 고치고 다시 돌려보세요.\n")


if __name__ == "__main__":
    main()