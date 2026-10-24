from lib import *
import pandas as pd

CARD = dict(
    id="np_where", ch="4. 새 열 만들기", cmd="np.where(조건, 참일 때, 거짓일 때)",
    title="조건에 따라 다른 값", excel="IF / 중첩 IF",
    desc="np.where 는 엑셀 IF 와 같다. 줄마다 조건을 보고 True 면 두 번째 값, False 면 세 번째 값을 넣는다. "
         "np.where 안에 np.where 를 또 넣으면 중첩 IF 가 된다. 편의점 결제 금액을 Big / Mid / Small 로 나누고, 금액이 빈 줄은 따로 표시한다.",
    code='''import pandas as pd
import numpy as np
pay = pd.DataFrame({"receipt": [1, 2, 3, 4, 5],
                    "amount": [12600.0, 4300.0, np.nan, 25600.0, 7700.0]})
pay["size"] = np.where(pay["amount"].isna(), "missing",
                       np.where(pay["amount"] >= 10000, "Big",
                                np.where(pay["amount"] >= 5000, "Mid", "Small")))
print(pay)''',
)

def stages(ns, out):
    p = ns["pay"]
    a = p["amount"]
    s1 = p[["receipt", "amount"]].copy(); s1["isna?"] = a.isna()
    c1 = {(i, "isna?"): ("t" if v else "f") for i, v in enumerate(s1["isna?"])}
    big = [str(r) for r, v in zip(p["receipt"], p["size"]) if v == "Big"]
    miss = [str(r) for r, v in zip(p["receipt"], p["size"]) if v == "missing"]
    return [
        S("결제 금액", "편의점 영수증 다섯 장(원). 3번은 금액이 비었다.", T(p[["receipt", "amount"]], fmt=",.0f")),
        S("첫 번째 IF", f"amount 가 비었나? {', '.join(miss)}번만 True → 'missing'. 나머지는 다음 IF 로 간다.",
          T(s1, fmt={"amount": ",.0f"}, hl=("isna?",), cls=c1)),
        S("두·세 번째 IF", f"10,000원 이상이면 'Big'({', '.join(big)}번), 5,000원 이상이면 'Mid', 나머지는 'Small'.",
          T(p, fmt={"amount": ",.0f"}, hl=("size",))),
    ]
