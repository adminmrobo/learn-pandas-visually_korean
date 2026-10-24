from lib import *
from snippets import SHOP

CARD = dict(
    id="dict_zip", ch="4. 새 열 만들기", cmd="dict(zip(a, b)) → map",
    title="다른 표에서 사전 만들기", excel="VLOOKUP(다른 시트)",
    desc="브랜드 표의 두 열을 zip 으로 짝지어 dict 로 만들면 '브랜드 → 배송 창고' 사전이 된다. 이 사전으로 쇼핑몰 주문에 창고를 붙인다. "
         "엑셀에서 다른 시트를 VLOOKUP 하는 것과 같다.",
    code=SHOP + '''
orders["brand"] = orders["brand"].str.strip()        # 'Linen ' 끝 공백부터 지운다
brands = pd.DataFrame({"brand": ["Mono", "Linen", "Denimo"], "warehouse": ["Seoul", "Busan", "Incheon"]})
where = dict(zip(brands["brand"], brands["warehouse"]))   # {'Mono': 'Seoul', ...}
print(where)
orders["warehouse"] = orders["brand"].map(where)
print(orders[["order_id", "brand", "warehouse"]])''',
)

def stages(ns, out):
    br, o, w = ns["brands"], ns["orders"], ns["where"]
    return [
        S("두 표", "위: 브랜드 표(brand, warehouse). 아래: 주문 명세.", T(br, title="brands"), T(o[["order_id", "brand"]], title="orders")),
        S("dict(zip())", "브랜드 표의 두 열을 한 줄씩 짝지어 사전을 만든다.", TX(str(w), "out", "where"), T(o[["order_id", "brand"]]),
          links=[[0, 0], [1, 1]]),
        S("map(where)", "주문의 브랜드마다 사전에서 창고를 찾아 붙인다.", T(o[["order_id", "brand", "warehouse"]], hl=("warehouse",))),
    ]
