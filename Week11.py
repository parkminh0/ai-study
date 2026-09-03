"""
11주차 연습 — 선형대수 직관

사용법:
    python week11_practice.py

이번 주는 NumPy가 대신 해주던 걸 직접 손으로 만들어봅니다.
np.dot()이나 A @ B 를 쓰지 마세요. for문으로 직접 짜는 게 목적입니다.
한 번 만들어보면 다시는 "행렬곱이 뭐였지?" 하지 않게 됩니다.

━━ 이번 주에 잡을 그림 ━━

내적(dot product)이 이번 주의 주인공입니다. 두 벡터를 넣으면 숫자 하나가 나오는데,
그 숫자가 "두 벡터가 얼마나 같은 방향인가"를 뜻합니다.

    같은 방향  →  내적이 큼
    직각       →  내적이 0
    반대 방향  →  내적이 음수

그리고 이게 31주차에 배울 "임베딩으로 비슷한 문서 찾기"의 정체입니다.
문장을 숫자 벡터로 바꾼 다음, 내적으로 방향이 비슷한 걸 찾는 거예요.
이번 주 마지막 문제에서 그걸 직접 만들어봅니다.
"""

import math


# ─────────────────────────────────────────────
# 문제 1. 내적 — 이번 주의 주인공
# ─────────────────────────────────────────────

def manual_dot(a, b):
    """두 벡터의 내적을 for문으로 직접 계산해주세요. (np.dot 금지)

    내적 = 같은 자리끼리 곱해서 전부 더하기

    manual_dot([1, 2, 3], [4, 5, 6])
        = 1*4 + 2*5 + 3*6
        = 4 + 10 + 18
        = 32

    힌트: total = 0 으로 시작해서 for i in range(len(a)) 로 돌면 됩니다.
          2주차 my_sum과 구조가 같습니다.
    """
    result = 0
    for x, y in zip(a, b):
        result += x * y
    return result


# ─────────────────────────────────────────────
# 문제 2. 행렬곱 — 내적을 여러 번 하는 것일 뿐
# ─────────────────────────────────────────────

def manual_matmul(A, B):
    """두 행렬의 곱을 for문으로 직접 계산해주세요. (@ 나 np.dot 금지)

    A = [[1, 2],        B = [[5, 6],
         [3, 4]]             [7, 8]]

    결과[0][0] = A의 0번 행 · B의 0번 열 = [1,2]·[5,7] = 1*5 + 2*7 = 19
    결과[0][1] = A의 0번 행 · B의 1번 열 = [1,2]·[6,8] = 1*6 + 2*8 = 22
    결과[1][0] = A의 1번 행 · B의 0번 열 = [3,4]·[5,7] = 3*5 + 4*7 = 43
    결과[1][1] = A의 1번 행 · B의 1번 열 = [3,4]·[6,8] = 3*6 + 4*8 = 50

    manual_matmul(A, B) -> [[19, 22], [43, 50]]

    ★ 핵심: 행렬곱은 "A의 각 행과 B의 각 열의 내적"을 모아놓은 것입니다.
      새로운 연산이 아니라, 문제 1을 여러 번 하는 것뿐입니다.

    힌트: for문 세 개가 필요합니다.
        i — A의 행 (결과의 행)
        j — B의 열 (결과의 열)
        k — 내적을 계산하며 훑는 위치

        for i in range(len(A)):
            row = []
            for j in range(len(B[0])):
                s = 0
                for k in range(len(B)):
                    s += A[i][k] * B[k][j]
                row.append(s)
            result.append(row)

    (힌트를 그대로 베끼지 말고, 왜 k가 저 자리에 오는지 종이에 그려보세요.
     A[i][k] 와 B[k][j] 에서 k가 양쪽에 다 있는 게 핵심입니다.)
    """
    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            s = 0
            for k in range(len(B)):
                s += A[i][k] * B[k][j]
            row.append(s)
        result.append(row)
    return result


# ─────────────────────────────────────────────
# 문제 3. 벡터의 길이
# ─────────────────────────────────────────────

def magnitude(v):
    """벡터의 길이(크기)를 돌려주세요.

    피타고라스 정리를 차원 수만큼 확장한 것입니다.
        2차원: √(x² + y²)
        n차원: √(v[0]² + v[1]² + ... )

    magnitude([3, 4]) -> 5.0        (3-4-5 직각삼각형)

    힌트: 제곱을 다 더하고 math.sqrt()
          사실 magnitude(v) == sqrt(manual_dot(v, v)) 입니다. 왜 그런지 생각해보세요.
    """
    return math.sqrt(sum(map(lambda x : x ** 2, v)))


# ─────────────────────────────────────────────
# 문제 4. 코사인 유사도 — 방향만 비교하기  ★ 31주차의 핵심
# ─────────────────────────────────────────────

