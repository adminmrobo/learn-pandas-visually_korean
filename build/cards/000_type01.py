from lib import *

CARD = dict(
    id="type01", ch="0. 한눈에 보는 groupby", cmd="groupby().sum()",
    title="나누고 · 합치고 · 모은다", excel="SUMIF, 피벗 테이블의 합계",
    desc="groupby 는 표를 같은 값끼리 나누고(Split), 조각마다 계산하고(Aggregate), 결과를 다시 한 표로 모은다(Combine). "
         "세 가게의 하루 매출로 이 세 동작을 본다. 이 책의 모든 집계 명령은 이 뼈대 위에서 움직인다.",
    code='''# 상가 세 가게의 오전 매출 기록 (천원)
import pandas as pd
df = pd.DataFrame({
    "store": ["Cafe", "Cafe", "Cafe", "CVS", "CVS", "CVS", "Shop", "Shop", "Shop"],
    "sales": [34, 25, 20, 10, 12, 1, 3, 0, 7],
})
# store 가 같은 줄끼리 나눠서 sales 를 더한다
result = df.groupby("store")["sales"].sum()
print(result)''',
    talk=[
        dict(who="asst", text="가게가 셋인데 매출을 한 번에 더할 수 있어요?"),
        dict(who="doc", text="같은 가게끼리 나누고, 더하고, 다시 모으면 돼요."),
    ],
)

def stages(ns, out):
    df, res = ns["df"], ns["result"]
    g = {"Cafe": "g0", "CVS": "g1", "Shop": "g2"}
    parts = [T(df[df.store == s], rcls=[g[s]] * 3) for s in ["Cafe", "CVS", "Shop"]]
    sums = [T(df[df.store == s].groupby("store")["sales"].sum().reset_index(), rcls=[g[s]], hl=("sales",)) for s in ["Cafe", "CVS", "Shop"]]
    return [
        S("원본 표", "store 열에 Cafe·CVS·Shop 세 가게가 섞여 있다. 같은 가게는 같은 색이다.",
          T(df, rcls=[g[s] for s in df.store])),
        S("Split · 나누기", 'groupby("store") 가 같은 가게끼리 줄을 모아 조각 세 개로 나눈다.', *parts),
        S("Aggregate · sum", "조각마다 sales 를 더한다. Cafe 는 34 + 25 + 20 = 79.", *sums, links=[[0, 0], [1, 1], [2, 2]]),
        S("Combine · 모으기", "세 결과를 한 표로 모은다. 가게 이름이 행 이름(index)이 된다.",
          T(res, index=True, hl=("sales",)), links=[[0, 0], [1, 0], [2, 0]]),
    ]
