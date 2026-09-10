"""
12주차 연습 — 확률·통계 (2단계 마지막 주)

사용법:
    python week12_practice.py

이번 주도 직접 만듭니다. statistics 모듈이나 np.mean은 쓰지 마세요.
공식을 손으로 짜봐야 그 숫자가 무슨 뜻인지 남습니다.

━━ 이번 주에 잡을 그림 두 가지 ━━

1. 표준편차 = "평균에서 보통 이만큼 떨어져 있다"
   평균만 보면 속습니다. 평균 연봉이 같아도 표준편차가 다르면 완전히 다른 회사입니다.

2. 조건부확률 P(A|B) 와 P(B|A) 는 완전히 다른 값이다
   이걸 헷갈리는 게 통계에서 가장 흔하고 가장 비싼 실수입니다.
   그리고 15주차 '정밀도와 재현율'이 정확히 이 두 방향입니다.
   이번 주에 확실히 잡아두면 15주차가 절반은 끝납니다.
"""

import math


# ─────────────────────────────────────────────
# 문제 1. 평균
# ─────────────────────────────────────────────

def mean(nums):
    """평균을 돌려주세요. 빈 리스트면 0.0

    2주차 my_average와 같습니다. 이번 주의 출발점이라 다시 만듭니다.
    """
    return 0.0 if len(nums) == 0 else sum(nums) / len(nums) 


# ─────────────────────────────────────────────
# 문제 2. 분산 — 흩어진 정도
# ─────────────────────────────────────────────

def variance(nums):
    """분산을 돌려주세요. 빈 리스트면 0.0

    분산 = 각 값이 평균에서 떨어진 거리를 제곱해서 평균낸 것

        1. 평균을 구한다
        2. 각 값에서 평균을 뺀다        (평균에서 얼마나 떨어졌나)
        3. 그걸 제곱한다                 (아래 설명 참고)
        4. 다 더해서 개수로 나눈다

    variance([2, 4, 4, 4, 5, 5, 7, 9]) -> 4.0

    ★ 왜 제곱하나요?
      그냥 더하면 +3과 -3이 상쇄돼서 항상 0이 나옵니다.
      제곱하면 부호가 사라져서 '떨어진 정도'만 남습니다.
      (절댓값을 써도 되긴 하는데, 제곱이 수학적으로 다루기 훨씬 편합니다)

    ※ 여기서는 개수 n으로 나눕니다(모분산).
      표본분산은 n-1로 나누는데, 그건 나중에 필요할 때 보시면 됩니다.
    """
    if len(nums) == 0:
        return 0.0
    m = mean(nums)
    s = 0
    for v in nums:
        s += (v - m) ** 2
    return s / len(nums)


# ─────────────────────────────────────────────
# 문제 3. 표준편차 — 분산을 되돌리기
# ─────────────────────────────────────────────

def std_dev(nums):
    """표준편차를 돌려주세요.

    표준편차 = √분산

    ★ 왜 루트를 씌우나요?
      분산은 제곱을 했기 때문에 단위도 제곱이 됩니다.
      가격(파운드)의 분산은 '파운드²'이라 무슨 뜻인지 알 수 없습니다.
      루트를 씌우면 단위가 원래대로 돌아와서 이렇게 읽을 수 있습니다:

          "평균 30파운드, 표준편차 8파운드"
          → 대충 22~38파운드 사이에 많이 몰려 있구나

      표준편차는 "평균에서 보통 이만큼 떨어져 있다"입니다.

    std_dev([2, 4, 4, 4, 5, 5, 7, 9]) -> 2.0
    """
    return variance(nums) ** 0.5


# ─────────────────────────────────────────────
# 문제 4. z-점수 — "평균에서 몇 표준편차만큼?"
# ─────────────────────────────────────────────

def z_score(value, nums):
    """value가 평균에서 표준편차 몇 개만큼 떨어져 있는지 돌려주세요.

    z = (값 - 평균) / 표준편차

    z = 0    딱 평균
    z = 1    평균보다 표준편차 1개만큼 위
    z = -2   평균보다 표준편차 2개만큼 아래 (꽤 낮은 편)

    ★ 이게 왜 유용한가:
      단위가 다른 것끼리 비교할 수 있게 됩니다.
      키 180cm와 몸무게 90kg 중 뭐가 더 '특이한가'는 그냥은 비교가 안 되는데,
      z-점수로 바꾸면 둘 다 '평균에서 몇 칸'이라는 같은 자로 잽니다.

    7주차 min_max_normalize와 비교해보세요. 둘 다 '스케일 맞추기'인데:
        min-max : 최솟값 0, 최댓값 1로 밀어넣기 (범위가 고정됨)
        z-점수  : 평균 0, 표준편차 1로 맞추기  (이상치에 덜 흔들림)
    18주차 StandardScaler가 바로 이 z-점수입니다.

    주의: 표준편차가 0이면 0으로 나누게 됩니다. 그럴 땐 0.0을 돌려주세요.
    """
    s = std_dev(nums)
    if s == 0:
        return 0.0
    return (value - mean(nums)) / s

