# -*- coding: utf-8 -*-
"""Monta treinamento-histograma-cep.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import math
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cep_data import (A2, ACOMP, BASE, CAPAZ, CHECK, D2, D4, ETAPAS, EX1, EX2, EXCL, FORMAS, LIMITE, NAOCAPAZ, PARADA, PARTES, REGRAS, S_AMP, S_FORA, S_LADO,  # noqa: E402
                      S_TEND, amp, classes, conf, fora_espec, media, resumo)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# em controle, no limite e com sinal: a mesma paleta de três cores do estudo de Calibração, validada para daltonismo nos dois modos
LIGHT = ("\n  --s1:#2A6FB0; --s1-tint:#DCE8F3;\n  --s2:#D19A2E; --s2-tint:#F8EBCB;\n  --s3:#B0413E; --s3-tint:#F5DEDC;\n  --on-s2:#16242E;")
DARK = ("\n  --s1:#4F97DB; --s1-tint:#1B2F42;\n  --s2:#B58E14; --s2-tint:#3A2C12;\n  --s3:#D14B45; --s3-tint:#3D1F1E;\n  --on-s2:#0F171C;")
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Situações */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.s1{background:var(--s1)} .chip.s2{background:var(--s2);color:var(--on-s2)} .chip.s3{background:var(--s3)}
.chip.sl{background:var(--sunk);color:var(--ink);box-shadow:inset 0 0 0 1px var(--rule)}
svg .hd-ink{fill:var(--ink)}
svg .f1{fill:var(--s1)} svg .f2{fill:var(--s2)} svg .f3{fill:var(--s3)} svg .f0{fill:var(--muted)}
svg .t1{fill:var(--s1-tint)} svg .t2{fill:var(--s2-tint)} svg .t3{fill:var(--s3-tint)}
svg .bx-s1{fill:var(--s1-tint);stroke:var(--s1);stroke-width:1.5} svg .bx-s2{fill:var(--s2-tint);stroke:var(--s2);stroke-width:1.5} svg .bx-s3{fill:var(--s3-tint);stroke:var(--s3);stroke-width:1.5}
svg .lane{fill:var(--sunk)}
svg .lim{stroke:var(--s3);stroke-width:1.5;stroke-dasharray:6 4;fill:none}
svg .esp{stroke:var(--ink);stroke-width:2;fill:none}
svg .ctr{stroke:var(--muted);stroke-width:1.2;fill:none}
svg .ser{stroke:var(--s1);stroke-width:1.8;fill:none;stroke-linejoin:round}
svg .p-ok{fill:var(--s1);stroke:var(--surface);stroke-width:1.5}
svg .p-sig{fill:var(--s3);stroke:var(--surface);stroke-width:1.5}
svg .p-exc{fill:var(--surface);stroke:var(--muted);stroke-width:1.8}
svg .curve{stroke:var(--s1);stroke-width:2;fill:var(--s1-tint);fill-opacity:.7}
svg .halo{paint-order:stroke;stroke:var(--surface);stroke-width:5px;stroke-linejoin:round}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas dos exemplos */
table.aud{font-size:.8rem;min-width:900px;line-height:1.4}
table.aud th, table.aud td{padding:7px 8px}
table.aud td.n{white-space:nowrap;font-weight:600;color:var(--muted)}
table.aud td.c, table.aud th.c{text-align:center;font-variant-numeric:tabular-nums}
table.aud td.no{background:var(--s3-tint);font-weight:600}
table.aud td small, table.aud th small{display:block;color:var(--muted);font-size:.76rem;margin-top:3px;font-weight:400}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha da organização (acima de cada exemplo) */"""
assert css.count("\n.ficha{") == 1
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

TNUM = ' style="font-variant-numeric:tabular-nums"'
END = ' text-anchor="end"'
MID = ' text-anchor="middle"'
W5, G5 = 164, 14
R1, R2 = resumo(EX1), resumo(EX2)


def br(v, d=1):
    """Número no formato brasileiro."""
    s = f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s


def nv(ex, v, extra=0):
    """Valor na casa decimal do exemplo: inteiro na pizzaria, um décimo na indústria."""
    return br(v, (0 if ex is EX1 else 1) + extra)


