# -*- coding: utf-8 -*-
"""Monta treinamento-gut.html: CSS herdado do estudo de PDCA + corpo próprio + tabelas e gráfico dos exemplos."""
import os
import re
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gut_data import ALTA, EX1, EX2, EX3, MEDIA, faixa, ordenar, pontos  # noqa: E402

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

pairs = [
    ("--p:#2B5C8A; --p-tint:#DCE8F3;", "--g:#7A4A9A; --g-tint:#E9DEF1;"),
    ("--d:#A96A12; --d-tint:#F6E8CF;", "--u:#A96A12; --u-tint:#F6E8CF;"),
    ("--c:#1E7B73; --c-tint:#D9EEEB;", "--t:#1E7B73; --t-tint:#D9EEEB;"),
    ("  --a:#B0413E; --a-tint:#F5DEDC;\n", ""),
    ("--p:#86B7E3; --p-tint:#1B2F42;", "--g:#C09ADB; --g-tint:#2E2139;"),
    ("--d:#E2AC4F; --d-tint:#3A2C12;", "--u:#E2AC4F; --u-tint:#3A2C12;"),
    ("--c:#5FC6BA; --c-tint:#15332F;", "--t:#5FC6BA; --t-tint:#15332F;"),
]
for a, b in pairs:
    assert a in css, a
    css = css.replace(a, b)
css = re.sub(r"\n\s*--a:#EC8E89; --a-tint:#3D1F1E;", "", css)

drop = (".tiles .p{", ".k.p{", "svg .bx-p{", "svg .bx-d{", "svg .bx-c{", "svg .bx-a{", "table.pdca",
        "svg .band{", "svg .series{", "svg .pt{", "svg .pt.on-hit{", "svg .goal{", "svg .xh{", "svg .root{",
        "/* Ficha do ciclo")
css = "\n".join(l for l in css.split("\n") if not l.startswith(drop))
css = css.replace("accent-color:var(--c)", "accent-color:var(--t)")
for v in ("var(--p)", "var(--d)", "var(--c)", "var(--a)", "--a:", "--a-tint"):
    assert v not in css, v

