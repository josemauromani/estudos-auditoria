# -*- coding: utf-8 -*-
"""Monta treinamento-pareto.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from par_data import CHECK, CORTE, DEPOIS, ETAPAS, EX1, EX2, EX3, OUTROS, PRIOR, colunas, linhas, pareto, taxa  # noqa: E402

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Gráfico de Pareto: barra cheia para a prioridade, barra vazada para o restante */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);white-space:nowrap}
.chip.pr{background:var(--p);color:var(--on-hue)}
.chip.sl{background:var(--sunk);color:var(--ink);box-shadow:inset 0 0 0 1px var(--rule)}
svg .hd-ink{fill:var(--ink)}
svg .bv{fill:var(--p)}
svg .bt{fill:var(--p-tint);stroke:var(--p);stroke-width:1.5}
svg .b-ant{fill:var(--sunk);stroke:var(--muted);stroke-width:1.5}
svg .b-dep{fill:var(--p)}
svg .cum{stroke:var(--ink);stroke-width:2;fill:none;stroke-linejoin:round;stroke-linecap:round}
svg .cpt{fill:var(--ink);stroke:var(--surface);stroke-width:2}
svg .halo{paint-order:stroke;stroke:var(--surface);stroke-width:4px;stroke-linejoin:round}
svg .tally{stroke:var(--ink);stroke-width:1.6;fill:none;stroke-linecap:round}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas dos exemplos */
table.aud{font-size:.8rem;min-width:860px;line-height:1.4}
table.aud th, table.aud td{padding:8px 9px}
table.aud td.n{white-space:nowrap;font-weight:600;color:var(--muted)}
table.aud td.c, table.aud th.c{text-align:center;font-variant-numeric:tabular-nums}
table.aud td.hi{background:var(--p-tint);font-weight:600}
table.aud tr.tot td{font-weight:600;background:var(--sunk)}
table.aud td small, table.aud th small{display:block;color:var(--muted);font-size:.76rem;margin-top:3px;font-weight:400}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha da coleta (acima de cada exemplo) */"""
assert css.count("\n.ficha{") == 1
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

TNUM = ' style="font-variant-numeric:tabular-nums"'


def dt(d):
    return d.strftime("%d/%m/%Y") if d else "—"


def br(v, casas=1):
    return f"{v:.{casas}f}".replace(".", ",")


def mil(v):
    return f"{v:,.0f}".replace(",", ".")


def pc(v):
    """Percentual inteiro, com a metade arredondada para cima, como na planilha."""
    return f"{int(100 * v + 0.5 + 1e-9)}%"


