"""
13주차 연습 — 머신러닝의 시작 (3단계 첫 주)

사용법:
    pip install scikit-learn
    python week13_practice.py

━━ 12주 전으로 돌아갑니다 ━━

첫날 제가 드렸던 first_ml.py, 기억나시나요?
그때는 load_iris가 뭔지도 모르는 상태로 돌리셨습니다.

지금은 다릅니다:
    - X와 y가 뭔지 압니다            (11주차 벡터)
    - 표를 다룰 줄 압니다             (8~9주차 pandas)
    - 정확도라는 숫자를 의심할 줄 압니다 (12주차 조건부확률)
    - 클래스가 상태를 기억한다는 걸 압니다 (4주차 WordCounter)

이번 주는 그 도구들을 모아서, 12주 전 그 코드를 '이해하며' 다시 씁니다.

━━ 4주차의 약속 ━━

4주차에 WordCounter를 만들면서 이런 얘기를 했었습니다:

    wc = WordCounter()      __init__  : 빈 상태로 만들기
    wc.add("AI is fun")     add       : 데이터를 넣어 상태를 채우기
    wc.get("ai")            get       : 채워진 상태로 답하기

    model = DecisionTreeClassifier()   __init__ : 빈 상태로 만들기
    model.fit(X, y)                    fit      : 데이터를 넣어 규칙을 채우기
    model.predict(new_data)            predict  : 채워진 규칙으로 답하기

똑같은 구조입니다. 머신러닝 모델은 특별한 존재가 아니라,
'데이터를 보고 규칙을 기억하는 클래스'일 뿐입니다.

━━ 지도학습 vs 비지도학습 ━━

    지도학습   : 문제(X)와 정답(y)을 같이 주고 규칙을 찾게 함  ← 이번 주
    비지도학습 : 정답 없이 데이터(X)만 주고 패턴을 찾게 함     ← 19주차
"""

from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text


LOADERS = {"iris": load_iris, "wine": load_wine, "cancer": load_breast_cancer}


# ─────────────────────────────────────────────
# 문제 1. 데이터 불러오기
# ─────────────────────────────────────────────

def load_dataset(name):
    """이름을 받아 (X, y, 특성이름목록, 정답이름목록) 을 돌려주세요.

    name은 "iris", "wine", "cancer" 중 하나입니다. LOADERS 딕셔너리를 쓰세요.

    X  — 입력. 각 줄이 표본 하나, 각 칸이 숫자 하나. (2차원)
    y  — 정답. 각 표본이 몇 번 종류인지. (1차원, 0/1/2 같은 숫자)

    힌트:
        data = LOADERS[name]()
        data.data            → X
        data.target          → y
        data.feature_names   → 특성 이름 (list()로 감싸세요)
        data.target_names    → 정답 이름 (list()로 감싸세요)

    돌려줄 것: (X, y, list(feature_names), list(target_names))
    """
    data = LOADERS[name]()
    return (data.data, data.target, data.feature_names, data.target_names)


# ─────────────────────────────────────────────
# 문제 2. 훈련용 / 시험용 나누기
# ─────────────────────────────────────────────

def split_data(X, y, seed=42):
    """데이터를 훈련용 70% / 시험용 30% 로 나눠주세요.

    돌려줄 것: (X_train, X_test, y_train, y_test)  ← 이 순서입니다

    ★ 왜 나누나요?
      모델이 공부한 문제로 시험을 보면 당연히 잘 맞힙니다. 외웠으니까요.
      진짜 실력은 '한 번도 못 본 문제'로만 잴 수 있습니다.
      기출문제로 만점 받았다고 수능 만점이 아닌 것과 같습니다.

    힌트: train_test_split(X, y, test_size=0.3, random_state=seed)
          random_state를 고정해야 돌릴 때마다 같은 결과가 나옵니다.
    """
    return train_test_split(X, y, test_size=0.3, random_state=seed)


# ─────────────────────────────────────────────
# 문제 3. 학습시키기 — fit
# ─────────────────────────────────────────────

def train_tree(X_train, y_train, max_depth=3):
    """결정트리 모델을 만들고 학습시켜서 돌려주세요.

    힌트:
        model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
        model.fit(X_train, y_train)
        return model

    ★ fit이 하는 일:
      데이터를 훑으면서 "어느 특성을 어디서 자르면 가장 깔끔하게 나뉘나"를 찾습니다.
      찾은 규칙은 model 안에 저장됩니다. (WordCounter의 self.counts 자리)

    ★ fit은 model을 '바꿉니다'. 새 model을 돌려주는 게 아닙니다.
      그래서 model.fit(...) 을 부른 뒤 그 model을 그대로 return 하면 됩니다.
      (model = model.fit(...) 이라고 써도 되지만 굳이 필요 없습니다)
    """
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)
    return model


# ─────────────────────────────────────────────
# 문제 4. 채점하기 — predict
# ─────────────────────────────────────────────

