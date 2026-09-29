# -*- coding: utf-8 -*-
"""Monta treinamento-ishikawa.html: CSS herdado do estudo de PDCA + corpo próprio + diagramas gerados a partir dos dados."""
import math
import os
import re
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ish_data import EX1, EX2, EX3, M6  # noqa: E402

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

for a, b in [("--p:#2B5C8A; --p-tint:#DCE8F3;", "--m:#2B5C8A; --m-tint:#DCE8F3;"),
             ("--p:#86B7E3; --p-tint:#1B2F42;", "--m:#86B7E3; --m-tint:#1B2F42;")]:
    assert a in css, a
    css = css.replace(a, b)
css, n = re.subn(r"\n\s*--[dca]:#\w+; --[dca]-tint:#\w+;", "", css)
assert n == 9, n

drop = (".tiles .p{", ".k.p{", "svg .bx-p{", "svg .bx-d{", "svg .bx-c{", "svg .bx-a{", "table.pdca",
        "svg .band{", "svg .series{", "svg .pt{", "svg .pt.on-hit{", "svg .goal{", "svg .xh{", "svg .root{",
        "/* Ficha do ciclo")
css = "\n".join(l for l in css.split("\n") if not l.startswith(drop))
css = css.replace("accent-color:var(--c)", "accent-color:var(--m)")
for v in ("var(--p)", "var(--d)", "var(--c)", "var(--a)"):
    assert v not in css, v

