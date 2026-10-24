from lib import *

CARD = dict(
    id="read_excel", ch="1. 불러오기와 살펴보기", cmd="pd.read_excel(header=None / skiprows)",
    title="지저분한 엑셀 읽기", excel="위쪽 제목 줄 무시하고 표 시작 찾기",
    desc="가게 엑셀은 맨 위에 제목 줄이 붙어 있곤 하다. header=None 은 '첫 줄을 열 이름으로 쓰지 말고 있는 그대로 보여 달라', "
         "skiprows=2 는 '위 두 줄은 건너뛰고 셋째 줄을 열 이름으로'라는 뜻이다. 예시는 카페 Koi 재료 원가표다.",
    code='''import pandas as pd
# 실습용 지저분한 엑셀을 먼저 만든다
rows = [["Cafe Koi ingredient cost", None, None],
        ["April 2025 (KRW)", None, None],
        [" supplier", "item ", " price "],
        ["Bean Lab", "Coffee beans 1kg", "₩32,000"],
        ["Bean Lab", "Decaf beans 1kg", "₩36,000"],
        [None, None, None],
        ["Milky Farm", "Milk 1L", "₩2,800"]]
pd.DataFrame(rows).to_excel("koi_cost.xlsx", sheet_name="cost", header=False, index=False)

raw = pd.read_excel("koi_cost.xlsx", sheet_name="cost", header=None)  # 있는 그대로
print(raw)
cost = pd.read_excel("koi_cost.xlsx", sheet_name="cost", skiprows=2)  # 위 두 줄 건너뛰기
print(cost)
print(list(cost.columns))''',
    tip='cost = pd.read_excel("내파일.xlsx", sheet_name="시트이름", skiprows=2). 먼저 header=None 으로 열어 진짜 열 이름이 몇 번째 줄인지 확인한다.',
)

def ws(df):
    d = df.copy(); d.columns = [str(c).replace(" ", "␣") for c in d.columns]; return d

def stages(ns, out):
    raw, cost = ns["raw"], ns["cost"]
    return [
        S("header=None", "날것 그대로 본 모습. 0·1번 줄은 제목, 2번 줄이 진짜 열 이름이다. 열 이름은 0, 1, 2 번호로 붙는다.",
          T(raw, index=True, rcls=["dim", "dim", "hr", "", "", "", ""])),
        S("skiprows=2", "위 두 줄을 버리고 셋째 줄을 열 이름으로 올렸다. 열 이름에 공백(␣)이 숨어 있고, 빈 줄과 ₩ 기호도 남아 있다. 2장 청소의 재료다.",
          T(ws(cost), index=True, rcls=["", "", "bad", ""])),
    ]
