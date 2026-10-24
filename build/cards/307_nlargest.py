from lib import *
from snippets import CVS

CARD = dict(
    id="nlargest", ch="3. 고르고 거르기", cmd=".nlargest() · .drop()",
    title="가장 큰 몇 개, 그리고 빼 보기", excel="LARGE",
    desc="nlargest(2) 는 가장 큰 두 줄을 꺼낸다. 그 줄 번호(index)를 drop 에 넣으면 그 줄들을 뺀 나머지가 된다. "
         "편의점 결제 중 큰 몇 건이 평균을 얼마나 끌어올리는지 볼 때 쓴다.",
    code=CVS + '''
one_day = cvs[cvs["time"].dt.date == pd.Timestamp("2025-03-08").date()]["amount"].head(7).reset_index(drop=True)
print(one_day.tolist())
top2 = one_day.nlargest(2)
print(top2)
rest = one_day.drop(top2.index)
print("mean all:", round(one_day.mean()), "/ mean without top2:", round(rest.mean()))''',
)

def stages(ns, out):
    d, t2, r = ns["one_day"], ns["top2"], ns["rest"]
    idx = list(t2.index)
    return [
        S("편의점 결제 7건", "3월 8일 토요일 결제 일곱 건(원).", T(d, index=True, fmt=",.0f", rcls=["hr" if i in idx else "" for i in range(len(d))])),
        S("nlargest(2)", f"가장 큰 두 줄과 그 번호({', '.join(map(str, idx))})를 꺼낸다.", T(t2, index=True, fmt=",.0f", hl=("amount",))),
        S("drop(top2.index)", f"{'·'.join(map(str, idx))}번을 뺀 {len(r)}건. 평균이 {d.mean():,.0f} → {r.mean():,.0f} 원으로 바뀐다.",
          T(r, index=True, fmt=",.0f"), TX(out.splitlines()[-1], "out", "출력")),
    ]
