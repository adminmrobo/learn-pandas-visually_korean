from lib import *
from snippets import CVS

CARD = dict(
    id="countplot", ch="8. 차트 그리기", cmd="sns.countplot(hue=)",
    title="줄 수를 세어 막대로", excel="COUNTIF 막대",
    desc="countplot 은 y 값 없이 x 값마다 몇 줄인지 세어 막대로 그린다. order 로 요일 순서를 고정하고, "
         "hue 에 True/False 열(주말 여부)을 넣으면 주말만 다른 색이 된다. 예시는 편의점 4주치 결제 기록이다.",
    code=CVS + '''
import matplotlib.pyplot as plt
import seaborn as sns

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
cvs["weekday"] = cvs["time"].dt.day_name().str[:3]
cvs["Weekend"] = cvs["weekday"].isin(["Sat", "Sun"])
ax = sns.countplot(data=cvs, x="weekday", order=days, hue="Weekend", palette=["#028090", "#D98E22"])
ax.set(title="CVS payments by weekday", xlabel="", ylabel="count")
plt.show()''',
)

def stages(ns, out):
    c = ns["cvs"]; days = ns["days"]
    vc = c["weekday"].value_counts().reindex(days).rename("count").reset_index()
    vc["Weekend"] = vc["weekday"].isin(["Sat", "Sun"])
    top = vc.loc[vc["count"].idxmax()]; low = vc.loc[vc["count"].idxmin()]
    return [
        S("결제의 요일", f"{len(c)}줄 가운데 앞 8줄. Weekend 열은 isin 으로 만들었다.",
          T(c[["time", "weekday", "Weekend"]].head(8))),
        S("요일별 세기", "value_counts 와 같은 일을 countplot 이 안에서 한다.", T(vc[["weekday", "count"]], hl=("count",))),
        S("그리기", f"주말(True) 막대만 주황. 가장 많은 날은 {top['weekday']}({top['count']}건), 가장 적은 날은 {low['weekday']}({low['count']}건)이다.",
          CH(type="bar", title="CVS payments by weekday", ylabel="count", cats=days, stack=1,
             series=[dict(name="False", values=[0 if w else int(n) for n, w in zip(vc["count"], vc["Weekend"])], c="#028090"),
                     dict(name="True", values=[int(n) if w else 0 for n, w in zip(vc["count"], vc["Weekend"])], c="#D98E22")])),
    ]
