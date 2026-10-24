from lib import *
from snippets import KOI

CARD = dict(
    id="head_tail", ch="1. 불러오기와 살펴보기", cmd=".shape · .head() · .tail()",
    title="몇 줄인지, 앞뒤가 어떤지 보기", excel="Ctrl+↓ 로 끝까지 내려 보기",
    desc="표를 읽자마자 가장 먼저 모양을 본다. shape 는 (행 수, 열 수), head(n) 은 앞 n줄, tail(n) 은 뒤 n줄이다. "
         "카페 Koi 장부 전체를 다 출력하지 않고도 제대로 읽혔는지 확인할 수 있다.",
    code=KOI + '''
print("rows x cols:", book.shape)   # (행, 열)
print(book.head(3))                 # 앞 3줄
print(book.tail(2))                 # 뒤 2줄''',
)

def stages(ns, out):
    book = ns["book"]; n = len(book)
    rc = ["g0" if i < 3 else ("g1" if i >= n - 2 else "") for i in range(n)]
    return [
        S("원본 표 book", f"{book.shape[0]}줄 × {book.shape[1]}열짜리 장부다. 위 3줄(파랑)과 아래 2줄(주황)을 꺼내 볼 것이다.",
          T(book, index=True, rcls=rc)),
        S("모양과 앞뒤",
          f"shape 는 {book.shape}. head(3) 은 0~2번 줄, tail(2) 는 {n-2}~{n-1}번 줄이다. 줄 번호(index)는 원래 번호를 그대로 들고 온다.",
          TX(f"rows x cols: {book.shape}", "out", "book.shape"),
          T(book.head(3), index=True, rcls=["g0"] * 3, title="book.head(3)"),
          T(book.tail(2), index=True, rcls=["g1"] * 2, title="book.tail(2)"), links=[[0, 0], [0, 1], [0, 2]]),
    ]
