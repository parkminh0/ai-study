"""
2주차 연습 — 반복문과 딕셔너리

사용법:
    python week2_practice.py

각 함수의 pass를 지우고 직접 채우세요.
채우는 대로 아래 채점 결과가 ✅로 바뀝니다.

규칙: sum(), max(), min()은 쓰지 마세요. 직접 만드는 게 목적입니다.
      len(), sorted()는 써도 됩니다.
"""


# ─────────────────────────────────────────────
# 문제 1. 반복문으로 숫자 다루기
# ─────────────────────────────────────────────

def my_sum(nums):
    """리스트 안 숫자를 모두 더해서 돌려주세요.

    힌트: total = 0 으로 시작해서, for 문으로 하나씩 더해갑니다.
    my_sum([1, 2, 3]) -> 6
    """
    result = 0
    for value in nums:
        result += value
    return result


def my_average(nums):
    """평균을 돌려주세요. 빈 리스트면 0.

    힌트: 위에서 만든 my_sum을 그대로 갖다 쓰세요. 함수는 재활용하라고 있는 겁니다.
    my_average([1, 2, 3, 4]) -> 2.5
    """
    if len(nums) == 0:
        return 0
    else:
        return my_sum(nums) / len(nums)


def my_max(nums):
    """가장 큰 값을 돌려주세요. 빈 리스트면 None.

    힌트: 첫 번째 값을 '현재 챔피언'으로 두고, 더 큰 게 나오면 교체합니다.
    my_max([3, 9, 2]) -> 9
    """
    if len(nums) == 0:
        return None
    
    result = nums[0]
    for value in nums:
        if value > result:
            result = value
    return result


# ─────────────────────────────────────────────
# 문제 2. 조건문
# ─────────────────────────────────────────────

def grade(score):
    """점수를 학점으로. 90이상 A, 80이상 B, 70이상 C, 나머지 F.

    힌트: if / elif / else. 순서가 중요합니다 — 왜 큰 수부터 검사해야 할까요?
    grade(85) -> "B"
    """
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "F"


# ─────────────────────────────────────────────
# 문제 3. 딕셔너리로 개수 세기  ← 이번 주의 핵심
# ─────────────────────────────────────────────

def count_words(text):
    """문장에서 단어가 몇 번 나왔는지 세어 딕셔너리로 돌려주세요.

    힌트: text.split() 이 단어 리스트를 만들어 줍니다.
          처음 보는 단어면 1, 이미 있으면 +1.
    count_words("a b a") -> {"a": 2, "b": 1}
    """
    dict = {}
    for value in text.split():
        dict[value] = dict.get(value, 0) + 1
    return dict


def top_n(counts, n):
    """가장 많이 나온 단어 n개를 [(단어, 횟수), ...] 순서로 돌려주세요.

    힌트: list(counts.items()) 로 [(단어, 횟수), ...] 를 만든 뒤
          .sort(key=..., reverse=True) 로 횟수 기준 내림차순 정렬합니다.
          key 부분이 어려우면 여기까지는 건너뛰어도 좋습니다.
    top_n({"a": 2, "b": 5, "c": 1}, 2) -> [("b", 5), ("a", 2)]
    """
    return sorted(list(counts.items()), key=lambda x : x[1], reverse=True)[:n]


# ═════════════════════════════════════════════
# 아래는 채점기입니다. 고치지 마세요.
# ═════════════════════════════════════════════

def _check(name, got, want):
    if got == want:
        print(f"  ✅ {name}")
        return True
    print(f"  ❌ {name}")
    print(f"       기대한 값: {want!r}")
    print(f"       나온 값  : {got!r}")
    return False


def main():
    print("\n2주차 연습 채점\n" + "─" * 42)
    results = []

    print("\n[문제 1] 반복문")
    results.append(_check("my_sum([1, 2, 3])", my_sum([1, 2, 3]), 6))
    results.append(_check("my_sum([])", my_sum([]), 0))
    results.append(_check("my_average([1, 2, 3, 4])", my_average([1, 2, 3, 4]), 2.5))
    results.append(_check("my_average([])", my_average([]), 0))
    results.append(_check("my_max([3, 9, 2])", my_max([3, 9, 2]), 9))
    results.append(_check("my_max([-5, -1, -9])", my_max([-5, -1, -9]), -1))
    results.append(_check("my_max([])", my_max([]), None))

    print("\n[문제 2] 조건문")
    results.append(_check("grade(95)", grade(95), "A"))
    results.append(_check("grade(85)", grade(85), "B"))
    results.append(_check("grade(70)", grade(70), "C"))
    results.append(_check("grade(12)", grade(12), "F"))

    print("\n[문제 3] 딕셔너리")
    results.append(_check('count_words("a b a")', count_words("a b a"), {"a": 2, "b": 1}))
    results.append(_check('count_words("")', count_words(""), {}))
    results.append(_check(
        'count_words("hi hi hi bye")',
        count_words("hi hi hi bye"),
        {"hi": 3, "bye": 1},
    ))
    results.append(_check(
        "top_n({a:2, b:5, c:1}, 2)",
        top_n({"a": 2, "b": 5, "c": 1}, 2),
        [("b", 5), ("a", 2)],
    ))

    passed = sum(1 for r in results if r)
    print("\n" + "─" * 42)
    print(f"{passed} / {len(results)} 통과")
    if passed == len(results):
        print("\n전부 통과했습니다. 커밋하고 3주차로 넘어가세요.")
        print("  git add . && git commit -m \"2주차 연습 완료\" && git push")
    else:
        print("\n❌ 항목의 '기대한 값'과 '나온 값'을 비교해보세요.")
        print("막히면 그 함수만 물어보시면 됩니다.")
    print()


if __name__ == "__main__":
    main()