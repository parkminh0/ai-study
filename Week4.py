"""
4주차 연습 — 클래스와 예외처리

사용법:
    python week4_practice.py

이번 주의 질문 하나: 함수로 다 되는데 클래스는 왜 있을까?
    함수는 부를 때마다 처음부터 시작합니다. 아무것도 기억하지 않아요.
    클래스는 자기 안에 값을 들고 있습니다. 계속 쌓아둘 수 있습니다.

    3주차의 word_frequency는 텍스트를 통째로 한 번에 받아야 했습니다.
    이번 주 WordCounter는 텍스트를 열 번 나눠 넣어도 알아서 누적합니다.
    그 차이가 클래스의 존재 이유입니다.
"""

import os
import requests

# ─────────────────────────────────────────────
# 문제 1. 기억하는 카운터
# ─────────────────────────────────────────────

class WordCounter:
    """텍스트를 넣을 때마다 단어 개수를 누적하는 클래스.

    사용 예:
        wc = WordCounter()
        wc.add("AI is fun")
        wc.add("AI is hard")
        wc.get("ai")   -> 2
        wc.total       -> 6
        wc.top(1)      -> [("ai", 2)]
    """

    def __init__(self):
        """처음 만들어질 때 딱 한 번 실행됩니다. 빈 상태를 준비하세요.

        힌트: self.counts = {} 와 self.total = 0
              self 는 '이 객체 자신'이라는 뜻입니다.
              self를 안 붙이면 함수가 끝날 때 사라집니다.
        """
        self.counts = {}
        self.total = 0
        r = requests.post('https://www.gutenberg.org/cache/epub/11/pg11.txt', data={'key': 'value'})
        self.add(r.text)

    def add(self, text):
        """텍스트를 받아 단어를 세어 누적하세요. (돌려줄 값 없음)

        힌트: 3주차 word_frequency의 for문을 거의 그대로 씁니다.
              단 counts 대신 self.counts에 쌓고, self.total도 같이 늘립니다.
              단어 다듬기: raw.strip(".,!?;:\\"'()[]").lower()
        """
        for v in text.split():
            val = v.strip(".,()!?").lower()
            self.counts[val] = self.counts.get(val, 0) + 1
            self.total += 1

    def get(self, word):
        """그 단어가 몇 번 나왔는지. 한 번도 없으면 0.

        힌트: 딕셔너리의 .get(키, 기본값) 한 줄이면 됩니다.
        """
        return self.counts.get(word, 0)

    def top(self, n):
        """많이 나온 순으로 n개. 3주차 top_n과 같은 규칙(동점이면 사전순).

        힌트: self.counts.items() 로 시작합니다.
        """
        return sorted(list(self.counts.items()), key=lambda x : (-x[1], x[0]))[:n]


# ─────────────────────────────────────────────
# 문제 2. 실험 기록장  ← 4단계에서 진짜로 쓰게 됩니다
# ─────────────────────────────────────────────

class ExperimentLog:
    """모델 성능을 여러 번 기록하고 요약하는 클래스.

    사용 예:
        log = ExperimentLog("결정트리")
        log.record(0.92)
        log.record(0.95)
        log.best()      -> 0.95
        log.average()   -> 0.935
        log.summary()   -> "결정트리: 2회, 최고 95.0%, 평균 93.5%"
    """

    def __init__(self, name):
        """이름을 받아서 저장하고, 빈 점수 목록을 준비하세요.

        힌트: self.name = name / self.scores = []
        """
        self.name = name
        self.scores = []

    def record(self, score):
        """점수 하나를 목록에 추가하세요."""
        self.scores.append(score)

    def best(self):
        """가장 높은 점수. 기록이 없으면 None.

        힌트: 2주차 my_max를 그대로 옮겨오면 됩니다. max()는 쓰지 마세요.
        """
        if len(self.scores) == 0:
            return None
        result = self.scores[0]
        for v in self.scores:
            if v > result:
                result = v
        return result

    def average(self):
        """평균 점수. 기록이 없으면 0. (2주차 my_average 재활용)"""
        if len(self.scores) == 0:
            return 0
        result = 0
        for v in self.scores:
            result += v
        return result / len(self.scores)

    def summary(self):
        """한 줄 요약 문자열. 기록이 없으면 "이름: 기록 없음"

        형식: "결정트리: 2회, 최고 95.0%, 평균 93.5%"

        힌트: f-string에서 f"{0.95:.1%}" 는 '95.0%' 가 됩니다.
              퍼센트 변환과 소수점 자리를 한 번에 해줍니다.
        """
        return f"{self.name}: 기록 없음" if len(self.scores) == 0 else f"{self.name}: {len(self.scores)}회, 최고 {self.best() * 100}%, 평균 {self.average() * 100}%"


# ─────────────────────────────────────────────
# 문제 3. 예외처리 — 터지지 않는 코드
# ─────────────────────────────────────────────

