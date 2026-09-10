"""
14주차 연습 — 회귀: 숫자를 예측하기

사용법:
    python week14_practice.py

13주차는 '분류'였습니다 — 이 꽃이 어느 품종인가(셋 중 하나).
이번 주는 '회귀'입니다 — 이 집은 얼마인가(연속된 숫자).

━━ 이번 주가 진짜 중요한 이유 ━━

경사하강법(gradient descent)을 직접 만듭니다.
이건 회귀만의 기법이 아닙니다. 딥러닝 전체가 이 방법으로 학습합니다.
22주차 역전파도, GPT를 학습시키는 것도 결국 같은 원리입니다:

    1. 지금 얼마나 틀렸는지 잰다              (손실)
    2. 어느 쪽으로 가야 덜 틀리는지 계산한다   (기울기)
    3. 그 방향으로 조금 움직인다               (학습률만큼)
    4. 1번으로 돌아간다

이번 주에 이걸 손으로 만들어보면, 22주차에 새로 배울 게 거의 없습니다.

━━ 안개 속 하산 비유 ━━

깜깜한 산에서 내려와야 합니다. 전체 지형은 안 보이고,
발밑의 경사만 느낄 수 있습니다.

    발밑이 어느 쪽으로 기울었는지 느낀다     ← 기울기(gradient)
    가장 가파르게 내려가는 쪽으로 한 걸음     ← 학습률(learning rate)만큼
    반복

보폭이 너무 작으면 밤새 못 내려오고,
너무 크면 계곡을 건너뛰어 반대편 산을 올라갑니다.
문제 4에서 직접 확인하게 됩니다.
"""

import numpy as np


# ─────────────────────────────────────────────
# 문제 1. 직선으로 예측하기
# ─────────────────────────────────────────────

def predict_line(X, w, b):
    """직선 y = wx + b 로 예측값을 돌려주세요.

    X는 NumPy 배열입니다. 7주차 브로드캐스팅을 쓰면 한 줄입니다.

    predict_line(np.array([1, 2, 3]), w=2, b=1) -> array([3, 5, 7])

    w(기울기)와 b(절편)가 '모델이 학습하는 것'입니다.
    13주차 결정트리에서는 규칙이 if문이었는데, 여기서는 숫자 두 개입니다.
    """
    return X * w + b


# ─────────────────────────────────────────────
# 문제 2. MSE — 얼마나 틀렸나
# ─────────────────────────────────────────────

def mse(y_true, y_pred):
    """평균제곱오차를 돌려주세요.

    MSE = 평균( (실제값 - 예측값)² )

    mse([1, 2, 3], [1, 2, 3]) -> 0.0      완벽
    mse([1, 2, 3], [2, 3, 4]) -> 1.0      전부 1씩 빗나감

    ★ 12주차 분산과 똑같은 모양입니다. 제곱하는 이유도 같습니다:
      +3만큼 틀린 것과 -3만큼 틀린 것이 상쇄되면 안 되니까요.

      덤으로 제곱은 '크게 틀린 것'에 더 큰 벌을 줍니다.
      1만큼 10번 틀리면 10, 10만큼 1번 틀리면 100.
      큰 실수를 특히 싫어하는 손실함수입니다.

    ★ 이 숫자를 '가장 작게 만드는' w와 b를 찾는 게 학습입니다.
    """
    return np.mean((np.array(y_true) - np.array(y_pred)) ** 2)


# ─────────────────────────────────────────────
# 문제 3. 기울기 — 어느 쪽으로 가야 하나  ★ 핵심
# ─────────────────────────────────────────────

