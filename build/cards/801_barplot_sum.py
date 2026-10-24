from lib import *
from snippets import KOI

CARD = dict(
    id="barplot_sum", ch="8. 차트 그리기", cmd='sns.barplot(estimator="sum", hue=)',
    title="막대: 평균이 아니라 합계로", excel="세로 막대형 차트",
    desc="seaborn barplot 에 장부 한 줄 한 줄을 그대로 넘기면, 막대 높이는 기본값으로 '평균'이 된다. "
         "카페 Koi 의 월별 매출·비용처럼 '얼마나 쌓였나'를 보려면 estimator=\"sum\" 을 꼭 넣는다. "
         "hue 는 색으로 나눌 열, errorbar=None 은 오차 막대를 끈다.",
    code=KOI + '''
import matplotlib.pyplot as plt
import seaborn as sns

book["Type"] = book["item"].map({"Coffee": "Sales", "Dessert": "Sales", "Milk": "Cost", "Rent": "Cost", "Broken cup": "Cost"})
book["K"] = book["cost"] + book["sales"]            # 금액(천원)
fig, ax = plt.subplots(1, 2, figsize=(9, 3.2), sharey=True)
sns.barplot(data=book, x="month", y="K", hue="Type", errorbar=None, palette=["#028090", "#D98E22"], ax=ax[0])
ax[0].set(title="Default = mean", xlabel="Month", ylabel="KRW thousand")
sns.barplot(data=book, x="month", y="K", hue="Type", estimator="sum", errorbar=None, palette=["#028090", "#D98E22"], ax=ax[1])
ax[1].set(title='estimator="sum"', xlabel="Month")
sns.move_legend(ax[1], "upper left", bbox_to_anchor=(1, 1))   # 범례를 그림 밖 오른쪽 위로
plt.show()''',
    talk=[
        dict(who="asst", text="막대가 평균이라고요? 한 달 매출은 합계 아니에요?"),
        dict(who="doc", text="맞아요. 그래서 estimator=\"sum\" 을 꼭 넣어요."),
    ],
)

def stages(ns, out):
    b = ns["book"]
    g = {"Sales": "g0", "Cost": "g1"}
    parts = []
    for (m, t), d in b.groupby(["month", "Type"], sort=False):
        parts.append(T(d[["month", "Type", "K"]], rcls=[g[t]] * len(d)))
    agg = b.groupby(["month", "Type"], sort=False)["K"].agg(["mean", "sum"]).reset_index()
    agg["mean"] = agg["mean"].round(1); agg["sum"] = agg["sum"].round(1)
    s4 = agg[(agg.month == 4) & (agg.Type == "Sales")].iloc[0]
    def ser(col):
        v = {(r.month, r.Type): r[col] for _, r in agg.iterrows()}
        return [dict(name=t, values=[v.get((m, t), 0) for m in (4, 5)], c=c) for t, c in [("Sales", "#028090"), ("Cost", "#D98E22")]]
    ymax = float(agg["sum"].max()) * 1.08
    return [
        S("장부 한 줄씩", "x=month, hue=Type, y=K. 색은 Type(Sales/Cost)이다.",
          T(b[["month", "item", "Type", "K"]], rcls=[g[t] for t in b.Type])),
        S("(month, Type) 로 나누기", f"막대 하나 = 조각 하나. 4월 Sales 조각에는 장부 {int((b.month.eq(4) & b.Type.eq('Sales')).sum())}줄이 들어 있다.", *parts),
        S("mean 과 sum", f"조각마다 두 가지로 계산해 본다. 4월 Sales: 평균 {s4['mean']}, 합계 {s4['sum']}. barplot 기본값은 mean 이다.",
          T(agg, hl=("sum",))),
        S("막대 그리기", "같은 데이터인데 평균 막대는 '쌓인 돈'을 보여 주지 못한다. 매출과 비용은 합계로 그린다.",
          CH(type="bar", title="Default = mean", xlabel="Month", ylabel="KRW thousand", cats=["4", "5"], series=ser("mean"), ymax=ymax),
          CH(type="bar", title='estimator="sum"', xlabel="Month", ylabel="KRW thousand", cats=["4", "5"], series=ser("sum"), ymax=ymax)),
    ]
