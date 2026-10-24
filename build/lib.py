"""Helpers for picturebook card modules.

A card module (build/cards/NNN_id.py) defines:
  CARD = dict(id=, ch=, cmd=, title=, excel=, desc=, code=, tip="", talk=[...])
  def stages(ns, out): -> list of stage dicts   (ns = namespace after running code, out = stdout text)

Helpers below turn DataFrames into the table nodes the page draws.
"""
import math
import numpy as np
import pandas as pd

def _fmt(v, fmt=None):
    if v is None:
        return "None"
    if isinstance(v, float) and math.isnan(v):
        return "NaN"
    if v is pd.NaT:
        return "NaT"
    if isinstance(v, (pd.Timestamp,)):
        return v.strftime("%Y-%m-%d") if (v.hour, v.minute, v.second) == (0, 0, 0) else str(v)
    if isinstance(v, (bool, np.bool_)):
        return "True" if v else "False"
    if fmt and isinstance(v, (int, float, np.integer, np.floating)):
        return format(v, fmt)
    if isinstance(v, (float, np.floating)):
        if float(v).is_integer() and abs(v) < 1e15:
            return f"{v:.1f}"
        return f"{round(float(v), 4):g}" if abs(v) < 1e6 else f"{v:,.0f}"
    return str(v)

def T(df, title=None, index=False, hl=(), hlrows=(), rcls=None, cls=None, fmt=None, nan_cls=True, ix_name=""):
    """DataFrame/Series -> table node.
    hl: column names to highlight (header + cells 'hl').
    hlrows: row positions to give row class 'hr'.
    rcls: list of row classes (g0..g5, ok, bad, dim, hr, more) - overrides hlrows.
    cls: optional dict {(row, colname): 'class'} extra cell classes.
    fmt: format spec string or dict col->spec for numbers.
    """
    if isinstance(df, pd.Series):
        df = df.to_frame(df.name if df.name is not None else "")
    cols = list(df.columns)
    head = ([ix_name if ix_name else (df.index.name or "")] if index else []) + [str(c) for c in cols]
    ccls = (["ix"] if index else []) + ["hl" if c in hl else "" for c in cols]
    rows, cl = [], []
    colvals = {c: df[c].tolist() for c in cols}   # 열마다 꺼내야 정수 열이 4.0 이 되지 않는다
    for ri, ix in enumerate(df.index):
        row, rc = [], []
        if index:
            row.append(_fmt(ix) if not isinstance(ix, tuple) else " / ".join(_fmt(i) for i in ix)); rc.append("ix")
        for c in cols:
            f = fmt.get(c) if isinstance(fmt, dict) else fmt
            v = colvals[c][ri]
            s = _fmt(v, f)
            k = []
            if c in hl: k.append("hl")
            if nan_cls and s in ("NaN", "NaT", "None"): k.append("nan")
            if cls and (ri, c) in cls: k.append(cls[(ri, c)])
            row.append(s); rc.append(" ".join(k))
        rows.append(row); cl.append(rc)
    if rcls is None:
        rcls = ["hr" if i in hlrows else "" for i in range(len(rows))]
    n = {"t": "table", "cols": head, "ccls": ccls, "rows": rows, "rcls": list(rcls), "cls": cl}
    if title: n["title"] = title
    return n

def RAW(cols, rows, title=None, ccls=None, rcls=None, cls=None):
    """Hand-made table node (all strings)."""
    rows = [[str(v) for v in r] for r in rows]
    n = {"t": "table", "cols": list(cols), "ccls": ccls or [""] * len(cols), "rows": rows,
         "rcls": rcls or [""] * len(rows), "cls": cls or [[""] * len(cols) for _ in rows]}
    if title: n["title"] = title
    return n

def TX(text, kind="code", title=None):
    """Text box. kind: 'code' (file/글자), 'out' (출력), 'err' (오류)."""
    n = {"t": "text", "text": text, "kind": kind}
    if title: n["title"] = title
    return n

def CH(**spec):
    """Animated chart node. spec types: bar, barh, line, hist, heatmap, scatter, waterfall, multi.
    See existing cards for field names."""
    return {"t": "chart", "spec": spec}

def IMG(card_id, k=0):
    """Reuse the k-th result image of this card inside a stage."""
    return {"t": "img", "src": f"assets/img/{card_id}{'' if k == 0 else '-' + str(k)}.png"}

def S(label, caption, *nodes, links=None):
    st = {"label": label, "caption": caption, "nodes": list(nodes)}
    if links is not None: st["links"] = links
    return st

def r1(x, d=1):
    return round(float(x), d)
