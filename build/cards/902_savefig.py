from lib import *

CARD = dict(
    id="savefig", ch="9. 저장하기", cmd='fig.savefig(dpi=200, bbox_inches="tight")',
    title="그림을 파일로 저장하기", excel="그림으로 저장",
    desc="fig.savefig 는 그림을 파일로 저장한다. dpi=200 은 보고서에 넣어도 선명한 해상도, bbox_inches=\"tight\" 는 "
         "그림 밖으로 나간 범례까지 잘리지 않게 여백을 맞춘다. Colab 에서 files.download 를 부르면 내 컴퓨터로 내려받는다.",
    code='''import os
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(["Apr", "May", "Jun"], [4.00, 4.28, 4.36], color="#028090", label="Sales")
ax.set(title="Cafe Koi monthly sales", ylabel="KRW million")
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))          # 범례를 그림 밖 오른쪽에
fig.savefig("koi_monthly_sales.png", dpi=200, bbox_inches="tight")
print("saved:", os.path.getsize("koi_monthly_sales.png") // 1024, "KB")
try:
    from google.colab import files
    files.download("koi_monthly_sales.png")     # Colab: 브라우저로 내려받기
except ImportError:
    pass                                         # Colab 이 아니면 지금 폴더에 저장된 파일을 연다''',
)

def stages(ns, out):
    first = out.splitlines()[0]
    return [
        S("그림 만들기", "fig(그림판) 위에 ax(축)로 그린다. 범례는 그림 밖 오른쪽.",
          CH(type="bar", title="Cafe Koi monthly sales", ylabel="KRW million", cats=["Apr", "May", "Jun"],
             series=[dict(name="Sales", values=[4.00, 4.28, 4.36], c="#028090")], labels=2)),
        S("savefig", 'dpi=200, bbox_inches="tight" 로 PNG 저장. 밖의 범례도 잘리지 않는다.', TX(first, "out", "출력")),
        S("files.download", "Colab 이면 브라우저가 파일을 내려받는다. 처음에는 '여러 파일 다운로드 허용' 창이 뜰 수 있다.",
          TX('files.download("koi_monthly_sales.png")', "code", "Colab")),
    ]
