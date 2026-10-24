from lib import *
from snippets import KOI

CARD = dict(
    id="loc_assign", ch="4. 새 열 만들기", cmd="df.loc[조건, [열]] = 값",
    title="잘못된 줄만 골라 고치기", excel="필터 후 붙여넣기",
    desc="loc 의 행 자리에 조건을 넣고 오른쪽에 값을 주면 조건에 맞는 줄의 그 칸만 바뀐다. 아래는 깨진 컵 값이 들어온 돈(sales) 칸에 "
         "잘못 적힌 줄의 cost·sales 를 맞바꾸는 장면이다. .values 를 붙여야 열 이름이 아닌 숫자만 옮겨진다.",
    code=KOI + '''
book.loc[6, ["cost", "sales"]] = [0.0, 8.1]   # 직원이 깨진 컵 값을 sales 칸에 잘못 적었다
fix = book["item"] == "Broken cup"
book.loc[fix, ["cost", "sales"]] = book.loc[fix, ["sales", "cost"]].values   # 두 칸 맞바꾸기
print(book[["item", "cost", "sales"]])''',
    talk=[dict(who="robo", state="wrong", text="삐빅! 깨진 컵이 매출로 잡혀 있었어.")],
)

def stages(ns, out):
    import pandas as pd
    exec(KOI, g := {}); before = g["book"]; before.loc[6, ["cost", "sales"]] = [0.0, 8.1]
    after = ns["book"]
    fix = [i for i, v in enumerate(ns["fix"]) if v]
    rc = ["bad" if i in fix else "" for i in range(len(before))]
    cls = {(i, c): "hc" for i in fix for c in ("cost", "sales")}
    return [
        S("고칠 줄 찾기", f"fix 마스크가 {fix[0]}번 줄(Broken cup)을 가리킨다. 나간 돈인데 sales 에 {before.loc[fix[0], 'sales']} 이 있다.",
          T(before[["item", "cost", "sales"]], rcls=rc)),
        S("맞바꾸기", "그 줄의 [sales, cost] 값을 [cost, sales] 자리에 넣는다. 다른 줄은 그대로다.",
          T(after[["item", "cost", "sales"]], rcls=["ok" if i in fix else "" for i in range(len(after))], cls=cls)),
    ]
