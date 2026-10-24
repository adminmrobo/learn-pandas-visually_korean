from lib import *
import importlib.util, os
_spec = importlib.util.spec_from_file_location("c814", os.path.join(os.path.dirname(__file__), "814_contour.py"))
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)

CARD = dict(
    id="surface", ch="8. 차트 그리기", cmd="ax.plot_surface()",
    title="같은 격자를 3D 곡면으로", excel="(엑셀 3D 표면 차트)",
    desc="같은 격자를 plot_surface 로 그리면 3D 곡면이 된다. 보기에는 화려하지만 각도에 따라 손익 0 선이 가려진다. "
         "오른쪽 2D 등고선은 같은 정보를 평면에 펼쳐 바로 읽힌다. 보고서에는 오른쪽을 쓴다.",
    code=_m.CODE_MODEL + '''
fig = plt.figure(figsize=(10, 4))
ax1 = fig.add_subplot(1, 2, 1, projection="3d")
ax1.plot_surface(P, C, Z, cmap="RdYlGn")
ax1.set(title="3D surface", xlabel="Price", ylabel="Bean cost")
ax2 = fig.add_subplot(1, 2, 2)
ax2.contourf(P, C, Z, levels=12, cmap="RdYlGn")
ax2.contour(P, C, Z, levels=[0], colors="black")
ax2.set(title="2D contour", xlabel="Price", ylabel="Bean cost")
plt.show()''',
)

def stages(ns, out):
    Z = ns["Z"]
    return [
        S("같은 격자 Z", f"앞 카드에서 만든 {Z.shape[0]} × {Z.shape[1]} 이익 격자. 가장 큰 값 {Z.max():.1f}, 가장 작은 값 {Z.min():.1f}(백만원).",
          TX(f"Z.shape = {Z.shape}\nZ.max() = {Z.max():.2f}\nZ.min() = {Z.min():.2f}", "out", "출력")),
        S("두 방식", "왼쪽 3D 는 0 선 위치를 읽기 어렵고, 오른쪽 2D 는 바로 읽힌다.", IMG("surface")),
    ]