def marker(i, mu=False):
    return (f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path class="{"ah-mu" if mu else "ah"}" d="M0 0 L10 5 L0 10 z"/></marker>')


def lines(o, txt, x, y, wrap, fs=10.5, cls="", step=13, maxl=3, anchor=None):
    """Texto quebrado em linhas; devolve o y da linha seguinte."""
    ls = textwrap.wrap(txt, wrap, break_on_hyphens=False)
    assert len(ls) <= maxl, txt
    attr = (f' class="{cls}"' if cls else "") + (f' text-anchor="{anchor}"' if anchor else "")
    for j, l in enumerate(ls):
        o.append(f'        <text{attr} x="{x}" y="{y + j * step}" font-size="{fs}">{escape(l)}</text>')
    return y + step * len(ls)


def cinco(o, itens, classes_, mk, y0=16, h=140, rotulo=None, maxd=5, mid=None, wrap_d=25):
    xs = []
    for k, (tit, desc) in enumerate(itens):
        x = 12 + k * (W5 + G5)
        xs.append(x)
        ink = classes_[k] == "bx-ink"
        o.append(f'        <rect class="{classes_[k]}" x="{x}" y="{y0}" width="{W5}" height="{h}"/>')
        if rotulo:
            o.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="{y0 + 20}" font-size="10">{escape(rotulo(k))}</text>')
        tl = textwrap.wrap(tit, 19, break_on_hyphens=False)
        yt = y0 + (42 if rotulo else 24)
        for j, l in enumerate(tl):
            o.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{yt + j * 15}" font-size="12.5">{escape(l)}</text>')
        lines(o, desc, x + 12, yt + 15 * len(tl) + 8, wrap_d, cls="t-ground" if ink else "", step=14.5, maxl=maxd)
        if mk and k < len(itens) - 1:
            ym = mid or (y0 + h / 2)
            o.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="{ym}" x2="{x + W5 + G5 - 2}" y2="{ym}" marker-end="url(#{mk})"/>')
    return xs


# ------------------------------------------------------------------ desenhos reutilizados
def carta(o, ex, r, valor, x0, x1, y0, y1, lo, hi, nome, lc, lsc, lic, rot_fmt, tick=None, marcas=True, pts_cls=None):
    """Um gráfico de controle (média ou amplitude) com linha central e limites; devolve as posições dos pontos."""
    py = lambda v: y1 - (v - lo) * (y1 - y0) / (hi - lo)  # noqa: E731
    n = len(ex["subs"])
    px = lambda k: x0 + 14 + k * (x1 - x0 - 28) / (n - 1)  # noqa: E731
    o.append(f'        <text class="mono mu" x="{x0}" y="{y0 - 10}" font-size="10">{escape(nome)}</text>')
    o.append(f'        <line class="ln-mu" x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}"/><line class="ln-mu" x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}"/>')
    for v, cls, rot in ((lsc, "lim", "LSC"), (lc, "ctr", "LC"), (lic, "lim", "LIC")):
        if v is None:
            continue
        o.append(f'        <line class="{cls}" x1="{x0}" y1="{py(v):.1f}" x2="{x1}" y2="{py(v):.1f}"/>')
        o.append(f'        <text class="mu halo" x="{x1 + 6}" y="{py(v) + 4:.1f}" font-size="10.5"{TNUM}>{rot} {rot_fmt(v)}</text>')
    pts = [(px(k), py(valor(g["v"]))) for k, g in enumerate(ex["subs"])]
    o.append('        <path class="ser" d="' + " ".join(f'{"M" if k == 0 else "L"}{x:.1f} {y:.1f}' for k, (x, y) in enumerate(pts)) + '"/>')
    for k, (x, y) in enumerate(pts):
        cls = pts_cls(k) if pts_cls else "p-ok"
        o.append(f'        <circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{4.5 if cls != "p-ok" else 3.8}"/>')
    if marcas:
        for k in range(0, n, tick or 4):
            o.append(f'        <text class="mu" x="{px(k):.1f}" y="{y1 + 15}" font-size="10"{MID}{TNUM}>{k + 1}</text>')
    return pts, px, py


def hist(o, ex, x0, x1, y0, y1, hmax, cor=lambda a, b: "f1", rot=True, valores=None, step_y=None):
    """Histograma das medições individuais, com os limites da especificação."""
    h = ex["head"]
    cl = classes(ex)
    vals = valores if valores is not None else [v for g in ex["subs"] for v in g["v"]]
    cont = [sum(1 for v in vals if a <= v < b) for a, b in cl]
    lo, hi = cl[0][0], cl[-1][1]
    px = lambda v: x0 + (v - lo) * (x1 - x0) / (hi - lo)  # noqa: E731
    py = lambda c: y1 - c * (y1 - y0) / hmax  # noqa: E731
    o.append(f'        <line class="ln-mu" x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}"/>')
    for (a, b), c in zip(cl, cont):
        if c:
            o.append(f'        <rect class="{cor(a, b)}" x="{px(a) + 1:.1f}" y="{py(c):.1f}" width="{px(b) - px(a) - 2:.1f}" height="{y1 - py(c):.1f}"/>')
            o.append(f'        <text class="mu" x="{(px(a) + px(b)) / 2:.1f}" y="{py(c) - 4:.1f}" font-size="9.5"{MID}{TNUM}>{c}</text>')
    if rot:
        for k, (a, b) in enumerate(cl):
            if k % 2 == 0:
                o.append(f'        <text class="mu" x="{px(a):.1f}" y="{y1 + 14}" font-size="9.5"{MID}{TNUM}>{br(a, 0) if float(a).is_integer() else nv(ex, a)}</text>')
    for v, t in ((h["lie"], "LIE"), (h["lse"], "LSE")):
        o.append(f'        <line class="esp" x1="{px(v):.1f}" y1="{y0 - 6}" x2="{px(v):.1f}" y2="{y1}"/>')
        o.append(f'        <text class="b" x="{px(v):.1f}" y="{y0 - 10}" font-size="10.5"{MID}{TNUM}>{t} {br(v, 0) if float(v).is_integer() else nv(ex, v)}</text>')
    return px, cont


def fmt_ex(ex, extra=1):
    return lambda v: nv(ex, v, extra)


# ------------------------------------------------------------------ figura 1: duas perguntas
L1 = R1["L"]
f1 = ['      <svg viewBox="0 0 900 290" role="img" aria-label="As duas ferramentas com os pesos da massa da pizzaria. À esquerda, o histograma das 125 bolas, com a '
      f'especificação de 380 a 420 g: o centro está no alvo, mas a largura ocupa quase toda a tolerância. À direita, o gráfico das médias dos 25 lotes, todas dentro '
      f'dos limites de controle de {br(L1["lic"])} a {br(L1["lsc"])} g.">']
f1.append('        <text class="b" x="20" y="24" font-size="13">Histograma: cabe na especificação?</text>')
f1.append('        <text class="b" x="470" y="24" font-size="13">Gráfico de controle: está estável no tempo?</text>')
hist(f1, EX1, 30, 410, 70, 230, 34)
f1.append(f'        <text class="mu" x="220" y="270" font-size="11"{MID}>125 bolas de massa, em gramas</text>')
carta(f1, EX1, R1, media, 470, 800, 70, 230, 385, 416, "MÉDIA DE CADA LOTE", L1["lc"], L1["lsc"], L1["lic"], fmt_ex(EX1))
f1.append(f'        <text class="mu" x="635" y="270" font-size="11"{MID}>Lotes de 22/03 a 15/04/2027</text>')
f1.append("      </svg>")

# ------------------------------------------------------------------ figura 2: etapas
et = ['      <svg viewBox="0 0 900 214" role="img" aria-label="As cinco etapas do controle estatístico de processo. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS)
      + ' Quando o processo muda de propósito, a base é refeita.">', "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
xs = cinco(et, ETAPAS, ["bx", "bx-p", "bx-d", "bx-c", "bx-ink"], "a2", h=138, rotulo=lambda k: f"ETAPA {k + 1}", mid=80)
xa, xb = xs[4] + W5 / 2, xs[2] + W5 / 2
et.append(f'        <path class="ln-mu dash" d="M{xa} 156 V184 H{xb} V160" marker-end="url(#a2m)"/>')
et.append(f'        <text class="mu halo" x="{(xa + xb) / 2}" y="188" font-size="11"{MID}>processo mudado de propósito: nova base</text>')
et.append("      </svg>")

# ------------------------------------------------------------------ figura 3: formas do histograma
fo = ['      <svg viewBox="0 0 900 210" role="img" aria-label="Seis formas de histograma e o que cada uma sugere. ' + " ".join(f"{a}: {b}" for a, b, _ in FORMAS) + '">']
for k, (nome, desc, perfil) in enumerate(FORMAS):
    x = 12 + k * 148
    fo.append(f'        <rect class="bx" x="{x}" y="10" width="138" height="190"/>')
    fo.append(f'        <text class="b" x="{x + 12}" y="32" font-size="12.5">{escape(nome)}</text>')
    for j, hgt in enumerate(perfil):
        if hgt:
            fo.append(f'        <rect class="{"f3" if nome == "Ilha" and j == 8 else "f1"}" x="{x + 14 + j * 12.2:.1f}" y="{120 - hgt * 8.5:.1f}" width="10.5" height="{hgt * 8.5:.1f}"/>')
    fo.append(f'        <line class="esp" x1="{x + 22}" y1="38" x2="{x + 22}" y2="120"/><line class="esp" x1="{x + 118}" y1="38" x2="{x + 118}" y2="120"/>')
    fo.append(f'        <line class="ln-mu" x1="{x + 10}" y1="120" x2="{x + 128}" y2="120"/>')
    lines(fo, desc, x + 12, 142, 22, fs=10.5, step=14, maxl=4)
fo.append("      </svg>")

# ------------------------------------------------------------------ figura 4: anatomia do gráfico X̄-R (base da indústria)
L2 = R2["L"]
an = [f'      <svg viewBox="0 0 900 330" role="img" aria-label="As partes do gráfico de média e amplitude, com a base da indústria. ' + " ".join(f"{a}: {b}" for a, b in PARTES)
      + f' Linha central da média {br(L2["lc"], 2)} µm, limites {br(L2["lic"], 2)} e {br(L2["lsc"], 2)} µm; amplitude média {br(L2["rb"], 2)} µm, limite superior {br(L2["lscr"], 2)} µm.">',
      "        <defs>" + marker("a4") + "</defs>"]
base2 = {**EX2, "subs": EX2["subs"][:14]}
cls_b = lambda k: "p-exc" if EX2["subs"][k]["excl"] else "p-ok"  # noqa: E731
pts, px4, py4 = carta(an, base2, R2, media, 40, 520, 40, 170, 39.4, 41.5, "MÉDIA DE CADA BOBINA (µm)", L2["lc"], L2["lsc"], L2["lic"], lambda v: br(v, 2), tick=2, pts_cls=cls_b)
carta(an, base2, R2, amp, 40, 520, 220, 300, 0, 1.6, "AMPLITUDE DE CADA BOBINA (µm)", L2["rb"], L2["lscr"], None, lambda v: br(v, 2), tick=2, pts_cls=cls_b)
xe, ye = pts[5]
an.append(f'        <line class="ln-mu" x1="{xe + 6:.1f}" y1="{ye - 2:.1f}" x2="{xe + 40:.1f}" y2="{ye - 14:.1f}"/>')
an.append(f'        <text class="mu halo" x="{xe + 44:.1f}" y="{ye - 10:.1f}" font-size="10.5">bobina excluída da base</text>')
an.append('        <rect class="bx" x="636" y="30" width="252" height="282"/>')
yy = 54
for a, b in PARTES:
    an.append(f'        <text class="b" x="650" y="{yy}" font-size="12">{escape(a)}</text>')
    yy = lines(an, b, 650, yy + 16, 38, fs=10.5, step=13.5, maxl=3) + 12
an.append("      </svg>")

# ------------------------------------------------------------------ figura 5: as regras
rg = ['      <svg viewBox="0 0 900 220" role="img" aria-label="As quatro regras de sinal deste material. ' + " ".join(f"{a}: {b}" for a, b in REGRAS) + '">']
PADS = {S_FORA: [0.1, -0.3, 0.4, 0.0, -0.2, 1.35, 0.1, -0.1, 0.2],
        S_AMP: [0.4, 0.5, 0.3, 0.6, 0.45, 1.35, 0.5, 0.4, 0.5],
        S_LADO: [0.3, 0.45, -0.1, -0.2, -0.3, -0.5, -0.2, -0.4, -0.35],
        S_TEND: [0.2, -0.3, 0.1, -0.1, 0.05, 0.25, 0.45, 0.7, 0.9]}
for k, (nome, desc) in enumerate(REGRAS):
    x = 12 + k * 222
    vals = PADS[nome]
    amp_ = nome == S_AMP
    rg.append(f'        <rect class="bx" x="{x}" y="10" width="212" height="200"/>')
    rg.append(f'        <text class="b" x="{x + 12}" y="32" font-size="12.5">{escape(nome)}</text>')
    yc, sc = (100, 40) if not amp_ else (118, 40)
    py = lambda v: yc - v * sc  # noqa: E731
    lims = [(1, "lim"), (0, "ctr"), (-1, "lim")] if not amp_ else [(1.0, "lim"), (0.45, "ctr")]
    for v, cls in lims:
        rg.append(f'        <line class="{cls}" x1="{x + 14}" y1="{py(v):.1f}" x2="{x + 198}" y2="{py(v):.1f}"/>')
    pp = [(x + 22 + j * 21, py(v)) for j, v in enumerate(vals)]
    rg.append('        <path class="ser" d="' + " ".join(f'{"M" if j == 0 else "L"}{a:.1f} {b:.1f}' for j, (a, b) in enumerate(pp)) + '"/>')
    sig = {S_FORA: {5}, S_AMP: {5}, S_LADO: {8}, S_TEND: {8}}[nome]
    marc = {S_LADO: range(2, 9), S_TEND: range(3, 9)}.get(nome, [])
    for j, (a, b) in enumerate(pp):
        rg.append(f'        <circle class="{"p-sig" if j in sig or j in marc else "p-ok"}" cx="{a:.1f}" cy="{b:.1f}" r="4"/>')
    lines(rg, desc, x + 12, 168, 34, fs=10.5, step=14, maxl=3)
rg.append("      </svg>")


# ------------------------------------------------------------------ figura 6: capacidade
def curva(o, cx, s, x0, x1, ybase, hmax, lie_x, lse_x, titulo, txt):
    pts = []
    for i in range(121):
        v = cx - 4 * s + i * 8 * s / 120
        if x0 <= v <= x1:
            pts.append((v, ybase - hmax * math.exp(-0.5 * ((v - cx) / s) ** 2)))
    o.append('        <path class="curve" d="M' + f'{pts[0][0]:.1f} {ybase} ' + " ".join(f"L{a:.1f} {b:.1f}" for a, b in pts) + f' L{pts[-1][0]:.1f} {ybase} Z"/>')
    o.append(f'        <line class="ln-mu" x1="{x0}" y1="{ybase}" x2="{x1}" y2="{ybase}"/>')
    for v, t in ((lie_x, "LIE"), (lse_x, "LSE")):
        o.append(f'        <line class="esp" x1="{v}" y1="{ybase - hmax - 14}" x2="{v}" y2="{ybase}"/><text class="b" x="{v}" y="{ybase - hmax - 18}" font-size="10.5"{MID}>{t}</text>')
    o.append(f'        <text class="b" x="{(x0 + x1) / 2}" y="{ybase + 22}" font-size="12"{MID}>{escape(titulo)}</text>')
    lines(o, txt, (x0 + x1) / 2, ybase + 40, 40, fs=10.5, cls="mu", step=14, maxl=2, anchor="middle")


cap = ['      <svg viewBox="0 0 900 250" role="img" aria-label="Três processos diante da mesma especificação. Estreito e centrado: Cp e Cpk de 1,67, capaz. '
       'Estreito e deslocado: Cp de 1,67 e Cpk de 0,67, não capaz por estar fora do centro. Largo e centrado: Cp e Cpk de 0,8, não capaz pela largura.">']
for k, (dx, s, tit, txt) in enumerate(((0, 18, "Cp 1,67 · Cpk 1,67", "Estreito e centrado: capaz."),
                                       (54, 18, "Cp 1,67 · Cpk 0,67", "Estreito, mas fora do centro: centralizar."),
                                       (0, 37.5, "Cp 0,80 · Cpk 0,80", "Centrado, mas largo: reduzir a variação."))):
    x0 = 20 + k * 296
    curva(cap, x0 + 135 + dx, s, x0, x0 + 270, 170, 110, x0 + 45, x0 + 225, tit, txt)
cap.append("      </svg>")

# ------------------------------------------------------------------ figura 7: limite de controle não é especificação
sig_i = L1["sigma"]
lc_ = ['      <svg viewBox="0 0 900 230" role="img" aria-label="Na pizzaria, as bolas variam com desvio de cerca de 8 g, e as médias de cinco bolas variam menos, cerca de 3,6 g. '
       f'Os limites de controle da média, de {br(L1["lic"])} a {br(L1["lsc"])} g, ficam dentro da especificação de 380 a 420 g, mas isso não diz que cada bola está dentro dela.">']
X0, X1 = 80, 820
lo, hi = 365, 435
pxv = lambda v: X0 + (v - lo) * (X1 - X0) / (hi - lo)  # noqa: E731


def gauss(o, cx, s, cls, hmax, ybase=170):
    pts = [(pxv(cx - 4 * s + i * 8 * s / 120), ybase - hmax * math.exp(-0.5 * ((-4 + i * 8 / 120)) ** 2)) for i in range(121)]
    o.append(f'        <path class="{cls}" d="M{pts[0][0]:.1f} {ybase} ' + " ".join(f"L{a:.1f} {b:.1f}" for a, b in pts) + f' L{pts[-1][0]:.1f} {ybase} Z"/>')


gauss(lc_, L1["lc"], sig_i, "curve", 55)
lc_[-1] = lc_[-1].replace('class="curve"', 'class="curve" style="fill-opacity:.35"')
gauss(lc_, L1["lc"], sig_i / math.sqrt(5), "curve", 125)
lc_.append(f'        <line class="ln-mu" x1="{X0}" y1="170" x2="{X1}" y2="170"/>')
for v, t, cls, y in ((380, "LIE 380", "esp", 30), (420, "LSE 420", "esp", 30), (L1["lic"], f'LIC {br(L1["lic"])}', "lim", 18), (L1["lsc"], f'LSC {br(L1["lsc"])}', "lim", 18)):
    lc_.append(f'        <line class="{cls}" x1="{pxv(v):.1f}" y1="{y + 6}" x2="{pxv(v):.1f}" y2="170"/>')
    lc_.append(f'        <text class="{"b" if cls == "esp" else "mu"} halo" x="{pxv(v):.1f}" y="{y}" font-size="10.5"{MID}{TNUM}>{t}</text>')
for v in range(370, 431, 10):
    lc_.append(f'        <text class="mu" x="{pxv(v):.1f}" y="186" font-size="10"{MID}{TNUM}>{v}</text>')
lc_.append(f'        <text class="b halo" x="{pxv(L1["lc"]):.1f}" y="36" font-size="11"{MID}>médias de cinco bolas</text>')
lc_.append(f'        <text class="mu halo" x="{pxv(423):.1f}" y="150" font-size="11">bolas, uma a uma</text>')
lc_.append(f'        <text x="450" y="218" font-size="11.5"{MID}>Os limites de controle valem para médias. A especificação vale para cada bola que vai ao forno.</text>')
lc_.append("      </svg>")


# ------------------------------------------------------------------ exemplos: fichas e tabelas
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Característica</dt><dd>{escape(h["carac"])}, de {br(h["lie"], 0)} a {br(h["lse"], 0)} {h["unid"]}.</dd></div>',
                      f'    <div><dt>Subgrupo</dt><dd>{escape(h["subgrupo"])}.</dd></div>',
                      f'    <div><dt>Medição</dt><dd>{escape(h["instr"])}.</dd></div>',
                      f'    <div><dt>Período</dt><dd>{escape(h["periodo"])}. Base: {"todos os subgrupos" if h["base"] >= len(ex["subs"]) else "os " + str(h["base"]) + " primeiros"}.</dd></div>',
                      f'    <div><dt>Responsável</dt><dd>{escape(h["resp"])}.</dd></div>',
                      '  </dl>'])


