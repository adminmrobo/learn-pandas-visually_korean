from lib import *
import re
from snippets import SHOP

def vis(df):
    """끝 공백을 눈에 보이게 ␣ 로 바꾼 사본"""
    d = df.copy()
    for c in d.columns:
        if d[c].dtype == object:
            d[c] = d[c].map(lambda v: re.sub(r" +$", lambda m: "␣" * len(m.group()), v) if isinstance(v, str) else v)
    return d

CARD = dict(
    id="merge", ch="5. 합치고 모양 바꾸기", cmd='merge(on=, how="left")',
    title="두 표를 열 기준으로 붙이기", excel="VLOOKUP 으로 열 여러 개 가져오기",
    desc='merge 는 두 표에서 같은 키(on) 값을 가진 줄끼리 옆으로 붙인다. how="left" 는 왼쪽 표의 줄을 하나도 버리지 않고, 짝이 없으면 NaN 을 채운다. '
         "쇼핑몰 주문표에 브랜드 표(공급처, 배송일)를 붙여 본다. 붙인 뒤에는 isna() 로 못 찾은 줄을 꼭 센다.",
    code=SHOP + '''
brands = pd.DataFrame({
    "brand": ["Mono", "Linen", "Denimo"],
    "supplier": ["Seoul Knit", "Busan Linen", "Daegu Denim"],
    "ship_days": [2, 4, 3],
})
out = orders.merge(brands, on="brand", how="left")
print(out[["order_id", "brand", "supplier", "ship_days"]])
print("not found:", out["supplier"].isna().sum())

# 범인은 "Linen " 끝의 공백. 지우고 다시 붙인다
orders["brand"] = orders["brand"].str.strip()
out = orders.merge(brands, on="brand", how="left")
print("not found after strip:", out["supplier"].isna().sum())''',
    tip='orders = pd.read_csv("orders.csv") 와 brands = pd.read_excel("brands.xlsx") 처럼 두 파일을 읽은 뒤 같은 방식으로 붙인다. 붙이기 전에 키 열에 .str.strip() 을 먼저 하는 습관을 들인다.',
    talk=[
        dict(who="asst", text="브랜드 표를 붙였는데 Linen 주문만 비었어요. 왜요?"),
        dict(who="doc", text="이름 끝에 공백이 숨어 있어요. 지우고 다시 붙여 볼까요?"),
    ],
)

def stages(ns, out):
    orders, brands = ns["orders"], ns["brands"]
    # 공백이 있던 처음 상태를 다시 만든다
    first = orders[["order_id", "brand"]].copy()
    first["brand"] = first["brand"].replace({"Linen": "Linen "})
    m1 = first.merge(brands, on="brand", how="left")
    miss = m1["supplier"].isna()
    g = {"Mono": "g0", "Linen": "g1", "Linen ": "g4", "Denimo": "g2"}
    lines = out.splitlines()
    nf = [l for l in lines if l.startswith("not found:")][0]
    nf2 = [l for l in lines if l.startswith("not found after")][0]
    m2 = orders[["order_id", "brand"]].merge(brands, on="brand", how="left")
    return [
        S("두 표", '왼쪽은 주문표(orders), 오른쪽은 브랜드 표(brands). 키는 brand. 주문표의 Linen 뒤에는 공백(␣)이 붙어 있다.',
          T(vis(first), rcls=[g[b] for b in first["brand"]]), T(brands, title="brands", rcls=[g[b] for b in brands["brand"]])),
        S("키로 짝짓기", f'같은 brand 끼리 짝을 찾는다. "Linen␣" 과 "Linen" 은 다른 글자라 짝이 없어 NaN. {nf}',
          T(vis(m1).astype(object), rcls=["bad" if x else "ok" for x in miss], hl=("supplier", "ship_days")),
          TX(nf, "out", "출력"), links=[[0, 0], [1, 0]]),
        S("strip 후 다시", f'.str.strip() 으로 끝 공백을 지우고 다시 붙이면 모든 줄이 짝을 찾는다. {nf2}',
          T(m2, rcls=["ok"] * len(m2), hl=("supplier", "ship_days")), TX(nf2, "out", "출력")),
    ]