def gradient(X, y, w, b):
    """지금의 w, b에서 MSE가 어느 쪽으로 기울어 있는지 (dw, db)로 돌려주세요.

    공식 (미분해서 나온 결과입니다. 유도는 몰라도 됩니다):

        오차 = 예측값 - 실제값
        dw = (2/n) × Σ(오차 × X)
        db = (2/n) × Σ(오차)

    돌려줄 것: (dw, db) 튜플

    ★ 이 숫자가 뜻하는 것:
      dw가 양수면 "w를 키우면 손실이 커진다" → 그러니 w를 줄여야 합니다.
      dw가 음수면 "w를 키우면 손실이 줄어든다" → 그러니 w를 키워야 합니다.

      그래서 항상 기울기의 '반대' 방향으로 움직입니다:  w = w - 학습률 × dw
      이 마이너스 부호가 '하강(descent)'의 정체입니다.

    힌트:
        n = len(X)
        error = predict_line(X, w, b) - y
        dw = (2/n) * np.sum(error * X)
        db = (2/n) * np.sum(error)
        return float(dw), float(db)
    """
    error = predict_line(X, w, b) - y
    n = len(X)
    dw = (2/n) * np.sum(error * X)
    db = (2/n) * np.sum(error)
    return float(dw), float(db)


# ─────────────────────────────────────────────
# 문제 4. 경사하강법 — 반복해서 내려가기  ★ 핵심
# ─────────────────────────────────────────────

def gradient_descent(X, y, lr=0.01, epochs=1000):
    """w=0, b=0 에서 시작해 epochs번 반복하며 손실을 줄여주세요.

    돌려줄 것: (w, b, history)
        history — 매 반복의 MSE를 담은 리스트 (업데이트 '전' 값을 기록)

    한 번의 반복:
        1. 지금 손실을 history에 기록
        2. 기울기를 구한다
        3. w -= lr * dw
           b -= lr * db

    ★ lr(학습률)이 이번 주 최대 함정입니다:
        너무 작으면  → 안 움직임. 1000번 돌려도 제자리
        적당하면     → 손실이 스르륵 줄어듦
        너무 크면    → 튕겨나가서 발산. 손실이 nan이 됨

      채점기가 세 경우를 다 보여줍니다.

    힌트:
        w, b = 0.0, 0.0
        history = []
        for _ in range(epochs):
            history.append(mse(y, predict_line(X, w, b)))
            dw, db = gradient(X, y, w, b)
            w -= lr * dw
            b -= lr * db
        return w, b, history
    """
    w, b = 0.0, 0.0
    history = []
    for _ in range(epochs):
        history.append(mse(y, predict_line(X, w, b)))
        dw, db = gradient(X, y, w, b)
        w -= lr * dw
        b -= lr * db
    return w, b, history


# ─────────────────────────────────────────────
# 문제 5. R² — 이 모델이 쓸모가 있나
# ─────────────────────────────────────────────

def r_squared(y_true, y_pred):
    """결정계수 R²를 돌려주세요.

    R² = 1 - (내 모델의 오차 합) / (그냥 평균으로 찍었을 때의 오차 합)

        ss_res = Σ(실제 - 예측)²          내 모델이 틀린 정도
        ss_tot = Σ(실제 - 실제평균)²       아무 생각 없이 평균만 답했을 때 틀린 정도
        R² = 1 - ss_res / ss_tot

    ★ 읽는 법:
        R² = 1.0   완벽하게 맞힘
        R² = 0.5   평균으로 찍는 것보다 오차를 절반 줄임
        R² = 0.0   평균으로 찍는 것과 똑같음. 모델이 무의미
        R² < 0     평균으로 찍느니만 못함 (가능합니다!)

    ★ MSE와 R²의 차이 — 완료 기준입니다:
        MSE는 '단위가 있는' 절대적 오차입니다.
             집값 예측 MSE가 1000이면 좋은 건지 나쁜 건지 알 수 없습니다.
             원 단위인지 억 단위인지에 따라 다르니까요.
        R²는 '단위가 없는' 상대적 점수입니다.
             기준선(평균으로 찍기)과 비교하므로 어떤 데이터든 같은 자로 잽니다.

      그래서 모델을 고칠 땐 MSE를 줄이고, 남에게 보고할 땐 R²를 말합니다.

    주의: ss_tot이 0이면 (모든 실제값이 같으면) 0으로 나눕니다. 0.0을 돌려주세요.
    """
     # 입력값을 NumPy 배열로 변환
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # 1. 실제값의 평균을 구합니다.
    y_mean = np.mean(y_true)
    
    # 2. 분자와 분모에 들어갈 오차 제곱합을 구합니다.
    ss_res = np.sum((y_true - y_pred) ** 2)      # 내 모델의 오차 합
    ss_tot = np.sum((y_true - y_mean) ** 2)      # 평균으로 찍었을 때의 오차 합
    
    # 3. 예외 처리: 모든 실제값이 같아서 ss_tot이 0인 경우 0.0을 반환합니다.
    if ss_tot == 0:
        return 0.0
        
    # 4. R² 공식을 적용하여 결과를 돌려줍니다.
    return 1.0 - (ss_res / ss_tot)


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


