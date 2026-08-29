"""
3주차 연습 — 함수와 파일 입출력

사용법:
    python week3_practice.py

각 함수의 pass를 지우고 직접 채우세요.
전부 통과하면 sample.txt를 읽어서 top_words.txt를 만들어 냅니다.
그게 이번 주 완료 기준입니다: "스크립트 하나로 파일을 읽고 결과를 저장한다"

규칙: 파일을 열 때는 반드시 with open(...) 형태를 쓰세요.
      collections.Counter는 아직 쓰지 마세요. 직접 만드는 게 목적입니다.
"""

import os


# ─────────────────────────────────────────────
# 문제 1. 파일 읽기
# ─────────────────────────────────────────────

def read_text(path):
    """파일 전체를 문자열 하나로 읽어서 돌려주세요.

    힌트:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    encoding="utf-8"을 빼먹으면 한글에서 깨집니다. 습관으로 붙이세요.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ─────────────────────────────────────────────
# 문제 2. 파일 쓰기
# ─────────────────────────────────────────────

def write_lines(path, lines):
    """문자열 리스트를 한 줄에 하나씩 파일로 저장하세요. (돌려줄 값 없음)

    힌트: "w" 모드로 열고, for문으로 f.write(line + "\\n")
          "\\n"을 안 붙이면 전부 한 줄로 붙어버립니다.

    write_lines("out.txt", ["a", "b"])  ->  파일 내용이 "a\\nb\\n"
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))
        f.write('\n')


# ─────────────────────────────────────────────
# 문제 3. 단어 다듬기
# ─────────────────────────────────────────────

def clean_word(word):
    """단어 양 끝의 구두점을 떼고 소문자로 바꿔 돌려주세요.

    왜 필요한가: "AI"와 "ai,"와 "AI."를 다른 단어로 세면 통계가 엉망이 됩니다.
                 실제 데이터 작업의 절반은 이런 '정리'입니다.

    힌트: 문자열에는 .strip("떼어낼문자들") 과 .lower() 가 있습니다.
          .strip은 양 끝만 건드리므로 don't 의 ' 는 살아남습니다.

    clean_word("Hello,")  -> "hello"
    clean_word("AI!")     -> "ai"
    clean_word("don't")   -> "don't"
    """
    return word.strip('.,?!()').lower()


# ─────────────────────────────────────────────
# 문제 4. 단어 세기 (2주차 코드 재활용)
# ─────────────────────────────────────────────

def word_frequency(text):
    """문자열을 받아 {단어: 횟수} 딕셔너리를 돌려주세요.
    단어는 clean_word로 다듬고, 빈 문자열("")이 되면 건너뜁니다.

    힌트: 2주차 count_words에 clean_word 한 줄만 끼워 넣으면 됩니다.
          지난주에 만든 함수를 재활용하는 것 — 이게 함수를 배우는 이유입니다.

    word_frequency("AI is fun. ai is hard!")
        -> {"ai": 2, "is": 2, "fun": 1, "hard": 1}
    """
    dict = {}
    for value in text.split():
        word = clean_word(value)
        dict[word] = dict.get(word, 0) + 1
    return dict


# ─────────────────────────────────────────────
# 문제 5. 상위 n개 뽑기
# ─────────────────────────────────────────────

def top_n(counts, n):
    """많이 나온 순서로 n개를 [(단어, 횟수), ...] 로 돌려주세요.
    횟수가 같으면 단어를 사전순(가나다/abc)으로.

    힌트: pairs.sort(key=lambda p: (-p[1], p[0]))
          앞에 마이너스를 붙이면 큰 것이 먼저 옵니다.
          두 개를 묶어 주면 첫 번째가 같을 때 두 번째로 비교합니다.

    top_n({"b": 2, "a": 2, "c": 5}, 2) -> [("c", 5), ("a", 2)]
    """
    return sorted(list(counts.items()), key=lambda x : (-x[1], x[0]))[:n]


# ─────────────────────────────────────────────
# 문제 6. 전부 이어 붙이기  ← 이번 주의 목표
# ─────────────────────────────────────────────

def save_top_words(in_path, out_path, n):
    """in_path 파일을 읽어 가장 많이 나온 단어 n개를 out_path에 저장하세요.
    저장 형식은 한 줄에 하나씩  단어: 횟수
    그리고 [(단어, 횟수), ...] 리스트를 돌려주세요.

    힌트: 위에서 만든 함수 4개를 순서대로 부르기만 하면 됩니다.
          read_text -> word_frequency -> top_n -> write_lines
          새로 짜는 코드는 거의 없습니다. 함수를 쌓는다는 게 이런 뜻입니다.

    저장 예시:
        ai: 5
        data: 3
    """
    topN = top_n(word_frequency(read_text(in_path)), n)
    ar = []
    for key, value in topN:
        ar.append(f"{key}: {value}")
    write_lines(out_path, ar)
    return topN