def cosine_similarity(a, b):
    """두 벡터가 얼마나 같은 방향인지를 -1 ~ 1 사이 숫자로 돌려주세요.

    공식:  내적 / (a의 길이 × b의 길이)

    왜 길이로 나누나요?
        내적만 쓰면 '긴 벡터'가 무조건 유리합니다.
        긴 문서가 무조건 비슷하다고 나와버려요.
        길이로 나누면 크기는 지워지고 '방향'만 남습니다.

    cosine_similarity([1, 0], [1, 0])   -> 1.0    같은 방향
    cosine_similarity([1, 0], [0, 1])   -> 0.0    직각 (전혀 무관)
    cosine_similarity([1, 0], [-1, 0])  -> -1.0   반대 방향
    cosine_similarity([1, 0], [5, 0])   -> 1.0    길이가 달라도 방향이 같으면 1

    주의: 길이가 0인 벡터가 들어오면 0으로 나누게 됩니다.
          (7주차 min_max_normalize의 NaN 함정, 기억나시죠?)
          그런 경우엔 0.0을 돌려주세요.
    """
    try:
        return manual_dot(a, b) / (magnitude(a) * magnitude(b))
    except:
        return 0.0


# ─────────────────────────────────────────────
# 문제 5. 문장을 숫자 벡터로
# ─────────────────────────────────────────────

def text_to_vector(text, vocab):
    """문장을 단어 개수 벡터로 바꿔주세요.

    vocab은 '단어 사전'입니다. 벡터의 각 자리가 어떤 단어인지 정해줍니다.

    vocab = ["red", "book", "blue"]
    text_to_vector("red book red", vocab) -> [2, 1, 0]
                                              │  │  └ "blue"가 0번
                                              │  └─── "book"이 1번
                                              └────── "red"가 2번

    소문자로 바꾸고 공백으로 나눠서 세면 됩니다.
    2주차 count_words와 같은 일인데, 결과를 딕셔너리가 아니라
    '정해진 순서의 리스트'로 만드는 게 다릅니다.
    순서가 고정되어야 벡터끼리 비교할 수 있으니까요.

    힌트: words = text.lower().split() 후에
          [words.count(w) for w in vocab]
    """
    text = text.lower().split()
    return [text.count(w) for w in vocab]


# ─────────────────────────────────────────────
# 문제 6. 가장 비슷한 문장 찾기 ← 전부 합치기
# ─────────────────────────────────────────────

def most_similar(query, texts):
    """texts 중에서 query와 가장 비슷한 문장과 그 점수를 돌려주세요.
    돌려줄 모양: (가장_비슷한_문장, 점수)   점수는 소수 셋째 자리 반올림

    순서:
        1. query와 texts의 모든 단어를 모아 vocab을 만듭니다 (정렬해서 순서 고정)
        2. query를 벡터로 바꿉니다
        3. texts를 하나씩 벡터로 바꿔가며 cosine_similarity를 계산합니다
        4. 점수가 가장 높은 것을 돌려줍니다

    힌트 (vocab 만들기):
        vocab = sorted({w for t in [query] + texts for w in t.lower().split()})

    ★ 이게 바로 검색 엔진과 RAG의 가장 단순한 형태입니다.
      31주차에는 단어 개수 대신 'LLM이 만든 임베딩'을 벡터로 쓰지만,
      비슷한 걸 찾는 방법은 오늘 만든 코사인 유사도 그대로입니다.
    """
    vocab = sorted({w for t in [query] + texts for w in t.lower().split()})
    query_vector = text_to_vector(query, vocab)
    rt, rc = 0, 0
    for i, t in enumerate(texts):
        text_vector = text_to_vector(t, vocab)
        s = cosine_similarity(query_vector, text_vector)
        if rc < s:
            rt, rc = t, s
    return (rt, rc)


# ═════════════════════════════════════════════
# 아래는 채점기입니다. 고치지 마세요.
# ═════════════════════════════════════════════

def _val(fn):
    try:
        return fn()
    except Exception as e:
        return f"<에러: {type(e).__name__}: {e}>"


def _close(a, b, tol=1e-6):
    try:
        return abs(float(a) - float(b)) < tol
    except Exception:
        return False


def _check(name, got, want, tol=None):
    ok = _close(got, want, tol) if tol is not None else got == want
    print(f"  {'✅' if ok else '❌'} {name}")
    if not ok:
        print(f"       기대한 값: {want!r}")
        print(f"       나온 값  : {got!r}")
    return ok


