from lib import *

CARD = dict(
    id="modulo", ch="4. 새 열 만들기", cmd="% (나머지)",
    title="딱 떨어지는 금액 찾기", excel="MOD",
    desc="% 는 나눈 나머지다. 금액 % 1000 == 0 이면 천 원 단위로 딱 떨어진다는 뜻이다. 편의점 결제는 보통 2,350원처럼 끝자리가 있어서, "
         "딱 떨어지는 금액은 계산대에서 손으로 친 결제일 수 있다. 그런 줄을 골라 확인한다.",
    code='''import pandas as pd
pay = pd.DataFrame({"receipt": [1, 2, 3, 4, 5],
                    "amount": [2350, 5000, 7820, 12000, 3640]})
pay["remainder"] = pay["amount"] % 1000
pay["Round"] = pay["amount"] % 1000 == 0
print(pay)
print("round payments:", pay["Round"].sum())''',
    talk=[dict(who="fly", text="딱 떨어지는 금액이 많으면, 누가 손으로 친 거 아냐?")],
)

def stages(ns, out):
    p = ns["pay"]
    r = [i for i, v in enumerate(p["Round"]) if v]
    vals = [f"{p['amount'].iloc[i]:,}" for i in r]
    cls = {(i, "Round"): ("t" if v else "f") for i, v in enumerate(p["Round"])}
    return [
        S("결제 금액", "편의점 결제 다섯 건(원).", T(p[["receipt", "amount"]], fmt={"amount": ","})),
        S("% 1000", f"1,000 으로 나눈 나머지. {' 과 '.join(vals)} 은 0.", T(p[["receipt", "amount", "remainder"]], fmt={"amount": ","}, hl=("remainder",))),
        S("== 0", f"나머지가 0 인 줄이 딱 떨어지는 결제. True 를 세면 {int(p['Round'].sum())}건.",
          T(p, fmt={"amount": ","}, hl=("Round",), cls=cls, rcls=["hr" if i in r else "" for i in range(len(p))])),
    ]