def accuracy(model, X, y):
    """모델의 정확도를 돌려주세요. (맞힌 비율, 0~1 사이)

    힌트:
        pred = model.predict(X)
        return accuracy_score(y, pred)

    ★ predict가 하는 일:
      fit 때 찾아둔 규칙에 새 데이터를 넣어서 답을 냅니다.
      규칙을 새로 찾지 않습니다. 이미 찾아둔 걸 쓰기만 합니다.

    ★ 12주차를 떠올리세요:
      정확도는 '전체 중 맞힌 비율'일 뿐입니다.
      환자가 1%인 데이터에서는 "전부 건강"이라고만 답해도 99%가 나옵니다.
      15주차에 이 문제를 제대로 다룹니다.
    """
    pred = model.predict(X)
    return accuracy_score(y, pred)


# ─────────────────────────────────────────────
# 문제 5. 전부 이어 붙이기  ← 6주차 save_top_words처럼
# ─────────────────────────────────────────────

def run_pipeline(name, max_depth=3, seed=42):
    """데이터 이름 하나를 받아, 불러오기부터 채점까지 전부 해서 요약을 돌려주세요.

    돌려줄 딕셔너리:
        {
            "name": "iris",
            "n_samples": 150,      전체 표본 수
            "n_features": 4,       특성(입력 숫자) 개수
            "n_classes": 3,        정답 종류 개수
            "train_acc": 0.9714,   훈련 데이터 정확도 (소수 넷째 자리 반올림)
            "test_acc": 0.9778,    시험 데이터 정확도 (소수 넷째 자리 반올림)
        }

    앞에서 만든 함수 4개를 순서대로 부르기만 하면 됩니다.
    (3주차 save_top_words에서 하셨던 것과 같은 조립입니다)

    ★ 이 함수의 진짜 의미:
      같은 코드가 iris에도, wine에도, cancer에도 그대로 돌아갑니다.
      데이터가 150개짜리든 569개짜리든, 특성이 4개든 30개든 상관없습니다.
      scikit-learn의 모든 모델이 fit/predict라는 같은 문을 갖고 있어서입니다.
      17주차에 모델을 바꿔 끼울 때 이 설계가 얼마나 편한지 보시게 됩니다.
    """
    X, y, feature_names, target_names = load_dataset(name)
    X_train, X_test, y_train, y_test = split_data(X, y)
    model = train_tree(X_train, y_train)
    return {
        "name": name,
        "n_samples": len(X),
        "n_features": len(feature_names),
        "n_classes": len(target_names),
        "train_acc": accuracy(model, X_train, y_train),
        "test_acc": accuracy(model, X_test, y_test), 
    }


# ─────────────────────────────────────────────
# 문제 6. 모델이 찾은 규칙 꺼내 보기
# ─────────────────────────────────────────────

def rules_text(model, feature_names, target_names):
    """학습된 트리가 찾은 규칙을 사람이 읽을 수 있는 글자로 돌려주세요.

    힌트:
        export_text(model, feature_names=list(feature_names),
                    class_names=list(target_names))

    ★ 이게 결정트리의 가장 큰 장점입니다.
      대부분의 모델은 '왜 그렇게 판단했는지' 알 수 없는 블랙박스인데,
      결정트리는 규칙을 그대로 꺼내서 읽을 수 있습니다.
      (이걸 '해석 가능성'이라고 하고, 의료·금융에서 특히 중요합니다)
    """
    return export_text(model, feature_names=list(feature_names),
                    class_names=list(target_names))


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


