from lib import *
from snippets import KOI

CARD = dict(
    id="col_math", ch="4. 새 열 만들기", cmd='df["new"] = df["a"] - df["b"]',
    title="열끼리 계산해 새 열", excel="=D2-C2 를 아래로 채우기",
    desc="열 하나는 숫자 묶음이라 열끼리 바로 더하고 뺄 수 있다. 줄마다 같은 자리끼리 계산되고, 왼쪽에 새 이름을 쓰면 새 열로 붙는다. "
         "엑셀에서 수식을 아래로 끌어 채우는 것과 같다. 카페 Koi 장부에서 줄마다 '남은 돈(net)'을 만든다.",
    code=KOI + '''
book["net"] = book["sales"] - book["cost"]     # 남은 돈 = 들어온 돈 − 나간 돈
print(book[["item", "cost", "sales", "net"]])
print("net total:", round(book["net"].sum(), 1))''',
    talk=[
        dict(who="asst", text="줄마다 들어온 돈에서 나간 돈을 빼고 싶어요."),
        dict(who="doc", text="열끼리 빼면 돼요. 결과에 이름을 붙이면 새 열이에요."),
    ],
)

def stages(ns, out):
    b = ns["book"]
    t = b[["item", "cost", "sales", "net"]]
    neg = [i for i, v in enumerate(t["net"]) if v < 0]
    return [
        S("원본", "나간 돈(cost)과 들어온 돈(sales) 두 열. 금액은 천원.", T(b[["item", "cost", "sales"]])),
        S("sales − cost", f"같은 줄끼리 뺀다. 판매는 +, 지출은 − 가 된다. 8줄을 다 더하면 {b['net'].sum():.1f} 천원.",
          T(t, hl=("net",), rcls=["bad" if i in neg else "" for i in range(len(t))])),
    ]
