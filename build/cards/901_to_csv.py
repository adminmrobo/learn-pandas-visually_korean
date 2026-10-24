from lib import *

CARD = dict(
    id="to_csv", ch="9. 저장하기", cmd='to_csv(encoding="utf-8-sig")',
    title="표를 CSV 로 저장하고 다시 읽기", excel="다른 이름으로 저장(CSV UTF-8)",
    desc="to_csv 로 표를 파일로 저장한다. encoding=\"utf-8-sig\" 로 저장하면 엑셀에서 더블클릭해도 한글이 깨지지 않는다. "
         "저장한 파일을 다시 읽어 확인하는 것까지가 한 단계다. 예시는 쇼핑몰의 외국어 가격표다. "
         "Colab 왼쪽 📁 폴더 아이콘에서 파일을 볼 수 있다.",
    code='''import pandas as pd
tag = pd.DataFrame({"상품": ["티셔츠", "셔츠", "청바지"], "name_en": ["Tee", "Shirt", "Denim"],
                    "krw": [19000, 39000, 89000], "usd": [13.0, 27.0, 61.0]}).set_index("상품")
tag.to_csv("price_tag.csv", encoding="utf-8-sig")              # index(상품)도 함께 저장
back = pd.read_csv("price_tag.csv", encoding="utf-8-sig")     # 다시 읽어 확인
print(back)''',
    tip='tag.to_csv("내파일.csv", encoding="utf-8-sig", index=False) 처럼 index=False 를 주면 행 이름 칸 없이 저장한다.',
    talk=[
        dict(who="asst", text="저장한 CSV 를 엑셀로 열면 한글이 깨져요. 왜요?"),
        dict(who="doc", text="utf-8-sig 로 저장하면 엑셀도 한글을 알아봐요."),
    ],
)

def stages(ns, out):
    import io
    tag, back = ns["tag"], ns["back"]
    buf = io.StringIO(); tag.to_csv(buf)
    return [
        S("표 tag", "상품 이름이 행 이름(index)이다.", T(tag, index=True, ix_name="상품")),
        S("to_csv", "쉼표로 이은 글자 파일이 된다. 행 이름도 첫 칸에 저장된다.", TX(buf.getvalue().strip(), "code", "price_tag.csv")),
        S("read_csv 로 확인", f"다시 읽으면 상품이 보통 열로 돌아온다. {len(back)}줄, 숫자가 그대로인지 확인한다.", T(back, hl=("상품",))),
    ]
