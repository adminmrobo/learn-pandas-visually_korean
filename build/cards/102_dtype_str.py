from lib import *

CSV = """item,code,stock
Linen shirt,00731,12
Denim jacket,00732,5"""

CARD = dict(
    id="dtype_str", ch="1. 불러오기와 살펴보기", cmd='dtype={"code": str}',
    title="앞자리 0 을 지키며 읽기", excel="셀 서식을 '텍스트'로",
    desc="쇼핑몰 상품코드 00731 은 숫자가 아니라 이름표다. 그냥 읽으면 pandas 가 숫자로 바꾸면서 앞의 0 이 사라진다. "
         "dtype 으로 그 열만 글자(str)로 읽으라고 알려 준다.",
    code='''import pandas as pd
import io
csv_text = """''' + CSV + '''"""
a = pd.read_csv(io.StringIO(csv_text))                       # 그냥 읽기
b = pd.read_csv(io.StringIO(csv_text), dtype={"code": str})  # code 열만 글자로
print(a)
print(b)
print("length of code:", len(b["code"].iloc[0]))''',
    tip='상품코드·우편번호·전화번호처럼 0 으로 시작할 수 있는 열은 처음부터 dtype={"열이름": str} 로 읽는다.',
)

def stages(ns, out):
    a, b = ns["a"], ns["b"]
    return [
        S("CSV 파일", "code 칸은 5자리이고 앞에 0 이 두 개 붙어 있다.", TX(CSV, "code", "shop_items.csv")),
        S("두 가지로 읽기",
          f'위는 숫자로 읽혀 0 이 사라졌다({a["code"].iloc[0]}). 아래는 dtype={{"code": str}} 덕분에 {len(b["code"].iloc[0])}자리 그대로다.',
          T(a, hl=("code",), title="그냥 읽기 a"), T(b, hl=("code",), title='dtype={"code": str} b'), links=[[0, 0], [0, 1]]),
    ]
