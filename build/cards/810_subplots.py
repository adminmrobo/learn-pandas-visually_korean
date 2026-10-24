from lib import *

CARD = dict(
    id="subplots", ch="8. 차트 그리기", cmd="plt.subplots(1, 2, sharey=True)",
    title="그림 두 칸 나란히", excel="차트 두 개 나란히",
    desc="plt.subplots(1, 2) 는 1행 2열짜리 그림판과 축 두 개(ax[0], ax[1])를 준다. plot 에 ax=ax[0] 을 주면 그 칸에 그린다. "
         "sharey=True 는 두 칸의 y 축 눈금을 같게 맞춘다. 카페와 편의점처럼 성격이 다른 두 가게를 한 막대에 섞지 않고 나란히 볼 때 쓴다.",
    code='''import pandas as pd
import matplotlib.pyplot as plt
# 하루 매출 가운데 시간대별 비율(%)
share = pd.DataFrame({"cafe%": [30.0, 25.0, 33.0, 10.0, 2.0],
                      "cvs%":  [14.0, 21.0, 17.0, 31.0, 17.0]},
                     index=["Morning", "Lunch", "Afternoon", "Evening", "Night"])
fig, ax = plt.subplots(1, 2, figsize=(9, 3.5), sharey=True)
share["cafe%"].plot.bar(ax=ax[0], color="#028090", rot=0, title="Cafe Koi: sales share (%)")
share["cvs%"].plot.bar(ax=ax[1], color="#D98E22", rot=0, title="CVS: sales share (%)")
ax[0].set_xlabel("Time of day")
ax[1].set_xlabel("Time of day")
plt.show()''',
)

def stages(ns, out):
    sh = ns["share"]; cats = list(sh.index); ym = float(sh.values.max()) * 1.15
    return [
        S("두 가게의 비율", f"시간대별 매출 비율. 가장 큰 시간대는 카페 {sh['cafe%'].idxmax()}, 편의점 {sh['cvs%'].idxmax()}.",
          T(sh, index=True, ix_name="time")),
        S("ax[0] · ax[1]", "왼쪽 칸과 오른쪽 칸에 하나씩. 같은 x 위치가 같은 시간대이고, y 눈금도 같다.",
          CH(type="multi", charts=[
              CH(type="bar", title="Cafe Koi: sales share (%)", xlabel="Time of day", cats=cats,
                 series=[dict(name="", values=[float(v) for v in sh["cafe%"]], c="#028090")], ymax=ym)["spec"],
              CH(type="bar", title="CVS: sales share (%)", xlabel="Time of day", cats=cats,
                 series=[dict(name="", values=[float(v) for v in sh["cvs%"]], c="#D98E22")], ymax=ym)["spec"]])),
    ]
