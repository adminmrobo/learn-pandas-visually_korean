from lib import *
from snippets import SHOP

CARD = dict(
    id="val_strip", ch="2. 청소하기", cmd="s.str.strip() · map(repr)",
    title="값 끝에 숨은 공백 찾기", excel="TRIM",
    desc="열 이름뿐 아니라 값에도 공백이 숨는다. 쇼핑몰 주문의 'Linen ' 은 'Linen' 과 다른 글자라서 사전 찾기(map)나 merge 에서 짝을 못 찾는다. "
         "map(repr) 로 따옴표를 씌워 보면 공백이 드러나고, str.strip() 으로 지운다.",
    code=SHOP + '''
b = orders["brand"]
print(b.map(repr).tolist())          # 따옴표로 감싸 공백을 드러낸다
print((b == "Linen").tolist())       # 'Linen ' 은 False
b = b.str.strip()
print((b == "Linen").tolist())       # 이제 Linen 두 줄이 True''',
    talk=[dict(who="asst", text="화면에선 똑같이 Linen 인데 왜 False 예요?")],
)

def stages(ns, out):
    import pandas as pd
    o = ns["orders"]; raw = o["brand"]; clean = ns["b"]
    shown = raw.map(lambda v: repr(v).replace(" ", "␣"))
    before = raw == "Linen"; after = clean == "Linen"
    lin = [i for i, v in enumerate(raw) if v.strip() == "Linen"]
    return [
        S("원본 값", f"map(repr) 로 따옴표를 씌우면 {', '.join(str(i)+'번' for i in lin)} 값 끝의 공백(␣)이 보인다.",
          T(pd.DataFrame({"brand": raw, "repr": shown}), cls={(i, "repr"): "ws" for i in lin}, rcls=["hr" if i in lin else "" for i in range(len(o))])),
        S('== "Linen"', "같은 브랜드인데 Linen 줄이 모두 False 다.",
          T(pd.DataFrame({"brand": shown, '== "Linen"': before}), cls={(i, '== "Linen"'): ("t" if v else "f") for i, v in enumerate(before)})),
        S("str.strip()", f"앞뒤 공백을 지우면 Linen 두 줄이 True 가 된다(True {int(after.sum())}개).",
          T(pd.DataFrame({"brand": clean.map(repr), '== "Linen"': after}), cls={(i, '== "Linen"'): ("t" if v else "f") for i, v in enumerate(after)}, hl=("brand",))),
    ]
