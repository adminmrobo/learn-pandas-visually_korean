from lib import *
from snippets import KOI

CARD = dict(
    id="df_from_series", ch="5. 합치고 모양 바꾸기", cmd='pd.DataFrame({"a": s1, "b": s2})',
    title="Series 여러 개를 한 표로", excel="열 나란히 붙이기",
    desc="같은 행 이름을 가진 Series 여러 개를 사전에 담아 pd.DataFrame 에 넣으면 행 이름을 기준으로 나란히 붙은 표가 된다. "
         "한쪽에만 있는 행은 다른 쪽이 NaN 이고, fillna(0) 으로 채울 수 있다. 카페 Koi 의 커피 매출과 디저트 매출을 월별로 나란히 놓는다(천원).",
    code=KOI + '''
coffee = book[book["item"] == "Coffee"].groupby("month")["sales"].sum()
dessert = book[book["item"] == "Dessert"].groupby("month")["sales"].sum()
both = pd.DataFrame({"coffee": coffee, "dessert": dessert})
print(both)
print(both.fillna(0))''',
)

def stages(ns, out):
    coffee, dessert, both = ns["coffee"], ns["dessert"], ns["both"]
    missing = [m for m in both.index if m not in dessert.index]
    f = both.fillna(0)
    return [
        S("Series 두 개", f"행 이름이 월(month)이다. 디저트는 {', '.join(str(m) for m in dessert.index)}월에만 팔렸다.",
          T(coffee.round(1), index=True, title="coffee"), T(dessert.round(1), index=True, title="dessert")),
        S("pd.DataFrame({...})", f"행 이름끼리 맞춰 나란히 붙는다. {', '.join(str(m) for m in missing)}월의 dessert 는 NaN.",
          T(both.round(1), index=True, ix_name="month"), links=[[0, 0], [1, 0]]),
        S("fillna(0)", "NaN 을 0 으로 채운다. 안 팔린 달은 0 원이 맞다.",
          T(f.round(1), index=True, ix_name="month", cls={(list(both.index).index(m), "dessert"): "hc" for m in missing})),
    ]
