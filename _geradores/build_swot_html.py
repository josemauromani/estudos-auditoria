# -*- coding: utf-8 -*-
"""Monta treinamento-swot.html: CSS herdado do estudo de PDCA + corpo próprio + gráfico de barras."""
import re
import sys
from html import escape

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# ---- cores dos quadrantes
pairs = [
    ("--p:#2B5C8A; --p-tint:#DCE8F3;", "--s:#1E7B73; --s-tint:#D9EEEB;"),
    ("--d:#A96A12; --d-tint:#F6E8CF;", "--w:#A96A12; --w-tint:#F6E8CF;"),
    ("--c:#1E7B73; --c-tint:#D9EEEB;", "--o:#2B5C8A; --o-tint:#DCE8F3;"),
    ("--a:#B0413E; --a-tint:#F5DEDC;", "--t:#B0413E; --t-tint:#F5DEDC;"),
    ("--p:#86B7E3; --p-tint:#1B2F42;", "--s:#5FC6BA; --s-tint:#15332F;"),
    ("--d:#E2AC4F; --d-tint:#3A2C12;", "--w:#E2AC4F; --w-tint:#3A2C12;"),
    ("--c:#5FC6BA; --c-tint:#15332F;", "--o:#86B7E3; --o-tint:#1B2F42;"),
    ("--a:#EC8E89; --a-tint:#3D1F1E;", "--t:#EC8E89; --t-tint:#3D1F1E;"),
]
for a, b in pairs:
    assert a in css, a
    css = css.replace(a, b)

# ---- regras específicas do PDCA saem; entram as da SWOT
drop = (".tiles .p{", ".k.p{", "svg .bx-p{", "svg .bx-d{", "svg .bx-c{", "svg .bx-a{", "table.pdca",
        "svg .band{", "svg .series{", "svg .pt{", "svg .pt.on-hit{", "svg .goal{", "svg .xh{", "svg .root{",
        "/* Ficha do ciclo")
css = "\n".join(l for l in css.split("\n") if not l.startswith(drop))
css = css.replace("accent-color:var(--c)", "accent-color:var(--s)")
assert "var(--p)" not in css and "var(--d)" not in css and "var(--c)" not in css and "var(--a)" not in css, "sobrou cor de fase"

