from lib import *

CARD = dict(
    id="to_numeric", ch="2. 청소하기", cmd='str.replace() → pd.to_numeric(errors="coerce")',
    title="₩39,000 을 숫자로", excel="찾기/바꾸기 + VALUE",
    desc="쇼핑몰 상품표의 '₩39,000' 은 숫자처럼 보이지만 글자라서 더할 수 없다. 먼저 str.replace 로 ₩ 와 쉼표를 지우고, pd.to_numeric 으로 숫자로 바꾼다. "
         "errors=\"coerce\" 는 '-' 나 빈 글자처럼 숫자로 못 바꾸는 값을 오류 대신 NaN 으로 둔다.",
    code='''import pandas as pd
s = pd.Series(["₩39,000", "₩52,000", "-3,000", "-", ""])     # -3,000 은 할인 쿠폰
step1 = s.str.replace("₩", "").str.replace(",", "")         # 기호와 쉼표 지우기
num = pd.to_numeric(step1, errors="coerce")                  # 글자 → 숫자, 못 바꾸면 NaN
print(pd.DataFrame({"raw": s, "replaced": step1, "number": num}))
print("sum:", num.sum())                                     # NaN 은 건너뛰고 더한다''',
    talk=[dict(who="robo", state="confused", text="삐빅, '-' 는 숫자가 아니라서 NaN 으로 남겼어.")],
)

def stages(ns, out):
    s, step1, num = ns["s"], ns["step1"], ns["num"]
    nanrows = ["bad" if v != v else "" for v in num]
    return [
        S("원본 글자", "₩ 기호, 쉼표, 마이너스(쿠폰), '-', 빈 글자가 섞여 있다.", T(s.rename("raw").to_frame())),
        S("str.replace", "₩ 를 지우고, 이어서 쉼표를 지운다. 마이너스 부호(-3000)는 남는다.",
          T(pd_frame(s, step1), hl=("replaced",))),
        S("pd.to_numeric", "숫자로 바꾼다. '-' 와 빈 글자는 숫자가 아니므로 errors=\"coerce\" 덕분에 NaN 이 된다.",
          T(pd_frame(s, step1, num), hl=("number",), rcls=nanrows)),
        S("이제 더할 수 있다", f"NaN 은 빼고 더한다. 39000 + 52000 − 3000 = {num.sum():,.0f}.", TX(out.splitlines()[-1], "out", "출력")),
    ]

def pd_frame(s, a, b=None):
    import pandas as pd
    d = {"raw": s, "replaced": a}
    if b is not None: d["number"] = b
    return pd.DataFrame(d)
