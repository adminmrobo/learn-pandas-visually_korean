from lib import *

CARD = dict(
    id="loc_iloc", ch="3. 고르고 거르기", cmd="loc[행, 열] · iloc[번호]",
    title="칸 하나 콕 집기", excel="셀 주소 B3",
    desc='loc 은 이름으로, iloc 은 번호(0부터)로 집는다. loc[조건, "열"] 처럼 행 자리에 마스크를 넣으면 조건에 맞는 줄의 그 열만 꺼낸다. '
         "iloc[0] 은 첫 줄, iloc[-1] 은 마지막 줄이다. 카페 Koi 월별 요약표(백만원)로 연습한다.",
    code='''import pandas as pd
# 카페 Koi 월별 요약 (백만원). 행 이름 = 월
summary = pd.DataFrame({"Sales": [4.00, 4.28, 4.36], "Cost": [0.84, 0.99, 0.57]}, index=[4, 5, 6])
summary.index.name = "month"
print(summary.loc[5, "Cost"])                       # 행 이름 5, 열 이름 Cost
print(summary["Sales"].iloc[0])                     # 첫 번째 값
print(summary["Sales"].iloc[-1])                    # 마지막 값
print(summary.loc[summary["Cost"] > 0.8, "Sales"])  # 조건에 맞는 줄의 Sales''',
)

def stages(ns, out):
    s = ns["summary"]
    v = s.loc[5, "Cost"]; a = s["Sales"].iloc[0]; z = s["Sales"].iloc[-1]
    sel = s.loc[s["Cost"] > 0.8, "Sales"]
    cls = {(1, "Cost"): "hc", (0, "Sales"): "hl", (2, "Sales"): "hl"}
    return [
        S("월별 요약표", "행 이름(index)이 월(4·5·6)이다. 0부터 세는 번호와 다르다는 점에 주의.", T(s, index=True, fmt="0.2f")),
        S("집어 오기", f'loc[5, "Cost"] = {v}. iloc[0] 은 첫 줄(4월) {a}, iloc[-1] 은 마지막 줄(6월) {z}.',
          T(s, index=True, fmt="0.2f", cls=cls), TX("\n".join(out.splitlines()[:3]), "out", "출력")),
        S("loc[조건, 열]", f"Cost > 0.8 인 {'·'.join(map(str, sel.index))}월의 Sales 만 꺼낸다.",
          T(sel, index=True, fmt="0.2f", hl=("Sales",))),
    ]
