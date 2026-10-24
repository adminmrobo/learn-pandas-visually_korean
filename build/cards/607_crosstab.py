from lib import *
from snippets import CVS

CARD = dict(
    id="crosstab", ch="6. 묶어서 집계하기", cmd="pd.crosstab(행, 열, values=, aggfunc=)",
    title="두 분류의 교차표", excel="피벗 테이블(행·열 필드)",
    desc="crosstab 은 두 열을 행과 열로 교차시킨 표다. values 와 aggfunc 를 안 주면 건수를 세고, 주면 칸마다 금액을 더한다. "
         "'도시락은 무엇으로 결제할까?' 같은 질문에 답한다. 편의점 상품군 × 결제수단으로 본다.",
    code=CVS + '''
print(pd.crosstab(cvs["category"], cvs["pay"]))                     # 건수
print(pd.crosstab(cvs["category"], cvs["pay"],
                  values=cvs["amount"] / 1000, aggfunc="sum").round(1))   # 금액(천원)''',
)

def stages(ns, out):
    cvs, pd = ns["cvs"], ns["pd"]
    ct = pd.crosstab(cvs["category"], cvs["pay"])
    cs = pd.crosstab(cvs["category"], cvs["pay"], values=cvs["amount"] / 1000, aggfunc="sum").round(1)
    lb = ct.loc["Lunchbox"]
    return [
        S("결제 기록", f"결제 {len(cvs)}건. 상품군(category)과 결제수단(pay) 두 분류가 있다.",
          T(cvs[["time", "category", "pay", "amount"]].head(6).astype(object), hl=("category", "pay"))),
        S("건수 교차", f"행 = category, 열 = pay. 칸마다 줄 수를 센다. 도시락(Lunchbox)은 카드 {lb['Card']}건, 현금 {lb['Cash']}건.",
          T(ct.astype(object), index=True, ix_name="category", hlrows=(list(ct.index).index("Lunchbox"),))),
        S("금액 교차", 'values=금액, aggfunc="sum" 을 주면 칸마다 금액을 더한다(천원).',
          T(cs.astype(object), index=True, ix_name="category")),
    ]