SIG_CLS = {S_FORA: "s3", S_AMP: "s3", S_LADO: "s2", S_TEND: "s2"}


def tab_dados(ex, r):
    h, L = ex["head"], r["L"]
    rows = []
    for k, g in enumerate(ex["subs"]):
        s = r["sg"][k]
        vals = "".join(f'<td class="c{" no" if v < h["lie"] or v > h["lse"] else ""}">{nv(ex, v)}</td>' for v in g["v"])
        fa = r["fases"][k]
        fase_ = f'<span class="chip sl">{fa}</span>' if fa == EXCL else fa
        sig = f'<span class="chip {SIG_CLS[s]}">{s}</span>' if s else "—"
        rows.append(f'<td class="n">{k + 1}</td><td>{g["data"].strftime("%d/%m")}<small>{escape(g["id"])}</small></td>{vals}'
                    f'<td class="c">{nv(ex, media(g["v"]), 1)}</td><td class="c">{nv(ex, amp(g["v"]))}</td><td>{fase_}{"<small>" + escape(g["motivo"]) + "</small>" if g["motivo"] else ""}</td>'
                    f'<td>{sig}</td>')
    cap_ = r["cap"]
    o = ['  <div class="tbl">', '    <table class="aud">',
         f'      <caption>{len(ex["subs"])} subgrupos · LC {nv(ex, L["lc"], 1)} · LSC {nv(ex, L["lsc"], 1)} · LIC {nv(ex, L["lic"], 1)} · R̄ {nv(ex, L["rb"], 1)} · '
         f'Cp {br(cap_["cp"], 2)} · Cpk {br(cap_["cpk"], 2)}</caption>',
         '      <thead><tr><th>#</th><th>Data</th><th class="c" colspan="5">Cinco medições (em ' + h["unid"] + ')</th><th class="c">Média</th><th class="c">Amplitude</th>'
         '<th style="width:22%">Fase</th><th>Sinal</th></tr></thead>', '      <tbody>']
    o += [f'        <tr>{x}</tr>' for x in rows]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


