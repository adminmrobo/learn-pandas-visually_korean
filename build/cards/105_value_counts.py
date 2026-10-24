from lib import *
from snippets import KOI

CARD = dict(
    id="value_counts", ch="1. 불러오기와 살펴보기", cmd=".value_counts()",
    title="값마다 몇 번 나오나", excel="COUNTIF",
    desc="한 열에서 같은 값끼리 모아 개수를 센다. 많은 순서로 정렬해서 보여 준다. normalize=True 를 주면 개수 대신 비율(합계 1)이 나온다. "
         "빈칸은 기본으로 빠지므로, 빈칸도 세려면 dropna=False 를 준다.",
    code=KOI + '''
print(book["item"].value_counts())                    # 개수
print(book["item"].value_counts(normalize=True))      # 비율
print(book["customer"].value_counts(dropna=False))    # 빈칸(None)도 센다''',
)

def stages(ns, out):
    book = ns["book"]
    vc = book["item"].value_counts(); pr = book["item"].value_counts(normalize=True)
    order = list(vc.index); g = {v: f"g{i}" for i, v in enumerate(order)}
    groups = [T(book.loc[book["item"] == v, ["item"]], rcls=[g[v]] * int(vc[v])) for v in order]
    res = vc.rename("count").to_frame().join(pr.rename("proportion"))
    cust = book["customer"].value_counts(dropna=False)
    return [
        S("item 열", f"장부의 item {len(book)}개. 같은 이름끼리 같은 색이다.", T(book[["item"]], rcls=[g[v] for v in book["item"]])),
        S("같은 값끼리 모으기", "같은 값끼리 묶는다. 0장 groupby 의 Split 과 같다.", *groups, links=[[0, i] for i in range(len(order))]),
        S("개수 · 비율",
          f"묶음마다 줄 수를 세고 큰 순서로 세운다. Coffee 는 {vc['Coffee']}번, 비율은 {vc['Coffee']} ÷ {len(book)} = {pr['Coffee']}.",
          T(res.astype(object), index=True, hl=("count", "proportion")), links=[[i, 0] for i in range(len(order))]),
        S("dropna=False", f"customer 를 셀 때 빈칸(None) {int(cust[cust.index.isna()].iloc[0])}개도 한 묶음으로 센다. 빼면 빈칸은 안 보인다.",
          T(cust.rename("count").to_frame(), index=True, ix_name="customer"), links=[[0, 0]]),
    ]
