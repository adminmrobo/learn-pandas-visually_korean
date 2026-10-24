from lib import *

CODE_MODEL = '''import numpy as np
import matplotlib.pyplot as plt
# 카페 Koi 한 달 가정: 값을 올리면 잔 수가 줄어든다
A = {"cups_at_4500": 3000, "drop_per_100": 60, "milk_etc": 600, "fixed": 8_000_000}
cups = lambda P: A["cups_at_4500"] - A["drop_per_100"] * (P - 4500) / 100
profit = lambda P, C: (cups(P) * (P - C - A["milk_etc"]) - A["fixed"]) / 1_000_000   # 백만원
P, C = np.meshgrid(np.linspace(3000, 6000, 13), np.linspace(300, 1500, 13))         # 판매가 × 원두 단가(원/잔)
Z = profit(P, C)'''

CARD = dict(
    id="contour", ch="8. 차트 그리기", cmd="ax.contourf() · ax.contour(levels=[0])",
    title="등고선으로 손익 0 선 찾기", excel="데이터 표 + 조건부 서식",
    desc="meshgrid 로 계산한 격자를 contourf 에 넘기면 값 높이별로 색을 칠한다(등고선 지도). contour(levels=[0]) 은 값이 정확히 "
         "0 인 곳만 선으로 긋는다 — 이익 0, 즉 손익분기선이다. 카페 Koi 의 커피 판매가와 원두 단가를 바꿔 가며 한 달 이익을 본다. "
         "colorbar 는 색이 뜻하는 값을 옆에 보여 준다.",
    code=CODE_MODEL + '''
for p in [3500, 4500, 5500]:                       # 손익 0 이 되는 원두 단가
    print(f"price {p}: break-even bean cost {p - A['milk_etc'] - A['fixed'] / cups(p):.0f}")
fig, ax = plt.subplots(figsize=(6.5, 4.5))
cf = ax.contourf(P, C, Z, levels=12, cmap="RdYlGn")
ax.contour(P, C, Z, levels=[0], colors="black", linewidths=2)
fig.colorbar(cf, label="Monthly profit (KRW million)")
ax.set(title="Cafe Koi: price x bean cost -> profit", xlabel="Coffee price (KRW)", ylabel="Bean cost per cup (KRW)")
plt.show()''',
    talk=[dict(who="asst", text="검은 선 아래쪽이 이익, 위쪽이 손해인 거죠?")],
)

def stages(ns, out):
    import pandas as pd
    P, C, Z = ns["P"], ns["C"], ns["Z"]
    sub = pd.DataFrame(Z[::-3, ::3].round(1), index=[f"{v:.0f}" for v in C[::-3, 0]], columns=[f"{v:.0f}" for v in P[0, ::3]])
    be = {p: round(p - ns["A"]["milk_etc"] - ns["A"]["fixed"] / ns["cups"](p)) for p in (3500, 4500, 5500)}
    return [
        S("격자 Z", f"13 × 13 = {Z.size}개 시나리오. 일부만 보면 이렇다(원두 단가↓ 행, 판매가→ 열, 백만원).",
          T(sub, index=True, ix_name="C \\ P")),
        S("contourf + contour", "색은 이익 크기, 검은 경계는 이익 0. 경계 위(비싼 원두)가 적자다.",
          CH(type="heatmap", title="Cafe Koi: price x bean cost -> profit", xlabel="Coffee price (KRW)", ylabel="Bean cost per cup (KRW)",
             rows=[f"{v:.0f}" for v in C[::-1, 0]], cols=[f"{v:.0f}" for v in P[0]], z=[[round(float(v), 2) for v in row] for row in Z[::-1]],
             cmap="rdylgn", dec=-1, zero=1)),
        S("Colab 결과", f"실제 matplotlib 등고선. 판매가 3500·4500·5500 원에서 버틸 수 있는 원두 단가는 {be[3500]} → {be[4500]} → {be[5500]} 원이다.",
          IMG("contour")),
    ]