# ------------------------------------------------------------------ figura 8: pizzaria, X̄-R e histograma
p8 = ['      <svg viewBox="0 0 900 360" role="img" aria-label="Gráfico de média e amplitude dos 25 lotes de massa da pizzaria. Todas as médias ficam entre '
      f'{br(L1["lic"])} e {br(L1["lsc"])} g, e todas as amplitudes abaixo de {br(L1["lscr"])} g, sem nenhuma das regras de sinal: o processo está em controle.">']
carta(p8, EX1, R1, media, 50, 790, 40, 180, 386, 415, "MÉDIA DO LOTE (g)", L1["lc"], L1["lsc"], L1["lic"], fmt_ex(EX1))
carta(p8, EX1, R1, amp, 50, 790, 230, 330, 0, 42, "AMPLITUDE DO LOTE (g)", L1["rb"], L1["lscr"], None, fmt_ex(EX1))
p8.append("      </svg>")

r1h = R1["hist"]
p9 = ['      <svg viewBox="0 0 900 270" role="img" aria-label="Histograma das 125 bolas da pizzaria. ' + " ".join(f"De {nv(EX1, a)} a {nv(EX1, b)} g: {c}." for (a, b), c in zip(classes(EX1), r1h["cont"]))
      + f' Três bolas ficam fora da especificação: {", ".join(nv(EX1, v) for g in EX1["subs"] for v in g["v"] if v < 380 or v > 420)} g, todas em lotes com média dentro do critério.">']
