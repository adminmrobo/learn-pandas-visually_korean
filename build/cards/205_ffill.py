from lib import *
from snippets import FX

CARD = dict(
    id="ffill", ch="2. 청소하기", cmd="reindex(date_range) · ffill()",
    title="주말엔 환율이 없다", excel="빈 셀을 위 값으로 채우기(Ctrl+D)",
    desc="외환시장은 토·일에 쉬어서 환율 표에는 주말 줄이 없다. 그런데 쇼핑몰 주문은 토요일에도 들어온다. "
         "pd.date_range 로 빠짐없는 달력을 만들어 reindex 하면 빈 날이 NaN 으로 생기고, ffill() 이 바로 위(금요일) 값으로 채운다.",
    code=FX + '''
usd = fx[("Close", "USDKRW=X")].rename("USDKRW")          # 달러 환율 한 열만
days = pd.date_range("2025-01-02", "2025-01-08", freq="D")  # 토·일까지 빠짐없는 달력
cal = usd.reindex(days)                                     # 없는 날은 NaN
filled = cal.ffill()                                        # 앞(금요일) 값으로 채우기
print(pd.DataFrame({"day": days.day_name().str[:3], "reindex": cal, "ffill": filled}))''',
    tip="ffill 은 '마지막으로 알려진 값'을 쓰는 규칙이다. 주말 주문에 금요일 환율을 쓴다고 정한 것이므로, 가게 규칙이 다르면(예: 월요일 환율) bfill() 을 쓴다.",
    talk=[dict(who="fly", text="토요일 주문은 무슨 환율로 계산해?")],
)

def stages(ns, out):
    import pandas as pd
    usd, days, cal, filled = ns["usd"], ns["days"], ns["cal"], ns["filled"]
    d1 = usd.to_frame(); d1.insert(0, "day", usd.index.day_name().str[:3])
    t = pd.DataFrame({"day": days.day_name().str[:3], "reindex": cal}, index=days)
    t2 = pd.DataFrame({"day": days.day_name().str[:3], "ffill": filled}, index=days)
    wk = ["bad" if v != v else "" for v in cal]
    fri = filled.loc["2025-01-03"]
    return [
        S("받은 환율", f"영업일 {len(usd)}일뿐이다. 01-03(금) 다음 줄이 바로 01-06(월)이다.", T(d1, index=True, ix_name="Date")),
        S("reindex(달력)", f"7일짜리 달력에 맞추면 토·일 두 줄이 NaN 으로 생긴다.", T(t, index=True, ix_name="Date", rcls=wk, hl=("reindex",))),
        S("ffill()", f"NaN 칸을 바로 위 값으로 채운다. 토·일 모두 금요일 환율 {fri} 이 들어갔다.",
          T(t2, index=True, ix_name="Date", rcls=["hr" if r else "" for r in wk], hl=("ffill",))),
    ]
