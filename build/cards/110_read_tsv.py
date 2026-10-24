from lib import *

TEXT = "Mon\tRamen 24, Drink 30, Lunchbox 12\nTue\tRamen 18, Drink 36, Lunchbox 10"

CARD = dict(
    id="read_tsv", ch="1. 불러오기와 살펴보기", cmd='read_csv(sep="\\t", header=None, names=)',
    title="탭으로 나뉜 메모 읽기", excel="텍스트 나누기(탭)",
    desc="칸 경계가 쉼표가 아니라 탭(\\t)이면 sep=\"\\t\" 를 준다. 첫 줄이 열 이름이 아니면 header=None 으로 막고, names 로 열 이름을 직접 붙인다. "
         "예시는 편의점 점장이 남긴 요일별 발주 메모다. 메모 안의 쉼표는 탭이 아니라서 칸을 나누지 않는다.",
    code='''import pandas as pd
import io
text = "''' + TEXT.replace("\t", "\\t").replace("\n", "\\n") + '''"
memo = pd.read_csv(io.StringIO(text), sep="\\t", header=None, names=["day", "order"])
print(memo)''',
)

def stages(ns, out):
    memo = ns["memo"]
    return [
        S("메모 파일", "⇥ 표시가 탭 문자다. 첫 줄도 데이터라 열 이름이 없다.", TX(TEXT.replace("\t", " ⇥ "), "code", "cvs_order_memo.txt")),
        S("탭으로 자르고 이름 붙이기", "탭 앞은 day, 뒤는 order 칸. header=None 덕분에 첫 줄도 데이터로 남고, 메모 속 쉼표는 그대로 글자로 남는다.",
          T(memo, hl=("day", "order"))),
    ]
