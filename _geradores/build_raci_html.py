# -*- coding: utf-8 -*-
"""Monta treinamento-raci.html: CSS herdado do estudo de PDCA + corpo próprio + matrizes e gráfico dos exemplos."""
import os
import re
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raci_data import EX1, EX2, EX3, NOMES, carga  # noqa: E402

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# tira as quatro cores das fases do PDCA e põe as quatro dos papéis depois da cor de destaque
css, n = re.subn(r"\n\s*--[pdca]:#\w+; --[pdca]-tint:#\w+;", "", css)
assert n == 12, n
LIGHT = "\n  --r:#1E7B73; --r-tint:#D9EEEB;\n  --a:#7A4A9A; --a-tint:#E9DEF1;\n  --c:#A96A12; --c-tint:#F6E8CF;\n  --i:#5B6B76; --i-tint:#E3E8EB;"
DARK = "\n  --r:#5FC6BA; --r-tint:#15332F;\n  --a:#C09ADB; --a-tint:#2E2139;\n  --c:#E2AC4F; --c-tint:#3A2C12;\n  --i:#9BABB6; --i-tint:#26343D;"
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)

drop = (".tiles .p{", ".k.p{", "svg .bx-p{", "svg .bx-d{", "svg .bx-c{", "svg .bx-a{", "table.pdca",
        "svg .band{", "svg .series{", "svg .pt{", "svg .pt.on-hit{", "svg .goal{", "svg .xh{", "svg .root{",
        "/* Ficha do ciclo")
css = "\n".join(l for l in css.split("\n") if not l.startswith(drop))
css = css.replace("accent-color:var(--c)", "accent-color:var(--r)")
for v in ("var(--p)", "var(--d)"):
    assert v not in css, v