def safe_read(path):
    """파일을 읽어 돌려주되, 파일이 없으면 프로그램을 죽이지 말고 "" 를 돌려주세요.

    왜 필요한가: 남이 쓰는 프로그램은 예상 못 한 입력을 받습니다.
                 터지는 대신 '적당히 넘어가는' 처리를 배웁니다.

    힌트:
        try:
            ...파일 읽기...
        except FileNotFoundError:
            return ""

    except 뒤에 에러 이름을 꼭 적으세요. 그냥 except: 로 다 잡으면
    엉뚱한 버그까지 숨겨버려서 나중에 원인을 못 찾습니다.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def to_number(text):
    """문자열을 실수로 바꿔 돌려주되, 못 바꾸면 None.

    to_number("3.5")  -> 3.5
    to_number("abc")  -> None
    to_number("")     -> None

    힌트: float("abc") 는 ValueError를 냅니다. 그걸 잡으세요.
    """
    try:
        return float(text)
    except ValueError:
        return None


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


def _try(fn, label):
    try:
        return fn(), None
    except Exception as e:
        print(f"  ❌ {label}")
        print(f"       에러: {type(e).__name__}: {e}")
        return None, e


def _val(fn):
    """아직 안 만든 함수 때문에 채점기가 멈추지 않도록 감싸줍니다."""
    try:
        return fn()
    except Exception as e:
        return f"<에러: {type(e).__name__}>"


def main():
    print("\n4주차 연습 채점\n" + "─" * 46)
    results = []

    print("\n[문제 1] WordCounter — 기억하는 클래스")
    wc, err = _try(lambda: WordCounter(), "WordCounter() 생성")
    if err:
        results.append(False)
    else:
        _val(lambda: (wc.add("AI is fun."), wc.add("ai is hard!")))
        results.append(_check('wc.get("ai") (두 번 나옴)', _val(lambda: wc.get("ai")), 2))
        results.append(_check('wc.get("없는단어")', _val(lambda: wc.get("없는단어")), 0))
        results.append(_check("wc.total (전체 단어 수)", _val(lambda: wc.total), 6))
        results.append(_check("wc.top(2)", _val(lambda: wc.top(2)), [("ai", 2), ("is", 2)]))
        wc2 = _val(lambda: WordCounter())
        results.append(_check("새 객체는 비어 있어야 함", _val(lambda: wc2.counts), {}))

    print("\n[문제 2] ExperimentLog — 실험 기록장")
    log, err = _try(lambda: ExperimentLog("결정트리"), "ExperimentLog 생성")
    if err:
        results.append(False)
    else:
        results.append(_check("빈 로그의 best()", _val(lambda: log.best()), None))
        results.append(_check("빈 로그의 average()", _val(lambda: log.average()), 0))
        results.append(_check("빈 로그의 summary()", _val(lambda: log.summary()),
                              "결정트리: 기록 없음"))
        _val(lambda: (log.record(0.92), log.record(0.95)))
        results.append(_check("log.best()", _val(lambda: log.best()), 0.95))
        results.append(_check("log.average()", _val(lambda: log.average()), 0.935))
        results.append(_check("log.summary()", _val(lambda: log.summary()),
                              "결정트리: 2회, 최고 95.0%, 평균 93.5%"))

    print("\n[문제 3] 예외처리")
    with open("_exists.txt", "w", encoding="utf-8") as f:
        f.write("있는 파일")
    results.append(_check('safe_read("_exists.txt")', safe_read("_exists.txt"), "있는 파일"))
    results.append(_check('safe_read("_없는파일.txt")', safe_read("_없는파일.txt"), ""))
    results.append(_check('to_number("3.5")', to_number("3.5"), 3.5))
    results.append(_check('to_number("abc")', to_number("abc"), None))
    results.append(_check('to_number("")', to_number(""), None))
    os.remove("_exists.txt")

    passed = sum(1 for r in results if r)
    print("\n" + "─" * 46)
    print(f"{passed} / {len(results)} 통과")

    if passed == len(results):
        print("""
전부 통과했습니다.

마지막으로 이걸 한번 보세요 — 13주차에 배울 scikit-learn 코드입니다.

    model = DecisionTreeClassifier()   # __init__  : 빈 상태로 만들기
    model.fit(X, y)                    # add 처럼  : 데이터를 넣어 상태를 채우기
    model.predict(new_data)            # get 처럼  : 채워진 상태를 이용해 답하기

오늘 만든 WordCounter와 구조가 똑같습니다.
머신러닝 모델이 '학습한 것을 기억한다'는 게 바로 이 self.counts 자리예요.

  git add . && git commit -m "4주차 클래스와 예외처리" && git push
""")
    else:
        print("\n❌ 항목의 '기대한 값'과 '나온 값'을 비교해보세요.")
        print("클래스에서 값이 사라진다면, self. 를 빠뜨렸는지 먼저 확인하세요.")
    print()


if __name__ == "__main__":
    main()