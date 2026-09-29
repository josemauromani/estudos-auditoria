# -*- coding: utf-8 -*-
"""Monta treinamento-5w2h.html: CSS herdado do estudo de PDCA + corpo próprio + tabelas e cronograma dos exemplos."""
import os
import re
import sys
from datetime import date, timedelta
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w5_data import EX1, EX2, EX3, dm, quando  # noqa: E402

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

for a, b in [("--p:#2B5C8A; --p-tint:#DCE8F3;", "--w:#2B5C8A; --w-tint:#DCE8F3;"),
             ("--d:#A96A12; --d-tint:#F6E8CF;", "--h:#A96A12; --h-tint:#F6E8CF;"),
             ("--p:#86B7E3; --p-tint:#1B2F42;", "--w:#86B7E3; --w-tint:#1B2F42;"),
             ("--d:#E2AC4F; --d-tint:#3A2C12;", "--h:#E2AC4F; --h-tint:#3A2C12;")]:
    assert a in css, a
    css = css.replace(a, b)
css, n = re.subn(r"\n\s*--[ca]:#\w+; --[ca]-tint:#\w+;", "", css)
assert n == 6, n

drop = (".tiles .p{", ".k.p{", "svg .bx-p{", "svg .bx-d{", "svg .bx-c{", "svg .bx-a{", "table.pdca",
        "svg .band{", "svg .series{", "svg .pt{", "svg .pt.on-hit{", "svg .goal{", "svg .xh{", "svg .root{",
        "/* Ficha do ciclo")
css = "\n".join(l for l in css.split("\n") if not l.startswith(drop))
css = css.replace("accent-color:var(--c)", "accent-color:var(--w)")
for v in ("var(--p)", "var(--d)", "var(--c)", "var(--a)"):
    assert v not in css, v