def main():
    print("\n11주차 연습 채점\n" + "─" * 50)
    results = []

    print("\n[문제 1] 내적")
    results.append(_check("manual_dot([1,2,3], [4,5,6])",
                          _val(lambda: manual_dot([1, 2, 3], [4, 5, 6])), 32))
    results.append(_check("manual_dot([1,0], [0,1]) — 직각이면 0",
                          _val(lambda: manual_dot([1, 0], [0, 1])), 0))
    results.append(_check("manual_dot([2,2], [-1,-1]) — 반대 방향이면 음수",
                          _val(lambda: manual_dot([2, 2], [-1, -1])), -4))

    print("\n[문제 2] 행렬곱")
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    results.append(_check("manual_matmul(A, B)", _val(lambda: manual_matmul(A, B)),
                          [[19, 22], [43, 50]]))
    C = [[1, 2, 3], [4, 5, 6]]      # 2×3
    D = [[7, 8], [9, 10], [11, 12]]  # 3×2
    results.append(_check("manual_matmul (2×3 × 3×2 = 2×2)",
                          _val(lambda: manual_matmul(C, D)), [[58, 64], [139, 154]]))

    # numpy와 대조 — 직접 만든 게 진짜 맞는지
    try:
        import numpy as np
        got = _val(lambda: manual_matmul(A, B))
        want = (np.array(A) @ np.array(B)).tolist()
        ok = got == want
        print(f"  {'✅' if ok else '❌'} numpy의 A @ B 와 결과가 일치")
        if not ok:
            print(f"       numpy: {want}")
            print(f"       내 것: {got}")
        results.append(ok)
    except ImportError:
        pass

    print("\n[문제 3] 벡터의 길이")
    results.append(_check("magnitude([3,4])", _val(lambda: magnitude([3, 4])), 5.0, tol=1e-6))
    results.append(_check("magnitude([1,1,1,1])", _val(lambda: magnitude([1, 1, 1, 1])), 2.0, tol=1e-6))

    print("\n[문제 4] 코사인 유사도")
    results.append(_check("같은 방향 [1,0]·[1,0]",
                          _val(lambda: cosine_similarity([1, 0], [1, 0])), 1.0, tol=1e-6))
    results.append(_check("직각 [1,0]·[0,1]",
                          _val(lambda: cosine_similarity([1, 0], [0, 1])), 0.0, tol=1e-6))
    results.append(_check("반대 방향 [1,0]·[-1,0]",
                          _val(lambda: cosine_similarity([1, 0], [-1, 0])), -1.0, tol=1e-6))
    results.append(_check("길이가 달라도 방향이 같으면 1 — [1,0]·[5,0]",
                          _val(lambda: cosine_similarity([1, 0], [5, 0])), 1.0, tol=1e-6))
    results.append(_check("영벡터는 0 (0으로 나누기 방지)",
                          _val(lambda: cosine_similarity([0, 0], [1, 2])), 0.0, tol=1e-6))

    print("\n[문제 5] 문장 → 벡터")
    vocab = ["red", "book", "blue"]
    results.append(_check('text_to_vector("red book red", vocab)',
                          _val(lambda: text_to_vector("red book red", vocab)), [2, 1, 0]))
    results.append(_check('text_to_vector("Blue BOOK", vocab) — 대소문자 무시',
                          _val(lambda: text_to_vector("Blue BOOK", vocab)), [0, 1, 1]))

    print("\n[문제 6] 가장 비슷한 문장 찾기")
    texts = [
        "the great gatsby",
        "a light in the attic",
        "the attic of secrets",
        "python programming basics",
    ]
    got = _val(lambda: most_similar("secrets in the attic", texts))
    ok = isinstance(got, tuple) and len(got) == 2 and got[0] == "the attic of secrets"
    print(f"  {'✅' if ok else '❌'} most_similar('secrets in the attic', ...)")
    if not ok:
        print("       기대: ('the attic of secrets', 점수)")
        print(f"       나온 값: {got!r}")
    results.append(ok)

    got2 = _val(lambda: most_similar("learning python", texts))
    ok2 = isinstance(got2, tuple) and got2[0] == "python programming basics"
    print(f"  {'✅' if ok2 else '❌'} most_similar('learning python', ...)")
    if not ok2:
        print(f"       기대: ('python programming basics', 점수) / 나온 값: {got2!r}")
    results.append(ok2)

    passed = sum(1 for r in results if r)
    total = len(results)
    print("\n" + "─" * 50)
    print(f"{passed} / {total} 통과")

    if passed == total:
        print("\n방금 만든 걸로 실제 검색을 해봅시다:\n")
        library = [
            "a light in the attic",
            "the black maria",
            "starving hearts",
            "shakespeare sonnets",
            "the coming woman",
            "the boys in the boat",
            "olio",
            "libertarianism for beginners",
        ]
        for q in ["light attic", "the boat", "beginners guide"]:
            best, score = most_similar(q, library)
            print(f'  "{q}"  →  "{best}"   (유사도 {score})')

        print("""
검색어와 정확히 같은 단어가 없어도, 겹치는 단어가 많으면 찾아냅니다.
이게 검색의 가장 단순한 형태입니다.

한계도 같이 보세요: "beginners guide"는 'guide'라는 단어가 어디에도 없어서
'beginners' 하나에만 의존합니다. 그리고 "책"과 "도서"처럼 뜻은 같지만
글자가 다른 단어는 전혀 못 잡습니다.

31주차의 임베딩이 바로 그 한계를 푸는 도구입니다.
단어 개수 대신 '뜻'을 벡터로 만들거든요. 하지만 비슷한 걸 찾는 방법은
오늘 만든 코사인 유사도 그대로입니다. 도구만 바뀌고 원리는 안 바뀝니다.

이제 matrix_as_transform.py 를 돌려서, 행렬이 공간에 무슨 짓을 하는지 보세요.

  git add . && git commit -m "11주차 선형대수 직관" && git push
""")
    else:
        print("\n❌ 항목의 '기대한 값'과 '나온 값'을 비교해보세요.\n")


if __name__ == "__main__":
    main()