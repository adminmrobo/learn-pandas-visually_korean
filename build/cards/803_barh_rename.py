from lib import *

CARD = dict(
    id="barh_rename", ch="8. 차트 그리기", cmd="rename(index=영어사전).plot.barh()",
    title="한글 라벨을 영어로 바꿔 가로 막대", excel="가로 막대형 차트",
    desc="Colab 기본 글꼴에는 한글이 없어 한글 라벨이 네모(□)로 나온다. 숫자는 그대로 두고 rename(index=사전) 으로 "
         "라벨만 영어로 바꾸면 글꼴 설치 없이 해결된다. 항목이 많고 이름이 길면 가로 막대(barh)가 읽기 쉽다. "
         "예시는 동네 편의점의 4주 상품군별 매출이다.",
    code='''import pandas as pd
import matplotlib.pyplot as plt
by_cat = pd.Series({"라면": 301.2, "아이스크림": 370.5, "음료": 729.6, "도시락": 819.8, "과자": 1034.9})   # 천원
eng = {"과자": "Snack", "도시락": "Lunchbox", "음료": "Drink", "아이스크림": "Ice cream", "라면": "Ramen"}
ax = by_cat.rename(index=eng).plot.barh(color="#028090")
ax.bar_label(ax.containers[0], fmt="%.1f")
ax.margins(x=0.15)                          # 숫자 자리 확보
ax.set(title="CVS sales by category (4 weeks)", xlabel="KRW thousand", ylabel="")
plt.show()''',
    talk=[dict(who="fly", text="한글 라벨 그대로 그리면 네모만 남지 않아?")],
)

def stages(ns, out):
    s = ns["by_cat"]; e = s.rename(index=ns["eng"])
    big = e.idxmax()
    return [
        S("한글 index", "행 이름이 한글이다. 이대로 그리면 Colab 에서 □□□ 가 된다.", T(s.rename("K"), index=True, ix_name="상품군")),
        S("rename(index=eng)", "사전으로 행 이름만 바꾼다. 값과 순서는 그대로다.", T(e.rename("K"), index=True, ix_name="category", hl=("K",))),
        S("plot.barh()", f"가로 막대. 아래에서 위로 index 순서대로 쌓인다. 가장 긴 막대는 {big}({e.max()})이다.",
          CH(type="barh", title="CVS sales by category (4 weeks)", xlabel="KRW thousand", cats=list(e.index),
             series=[dict(name="", values=[float(v) for v in e], c="#028090")], labels=1)),
    ]
