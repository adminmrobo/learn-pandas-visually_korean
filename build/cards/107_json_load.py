from lib import *

REPLY = """{"status": "ok", "store": "Cafe Koi",
 "orders": [{"order_no": "D-2041", "menu": "Latte", "qty": 2, "price": "5,000"},
            {"order_no": "D-2042", "menu": "Cheesecake", "qty": 1, "price": "6,500"},
            {"order_no": "D-2043", "menu": "Americano", "qty": 3, "price": "4,500"}]}"""

CARD = dict(
    id="json_load", ch="1. 불러오기와 살펴보기", cmd="json.loads() → pd.DataFrame()",
    title="JSON 응답을 표로", excel="(엑셀에 없음) 웹 응답 읽기",
    desc="배달앱 같은 웹 서비스는 JSON 이라는 글자로 답한다. json 으로 읽으면 파이썬 사전(dict)이 되고, 표는 보통 그 안의 목록 키(여기서는 \"orders\")에 들어 있다. "
         "그 목록을 pd.DataFrame 에 넣으면 표가 된다.",
    code='''import pandas as pd
import json
reply = """''' + REPLY + '''"""
app = json.loads(reply)                  # 글자 → 사전(dict)
print("status:", app["status"], app["store"])
orders = pd.DataFrame(app["orders"])     # orders 부분 → 표
print(orders)''',
    tip='파일로 받았다면 with open("delivery.json", encoding="utf-8") as f: app = json.load(f) 로 읽는다. 파일은 json.load, 글자는 json.loads.',
)

def stages(ns, out):
    app, orders = ns["app"], ns["orders"]
    d = RAW(["key", "value"], [["status", app["status"]], ["store", app["store"]], ["orders", f"[ … {len(app['orders'])}개 … ]"]],
            title="app (dict)", rcls=["", "", "hr"])
    return [
        S("JSON 글자", "중괄호 { } 는 사전, 대괄호 [ ] 는 목록이다.", TX(REPLY, "code", "reply")),
        S("사전(dict)", f'json.loads 가 글자를 사전으로 바꾼다. status 가 "{app["status"]}" 이면 정상이다.', d),
        S("pd.DataFrame", f"orders 안의 항목 하나가 한 줄, 항목 안의 키가 열 이름이 된다. {len(orders)}줄. price 는 아직 글자(\"5,000\")다.",
          T(orders, hl=("price",))),
    ]
