from lib import *
from snippets import FX

CARD = dict(
    id="yf_download", ch="1. 불러오기와 살펴보기", cmd="yf.download()",
    title="환율을 표로 받아 오기", excel="데이터 가져오기(웹)",
    desc="yfinance 의 yf.download 는 티커(USDKRW=X = 1달러가 몇 원인지)와 기간을 주면 날짜별 시세를 표로 돌려준다. "
         "열은 (Price, Ticker) 두 층으로 된 MultiIndex 이고, 외환시장이 쉬는 토·일 날짜는 표에 없다. "
         "yfinance 는 공식 API 가 아니라서 막히거나 형식이 바뀔 수 있으니, 실패하면 저장해 둔 값으로 넘어가게 짠다.",
    code='''# !pip install yfinance        # Colab 에 없으면 먼저 한 번 실행
USE_LIVE = False                # True 로 바꾸면 인터넷에서 실제 환율을 받는다
''' + FX + '''                  # ← 연습용 예시값 (yfinance 가 막혀도 실습이 이어지게)
if USE_LIVE:
    try:
        import yfinance as yf
        live = yf.download(["USDKRW=X", "JPYKRW=X", "CNYKRW=X"],
                           start="2025-01-02", end="2025-01-09", progress=False)
        if live.empty:
            print("empty reply → 예시값 사용")
        else:
            fx = live[["Close"]].round(2)
    except Exception as e:
        print("download failed →", e)
print(fx)
print(fx.columns.tolist())
print("days:", len(fx), "| weekdays:", fx.index.day_name().str[:3].tolist())''',
    tip='USE_LIVE = True 로 바꾸면 실제 값이 들어와 숫자가 이 페이지와 조금 다르다. 받은 표는 fx.to_csv("fx_backup.csv") 로 바로 저장해 두면 다음에 막혀도 쓸 수 있다.',
    talk=[
        dict(who="asst", text="달러로 얼마예요? 하고 물으면 환율은 어디서 구해요?"),
        dict(who="doc", text="yfinance 로 날짜별 환율을 표로 받아 볼까요?"),
    ],
)

def stages(ns, out):
    fx = ns["fx"]
    flat = fx.copy(); flat.columns = [t for _, t in fx.columns]
    hdr = RAW(["Price", "Close", "Close", "Close"], [["Ticker", *[t for _, t in fx.columns]]], title="열 이름 두 층",
              ccls=["ix", "hl", "hl", "hl"], cls=[["ix", "hl", "hl", "hl"]])
    days = fx.index.day_name().str[:3].tolist()
    cal = RAW(["date", "day", "in fx?"],
              [[d.strftime("%m-%d"), d.day_name()[:3], "yes" if d in fx.index else "no"] for d in __import__("pandas").date_range(fx.index[0], fx.index[-1])],
              rcls=["" if d in fx.index else "bad" for d in __import__("pandas").date_range(fx.index[0], fx.index[-1])], title="달력")
    return [
        S("요청", "티커 세 개와 기간을 보낸다. USDKRW=X 는 1달러가 몇 원인지, JPYKRW=X 는 1엔이 몇 원인지다.",
          TX('yf.download(["USDKRW=X", "JPYKRW=X", "CNYKRW=X"],\n            start="2025-01-02", end="2025-01-09")', "code", "보내는 것")),
        S("받은 표", f"날짜가 행, 티커가 열이다. 열 이름이 Price(Close) 와 Ticker 두 층으로 쌓여 있다.",
          T(flat, index=True, ix_name="Date"), hdr),
        S("빠진 날", f"{len(fx)}일만 왔다. 01-04(토)·01-05(일)는 시장이 쉬어 줄이 없다. 이 빈 날은 2장 ffill 에서 채운다.", cal),
    ]
