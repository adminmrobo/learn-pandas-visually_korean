from lib import *

CARD = dict(
    id="axhline", ch="8. 차트 그리기", cmd="ax.axhline()",
    title="기준선 하나 긋기", excel="목표선 계열 추가",
    desc="axhline(y) 는 그 높이에 가로선을 긋는다. 쇼핑몰이 해외 손님용 달러 가격을 $0.50 단위로 반올림해 붙이면, "
         "실제 환산가보다 조금 비싸거나 싸진다. 그 차이를 원화로 바꿔 막대로 그리고 0 에 기준선을 그으면 "
         "어느 상품이 위(더 받음)·아래(덜 받음)인지 바로 보인다.",
    code='''import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

rate = 1455.9                                     # 원·달러 환율(예시값)
tag = pd.DataFrame({"item": ["Tee", "Cap", "Shirt", "Knit", "Denim", "Coat"],
                    "price_krw": [19000, 25000, 39000, 52000, 89000, 159000]})
tag["usd_exact"] = (tag["price_krw"] / rate).round(2)
tag["usd_tag"] = (tag["price_krw"] / rate * 2).round() / 2      # $0.50 단위 반올림
tag["diff_krw"] = ((tag["usd_tag"] - tag["price_krw"] / rate) * rate).round(0)
print(tag)
ax = sns.barplot(data=tag, x="item", y="diff_krw", color="#028090")
ax.axhline(0, color="#D98E22", ls="--", label="Exact price")
ax.bar_label(ax.containers[0], fmt="%.0f", fontsize=8)
ax.set(title="Rounded USD tag vs exact price", xlabel="Item", ylabel="Difference (KRW)")
ax.legend()
plt.show()''',
    talk=[dict(who="robo", state="confused", text="삐빅, 반올림했더니 어떤 옷은 더 받고 어떤 옷은 덜 받아.")],
)

def stages(ns, out):
    t = ns["tag"]
    up = ", ".join(t.loc[t.diff_krw > 0, "item"]); dn = ", ".join(t.loc[t.diff_krw < 0, "item"])
    return [
        S("가격표 계산", f"usd_exact = 원화 ÷ {ns['rate']}. usd_tag 는 $0.50 단위로 반올림한 값이다.",
          T(t[["item", "price_krw", "usd_exact", "usd_tag"]], hl=("usd_tag",))),
        S("차이를 원화로", "diff_krw = (붙인 달러 − 실제 달러) × 환율. 양수면 손님이 조금 더 낸다.",
          T(t[["item", "diff_krw"]], hl=("diff_krw",), rcls=["ok" if v >= 0 else "bad" for v in t.diff_krw])),
        S("막대 + 기준선", f"점선 0 위는 {up}, 아래는 {dn}. 차이는 많아야 {int(t.diff_krw.abs().max())}원이다.",
          CH(type="bar", title="Rounded USD tag vs exact price", xlabel="Item", ylabel="Difference (KRW)", cats=list(t["item"]),
             series=[dict(name="", values=[float(v) for v in t["diff_krw"]], c="#028090")], labels=1,
             hline=dict(y=0, label="Exact price", c="#D98E22"))),
    ]
