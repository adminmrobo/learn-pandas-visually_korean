from lib import *

CARD = dict(
    id="rank", ch="6. 묶어서 집계하기", cmd=".rank(ascending=False)",
    title="순위 매기기", excel="RANK",
    desc="rank 는 값마다 순위를 준다. ascending=False 면 큰 값이 1위. 합계 순위와 평균 순위를 나란히 놓으면 무엇으로 줄 세우느냐에 따라 "
         "순서가 바뀌는 것을 볼 수 있다. 의류 쇼핑몰 다섯 브랜드의 주문 금액(천원)으로 본다.",
    code='''import pandas as pd
s = pd.DataFrame({"mean": [28.2, 84.0, 51.7, 45.0, 19.5], "sum": [141.0, 168.0, 155.0, 90.0, 117.0]},
                 index=["Mono", "Denimo", "Linen", "Knitty", "Basic"])
s["rank_sum"] = s["sum"].rank(ascending=False).astype(int)
s["rank_mean"] = s["mean"].rank(ascending=False).astype(int)
print(s)''',
)

def stages(ns, out):
    s = ns["s"]
    moved = [b for b in s.index if s.loc[b, "rank_sum"] != s.loc[b, "rank_mean"]]
    k = s.loc["Knitty"]
    return [
        S("브랜드별 평균·합계", "다섯 브랜드의 주문 한 건 평균과 전체 합계.", T(s[["mean", "sum"]], index=True, ix_name="brand")),
        S("rank 두 번", f"Knitty 는 합계로 {int(k['rank_sum'])}위인데 평균으로 {int(k['rank_mean'])}위다. 순위가 바뀐 브랜드: {', '.join(moved)}.",
          T(s.astype(object), index=True, ix_name="brand", hl=("rank_sum", "rank_mean"),
            rcls=["hr" if b in moved else "" for b in s.index])),
    ]
