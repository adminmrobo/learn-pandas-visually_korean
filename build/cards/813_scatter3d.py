from lib import *

CARD = dict(
    id="scatter3d", ch="8. 차트 그리기", cmd='fig.add_subplot(projection="3d")',
    title="3D 산점, 정말 읽히는가", excel="(엑셀 3D 차트)",
    desc="add_subplot(projection=\"3d\") 로 3D 축을 만들고 scatter(x, y, z) 로 점을 찍는다. 요일·고객 유형 같은 글자 축은 "
         "map 으로 숫자 좌표(0, 1, 2…)로 바꿔야 한다. 카페 Koi 매출을 월 × 요일 × 고객 유형 큐브로 그려 보면 공이 서로 가려 "
         "읽기 어렵다. 보고서에는 한 면을 잘라 히트맵으로 쓴다.",
    code='''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng(0)
cube = pd.DataFrame([(m, d, k) for m in range(4, 13) for d in ["Mon", "Wed", "Fri", "Sun"] for k in ["Regular", "Walk-in", "Tourist"]],
                    columns=["month", "weekday", "customer"])
cube["sales"] = rng.integers(20, 650, len(cube))          # 칸마다 매출 합계(천원)
cube["d"] = cube["weekday"].map({"Mon": 0, "Wed": 1, "Fri": 2, "Sun": 3})
cube["k"] = cube["customer"].map({"Regular": 0, "Walk-in": 1, "Tourist": 2})
print(cube.head(4))
fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(projection="3d")
ax.scatter(cube["month"], cube["d"], cube["k"], s=cube["sales"] / 3, c=cube["sales"], cmap="YlGnBu")
ax.set_yticks([0, 1, 2, 3], ["Mon", "Wed", "Fri", "Sun"])        # 숫자 좌표에 글자 눈금을 다시 붙인다
ax.set_zticks([0, 1, 2], ["Regular", "Walk-in", "Tourist"])
ax.set_box_aspect(None, zoom=0.85)                               # 축 이름이 잘리지 않게 조금 작게
ax.set(xlabel="Month", ylabel="Weekday", zlabel="Customer", title="Cafe Koi sales cube in 3D")
plt.show()''',
    talk=[dict(who="robo", state="thinking", text="3D면 더 멋지잖아? 삐빅. …근데 제일 큰 공이 어디지?")],
)

def stages(ns, out):
    c = ns["cube"]; top = c.loc[c["sales"].idxmax()]
    return [
        S("큐브 (세로 목록)", f"월 × 요일 × 고객 유형 칸마다 매출 하나. 모두 {len(c)}칸이다.", T(c[["month", "weekday", "customer", "sales"]].head(6))),
        S("글자 → 좌표", "요일은 d, 고객 유형은 k 로 숫자 좌표가 된다.", T(c[["month", "d", "k", "sales"]].head(6), hl=("d", "k"))),
        S("3D 산점", f"공의 크기·색·위치가 서로 가린다. 가장 큰 칸({top['month']}월 {top['weekday']} {top['customer']}, {top['sales']})을 그림에서 바로 찾기 어렵다.",
          IMG("scatter3d")),
    ]
