from lib import *

CARD = dict(
    id="first_digit", ch="2. 청소하기", cmd="astype(str).str.lstrip().str[0]",
    title="금액의 첫 자리 숫자 뽑기", excel="LEFT(TEXT())",
    desc="영수증 금액의 첫 자리가 1~9 중 무엇인지 세면 벤포드 검사를 할 수 있다. 숫자를 글자로 바꾸고(astype(str)), 앞의 '0' 과 '.' 을 벗겨 낸 뒤(lstrip(\"0.\")), "
         "첫 글자를 집고(str[0]), 다시 숫자로 바꾼다(astype(int)). 예시는 편의점 결제 금액(천원)이다.",
    code='''import pandas as pd
amt = pd.Series([12.6, 2.0, 0.6, 135.0, 3.4])   # 편의점 결제 금액(천원)
t1 = amt.astype(str)              # 숫자 → 글자
t2 = t1.str.lstrip("0.")          # 앞쪽 0 과 . 벗기기 ('0.6' → '6')
t3 = t2.str[0]                    # 첫 글자
first = t3.astype(int)            # 다시 숫자
print(pd.DataFrame({"amount": amt, "str": t1, "lstrip": t2, "[0]": t3, "first": first}))''',
)

def stages(ns, out):
    import pandas as pd
    amt, t1, t2, t3, first = ns["amt"], ns["t1"], ns["t2"], ns["t3"], ns["first"]
    return [
        S("금액", "다섯 개의 결제 금액(천원).", T(amt.rename("amount").to_frame())),
        S("astype(str)", "숫자를 글자로 바꾼다. 이제 글자처럼 자를 수 있다.", T(pd.DataFrame({"amount": amt, "str": t1}), hl=("str",))),
        S('lstrip("0.")', f"왼쪽 끝의 0 과 . 을 벗긴다. 0.6 의 첫 자리는 {first.iloc[2]}이다.",
          T(pd.DataFrame({"str": t1, "lstrip": t2}), hl=("lstrip",), rcls=["", "", "hr", "", ""])),
        S("str[0] → astype(int)", "첫 글자만 집어 숫자로 바꾼다.", T(pd.DataFrame({"lstrip": t2, "[0]": t3, "first": first}), hl=("first",))),
    ]
