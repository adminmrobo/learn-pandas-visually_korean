from lib import *
from snippets import CVS

CARD = dict(
    id="benford", ch="7. numpy 계산", cmd="np.arange · np.log10",
    title="벤포드 이론값 계산", excel="=LOG10(1+1/A2)",
    desc="np.arange(1, 10) 은 1부터 9까지의 숫자 배열이다. 배열에 수식을 쓰면 원소마다 한꺼번에 계산된다. "
         "벤포드 법칙에서 첫 자리가 d 일 확률은 log10(1 + 1/d) 이다. 편의점 영수증 금액의 첫 자리와 나란히 놓아 본다.",
    code=CVS + '''
d = np.arange(1, 10)                         # [1 2 3 ... 9]
ben = pd.Series(np.log10(1 + 1 / d), index=d)
first = cvs["amount"].astype(int).astype(str).str[0].astype(int)     # 영수증 금액의 첫 자리
obs = first.value_counts(normalize=True).sort_index()
cmp = pd.DataFrame({"observed%": obs * 100, "benford%": ben * 100}).round(1)
print(cmp)
print("total:", round(ben.sum(), 6))''',
    talk=[
        dict(who="asst", text="영수증 금액은 첫 자리가 1인 게 제일 많다는데 왜요?"),
        dict(who="doc", text="숫자가 커질 때 1로 시작하는 구간을 가장 오래 지나요. 계산해 볼까요?"),
    ],
)

def stages(ns, out):
    np = ns["np"]
    d, ben, cmp = ns["d"], ns["ben"], ns["cmp"]
    step = __import__("pandas").DataFrame({"d": d, "1 + 1/d": (1 + 1 / d).round(3)})
    pct = (ben * 100).round(1).rename("benford%").to_frame()
    c = cmp.fillna(0)
    return [
        S("np.arange(1, 10)", "1 부터 9 까지(10 은 빠진다). 배열 하나에 숫자 아홉 개.", TX(str(d), "out", "d")),
        S("1 + 1/d", "원소마다 한꺼번에 계산된다. 1 → 2.0, 2 → 1.5 …", T(step.astype(object))),
        S("log10 × 100", f"로그를 취하면 확률이 된다. 1 이 {pct.loc[1, 'benford%']}%, 9 는 {pct.loc[9, 'benford%']}%. 다 더하면 1.",
          T(pct, index=True, ix_name="d", hl=("benford%",))),
        S("영수증과 비교", f"편의점 영수증 {len(ns['cvs'])}건의 첫 자리 비율과 나란히 놓는다. 1 은 {c.loc[1, 'observed%']}%. "
          "편의점은 금액대가 좁아 벤포드와 꼭 같지는 않다. 차이가 크면 왜인지 들여다볼 신호다.",
          CH(type="bar", title="First digit (%)", xlabel="First digit", cats=[str(i) for i in c.index],
             series=[{"name": "Receipts", "values": [float(v) for v in c["observed%"]], "c": "#4472C4"},
                     {"name": "Benford", "values": [float(v) for v in c["benford%"]], "c": "#D98E22"}])),
    ]
