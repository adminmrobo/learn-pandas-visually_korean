from lib import *

CARD = dict(
    id="col_strip", ch="2. 청소하기", cmd="df.columns.str.strip()",
    title="열 이름 앞뒤 공백 지우기", excel="TRIM",
    desc="엑셀에서 넘어온 열 이름에는 ' price ' 처럼 눈에 안 보이는 공백이 숨어 있다. 그대로 두면 cost[\"price\"] 가 KeyError 를 낸다. "
         "columns 에 .str.strip() 을 하면 모든 열 이름의 앞뒤 공백이 한 번에 지워진다. 예시는 카페 Koi 재료 원가표다.",
    code='''import pandas as pd
cost = pd.DataFrame({" supplier": ["Bean Lab", "Milky Farm"],
                     "item ": ["Coffee beans 1kg", "Milk 1L"],
                     " price ": ["₩32,000", "₩2,800"]})
print(list(cost.columns))           # 공백이 보인다
try:
    cost["price"]
except KeyError as e:
    print("KeyError:", e)           # 공백 때문에 못 찾는다
cost.columns = cost.columns.str.strip()
print(list(cost.columns))           # 공백이 사라졌다
print(cost["price"])                # 이제 꺼낼 수 있다''',
    talk=[
        dict(who="asst", text="price 열이 분명히 있는데 왜 못 찾는다고 해요?"),
        dict(who="doc", text="이름 앞뒤에 안 보이는 공백이 있어요. 지우고 다시 볼까요?"),
    ],
)

def ws(xs):
    return [str(x).replace(" ", "␣") for x in xs]

def stages(ns, out):
    cost = ns["cost"]
    before = [" supplier", "item ", " price "]
    dirty = cost.copy(); dirty.columns = ws(before)
    return [
        S("원본 열 이름", "␣ 가 공백 자리다. 사람 눈에는 안 보여도 컴퓨터에게는 다른 이름이라 \"price\" 로는 못 찾는다.",
          T(dirty), TX([l for l in out.splitlines() if l.startswith("KeyError")][0], "err", 'cost["price"]')),
        S("columns 만 꺼내기", "열 이름 목록만 따로 보면 공백이 드러난다.", RAW(["columns"], [[w] for w in ws(before)], cls=[["ws"]] * 3)),
        S(".str.strip()", "목록의 이름마다 앞뒤 공백을 지운다.", RAW(["columns"], [[c] for c in cost.columns], ccls=["hl"], cls=[["hl"]] * 3)),
        S("다시 표에 꽂기", '깨끗한 이름을 cost.columns 에 다시 넣는다. 이제 cost["price"] 가 된다.', T(cost, hl=("price",))),
    ]
