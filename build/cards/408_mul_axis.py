from lib import *
import pandas as pd

CARD = dict(
    id="mul_axis", ch="4. 새 열 만들기", cmd="df[cols].mul(배수, axis=0)",
    title="줄마다 다른 단위 맞추기", excel="단위 환산 열 곱하기",
    desc="AI 가 만든 외화 가격표에서 엔(JPY)만 '100엔당 원'으로 적혀 있다. unit 열을 사전으로 '곱할 배수'로 바꾸고(map), "
         "숫자 열 여러 개에 줄마다 그 배수를 곱해 모두 '1단위당 원'으로 맞춘다. axis=0 은 '줄 방향으로 하나씩 대응해 곱하라'는 뜻이다.",
    code='''import pandas as pd
tag = pd.DataFrame({"currency": ["USD", "JPY", "CNY"],
                    "rate_open": [1466.5, 934.0, 200.6], "rate_close": [1455.9, 927.0, 199.5],
                    "unit": ["1", "100", "1"]})               # JPY 는 100엔 기준으로 적혀 있다
to_one = {"1": 1, "100": 0.01}                               # 1단위당 원으로 바꿀 배수
factor = tag["unit"].map(to_one)
num = ["rate_open", "rate_close"]
tag[num] = tag[num].mul(factor, axis=0)
tag["unit"] = "1"
print(tag)''',
)

def stages(ns, out):
    t = ns["tag"]
    raw = pd.DataFrame({"currency": ["USD", "JPY", "CNY"], "rate_open": [1466.5, 934.0, 200.6],
                        "rate_close": [1455.9, 927.0, 199.5], "unit": ["1", "100", "1"]})
    f = raw[["currency", "unit"]].copy(); f["factor"] = ns["factor"]
    return [
        S("단위가 섞인 표", "USD·CNY 는 1단위당 원, JPY 만 100엔당 원으로 적혀 있다.", T(raw, rcls=["", "hr", ""])),
        S("unit → 배수", "사전으로 단위를 '1단위당 원으로 바꿀 때 곱할 수'로 바꾼다.", T(f, hl=("factor",))),
        S("mul(axis=0)", f"줄마다 자기 배수를 곱한다. JPY 는 {raw['rate_open'][1]:g} → {t['rate_open'][1]:g} 원. 이제 모두 1단위당 원.",
          T(t, hl=("rate_open", "rate_close"))),
    ]
