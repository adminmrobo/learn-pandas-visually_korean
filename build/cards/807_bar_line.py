from lib import *
from snippets import CVS

CARD = dict(
    id="bar_line", ch="8. 차트 그리기", cmd="plot.bar() + ax.plot()",
    title="막대 위에 선 겹치기", excel="콤보 차트",
    desc="pandas 의 plot.bar 가 돌려주는 ax 위에 ax.plot 으로 선을 하나 더 그리면 두 그래프가 겹친다. "
         "막대는 0, 1, 2 … 자리에 서므로 선의 x 도 range(9) 로 맞춘다. label 을 주고 ax.legend() 를 부르면 범례가 생긴다. "
         "예시는 편의점 영수증 금액의 첫 자리 비율과 벤포드 법칙의 기대 비율이다.",
    code=CVS + '''
import matplotlib.pyplot as plt

first = cvs["amount"].astype(int).astype(str).str[0].astype(int)       # 금액의 첫 자리
d = np.arange(1, 10)
cmp = pd.DataFrame({"observed%": (first.value_counts(normalize=True).reindex(d, fill_value=0) * 100).round(1),
                    "benford%": (np.log10(1 + 1 / d) * 100).round(1)}, index=d)
print(cmp)
ax = cmp["observed%"].plot.bar(color="#028090", rot=0, label="Observed")
ax.plot(range(9), cmp["benford%"], color="#D98E22", marker="o", label="Benford")
ax.set(title="First digit of CVS receipts", xlabel="First digit", ylabel="%")
ax.legend()
plt.show()''',
)

def stages(ns, out):
    cmp = ns["cmp"]
    return [
        S("비교표", f"영수증 {len(ns['first'])}장의 첫 자리 비율과 벤포드 기대 비율. 1 로 시작하는 금액이 {cmp.loc[1, 'observed%']}% 로 가장 많다.",
          T(cmp, index=True, ix_name="digit")),
        S("막대 + 선", f"관측(막대)과 기대(선)를 겹쳐 본다. 5 는 관측 {cmp.loc[5, 'observed%']}% 로 기대 {cmp.loc[5, 'benford%']}% 보다 높다. 차이는 증거가 아니라 확인할 곳을 고르는 단서다.",
          CH(type="bar", title="First digit of CVS receipts", xlabel="First digit", ylabel="%", cats=[str(i) for i in cmp.index],
             series=[dict(name="Observed", values=[float(v) for v in cmp["observed%"]], c="#028090")],
             overlay=dict(name="Benford", values=[float(v) for v in cmp["benford%"]], c="#D98E22"))),
    ]
