from lib import *

CARD = dict(
    id="polyfit", ch="7. numpy 계산", cmd="np.polyfit · np.polyval",
    title="추세선 기울기 구하기", excel="추세선 / SLOPE · INTERCEPT",
    desc="polyfit(x, y, 1) 은 점들을 가장 잘 지나는 직선의 기울기와 절편을 준다. polyval(직선, 1450) 은 x = 1450 일 때 그 직선의 y 값이다. "
         "쇼핑몰의 월평균 원·달러 환율과 미국 주문 수로 본다(환율은 연습용 예시값). 같이 움직인다고 환율이 주문의 원인이라는 뜻은 아니다.",
    code='''import numpy as np
import matplotlib.pyplot as plt
rate = np.array([1455, 1440, 1460, 1430, 1395, 1365, 1375, 1385, 1390, 1405, 1430, 1460])   # 월평균 원/달러
us_orders = np.array([118, 110, 121, 104, 96, 88, 92, 95, 97, 101, 112, 124])            # 미국 주문 수
fit = np.polyfit(rate, us_orders, 1)          # [기울기, 절편]
print("slope:", round(float(fit[0]), 3), "/ intercept:", round(float(fit[1]), 1))
print("trend at 1450:", round(float(np.polyval(fit, 1450)), 1))

fig, ax = plt.subplots(figsize=(5, 3.4))
ax.scatter(rate, us_orders, color="#1F3A5F")
xs = np.array([rate.min(), rate.max()])
ax.plot(xs, np.polyval(fit, xs), color="#D98E22", linewidth=2, label="trend")
ax.set(title="KRW per USD vs US orders", xlabel="KRW per USD", ylabel="US orders")
ax.legend()
plt.show()''',
)

def stages(ns, out):
    pd = __import__("pandas")
    rate, y, fit = ns["rate"], ns["us_orders"], ns["fit"]
    t = pd.DataFrame({"month": range(1, 13), "rate": rate, "us_orders": y})
    lines = out.splitlines()
    tr = round(float(ns["np"].polyval(fit, 1450)), 1)
    return [
        S("점 열두 개", "월평균 환율(x)과 미국 주문 수(y). 원화가 약할 때(환율이 높을 때) 주문이 많아 보인다.", T(t.astype(object))),
        S("polyfit(x, y, 1)", f"점들 사이를 지나는 직선: y = 기울기 × x + 절편. 환율이 1원 오를 때 주문이 약 {fit[0]:.2f}건 늘어나는 기울기다.",
          IMG("polyfit"), TX(lines[0], "out", "출력")),
        S("polyval(fit, 1450)", f"직선 위 x = 1450 의 높이. 추세값 {tr}건. 추세는 '같이 움직인다'는 뜻일 뿐, 원인은 따로 따져 봐야 한다.",
          TX(lines[1], "out", "출력")),
    ]
