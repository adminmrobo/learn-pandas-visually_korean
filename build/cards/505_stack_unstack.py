from lib import *
from snippets import FX

CARD = dict(
    id="stack_unstack", ch="5. 합치고 모양 바꾸기", cmd="unstack() · stack()",
    title="세로 목록 ↔ 가로 표", excel="피벗 ↔ 피벗 해제",
    desc="stack() 은 열 이름을 안쪽 행 이름으로 내려 칸 하나가 한 줄인 세로 목록을 만든다. unstack() 은 반대로 안쪽 행 이름을 열로 올려 가로 표로 되돌린다. "
         "unstack 에 어느 이름을 올릴지 고르면 표가 돌아간다. 환율 표(날짜 × 통화)로 본다.",
    code=FX + '''
close = fx["Close"].head(2)       # 이틀치만
print(close)
long = close.stack()              # 통화가 행 이름 안쪽으로
print(long)
print(long.unstack("Ticker"))     # 통화를 다시 열로 = 원래 모양
print(long.unstack("Date"))       # 날짜를 열로 = 돌린 모양''',
)

def stages(ns, out):
    close, long = ns["close"], ns["long"]
    g = {t: f"g{i}" for i, t in enumerate(close.columns)}
    lt = long.rename("rate").to_frame()
    lt.index = [f"{d:%m-%d} / {t}" for d, t in lt.index]
    back = long.unstack("Date")
    back.columns = [f"{d:%Y-%m-%d}" for d in back.columns]
    return [
        S("가로 표", "행은 날짜, 열은 통화. 칸 하나가 '그날 그 통화의 환율'이다.", T(close, index=True, ix_name="Date")),
        S("stack()", f"열(Ticker)이 행 이름 안쪽으로 내려갔다. 칸 {len(long)}개가 한 줄씩 된다.",
          T(lt, index=True, ix_name="Date / Ticker", rcls=[g[t] for _, t in long.index])),
        S('unstack("Date")', '안쪽 Ticker 대신 Date 를 열로 올리면 표가 돌아간다. unstack("Ticker") 는 원래 모양으로 돌아온다.',
          T(back, index=True, ix_name="Ticker", rcls=[g[t] for t in back.index])),
    ]
