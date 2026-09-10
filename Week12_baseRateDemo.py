"""
P(A|B) 와 P(B|A)는 얼마나 다른가 — 직접 세어보기

사용법:
    python base_rate_demo.py

수식 없이, 사람 10만 명을 실제로 만들어서 손으로 세어봅니다.
"""

BASE_RATE = 0.01       # 인구 100명 중 1명이 실제 환자
SENSITIVITY = 0.99     # 환자를 양성으로 잡아낼 확률 (아주 좋은 검사)
SPECIFICITY = 0.95     # 건강한 사람을 음성으로 판정할 확률
N = 100_000


def main():
    sick = round(N * BASE_RATE)
    healthy = N - sick

    sick_positive = round(sick * SENSITIVITY)          # 진짜 환자인데 양성 (맞게 잡음)
    sick_negative = sick - sick_positive               # 진짜 환자인데 음성 (놓침)
    healthy_negative = round(healthy * SPECIFICITY)    # 건강한데 음성 (맞게 통과)
    healthy_positive = healthy - healthy_negative      # 건강한데 양성 (헛경보)

    total_positive = sick_positive + healthy_positive

    print(f"""
━━ 상황 설정 ━━
  전체 인구            {N:,}명
  실제 유병률          {BASE_RATE:.0%}  →  진짜 환자 {sick:,}명
  검사 민감도          {SENSITIVITY:.0%}  (환자를 양성으로 잡아냄)
  검사 특이도          {SPECIFICITY:.0%}  (건강한 사람을 음성으로 판정)

  꽤 좋은 검사처럼 보입니다.

━━ 실제로 세어보면 ━━

                      양성 판정      음성 판정        합계
  실제 환자      {sick_positive:>10,} {sick_negative:>13,} {sick:>11,}
  건강한 사람    {healthy_positive:>10,} {healthy_negative:>13,} {healthy:>11,}
  합계           {total_positive:>10,} {sick_negative + healthy_negative:>13,} {N:>11,}

━━ 두 방향의 조건부확률 ━━

  P(양성 | 환자)  =  {sick_positive:,} / {sick:,}
                  =  {sick_positive / sick:.1%}
                     "환자라면 검사가 잡아낼 확률"  ← 검사 성능

  P(환자 | 양성)  =  {sick_positive:,} / {total_positive:,}
                  =  {sick_positive / total_positive:.1%}
                     "양성이 나왔을 때 진짜 환자일 확률"  ← 내가 알고 싶은 것

  {sick_positive / sick:.0%} 와 {sick_positive / total_positive:.0%}.
  같은 데이터인데 방향만 바꿨을 뿐입니다.

━━ 왜 이렇게 되나 ━━

  건강한 사람이 {healthy:,}명이나 되기 때문입니다.
  그중 {100-SPECIFICITY*100:.0f}%만 헛경보가 나도 {healthy_positive:,}명입니다.
  진짜 환자 {sick_positive:,}명보다 훨씬 많습니다.

  양성 판정을 받은 {total_positive:,}명 중 대부분이 사실 건강한 사람인 거죠.
  검사가 나빠서가 아니라, 애초에 환자가 드물어서 생기는 일입니다.
  이걸 '기저율(base rate)'이라고 합니다.

━━ 15주차 예고 ━━

  방금 본 두 숫자에는 이름이 있습니다:

    재현율(Recall)     = P(양성 판정 | 실제 환자)  = {sick_positive / sick:.1%}
                        놓치지 않는 능력
    정밀도(Precision)  = P(실제 환자 | 양성 판정)  = {sick_positive / total_positive:.1%}
                        헛다리 짚지 않는 능력

  15주차에 '정확도만 보면 안 되는 이유'를 배우는데, 그 이유가 이겁니다.
  참고로 이 검사의 정확도는 {(sick_positive + healthy_negative) / N:.1%}입니다.
  훌륭해 보이죠. 그런데 "무조건 음성"이라고만 답하는 엉터리 검사도
  정확도가 {healthy / N:.1%}입니다. 정확도는 이런 걸 못 걸러냅니다.

━━ 직접 해보기 ━━

  파일 맨 위 BASE_RATE를 0.30으로 바꿔서 다시 돌려보세요.
  흔한 병이면 P(환자|양성)이 어떻게 변하는지 보시면,
  '기저율이 왜 중요한지'가 몸에 남습니다.
""")


if __name__ == "__main__":
    main()