Q = "swot"
extra = """
/* Quadrantes */
.tiles .s{background:var(--s)} .tiles .w{background:var(--w)} .tiles .o{background:var(--o)} .tiles .t{background:var(--t)}
.k.s{background:var(--s)} .k.w{background:var(--w)} .k.o{background:var(--o)} .k.t{background:var(--t)}
.k + .k{margin-left:2px}
svg .bx-s{fill:var(--s-tint);stroke:var(--s);stroke-width:1.5} svg .hd-s{fill:var(--s)}
svg .bx-w{fill:var(--w-tint);stroke:var(--w);stroke-width:1.5} svg .hd-w{fill:var(--w)}
svg .bx-o{fill:var(--o-tint);stroke:var(--o);stroke-width:1.5} svg .hd-o{fill:var(--o)}
svg .bx-t{fill:var(--t-tint);stroke:var(--t);stroke-width:1.5} svg .hd-t{fill:var(--t)}
svg .ref{stroke:var(--muted);stroke-width:1;stroke-dasharray:4 3}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Matriz dos exemplos */
.swot{display:grid;grid-template-columns:minmax(0,1fr);gap:2px;border:1px solid var(--rule);background:var(--surface);padding:2px}
@media (min-width:680px){.swot{grid-template-columns:repeat(2,minmax(0,1fr))}}
.quad{display:flex;flex-direction:column}
.quad.s{background:var(--s-tint)} .quad.w{background:var(--w-tint)} .quad.o{background:var(--o-tint)} .quad.t{background:var(--t-tint)}
.qh{display:flex;align-items:baseline;gap:10px;padding:9px 14px;color:var(--on-hue)}
.quad.s .qh{background:var(--s)} .quad.w .qh{background:var(--w)} .quad.o .qh{background:var(--o)} .quad.t .qh{background:var(--t)}
.qh b{font:700 1.5rem/1 var(--display)}
.qh span{font:600 1rem/1.2 var(--body)}
.qh small{margin-left:auto;font:400 .68rem/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;opacity:.9}
.quad ol{list-style:none;padding:12px 14px 14px;margin:0;gap:8px;font-size:.88rem;line-height:1.4}
.quad li{display:grid;grid-template-columns:30px minmax(0,1fr) 28px;gap:6px;align-items:baseline}
.quad li b{font:600 .8rem var(--body);color:var(--muted)}
.quad li i{font:500 .8rem var(--mono);font-style:normal;text-align:right;font-variant-numeric:tabular-nums}

/* Ficha da análise (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)

# ---- gráfico de barras do exemplo 1
NAME = {"S": "Força", "W": "Fraqueza", "O": "Oportunidade", "T": "Ameaça"}
DATA = [
    ("S1", "Receita própria, elogiada nas avaliações", 5, 4), ("S2", "Entrega própria, com 95% no prazo", 4, 4),
    ("S3", "Clientela fiel no bairro", 4, 3), ("S4", "Equipe estável", 3, 3),
    ("W1", "Forno único, que limita a produção no pico", 5, 4), ("W2", "Dependência de um aplicativo para 70% dos pedidos", 4, 5),
    ("W3", "Sem controle de custo por pizza", 3, 3), ("W4", "Pouca presença nas redes sociais", 2, 3),
    ("O1", "Novos condomínios em construção no bairro", 5, 4), ("O2", "Procura por opções vegetarianas e sem glúten", 3, 3),
    ("O3", "Empresas buscando fornecedores para eventos", 2, 3), ("O4", "Pedido por aplicativo de mensagens", 4, 4),
    ("T1", "Aumento da taxa cobrada pelo aplicativo", 4, 4), ("T2", "Chegada de uma rede de pizzarias ao bairro", 4, 3),
    ("T3", "Alta do preço do queijo e da farinha", 3, 4), ("T4", "Obras na avenida principal", 2, 2),
]
order = "SWOT"
rows = sorted(DATA, key=lambda d: (-d[2] * d[3], order.index(d[0][0]), d[0]))
prio = lambda v: "alta" if v >= 15 else ("média" if v >= 8 else "baixa")

X0, SC, TOP, RH, BH = 400, 18, 44, 25, 14
H = TOP + RH * len(rows) + 64
sx = lambda v: X0 + v * SC
out = []
out.append(f'      <svg id="bars" viewBox="0 0 900 {H}" role="img" aria-label="Gráfico de barras horizontais com a pontuação dos 16 fatores do exemplo 1, do maior para o menor. Quatro fatores têm 20 pontos: S1, W1, W2 e O1. Três têm 16 pontos: S2, O4 e T1. O menor é T4, com 4 pontos. As faixas de prioridade começam em 8 pontos, para média, e em 15 pontos, para alta.">')
bottom = TOP + RH * len(rows)
for v in (0, 5, 10, 20, 25):
    out.append(f'        <line class="grid" x1="{sx(v)}" y1="{TOP - 6}" x2="{sx(v)}" y2="{bottom}"/>')
    out.append(f'        <text class="mu" x="{sx(v)}" y="{bottom + 16}" font-size="11" text-anchor="middle" style="font-variant-numeric:tabular-nums">{v}</text>')
for v, lab in ((8, "média: de 8 a 14"), (15, "alta: 15 ou mais")):
    out.append(f'        <line class="ref" x1="{sx(v)}" y1="{TOP - 16}" x2="{sx(v)}" y2="{bottom}"/>')
    out.append(f'        <text class="mu" x="{sx(v) + 5}" y="{TOP - 14}" font-size="11">{lab}</text>')
out.append(f'        <text class="mu" x="{sx(0) + 5}" y="{TOP - 14}" font-size="11">baixa: até 7</text>')
out.append(f'        <text class="mono mu" x="{sx(12.5)}" y="{bottom + 34}" font-size="10" text-anchor="middle">PONTOS (IMPACTO × INTENSIDADE)</text>')
for k, (code, text, imp, inten) in enumerate(rows):
    v = imp * inten
    q = code[0].lower()
    y = TOP + RH * k + (RH - BH) / 2
    x1 = sx(v)
    out.append(f'        <rect class="hd-{q}" x="20" y="{y - 2:.1f}" width="26" height="18"/>')
    out.append(f'        <text class="b on" x="33" y="{y + 11:.1f}" font-size="10.5" text-anchor="middle">{code}</text>')
    out.append(f'        <text x="54" y="{y + 11.5:.1f}" font-size="11.5">{escape(text)}</text>')
    out.append(f'        <path class="bar hd-{q}" data-k="{code}" d="M{X0} {y:.1f} H{x1 - 4} Q{x1} {y:.1f} {x1} {y + 4:.1f} V{y + BH - 4:.1f} Q{x1} {y + BH:.1f} {x1 - 4} {y + BH:.1f} H{X0} Z"/>')
    out.append(f'        <text class="b" x="{x1 + 7}" y="{y + 11.5:.1f}" font-size="11.5" style="font-variant-numeric:tabular-nums">{v}</text>')
ly = bottom + 54
lx = 20
for q in "SWOT":
    out.append(f'        <rect class="hd-{q.lower()}" x="{lx}" y="{ly - 10}" width="14" height="12"/>')
    lab = {"S": "Forças", "W": "Fraquezas", "O": "Oportunidades", "T": "Ameaças"}[q]
    out.append(f'        <text x="{lx + 21}" y="{ly}" font-size="11.5">{q} · {lab}</text>')
    lx += 150
for k, (code, text, imp, inten) in enumerate(rows):
    v = imp * inten
    y = TOP + RH * k
    out.append(f'        <rect class="hit" x="14" y="{y}" width="872" height="{RH}" tabindex="0" role="img" '
               f'aria-label="{code}, {escape(text)}: {v} pontos, prioridade {prio(v)}" data-k="{code}" data-q="{NAME[code[0]]}" '
               f'data-v="{v}" data-i="{imp}" data-n="{inten}" data-p="{prio(v)}" data-x="{sx(v)}" data-y="{y}"/>')
out.append("      </svg>")
bars = "\n".join(out)

tb = ['        <table>', '          <thead><tr><th>Código</th><th>Fator</th><th>Impacto</th><th>Intensidade</th><th>Pontos</th><th>Prioridade</th></tr></thead>', '          <tbody>']
for code, text, imp, inten in rows:
    v = imp * inten
    tb.append(f'            <tr><td>{code}</td><td>{escape(text)}</td><td class="num">{imp}</td><td class="num">{inten}</td><td class="num">{v}</td><td>{prio(v).capitalize()}</td></tr>')
tb += ['          </tbody>', '        </table>']

body = open(BODY, encoding="utf-8").read()
assert "<!--BARS-->" in body and "<!--BARTABLE-->" in body
body = body.replace("<!--BARS-->", bars).replace("<!--BARTABLE-->", "\n".join(tb))

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Matriz SWOT na prática</title>")
assert "Matriz SWOT" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, len(rows), "barras; soma por quadrante:",
      {q: sum(i * n for c, _, i, n in DATA if c[0] == q) for q in "SWOT"})