def marker(i):
    return (f'        <defs><marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            '<path class="ah" d="M0 0 L10 5 L0 10 z"/></marker></defs>')


def tally(x, y, n, h=15):
    """Traços de contagem, em grupos de cinco: quatro traços e um corte."""
    o = []
    for g in range((n + 4) // 5):
        k = min(5, n - 5 * g)
        gx = x + g * 27
        for j in range(min(k, 4)):
            o.append(f'<line class="tally" x1="{gx + j * 5}" y1="{y}" x2="{gx + j * 5}" y2="{y + h}"/>')
        if k == 5:
            o.append(f'<line class="tally" x1="{gx - 3}" y1="{y + h - 3}" x2="{gx + 18}" y2="{y + 3}"/>')
    return "".join(o)


def pareto_g(rows, ox, oy, w, h, *, unidade, eixo=None, wrap=16, fs=11, ident=None, rot=None):
    """Desenha um Pareto na área dada. Os dois eixos usam a mesma régua: o total, à esquerda, fica na altura dos 100%."""
    p = pareto(rows)
    total = sum(r["v"] for r in p)
    sy = lambda v: round(oy + h - v / total * h, 1)  # noqa: E731
    slot = w / len(p)
    bw = round(slot * 0.62, 1)
    o, geo = [], []
    for f in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        y = sy(f * total)
        o.append(f'        <line class="grid" x1="{ox}" y1="{y}" x2="{ox + w}" y2="{y}"/>')
        o.append(f'        <text class="mu" x="{ox - 8}" y="{y + 4}" font-size="{fs}" text-anchor="end"{TNUM}>{mil(f * total)}</text>')
        o.append(f'        <text class="mu" x="{ox + w + 8}" y="{y + 4}" font-size="{fs}"{TNUM}>{round(100 * f)}%</text>')
    o.append(f'        <text class="mono mu" x="{ox - 8}" y="{oy - 16}" font-size="9.5" text-anchor="end">{escape((eixo or unidade).upper())}</text>')
    o.append(f'        <text class="mono mu" x="{ox + w + 8}" y="{oy - 16}" font-size="9.5">ACUMULADO</text>')
    yc = sy(CORTE * total)
    o.append(f'        <line class="goal" x1="{ox}" y1="{yc}" x2="{ox + w}" y2="{yc}"/>')
    for k, r in enumerate(p):
        x = round(ox + slot * k + (slot - bw) / 2, 1)
        top, base = sy(r["v"]), oy + h
        rad = min(4, (base - top) / 2)
        cls = "bv" if r["classe"] == PRIOR else "bt"
        o.append(f'        <path class="bar {cls}" data-k="{k}" d="M{x} {base} V{top + rad} Q{x} {top} {x + rad} {top} H{x + bw - rad} Q{x + bw} {top} {x + bw} {top + rad} V{base} Z"/>')
        cx = round(x + bw / 2, 1)
        dentro = base - top >= 30
        o.append(f'        <text class="b{" on" if dentro and cls == "bv" else ""}" x="{cx}" y="{top + 18 if dentro else top - 7}" font-size="{fs + 0.5}" text-anchor="middle"{TNUM} pointer-events="none">{mil(r["v"])}</text>')
        for j, l in enumerate(textwrap.wrap((rot or {}).get(r["nome"], r["nome"]), wrap, break_long_words=False)):
            o.append(f'        <text x="{cx}" y="{base + 17 + j * (fs + 2)}" font-size="{fs}" text-anchor="middle">{escape(l)}</text>')
        geo.append(dict(r, x=x, cx=cx, top=top, ya=sy(r["acc"] * total), bw=bw))
    o.append('        <polyline class="cum" points="' + " ".join(f'{g["cx"]},{g["ya"]}' for g in geo) + '"/>')
    for k, g in enumerate(geo):
        o.append(f'        <circle class="cpt" cx="{g["cx"]}" cy="{g["ya"]}" r="4.5"/>')
        if 0 < k < len(geo) - 1:
            o.append(f'        <text class="b halo" x="{g["cx"]}" y="{g["ya"] - 10}" font-size="{fs}" text-anchor="middle"{TNUM}>{pc(g["acc"])}</text>')
    if ident:
        for k, g in enumerate(geo):
            o.append(f'        <rect class="hit" x="{round(ox + slot * k, 1)}" y="{oy - 8}" width="{round(slot, 1)}" height="{h + 8}" tabindex="0" role="img" '
                     f'aria-label="{escape(g["nome"])}: {mil(g["v"])} {unidade}, {pc(g["pct"])} do total, acumulado de {pc(g["acc"])}. {g["classe"]}." data-k="{k}" data-n="{escape(g["nome"])}" '
                     f'data-v="{mil(g["v"])}" data-p="{pc(g["pct"])[:-1]}" data-c="{pc(g["acc"])[:-1]}" data-cl="{g["classe"]}" data-cx="{g["cx"]}" data-cy="{min(g["top"], g["ya"])}"/>')
    return o, geo, dict(total=total, yc=yc, base=oy + h, sy=sy)


def descr(rows, unidade):
    p = pareto(rows)
    return " ".join(f'{r["nome"]}: {mil(r["v"])} {unidade}, {pc(r["pct"])}, acumulado de {pc(r["acc"])}.' for r in p)


H1, H2 = EX1["head"], EX2["head"]
L1, L2 = linhas(EX1), linhas(EX2)
P1, P2 = pareto(L1), pareto(L2)
T1, T2 = sum(v for _, v in L1), sum(v for _, v in L2)
CURTO = dict(zip((n for n, _, _ in EX1["folha"]), EX1["curto"]))
NOITE = EX1["noite"]

# ------------------------------------------------------------------ figura 1: da folha ao gráfico
EMB = [2, 0, 3, 1, 4]  # a folha segue a ordem do formulário, e não a do tamanho
PX = [10, 310, 610]
da = ['      <svg viewBox="0 0 900 250" role="img" aria-label="Da folha ao gráfico, em três partes. Contar: a folha de verificação recebe um traço por ocorrência, na ordem do formulário. '
      'Ordenar: os totais do período são postos do maior para o menor, com a parte do total e o acumulado: ' + descr(L1, "atrasos")
      + ' Decidir: o gráfico de Pareto mostra que duas barras somam ' + pc(P1[1]["acc"]) + ' do total.">', marker("a1")]
for k, (tit, sub_) in enumerate([("1 · CONTAR", "A folha, na ordem do formulário"), ("2 · ORDENAR", "Os totais, do maior para o menor"), ("3 · DECIDIR", "O gráfico, com o acumulado")]):
    x = PX[k]
    da.append(f'        <rect class="{["bx-p", "bx-d", "bx-c"][k]}" x="{x}" y="10" width="280" height="196"/>')
    da.append(f'        <text class="mono mu" x="{x + 14}" y="30" font-size="10">{tit}</text>')
    da.append(f'        <text class="b" x="{x + 14}" y="48" font-size="12">{sub_}</text>')
    if k < 2:
        da.append(f'        <line class="ln" x1="{x + 282}" y1="108" x2="{x + 297}" y2="108" marker-end="url(#a1)"/>')
for j, i in enumerate(EMB):
    y = 70 + j * 26
    da.append(f'        <text x="24" y="{y + 12}" font-size="10.5">{escape(EX1["curto"][i])}</text>')
    da.append(f'        <g transform="translate(168,{y})">{tally(0, 0, sum(NOITE["linhas"][i]), 13)}</g>')
for j, r in enumerate(P1):
    y = 70 + j * 26
    da.append(f'        <text x="324" y="{y + 12}" font-size="10.5">{escape(CURTO[r["nome"]])}</text>')
    da.append(f'        <text class="b" x="496" y="{y + 12}" font-size="10.5" text-anchor="end"{TNUM}>{r["v"]}</text>')
    da.append(f'        <text class="mu" x="536" y="{y + 12}" font-size="10.5" text-anchor="end"{TNUM}>{pc(r["pct"])}</text>')
    da.append(f'        <text class="mu" x="578" y="{y + 12}" font-size="10.5" text-anchor="end"{TNUM}>{pc(r["acc"])}</text>')
bx, bb, bh, bs = 640, 190, 116, 44
pts = []
for j, r in enumerate(P1):
    hh = round(r["pct"] * bh, 1)
    x = bx + j * bs
    da.append(f'        <rect class="{"bv" if r["classe"] == PRIOR else "bt"}" x="{x}" y="{bb - hh}" width="30" height="{hh}"/>')
    pts.append(f'{x + 15},{round(bb - r["acc"] * bh, 1)}')
da.append(f'        <line class="grid" x1="{bx - 8}" y1="{bb}" x2="{bx + 5 * bs - 6}" y2="{bb}"/>')
da.append(f'        <polyline class="cum" points="{" ".join(pts)}"/>')
for p_ in pts:
    cx_, cy_ = p_.split(",")
    da.append(f'        <circle class="cpt" cx="{cx_}" cy="{cy_}" r="4"/>')
da.append(f'        <text class="b halo" x="{bx + bs + 40}" y="{round(bb - P1[1]["acc"] * bh, 1) + 22}" font-size="11">{pc(P1[1]["acc"])} em duas barras</text>')
da.append(f'        <text x="450" y="236" font-size="11.5" text-anchor="middle">A folha da esquerda é a de uma noite. A tabela e o gráfico são do período inteiro: {T1} atrasos.</text>')
da.append("      </svg>")

# ------------------------------------------------------------------ figura 2: as cinco etapas
W5, G5 = 164, 14
fl = ['      <svg viewBox="0 0 900 206" role="img" aria-label="As cinco etapas do trabalho. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS) + ' Depois da ação, a contagem recomeça.">',
      '        <defs><marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah" d="M0 0 L10 5 L0 10 z"/></marker>'
      '<marker id="a2m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah-mu" d="M0 0 L10 5 L0 10 z"/></marker></defs>']
for k, (nome, desc) in enumerate(ETAPAS):
    x = 12 + k * (W5 + G5)
    ink = k == 4
    fl.append(f'        <rect class="{["bx", "bx-p", "bx-d", "bx-c", "bx-ink"][k]}" x="{x}" y="16" width="{W5}" height="124"/>')
    fl.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="36" font-size="10">{k + 1}</text>')
    fl.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="58" font-size="13">{escape(nome)}</text>')
    for j, l in enumerate(textwrap.wrap(desc, 26)[:4]):
        fl.append(f'        <text{" class=" + chr(34) + "t-ground" + chr(34) if ink else ""} x="{x + 12}" y="{80 + j * 14.5}" font-size="10.5">{escape(l)}</text>')
    if k < 4:
        fl.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="78" x2="{x + W5 + G5 - 2}" y2="78" marker-end="url(#a2)"/>')
xa, xb = 12 + 4 * (W5 + G5) + W5 / 2, 12 + (W5 + G5) + W5 / 2
fl.append(f'        <path class="ln-mu dash" d="M{xa} 142 V170 H{xb} V146" marker-end="url(#a2m)"/>')
fl.append('        <text class="mu halo" x="540" y="174" font-size="11" text-anchor="middle">depois da ação, a mesma folha, com as mesmas categorias</text>')
fl.append('        <text x="450" y="198" font-size="11.5" text-anchor="middle">A definição decide tudo: uma categoria mal definida é contada de um jeito por pessoa.</text>')
fl.append("      </svg>")

# ------------------------------------------------------------------ figura 3: a folha de uma noite
CT = [sum(l[j] for l in NOITE["linhas"]) for j in range(4)]
NT = sum(CT)
fo = ['      <svg viewBox="0 0 900 360" role="img" aria-label="Folha de verificação de uma noite da pizzaria: ' + NOITE["dia"] + ", entregas que chegaram depois de 40 minutos, por motivo e por faixa de horário. "
      + " ".join(f'{n}: {", ".join(f"{v} às {c}" for c, v in zip(NOITE["cols"], l))}, total {sum(l)}.' for (n, _, _), l in zip(EX1["folha"], NOITE["linhas"]))
      + f' Total da noite: {NT} atrasos em {NOITE["base"]} entregas.">',
      '        <rect class="bx" x="60" y="10" width="780" height="340"/>',
      '        <rect class="hd-ink" x="60" y="10" width="780" height="34"/>',
      '        <text class="b t-ground" x="76" y="32" font-size="13">Folha de verificação · Entregas que chegaram depois de 40 minutos</text>',
      f'        <text class="mono mu" x="76" y="62" font-size="9.5">DATA</text><text x="76" y="78" font-size="11.5">{NOITE["dia"]}</text>',
      '        <text class="mono mu" x="250" y="62" font-size="9.5">LOCAL</text><text x="250" y="78" font-size="11.5">Bancada da expedição</text>',
      '        <text class="mono mu" x="440" y="62" font-size="9.5">REGISTRA</text><text x="440" y="78" font-size="11.5">Líder da expedição</text>',
      f'        <text class="mono mu" x="620" y="62" font-size="9.5">ENTREGAS DA NOITE</text><text x="620" y="78" font-size="11.5">{NOITE["base"]}</text>',
      '        <rect class="band" x="60" y="90" width="780" height="26"/>',
      '        <text class="b" x="76" y="107" font-size="11">Motivo principal do atraso</text>']
for j, c in enumerate(NOITE["cols"]):
    fo.append(f'        <text class="b" x="{372 + j * 110}" y="107" font-size="11" text-anchor="middle">{c}</text>')
fo.append('        <text class="b" x="795" y="107" font-size="11" text-anchor="middle">Total</text>')
for i, ((nome, _, _), l) in enumerate(zip(EX1["folha"], NOITE["linhas"])):
    y = 116 + i * 40
    fo.append(f'        <line class="grid" x1="60" y1="{y + 40}" x2="840" y2="{y + 40}"/>')
    fo.append(f'        <text x="76" y="{y + 24}" font-size="11.5">{escape(nome)}</text>')
    for j, v in enumerate(l):
        if v:
            fo.append(f'        <g transform="translate({372 + j * 110 - (9 if v < 5 else 8)},{y + 12})">{tally(0, 0, v)}</g>')
    fo.append(f'        <text class="b" x="795" y="{y + 25}" font-size="12.5" text-anchor="middle"{TNUM}>{sum(l)}</text>')
fo.append(f'        <text class="mu" x="604" y="{116 + 4 * 40 + 24}" font-size="10" font-style="italic">moto quebrou</text>')
for x in (316, 426, 536, 646, 756):
    fo.append(f'        <line class="grid" x1="{x}" y1="90" x2="{x}" y2="342"/>')
fo.append('        <text class="b" x="76" y="334" font-size="11.5">Total</text>')
for j, v in enumerate(CT):
    fo.append(f'        <text class="b" x="{372 + j * 110}" y="334" font-size="12.5" text-anchor="middle"{TNUM}>{v}</text>')
fo.append(f'        <text class="b" x="795" y="334" font-size="12.5" text-anchor="middle"{TNUM}>{NT}</text>')
fo.append("      </svg>")

# ------------------------------------------------------------------ figura 4: as partes do gráfico
TIT1 = f'Atrasos nas entregas, por motivo principal · {T1} atrasos em {mil(H1["base"])} entregas · 15/06 a 09/07/2026'
an = ['      <svg viewBox="0 0 900 352" role="img" aria-label="As partes do gráfico de Pareto, no exemplo dos atrasos da pizzaria. ' + descr(L1, "atrasos")
      + ' Seis partes estão indicadas: o título, com o total, o período e a base; o eixo da esquerda, de zero ao total; as barras em ordem decrescente; '
      'a linha do acumulado; o corte de 80%; o eixo da direita, com os 100% na altura do total; e a barra Outros, por último.">']
g_, geo, inf = pareto_g(L1, 232, 74, 430, 236, unidade="atrasos", wrap=13, fs=10.5, rot=CURTO)
an.append(f'        <text class="b" x="447" y="28" font-size="12" text-anchor="middle">{escape(TIT1)}</text>')
an += g_


def nota(x, y, titulo, texto, ancora="start", w=24):
    o = [f'        <text class="b" x="{x}" y="{y}" font-size="11.5" text-anchor="{ancora}">{escape(titulo)}</text>']
    for j, l in enumerate(textwrap.wrap(texto, w)):
        o.append(f'        <text class="mu" x="{x}" y="{y + 15 + j * 13.5}" font-size="10.5" text-anchor="{ancora}">{escape(l)}</text>')
    return o


an += nota(14, 70, "Eixo da esquerda", "Começa em zero e vai até o total.")
an.append('        <line class="ln-mu" x1="152" y1="74" x2="196" y2="74"/>')
an += nota(14, 128, "Linha do acumulado", "Soma as barras, da primeira até a atual.")
an.append(f'        <line class="ln-mu" x1="152" y1="{geo[1]["ya"]}" x2="{geo[1]["cx"] - 9}" y2="{geo[1]["ya"]}"/>')
an += nota(14, 214, "Barras em ordem", "Da maior para a menor. A altura é a contagem.")
an.append(f'        <line class="ln-mu" x1="152" y1="{geo[0]["top"] + 30}" x2="{geo[0]["x"] - 4}" y2="{geo[0]["top"] + 30}"/>')
an += nota(14, 284, "Barra cheia", "Entra na prioridade: começa antes do corte.")
an.append(f'        <line class="ln-mu" x1="152" y1="294" x2="{geo[0]["x"] - 4}" y2="294"/>')
an += nota(886, 70, "Eixo da direita", "Os 100% ficam na altura do total.", "end")
an.append('        <line class="ln-mu" x1="742" y1="66" x2="790" y2="66"/>')
an += nota(886, 136, "Corte de 80%", "Separa a prioridade do que fica para depois.", "end")
an.append(f'        <line class="ln-mu" x1="742" y1="{inf["yc"]}" x2="770" y2="{inf["yc"]}"/><line class="ln-mu" x1="770" y1="{inf["yc"]}" x2="800" y2="132"/>')
an += nota(886, 290, "Outros por último", "Mesmo sendo maior do que a barra anterior.", "end", 22)
an.append(f'        <line class="ln-mu" x1="752" y1="300" x2="{geo[4]["x"] + geo[4]["bw"] + 4}" y2="296"/>')
an.append('        <text class="mu" x="447" y="46" font-size="10.5" text-anchor="middle">O título informa o que foi contado, o total, a base e o período.</text>')
an.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(h, como=True):
    o = ['  <dl class="ficha">',
         f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
         f'    <div><dt>O que se conta</dt><dd>{escape(h["conta"])}</dd></div>',
         f'    <div><dt>Período e fonte</dt><dd>{escape(h["periodo"])}</dd></div>']
    if como and h.get("como"):
        o.append(f'    <div><dt>Como se registra</dt><dd>{escape(h["como"])}</dd></div>')
    o += [f'    <div><dt>Análise</dt><dd>{dt(h["data"])}, por {escape(h["por"][0].lower() + h["por"][1:])}.</dd></div>',
          f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>', '  </dl>']
    return "\n".join(o)


def folha_tab(ex, titulo):
    cols = colunas(ex)
    tot = sum(v for _, v in cols)
    mx = max(v for _, v in cols)
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{escape(titulo)}</caption>',
         '      <thead><tr><th style="width:38%">Categoria<small>Conta quando…</small></th>' + "".join(f'<th class="c">{escape(c)}</th>' for c, _ in cols) + '<th class="c">Total</th></tr></thead>',
         '      <tbody>']
    for nome, defin, v in ex["folha"]:
        o.append(f'        <tr><td><strong>{escape(nome)}</strong><small>{escape(defin)}</small></td>' + "".join(f'<td class="c">{x}</td>' for x in v) + f'<td class="c"><strong>{sum(v)}</strong></td></tr>')
    o.append('        <tr class="tot"><td>Total</td>' + "".join(f'<td class="c{" hi" if v == mx else ""}">{v}</td>' for _, v in cols) + f'<td class="c">{tot}</td></tr>')
    o.append('        <tr class="tot"><td>Parte do total</td>' + "".join(f'<td class="c">{pc(v / tot)}</td>' for _, v in cols) + '<td class="c">100%</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def chip(classe):
    return f'<span class="chip {"pr" if classe == PRIOR else "sl"}">{classe}</span>'


def pareto_tab(rows, titulo, col1, unidade, base=None, base_nome=None, bases=None):
    """Com `bases` (nome -> base de cada linha), a tabela mostra a base e a taxa de cada linha."""
    p = pareto(rows)
    tot = sum(r["v"] for r in p)
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{escape(titulo)}</caption>',
         f'      <thead><tr><th class="c" style="width:7%">Ordem</th><th style="width:36%">{escape(col1)}</th><th class="c">{escape(unidade)}</th><th class="c">Parte do total</th><th class="c">Acumulado</th>'
         + (f'<th class="c">{escape(base_nome[0].upper() + base_nome[1:])}</th>' if bases else "")
         + (f'<th class="c">Por 100 {escape(base_nome)}</th>' if base or bases else "") + '<th>Classe</th></tr></thead>', '      <tbody>']
    for r in p:
        b = bases[r["nome"]] if bases else base
        o.append(f'        <tr><td class="c n">{r["k"]}</td><td><strong>{escape(r["nome"])}</strong></td><td class="c">{mil(r["v"])}</td><td class="c">{pc(r["pct"])}</td><td class="c">{pc(r["acc"])}</td>'
                 + (f'<td class="c">{mil(b)}</td>' if bases else "")
                 + (f'<td class="c">{br(taxa(r["v"], b))}</td>' if b else "") + f'<td>{chip(r["classe"])}</td></tr>')
    bt = sum(bases.values()) if bases else base
    o.append(f'        <tr class="tot"><td></td><td>Total</td><td class="c">{mil(tot)}</td><td class="c">100%</td><td class="c"></td>'
             + (f'<td class="c">{mil(bt)}</td>' if bases else "")
             + (f'<td class="c">{br(taxa(tot, bt))}</td>' if bt else "") + '<td></td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


ex1folha = folha_tab(EX1, f'Folha do período · motivo do atraso por dia da semana · {T1} atrasos em {mil(H1["base"])} entregas')
ex1pareto = pareto_tab(L1, "Pareto por motivo do atraso", "Motivo principal", "Atrasos", H1["base"], H1["base_nome"])
ex2folha = folha_tab(EX2, f'Folha do período · motivo da devolução por área requisitante · {T2} devoluções em {H2["base"]} requisições')
ex2pareto = pareto_tab(L2, "Pareto por motivo da devolução", "Motivo", "Devoluções", H2["base"], H2["base_nome"])
ex2area = pareto_tab(colunas(EX2), "Pareto por área requisitante · as colunas da mesma folha, com as requisições de cada área", "Área requisitante", "Devoluções",
                     base_nome=H2["base_nome"], bases=dict(zip(EX2["cols"], EX2["req"])))

# exemplo 3: por ocorrências e por peso
DEF = EX3["defeitos"]
R3N = [(n, q) for n, q, _ in DEF]
R3K = [(n, q * kg) for n, q, kg in DEF]
P3N, P3K = pareto(R3N), pareto(R3K)
ON = {r["nome"]: r for r in P3N}
OK_ = {r["nome"]: r for r in P3K}
o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>Bobinas reprovadas por defeito · {sum(q for _, q in R3N)} bobinas e {mil(sum(v for _, v in R3K))} kg refugados</caption>',
     '      <thead><tr><th style="width:30%">Defeito principal</th><th class="c">Bobinas</th><th class="c">Parte</th><th class="c">Ordem por bobinas</th>'
     '<th class="c">Quilos por bobina</th><th class="c">Quilos refugados</th><th class="c">Parte</th><th class="c">Ordem por quilos</th></tr></thead>', '      <tbody>']
for n, q, kg in DEF:
    a, b = ON[n], OK_[n]
    o.append(f'        <tr><td><strong>{escape(n)}</strong></td><td class="c">{q}</td><td class="c">{pc(a["pct"])}</td><td class="c{" hi" if a["k"] == 1 else ""}">{a["k"]}º</td>'
             f'<td class="c">{kg}</td><td class="c">{mil(q * kg)}</td><td class="c">{pc(b["pct"])}</td><td class="c{" hi" if b["k"] == 1 else ""}">{b["k"]}º</td></tr>')
o.append(f'        <tr class="tot"><td>Total</td><td class="c">{sum(q for _, q in R3N)}</td><td class="c">100%</td><td class="c"></td><td class="c"></td>'
         f'<td class="c">{mil(sum(v for _, v in R3K))}</td><td class="c">100%</td><td class="c"></td></tr>')
o += ['      </tbody>', '    </table>', '  </div>']
ex3tab = "\n".join(o)
ROT3 = {"Impressão fora de registro": "Impressão", "Espessura fora da especificação": "Espessura", "Solda fraca": "Solda fraca", "Furos e géis": "Furos e géis"}
e3 = ['      <svg viewBox="0 0 900 360" role="img" aria-label="Dois gráficos de Pareto das bobinas reprovadas. Por número de bobinas: ' + descr(R3N, "bobinas")
      + " Por quilos refugados: " + descr(R3K, "kg") + '">']
for ox, rows, un, tit in ((58, R3N, "bobinas", "Por número de bobinas"), (496, R3K, "kg", "Por quilos refugados")):
    g_, _, inf3 = pareto_g(rows, ox, 72, 324, 220, unidade=un, wrap=8, fs=10, rot=ROT3)
    e3.append(f'        <text class="b" x="{ox + 162}" y="26" font-size="12.5" text-anchor="middle">{tit} · total de {mil(inf3["total"])}</text>')
    e3 += g_
e3.append('        <text x="450" y="348" font-size="11.5" text-anchor="middle">Os mesmos registros, duas ordens. A barra da espessura passa da segunda para a primeira posição.</text>')
e3.append("      </svg>")

# ------------------------------------------------------------------ módulo 7: o Pareto da pizzaria
ch = ['      <svg id="bars" viewBox="0 0 900 400" role="img" aria-label="Gráfico de Pareto dos atrasos nas entregas da pizzaria, por motivo principal. ' + descr(L1, "atrasos") + '">',
      f'        <text class="b" x="450" y="24" font-size="12.5" text-anchor="middle">{escape(TIT1)}</text>']
g_, geo1, inf1 = pareto_g(L1, 80, 64, 740, 250, unidade="atrasos", wrap=18, fs=11.5, ident="bars")
ch += g_
ch.append(f'        <text class="mu halo" x="{80 + 740 - 6}" y="{inf1["yc"] - 6}" font-size="10.5" text-anchor="end">corte de 80%</text>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>Motivo principal</th><th class="c">Atrasos</th><th class="c">Parte do total</th><th class="c">Acumulado</th><th>Classe</th></tr></thead>', '          <tbody>']
for r in P1:
    tb.append(f'            <tr><td><strong>{escape(r["nome"])}</strong></td><td class="c">{r["v"]}</td><td class="c">{pc(r["pct"])}</td><td class="c">{pc(r["acc"])}</td><td>{r["classe"]}</td></tr>')
tb += ['          </tbody>', '        </table>']
npri = sum(1 for r in P1 if r["classe"] == PRIOR)
charttext = (f'  <p>A linha do acumulado chega a {pc(P1[1]["acc"])} na segunda barra e cruza o corte na terceira, com {pc(P1[npri - 1]["acc"])}. '
             f'São {npri} categorias na prioridade, de {len(P1) - 1} com nome: o gráfico é concentrado. A primeira barra, sozinha, tem {pc(P1[0]["pct"])} dos atrasos, '
             f'ou {br(taxa(P1[0]["v"], H1["base"]))} de cada 100 entregas. “Outros” tem {pc(P1[-1]["pct"])}, abaixo do limite de 10%, e fica por último mesmo sendo maior do que a barra do trânsito.</p>')

# antes e depois, em taxa por 100 entregas, na ordem do primeiro Pareto
DP = EX1["depois"]
ANT = {n: v for n, v in L1}
DEP = dict(zip((n for n, _, _ in EX1["folha"]), DP["valores"]))
PD = pareto(list(DEP.items()))
TD = sum(DP["valores"])
X0, SC, TOP, RH, BH = 300, 60, 56, 48, 14
bottom = TOP + RH * len(P1)
ad = [f'      <svg viewBox="0 0 900 {bottom + 50}" role="img" aria-label="Atrasos por 100 entregas, antes e depois das ações, por motivo. '
      + " ".join(f'{r["nome"]}: {br(taxa(ANT[r["nome"]], H1["base"]))} antes e {br(taxa(DEP[r["nome"]], DP["base"]))} depois.' for r in P1) + '">',
      '        <g font-size="11.5">',
      f'          <rect class="b-ant" x="{X0}" y="12" width="14" height="14"/><text x="{X0 + 22}" y="24">Antes · 15/06 a 09/07 · {mil(H1["base"])} entregas</text>',
      f'          <rect class="b-dep" x="{X0 + 290}" y="12" width="14" height="14"/><text x="{X0 + 312}" y="24">Depois · 10/08 a 06/09 · {mil(DP["base"])} entregas</text>',
      '        </g>']
for v in range(0, 10, 2):
    x = X0 + v * SC
    ad.append(f'        <line class="grid" x1="{x}" y1="{TOP - 8}" x2="{x}" y2="{bottom}"/>')
    ad.append(f'        <text class="mu" x="{x}" y="{bottom + 16}" font-size="11" text-anchor="middle"{TNUM}>{v}</text>')
ad.append(f'        <text class="mono mu" x="{X0 + 4 * SC}" y="{bottom + 38}" font-size="10" text-anchor="middle">ATRASOS POR 100 ENTREGAS</text>')
for k, r in enumerate(P1):
    y = TOP + RH * k + (RH - 2 * BH - 2) / 2
    a, d = taxa(ANT[r["nome"]], H1["base"]), taxa(DEP[r["nome"]], DP["base"])
    ad.append(f'        <text x="20" y="{y + 19}" font-size="12">{escape(r["nome"])}</text>')
    for j, (v, cls) in enumerate(((a, "b-ant"), (d, "b-dep"))):
        yy, x1 = y + j * (BH + 2), round(X0 + v * SC, 1)
        ad.append(f'        <path class="{cls}" d="M{X0} {yy} H{x1 - 3} Q{x1} {yy} {x1} {yy + 3} V{yy + BH - 3} Q{x1} {yy + BH} {x1 - 3} {yy + BH} H{X0} Z"/>')
        ad.append(f'        <text class="{"b" if j else "mu"}" x="{x1 + 7}" y="{yy + 11.5}" font-size="11.5"{TNUM}>{br(v)}</text>')
ad.append("      </svg>")
at = ['        <table class="aud">', '          <thead><tr><th>Motivo principal</th><th class="c">Atrasos antes</th><th class="c">Por 100 entregas</th><th class="c">Atrasos depois</th>'
      '<th class="c">Por 100 entregas</th><th class="c">Variação da taxa</th></tr></thead>', '          <tbody>']
for r in P1:
    a, d = taxa(ANT[r["nome"]], H1["base"]), taxa(DEP[r["nome"]], DP["base"])
    at.append(f'            <tr><td><strong>{escape(r["nome"])}</strong></td><td class="c">{ANT[r["nome"]]}</td><td class="c">{br(a)}</td><td class="c">{DEP[r["nome"]]}</td><td class="c">{br(d)}</td>'
              f'<td class="c">{"−" if d < a else "+"}{round(100 * abs(d - a) / a)}%</td></tr>')
ta, td_ = taxa(T1, H1["base"]), taxa(TD, DP["base"])
at.append(f'            <tr class="tot"><td>Total</td><td class="c">{T1}</td><td class="c">{br(ta)}</td><td class="c">{TD}</td><td class="c">{br(td_)}</td><td class="c">−{round(100 * (ta - td_) / ta)}%</td></tr>')
at += ['          </tbody>', '        </table>']
n0 = P1[0]["nome"]
assert PD[0]["nome"] == "Fila no forno"
adtext = (f'  <p>A taxa de atrasos caiu de {br(ta)} para {br(td_)} por 100 entregas. A barra tratada, a da pizza pronta que esperava entregador, passou de {br(taxa(ANT[n0], H1["base"]))} para '
          f'{br(taxa(DEP[n0], DP["base"]))}: a escala reforçada no pico funcionou. O endereço incompleto quase desapareceu, com o campo obrigatório. A fila no forno também caiu, de '
          f'{br(taxa(ANT["Fila no forno"], H1["base"]))} para {br(taxa(DEP["Fila no forno"], DP["base"]))}, porque a saída mais rápida deixou de somar espera à espera, mas ela não foi tratada, '
          f'e agora é a primeira barra, com {DEP["Fila no forno"]} dos {TD} atrasos, ou {pc(PD[0]["pct"])}. O novo Pareto entrega o problema do próximo ciclo. '
          f'Em contagem, os atrasos passaram de {T1} para {TD}; a comparação correta é a da taxa, porque o segundo período teve {mil(DP["base"])} entregas, e o primeiro, {mil(H1["base"])}.</p>')

# ------------------------------------------------------------------ módulo 10: figura da ISO
PARTES = [("9.1.1 · Definir os métodos", "Como os dados são coletados e analisados, para que o resultado seja válido.", "Folha com critério e categorias definidas"),
          ("9.1.3 · Analisar os dados", "Avaliar o desempenho e a necessidade de melhoria a partir dos dados.", "Pareto, com leitura e decisão registrada"),
          ("10.2 · Procurar a repetição", "Verificar se existem não conformidades parecidas.", "Contagem por tipo, por processo e por causa"),
          ("9.3 · Levar à direção", "As tendências entram na análise crítica.", "Pareto do período e o antes e depois")]
iso = ['      <svg viewBox="0 0 900 190" role="img" aria-label="O que a norma pede sobre análise de dados. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in PARTES) + '">']
for k, (a, b, c) in enumerate(PARTES):
    x = 10 + k * 222
    iso.append(f'        <rect class="bx" x="{x}" y="14" width="214" height="162"/>')
    iso.append(f'        <rect class="hd-ink" x="{x}" y="14" width="214" height="34"/>')
    iso.append(f'        <text class="b t-ground" x="{x + 12}" y="36" font-size="12">{escape(a)}</text>')
    yy = 70
    for l in textwrap.wrap(b, 32):
        iso.append(f'        <text x="{x + 12}" y="{yy}" font-size="11.5">{escape(l)}</text>')
        yy += 16
    yy = 138
    for l in textwrap.wrap("Neste estudo: " + c, 34)[:2]:
        iso.append(f'        <text class="mu" x="{x + 12}" y="{yy}" font-size="11">{escape(l)}</text>')
        yy += 15
iso.append("      </svg>")

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--DAFIG-->", "\n".join(da)), ("<!--FLUXO-->", "\n".join(fl)), ("<!--FOLHAFIG-->", "\n".join(fo)), ("<!--ANATOMIA-->", "\n".join(an)),
                 ("<!--EX1HEAD-->", ficha(H1)), ("<!--EX1FOLHA-->", ex1folha), ("<!--EX1PARETO-->", ex1pareto),
                 ("<!--EX2HEAD-->", ficha(H2)), ("<!--EX2FOLHA-->", ex2folha), ("<!--EX2PARETO-->", ex2pareto), ("<!--EX2AREA-->", ex2area),
                 ("<!--EX3HEAD-->", ficha(EX3["head"])), ("<!--EX3TAB-->", ex3tab), ("<!--EX3FIG-->", "\n".join(e3)),
                 ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHARTTEXT-->", charttext),
                 ("<!--ADFIG-->", "\n".join(ad)), ("<!--ADTABLE-->", "\n".join(at)), ("<!--ADTEXT-->", adtext),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Pareto e folha de verificação</title>")
assert "Pareto e folha de verificação" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| atrasos:", T1, "| devoluções:", T2,
      "| prioridade:", [r["nome"] for r in P1 if r["classe"] == PRIOR])
