from lib import *
from snippets import KOI, KOI_KIND

CARD = dict(
    id="map_dict", ch="4. 새 열 만들기", cmd=".map({사전})",
    title="사전으로 분류 붙이기", excel="VLOOKUP(작은 표)",
    desc="사전(dict)은 '왼쪽 값 → 오른쪽 값' 짝의 목록이다. 열에 map(사전)을 하면 값마다 사전에서 짝을 찾아 바꿔 준다. "
         "사전에 없는 값은 NaN 이 되므로, 분류한 뒤에는 isna().sum() 으로 빠진 게 없는지 꼭 확인한다.",
    code=KOI + "\n" + KOI_KIND + '''   # Broken cup 을 일부러 뺐다
book["type"] = book["item"].map(kind)
print(book[["item", "type"]])
print("unmapped:", book["type"].isna().sum())''',
    talk=[
        dict(who="asst", text="깨진 컵은 왜 분류가 비었어요?"),
        dict(who="robo", state="confused", text="삐빅, 사전에 없는 이름이야. 짝을 못 찾았어."),
    ],
)

def stages(ns, out):
    book = ns["book"]; kind = ns["kind"]
    d = RAW(["key", "value"], [[k, v] for k, v in kind.items()], title="kind 사전")
    bad = [i for i, v in enumerate(book["type"]) if not isinstance(v, str)]
    return [
        S("item 열과 사전", "왼쪽은 장부의 item, 오른쪽은 분류 사전이다. Broken cup 은 사전에 없다.", T(book[["item"]]), d),
        S("map(kind)", "값마다 사전에서 짝을 찾는다. 6번 Broken cup 은 짝이 없어 NaN.",
          T(book[["item", "type"]], hl=("type",), rcls=["bad" if i in bad else "" for i in range(len(book))]), links=[[0, 0], [1, 0]]),
        S("빠진 것 세기", "isna().sum() 이 1 이면 사전에 짝을 하나 더 넣어야 한다.", TX(out.splitlines()[-1], "out", "출력")),
    ]
