from lib import *
from snippets import FX

CARD = dict(
    id="droplevel", ch="5. 합치고 모양 바꾸기", cmd='fx["Close"] · droplevel()',
    title="두 줄 열 이름 펴기", excel="두 줄 머리글을 한 줄로 합치기",
    desc="yfinance 의 yf.download 로 받은 표는 열 이름이 두 줄(Price, Ticker)이다. fx[\"Close\"] 처럼 윗줄 이름으로 꺼내면 아랫줄만 남은 표가 되고, "
         'columns.droplevel("Price") 는 윗줄을 지워 한 줄 열 이름으로 편다. 아래 환율은 연습용 예시값이다.',
    code=FX + '''
print(fx.columns.tolist())          # 열 이름이 (Price, Ticker) 두 겹
close = fx["Close"]                 # 윗줄 이름으로 꺼내기
print(close.head(2))
flat = fx.copy()
flat.columns = flat.columns.droplevel("Price")   # 윗줄 지우기
print(flat.columns.tolist())
print(flat["USDKRW=X"].head(2))''',
    tip='실제로는 import yfinance as yf 후 fx = yf.download(["USDKRW=X", "JPYKRW=X", "CNYKRW=X"], start="2025-01-02", end="2025-01-09") 로 받는다. 받자마자 fx.columns 를 출력해 두 겹인지 먼저 확인한다.',
)

def stages(ns, out):
    fx, close, flat = ns["fx"], ns["close"], ns["flat"]
    h = fx.head(2)
    top = RAW(["Price →"] + [p for p, _ in h.columns] , [["Ticker →"] + [t for _, t in h.columns]] +
              [[f"{d:%Y-%m-%d}"] + [str(v) for v in r] for d, r in zip(h.index, h.values)],
              ccls=["ix"] + ["hl"] * h.shape[1], rcls=["hr", "", ""])
    cols = [l for l in out.splitlines() if l.startswith("[")]
    return [
        S("두 줄 열 이름", "열 이름 위에 Close, 아래에 통화 코드가 있다. 열 하나의 진짜 이름은 ('Close', 'USDKRW=X') 같은 짝이다.",
          top, TX(cols[0], "out", "fx.columns.tolist()")),
        S('fx["Close"]', "윗줄 이름 Close 로 꺼내면 아랫줄(통화)만 열 이름으로 남는다.",
          T(close.head(2), index=True, ix_name="Date"), links=[[0, 0]]),
        S('droplevel("Price")', '표는 그대로 두고 윗줄만 지운다. 이제 flat["USDKRW=X"] 처럼 한 번에 꺼낸다.',
          TX(cols[1], "out", "flat.columns.tolist()"), T(flat["USDKRW=X"].head(2), index=True, ix_name="Date")),
    ]
