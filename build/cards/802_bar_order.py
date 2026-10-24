from lib import *

CARD = dict(
    id="bar_order", ch="8. 차트 그리기", cmd="order= · ax.bar_label() · plt.xticks(rotation=)",
    title="막대 순서 정하고 값 적기", excel="데이터 레이블 · 정렬",
    desc="order 에 순서 목록을 주면 막대가 그 순서로 선다. 합계 큰 순서를 미리 계산해 넘기는 것이 요령이다. "
         "ax.bar_label 은 막대 끝에 값을 적고, xticks(rotation=45) 는 x 축 글자를 기울여 겹치지 않게 한다. "
         "예시는 의류 쇼핑몰의 브랜드별 주문 금액이다.",
    code='''import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 의류 쇼핑몰 주문 9건 (천원)
orders = pd.DataFrame({"brand": ["Mono", "Linen", "Linen", "Denimo", "Linen", "Denimo", "Knitly", "Denimo", "Mono"],
                       "sales_k": [39, 52, 45, 89, 52, 79, 129, 65, 45]})
order = orders.groupby("brand")["sales_k"].sum().sort_values(ascending=False).index
print(list(order))
ax = sns.barplot(data=orders, x="brand", y="sales_k", order=order, estimator="sum", errorbar=None, color="#028090")
ax.bar_label(ax.containers[0], fmt="%.0f", fontsize=8)
ax.set(title="Sales by brand (sum)", xlabel="Brand", ylabel="KRW thousand")
plt.xticks(rotation=45)
plt.show()''',
)

def stages(ns, out):
    o = ns["orders"]; order = list(ns["order"])
    sm = o.groupby("brand")["sales_k"].sum().sort_values(ascending=False).rename("sum").reset_index()
    top = sm.iloc[0]
    return [
        S("주문 명세", "브랜드마다 주문이 여러 건이다.", T(o)),
        S("합계 → 순서", f"groupby 합계를 큰 순서로 정렬하고 그 index 를 order 로 쓴다. 1등은 {top['brand']} {top['sum']}.",
          T(sm, hl=("sum",)), TX(str(order), "out", "order")),
        S("그리기", "order 순서로 서고, bar_label 이 막대 위에 합계를 적는다.",
          CH(type="bar", title="Sales by brand (sum)", xlabel="Brand", ylabel="KRW thousand", cats=order,
             series=[dict(name="", values=[float(v) for v in sm["sum"]], c="#028090")], labels=1, rot=1)),
    ]
