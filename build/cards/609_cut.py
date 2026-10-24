from lib import *
from snippets import CVS

CARD = dict(
    id="cut", ch="6. 묶어서 집계하기", cmd="pd.cut(bins=, labels=)",
    title="숫자를 구간으로 나누기", excel="중첩 IF / VLOOKUP 근사 일치",
    desc="pd.cut 은 연속된 숫자를 구간 상자에 넣는다. bins=[0, 3000, 10000, 20000, 100000] 은 (0, 3000], (3000, 10000] … 네 상자이고 "
         "labels 로 상자 이름을 붙인다. 그 뒤 groupby 로 상자별 건수와 합계를 낸다. 편의점 결제 금액(원)으로 본다.",
    code=CVS + '''
cvs["size"] = pd.cut(cvs["amount"], bins=[0, 3000, 10000, 20000, 100000],
                     labels=["Small", "Medium", "Large", "Bulk"])
print(cvs[["amount", "size"]].head(6))
print(cvs.groupby("size", observed=True)["amount"].agg(["count", "sum"]))''',
)

def stages(ns, out):
    cvs = ns["cvs"]
    h = cvs[["amount", "size"]].head(6).astype(object)
    agg = cvs.groupby("size", observed=True)["amount"].agg(["count", "sum"])
    g = {"Small": "g0", "Medium": "g1", "Large": "g2", "Bulk": "g3"}
    big = agg["sum"].idxmax()
    return [
        S("결제 금액", f"결제 {len(cvs)}건 중 앞 6줄. 금액이 1,600원부터 {cvs['amount'].max():,.0f}원까지 흩어져 있다.",
          T(cvs[["time", "amount"]].head(6).astype(object))),
        S("pd.cut", "3,000원 이하는 Small, 3,000원 초과 10,000원 이하는 Medium … 상자 이름이 붙는다.",
          T(h, hl=("size",), rcls=[g[s] for s in h["size"]])),
        S("상자별 집계", f'groupby("size") 로 합친다. 건수는 {agg["count"].idxmax()} 이 {agg["count"].max()}건으로 가장 많고, 금액 합계도 {big} 이 가장 크다. observed=True 는 빈 상자를 빼라는 뜻.',
          T(agg.astype(object), index=True, ix_name="size", rcls=[g[s] for s in agg.index], hl=("count", "sum"))),
    ]
