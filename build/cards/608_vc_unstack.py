from lib import *
from snippets import CVS

CARD = dict(
    id="vc_unstack", ch="6. 묶어서 집계하기", cmd="groupby()[열].value_counts(normalize=True).unstack()",
    title="그룹별 비율표", excel="피벗 '행 합계 대비 %'",
    desc="주중/주말로 묶은 뒤 결제수단 value_counts(normalize=True) 를 하면 그룹 안에서의 비율이 나온다. unstack 으로 결제수단을 열로 올리면 "
         "비율표가 된다. 한쪽 그룹에 없는 값이 있으면 빈칸이 생기므로 fillna(0) 을 붙여 둔다.",
    code=CVS + '''
cvs["week"] = np.where(cvs["time"].dt.dayofweek >= 5, "Weekend", "Weekday")
share = cvs.groupby("week")["pay"].value_counts(normalize=True)
print(share.round(3))
wide = share.unstack().fillna(0).round(3)
print(wide)''',
)

def stages(ns, out):
    cvs, share, wide = ns["cvs"], ns["share"], ns["wide"]
    n = cvs["week"].value_counts()
    sl = share.round(3).rename("share").to_frame().astype(object)
    g = {"Weekday": "g0", "Weekend": "g1"}
    return [
        S("결제 기록", f"주중 {n['Weekday']}건, 주말 {n['Weekend']}건. week 열로 나눈다.",
          T(cvs[["time", "week", "pay"]].head(6).astype(object), rcls=[g[w] for w in cvs["week"].head(6)])),
        S("그룹 안 비율", f"그룹마다 결제수단 비율을 낸다. 주말 카드 비율 {wide.loc['Weekend', 'Card']}. 그룹 안에서 더하면 1.",
          T(sl, index=True, ix_name="week / pay", rcls=[g[w] for w, _ in share.index])),
        S("unstack · fillna(0)", "결제수단을 열로 올리면 주중/주말을 한눈에 비교하는 비율표가 된다. 빈칸이 생기면 0 으로 채운다.",
          T(wide.astype(object), index=True, ix_name="week", rcls=[g[w] for w in wide.index])),
    ]
