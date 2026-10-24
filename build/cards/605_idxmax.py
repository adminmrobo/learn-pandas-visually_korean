from lib import *
from snippets import CVS

CARD = dict(
    id="idxmax", ch="6. 묶어서 집계하기", cmd=".max() · .idxmax() · .mean() · .median()",
    title="가장 큰 값과 그 위치, 평균과 중앙값", excel="MAX · INDEX/MATCH · AVERAGE · MEDIAN",
    desc="max() 는 가장 큰 값, idxmax() 는 그 값이 있는 행 이름(예: 몇 시)을 준다. mean 은 평균, median 은 줄 세웠을 때 가운데 값이다. "
         "아주 큰 결제 몇 건이 있으면 평균이 중앙값보다 크게 끌려 올라간다. 동네 편의점 4주치 결제 기록으로 본다.",
    code=CVS + '''
by_hour = cvs.groupby(cvs["time"].dt.hour)["amount"].sum()     # 시간대별 매출(원)
print("max:", by_hour.max(), "/ hour:", by_hour.idxmax())
print("mean:", round(cvs["amount"].mean()), "/ median:", cvs["amount"].median())''',
)

def stages(ns, out):
    bh, cvs = ns["by_hour"], ns["cvs"]
    top = int(bh.idxmax())
    lines = out.splitlines()
    big = cvs.nlargest(3, "amount")[["time", "category", "amount"]].astype(object)
    return [
        S("시간대별 매출", "행 이름이 시(0~23)다. 막대 하나가 4주 동안 그 시간대에 팔린 금액 합계(만원).",
          CH(type="bar", title="Sales by hour (KRW 10k)", xlabel="Hour", cats=[str(h) for h in bh.index],
             series=[{"name": "", "values": [round(v / 10000, 1) for v in bh.values], "c": "#4472C4"}])),
        S("max · idxmax", f"가장 큰 값 {bh.max():,.0f}원과 그 위치 {top}시. 'Q. 가장 바쁜 시간은?' 의 답이다.",
          T((bh.loc[[top]] / 10000).round(1).rename("sales (10k)").to_frame().astype(object), index=True, ix_name="hour", rcls=["hr"]),
          TX(lines[0], "out", "출력")),
        S("mean vs median", f"결제 {len(cvs)}건을 줄 세우면 가운데 값은 {cvs['amount'].median():,.0f}원. 평균은 큰 결제 몇 건에 끌려 {cvs['amount'].mean():,.0f}원.",
          T(big, title="가장 큰 결제 3건"), TX(lines[1], "out", "출력")),
    ]
