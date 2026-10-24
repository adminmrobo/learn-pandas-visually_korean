from lib import *

CSV = """date,item,cost,sales
2025-04-01,Coffee,0,9.4
2025-04-01,Milk,22.3,0
2025-04-01,Coffee,0,82.0
2025-04-02,Coffee,0,82.3"""

CARD = dict(
    id="read_csv", ch="1. 불러오기와 살펴보기", cmd="pd.read_csv()",
    title="CSV 파일을 표로 읽기", excel="파일 열기",
    desc="CSV 는 쉼표로 칸을 나눈 글자 파일이다. read_csv 는 줄을 행으로, 쉼표를 칸 경계로 읽어 표(DataFrame)를 만든다. "
         "parse_dates 를 주면 날짜 글자를 날짜형으로 바꿔 읽는다. 예시는 카페 Koi 장부의 앞부분이다(금액은 천원).",
    code='''# 파일 없이 바로 실습: CSV 글자를 io.StringIO 로 '가짜 파일'처럼 만든다
import pandas as pd
import io
csv_text = """''' + CSV + '''"""
raw = pd.read_csv(io.StringIO(csv_text), dtype=str)             # 모두 글자로 읽은 모습
book = pd.read_csv(io.StringIO(csv_text), parse_dates=["date"])  # 제대로 읽은 모습
print("rows x cols:", book.shape)
print(book)
print(book.dtypes)''',
    tip='book = pd.read_csv("koi_book.csv", encoding="utf-8-sig", parse_dates=["date"]) 처럼 파일 이름을 넣는다. 엑셀에서 저장한 한글 CSV 는 encoding="utf-8-sig".',
    talk=[
        dict(who="asst", text="장부 파일을 열면 제일 먼저 뭘 봐요?"),
        dict(who="doc", text="몇 줄인지, 칸이 어떤 자료형인지부터요."),
    ],
)

def stages(ns, out):
    raw, book = ns["raw"], ns["book"]
    dt = book.dtypes.astype(str).rename("dtype").to_frame()
    return [
        S("CSV 파일", "파일 안은 그냥 글자다. 첫 줄은 열 이름, 쉼표(,)가 칸 경계다.", TX(CSV, "code", "koi_book.csv 앞부분")),
        S("쉼표로 자르기", "줄은 행, 쉼표 사이는 칸이 된다. 이 순간에는 아직 모든 칸이 글자다.", T(raw)),
        S("자료형 정하기", "숫자처럼 생긴 칸은 숫자로, parse_dates 로 지정한 date 는 날짜형으로 바뀐다.",
          T(book, hl=("date", "cost", "sales")), T(dt, index=True, title="book.dtypes")),
    ]
