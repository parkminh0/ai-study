"""
경사하강법이 내려가는 걸 눈으로 보기

사용법:
    python Week14.py     (먼저 전부 통과시키세요)
    python gradient_descent_viz.py

Week14.py 에서 만든 함수들을 그대로 가져다 씁니다.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_diabetes

from viz_style import apply_style, clean_axes, PRIMARY, CATEGORICAL
from Week14 import predict_line, mse, gradient_descent, r_squared

apply_style()

d = load_diabetes()
X = d.data[:, 2]     # BMI
y = d.target

w, b, history = gradient_descent(X, y, lr=0.5, epochs=20000)
pred = predict_line(X, w, b)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))

# ── 1. 손실 곡선 ────────────────────────────
ax = axes[0]
ax.plot(history, color=PRIMARY)
ax.set_title("① 손실이 줄어드는 과정")
ax.set_xlabel("반복 횟수")
ax.set_ylabel("MSE (평균제곱오차)")
ax.set_yscale("log")     # 처음에 급격히 줄어서 로그 눈금이 잘 보입니다
clean_axes(ax)
ax.annotate(f"최종 {history[-1]:.0f}", xy=(len(history) - 1, history[-1]),
            xytext=(-70, 20), textcoords="offset points", fontsize=9,
            color=PRIMARY, arrowprops=dict(arrowstyle="->", color=PRIMARY))

# ── 2. 찾아낸 직선 ──────────────────────────
ax = axes[1]
ax.scatter(X, y, color=PRIMARY, alpha=0.35, s=22,
           edgecolors="white", linewidths=0.8, label="실제 데이터")
xs = np.linspace(X.min(), X.max(), 100)
ax.plot(xs, predict_line(xs, w, b), color=CATEGORICAL[1], linewidth=2.5,
        label=f"학습한 직선 (w={w:.0f}, b={b:.0f})")
ax.set_title("② 데이터와 학습한 직선")
ax.set_xlabel("BMI (표준화된 값)")
ax.set_ylabel("1년 뒤 당뇨 진행도")
ax.legend()
clean_axes(ax)

# ── 3. 예측 vs 실제 ─────────────────────────
ax = axes[2]
ax.scatter(y, pred, color=PRIMARY, alpha=0.4, s=22,
           edgecolors="white", linewidths=0.8)
lims = [min(y.min(), pred.min()), max(y.max(), pred.max())]
ax.plot(lims, lims, color="#8a948f", linewidth=1.5, linestyle="-",
        label="완벽한 예측선")
ax.set_title(f"③ 예측 vs 실제  (R² = {r_squared(y, pred):.3f})")
ax.set_xlabel("실제값")
ax.set_ylabel("예측값")
ax.legend()
clean_axes(ax)

fig.tight_layout()
fig.savefig("gradient_descent.png", bbox_inches="tight", dpi=110)
print("gradient_descent.png 저장 완료\n")

print(f"""세 그림에서 읽을 것

① 손실 곡선
   처음엔 급격히, 나중엔 천천히 줄어듭니다.
   산에서 내려올 때 처음엔 경사가 가파르고 바닥 근처는 평평한 것과 같습니다.
   이 곡선이 평평해지면 "더 돌려도 소용없다"는 신호입니다.

   ★ 이 곡선을 매번 그려보는 습관을 들이세요.
     24주차 신경망 학습에서도 제일 먼저 보는 게 이 그림입니다.
     안 줄어들면 학습률이 잘못됐거나 코드에 버그가 있는 겁니다.

② 학습한 직선
   점들 한가운데를 지나갑니다. 이게 '최적'의 뜻입니다 —
   모든 점을 지나는 게 아니라, 전체 오차가 가장 작은 직선입니다.

③ 예측 vs 실제
   회귀 모델을 볼 때 가장 유용한 그림입니다.
   점들이 대각선에 가까울수록 좋은 모델입니다.

   지금은 꽤 흩어져 있죠. R² = {r_squared(y, pred):.2f} 이니
   BMI 하나로는 {r_squared(y, pred)*100:.0f}%밖에 설명 못 한다는 뜻입니다.
   당연합니다 — 당뇨 진행도가 BMI 하나로 정해질 리가 없으니까요.

   그리고 이 그림에는 또 하나가 숨어 있습니다. 실제값 구간별로 잔차(실제-예측)를
   나눠서 재보면:""")

resid = y - pred
qs = np.quantile(y, [0, 0.25, 0.5, 0.75, 1.0])
print()
for i in range(4):
    m = (y >= qs[i]) & (y <= qs[i + 1])
    print(f"     실제 {qs[i]:>5.0f}~{qs[i+1]:>5.0f}   평균 잔차 {resid[m].mean():>+7.1f}"
          f"   {'과대예측' if resid[m].mean() < 0 else '과소예측'}")

print("""
   낮은 값은 높게, 높은 값은 낮게 예측합니다. 전체적으로 '평균 쪽으로 끌어당기는' 셈이죠.
   예측력이 약한 모델에서 흔히 나타나는 현상입니다.

   중요한 건 이겁니다: R² 라는 숫자 하나로는 이 패턴을 절대 못 봅니다.
   그림을 그려야 보입니다. 그래서 모델을 만들면 항상 이 그림을 그려보세요.
   17주차에 배울 트리 계열 모델이 이런 패턴을 더 잘 잡습니다.
""")