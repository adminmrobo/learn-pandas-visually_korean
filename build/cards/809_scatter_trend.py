from lib import *

CARD = dict(
    id="scatter_trend", ch="8. 차트 그리기", cmd="sns.scatterplot(hue=) + 추세선",
    title="점 찍고 추세선 긋기", excel="분산형 차트 + 추세선",
    desc="scatterplot 은 점 하나에 한 줄(하루 · 나라)을 찍는다. hue 로 나라별 색을 나누고, 나라마다 polyfit 으로 구한 직선을 "
         "ax.plot 으로 덧그린다. 의류 쇼핑몰의 해외 주문 수와 그날 원·달러 환율을 놓고 본다. 두 값이 같이 움직여도 "
         "환율이 주문을 만든 원인이라고 바로 말할 수는 없다.",
    code='''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 영업일 6일 × 나라 2곳: 그날 원·달러 환율(예시값)과 해외 주문 수
days = pd.DataFrame({"country": ["US", "JP"] * 6,
                     "usdkrw": [1441.0, 1441.0, 1447.5, 1447.5, 1452.3, 1452.3, 1458.8, 1458.8, 1466.5, 1466.5, 1471.2, 1471.2],
                     "orders": [12, 9, 14, 8, 15, 10, 18, 9, 19, 11, 22, 10]})
fit = {k: np.polyfit(d["usdkrw"], d["orders"], 1) for k, d in days.groupby("country")}
print("trend at 1460:", {k: round(float(np.polyval(f, 1460)), 1) for k, f in fit.items()})
ax = sns.scatterplot(data=days, x="usdkrw", y="orders", hue="country", alpha=0.7, palette={"US": "#1F3A5F", "JP": "#D98E22"})
x = np.linspace(1440, 1472, 50)
for k, c in [("US", "#1F3A5F"), ("JP", "#D98E22")]:
    ax.plot(x, np.polyval(fit[k], x), color=c)
ax.set(title="Overseas orders vs USD/KRW", xlabel="USD/KRW", ylabel="Orders per day")
plt.show()''',
)

def stages(ns, out):
    import numpy as np
    d = ns["days"]; fit = ns["fit"]
    us, jp = d[d.country == "US"], d[d.country == "JP"]
    t = {k: round(float(np.polyval(f, 1460)), 1) for k, f in fit.items()}
    slope = {k: float(f[0]) * 10 for k, f in fit.items()}
    lines = [dict(x=[1440, 1472], y=[float(np.polyval(fit[k], 1440)), float(np.polyval(fit[k], 1472))], c=i) for i, k in enumerate(["US", "JP"])]
    return [
        S("주문 기록", "하루 × 나라마다 한 줄. 환율은 그날 종가 예시값이다.", T(d, rcls=["g0" if c == "US" else "g1" for c in d.country])),
        S("나라로 나눠 직선 맞추기", "groupby(\"country\") 조각마다 polyfit 으로 기울기와 절편을 구한다.",
          T(us, rcls=["g0"] * len(us)), T(jp, rcls=["g1"] * len(jp))),
        S("점 + 선", f"환율 1460 에서 추세값은 US {t['US']}건, JP {t['JP']}건. 환율이 10원 오를 때 US 선은 {slope['US']:.1f}건, JP 선은 {slope['JP']:.1f}건 움직인다.",
          CH(type="scatter", title="Overseas orders vs USD/KRW", xlabel="USD/KRW", ylabel="Orders per day",
             names=["US", "JP"], colors=["#1F3A5F", "#D98E22"],
             points=[dict(x=float(r.usdkrw), y=float(r.orders), g=0 if r.country == "US" else 1) for r in d.itertuples()],
             lines=lines)),
    ]
