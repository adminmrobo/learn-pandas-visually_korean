"""Canonical example data. Paste these strings into card code so every card is self-contained
and the same store looks the same everywhere. Money unit for Koi book: KRW thousand (천원)."""

# 카페 Koi 장부 8줄 (원래 journal 'j' 자리). cost = 나간 돈, sales = 들어온 돈, 천원 단위.
KOI = '''import pandas as pd
book = pd.DataFrame({
    "date": pd.to_datetime(["2025-04-01", "2025-04-01", "2025-04-01", "2025-04-02",
                            "2025-05-03", "2025-05-04", "2025-05-10", "2025-05-11"]),
    "item":  ["Coffee", "Milk", "Coffee", "Coffee", "Rent", "Dessert", "Broken cup", "Coffee"],
    "cost":  [0.0, 22.3, 0.0, 0.0, 241.9, 0.0, 8.1, 0.0],
    "sales": [9.4, 0.0, 82.0, 82.3, 0.0, 35.0, 0.0, 60.0],
    "customer": ["Regular", None, "Walk-in", "Walk-in", None, "Tourist", None, "Regular"],
    "month": [4, 4, 4, 4, 5, 5, 5, 5],
})'''

# Koi 장부 item -> 분류 사전. 'Broken cup' 은 일부러 빠져 있다 (map 하면 NaN).
KOI_KIND = '''kind = {"Coffee": "Sales", "Dessert": "Sales", "Milk": "Cost", "Rent": "Cost"}'''

# 동네 편의점 결제 기록 (생성). 4주(2025-03-03 월 ~ 03-30 일), 420건, 원 단위.
CVS = '''import numpy as np
import pandas as pd
rng = np.random.default_rng(7)
n = 420
w = np.array([2, 1, 1, 1, 1, 1, 2, 6, 8, 5, 4, 5, 8, 7, 4, 4, 5, 6, 8, 9, 7, 5, 4, 3])   # 시간대별 손님 비중
hour = rng.choice(np.arange(24), n, p=w / w.sum())
cvs = pd.DataFrame({
    "time": pd.Timestamp("2025-03-03") + pd.to_timedelta(rng.integers(0, 28, n), unit="D") + pd.to_timedelta(hour, unit="h")
            + pd.to_timedelta(rng.integers(0, 60, n), unit="min"),
    "category": rng.choice(["Snack", "Drink", "Lunchbox", "Ramen", "Ice cream"], n, p=[.3, .3, .15, .15, .1]),
    "pay": rng.choice(["Card", "Cash", "Mobile"], n, p=[.6, .1, .3]),
})
base = cvs["category"].map({"Snack": 2500, "Drink": 2000, "Lunchbox": 5500, "Ramen": 1800, "Ice cream": 2200})
cvs["amount"] = (base * rng.integers(1, 5, n) * rng.uniform(0.8, 1.6, n) / 100).round() * 100
cvs = cvs.sort_values("time").reset_index(drop=True)'''

# 의류 쇼핑몰 해외 주문 6줄. price_krw = 원화 정가. brand 이름 끝 공백은 일부러 넣은 함정.
SHOP = '''import pandas as pd
orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104, 105, 106],
    "date": pd.to_datetime(["2025-01-02", "2025-01-03", "2025-01-04", "2025-01-06", "2025-01-07", "2025-01-08"]),
    "brand":    ["Mono", "Linen ", "Denimo", "Mono", "Linen ", "Denimo"],
    "country":  ["US", "JP", "CN", "US", "KR", "JP"],
    "currency": ["USD", "JPY", "CNY", "USD", "KRW", "JPY"],
    "price_krw": [39000, 52000, 89000, 45000, 52000, 39000],
})'''

# yfinance 모양의 환율 표 (2025-01-02 ~ 01-08 영업일 5일). 값은 연습용 예시값이다.
# 실제로는 yf.download(["USDKRW=X", "JPYKRW=X", "CNYKRW=X"], start="2025-01-02", end="2025-01-09")
FX = '''import pandas as pd
dates = pd.to_datetime(["2025-01-02", "2025-01-03", "2025-01-06", "2025-01-07", "2025-01-08"])
fx = pd.DataFrame({
    ("Close", "CNYKRW=X"): [200.6, 200.9, 199.4, 198.8, 199.5],
    ("Close", "JPYKRW=X"): [9.34, 9.37, 9.29, 9.25, 9.27],
    ("Close", "USDKRW=X"): [1466.5, 1470.2, 1460.8, 1452.3, 1455.9],
}, index=dates)
fx.columns.names = ["Price", "Ticker"]
fx.index.name = "Date"'''
