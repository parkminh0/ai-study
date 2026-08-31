"""
순수 파이썬 반복문 vs NumPy — 속도 비교

사용법:
    python speed_compare.py

정답을 맞히는 연습이 아니라, 눈으로 차이를 보는 실험입니다.
"""

import math
import time
import numpy as np

N = 3_000_000


def pure_python(n):
    """숫자 하나하나에 sqrt(x^2 + 3x + 2) 계산을 반복합니다."""
    result = []
    for i in range(n):
        x = i * 0.0001
        result.append(math.sqrt(x**2 + 3 * x + 2))
    return sum(result)


def numpy_version(n):
    """같은 계산을 배열 전체에 한 번에 적용합니다."""
    x = np.arange(n) * 0.0001
    return float(np.sqrt(x**2 + 3 * x + 2).sum())


def main():
    print(f"\n{N:,}개의 숫자에 sqrt(x²+3x+2) 계산하고 모두 더하기\n" + "─" * 46)

    t0 = time.perf_counter()
    r1 = pure_python(N)
    t1 = time.perf_counter()
    py_time = t1 - t0
    print(f"순수 파이썬 for문 : {py_time:.3f}초   (결과: {r1:.2f})")

    t0 = time.perf_counter()
    r2 = numpy_version(N)
    t1 = time.perf_counter()
    np_time = t1 - t0
    print(f"NumPy 벡터 연산   : {np_time:.3f}초   (결과: {r2:.2f})")

    ratio = py_time / np_time if np_time > 0 else float("inf")
    print(f"\nNumPy가 약 {ratio:.1f}배 빠릅니다. (기기마다 배율은 다르게 나옵니다)")

    print("""
왜 차이가 날까요?

파이썬 for문은 숫자 하나씩 꺼내서 파이썬 객체로 만들고,
math.sqrt를 부르고, 결과를 리스트에 담는 과정을 300만 번 반복합니다.
매번 '이게 정수인지 실수인지' 확인하는 부담도 있습니다.

NumPy는 숫자들을 메모리에 촘촘히 붙여 저장해두고,
C로 미리 짜여진 코드가 그 덩어리 전체에 sqrt를 한 번에 적용합니다.
파이썬 반복문이 끼어들 틈이 없어서 훨씬 빠릅니다.

참고로 모든 연산이 이렇게 크게 차이 나는 건 아닙니다.
그냥 숫자를 더하기만 하는 것처럼 계산이 아주 가벼우면,
배열을 새로 만드는 비용이 오히려 더 커서 차이가 작거나 역전되기도 합니다.
'배열 하나를 새로 만드는 것'과 '이미 있는 배열을 계산하는 것'은
비용이 다르다는 걸 기억해두세요 — 8단계 데이터 파이프라인에서 다시 만납니다.

규칙 하나만 기억하세요:
    NumPy 배열을 다룰 때 for문으로 하나씩 접근하고 있다면,
    대부분 배열 연산이나 axis로 바꿀 수 있는 방법이 있습니다.
""")


if __name__ == "__main__":
    main()