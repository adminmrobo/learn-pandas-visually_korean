from lib import *

CARD = dict(
    id="weighted", ch="6. 묶어서 집계하기", cmd='groupby()[["x", "n"]].sum() → 나누기',
    title="평균 환율과 주문 가중 평균 환율", excel="SUMPRODUCT / SUM",
    desc="날마다 환율이 다르고 주문 금액도 다르면, 환율을 그냥 평균 내는 것(단순 평균)은 주문이 적은 날을 크게 친다. "
         "환율 × 주문 금액(원화로 바꾼 금액)을 먼저 만들고, 통화별로 그 합을 주문 금액 합으로 나누면 주문 가중 평균 환율이 된다. 환율은 연습용 예시값이다.",
    code='''import pandas as pd
d = pd.DataFrame({
    "date": ["01-02", "01-03", "01-06", "01-07", "01-08"] * 2,
    "currency": ["USD"] * 5 + ["JPY"] * 5,
    "rate":   [1466.5, 1470.2, 1460.8, 1452.3, 1455.9, 9.34, 9.37, 9.29, 9.25, 9.27],   # 1단위당 원
    "amount": [120, 30, 40, 400, 60, 5000, 20000, 3000, 1000, 8000],                  # 그날 주문(외화)
})
d["krw"] = d["rate"] * d["amount"]                     # 원화로 바꾼 금액
g = d.groupby("currency")[["krw", "amount"]].sum()
g["weighted"] = (g["krw"] / g["amount"]).round(2)
g["simple"] = d.groupby("currency")["rate"].mean().round(2)
print(g)''',
    talk=[
        dict(who="asst", text="달러 단순 평균은 1461.14인데 가중 평균은 1456.6이에요. 왜요?"),
        dict(who="doc", text="주문이 몰린 1월 7일 환율이 낮았어요. 그날 쪽으로 끌려간 거예요."),
    ],
)

def stages(ns, out):
    d, g = ns["d"], ns["g"]
    u = g.loc["USD"]
    assert (u["simple"], u["weighted"]) == (1461.14, 1456.6), (u["simple"], u["weighted"])
    gc = {"USD": "g0", "JPY": "g1"}
    big = d[d.currency == "USD"]["amount"].idxmax()
    return [
        S("날짜별 환율과 주문", "통화마다 다섯 날. 주문 금액(amount)이 날마다 크게 다르다.",
          T(d[["date", "currency", "rate", "amount"]].astype(object), rcls=["hr" if i == big else gc[c] for i, c in enumerate(d.currency)])),
        S("rate × amount", "줄마다 환율 × 주문 금액 = 그날 주문의 원화 금액.",
          T(d[["currency", "rate", "amount", "krw"]].round(1).astype(object), hl=("krw",), rcls=[gc[c] for c in d.currency])),
        S("그룹 합계", "통화별로 krw 와 amount 를 각각 더한다.",
          T(g[["krw", "amount"]].round(1).astype(object), index=True, ix_name="currency", rcls=[gc[c] for c in g.index])),
        S("나누기", f"합계 ÷ 주문 금액 = 가중 평균. 달러는 단순 {u['simple']} → 가중 {u['weighted']}. 주문이 몰린 날(01-07) 쪽으로 끌린다.",
          T(g[["weighted", "simple"]].astype(object), index=True, ix_name="currency", hl=("weighted",), rcls=[gc[c] for c in g.index])),
    ]
