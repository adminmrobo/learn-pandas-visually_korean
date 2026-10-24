from lib import *
from snippets import KOI

CARD = dict(
    id="query", ch="3. 고르고 거르기", cmd='df.query("...")',
    title="글자로 쓰는 필터", excel="고급 필터",
    desc="query 는 조건을 문장처럼 쓴다. 열 이름을 그대로 쓰고 and / or 를 쓸 수 있다. 글자 값은 작은따옴표로 감싼다. "
         "book[(book[\"month\"] == 5) & (book[\"customer\"] == \"Regular\")] 와 결과가 같다.",
    code=KOI + '''
reg = book.query("month == 5 and customer == 'Regular'")
print(reg)
print("count:", len(reg), "/ sum:", reg["sales"].sum())''',
)

def stages(ns, out):
    b, r = ns["book"], ns["reg"]
    t = b[["item", "sales", "customer", "month"]].copy()
    c1 = t["month"] == 5; c2 = t["customer"] == "Regular"
    t["month==5"] = c1; t["Regular?"] = c2
    cls = {}
    for i in range(len(t)):
        cls[(i, "month==5")] = "t" if c1.iloc[i] else "f"; cls[(i, "Regular?")] = "t" if c2.iloc[i] else "f"
    hit = list(r.index)
    return [
        S("원본", "5월 이면서 단골(Regular)인 줄을 찾는다.", T(b[["item", "sales", "customer", "month"]])),
        S("두 조건 검사", f"month == 5 와 customer == 'Regular' 를 줄마다 본다. 둘 다 맞는 줄은 {', '.join(map(str, hit))}번뿐이다.",
          T(t, hl=("month==5", "Regular?"), cls=cls, rcls=["ok" if i in hit else "" for i in range(len(t))])),
        S("결과", f"{len(r)}줄이 남는다. 합계 {r['sales'].sum():g} 천원.", T(r, index=True), TX(out.splitlines()[-1], "out", "출력")),
    ]