extra = """
/* Categorias e marcações do diagrama */
.tiles .m{background:var(--m)}
.k.m{background:var(--m)}
svg .bx-m{fill:var(--m-tint);stroke:var(--m);stroke-width:1.5} svg .hd-m{fill:var(--m)}
svg .root{fill:var(--accent);stroke:var(--surface);stroke-width:2}
svg .ring{fill:var(--surface);stroke:var(--accent);stroke-width:1.5}
svg text.cut{fill:var(--muted);text-decoration:line-through}
svg text.open{fill:var(--muted);font-style:italic}
svg .bar{fill:var(--accent)}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabela das causas */
table.causas{font-size:.84rem;min-width:860px}
table.causas td.cod{font-weight:600;color:var(--muted);width:7%}
table.causas td.res b{font-weight:600}
table.causas td.res small{display:block;color:var(--muted);font-size:.8rem}
table.causas tr.cut td.cau{color:var(--muted);text-decoration:line-through}
table.causas tr.open td.cau{color:var(--muted);font-style:italic}

/* Exercício com seis opções */
.quiz.wide .q{grid-template-columns:minmax(0,1fr)}
.quiz.wide .opts{flex-wrap:wrap}
.quiz.wide .opts button{width:auto;height:36px;padding:0 12px;font:600 .85rem/1 var(--body)}

/* Ficha da análise (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)


def estado(c):
    if c["res"] == "Confirmada":
        return "go" if c["segue"] else "ok"
    return "cut" if c["res"] == "Descartada" else "open"


def fish(fid, cats, itens, efeito, aria, legend=True):
    """Espinha de peixe com até seis categorias (metade acima, metade abaixo) e até três causas por ramo."""
    SP, TOPY, BOTY, DY = 210, 52, 368, 158
    ntop = math.ceil(len(cats) / 2)
    joints = {3: [258, 472, 686], 2: [360, 650], 1: [500]}
    H = 440 if legend else 410
    o = [f'      <svg viewBox="0 0 900 {H}" role="img" aria-label="{escape(aria)}">',
         '        <defs>',
         f'          <marker id="{fid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah" d="M0 0 L10 5 L0 10 z"/></marker>',
         '        </defs>',
         f'        <line class="ln" x1="14" y1="{SP}" x2="696" y2="{SP}" marker-end="url(#{fid})" stroke-width="2"/>',
         f'        <rect class="bx-ink" x="702" y="{SP - 44}" width="188" height="88"/>',
         f'        <text class="mono t-ground" x="796" y="{SP - 24}" font-size="10" text-anchor="middle">EFEITO</text>']
    y0 = SP - 4 + (3 - len(efeito)) * 8
    for i, t in enumerate(efeito):
        o.append(f'        <text class="b t-ground" x="796" y="{y0 + 16 * i}" font-size="12.5" text-anchor="middle">{escape(t)}</text>')
    for half, group in ((0, cats[:ntop]), (1, cats[ntop:])):
        js = joints[len(group)] if group else []
        for xj, cat in zip(js, group):
            xs = xj - 75
            ye = TOPY if half == 0 else BOTY
            o.append(f'        <line class="ln" x1="{xs}" y1="{ye}" x2="{xj}" y2="{SP}"/>')
            by = ye - 26 if half == 0 else ye
            o.append(f'        <rect class="hd-m" x="{xs - 66}" y="{by}" width="132" height="26"/>')
            o.append(f'        <text class="on b" x="{xs}" y="{by + 17.5}" font-size="12.5" text-anchor="middle">{escape(cat)}</text>')
            causes = [c for c in itens if c["cat"] == cat][:3]
            slots = [92, 130, 168] if half == 0 else [328, 290, 252]
            if not causes:
                y = slots[0]
                bx = xs + (abs(y - ye) / DY) * 75
                o.append(f'        <text class="open" x="{bx - 12:.1f}" y="{y - 5}" font-size="11" text-anchor="end">sem causas levantadas</text>')
            for y, c in zip(slots, causes):
                bx = xs + (abs(y - ye) / DY) * 75
                st = c.get("st", "plain")
                cls = {"go": "b", "ok": "", "cut": "cut", "open": "open", "plain": ""}[st]
                o.append(f'        <line class="ln-mu" stroke-width="1" x1="{bx:.1f}" y1="{y}" x2="{bx - 196:.1f}" y2="{y}"/>')
                o.append(f'        <text{" class=" + chr(34) + cls + chr(34) if cls else ""} x="{bx - 9:.1f}" y="{y - 5}" font-size="11" text-anchor="end">{escape(c["curto"])}</text>')
                if st == "go":
                    o.append(f'        <circle class="root" cx="{bx:.1f}" cy="{y}" r="5"/>')
                elif st == "ok":
                    o.append(f'        <circle class="ring" cx="{bx:.1f}" cy="{y}" r="4"/>')
    if legend:
        y = 424
        o.append(f'        <circle class="root" cx="22" cy="{y - 4}" r="5"/><text class="b" x="34" y="{y}" font-size="11">confirmada, segue para o plano</text>')
        o.append(f'        <circle class="ring" cx="252" cy="{y - 4}" r="4"/><text x="264" y="{y}" font-size="11">confirmada, fica para depois</text>')
        o.append(f'        <text class="cut" x="468" y="{y}" font-size="11">descartada pelos dados</text>')
        o.append(f'        <text class="open" x="650" y="{y}" font-size="11">não verificada</text>')
    o.append("      </svg>")
    return "\n".join(o)


def fish_ex(fid, ex, intro):
    itens = [dict(c, st=estado(c)) for c in ex["causas"]]
    partes = []
    for cat in ex["cats"]:
        cs = [c for c in itens if c["cat"] == cat]
        if not cs:
            partes.append(f"{cat}: sem causas levantadas")
            continue
        nome = {"go": "confirmada, segue para o plano", "ok": "confirmada", "cut": "descartada", "open": "não verificada"}
        partes.append(f"{cat}: " + "; ".join(f'{c["curto"].lower()} ({nome[c["st"]]})' for c in cs))
    return fish(fid, ex["cats"], itens, ex["efeito_curto"], intro + " " + ". ".join(partes) + ".")


def tabela(ex):
    o = ['  <div class="tbl">', '    <table class="causas">',
         '      <thead><tr><th>Código</th><th style="width:13%">Categoria</th><th style="width:24%">Causa provável</th>'
         '<th style="width:21%">Como foi verificada</th><th style="width:13%">Resultado</th><th>Evidência</th></tr></thead>', '      <tbody>']
    for c in ex["causas"]:
        st = estado(c)
        res = f"<b>{c['res']}</b>" + ("<small>segue para o plano</small>" if st == "go" else "")
        row = f' class="{st}"' if st in ("cut", "open") else ""
        o.append(f'        <tr{row}><td class="cod">{c["k"]}</td><td>{escape(c["cat"])}</td><td class="cau">{escape(c["causa"])}</td>'
                 f'<td>{escape(c["como"])}</td><td class="res">{res}</td><td>{escape(c["evid"] or "—")}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


# ---- figura dos 6M, com perguntas de apoio
GUIA = {
    "Método": ["O procedimento é claro e seguido?", "A sequência das etapas ajuda?"],
    "Mão de obra": ["As pessoas foram treinadas?", "A escala cobre a demanda?"],
    "Máquina": ["O equipamento está em bom estado?", "A manutenção está em dia?"],
    "Material": ["Os insumos chegam no padrão?", "As informações chegam completas?"],
    "Medição": ["Os instrumentos estão calibrados?", "O indicador mede o que importa?"],
    "Meio ambiente": ["O espaço e a temperatura ajudam?", "Algo de fora afeta o processo?"],
}
guia = [dict(cat=cat, curto=t) for cat, ts in GUIA.items() for t in ts]
for g in guia:
    assert len(g["curto"]) <= 34, g
fig6m = fish("a3", M6, guia, ["O problema,", "com número, local", "e período"],
             "Diagrama com as seis categorias dos 6M e duas perguntas de apoio em cada uma. "
             + " ".join(f"{cat}: {' '.join(ts)}" for cat, ts in GUIA.items()), legend=False)

# ---- gráfico dos motivos de atraso
rows = EX1["pareto"]
X0, SC, TOP, RH, BH = 330, 8.4, 44, 30, 14
bottom = TOP + RH * len(rows)
H = bottom + 44
sx = lambda v: round(X0 + v * SC, 1)
out = [f'      <svg id="bars" viewBox="0 0 900 {H}" role="img" aria-label="Gráfico de barras horizontais com o motivo do atraso em 200 entregas: '
       + "; ".join(f"{n.lower()}, {v}%" for n, v in rows) + '.">']
for v in (0, 10, 20, 30, 40, 50):
    out.append(f'        <line class="grid" x1="{sx(v)}" y1="{TOP - 6}" x2="{sx(v)}" y2="{bottom}"/>')
    out.append(f'        <text class="mu" x="{sx(v)}" y="{bottom + 16}" font-size="11" text-anchor="middle" style="font-variant-numeric:tabular-nums">{v}%</text>')
out.append(f'        <text class="mono mu" x="{sx(25)}" y="{bottom + 36}" font-size="10" text-anchor="middle">PARTE DOS ATRASOS</text>')
out.append(f'        <text class="mono mu" x="880" y="{TOP - 14}" font-size="10" text-anchor="end">ACUMULADO</text>')
acc = 0
for k, (nome, v) in enumerate(rows):
    acc += v
    y = TOP + RH * k + (RH - BH) / 2
    x1 = sx(v)
    out.append(f'        <text x="20" y="{y + 11.5:.1f}" font-size="11.5">{escape(nome)}</text>')
    out.append(f'        <path class="bar" data-k="{k}" d="M{X0} {y:.1f} H{x1 - 4} Q{x1} {y:.1f} {x1} {y + 4:.1f} V{y + BH - 4:.1f} Q{x1} {y + BH:.1f} {x1 - 4} {y + BH:.1f} H{X0} Z"/>')
    out.append(f'        <text class="b" x="{x1 + 7}" y="{y + 11.5:.1f}" font-size="11.5" style="font-variant-numeric:tabular-nums">{v}%</text>')
    out.append(f'        <text class="mu" x="880" y="{y + 11.5:.1f}" font-size="11.5" text-anchor="end" style="font-variant-numeric:tabular-nums">{acc}%</text>')
acc = 0
for k, (nome, v) in enumerate(rows):
    acc += v
    out.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" '
               f'aria-label="{escape(nome)}: {v}% dos atrasos, acumulado de {acc}%" data-k="{k}" data-n="{escape(nome)}" '
               f'data-v="{v}" data-q="{v * 2}" data-c="{acc}" data-x="{sx(v)}"/>')
out.append("      </svg>")
tb = ['        <table>', '          <thead><tr><th>Motivo do atraso</th><th>Entregas</th><th>Parte dos atrasos</th><th>Acumulado</th></tr></thead>', '          <tbody>']
acc = 0
for nome, v in rows:
    acc += v
    tb.append(f'            <tr><td>{escape(nome)}</td><td class="num">{v * 2}</td><td class="num">{v}%</td><td class="num">{acc}%</td></tr>')
tb += ['          </tbody>', '        </table>']

body = open(BODY, encoding="utf-8").read()
subs = [
    ("<!--FIG6M-->", fig6m),
    ("<!--FISH1-->", fish_ex("a4", EX1, "Diagrama de Ishikawa do exemplo 1, com o efeito 18% das entregas chegam depois de 40 minutos.")),
    ("<!--FISH2-->", fish_ex("a5", EX2, "Diagrama de Ishikawa do exemplo 2, com o efeito 40% das requisições de compra são devolvidas.")),
    ("<!--FISH3-->", fish_ex("a6", EX3, "Diagrama de Ishikawa do exemplo 3, com o efeito 3 de 25 instrumentos em uso com a calibração vencida.")),
    ("<!--TAB1-->", tabela(EX1)), ("<!--TAB2-->", tabela(EX2)), ("<!--TAB3-->", tabela(EX3)),
    ("<!--PARETO-->", "\n".join(out)), ("<!--PARETOTABLE-->", "\n".join(tb)),
]
for tag, val in subs:
    assert tag in body, tag
    body = body.replace(tag, val)

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Diagrama de Ishikawa na prática</title>")
assert "Ishikawa" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
for name, ex in (("EX1", EX1), ("EX2", EX2), ("EX3", EX3)):
    cs = ex["causas"]
    print(name, len(cs), "hipóteses |", {r: sum(1 for c in cs if c["res"] == r) for r in ("Confirmada", "Descartada", "Não verificada")},
          "| seguem:", sum(1 for c in cs if c["segue"]))
