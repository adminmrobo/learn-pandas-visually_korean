from lib import *

CARD = dict(
    id="cumsum", ch="4. 새 열 만들기", cmd=".cumsum()",
    title="누적 합으로 시재 만들기", excel="=B2+C3 를 아래로 (누계)",
    desc="cumsum 은 위에서부터 차례로 더한 누적 합이다. 편의점 계산대에 아침에 넣어 둔 돈(기초 시재)에 "
         "하루하루 현금 입금 − 출금의 누적 합을 더하면 그날 저녁 계산대에 있어야 할 돈이 된다.",
    code='''import pandas as pd
cash = pd.DataFrame({"date": ["03-03", "03-04", "03-05", "03-06"],
                     "cash_in": [178800, 59700, 0, 112300], "cash_out": [0, 22700, 25100, 174700]})
cash["net"] = cash["cash_in"] - cash["cash_out"]
opening = 100000                                    # 처음 계산대에 넣어 둔 돈
cash["drawer"] = opening + cash["net"].cumsum()
print(cash)''',
)

def stages(ns, out):
    c = ns["cash"]
    cs = c[["date", "net"]].copy(); cs["net.cumsum()"] = c["net"].cumsum()
    f = {k: "," for k in ["cash_in", "cash_out", "net", "drawer", "net.cumsum()"]}
    n = c["net"].tolist()
    return [
        S("하루 현금", "입금 − 출금 = 그날 남은 현금(net). 단위는 원.", T(c[["date", "cash_in", "cash_out", "net"]], fmt=f, hl=("net",))),
        S("net.cumsum()", f"{n[0]:,} → {n[0]:,} + {n[1]:,} → … 위에서부터 계속 더해 내려간다.", T(cs, fmt=f, hl=("net.cumsum()",))),
        S(f"+ 기초 {ns['opening']:,}", "누적 합에 처음 넣어 둔 돈을 더하면 그날 계산대에 있어야 할 돈(drawer).",
          T(c[["date", "net", "drawer"]], fmt=f, hl=("drawer",))),
    ]
