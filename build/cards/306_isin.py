from lib import *
from snippets import SHOP

CARD = dict(
    id="isin", ch="3. 고르고 거르기", cmd=".isin([...])",
    title="목록 안에 있나", excel="OR 여러 개",
    desc="isin 은 값이 목록 안에 들어 있으면 True 를 준다. == \"US\" | == \"JP\" 를 두 번 쓰는 대신 한 번에 쓴다. "
         "의류 쇼핑몰 주문 중 달러·엔 가격 안내가 필요한 미국·일본 주문을 표시한다.",
    code=SHOP + '''
orders["needs_guide"] = orders["country"].isin(["US", "JP"])
print(orders[["order_id", "country", "needs_guide"]])
print(orders[orders["needs_guide"]]["order_id"].tolist())''',
)

def stages(ns, out):
    o = ns["orders"]
    t = o[["order_id", "country", "needs_guide"]]
    cls = {(i, "needs_guide"): ("t" if v else "f") for i, v in enumerate(t["needs_guide"])}
    n = int(t["needs_guide"].sum())
    return [
        S("나라 열", "쇼핑몰 주문 여섯 건의 배송 나라.", T(o[["order_id", "country"]])),
        S('isin(["US", "JP"])', f"목록 안에 있는 US·JP 만 True. {n}건이다. 새 열 needs_guide 로 붙였다.",
          T(t, hl=("needs_guide",), cls=cls)),
    ]