extra = """
/* Critérios */
.tiles .g{background:var(--g)} .tiles .u{background:var(--u)} .tiles .t{background:var(--t)}
.k.g{background:var(--g)} .k.u{background:var(--u)} .k.t{background:var(--t)}
svg .bx-g{fill:var(--g-tint);stroke:var(--g);stroke-width:1.5} svg .hd-g{fill:var(--g)}
svg .bx-u{fill:var(--u-tint);stroke:var(--u);stroke-width:1.5} svg .hd-u{fill:var(--u)}
svg .bx-t{fill:var(--t-tint);stroke:var(--t);stroke-width:1.5} svg .hd-t{fill:var(--t)}
svg .lv-g{fill:var(--g);fill-opacity:.36} svg .lv-u{fill:var(--u);fill-opacity:.36} svg .lv-t{fill:var(--t);fill-opacity:.36}
svg .bar{fill:var(--accent)}
svg .ref{stroke:var(--muted);stroke-width:1;stroke-dasharray:4 3}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabela dos exemplos */
table.gut th.g{background:var(--g);color:var(--on-hue)} table.gut th.u{background:var(--u);color:var(--on-hue)} table.gut th.t{background:var(--t);color:var(--on-hue)}
table.gut th.n, table.gut td.n{text-align:center;width:7%}
table.gut td.n{font:400 .86rem var(--mono);font-variant-numeric:tabular-nums}
table.gut td.g{background:var(--g-tint)} table.gut td.u{background:var(--u-tint)} table.gut td.t{background:var(--t-tint)}
table.gut td.pts{font-weight:600}
table.gut td.cod{font-weight:600;color:var(--muted);width:8%}
table.gut td small{display:block;color:var(--muted);font-size:.8rem}

/* Ficha da matriz (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)


def tabela(ex):
    o = ['  <div class="tbl">', '    <table class="gut">',
         '      <thead><tr><th class="n">Ordem</th><th>Código</th><th>Problema</th><th class="n g">G</th><th class="n u">U</th>'
         '<th class="n t">T</th><th class="n">Pontos</th><th style="width:17%">Prioridade</th></tr></thead>', '      <tbody>']
    for i, p in enumerate(ordenar(ex["itens"]), 1):
        v = pontos(p)
        alerta = "<small>gravidade máxima</small>" if p["g"] == 5 else ""
        o.append(f'        <tr><td class="n">{i}º</td><td class="cod">{p["k"]}</td><td>{escape(p["txt"])}</td>'
                 f'<td class="n g">{p["g"]}</td><td class="n u">{p["u"]}</td><td class="n t">{p["t"]}</td>'
                 f'<td class="n pts">{v}</td><td>{faixa(v)}{alerta}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


# ---- gráfico de barras do exemplo 1
rows = ordenar(EX1["itens"])
X0, SC, TOP, RH, BH = 360, 3.4, 44, 27, 14
bottom = TOP + RH * len(rows)
H = bottom + 44
sx = lambda v: round(X0 + v * SC, 1)
out = [f'      <svg id="bars" viewBox="0 0 900 {H}" role="img" aria-label="Gráfico de barras horizontais com a pontuação dos oito problemas do exemplo 1, '
       f'do maior para o menor: {", ".join(p["k"] + " com " + str(pontos(p)) for p in rows)}. A faixa média começa em {MEDIA} pontos e a alta em {ALTA}.">']
for v in (0, 25, 50, 75, 100, 125):
    out.append(f'        <line class="grid" x1="{sx(v)}" y1="{TOP - 6}" x2="{sx(v)}" y2="{bottom}"/>')
    out.append(f'        <text class="mu" x="{sx(v)}" y="{bottom + 16}" font-size="11" text-anchor="middle" style="font-variant-numeric:tabular-nums">{v}</text>')
out.append(f'        <text class="mu" x="{sx(0) + 5}" y="{TOP - 14}" font-size="11">baixa: até {MEDIA - 1}</text>')
for v, lab in ((MEDIA, f"média: de {MEDIA} a {ALTA - 1}"), (ALTA, f"alta: {ALTA} ou mais")):
    out.append(f'        <line class="ref" x1="{sx(v)}" y1="{TOP - 16}" x2="{sx(v)}" y2="{bottom}"/>')
    out.append(f'        <text class="mu" x="{sx(v) + 5}" y="{TOP - 14}" font-size="11">{lab}</text>')
out.append(f'        <text class="mono mu" x="{sx(62.5)}" y="{bottom + 36}" font-size="10" text-anchor="middle">PONTOS (G × U × T)</text>')
for k, p in enumerate(rows):
    v = pontos(p)
    y = TOP + RH * k + (RH - BH) / 2
    x1 = sx(v)
    out.append(f'        <text class="b mu" x="20" y="{y + 11.5:.1f}" font-size="11.5">{p["k"]}</text>')
    alerta = '<tspan class="mu"> · gravidade 5</tspan>' if p["g"] == 5 else ""
    out.append(f'        <text x="46" y="{y + 11.5:.1f}" font-size="11.5">{escape(p["curto"])}{alerta}</text>')
    r = min(4, (x1 - X0) / 2)
    out.append(f'        <path class="bar" data-k="{p["k"]}" d="M{X0} {y:.1f} H{x1 - r:.1f} Q{x1} {y:.1f} {x1} {y + r:.1f} V{y + BH - r:.1f} '
               f'Q{x1} {y + BH:.1f} {x1 - r:.1f} {y + BH:.1f} H{X0} Z"/>')
    out.append(f'        <text class="b" x="{x1 + 7}" y="{y + 11.5:.1f}" font-size="11.5" style="font-variant-numeric:tabular-nums">{v}</text>')
for k, p in enumerate(rows):
    v = pontos(p)
    y = TOP + RH * k
    out.append(f'        <rect class="hit" x="14" y="{y}" width="872" height="{RH}" tabindex="0" role="img" '
               f'aria-label="{p["k"]}, {escape(p["curto"])}: {v} pontos, prioridade {faixa(v).lower()}" data-k="{p["k"]}" data-o="{k + 1}" '
               f'data-v="{v}" data-g="{p["g"]}" data-u="{p["u"]}" data-t="{p["t"]}" data-p="{faixa(v).lower()}" data-x="{sx(v)}"/>')
out.append("      </svg>")

tb = ['        <table>', '          <thead><tr><th>Ordem</th><th>Código</th><th>Problema</th><th>G</th><th>U</th><th>T</th><th>Pontos</th><th>Prioridade</th></tr></thead>', '          <tbody>']
for i, p in enumerate(rows, 1):
    v = pontos(p)
    tb.append(f'            <tr><td>{i}º</td><td>{p["k"]}</td><td>{escape(p["txt"])}</td><td class="num">{p["g"]}</td><td class="num">{p["u"]}</td>'
              f'<td class="num">{p["t"]}</td><td class="num">{v}</td><td>{faixa(v)}</td></tr>')
tb += ['          </tbody>', '        </table>']

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--BARS-->", "\n".join(out)), ("<!--BARTABLE-->", "\n".join(tb)),
                 ("<!--EX1-->", tabela(EX1)), ("<!--EX2-->", tabela(EX2)), ("<!--EX3-->", tabela(EX3))):
    assert tag in body, tag
    body = body.replace(tag, val)
# níveis da escala: tom único, do claro ao escuro
for a, b in ((".3", ".08"), (".45", ".15"), (".62", ".22"), (".8", ".29")):
    body = body.replace(f'style="fill-opacity:{a}"', f'style="fill-opacity:{b}"')

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Matriz GUT na prática</title>")
assert "Matriz GUT" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
for name, ex in (("EX1", EX1), ("EX2", EX2), ("EX3", EX3)):
    print(name, [(p["k"], pontos(p), faixa(pontos(p))) for p in ordenar(ex["itens"])])
