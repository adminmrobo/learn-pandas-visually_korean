from lib import *
from snippets import KOI

CARD = dict(
    id="isna", ch="1. 불러오기와 살펴보기", cmd=".dtypes · .isna().sum()",
    title="자료형과 빈칸 세기", excel="필터로 (빈 셀) 찾기",
    desc="dtypes 는 열마다 자료형을 보여 준다. isna() 는 칸마다 '비었나?'를 True/False 로 바꾼 같은 크기의 표를 만든다. "
         "여기에 sum() 을 하면 True 를 1로 세므로 열마다 빈칸 수가 나온다.",
    code=KOI + '''
print(book.dtypes)            # 열마다 자료형
print(book.isna())            # 칸마다 빈칸이면 True
print(book.isna().sum())      # 열마다 True 개수 = 빈칸 수''',
)

def stages(ns, out):
    book = ns["book"]; na = book.isna(); s = na.sum()
    cls = {(i, c): ("t" if na.iloc[i][c] else "f") for i in range(len(na)) for c in na.columns}
    return [
        S("원본 표", f"customer 열 {s['customer']}칸이 비었다(None). 우유를 사거나 월세를 낸 줄은 손님이 없다.",
          T(book, hl=("customer",))),
        S("isna()", "모든 칸을 True(비었음)/False 로 바꾼다. 표 크기는 그대로다.", T(na, cls=cls)),
        S("sum()", f"True=1, False=0 으로 열마다 더한다. customer 만 {s['customer']} 이다.",
          T(s.rename("missing").to_frame(), index=True, hlrows=[list(s.index).index("customer")])),
    ]
