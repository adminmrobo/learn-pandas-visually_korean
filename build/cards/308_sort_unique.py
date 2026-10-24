from lib import *
from snippets import KOI

CARD = dict(
    id="sort_unique", ch="3. 고르고 거르기", cmd="sort_values() · unique()",
    title="정렬하고, 종류만 보기", excel="정렬 · 중복 제거",
    desc="sort_values 는 값 순서로 줄을 다시 세운다(ascending=False 면 큰 것부터). unique 는 겹치는 값을 빼고 종류만 보여 준다. "
         "카페 Koi 장부에서 들어온 돈이 큰 줄부터 보고, 어떤 항목이 있는지 종류만 뽑는다.",
    code=KOI + '''
print(book[["item", "sales"]].sort_values("sales"))                    # 작은 것부터
print(book[["item", "sales"]].sort_values("sales", ascending=False))   # 큰 것부터
print(book["item"].unique().tolist())''',
)

def stages(ns, out):
    b = ns["book"][["item", "sales"]]
    u = ns["book"]["item"].unique().tolist()
    return [
        S("원본", "장부 순서대로라 sales 크기가 뒤죽박죽이다.", T(b, index=True)),
        S("sort_values", "왼쪽은 작은 것부터(기본), 오른쪽은 ascending=False 로 큰 것부터. 줄 번호가 같이 움직인다.",
          T(b.sort_values("sales"), index=True, hl=("sales",)), T(b.sort_values("sales", ascending=False), index=True, hl=("sales",)),
          links=[[0, 0], [0, 1]]),
        S("unique", f"item 열 8줄에서 겹치는 이름을 빼면 {len(u)}종류가 남는다.",
          T(ns["book"][["item"]]), TX(str(u), "out", "unique().tolist()"), links=[]),
    ]
