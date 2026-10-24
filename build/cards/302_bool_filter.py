from lib import *
from snippets import KOI

CARD = dict(
    id="bool_filter", ch="3. 고르고 거르기", cmd='df[df["month"] == 4]',
    title="조건에 맞는 줄만 남기기", excel="자동 필터",
    desc='book["month"] == 4 는 줄마다 True/False 를 만든다(마스크). 이 마스크를 다시 book[...] 안에 넣으면 '
         "True 인 줄만 남는다. 엑셀 자동 필터와 같다. 카페 Koi 장부에서 4월 줄만 남긴다.",
    code=KOI + '''
mask = book["month"] == 4       # 줄마다 True/False
print(mask.tolist())
apr = book[mask]                # True 인 줄만
print(apr)
print("April rows:", len(apr))''',
)

def stages(ns, out):
    b, m, apr = ns["book"], ns["mask"], ns["apr"]
    mk = b[["item", "month"]].copy(); mk["mask"] = m
    cls = {(i, "mask"): ("t" if v else "f") for i, v in enumerate(m)}
    off = [i for i, v in enumerate(m) if not v]
    return [
        S("원본 표", "month 열을 본다. 4월과 5월 줄이 섞여 있다.", T(b, hl=("month",))),
        S("마스크 만들기", "== 4 를 줄마다 검사해 True/False 열이 생긴다.", T(mk, hl=("mask",), cls=cls)),
        S("True 만 남기기", f"False 인 {off[0]}~{off[-1]}번 줄이 빠지고 4월 {len(apr)}줄만 남는다.", T(apr, index=True)),
    ]