hist(p9, EX1, 40, 560, 50, 220, 34, cor=lambda a, b: "f3" if b <= 380 or a >= 420 else "f1")
p9.append(f'        <text class="mu" x="300" y="256" font-size="11"{MID}>Peso de cada bola, em gramas</text>')
p9.append('        <rect class="bx" x="600" y="40" width="288" height="190"/>')
yy = lines(p9, f"{r1h['fora']} de {r1h['n']} bolas fora", 616, 68, 34, fs=13, cls="b", step=16, maxl=1)
lines(p9, "As três vieram de lotes com média dentro de 380 a 420 g. O plano de controle registrava só a média, e o forno recebe cada bola: a média aprovava bolas fora.",
      616, yy + 10, 40, fs=11, step=15, maxl=8)
p9.append("      </svg>")

# ------------------------------------------------------------------ figura 10: indústria, amplitude e histogramas da base e do acompanhamento
fa2 = R2["fases"]
vb = [v for k, g in enumerate(EX2["subs"]) if fa2[k] == BASE for v in g["v"]]
va = [v for k, g in enumerate(EX2["subs"]) if fa2[k] == ACOMP for v in g["v"]]
p10 = ['      <svg viewBox="0 0 900 270" role="img" aria-label="Histogramas da espessura na indústria. Na base, de 04 a 10/07, os valores ficam entre '
       f'{nv(EX2, min(vb))} e {nv(EX2, max(vb))} µm, estreitos e no centro. No acompanhamento, de 11 a 16/07, se espalham de {nv(EX2, min(va))} a {nv(EX2, max(va))} µm e descem: '
       'dois pontos abaixo de 38 µm.">']
