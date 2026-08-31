"""
그래프 공통 설정 — 한글 폰트와 색을 한곳에 모아둡니다.

matplotlib은 기본 폰트에 한글이 없어서, 그냥 쓰면 제목이 □□□로 나옵니다.
아래 setup_korean_font()가 이 컴퓨터에 있는 한글 폰트를 찾아 설정해줍니다.
"""

import glob
import warnings

import matplotlib.pyplot as plt
from matplotlib import font_manager

# ── 색의 '역할' ────────────────────────────────
# 색은 매번 고르는 게 아니라 역할로 정해두고 씁니다.
# 아래 값들은 색맹 안전성 검사를 통과한 팔레트입니다.

# 순서 없는 항목 구분용 (제품, 팀, 지역...) — 정해진 순서대로 앞에서부터 쓰세요
CATEGORICAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
               "#e87ba4", "#008300", "#4a3aa7", "#e34948"]

# 크기/양을 나타낼 때 — 한 가지 색, 연한 것 → 진한 것
BLUE_RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281"]

PRIMARY = "#2a78d6"     # 시리즈가 하나일 때 쓰는 기본색
INK = "#0b0b0b"         # 제목 글씨
MUTED = "#52514e"       # 축 라벨 등 보조 글씨
GRID = "#e3e2df"        # 격자 — 배경보다 아주 살짝만 진하게


def setup_korean_font(verbose=True):
    """이 컴퓨터에서 쓸 수 있는 한글 폰트를 찾아 설정합니다.

    운영체제마다 들어 있는 한글 폰트가 다릅니다:
        macOS    AppleGothic, Apple SD Gothic Neo
        Windows  Malgun Gothic (맑은 고딕)
        Linux    NanumGothic, Noto Sans CJK
    """
    candidates = [
        "Apple SD Gothic Neo", "AppleGothic",       # macOS
        "Malgun Gothic",                             # Windows
        "NanumGothic", "Nanum Gothic", "NanumBarunGothic",
        "Noto Sans KR", "Noto Sans CJK KR", "Noto Sans CJK JP",
        "Pretendard", "Source Han Sans KR",
    ]

    installed = {f.name for f in font_manager.fontManager.ttflist}
    found = next((name for name in candidates if name in installed), None)

    # 이름으로 못 찾으면, 폰트 파일을 직접 뒤져서 등록해봅니다
    if found is None:
        patterns = [
            "/usr/share/fonts/**/NotoSansCJK*.ttc",
            "/usr/share/fonts/**/NanumGothic*.ttf",
            "/System/Library/Fonts/**/AppleSDGothicNeo*.ttc",
        ]
        for pattern in patterns:
            for path in glob.glob(pattern, recursive=True):
                try:
                    font_manager.fontManager.addfont(path)
                except Exception:
                    continue
        installed = {f.name for f in font_manager.fontManager.ttflist}
        found = next((name for name in candidates if name in installed), None)

    if found:
        plt.rcParams["font.family"] = found
        if verbose:
            print(f"[한글 폰트] {found} 사용")
    elif verbose:
        print("[한글 폰트] 못 찾았습니다. 제목이 □□□로 보이면 그래프 제목을 영어로 쓰세요.")

    # 한글 폰트를 쓰면 음수 기호(−)가 깨지는 경우가 있어서, 일반 하이픈을 쓰게 합니다.
    plt.rcParams["axes.unicode_minus"] = False
    return found


def apply_style(korean=True):
    """모든 그래프에 적용할 기본 스타일. 그래프 그리기 전에 한 번 부르세요."""
    if korean:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            setup_korean_font()

    plt.rcParams.update({
        "figure.figsize": (8, 4.5),
        "figure.dpi": 110,
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlecolor": INK,
        "axes.labelcolor": MUTED,
        "axes.edgecolor": GRID,
        "axes.grid": True,
        "axes.axisbelow": True,     # 격자를 데이터 뒤로 보냅니다
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "grid.linestyle": "-",      # 점선 격자는 쓰지 마세요 — 노이즈가 됩니다
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "lines.linewidth": 2,
        "lines.markersize": 6,
        "legend.frameon": False,
    })


def clean_axes(ax):
    """위·오른쪽 테두리를 지웁니다. 없어도 되는 선은 없는 게 낫습니다."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)