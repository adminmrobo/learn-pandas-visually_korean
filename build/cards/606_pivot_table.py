from lib import *
from snippets import CVS

CARD = dict(
    id="pivot_table", ch="6. 묶어서 집계하기", cmd="pivot_table(index=, columns=, values=, aggfunc=)",
    title="피벗 테이블", excel="피벗 테이블",
    desc="index 는 행에, columns 는 열에 놓을 기준이고, values 는 계산할 숫자, aggfunc 는 계산 방법(sum, mean, count)이다. "
         "groupby 두 개 + unstack 을 한 번에 하는 것과 같다. 편의점 매출을 요일 × 오전/오후로 펼친다(천원).",
    code=CVS + '''
cvs["day"] = cvs["time"].dt.day_name().str[:3]                       # Mon, Tue ...
cvs["half"] = np.where(cvs["time"].dt.hour < 12, "AM", "PM")          # 오전 / 오후
cvs["amount_k"] = cvs["amount"] / 1000
pv = cvs.pivot_table(index="day", columns="half", values="amount_k", aggfunc="sum")
pv = pv.reindex(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]).round(1)   # 달력 순서로
print(pv)''',
)

def stages(ns, out):
    cvs, pv = ns["cvs"], ns["pv"]
    head = cvs[["time", "day", "half", "amount_k"]].head(6).astype(object)
    m = cvs[(cvs.day == "Mon") & (cvs.half == "AM")]
    best = pv.stack().idxmax()
    ri = list(pv.index).index(best[0])
    return [
        S("원본", f"결제 {len(cvs)}건 중 앞 6줄. day(행 기준), half(열 기준), amount_k(계산할 값).",
          T(head, hl=("day", "half", "amount_k"))),
        S("칸마다 모으기", f"(day, half) 쌍마다 조각이 된다. 예: 월요일 오전 조각에는 결제 {len(m)}건이 들어 있고, 더하면 {m['amount_k'].sum():.1f}.",
          T(m[["time", "day", "half", "amount_k"]].head(5).astype(object), title="Mon · AM 조각 (앞 5줄)", rcls=["g0"] * min(5, len(m)))),
        S("sum 을 칸에 놓기", f"조각 합을 (행=day, 열=half) 칸에 적는다. 가장 큰 칸은 {best[0]} {best[1]} {pv.loc[best]}.",
          T(pv.astype(object), index=True, ix_name="day", cls={(ri, best[1]): "hc"})),
    ]