for k, (vals, tit, cor) in enumerate(((vb, f"Base: {len(vb)} medições, 04 a 10/07", "f1"), (va, f"Acompanhamento: {len(va)} medições, 11 a 16/07", "f2"))):
    x0 = 50 + k * 440
    hist(p10, EX2, x0, x0 + 380, 60, 210, 45, cor=lambda a, b, c=cor: "f3" if b <= 38 else c, valores=vals)
    p10.append(f'        <text class="b" x="{x0 + 190}" y="250" font-size="12"{MID}>{tit}</text>')
p10.append("      </svg>")

# ------------------------------------------------------------------ figura 11: interativa, médias da indústria
X0, X1, Y0, Y1 = 60, 790, 30, 250
LO, HI = 37.9, 41.3
n2 = len(EX2["subs"])
pxi = lambda k: X0 + 16 + k * (X1 - X0 - 32) / (n2 - 1)  # noqa: E731
pyi = lambda v: Y1 - (v - LO) * (Y1 - Y0) / (HI - LO)  # noqa: E731
ch = [f'      <svg id="bars" viewBox="0 0 900 320" role="img" aria-label="Médias de espessura das 25 bobinas da indústria, com a linha central de {br(L2["lc"], 2)} µm e os limites de '
      f'{br(L2["lic"], 2)} e {br(L2["lsc"], 2)} µm. ' + " ".join(f'{k + 1}: {br(media(g["v"]), 2)}{" (" + R2["sg"][k].lower() + ")" if R2["sg"][k] else ""}.' for k, g in enumerate(EX2["subs"])) + '">']
