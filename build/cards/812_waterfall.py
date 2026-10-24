from lib import *

CARD = dict(
    id="waterfall", ch="8. 차트 그리기", cmd="ax.bar(bottom=)",
    title="떠 있는 막대로 폭포 그리기", excel="폭포 차트",
    desc="ax.bar 의 bottom 은 막대가 시작하는 높이다. 기초 재고는 0 에서, 입고는 기초 꼭대기에서 위로, 사용과 폐기는 "
         "줄어든 높이에서 위로 그리면 막대들이 계단처럼 이어진다. 카페 Koi 의 한 달 원두 재고(kg)로 "
         "8.0 + 20.0 − 16.5 − 1.2 = 10.3 을 그린다.",
    code='''import matplotlib.pyplot as plt
q = {"opening": 8.0, "in": 20.0, "used": 16.5, "waste": 1.2}
q["closing"] = q["opening"] + q["in"] - q["used"] - q["waste"]
print("closing:", round(q["closing"], 1), "kg")
labels = ["Opening", "In", "Used", "Waste", "Closing"]
top = q["opening"] + q["in"]
bottom = [0, q["opening"], top - q["used"], top - q["used"] - q["waste"], 0]
height = [q["opening"], q["in"], q["used"], q["waste"], q["closing"]]
fig, ax = plt.subplots(figsize=(6.5, 3.5))
bars = ax.bar(labels, height, bottom=bottom, color=["#1F3A5F", "#028090", "#D98E22", "#C9382A", "#1F3A5F"])
ax.bar_label(bars, labels=[f"{v:+.1f}" if i in (1, 2, 3) else f"{v:.1f}"
                           for i, v in enumerate([q["opening"], q["in"], -q["used"], -q["waste"], q["closing"]])])
ax.margins(y=0.15)
ax.set(title="Cafe Koi coffee beans, April (kg)")
plt.show()''',
    talk=[dict(who="fly", text="버린 원두 1.2kg 도 빠짐없이 들어갔어?")],
)

def stages(ns, out):
    import pandas as pd
    tb = pd.DataFrame({"bar": ns["labels"], "bottom": ns["bottom"], "height": ns["height"]})
    tb["top"] = tb["bottom"] + tb["height"]
    tb = tb.round(1)
    q = ns["q"]
    return [
        S("bottom 과 height", f"막대마다 시작 높이(bottom)와 길이(height). 사용(Used)은 {tb.loc[2, 'bottom']} 에서 시작해 {q['used']} 만큼 올라간다.",
          T(tb, hl=("bottom",))),
        S("떠 있는 막대", f"기초 {q['opening']} → +{q['in']} → −{q['used']} → −{q['waste']} → 기말 {q['closing']:.1f} 이 한 줄로 이어진다.",
          IMG("waterfall")),
    ]
