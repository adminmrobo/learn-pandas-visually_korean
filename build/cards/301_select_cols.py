from lib import *
from snippets import KOI

CARD = dict(
    id="select_cols", ch="3. 고르고 거르기", cmd='df["col"] · df[["a", "b"]]',
    title="열 하나, 열 여러 개 꺼내기", excel="열 선택",
    desc="대괄호 하나에 열 이름 하나를 넣으면 한 줄짜리 Series 가 나온다. 대괄호를 두 겹으로 쓰고 안에 목록을 넣으면 "
         "그 열들만 남은 작은 표(DataFrame)가 나온다. 카페 Koi 장부에서 월(month)과 들어온 돈(sales)만 꺼내 본다.",
    code=KOI + '''
print(book["month"].head(3))                # 열 하나 → Series
print(book[["month", "sales"]].head(3))     # 열 여러 개 → DataFrame''',
    talk=[
        dict(who="asst", text="장부가 너무 넓어요. 필요한 칸만 볼 수 있어요?"),
        dict(who="doc", text="열 이름으로 꺼내면 돼요. 줄은 조건으로 고르고요."),
    ],
)

def stages(ns, out):
    b = ns["book"]
    return [
        S("원본 표 book", "카페 Koi 장부 8줄이다. month 와 sales 열을 꺼낼 것이다.", T(b, hl=("month", "sales"))),
        S("꺼내기", '왼쪽 book["month"] 는 열 하나(Series), 오른쪽 book[["month", "sales"]] 는 두 열짜리 표다. 줄 번호는 따라온다.',
          T(b["month"].head(3), index=True, title='book["month"].head(3)'),
          T(b[["month", "sales"]].head(3), index=True, title='book[["month", "sales"]].head(3)'),
          links=[[0, 0], [0, 1]]),
    ]
