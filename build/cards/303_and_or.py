from lib import *
from snippets import KOI

CARD = dict(
    id="and_or", ch="3. 고르고 거르기", cmd="(조건1) & (조건2)",
    title="조건 두 개를 함께", excel="AND 필터",
    desc="조건 두 개를 함께 쓰려면 각 조건을 괄호로 감싸고 & (그리고), | (또는) 로 잇는다. 'and', 'or' 를 쓰면 오류가 난다. "
         "아래는 '나간 돈 항목인데 들어온 돈(sales) 칸에 적힌 줄'을 찾는 검사다.",
    code=KOI + '''
book.loc[6, ["cost", "sales"]] = [0.0, 8.1]   # 직원이 깨진 컵 값을 sales 칸에 잘못 적었다
is_cost = book["item"].isin(["Milk", "Rent", "Broken cup"])   # 나간 돈 항목인가
in_sales = book["sales"] > 0                                   # sales 칸에 금액이 있나
wrong = book[is_cost & in_sales]                               # 둘 다 True
print(wrong)
either = book[(book["item"] == "Rent") | (book["item"] == "Milk")]   # | 는 '또는'
print(either[["item", "cost"]])''',
)

def stages(ns, out):
    b, a, c, w = ns["book"], ns["is_cost"], ns["in_sales"], ns["wrong"]
    t = b[["item", "cost", "sales"]].copy(); t["is_cost"] = a; t["in_sales"] = c
    cls = {}
    for i in range(len(t)):
        cls[(i, "is_cost")] = "t" if a.iloc[i] else "f"; cls[(i, "in_sales")] = "t" if c.iloc[i] else "f"
    t2 = t.copy(); t2["both"] = a & c
    cls2 = dict(cls); cls2.update({(i, "both"): ("hc" if v else "f") for i, v in enumerate(t2["both"])})
    hit = list(w.index)
    return [
        S("원본", "나간 돈 항목(Milk, Rent, Broken cup)인데 sales 칸에 금액이 있다면 잘못 적은 것이다.", T(b[["item", "cost", "sales"]])),
        S("조건 두 개", "왼쪽 조건(나간 돈 항목?)과 오른쪽 조건(sales > 0?)을 줄마다 따로 계산한다.", T(t, hl=("is_cost", "in_sales"), cls=cls)),
        S("& 로 합치기", f"둘 다 True 인 줄만 True. {hit[0]}번 {w['item'].iloc[0]} 한 줄이 걸린다.",
          T(t2, hl=("both",), cls=cls2, rcls=["bad" if i in hit else "" for i in range(len(t2))])),
        S("결과", "잘못 적힌 줄만 꺼냈다. | 로 이으면 '또는'이 되어 Rent 나 Milk 인 줄이 모두 나온다.",
          T(w, index=True), T(ns["either"][["item", "cost"]], index=True, title="(Rent) | (Milk)")),
    ]
