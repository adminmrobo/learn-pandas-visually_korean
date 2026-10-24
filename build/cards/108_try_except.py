from lib import *

GOOD = '{"item": "Linen shirt", "KRW": 52000, "USD": 35.5}'
BAD = '{"item": "Linen shirt", "KRW": 52000, "USD": 35.5'

CARD = dict(
    id="try_except", ch="1. 불러오기와 살펴보기", cmd="try / except",
    title="실패해도 멈추지 않게", excel="IFERROR",
    desc="AI 에게 다국어 가격표를 JSON 으로 받았는데 답이 중간에 잘리면 JSON 으로 읽을 수 없어 오류가 난다. "
         "try 안의 코드가 실패하면 프로그램을 멈추는 대신 except 아래 코드를 실행한다. 엑셀의 IFERROR 와 같은 생각이다.",
    code="""import json
good_reply = '""" + GOOD + """'
bad_reply = '""" + BAD + """'   # 끝이 잘림
for reply in [good_reply, bad_reply]:
    try:
        print("OK →", json.loads(reply))
    except json.JSONDecodeError as e:
        print("parse failed →", e)""",
)

def stages(ns, out):
    ok, fail = out.splitlines()
    import json
    try:
        json.loads(BAD); err = ""
    except json.JSONDecodeError as e:
        err = str(e)
    return [
        S("두 응답", "위는 } 로 닫혀 있고, 아래는 끝이 잘렸다.", TX(GOOD, "code", "good_reply"), TX(BAD, "code", "bad_reply")),
        S("try", "json.loads 를 시도한다. 완전한 글자는 사전이 되고, 잘린 글자는 JSONDecodeError 를 낸다.",
          TX(ok.split("→ ", 1)[1], "out", "성공"), TX("JSONDecodeError\n" + err, "err", "실패")),
        S("except", "오류가 나도 멈추지 않고 except 아래의 print 를 실행한다. 다음 응답으로 넘어갈 수 있다.",
          TX(ok, "out", "출력"), TX(fail, "out", "출력")),
    ]
