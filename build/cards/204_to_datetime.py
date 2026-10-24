from lib import *

CARD = dict(
    id="to_datetime", ch="2. 청소하기", cmd='pd.to_datetime(errors="coerce")',
    title="날짜 글자를 날짜형으로", excel="DATEVALUE",
    desc="'2025-01-06' 같은 글자를 날짜형으로 바꿔야 날짜끼리 빼서 배송에 며칠 걸렸는지 셀 수 있다. "
         "날짜가 아닌 '-' 가 섞여 있으면 errors=\"coerce\" 로 NaT(날짜용 빈칸)로 만든다. 예시는 쇼핑몰 주문의 배송 완료일이다.",
    code='''import pandas as pd
d = pd.Series(["2025-01-06", "2025-01-09", "-", None])     # 아직 배송 중이면 '-' 나 빈칸
delivered = pd.to_datetime(d, errors="coerce")            # '-' 와 None 은 NaT
print(delivered)
print("missing:", delivered.isna().sum())''',
)

def stages(ns, out):
    d, dl = ns["d"], ns["delivered"]
    return [
        S("배송 완료일 글자", "날짜 두 개, '-' 하나, 빈칸 하나.", T(d.rename("delivered (text)").to_frame())),
        S("pd.to_datetime", "날짜는 datetime64 로, 나머지는 NaT 가 된다. NaT 는 날짜 열의 NaN 이다.",
          T(dl.rename("delivered").to_frame(), hl=("delivered",), rcls=["", "", "bad", "bad"])),
        S("빈칸 세기", f"NaT 도 isna() 로 센다. 아직 배송이 안 끝난 주문이 {int(dl.isna().sum())}건이다.", TX(out.splitlines()[-1], "out", "출력")),
    ]
