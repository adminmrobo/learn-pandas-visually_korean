from lib import *

CARD = dict(
    id="meshgrid", ch="7. numpy 계산", cmd="lambda · np.linspace · np.meshgrid",
    title="가정 격자 한 번에 계산", excel="데이터 표(가상 분석)",
    desc="linspace 는 구간을 같은 간격으로 나눈 값들, meshgrid 는 두 목록의 모든 조합 격자를 만든다. lambda 로 '커피 한 잔 값 P, 원두 원가 B → 한 달 이익' "
         "계산식을 함수로 두면 격자 전체를 한 번에 계산한다. 엑셀의 2변수 데이터 표와 같다. 카페 Koi 의 가정으로 해 본다.",
    code='''import numpy as np
import pandas as pd
A = {"cups": 3000, "other": 1500, "fixed": 6_000_000}     # 한 달 잔 수, 잔당 기타 원가(원), 고정비(원)
profit = lambda P, B: (A["cups"] * (P - B - A["other"]) - A["fixed"]) / 10000   # 만원
p = np.linspace(4000, 5000, 3)      # 커피값 4,000 / 4,500 / 5,000원
b = np.linspace(600, 1200, 4)       # 원두 원가 600 / 800 / 1,000 / 1,200원
P, B = np.meshgrid(p, b)
Z = profit(P, B)
print(pd.DataFrame(Z.round(1), index=b.astype(int), columns=p.astype(int)))''',
)

def stages(ns, out):
    pd = __import__("pandas")
    p, b, P, B, Z = ns["p"], ns["b"], ns["P"], ns["B"], ns["Z"]
    Pt = pd.DataFrame(P.astype(int), index=b.astype(int), columns=p.astype(int))
    Bt = pd.DataFrame(B.astype(int), index=b.astype(int), columns=p.astype(int))
    Zt = pd.DataFrame(Z.round(1), index=b.astype(int), columns=p.astype(int))
    zero = [(i, c) for i, r in enumerate(Zt.index) for c in Zt.columns if Zt.loc[r, c] == 0]
    cls = {(i, c): "hc" for i, c in zero}
    zr, zc = Zt.index[zero[0][0]], zero[0][1]
    return [
        S("linspace", "커피값 3칸, 원두 원가 4칸을 같은 간격으로 만든다.", TX(str(p.astype(int)), "out", "p (커피값)"), TX(str(b.astype(int)), "out", "b (원두 원가)")),
        S("meshgrid", f"가능한 모든 (P, B) 조합 {len(b)} × {len(p)} = {Z.size}칸 격자. 칸 하나가 시나리오 하나다. 행 = 원두 원가, 열 = 커피값.",
          T(Pt.astype(object), index=True, ix_name="B \\ P", title="P"), T(Bt.astype(object), index=True, ix_name="B \\ P", title="B")),
        S("profit(P, B)", f"격자 칸마다 같은 식을 계산한다(만원). 원두 {zr}원, 커피 {zc}원 칸이 정확히 0 — 손익분기다.",
          T(Zt.astype(object), index=True, ix_name="B \\ P", cls=cls)),
    ]
