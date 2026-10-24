from lib import *

CARD = dict(
    id="reindex", ch="5. 합치고 모양 바꾸기", cmd="reindex(columns=[...])",
    title="열 순서를 내가 정한 대로", excel="열 끌어서 옮기기",
    desc="요일별로 집계하면 요일 열이 알파벳 순서(Fri, Mon, Sat …)로 나오기 쉽다. reindex 에 원하는 순서 목록을 주면 그 순서로 다시 세운다. "
         "목록에 있는데 표에 없는 열은 NaN 으로 생긴다. 편의점 아이스크림 판매 건수로 본다.",
    code='''import pandas as pd
# 편의점 아이스크림 판매 건수 (주 × 요일). 집계하면 열이 알파벳 순서로 나온다
ice = pd.DataFrame({"Fri": [15, 20], "Mon": [16, 8], "Sat": [None, 3], "Thu": [13, 12]},
                   index=["Week 1", "Week 2"])
print(ice)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
print(ice.reindex(columns=days))''',
)

def stages(ns, out):
    ice, days = ns["ice"], ns["days"]
    r = ice.reindex(columns=days)
    miss = [d for d in days if d not in ice.columns]
    cls = {(i, d): "nan" for i in range(len(r)) for d in miss}
    return [
        S("알파벳 순서", "Fri, Mon, Sat, Thu — 달력 순서가 아니다.", T(ice.astype(object), index=True)),
        S("reindex(columns=days)", f"Mon~Sun 순서로 다시 세운다. 표에 없던 {'·'.join(miss)} 는 NaN 열로 생긴다.",
          T(r.astype(object), index=True, hl=tuple(miss), cls=cls)),
    ]