extra = """
/* Papéis */
.tiles .r{background:var(--r)} .tiles .a{background:var(--a)} .tiles .c{background:var(--c)} .tiles .i{background:var(--i)}
.k.r{background:var(--r)} .k.a{background:var(--a)} .k.c{background:var(--c)} .k.i{background:var(--i)}
.k + .k{margin-left:2px}
svg .bx-r{fill:var(--r-tint);stroke:var(--r);stroke-width:1.5} svg .hd-r{fill:var(--r)}
svg .bx-a{fill:var(--a-tint);stroke:var(--a);stroke-width:1.5} svg .hd-a{fill:var(--a)}
svg .bx-c{fill:var(--c-tint);stroke:var(--c);stroke-width:1.5} svg .hd-c{fill:var(--c)}
svg .bx-i{fill:var(--i-tint);stroke:var(--i);stroke-width:1.5} svg .hd-i{fill:var(--i)}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Matriz dos exemplos */
table.raci{min-width:760px;font-size:.86rem}
table.raci th.p{text-align:center;font-size:.76rem;line-height:1.25;width:11%}
table.raci td.n{width:5%;font-weight:600;color:var(--muted)}
table.raci td.l{text-align:center;white-space:nowrap}
table.raci td.l .k{width:1.7em;height:1.7em;font-size:.9em}
.leg{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:.84rem;color:var(--muted);margin:0;padding:0;list-style:none;flex-direction:row}
.leg .k{margin-right:6px}

/* Ficha da matriz (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)


def tile(letra):
    if not letra:
        return ""
    return "".join(f'<span class="k {l.lower()}">{l}</span>' for l in letra.split("/"))


def tabela(ex):
    o = ['  <div class="tbl">', '    <table class="raci">',
         '      <thead><tr><th>#</th><th>Atividade</th>' + "".join(f'<th class="p">{escape(p)}</th>' for p in ex["papeis"]) + '</tr></thead>',
         '      <tbody>']
    for k, (atv, cel) in enumerate(ex["linhas"], 1):
        o.append(f'        <tr><td class="n">{k}</td><td>{escape(atv)}</td>'
                 + "".join(f'<td class="l">{tile(c)}</td>' for c in cel) + '</tr>')
    o += ['      </tbody>', '    </table>', '  </div>',
          '  <ul class="leg">' + "".join(f'<li><span class="k {l.lower()}">{l}</span>{NOMES[l]}</li>' for l in "RACI")
          + '<li>Duas letras na mesma célula: o papel executa e responde pelo resultado.</li></ul>']
    return "\n".join(o)


# ---- gráfico de carga por papel (exemplo 2)
rows = carga(EX2)
natv = len(EX2["linhas"])
X0, U, TOP, RH, BH = 230, 60, 30, 34, 18
bottom = TOP + RH * len(rows)
H = bottom + 70
out = [f'      <svg id="bars" viewBox="0 0 900 {H}" role="img" aria-label="Gráfico de barras empilhadas com a carga de cada papel na matriz do exemplo 2: '
       + "; ".join(f'{r["papel"]}, R {r["R"]}, A {r["A"]}, C {r["C"]}, I {r["I"]}' for r in rows) + '.">']
for v in range(0, 11, 2):
    x = X0 + v * U
    out.append(f'        <line class="grid" x1="{x}" y1="{TOP - 6}" x2="{x}" y2="{bottom}"/>')
    out.append(f'        <text class="mu" x="{x}" y="{bottom + 16}" font-size="11" text-anchor="middle" style="font-variant-numeric:tabular-nums">{v}</text>')
out.append(f'        <text class="mono mu" x="{X0 + 5 * U}" y="{bottom + 36}" font-size="10" text-anchor="middle">PARTICIPAÇÕES NAS {natv} ATIVIDADES</text>')
for k, r in enumerate(rows):
    y = TOP + RH * k + (RH - BH) / 2
    out.append(f'        <text x="20" y="{y + 13:.1f}" font-size="11.5">{escape(r["papel"])}</text>')
    x = X0
    partes = [(l, r[l]) for l in "RACI" if r[l]]
    for j, (l, v) in enumerate(partes):
        w = v * U - 2
        if j == len(partes) - 1:
            x1 = x + w
            out.append(f'        <path class="seg hd-{l.lower()}" data-k="{k}" d="M{x} {y:.1f} H{x1 - 4} Q{x1} {y:.1f} {x1} {y + 4:.1f} V{y + BH - 4:.1f} '
                       f'Q{x1} {y + BH:.1f} {x1 - 4} {y + BH:.1f} H{x} Z"/>')
        else:
            out.append(f'        <rect class="seg hd-{l.lower()}" data-k="{k}" x="{x}" y="{y:.1f}" width="{w}" height="{BH}"/>')
        out.append(f'        <text class="on b" x="{x + w / 2:.1f}" y="{y + 13:.1f}" font-size="11" text-anchor="middle">{l} {v}</text>')
        x += v * U
lx, ly = 20, bottom + 60
for l in "RACI":
    out.append(f'        <rect class="hd-{l.lower()}" x="{lx}" y="{ly - 10}" width="14" height="12"/>')
    out.append(f'        <text x="{lx + 21}" y="{ly}" font-size="11.5">{l} · {NOMES[l]}</text>')
    lx += 150
for k, r in enumerate(rows):
    part = sum(1 for _, cel in EX2["linhas"] if cel[k])
    tot = r["R"] + r["A"] + r["C"] + r["I"]
    out.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" '
               f'aria-label="{escape(r["papel"])}: R {r["R"]}, A {r["A"]}, C {r["C"]}, I {r["I"]}" data-k="{k}" data-p="{escape(r["papel"])}" '
               f'data-r="{r["R"]}" data-a="{r["A"]}" data-c="{r["C"]}" data-i="{r["I"]}" '
               f'data-n="Participa de {part} das {natv} atividades" data-x="{X0 + tot * U / 2:.1f}"/>')
out.append("      </svg>")

tb = ['        <table>', '          <thead><tr><th>Papel</th><th>R</th><th>A</th><th>C</th><th>I</th><th>Atividades de que participa</th></tr></thead>', '          <tbody>']
for k, r in enumerate(rows):
    part = sum(1 for _, cel in EX2["linhas"] if cel[k])
    tb.append(f'            <tr><td>{escape(r["papel"])}</td><td class="num">{r["R"]}</td><td class="num">{r["A"]}</td><td class="num">{r["C"]}</td>'
              f'<td class="num">{r["I"]}</td><td class="num">{part} de {natv}</td></tr>')
tb += ['          </tbody>', '        </table>']

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--CARGA-->", "\n".join(out)), ("<!--CARGATABLE-->", "\n".join(tb)),
                 ("<!--EX1-->", tabela(EX1)), ("<!--EX2-->", tabela(EX2)), ("<!--EX3-->", tabela(EX3))):
    assert tag in body, tag
    body = body.replace(tag, val)

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Matriz RACI na prática</title>")
assert "Matriz RACI" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
for name, ex in (("EX1", EX1), ("EX2", EX2), ("EX3", EX3)):
    print(name, len(ex["linhas"]), "atividades |", [(c["papel"].split()[0], c["R"], c["A"], c["C"], c["I"]) for c in carga(ex)])