# ─────────────────────────────────────────────
# 문제 5. 정규분포의 68-95-99.7 법칙
# ─────────────────────────────────────────────

def within_std(nums, k):
    """평균에서 표준편차 k개 이내에 있는 값의 '비율'을 돌려주세요.

    within_std(nums, 1) -> 0.68 근처   (정규분포라면)
    within_std(nums, 2) -> 0.95 근처
    within_std(nums, 3) -> 0.997 근처

    이게 그 유명한 68-95-99.7 법칙입니다.
    데이터가 종 모양(정규분포)이면 이 비율이 거의 항상 나옵니다.

    반대로 이 비율이 크게 어긋나면 "이 데이터는 정규분포가 아니구나"를 알 수 있습니다.
    (그래서 이 함수는 데이터 모양을 진단하는 도구이기도 합니다)

    힌트: abs(n - 평균) <= k * 표준편차 인 값의 개수를 세고 전체로 나누세요.
          표준편차가 0이면 모든 값이 같다는 뜻이니 1.0을 돌려주세요.
    """
    s = std_dev(nums)
    if s == 0:
        return 1.0
    
    m = mean(nums)
    cnt = 0
    for num in nums:
        if abs(num - m) <= k * s:
            cnt += 1

    return cnt / len(nums)

# ─────────────────────────────────────────────
# 문제 6. 확률
# ─────────────────────────────────────────────

def probability(records, key, value):
    """records 중에서 record[key] == value 인 것의 비율을 돌려주세요.

    records는 딕셔너리 리스트입니다:
        [{"sick": True, "test": "양성"}, {"sick": False, "test": "음성"}, ...]

    probability(records, "sick", True)  ->  전체 중 실제 환자의 비율

    힌트: 조건에 맞는 개수를 세고 전체 개수로 나누면 됩니다. 빈 리스트면 0.0
    """
    if len(records) == 0:
        return 0.0
    
    cnt = 0
    for record in records:
        if record[key] == value:
            cnt += 1
    return cnt / len(records)


# ─────────────────────────────────────────────
# 문제 7. 조건부확률  ★ 15주차의 핵심
# ─────────────────────────────────────────────

def conditional_prob(records, given_key, given_value, target_key, target_value):
    """P(target | given) — given이 참인 것들 '중에서만' target의 비율을 구해주세요.

    conditional_prob(records, "sick", True, "test", "양성")
        = 실제 환자들 중에서 검사가 양성으로 나온 비율
        = P(양성 | 환자)

    conditional_prob(records, "test", "양성", "sick", True)
        = 양성 판정 받은 사람들 중에서 진짜 환자인 비율
        = P(환자 | 양성)

    ★ 이 둘은 완전히 다른 숫자입니다. 순서가 바뀌면 답이 바뀝니다.
      base_rate_demo.py 를 돌려보면 얼마나 다른지 눈으로 보실 수 있습니다.

    구하는 법:
        1. given 조건에 맞는 것만 먼저 골라낸다  ← 이게 '전체'가 됩니다
        2. 그중에서 target에 맞는 개수를 센다
        3. 나눈다

    핵심은 1번입니다. '분모가 바뀌는 것'이 조건부확률의 전부입니다.
    조건이 붙으면 세상이 그 조건 안으로 좁혀집니다.

    힌트: subset = [r for r in records if r.get(given_key) == given_value]
          빈 subset이면 0.0
    """
    subset = [r for r in records if r.get(given_key) == given_value]
    if len(subset) == 0:
        return 0.0
    return probability(subset, target_key, target_value)


# ═════════════════════════════════════════════
# 아래는 채점기입니다. 고치지 마세요.
# ═════════════════════════════════════════════

def _val(fn):
    try:
        return fn()
    except Exception as e:
        return f"<에러: {type(e).__name__}: {e}>"


def _check(name, got, want, tol=1e-6):
    try:
        ok = abs(float(got) - float(want)) < tol
    except Exception:
        ok = got == want
    print(f"  {'✅' if ok else '❌'} {name}")
    if not ok:
        print(f"       기대한 값: {want}")
        print(f"       나온 값  : {got}")
    return ok


