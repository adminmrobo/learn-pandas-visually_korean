from lib import *

CARD = dict(
    id="line_annot", ch="8. 차트 그리기", cmd="ax.plot() · ax.annotate()",
    title="선 긋고 화살표 달기", excel="꺾은선형 차트 + 도형",
    desc="plt.subplots 로 그림판(fig)과 축(ax)을 만들고 ax.plot(x, y) 로 선을 긋는다. annotate 는 xy(가리킬 점)와 "
         "xytext(글자 위치)를 받아 화살표를 단다. 편의점 계산대 현금 시재가 가장 적었던 날처럼 꼭 봐야 할 점을 짚어 준다.",
    code='''import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
cash = pd.DataFrame({"date": pd.date_range("2025-03-03", periods=10),
                     "drawer": [312.5, 348.2, 331.0, 286.4, 359.8, 402.1, 388.0, 417.6, 455.3, 440.9]})   # 천원
low = cash.loc[cash["drawer"].idxmin()]
print(low)
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(cash["date"], cash["drawer"], color="#028090")
ax.annotate("low", xy=(low["date"], low["drawer"]), xytext=(low["date"] + pd.Timedelta(days=2), 300),
            arrowprops=dict(arrowstyle="->"))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))   # 날짜 글자를 짧게
ax.set(title="CVS cash in drawer (end of day)", ylabel="KRW thousand")
plt.show()''',
)

def stages(ns, out):
    c = ns["cash"]; i = int(c["drawer"].idxmin()); low = c.loc[i]
    return [
        S("일별 시재", "열흘 동안 문 닫을 때 계산대에 남은 현금이다.", T(c)),
        S("idxmin → low", f"가장 작은 값의 줄을 찾는다. {low['date'].month}월 {low['date'].day}일 {low['drawer']}.",
          T(c, rcls=["hr" if k == i else "" for k in range(len(c))])),
        S("plot + annotate", "선을 긋고 가장 낮은 점에 화살표를 단다.",
          CH(type="line", title="CVS cash in drawer (end of day)", ylabel="KRW thousand",
             xs=[d.strftime("%m-%d") for d in c["date"]], ys=[float(v) for v in c["drawer"]], c="#028090",
             annot=dict(i=i, text="low"))),
    ]
