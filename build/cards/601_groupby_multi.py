from lib import *
from snippets import KOI

CARD = dict(
    id="groupby_multi", ch="6. 묶어서 집계하기", cmd="groupby([열1, 열2])",
    title="두 기준으로 묶기", excel="피벗 행에 필드 두 개",
    desc="groupby 에 열 목록을 주면 두 기준이 모두 같은 줄끼리 묶는다. 결과의 행 이름은 두 겹(월, 구분)이 된다. "
         "세 개를 넣으면 월 × 요일 × 손님 같은 '데이터 큐브'가 된다. 카페 Koi 장부를 월과 매출/비용으로 나눠 순액(net)을 더한다(천원).",
    code=KOI + '''
book["net"] = book["sales"] - book["cost"]     # 들어온 돈은 +, 나간 돈은 −
book["type"] = book["item"].map({"Coffee": "Sales", "Dessert": "Sales",
                                 "Milk": "Cost", "Rent": "Cost", "Broken cup": "Cost"})
print(book.groupby(["month", "type"])["net"].sum())''',
    talk=[
        dict(who="asst", text="월별로, 또 매출·비용별로 한 번에 나눌 수 있어요?"),
        dict(who="doc", text="groupby 에 열을 두 개 주면 돼요. 나누는 칸이 넷이 되죠."),
    ],
)

def stages(ns, out):
    b = ns["book"]
    res = b.groupby(["month", "type"])["net"].sum().round(1)
    keys = list(res.index)
    gmap = {k: f"g{i}" for i, k in enumerate(keys)}
    show = b[["month", "item", "type", "net"]].astype(object)
    parts = [T(b[(b.month == m) & (b.type == t)][["month", "type", "net"]].astype(object), rcls=[gmap[(m, t)]] * int(((b.month == m) & (b.type == t)).sum()))
             for m, t in keys]
    r = res.to_frame().astype(object)
    return [
        S("원본", "month(월)와 type(매출/비용) 두 열로 묶는다. net 은 들어온 돈 − 나간 돈.",
          T(show, rcls=[gmap[(m, t)] for m, t in zip(b.month, b.type)], hl=("month", "type"))),
        S("Split", f"(month, type) 쌍이 같은 줄끼리 조각이 된다. 조각 {len(keys)}개.", *parts),
        S("Aggregate · Combine", f"조각마다 net 을 더해 두 겹 이름의 표로 모은다. 5월 비용 순액은 {res[(5, 'Cost')]}(천원).",
          T(r, index=True, ix_name="month / type", rcls=[gmap[k] for k in keys], hl=("net",)),
          links=[[i, 0] for i in range(len(keys))]),
    ]
