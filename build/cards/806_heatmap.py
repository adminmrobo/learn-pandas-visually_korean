from lib import *
from snippets import CVS

CARD = dict(
    id="heatmap", ch="8. 차트 그리기", cmd="sns.heatmap(annot=True)",
    title="피벗 표를 색으로 칠하기", excel="조건부 서식(색조)",
    desc="피벗 표를 그대로 heatmap 에 넘기면 칸 값이 클수록 진한 색으로 칠해진다. annot=True 는 칸 안에 숫자를 적고 "
         "fmt=\".0f\" 는 소수점 없이 적으라는 뜻이다. 편의점 결제를 시간대 × 요일로 세면 언제 바쁜지 한 장에 보인다.",
    code=CVS + '''
import matplotlib.pyplot as plt
import seaborn as sns

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
cvs["weekday"] = cvs["time"].dt.day_name().str[:3]
cvs["band"] = pd.cut(cvs["time"].dt.hour, bins=[0, 6, 10, 14, 18, 22, 24], right=False,
                     labels=["0-5", "6-9", "10-13", "14-17", "18-21", "22-23"])
hm = cvs.pivot_table(index="band", columns="weekday", values="amount", aggfunc="count", observed=False)[days]
print(hm)
ax = sns.heatmap(hm, annot=True, fmt=".0f", cmap="YlGnBu")
ax.set(title="CVS payments: time band x weekday", xlabel="", ylabel="Hour")
plt.show()''',
)

def stages(ns, out):
    hm = ns["hm"]
    r, c = hm.stack().idxmax()
    return [
        S("피벗 표", "시간대 × 요일 결제 건수. 4주치를 셌다.", T(hm, index=True, ix_name="band")),
        S("heatmap", f"값이 클수록 진한 파랑. 가장 진한 칸은 {c} {r}시({int(hm.loc[r, c])}건), 새벽(0-5)은 옅다.",
          CH(type="heatmap", title="CVS payments: time band x weekday", ylabel="Hour",
             rows=[str(x) for x in hm.index], cols=list(hm.columns), z=[[float(v) for v in row] for row in hm.values], dec=0)),
    ]