# ═════════════════════════════════════════════
# 아래는 채점기입니다. 고치지 마세요.
# ═════════════════════════════════════════════

SAMPLE = """AI is changing how we work.
Machine learning is a part of AI, and deep learning is a part of machine learning.
Data matters more than the model. Data, data, data!
A model is only as good as the data you give it.
Learning AI takes time, but the basics do not change much."""


def _ensure_sample():
    if not os.path.exists("sample.txt"):
        with open("sample.txt", "w", encoding="utf-8") as f:
            f.write(SAMPLE)
        print("  (sample.txt를 새로 만들었습니다)")


def _check(name, got, want):
    if got == want:
        print(f"  ✅ {name}")
        return True
    print(f"  ❌ {name}")
    print(f"       기대한 값: {want!r}")
    print(f"       나온 값  : {got!r}")
    return False


def main():
    print("\n3주차 연습 채점\n" + "─" * 46)
    _ensure_sample()
    results = []
    tmp_in, tmp_out = "_test_in.txt", "_test_out.txt"

    with open(tmp_in, "w", encoding="utf-8") as f:
        f.write("AI is fun. ai is hard! Data data DATA?")

    print("\n[문제 1] 파일 읽기")
    try:
        results.append(_check("read_text(임시파일)", read_text(tmp_in),
                              "AI is fun. ai is hard! Data data DATA?"))
    except Exception as e:
        results.append(_check("read_text", f"에러: {e}", "정상 동작"))

    print("\n[문제 2] 파일 쓰기")
    try:
        write_lines(tmp_out, ["첫째 줄", "둘째 줄"])
        with open(tmp_out, "r", encoding="utf-8") as f:
            results.append(_check("write_lines 결과", f.read(), "첫째 줄\n둘째 줄\n"))
    except Exception as e:
        results.append(_check("write_lines", f"에러: {e}", "정상 동작"))

    print("\n[문제 3] 단어 다듬기")
    results.append(_check('clean_word("Hello,")', clean_word("Hello,"), "hello"))
    results.append(_check('clean_word("AI!")', clean_word("AI!"), "ai"))
    results.append(_check('clean_word("don\'t")', clean_word("don't"), "don't"))
    results.append(_check('clean_word("(data)")', clean_word("(data)"), "data"))

    print("\n[문제 4] 단어 세기")
    results.append(_check(
        'word_frequency("AI is fun. ai is hard!")',
        word_frequency("AI is fun. ai is hard!"),
        {"ai": 2, "is": 2, "fun": 1, "hard": 1}))
    results.append(_check('word_frequency("")', word_frequency(""), {}))

    print("\n[문제 5] 상위 n개")
    results.append(_check("top_n({b:2, a:2, c:5}, 2)",
                          top_n({"b": 2, "a": 2, "c": 5}, 2), [("c", 5), ("a", 2)]))
    results.append(_check("top_n({a:1}, 5)", top_n({"a": 1}, 5), [("a", 1)]))

    print("\n[문제 6] 전부 이어 붙이기")
    try:
        got = save_top_words(tmp_in, tmp_out, 2)
        results.append(_check("save_top_words 반환값", got, [("data", 3), ("ai", 2)]))
        with open(tmp_out, "r", encoding="utf-8") as f:
            results.append(_check("저장된 파일 내용", f.read(), "data: 3\nai: 2\n"))
    except Exception as e:
        results.append(_check("save_top_words", f"에러: {e}", "정상 동작"))

    for p in (tmp_in, tmp_out):
        if os.path.exists(p):
            os.remove(p)

    passed = sum(1 for r in results if r)
    print("\n" + "─" * 46)
    print(f"{passed} / {len(results)} 통과")

    if passed == len(results):
        pairs = save_top_words("sample.txt", "top_words.txt", 10)
        print("\n전부 통과했습니다. sample.txt를 분석해 top_words.txt를 만들었습니다:\n")
        for word, count in pairs:
            print(f"    {word:<10} {'█' * count} {count}")
        print("\n이제 sample.txt를 본인이 좋아하는 글로 바꿔서 다시 돌려보세요.")
        print("  git add . && git commit -m \"3주차 단어 빈도 분석기\" && git push")
    else:
        print("\n❌ 항목의 '기대한 값'과 '나온 값'을 비교해보세요.")
    print()


if __name__ == "__main__":
    main()