"""Run every card's code, capture output + figures, assemble data, write site/index.html.

usage: python3 build/build.py [card_id ...]    (no args = all cards)
"""
import contextlib, glob, importlib.util, io, json, os, sys, tempfile, traceback
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = ROOT   # 결과: repo 맨 위 index.html, assets/img
IMG = os.path.join(SITE, "assets", "img")
sys.path.insert(0, os.path.join(ROOT, "build"))

def load(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_card(m):
    c = dict(m.CARD)
    cid = c["id"]
    for f in glob.glob(os.path.join(IMG, cid + ".png")) + glob.glob(os.path.join(IMG, cid + "-*.png")):
        os.remove(f)
    imgs = []
    def show(*a, **k):
        for num in plt.get_fignums():
            fig = plt.figure(num)
            name = cid + ("" if not imgs else f"-{len(imgs)}") + ".png"
            fig.savefig(os.path.join(IMG, name), dpi=80, bbox_inches="tight", facecolor="white")
            imgs.append("assets/img/" + name)
        plt.close("all")
    plt.close("all")
    orig_show = plt.show; plt.show = show
    ns = {"__name__": "__main__"}
    buf = io.StringIO()
    cwd = os.getcwd(); tmp = tempfile.mkdtemp()
    try:
        os.chdir(tmp)
        plt.rcParams.update(matplotlib.rcParamsDefault)
        with contextlib.redirect_stdout(buf):
            exec(compile(c["code"], cid, "exec"), ns)
        if plt.get_fignums(): show()
    finally:
        os.chdir(cwd); plt.show = orig_show
    out = buf.getvalue().rstrip("\n")
    c["output"] = out
    c["imgs"] = imgs
    c["stages"] = m.stages(ns, out)
    c.setdefault("tip", ""); c.setdefault("talk", [])
    c.pop("kit", None)
    return c

def main(only):
    files = sorted(glob.glob(os.path.join(ROOT, "build", "cards", "*.py")))
    cards, bad = [], []
    for p in files:
        m = load(p)
        if only and m.CARD["id"] not in only:
            continue
        try:
            cards.append(run_card(m)); print("ok  ", m.CARD["id"], len(cards[-1]["imgs"]), "img")
        except Exception:
            bad.append(m.CARD["id"]); print("FAIL", m.CARD["id"]); traceback.print_exc()
    if only:
        os.makedirs(os.path.join(ROOT, "build", "_preview"), exist_ok=True)
        for c in cards:
            json.dump(c, open(os.path.join(ROOT, "build", "_preview", c["id"] + ".json"), "w"), ensure_ascii=False, indent=1)
        return bad
    ids = [c["id"] for c in cards]
    assert len(ids) == len(set(ids)), "duplicate ids"
    tpl = open(os.path.join(ROOT, "build", "template.html"), encoding="utf-8").read()
    data = json.dumps(cards, ensure_ascii=False).replace("</", "<\\/")
    html = tpl.replace("__CARD_DATA__", data).replace("__CARD_COUNT__", str(len(cards)))
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(html)
    print(len(cards), "cards ->", os.path.join(SITE, "index.html"), "fail:", bad)
    return bad

if __name__ == "__main__":
    sys.exit(1 if main(set(sys.argv[1:])) else 0)