def main():
    print("\n12주차 연습 채점\n" + "─" * 50)
    results = []

    data = [2, 4, 4, 4, 5, 5, 7, 9]

    print("\n[문제 1~3] 평균 · 분산 · 표준편차")
    results.append(_check("mean(data)", _val(lambda: mean(data)), 5.0))
    results.append(_check("mean([]) — 빈 리스트", _val(lambda: mean([])), 0.0))
    results.append(_check("variance(data)", _val(lambda: variance(data)), 4.0))
    results.append(_check("std_dev(data)", _val(lambda: std_dev(data)), 2.0))
    results.append(_check("std_dev([5,5,5]) — 다 같으면 0",
                          _val(lambda: std_dev([5, 5, 5])), 0.0))

    print("\n[문제 4] z-점수")
    results.append(_check("z_score(5, data) — 평균이면 0", _val(lambda: z_score(5, data)), 0.0))
    results.append(_check("z_score(7, data) — 표준편차 1개 위", _val(lambda: z_score(7, data)), 1.0))
    results.append(_check("z_score(1, data) — 표준편차 2개 아래", _val(lambda: z_score(1, data)), -2.0))
    results.append(_check("z_score(5, [5,5,5]) — 0으로 나누기 방지",
                          _val(lambda: z_score(5, [5, 5, 5])), 0.0))

    print("\n[문제 5] 68-95-99.7")
    results.append(_check("within_std([1..9], 1)",
                          _val(lambda: within_std([1, 2, 3, 4, 5, 6, 7, 8, 9], 1)),
                          5 / 9))
    results.append(_check("within_std(data, 3) — 거의 전부",
                          _val(lambda: within_std(data, 3)), 1.0))
    results.append(_check("within_std([5,5,5], 1) — 다 같으면 1.0",
                          _val(lambda: within_std([5, 5, 5], 1)), 1.0))

    # 진짜 정규분포로 68-95-99.7이 나오는지 확인
    try:
        import random
        random.seed(0)
        normal = [random.gauss(0, 1) for _ in range(20000)]
        got1 = _val(lambda: within_std(normal, 1))
        got2 = _val(lambda: within_std(normal, 2))
        ok = isinstance(got1, float) and abs(got1 - 0.68) < 0.02 and abs(got2 - 0.95) < 0.02
        print(f"  {'✅' if ok else '❌'} 진짜 정규분포 2만 개로 확인 "
              f"(1σ={got1:.3f} 2σ={got2:.3f})" if isinstance(got1, float)
              else f"  ❌ 정규분포 확인 실패: {got1}")
        results.append(ok)
    except Exception:
        pass

    print("\n[문제 6~7] 확률 · 조건부확률")
    records = [
        {"sick": True, "test": "양성"},
        {"sick": True, "test": "양성"},
        {"sick": True, "test": "음성"},
        {"sick": False, "test": "양성"},
        {"sick": False, "test": "음성"},
        {"sick": False, "test": "음성"},
        {"sick": False, "test": "음성"},
        {"sick": False, "test": "음성"},
    ]
    results.append(_check("probability(환자) = 3/8",
                          _val(lambda: probability(records, "sick", True)), 3 / 8))
    results.append(_check("P(양성 | 환자) = 2/3  ← 환자 3명 중 2명이 양성",
                          _val(lambda: conditional_prob(records, "sick", True, "test", "양성")),
                          2 / 3))
    results.append(_check("P(환자 | 양성) = 2/3  ← 양성 3명 중 2명이 환자",
                          _val(lambda: conditional_prob(records, "test", "양성", "sick", True)),
                          2 / 3))
    results.append(_check("P(음성 | 건강) = 4/5",
                          _val(lambda: conditional_prob(records, "sick", False, "test", "음성")),
                          4 / 5))
    results.append(_check("조건에 맞는 게 없으면 0.0",
                          _val(lambda: conditional_prob(records, "sick", "몰라", "test", "양성")),
                          0.0))

    passed = sum(1 for r in results if r)
    total = len(results)
    print("\n" + "─" * 50)
    print(f"{passed} / {total} 통과")

    if passed == total:
        print("""
전부 통과했습니다.

위 예제에서는 P(양성|환자)와 P(환자|양성)이 우연히 둘 다 2/3였습니다.
일부러 그렇게 만든 겁니다 — "그럼 같은 거 아닌가?" 싶으시라고요.

base_rate_demo.py 를 돌려보세요. 현실적인 숫자를 넣으면
이 둘이 얼마나 끔찍하게 달라지는지 보실 수 있습니다.

  python base_rate_demo.py
""")
    else:
        print("\n❌ 항목의 '기대한 값'과 '나온 값'을 비교해보세요.\n")


if __name__ == "__main__":
    main()