def main():
    print("\n13주차 연습 채점\n" + "─" * 54)
    results = []

    print("\n[문제 1] 데이터 불러오기")
    got = _val(lambda: load_dataset("iris"))
    ok = isinstance(got, tuple) and len(got) == 4
    results.append(_report(ok, "load_dataset('iris') — 4개짜리 튜플",
                           f"돌려준 것: {got!r}"[:200]))
    if not ok:
        print("\n1번을 먼저 해결해야 나머지를 채점할 수 있습니다.\n")
        return
    X, y, fnames, tnames = got
    results.append(_report(X.shape == (150, 4), f"iris의 X 모양 = (150, 4)", f"나온 값: {X.shape}"))
    results.append(_report(len(y) == 150, "iris의 y 길이 = 150", f"나온 값: {len(y)}"))
    results.append(_report(len(tnames) == 3 and "setosa" in tnames[0],
                           f"정답 이름 3개 (setosa, versicolor, virginica)", f"나온 값: {tnames}"))

    print("\n[문제 2] 나누기")
    sp = _val(lambda: split_data(X, y))
    # train_test_split은 리스트를 돌려주므로 tuple/list 둘 다 받습니다
    ok = isinstance(sp, (tuple, list)) and len(sp) == 4
    results.append(_report(ok, "split_data — 4개짜리 (X_train, X_test, y_train, y_test)",
                           f"돌려준 것: {type(sp).__name__}, 길이 "
                           f"{len(sp) if hasattr(sp, '__len__') else '?'}"))
    if ok:
        Xtr, Xte, ytr, yte = sp
        results.append(_report(len(Xtr) == 105 and len(Xte) == 45,
                               "훈련 105개 / 시험 45개 (70:30)",
                               f"나온 값: 훈련 {len(Xtr)}개 / 시험 {len(Xte)}개\n"
                               "test_size=0.3 을 쓰셨나요?"))
        results.append(_report(len(ytr) == 105 and len(yte) == 45,
                               "y도 같은 비율로 나뉨",
                               f"나온 값: {len(ytr)} / {len(yte)}\n"
                               "돌려주는 순서가 (X_train, X_test, y_train, y_test) 인지 확인하세요"))
    else:
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42)

    print("\n[문제 3~4] fit 과 predict")
    model = _val(lambda: train_tree(Xtr, ytr))
    ok = hasattr(model, "predict") and hasattr(model, "tree_")
    results.append(_report(ok, "train_tree — 학습된 모델을 돌려줌",
                           f"돌려준 것: {model!r}"[:150] +
                           "\nmodel.fit(...) 을 부른 뒤 model 을 return 했는지 확인하세요"))
    if not ok:
        model = DecisionTreeClassifier(max_depth=3, random_state=42).fit(Xtr, ytr)

    ref_test = accuracy_score(yte, model.predict(Xte))
    got_acc = _val(lambda: accuracy(model, Xte, yte))
    results.append(_report(isinstance(got_acc, float) and abs(got_acc - ref_test) < 1e-9,
                           f"accuracy — 시험 정확도 {ref_test:.1%}",
                           f"나온 값: {got_acc}"))

    print("\n[문제 5] 전체 파이프라인")
    for name, exp_samples, exp_features, exp_classes in [
        ("iris", 150, 4, 3), ("wine", 178, 13, 3), ("cancer", 569, 30, 2),
    ]:
        r = _val(lambda n=name: run_pipeline(n))
        if not isinstance(r, dict):
            results.append(_report(False, f"run_pipeline('{name}')", f"딕셔너리가 아닙니다: {r!r}"[:150]))
            continue
        ok = (r.get("n_samples") == exp_samples and r.get("n_features") == exp_features
              and r.get("n_classes") == exp_classes
              and isinstance(r.get("test_acc"), float))
        results.append(_report(
            ok, f"run_pipeline('{name}') — 표본 {exp_samples}, 특성 {exp_features}, 종류 {exp_classes}",
            f"나온 값: {r}"))

    print("\n[문제 6] 규칙 꺼내 보기")
    txt = _val(lambda: rules_text(model, fnames, tnames))
    ok = isinstance(txt, str) and "class:" in txt and "<=" in txt
    results.append(_report(ok, "rules_text — 트리 규칙을 글자로",
                           f"나온 값: {txt!r}"[:200]))

    passed = sum(1 for r in results if r)
    total = len(results)
    print("\n" + "─" * 54)
    print(f"{passed} / {total} 통과")

    if passed == total:
        print("\n같은 코드를 세 데이터에 돌린 결과입니다:\n")
        print(f"  {'데이터':<10} {'표본':>6} {'특성':>5} {'종류':>5} {'훈련':>8} {'시험':>8} {'차이':>8}")
        print("  " + "─" * 54)
        for n in ["iris", "wine", "cancer"]:
            r = run_pipeline(n)
            gap = r["train_acc"] - r["test_acc"]
            print(f"  {r['name']:<10} {r['n_samples']:>6} {r['n_features']:>5} "
                  f"{r['n_classes']:>5} {r['train_acc']:>7.1%} {r['test_acc']:>8.1%} {gap:>+8.1%}")

        print("""
  코드를 한 줄도 안 바꿨습니다. 데이터 이름만 바꿨을 뿐입니다.

이번 주에 확실히 해둘 것 — 완료 기준입니다:

    fit(X, y)      데이터를 보고 '규칙을 찾아서 모델 안에 저장'한다
    predict(X)     저장된 규칙에 새 데이터를 넣어 '답을 낸다'

    fit은 학습, predict는 사용. fit 없이 predict는 못 합니다.

그리고 위 표의 마지막 열(차이)을 눈여겨보세요.

보통은 훈련 정확도가 시험 정확도보다 높습니다. 공부한 문제를 더 잘 푸는 건
당연하니까요. 그런데 iris를 보면 차이가 '음수'입니다 —
못 본 문제를 더 잘 맞혔다는 뜻인데, 이게 어떻게 가능할까요?

    iris의 시험 데이터는 45개뿐입니다.
    어떤 45개가 뽑혔느냐에 따라 점수가 출렁입니다.
    이번 random_state=42 에서는 마침 쉬운 45개가 뽑힌 겁니다.

split_data의 seed를 0, 1, 7 로 바꿔서 직접 돌려보세요.
같은 코드, 같은 데이터인데 점수가 꽤 달라질 겁니다.

여기서 얻을 교훈: **정확도 하나만 보고 판단하면 안 됩니다.**
시험 데이터가 작을수록 그 숫자는 운에 좌우됩니다.
16주차에 이 문제를 제대로 푸는 방법(교차검증)을 배웁니다.

  git add . && git commit -m "13주차 머신러닝 시작" && git push
""")
    else:
        print("\n❌ 항목을 확인하세요.\n")


if __name__ == "__main__":
    main()