def _report(ok, name, detail=""):
    print(f"  {'✅' if ok else '❌'} {name}")
    if not ok and detail:
        for line in str(detail).split("\n"):
            print(f"       {line}")
    return bool(ok)


def main():
    print("\n14주차 연습 채점\n" + "─" * 54)
    results = []

    print("\n[문제 1] 직선 예측")
    got = _val(lambda: predict_line(np.array([1, 2, 3]), 2, 1))
    results.append(_report(
        isinstance(got, np.ndarray) and np.allclose(got, [3, 5, 7]),
        "predict_line([1,2,3], w=2, b=1) = [3, 5, 7]", f"나온 값: {got}"))

    print("\n[문제 2] MSE")
    results.append(_report(_close(_val(lambda: mse([1, 2, 3], [1, 2, 3])), 0.0),
                           "mse — 완벽하면 0", f"나온 값: {_val(lambda: mse([1,2,3],[1,2,3]))}"))
    results.append(_report(_close(_val(lambda: mse([1, 2, 3], [2, 3, 4])), 1.0),
                           "mse — 전부 1씩 빗나가면 1.0"))
    results.append(_report(_close(_val(lambda: mse([0, 0], [3, 4])), 12.5),
                           "mse([0,0],[3,4]) = (9+16)/2 = 12.5",
                           f"나온 값: {_val(lambda: mse([0,0],[3,4]))}"))

    print("\n[문제 3] 기울기")
    X = np.array([1.0, 2.0, 3.0])
    y = np.array([2.0, 4.0, 6.0])          # 정답은 w=2, b=0
    g = _val(lambda: gradient(X, y, 0.0, 0.0))
    ok = isinstance(g, tuple) and len(g) == 2
    results.append(_report(ok, "gradient — (dw, db) 튜플", f"나온 값: {g!r}"))
    if ok:
        # w=0,b=0 에서: error = -y, dw = (2/3)*(-2-8-18) = -18.667, db = (2/3)*(-12) = -8
        results.append(_report(_close(g[0], -18.666666, 1e-4) and _close(g[1], -8.0, 1e-4),
                               "gradient(w=0,b=0) = (-18.667, -8.0)",
                               f"나온 값: {g}\n둘 다 음수여야 합니다 — "
                               "w와 b를 '키워야' 손실이 준다는 뜻입니다"))

    print("\n[문제 4] 경사하강법")
    out = _val(lambda: gradient_descent(X, y, lr=0.1, epochs=500))
    ok = isinstance(out, tuple) and len(out) == 3
    results.append(_report(ok, "gradient_descent — (w, b, history)", f"나온 값: {type(out)}"))
    if ok:
        w, b, hist = out
        results.append(_report(_close(w, 2.0, 0.05) and abs(b) < 0.15,
                               f"y=2x 를 학습했나 — w≈2.0, b≈0.0 (나온 값: w={w:.3f}, b={b:.3f})"))
        results.append(_report(len(hist) == 500, f"history 길이 = 500 (나온 값: {len(hist)})"))
        results.append(_report(hist[0] > hist[-1] and hist[-1] < 0.01,
                               f"손실이 줄었나 — 처음 {hist[0]:.2f} → 마지막 {hist[-1]:.6f}"))

    print("\n[문제 5] R²")
    results.append(_report(_close(_val(lambda: r_squared([1, 2, 3], [1, 2, 3])), 1.0),
                           "r_squared — 완벽하면 1.0"))
    mean_pred = [2, 2, 2]
    results.append(_report(_close(_val(lambda: r_squared([1, 2, 3], mean_pred)), 0.0),
                           "r_squared — 평균으로만 찍으면 0.0",
                           f"나온 값: {_val(lambda: r_squared([1,2,3], mean_pred))}"))
    neg = _val(lambda: r_squared([1, 2, 3], [3, 2, 1]))
    results.append(_report(isinstance(neg, (int, float)) and not isinstance(neg, bool) and neg < 0,
                           "r_squared — 평균보다 못하면 음수", f"나온 값: {neg!r}"))
    results.append(_report(_close(_val(lambda: r_squared([5, 5, 5], [1, 2, 3])), 0.0),
                           "r_squared — 실제값이 다 같으면 0.0 (0으로 나누기 방지)"))

    passed = sum(1 for r in results if r)
    total = len(results)
    print("\n" + "─" * 54)
    print(f"{passed} / {total} 통과")

    if passed == total:
        print("\n━━ 학습률을 바꿔보면 ━━\n")
        for lr in [0.0001, 0.1, 0.5]:
            # 발산할 때 나오는 overflow 경고는 예상된 것이라 잠시 숨깁니다
            with np.errstate(over="ignore", invalid="ignore"):
                w, b, hist = gradient_descent(X, y, lr=lr, epochs=500)
            last = hist[-1]
            if not np.isfinite(last):
                verdict = "발산 — 튕겨나갔습니다"
            elif last > 1.0:
                verdict = "너무 느림 — 아직 못 내려왔습니다"
            else:
                verdict = "잘 수렴했습니다"
            shown = f"{last:.6f}" if np.isfinite(last) else "nan"
            print(f"  lr={lr:<8} 최종 손실 {shown:>12}   w={w:>10.3f}   {verdict}")

        print("""
  학습률 하나로 결과가 완전히 달라집니다.
  이게 딥러닝에서 가장 먼저 만지는 값이고, 24주차에 다시 만납니다.

  ※ 여기서 lr=0.5는 발산했지만, 아래 진짜 데이터에서는 lr=0.5가 잘 작동합니다.
    "안전한 학습률"이라는 절대적인 값은 없습니다 — 데이터의 크기(스케일)에 달렸습니다.
    그래서 18주차에 '스케일링'을 배웁니다. 값의 범위를 미리 맞춰두면
    학습률 고르기가 훨씬 쉬워지거든요.

━━ 진짜 데이터로 ━━\n""")

        from sklearn.datasets import load_diabetes
        from sklearn.linear_model import LinearRegression

        d = load_diabetes()
        Xb = d.data[:, 2]          # BMI 한 개만 사용
        yb = d.target

        w2, b2, _ = gradient_descent(Xb, yb, lr=0.5, epochs=20000)
        sk = LinearRegression().fit(Xb.reshape(-1, 1), yb)

        print(f"  당뇨병 데이터 442명, BMI 하나로 1년 뒤 진행도 예측\n")
        print(f"  {'':16} {'기울기(w)':>12} {'절편(b)':>12}")
        print(f"  {'내가 만든 것':16} {w2:>12.3f} {b2:>12.3f}")
        print(f"  {'scikit-learn':16} {sk.coef_[0]:>12.3f} {sk.intercept_:>12.3f}")

        pred = predict_line(Xb, w2, b2)
        print(f"\n  MSE = {mse(yb, pred):.1f}     R² = {r_squared(yb, pred):.3f}")
        print(f"""
  for문 몇 줄로 만든 것이 scikit-learn과 거의 같은 답을 찾았습니다.
  라이브러리가 마법을 부리는 게 아니라, 방금 그 계산을 하고 있었던 겁니다.

  R²가 {r_squared(yb, pred):.2f}라는 건, BMI 하나만으로는
  전체 변동의 {r_squared(yb, pred)*100:.0f}%밖에 설명하지 못한다는 뜻입니다.
  나머지 특성 9개를 다 쓰면 얼마나 오를까요? 직접 해보세요:

      from sklearn.linear_model import LinearRegression
      model = LinearRegression().fit(d.data, d.target)   # 특성 10개 전부
      print(r_squared(d.target, model.predict(d.data)))

  git add . && git commit -m "14주차 회귀와 경사하강법" && git push
""")
    else:
        print("\n❌ 항목을 확인하세요.\n")


if __name__ == "__main__":
    main()