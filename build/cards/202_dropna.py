from lib import *

CARD = dict(
    id="dropna", ch="2. 청소하기", cmd='dropna(how="all")',
    title="완전히 빈 줄만 지우기", excel="빈 행 삭제",
    desc="dropna() 는 빈칸이 있는 줄을 지운다. 그냥 쓰면 빈칸이 하나라도 있는 줄을 모두 지워 버린다. how=\"all\" 을 주면 모든 칸이 빈 줄만 지운다. "
         "원가표에서 배송일만 아직 안 정해진 재료는 살려야 하므로 how=\"all\" 이 맞다.",
    code='''import pandas as pd
import numpy as np
cost = pd.DataFrame({"supplier": ["Bean Lab", "Bean Lab", np.nan, "Milky Farm"],
                     "price": [32000, 36000, np.nan, 2800],
                     "delivery": ["2025-04-03", np.nan, np.nan, "2025-04-02"]})
print(cost.dropna(how="all"))   # 모든 칸이 빈 줄만 지움 → 3줄
print(cost.dropna())            # 빈칸이 하나라도 있으면 지움 → 2줄 (재료 하나를 잃는다)''',
)

def stages(ns, out):
    cost = ns["cost"]
    a, b = cost.dropna(how="all"), cost.dropna()
    lost = cost.loc[[i for i in a.index if i not in b.index]]
    return [
        S("원본", "2번 줄은 완전히 비었다. 1번 줄은 delivery 만 비었다(배송일 미정).", T(cost, index=True, rcls=["", "hr", "bad", ""])),
        S("두 가지 지우기",
          f'how="all" 은 2번 줄만 지워 {len(a)}줄이 남는다. 기본값 dropna() 는 1번 줄까지 지워 {len(b)}줄, price {int(lost["price"].iloc[0]):,}원짜리 재료가 사라진다.',
          T(a, index=True, title='dropna(how="all")', rcls=["", "hr", ""]), T(b, index=True, title="dropna()"), links=[[0, 0], [0, 1]]),
    ]
