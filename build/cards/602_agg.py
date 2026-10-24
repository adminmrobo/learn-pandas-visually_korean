from lib import *

CARD = dict(
    id="agg", ch="6. 묶어서 집계하기", cmd='groupby().agg(["count", "mean", "sum"])',
    title="한 번에 여러 계산", excel="피벗 값 필드 여러 개",
    desc="agg 에 함수 이름 목록을 주면 조각마다 여러 계산을 한꺼번에 해서 열로 늘어놓는다. 주문 수(count), 평균(mean), 합계(sum)를 같이 보면 "
         "'평균으로 보면 작아 보이는' 브랜드가 드러난다. 의류 쇼핑몰 브랜드별 주문 금액(천원)으로 본다.",
    code='''import pandas as pd
orders = pd.DataFrame({
    "brand": ["Mono", "Mono", "Mono", "Mono", "Mono", "Denimo", "Denimo", "Linen", "Linen", "Linen"],
    "price_k": [29, 25, 31, 27, 29, 89, 79, 52, 48, 55],     # 주문 금액(천원)
})
s = orders.groupby("brand")["price_k"].agg(["count", "mean", "sum"]).round(1)
print(s)''',
)

def stages(ns, out):
    o, s = ns["orders"], ns["s"]
    g = {b: f"g{i}" for i, b in enumerate(s.index)}
    parts = [T(o[o.brand == b], rcls=[g[b]] * int((o.brand == b).sum())) for b in s.index]
    m = s.loc["Mono"]
    return [
        S("주문 명세", "브랜드마다 주문 수가 다르다. Mono 는 싼 옷이 자주, Denimo 는 비싼 옷이 가끔 팔린다.",
          T(o, rcls=[g[b] for b in o.brand])),
        S("Split", "브랜드별로 나눈다.", *parts),
        S("agg 3종", f"조각마다 개수·평균·합계를 한 줄로 만든다. Mono 는 평균 {m['mean']} 로 가장 작지만 주문이 {int(m['count'])}건이라 합계 {m['sum']}.",
          T(s.astype(object), index=True, ix_name="brand", rcls=[g[b] for b in s.index], hl=("sum",)),
          links=[[i, 0] for i in range(len(s))]),
    ]
