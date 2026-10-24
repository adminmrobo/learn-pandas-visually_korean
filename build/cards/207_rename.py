from lib import *

CARD = dict(
    id="rename", ch="2. 청소하기", cmd="rename(columns={...}) · df.columns = [...]",
    title="열 이름을 영어로 바꾸기", excel="머리글 고쳐 쓰기",
    desc="rename 은 사전에 적은 열만 골라 이름을 바꾼다. df.columns = [...] 는 모든 열 이름을 순서대로 통째로 바꾼다. "
         "편의점 POS 에서 내려받은 파일은 열 이름이 한글이라, 영어로 바꾸면 query 와 차트 라벨이 쉬워진다.",
    code='''import pandas as pd
pos = pd.DataFrame({"결제시각": ["2025-03-03 08:04", "2025-03-03 12:31"],
                    "상품군": ["Drink", "Lunchbox"], "결제금액(원)": [2000, 5500]})
pos = pos.rename(columns={"결제시각": "time", "결제금액(원)": "amount"})   # 고른 열만
print(pos)
stock = pd.DataFrame({"상품": ["Ramen", "Ice cream"], "재고": [24, 9], "유통기한": ["2025-09-30", "2026-02-28"]})
stock.columns = ["item", "qty", "expiry"]   # 순서대로 통째로 바꾸기
print(stock)''',
)

def stages(ns, out):
    import pandas as pd
    pos, stock = ns["pos"], ns["stock"]
    p0 = pos.copy(); p0.columns = ["결제시각", "상품군", "결제금액(원)"]
    s0 = stock.copy(); s0.columns = ["상품", "재고", "유통기한"]
    return [
        S("한글 열 이름", "POS 파일은 열 이름이 한글이다. 표 출력은 괜찮지만 차트 라벨과 query 에서 불편하다.", T(p0, title="pos"), T(s0, title="stock")),
        S("이름 바꾸기", "위: rename 은 사전의 짝대로 바꾸고, 사전에 없는 상품군은 그대로 둔다. 아래: columns = [...] 는 왼쪽부터 순서대로 덮어쓴다. 값은 그대로다.",
          T(pos, hl=("time", "amount"), title="pos"), T(stock, hl=("item", "qty", "expiry"), title="stock")),
    ]
