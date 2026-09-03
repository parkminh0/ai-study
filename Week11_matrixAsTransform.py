"""
행렬은 '공간을 변형시키는 것'이다 — 눈으로 보기

사용법:
    python matrix_as_transform.py

3Blue1Brown 영상의 핵심 메시지를 직접 그려봅니다.
완료 기준이 "행렬곱이 하는 일을 그림으로 설명할 수 있다"인데,
이 그림이 그 설명입니다.

핵심: 행렬은 숫자 표가 아니라 '공간을 어떻게 바꿀지 적어둔 지시서'입니다.
      A @ v 는 "v라는 점을 A가 시키는 대로 옮겨라"라는 뜻입니다.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from viz_style import apply_style, PRIMARY, CATEGORICAL

apply_style()
ORIGINAL = "#b9b7b2"     # 변형 전 — 회색으로 물러나게
TRANSFORMED = PRIMARY    # 변형 후 — 눈에 띄게

# 정사각형 하나와 격자를 준비합니다
SQUARE = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]).T   # 2×5

TRANSFORMS = [
    ("원래 공간\n(아무것도 안 함)", np.array([[1, 0], [0, 1]])),
    ("가로로 2배 늘리기", np.array([[2, 0], [0, 1]])),
    ("90도 회전", np.array([[0, -1], [1, 0]])),
    ("비스듬히 밀기(전단)", np.array([[1, 1], [0, 1]])),
    ("납작하게 뭉개기\n(행렬식 = 0)", np.array([[1, 1], [1, 1]])),
    ("뒤집으면서 늘리기", np.array([[1.5, 0], [0, -1]])),
]


def grid_lines(n=5):
    """격자선들을 (2, N) 점 묶음 리스트로 만듭니다."""
    lines = []
    for i in range(-n, n + 1):
        lines.append(np.array([[i, i], [-n, n]]))       # 세로선
        lines.append(np.array([[-n, n], [i, i]]))       # 가로선
    return lines


def draw_panel(ax, M, title):
    # 변형된 격자
    for line in grid_lines(4):
        moved = M @ line
        ax.plot(moved[0], moved[1], color=GRID_C, linewidth=0.7, zorder=1)

    # 원래 정사각형 (회색, 참고용)
    ax.fill(SQUARE[0], SQUARE[1], color=ORIGINAL, alpha=0.35, zorder=2)
    ax.plot(SQUARE[0], SQUARE[1], color=ORIGINAL, linewidth=1.5, zorder=2)

    # 변형된 정사각형
    moved_sq = M @ SQUARE
    ax.fill(moved_sq[0], moved_sq[1], color=TRANSFORMED, alpha=0.30, zorder=3)
    ax.plot(moved_sq[0], moved_sq[1], color=TRANSFORMED, linewidth=2, zorder=3)

    # 기저벡터 — 이 두 화살표가 어디로 가는지가 행렬의 전부입니다
    i_hat, j_hat = M @ np.array([1, 0]), M @ np.array([0, 1])
    ax.annotate("", xy=i_hat, xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=CATEGORICAL[1], linewidth=2.5))
    ax.annotate("", xy=j_hat, xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=CATEGORICAL[2], linewidth=2.5))

    det = np.linalg.det(M)
    ax.set_title(f"{title}\n{M.tolist()}   넓이 배율 = {det:.1f}", fontsize=10)
    ax.set_xlim(-1.8, 2.6)
    ax.set_ylim(-1.6, 2.2)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)


GRID_C = "#e3e2df"

fig, axes = plt.subplots(2, 3, figsize=(13, 8.5))
for ax, (title, M) in zip(axes.flat, TRANSFORMS):
    draw_panel(ax, M, title)

fig.suptitle("행렬 = 공간을 변형시키는 지시서", fontsize=15, fontweight="bold")
fig.text(0.5, 0.945,
         "회색 = 원래 정사각형   |   파란색 = 변형된 결과   |   "
         "주황 화살표 = (1,0)이 간 곳,  초록 화살표 = (0,1)이 간 곳",
         ha="center", fontsize=9.5, color="#52514e")
fig.tight_layout(rect=[0, 0.02, 1, 0.93])
fig.savefig("matrix_transform.png", bbox_inches="tight", dpi=110)
print("matrix_transform.png 저장 완료 — 열어보세요.\n")

print("""그림에서 확인할 것 세 가지

1. 행렬의 '열'이 화살표가 도착한 자리입니다.
   [[2, 0],        1열 = (2,0)  →  주황 화살표가 간 곳
    [0, 1]]        2열 = (0,1)  →  초록 화살표가 간 곳

   행렬을 외울 필요가 없습니다. "이 두 화살표를 어디로 보낼까"만 정하면
   그게 곧 행렬입니다.

2. 격자가 어떻게 되든 '평행'과 '균등 간격'은 유지됩니다.
   이게 '선형'변환의 정의입니다. 휘어지거나 구부러지지 않습니다.

3. 마지막 전 그림(납작하게 뭉개기)에서 넓이 배율이 0입니다.
   2차원이 1차원 선으로 찌부러진 겁니다. 이걸 '행렬식이 0'이라고 하고,
   한번 뭉개지면 원래대로 되돌릴 수 없습니다.
   (역행렬이 없다는 말이 이 뜻입니다)

━━ 이게 왜 AI와 관련 있나 ━━

23주차에 만들 신경망의 한 층이 정확히 이 연산입니다:

    출력 = 활성화함수( 가중치행렬 @ 입력 + 편향 )
                       └────────────────┘
                       오늘 본 '공간 변형'

신경망이 '학습한다'는 건, 데이터를 잘 구분할 수 있는 모양으로
공간을 변형시키는 행렬을 찾아간다는 뜻입니다.
층을 여러 개 쌓는 건 변형을 여러 번 연달아 하는 것이고요.

지금 이 그림을 확실히 잡아두면 23주차가 훨씬 수월합니다.
""")