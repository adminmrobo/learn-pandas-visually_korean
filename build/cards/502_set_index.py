from lib import *
from snippets import KOI

CARD = dict(
    id="set_index", ch="5. 합치고 모양 바꾸기", cmd="set_index() · reset_index()",
    title="열을 행 이름으로, 다시 열로", excel="첫 열을 머리글로 고정",
    desc='set_index("열") 은 그 열을 행 이름(index)으로 올린다. 그러면 a.loc[5, "sales"] 처럼 이름으로 값을 바로 집을 수 있다. '
         "reset_index() 는 반대로 행 이름을 보통 열로 내려놓는다. 카페 Koi 장부를 월별로 요약해서 해 본다(천원).",
    code=KOI + '''
m = book.groupby("month", as_index=False)[["sales", "cost"]].sum().round(1)
print(m)
a = m.set_index("month")          # month 가 행 이름으로 올라간다
print(a)
print("May sales:", a.loc[5, "sales"])
print(a.reset_index())            # 다시 보통 열로''',
)

def stages(ns, out):
    m, a = ns["m"], ns["a"]
    may = [l for l in out.splitlines() if l.startswith("May sales")][0]
    return [
        S("원본", "월별 요약표. 행 이름은 0, 1 번호이고 month 는 보통 열이다.", T(m.astype(object), index=True, hl=("month",))),
        S('set_index("month")', f'month 가 행 이름이 됐다. 이제 a.loc[5, "sales"] 처럼 월 이름으로 값을 집는다. 5월 매출 {a.loc[5, "sales"]}.',
          T(a.astype(object), index=True, ix_name="month", cls={(1, "sales"): "hc"}), TX(may, "out", "출력")),
        S("reset_index()", "행 이름을 다시 보통 열로 내려놓는다. 번호 0, 1 이 새로 붙는다.", T(a.reset_index().astype(object), index=True, hl=("month",))),
    ]
