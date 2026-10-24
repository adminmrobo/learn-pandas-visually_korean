from lib import *
from snippets import FX

CARD = dict(
    id="shift", ch="4. 새 열 만들기", cmd=".shift(-1)",
    title="다음 줄 값을 옆에 붙이기", excel="한 칸 아래 셀 참조",
    desc="shift(-1) 은 열을 한 칸 위로 당겨서 '다음 줄 값'을 지금 줄 옆에 놓는다(shift(1) 은 이전 줄 값). "
         "원·달러 환율의 오늘 값과 다음 영업일 값을 나란히 놓고 빼면 하루 사이 얼마나 움직였는지 보인다.",
    code=FX + '''
usd = fx[("Close", "USDKRW=X")].rename("usd").to_frame()   # 원·달러 종가만
usd["next_usd"] = usd["usd"].shift(-1)
usd["change"] = (usd["next_usd"] - usd["usd"]).round(1)
print(usd)''',
)

def stages(ns, out):
    u = ns["usd"]
    big = u["change"].abs().idxmax()
    return [
        S("원·달러 종가", "영업일 다섯 날의 1달러당 원. 예시값이다.", T(u[["usd"]], index=True)),
        S("shift(-1)", "usd 열을 한 칸 위로 당긴다. 마지막 줄은 다음 값이 없어 NaN.", T(u[["usd", "next_usd"]], index=True, hl=("next_usd",))),
        S("빼기", f"다음 영업일 − 오늘. 가장 크게 움직인 건 {big:%m-%d} 에서 다음 영업일로 넘어갈 때, {u.loc[big, 'change']:+g}원이다.",
          T(u, index=True, hl=("change",), rcls=["hr" if ix == big else "" for ix in u.index])),
    ]
