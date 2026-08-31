"""
7주차 연습 — NumPy

사용법:
    pip install numpy
    python week7_practice.py

지금까지 숫자를 하나씩 다뤘다면, 이제부터는 숫자 뭉치를 통째로 다룹니다.
    [1, 2, 3] + [10, 20, 30]  # 파이썬 리스트: 에러 또는 이어붙이기
    array([1,2,3]) + array([10,20,30])  # NumPy: [11, 22, 33] — 각 자리끼리 더함

이 차이 하나가 NumPy를 쓰는 이유의 8할입니다.
"""

import numpy as np


# ─────────────────────────────────────────────
# 문제 1. 배열 만들기와 인덱싱
# ─────────────────────────────────────────────

def make_array(nums):
    """리스트를 NumPy 배열로 바꿔주세요.

    make_array([1, 2, 3]) -> array([1, 2, 3])

    힌트: np.array(nums)
    """
    return np.array(nums)


def get_middle_row(matrix):
    """2차원 배열(행렬)에서 가운데 행을 돌려주세요. (행이 홀수 개라고 가정)

    get_middle_row(np.array([[1,2],[3,4],[5,6]])) -> array([3, 4])

    힌트: len(matrix) 로 행 개수를 알 수 있습니다. 가운데 인덱스 = 행개수 // 2
          matrix[인덱스] 로 그 행 하나를 통째로 꺼냅니다.
    """
    return np.array(matrix)[len(matrix) // 2]


# ─────────────────────────────────────────────
# 문제 2. 축(axis) — 어느 방향으로 더할 것인가  ★ 이번 주 핵심
# ─────────────────────────────────────────────

def row_sums(matrix):
    """각 '행'의 합을 구해 1차원 배열로 돌려주세요. (가로로 더하기)

    matrix = [[1, 2, 3],
              [4, 5, 6]]
    row_sums(matrix) -> array([6, 15])     # 1+2+3=6,  4+5+6=15

    힌트: np.sum(matrix, axis=1)
          axis=1 은 '각 행 안에서' 더하라는 뜻입니다. (→ 방향)
    """
    return np.sum(matrix, axis=1)


def col_sums(matrix):
    """각 '열'의 합을 구해 1차원 배열로 돌려주세요. (세로로 더하기)

    같은 matrix로:
    col_sums(matrix) -> array([5, 7, 9])   # 1+4=5,  2+5=7,  3+6=9

    힌트: np.sum(matrix, axis=0)
          axis=0 은 '각 열을 따라 아래로' 더하라는 뜻입니다. (↓ 방향)
          row_sums과 axis 숫자만 다릅니다 — 헷갈리면 그림을 그려보세요.
    """
    return np.sum(matrix, axis=0)


# ─────────────────────────────────────────────
# 문제 3. 브로드캐스팅 — 크기가 다른데 어떻게 계산되나  ★ 핵심
# ─────────────────────────────────────────────

def scale_by(matrix, factor):
    """행렬의 모든 원소에 factor를 곱해서 돌려주세요.

    scale_by(np.array([[1,2],[3,4]]), 10) -> array([[10,20],[30,40]])

    힌트: matrix * factor 그대로 됩니다.
          숫자 하나(factor)가 행렬 전체 크기에 맞춰 '복제'되어 곱해집니다.
          이게 브로드캐스팅의 가장 단순한 형태입니다.
    """
    return matrix * factor


def add_row_vector(matrix, row_vector):
    """matrix의 모든 행에 row_vector를 더해서 돌려주세요.

    matrix       = [[1, 2, 3],
                     [4, 5, 6]]
    row_vector   = [10, 20, 30]

    add_row_vector(matrix, row_vector)
        -> array([[11, 22, 33],
                   [14, 25, 36]])

    힌트: matrix + row_vector 그대로 됩니다.
          (2, 3) 크기 행렬에 (3,) 크기 벡터를 더하면,
          NumPy가 row_vector를 각 행마다 복제해서 더해줍니다.
          이게 8단계 신경망에서 '편향(bias)을 더한다'는 연산의 정체입니다.
    """
    return matrix + row_vector


def min_max_normalize(arr):
    """arr의 모든 값을 0~1 사이로 눌러서 돌려주세요.

    min_max_normalize(np.array([0, 5, 10])) -> array([0. , 0.5, 1. ])

    공식: (값 - 최솟값) / (최댓값 - 최솟값)

    힌트: arr.min(), arr.max() 로 최솟값·최댓값을 구합니다.
          그다음 (arr - lo) / (hi - lo) — 이것도 브로드캐스팅입니다.
          숫자 하나(lo, hi)가 배열 전체에서 한 번에 빠지고 나뉩니다.
          11주차 데이터 정규화에서 그대로 다시 만나게 됩니다.
    """
    minimum, maximum = arr.min(), arr.max()
    return (arr - arr.min()) / (arr.max() - arr.min())


# ═════════════════════════════════════════════
# 아래는 채점기입니다. 고치지 마세요.
# ═════════════════════════════════════════════

def _eq(a, b):
    """숫자든 배열이든 알아서 비교합니다."""
    try:
        return bool(np.allclose(np.asarray(a, dtype=float), np.asarray(b, dtype=float)))
    except Exception:
        return a == b


def _check(name, got, want):
    if _eq(got, want):
        print(f"  ✅ {name}")
        return True
    print(f"  ❌ {name}")
    print(f"       기대한 값: {want}")
    print(f"       나온 값  : {got}")
    return False


def _val(fn):
    """아직 안 만든 함수 때문에 채점기가 멈추지 않도록 감싸줍니다."""
    try:
        return fn()
    except Exception as e:
        return f"<에러: {type(e).__name__}: {e}>"


def main():
    print("\n7주차 연습 채점\n" + "─" * 46)
    results = []

    m = np.array([[1, 2, 3], [4, 5, 6]])
    m3 = np.array([[1, 2], [3, 4], [5, 6]])

    print("\n[문제 1] 배열과 인덱싱")
    results.append(_check("make_array([1,2,3])", _val(lambda: make_array([1, 2, 3])), [1, 2, 3]))
    results.append(_check("get_middle_row (3행 중 가운데)", _val(lambda: get_middle_row(m3)), [3, 4]))

    print("\n[문제 2] 축(axis)")
    results.append(_check("row_sums(matrix)", _val(lambda: row_sums(m)), [6, 15]))
    results.append(_check("col_sums(matrix)", _val(lambda: col_sums(m)), [5, 7, 9]))

    print("\n[문제 3] 브로드캐스팅")
    results.append(_check("scale_by(matrix, 10)", _val(lambda: scale_by(m, 10)),
                          [[10, 20, 30], [40, 50, 60]]))
    results.append(_check(
        "add_row_vector(matrix, [10,20,30])",
        _val(lambda: add_row_vector(m, np.array([10, 20, 30]))),
        [[11, 22, 33], [14, 25, 36]]))
    results.append(_check(
        "min_max_normalize([0,5,10])",
        _val(lambda: min_max_normalize(np.array([0, 5, 10]))),
        [0.0, 0.5, 1.0]))

    def _nan_probe():
        r = min_max_normalize(np.array([2.0, 2.0, 2.0]))
        arr = np.asarray(r, dtype=float)
        if np.isnan(arr).any():
            return "NaN 발생 — 최댓값=최솟값일 때 0으로 나눔"
        return r

    results.append(_check(
        "min_max_normalize([2,2,2]) 는 나눗셈이 0이 되는 함정",
        _val(_nan_probe),
        "NaN 발생 — 최댓값=최솟값일 때 0으로 나눔"))

    passed = sum(1 for r in results if r)
    print("\n" + "─" * 46)
    print(f"{passed} / {len(results)} 통과")

    if passed == len(results):
        print("""
전부 통과했습니다.

마지막 문제가 이상하게 느껴지셨을 텐데, 일부러 넣었습니다.
모든 값이 똑같은 배열을 정규화하면 최댓값-최솟값이 0이 되어
0으로 나누는 상황이 생깁니다. 에러 없이 조용히 'nan'이 나오는데,
이런 조용한 실패가 나중에 제일 찾기 어려운 버그가 됩니다.
지금은 이런 게 있다는 것만 기억해두세요 — 16주차에 다시 다룹니다.

다음으로 speed_compare.py 를 돌려서 NumPy가 왜 쓰이는지
직접 눈으로 확인해보세요.

  git add . && git commit -m "7주차 NumPy 연습" && git push
""")
    else:
        print("\n❌ 항목의 '기대한 값'과 '나온 값'을 비교해보세요.")
        print("axis=0 과 axis=1 이 헷갈리면: 종이에 행렬을 그리고")
        print("화살표로 '이 방향으로 더한다'를 표시해보세요.")
    print()


if __name__ == "__main__":
    main()