xb_ = pxi(R2["fases"].index(ACOMP)) - (pxi(1) - pxi(0)) / 2
ch.append(f'        <rect class="lane" x="{xb_:.1f}" y="{Y0}" width="{X1 - xb_:.1f}" height="{Y1 - Y0}"/>')
ch.append(f'        <text class="mono mu" x="{X0 + 8}" y="{Y0 + 14}" font-size="10">BASE</text><text class="mono mu" x="{xb_ + 8:.1f}" y="{Y0 + 14}" font-size="10">ACOMPANHAMENTO</text>')
for v in (38, 39, 40, 41):
    ch.append(f'        <line class="grid" x1="{X0}" y1="{pyi(v):.1f}" x2="{X1}" y2="{pyi(v):.1f}"/><text class="mu" x="{X0 - 8}" y="{pyi(v) + 4:.1f}" font-size="10.5"{END}{TNUM}>{v}</text>')
ch.append(f'        <line class="esp" x1="{X0}" y1="{pyi(38):.1f}" x2="{X1}" y2="{pyi(38):.1f}"/><text class="b halo" x="{X1 + 6}" y="{pyi(38) + 4:.1f}" font-size="10.5">LIE 38</text>')
for v, cls, rot in ((L2["lsc"], "lim", "LSC"), (L2["lc"], "ctr", "LC"), (L2["lic"], "lim", "LIC")):
    ch.append(f'        <line class="{cls}" x1="{X0}" y1="{pyi(v):.1f}" x2="{X1}" y2="{pyi(v):.1f}"/>')
    ch.append(f'        <text class="mu halo" x="{X1 + 6}" y="{pyi(v) + 4:.1f}" font-size="10.5"{TNUM}>{rot} {br(v, 2)}</text>')
ptsi = [(pxi(k), pyi(media(g["v"]))) for k, g in enumerate(EX2["subs"])]
ch.append('        <path class="ser" d="' + " ".join(f'{"M" if k == 0 else "L"}{x:.1f} {y:.1f}' for k, (x, y) in enumerate(ptsi)) + '"/>')
hits = []
for k, ((x, y), g) in enumerate(zip(ptsi, EX2["subs"])):
    s, fa = R2["sg"][k], R2["fases"][k]
    cls = "p-exc" if fa == EXCL else "p-sig" if s else "p-ok"
    ch.append(f'        <circle class="pt-c {cls}" data-k="{k}" cx="{x:.1f}" cy="{y:.1f}" r="{5 if cls != "p-ok" else 4.2}"/>')
    if k % 2 == 0:
        ch.append(f'        <text class="mu" x="{x:.1f}" y="{Y1 + 16}" font-size="10"{MID}{TNUM}>{g["data"].strftime("%d/%m")}</text>')
    st = s or ("Excluído da base" if fa == EXCL else "Sem sinal")
    hits.append(f'        <rect class="hit" x="{x - 12:.1f}" y="{Y0}" width="24" height="{Y1 - Y0}" tabindex="0" role="img" '
                f'aria-label="Bobina {k + 1}, {g["data"].strftime("%d/%m")}, {g["id"]}: média {br(media(g["v"]), 2)} µm, amplitude {br(amp(g["v"]), 1)} µm. {st}." '
                f'data-k="{k}" data-n="Bobina {k + 1} · {g["data"].strftime("%d/%m")} · {g["id"]}" data-s="{br(media(g["v"]), 2)} µm" '
                f'data-d="amplitude {br(amp(g["v"]), 1)} µm" data-p="{st.lower()}" data-cx="{x:.1f}" data-cy="{y:.1f}"/>')
k1 = R2["primeiro"]
x1_, y1_ = ptsi[k1]
ch.append(f'        <line class="ln-mu" x1="{x1_:.1f}" y1="{y1_ + 8:.1f}" x2="{x1_:.1f}" y2="{pyi(38.6):.1f}"/>')
ch.append(f'        <text class="b halo" x="{x1_ - 6:.1f}" y="{pyi(38.6) + 4:.1f}" font-size="10.5"{END}>primeiro sinal: {EX2["subs"][k1]["data"].strftime("%d/%m")}</text>')
ch.append(f'        <text class="mu" x="{(X0 + X1) / 2}" y="{Y1 + 40}" font-size="11"{MID}>A parada da extrusora 3 foi em {PARADA.strftime("%d/%m")}, cinco dias depois do primeiro sinal.</text>')
ch += hits + ["      </svg>"]
tb = ['        <table class="aud">', '          <thead><tr><th>Bobina</th><th>Data</th><th class="c">Média</th><th class="c">Amplitude</th><th>Fase</th><th>Sinal</th></tr></thead>', '          <tbody>']
for k, g in enumerate(EX2["subs"]):
    tb.append(f'            <tr><td>{k + 1}</td><td>{g["data"].strftime("%d/%m")} · {g["id"]}</td><td class="c">{br(media(g["v"]), 2)}</td><td class="c">{br(amp(g["v"]), 1)}</td>'
              f'<td>{R2["fases"][k]}</td><td>{R2["sg"][k] or "—"}</td></tr>')
