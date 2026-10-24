from lib import *
from snippets import SHOP

CARD = dict(
    id="dt_access", ch="4. 새 열 만들기", cmd=".dt.day_name() · (날짜 − 날짜).dt.days",
    title="날짜에서 요일·경과일 뽑기", excel='TEXT(날짜,"ddd") · 날짜 빼기',
    desc="날짜형 열 뒤에 .dt 를 붙이면 날짜 기능을 쓸 수 있다. day_name() 은 요일 이름, .str[:3] 은 앞 세 글자. "
         "도착일에서 주문일을 빼면 기간이 되고, .dt.days 로 날수만 꺼낸다. 쇼핑몰 해외 주문이 며칠 걸려 도착했는지 본다.",
    code=SHOP + '''
orders["arrived"] = pd.to_datetime(["2025-01-09", "2025-01-07", "2025-01-13", "2025-01-10", "2025-01-08", "2025-01-11"])
orders["weekday"] = orders["date"].dt.day_name().str[:3]            # Thu, Fri ...
orders["days"] = (orders["arrived"] - orders["date"]).dt.days       # 걸린 날수
print(orders[["order_id", "date", "weekday", "arrived", "days"]])''',
)

def stages(ns, out):
    o = ns["orders"]
    mx = o.loc[o["days"].idxmax()]
    return [
        S("주문일", "날짜형(datetime64) 열 date.", T(o[["order_id", "date"]])),
        S("day_name().str[:3]", f"요일 이름 {o['date'].iloc[0].day_name()} → 앞 세 글자 {o['weekday'].iloc[0]}.",
          T(o[["order_id", "date", "weekday"]], hl=("weekday",))),
        S("도착일 − 주문일", f"빼면 기간, .dt.days 로 날수만 남긴다. 가장 오래 걸린 주문은 {mx['order_id']}번({mx['country']}) {mx['days']}일.",
          T(o[["order_id", "date", "arrived", "days"]], hl=("days",))),
    ]