extra = """
/* Perguntas */
.tiles .w{background:var(--w)} .tiles .h{background:var(--h)}
.k.w{background:var(--w)} .k.h{background:var(--h)}
svg .bx-w{fill:var(--w-tint);stroke:var(--w);stroke-width:1.5} svg .hd-w{fill:var(--w)}
svg .bx-h{fill:var(--h-tint);stroke:var(--h);stroke-width:1.5} svg .hd-h{fill:var(--h)}
svg .ref{stroke:var(--ink);stroke-width:1;stroke-dasharray:4 3}
svg .st-ok{fill:var(--good)} svg .st-late{fill:var(--bad)} svg .st-run{fill:var(--accent)} svg .st-wait{fill:var(--muted);fill-opacity:.55}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabela dos planos */
table.plan{min-width:840px;font-size:.8rem;line-height:1.35}
table.plan th, table.plan td{padding:8px 9px}
table.plan th.w{background:var(--w);color:var(--on-hue)} table.plan th.h{background:var(--h);color:var(--on-hue)}
table.plan th small{display:block;font:400 .68rem/1.2 var(--mono);letter-spacing:.08em;opacity:.9}
table.plan td.cod{font-weight:600;color:var(--muted)}
table.plan td.w1{background:var(--w-tint)}
table.plan td.nw{white-space:nowrap}

/* Exercício com sete opções */
.quiz.wide .q{grid-template-columns:minmax(0,1fr)}
.quiz.wide .opts{flex-wrap:wrap}
.quiz.wide .opts button{width:auto;height:36px;padding:0 12px;font:600 .85rem/1 var(--body)}

/* Ficha do plano (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)


def tabela(ex):
    o = ['  <div class="tbl">', '    <table class="plan">',
         '      <thead><tr><th style="width:5%">#</th><th class="w" style="width:19%">O quê<small>WHAT</small></th>'
         '<th class="w" style="width:17%">Por quê<small>WHY</small></th><th class="w" style="width:11%">Onde<small>WHERE</small></th>'
         '<th class="w" style="width:9%">Quando<small>WHEN</small></th><th class="w" style="width:11%">Quem<small>WHO</small></th>'
         '<th class="h" style="width:18%">Como<small>HOW</small></th><th class="h">Quanto<small>HOW MUCH</small></th></tr></thead>', '      <tbody>']
    for p in ex["itens"]:
        o.append(f'        <tr><td class="cod">{p["k"]}</td><td class="w1"><strong>{escape(p["oque"])}</strong></td><td>{escape(p["porque"])}</td>'
                 f'<td>{escape(p["onde"])}</td><td>{quando(p)}</td><td>{escape(p["quem"])}</td>'
                 f'<td>{escape(p["como"])}</td><td>{escape(p["custo_txt"])}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


# ---- cronograma do exemplo 1
rows = EX1["itens"]
status = EX1["ref_status"]
ref = EX1["ref"]
T0, T1 = date(2026, 7, 27), date(2026, 9, 21)
X0, X1, TOP, RH, BH = 330, 760, 50, 30, 14
ppd = (X1 - X0) / (T1 - T0).days
sx = lambda d: round(X0 + (d - T0).days * ppd, 1)
bottom = TOP + RH * len(rows)
H = bottom + 66
CLS = {"Concluída": "st-ok", "Atrasada": "st-late", "Em andamento": "st-run", "Não iniciada": "st-wait"}
resumo = "; ".join(f'{p["k"]}, {p["curto"].lower()}, de {dm(p["inicio"])} a {dm(p["prazo"])}, {s.lower()}' for p, s in zip(rows, status))
out = [f'      <svg id="gantt" viewBox="0 0 900 {H}" role="img" aria-label="Cronograma das seis ações do exemplo 1, com a situação em {dm(ref)}: {resumo}.">']
d = T0
while d <= T1:
    out.append(f'        <line class="grid" x1="{sx(d)}" y1="{TOP - 6}" x2="{sx(d)}" y2="{bottom}"/>')
    out.append(f'        <text class="mu" x="{sx(d)}" y="{bottom + 16}" font-size="10.5" text-anchor="middle" style="font-variant-numeric:tabular-nums">{dm(d)}</text>')
    d += timedelta(days=7)
out.append(f'        <line class="ref" x1="{sx(ref)}" y1="{TOP - 22}" x2="{sx(ref)}" y2="{bottom}"/>')
out.append(f'        <text x="{sx(ref) + 6}" y="{TOP - 14}" font-size="11"><tspan class="b">situação em {dm(ref)}</tspan></text>')
out.append(f'        <text class="mono mu" x="{X1 + 16}" y="{TOP - 14}" font-size="10">SITUAÇÃO</text>')
out.append(f'        <text class="mono mu" x="{(X0 + X1) / 2}" y="{bottom + 36}" font-size="10" text-anchor="middle">SEMANAS DE 2026</text>')
for k, (p, s) in enumerate(zip(rows, status)):
    y = TOP + RH * k + (RH - BH) / 2
    a, b = sx(p["inicio"]), sx(p["prazo"] + timedelta(days=1))
    out.append(f'        <text class="b mu" x="20" y="{y + 11.5:.1f}" font-size="11.5">{p["k"]}</text>')
    out.append(f'        <text x="46" y="{y + 11.5:.1f}" font-size="11.5">{escape(p["curto"])}</text>')
    out.append(f'        <rect class="bar {CLS[s]}" data-k="{p["k"]}" x="{a}" y="{y:.1f}" width="{b - a:.1f}" height="{BH}" rx="4"/>')
    out.append(f'        <rect class="{CLS[s]}" x="{X1 + 16}" y="{y + 2:.1f}" width="10" height="10"/>')
    out.append(f'        <text x="{X1 + 32}" y="{y + 11.5:.1f}" font-size="11.5">{s}</text>')
lx, ly = 20, bottom + 56
for s in ("Concluída", "Em andamento", "Atrasada", "Não iniciada"):
    out.append(f'        <rect class="{CLS[s]}" x="{lx}" y="{ly - 10}" width="14" height="12"/>')
    out.append(f'        <text x="{lx + 21}" y="{ly}" font-size="11.5">{s}</text>')
    lx += 150
for k, (p, s) in enumerate(zip(rows, status)):
    y = TOP + RH * k
    mid = (sx(p["inicio"]) + sx(p["prazo"] + timedelta(days=1))) / 2
    out.append(f'        <rect class="hit" x="14" y="{y}" width="872" height="{RH}" tabindex="0" role="img" '
               f'aria-label="{p["k"]}, {escape(p["curto"])}: de {dm(p["inicio"])} a {dm(p["prazo"])}, {s.lower()}" data-k="{p["k"]}" '
               f'data-s="{s}" data-q="{escape(p["quem"])}" data-i="{dm(p["inicio"])}" data-p="{dm(p["prazo"])}" data-x="{mid:.1f}"/>')
out.append("      </svg>")

tb = ['        <table>', '          <thead><tr><th>Código</th><th>Ação</th><th>Quem</th><th>Início</th><th>Prazo</th><th>Situação em ' + dm(ref) + '</th></tr></thead>', '          <tbody>']
for p, s in zip(rows, status):
    tb.append(f'            <tr><td>{p["k"]}</td><td>{escape(p["oque"])}</td><td>{escape(p["quem"])}</td><td class="num">{dm(p["inicio"])}</td>'
              f'<td class="num">{dm(p["prazo"])}</td><td>{s}</td></tr>')
tb += ['          </tbody>', '        </table>']

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--GANTT-->", "\n".join(out)), ("<!--GANTTTABLE-->", "\n".join(tb)),
                 ("<!--EX1-->", tabela(EX1)), ("<!--EX2-->", tabela(EX2)), ("<!--EX3-->", tabela(EX3))):
    assert tag in body, tag
    body = body.replace(tag, val)

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>5W2H na prática</title>")
assert "5W2H" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
for name, ex in (("EX1", EX1), ("EX2", EX2), ("EX3", EX3)):
    print(name, len(ex["itens"]), "ações; custo previsto", sum(p["custo"] for p in ex["itens"]))