tb += ['          </tbody>', '        </table>']

# ------------------------------------------------------------------ figura 12: nas normas
ISOP = [("ISO 9001, 9.1", "Determinar o que medir, os métodos de análise, quando medir e quando analisar.", "análise dos dados"),
        ("ISO 9001, 8.5.1", "Monitorar nas etapas certas, com recursos de medição adequados.", "o subgrupo e a reação"),
        ("ISO 7870-2", "A norma dos gráficos de controle de Shewhart: tipos, limites e regras.", "os limites e os sinais"),
        ("ISO 22514", "A série sobre capacidade e desempenho de processos.", "Cp e Cpk")]
iso = ['      <svg viewBox="0 0 900 190" role="img" aria-label="As normas ligadas ao controle estatístico. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in ISOP) + '">']
for k, (a, b, c) in enumerate(ISOP):
    x = 10 + k * 222
    iso.append(f'        <rect class="bx" x="{x}" y="14" width="214" height="164"/>')
    iso.append(f'        <rect class="hd-ink" x="{x}" y="14" width="214" height="34"/>')
    iso.append(f'        <text class="b t-ground" x="{x + 12}" y="36" font-size="11.5">{escape(a)}</text>')
    lines(iso, b, x + 12, 70, 32, fs=11.5, step=16, maxl=4)
    lines(iso, "Neste estudo: " + c, x + 12, 146, 34, fs=11, cls="mu", step=15, maxl=2)
iso.append("      </svg>")

# ------------------------------------------------------------------ tabela das constantes
const = "\n".join([
    f'        <tr><td><strong>Linha central da média</strong></td><td>Média das médias dos subgrupos da base</td><td class="num">{br(L1["lc"], 1)} g</td><td class="num">{br(L2["lc"], 2)} µm</td></tr>',
    f'        <tr><td><strong>Amplitude média (R̄)</strong></td><td>Média das amplitudes da base</td><td class="num">{br(L1["rb"], 1)} g</td><td class="num">{br(L2["rb"], 2)} µm</td></tr>',
    f'        <tr><td><strong>Limites da média</strong></td><td>Linha central ± {br(A2, 3)} × R̄</td><td class="num">{br(L1["lic"], 1)} a {br(L1["lsc"], 1)} g</td>'
    f'<td class="num">{br(L2["lic"], 2)} a {br(L2["lsc"], 2)} µm</td></tr>',
    f'        <tr><td><strong>Limite da amplitude</strong></td><td>{br(D4, 3)} × R̄ (o inferior é zero)</td><td class="num">{br(L1["lscr"], 1)} g</td><td class="num">{br(L2["lscr"], 2)} µm</td></tr>',
    f'        <tr><td><strong>Desvio estimado (σ)</strong></td><td>R̄ ÷ {br(D2, 3)}</td><td class="num">{br(L1["sigma"], 2)} g</td><td class="num">{br(L2["sigma"], 3)} µm</td></tr>',
])

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))
c1, c2 = R1["cap"], R2["cap"]
NUMS = {"{{CP1}}": br(c1["cp"], 2), "{{CPK1}}": br(c1["cpk"], 2), "{{CP2}}": br(c2["cp"], 2), "{{CPK2}}": br(c2["cpk"], 2), "{{SIG1}}": br(L1["sigma"], 1),
        "{{LIC1}}": br(L1["lic"], 1), "{{LSC1}}": br(L1["lsc"], 1), "{{LIC2}}": br(L2["lic"], 2), "{{LSC2}}": br(L2["lsc"], 2), "{{LC2}}": br(L2["lc"], 2),
        "{{PRIM}}": EX2["subs"][R2["primeiro"]]["data"].strftime("%d/%m"), "{{NSIN2}}": str(sum(1 for k, s in enumerate(R2["sg"]) if s and R2["fases"][k] == ACOMP)),
        "{{FORA1}}": str(R1["hist"]["fora"]), "{{FORA2}}": str(R2["hist"]["fora"]), "{{STAT1}}": c1["status"].lower(), "{{STAT2}}": c2["status"].lower()}
assert c1["status"] == NAOCAPAZ and c2["status"] == CAPAZ and LIMITE

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--DUAS-->", "\n".join(f1)), ("<!--FLUXO-->", "\n".join(et)), ("<!--FORMAS-->", "\n".join(fo)), ("<!--ANATOMIA-->", "\n".join(an)),
                 ("<!--CONST-->", const), ("<!--REGRAS-->", "\n".join(rg)), ("<!--CAPAC-->", "\n".join(cap)), ("<!--LIMESP-->", "\n".join(lc_)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1FIG-->", "\n".join(p8)), ("<!--EX1HIST-->", "\n".join(p9)), ("<!--EX1TAB-->", tab_dados(EX1, R1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2FIG-->", "\n".join(p10)), ("<!--EX2TAB-->", tab_dados(EX2, R2)),
                 ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
for k, v in NUMS.items():
    body = body.replace(k, v)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"
assert "{{" not in body, re.findall(r"\{\{\w+\}\}", body)
assert all(conf(g) == "OK" for ex in (EX1, EX2) for g in ex["subs"]) and fora_espec

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Histograma e CEP</title>")
assert "CEP" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'))
