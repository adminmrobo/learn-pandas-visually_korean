from lib import *
import pandas as pd
from snippets import CVS

CARD = dict(
    id="histplot", ch="8. 차트 그리기", cmd="sns.histplot() · ax.axvline()",
    title="분포 막대와 기준선", excel="히스토그램 차트",
    desc="히스토그램은 값을 같은 폭의 구간(binwidth)으로 나눠 구간마다 몇 개인지 막대로 세운다. axvline 은 세로 기준선이다. "
         "편의점 결제 금액에 평균선(점선)과 중앙값선(실선)을 같이 그리면 큰 결제 몇 건이 평균을 얼마나 끌었는지 보인다.",
    code=CVS + '''
import matplotlib.pyplot as plt
import seaborn as sns

amt = cvs["amount"] / 1000                          # 천원 단위
print("mean:", round(amt.mean(), 2), " median:", amt.median())
ax = sns.histplot(amt, binwidth=2, binrange=(0, 36), color="#028090")
ax.axvline(amt.mean(), color="#D98E22", ls="--", label=f"mean {amt.mean():.2f}")
ax.axvline(amt.median(), color="#1F2A2E", label=f"median {amt.median():.2f}")
ax.set(title="CVS payment amount", xlabel="Amount (KRW thousand)", ylabel="count")
ax.legend()
plt.show()''',
)

def stages(ns, out):
    import numpy as np
    amt = ns["amt"]
    edges = list(np.arange(0, 38, 2))
    cnt, _ = np.histogram(amt, bins=edges)
    tb = pd.DataFrame({"bin": [f"{a}~{a+2}" for a in edges[:-1]], "count": cnt})
    tb = tb[tb["count"] > 0]
    mean, med = float(amt.mean()), float(amt.median())
    return [
        S(f"결제 {len(amt)}건", f"앞 8건만 보인다. 대부분 몇 천 원이고, 가장 큰 결제는 {amt.max()*1000:,.0f}원이다.",
          T(amt.head(8).rename("amount_k").to_frame())),
        S("2 폭 구간에 담기", "0~2, 2~4 … 구간마다 개수를 센다. 빈 구간은 표에서 뺐다.", T(tb, hl=("count",))),
        S("막대 + 기준선", f"점선(평균 {mean:.2f})이 실선(중앙값 {med:.2f})보다 오른쪽에 있다. 큰 결제 몇 건이 평균을 끌어당긴 것이다.",
          CH(type="hist", title="CVS payment amount", xlabel="Amount (KRW thousand)", ylabel="count",
             edges=[float(e) for e in edges], counts=[int(c) for c in cnt], c="#028090",
             vlines=[dict(x=mean, label=f"mean {mean:.2f}", c="#D98E22", dash=1), dict(x=med, label=f"median {med:.2f}", c="#1F2A2E")])),
    ]
