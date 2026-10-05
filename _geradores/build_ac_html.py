# -*- coding: utf-8 -*-
"""Monta treinamento-analise-critica.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ac_data import (A_ABERTA, A_ATRASO, A_PRAZO, A_VENCIDA, ATE, CHECK, CRI, CRITERIOS, ENTRADAS, EX1, EX2, FAV, ITENS, MEL, MUD, NOME, PAUTA,  # noqa: E402
                     REC, SAIDAS, SITS, TIPOS, TRIMESTRES, decisoes, historico, situacao_acao)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# situações: paleta validada para daltonismo nos dois modos (azul, âmbar e vermelho), a mesma do estudo de Indicadores
LIGHT = ("\n  --s1:#2A6FB0; --s1-tint:#DCE8F3;\n  --s2:#D19A2E; --s2-tint:#F8EBCB;\n  --s3:#B0413E; --s3-tint:#F5DEDC;\n  --on-s2:#16242E;")
DARK = ("\n  --s1:#4F97DB; --s1-tint:#1B2F42;\n  --s2:#B58E14; --s2-tint:#3A2C12;\n  --s3:#D14B45; --s3-tint:#3D1F1E;\n  --on-s2:#0F171C;")
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Situação da entrada e tipo de saída */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.s1{background:var(--s1)} .chip.s2{background:var(--s2);color:var(--on-s2)} .chip.s3{background:var(--s3)}
.chip.sl{background:var(--sunk);color:var(--ink);box-shadow:inset 0 0 0 1px var(--rule)}
svg .hd-ink{fill:var(--ink)}
svg .f1{fill:var(--s1)} svg .f2{fill:var(--s2)} svg .f3{fill:var(--s3)}
svg .on2{fill:var(--on-s2)}
svg .diag{fill:var(--sunk)}
svg .dot{fill:var(--ink)}
svg .seg{stroke:var(--surface);stroke-width:2}
svg .halo{paint-order:stroke;stroke:var(--surface);stroke-width:5px;stroke-linejoin:round}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas dos exemplos */
table.aud{font-size:.8rem;min-width:860px;line-height:1.4}
table.aud th, table.aud td{padding:8px 9px}
table.aud td.n{white-space:nowrap;font-weight:600;color:var(--muted)}
table.aud td.c, table.aud th.c{text-align:center;font-variant-numeric:tabular-nums}
table.aud td.nw{white-space:nowrap;font-variant-numeric:tabular-nums}
table.aud td small{display:block;color:var(--muted);font-size:.76rem;margin-top:3px}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha da reunião (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

SCLS = {FAV: "s1", ATE: "s2", CRI: "s3"}
ESTUDO = {"w5h2": ("5W2H", "../5W2H/treinamento-5w2h.html"), "swot": ("Matriz SWOT", "../SWOT/treinamento-swot.html"),
          "ind": ("Indicadores", "../Indicadores/treinamento-indicadores.html"), "proc": ("Mapa de processos", "../Processos/treinamento-processos.html"),
          "nc": ("Não conformidade", "../Nao-Conformidade/treinamento-nao-conformidade.html"), "auditoria": ("Auditoria interna", "../Auditoria/treinamento-auditoria.html"),
          "riscos": ("Matriz de riscos", "../Riscos/treinamento-riscos.html"), "pdca": ("PDCA", "../PDCA/treinamento-pdca.html"),
          "sat": ("Satisfação do cliente", "../Satisfacao/treinamento-satisfacao.html"), "forn": ("Fornecedores", "../Fornecedores/treinamento-fornecedores.html"),
          "rec": ("Recursos", "../Recursos/treinamento-recursos.html")}
assert all(os.path.exists(os.path.join(os.path.dirname(os.path.abspath(SRC)), v[1])) for v in ESTUDO.values() if "Processos" not in v[1])


def dt(d):
    return d.strftime("%d/%m/%Y") if d else ""


def reais(v):
    return "R$ " + f"{v:,.0f}".replace(",", ".")


def chip(s):
    return f'<span class="chip {SCLS[s]}">{s}</span>'


def plural(n, um, varios):
    return f"{n} {um if n == 1 else varios}"


# ------------------------------------------------------------------ módulo 4: entradas
o = ['  <div class="tbl">', '    <table>',
     '      <thead><tr><th style="width:9%">Item</th><th style="width:25%">Entrada</th><th style="width:36%">O que a direção quer saber</th><th>Onde buscar</th></tr></thead>',
     '      <tbody>']
for item, nome, olhar, fonte, _ in ENTRADAS:
    o.append(f'        <tr><td class="num">9.3.2 {item}</td><td><strong>{nome}</strong></td><td>{escape(olhar)}</td><td>{escape(fonte)}</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>']
entradastab = "\n".join(o)

RY = 32
fh = 54 + RY * len(ENTRADAS) + 6
fo = [f'      <svg viewBox="0 0 900 {fh}" role="img" aria-label="As doze entradas da análise crítica e onde buscar cada uma. '
      + " ".join(f'{i}, {n.lower()}: {f.lower()}' + (f', do estudo de {ESTUDO[k][0]}.' if k else ".") for i, n, _, f, k in ENTRADAS) + '">',
      '        <defs><marker id="a3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah-mu" d="M0 0 L10 5 L0 10 z"/></marker></defs>',
      '        <rect class="hd-ink" x="20" y="14" width="330" height="34"/>',
      '        <text class="b t-ground" x="36" y="36" font-size="13">Entrada da análise crítica</text>',
      '        <rect class="hd-ink" x="410" y="14" width="470" height="34"/>',
      '        <text class="b t-ground" x="426" y="36" font-size="13">Onde buscar</text>']
for k, (item, nome, _, fonte, est) in enumerate(ENTRADAS):
    y = 54 + RY * k
    fo.append(f'        <rect class="bx" x="20" y="{y}" width="330" height="{RY - 4}"/>')
    fo.append(f'        <text x="36" y="{y + 19}" font-size="12"><tspan class="b">{item}</tspan>  {escape(nome)}</text>')
    fo.append(f'        <line class="ln-mu" x1="352" y1="{y + 14}" x2="406" y2="{y + 14}" marker-end="url(#a3)"/>')
    fo.append(f'        <rect class="{"bx" if est else "diag"}" x="410" y="{y}" width="470" height="{RY - 4}"/>')
    fo.append(f'        <text x="426" y="{y + 19}" font-size="12">{escape(fonte)}</text>')
    if est:
        fo.append(f'        <a href="{ESTUDO[est][1]}"><text class="b" x="866" y="{y + 19}" font-size="11.5" text-anchor="end">{escape(ESTUDO[est][0])}</text></a>')
    else:
        fo.append(f'        <text class="mu" x="866" y="{y + 19}" font-size="11" text-anchor="end">sem estudo na série</text>')
fo.append("      </svg>")

# ------------------------------------------------------------------ módulo 5: saídas
TCH = {MEL: "Melhoria", MUD: "Mudança no sistema", REC: "Recursos"}
o = ['  <div class="tbl">', '    <table>',
     '      <thead><tr><th style="width:9%">Item</th><th style="width:25%">Saída</th><th style="width:36%">O que a direção decide</th><th>Exemplo</th></tr></thead>',
     '      <tbody>']
for tipo, letra, nome, desc, ex in SAIDAS:
    o.append(f'        <tr><td class="num">9.3.3 {letra}</td><td><strong>{nome}</strong></td><td>{escape(desc)}</td><td>{escape(ex)}</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>']
saidastab = "\n".join(o)


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    pres = sum(1 for p in ex["part"] if p[3] == "Presente")
    o = ['  <dl class="ficha">',
         f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
         f'    <div><dt>Data e período</dt><dd>{dt(h["data"])}. {escape(h["periodo"])}</dd></div>',
         f'    <div><dt>Participantes</dt><dd>{escape(h["conduz"])}, que conduz, e mais {pres - 1} presentes</dd></div>',
         f'    <div><dt>Análise anterior</dt><dd>{dt(h["anterior"]) if h["anterior"] else "Não houve"}</dd></div>',
         f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
         '  </dl>']
    return "\n".join(o)


def painel(ex, nome):
    cont = {s: sum(1 for e in ex["entradas"] if e["sit"] == s) for s in SITS}
    o = [f'      <svg viewBox="0 0 900 366" role="img" aria-label="Painel das doze entradas da análise crítica da {nome}. '
         + " ".join(f'{e["item"]}, {NOME[e["item"]].lower()}: {e["sit"].lower()}, {e["tend"].lower()}, {plural(len(decisoes(ex, e["item"])), "decisão", "decisões")}.' for e in ex["entradas"])
         + '">']
    for k, e in enumerate(ex["entradas"]):
        x, y = 10 + (k % 3) * 296, 10 + (k // 3) * 84
        nd = len(decisoes(ex, e["item"]))
        o.append(f'        <rect class="bx" x="{x}" y="{y}" width="288" height="76"/>')
        o.append(f'        <rect class="f{SCLS[e["sit"]][1]}" x="{x}" y="{y}" width="8" height="76"/>')
        o.append(f'        <text x="{x + 22}" y="{y + 24}" font-size="12"><tspan class="mono mu" font-size="10.5">{e["item"].upper()}</tspan>  <tspan class="b">{escape(NOME[e["item"]])}</tspan></text>')
        o.append(f'        <text x="{x + 22}" y="{y + 46}" font-size="12"><tspan class="b">{e["sit"]}</tspan> · {e["tend"].lower()}</text>')
        o.append(f'        <text class="mu" x="{x + 22}" y="{y + 64}" font-size="11">{plural(nd, "decisão", "decisões") if nd else "sem decisão"}</text>')
    o.append('        <g font-size="11.5">')
    xs = 10
    for s in SITS:
        o.append(f'          <rect class="f{SCLS[s][1]}" x="{xs}" y="346" width="14" height="14"/><text x="{xs + 22}" y="358">{s}: {cont[s]}</text>')
        xs += 150
    o.append('        </g>')
    o.append("      </svg>")
    return "\n".join(o)


def ent_tab(ex):
    o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Entradas analisadas</caption>',
         '      <thead><tr><th>Item</th><th style="width:16%">Entrada</th><th style="width:30%">Resultado no período</th><th style="width:10%">Tendência</th>'
         '<th style="width:9%">Situação</th><th style="width:23%">Conclusão da direção</th><th class="c">Decisão nº</th></tr></thead>', '      <tbody>']
    for e in ex["entradas"]:
        ds = ", ".join(str(s["n"]) for s in decisoes(ex, e["item"])) or "—"
        o.append(f'        <tr><td class="n">{e["item"]}</td><td><strong>{escape(NOME[e["item"]])}</strong><small>{escape(e["quem"])}</small></td>'
                 f'<td>{escape(e["resultado"])}<small>Fonte: {escape(e["fonte"][0].lower() + e["fonte"][1:]) if not e["fonte"].startswith(("Matriz", "Mapa", "Diagnóstico")) else escape(e["fonte"])}</small></td>'
                 f'<td>{e["tend"]}</td><td>{chip(e["sit"])}</td><td>{escape(e["conclusao"])}</td><td class="c">{ds}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def sai_tab(ex):
    total = sum(s["valor"] or 0 for s in ex["saidas"])
    o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Saídas: decisões e ações</caption>',
         '      <thead><tr><th>Nº</th><th style="width:8%">Entrada</th><th style="width:15%">Tipo</th><th style="width:34%">Decisão</th><th style="width:15%">Responsável</th>'
         '<th style="width:9%">Prazo</th><th>Recurso</th></tr></thead>', '      <tbody>']
    for s in ex["saidas"]:
        rec = escape(s["recurso"]) if s["recurso"] else "—"
        if s["valor"]:
            rec += f'<small>{reais(s["valor"])}</small>'
        o.append(f'        <tr><td class="n">{s["n"]}</td><td class="c">{s["item"]}</td><td><span class="chip sl">{s["tipo"]}</span></td><td>{escape(s["decisao"])}</td>'
                 f'<td>{escape(s["quem"])}</td><td class="nw">{dt(s["prazo"])}</td><td>{rec}</td></tr>')
    o.append(f'        <tr><td colspan="6"><strong>Recursos aprovados na reunião</strong></td><td class="nw"><strong>{reais(total)}</strong></td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def sis_tab(ex):
    o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Avaliação do sistema</caption>',
         '      <thead><tr><th style="width:14%">Critério</th><th style="width:32%">Pergunta</th><th style="width:10%">Resposta</th><th>Justificativa</th></tr></thead>', '      <tbody>']
    for (nome, perg, _), (resp, just) in zip(CRITERIOS, ex["sistema"]):
        o.append(f'        <tr><td><strong>{nome}</strong></td><td>{escape(perg)}</td><td>{resp}</td><td>{escape(just)}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def ant_tab(ex):
    ref = ex["head"]["data"]
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>Entrada “a” · ações das análises anteriores, em {dt(ref)}</caption>',
         '      <thead><tr><th>Nº</th><th style="width:9%">Análise</th><th style="width:24%">Ação decidida</th><th style="width:14%">Responsável</th><th style="width:9%">Prazo</th>'
         '<th style="width:15%">Situação</th><th>Resultado</th></tr></thead>', '      <tbody>']
    cls = {A_PRAZO: "s1", A_ATRASO: "s2", A_VENCIDA: "s3", A_ABERTA: "sl"}
    for a in ex["anteriores"]:
        s = situacao_acao(a, ref)
        res = (f'Eficaz: {a["eficaz"].lower()}. ' if a["eficaz"] else "") + a["obs"]
        o.append(f'        <tr><td class="n">{a["n"]}</td><td class="nw">{dt(a["origem"])}</td><td>{escape(a["acao"])}</td><td>{escape(a["quem"])}</td><td class="nw">{dt(a["prazo"])}</td>'
                 f'<td><span class="chip {cls[s]}">{s}</span></td><td>{escape(res.strip()) or "—"}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


# ------------------------------------------------------------------ exemplo 3: pauta dividida
GX, GY, CW, CH = 360, 50, 110, 28
n = len(ITENS)
mh = GY + n * CH + 40
tot = [sum(PAUTA[i][k] for i in ITENS) for k in range(4)]
px = [f'      <svg viewBox="0 0 900 {mh}" role="img" aria-label="Pauta da análise crítica dividida em quatro reuniões. '
      + " ".join(f"{t}: {tot[k]} entradas." for k, t in enumerate(TRIMESTRES)) + " "
      + " ".join(f"{i}, {NOME[i].lower()}: " + ", ".join(t.lower() for k, t in enumerate(TRIMESTRES) if PAUTA[i][k]) + "." for i in ITENS) + '">',
      f'        <text class="mono mu" x="20" y="{GY - 14}" font-size="9.5">ENTRADA</text>',
      f'        <text class="mono mu" x="{GX + 4 * CW + 50}" y="{GY - 14}" font-size="9.5" text-anchor="middle">VEZES NO ANO</text>']
for k, t in enumerate(TRIMESTRES):
    px.append(f'        <text class="b" x="{GX + k * CW + CW / 2}" y="{GY - 14}" font-size="12" text-anchor="middle">{t}</text>')
px.append(f'        <rect class="diag" x="{GX + 3 * CW + 1}" y="{GY}" width="{CW - 2}" height="{n * CH}"/>')
for r, i in enumerate(ITENS):
    y = GY + r * CH
    px.append(f'        <line class="grid" x1="20" y1="{y}" x2="{GX + 4 * CW + 100}" y2="{y}"/>')
    px.append(f'        <text x="20" y="{y + 19}" font-size="11.5"><tspan class="b">{i}</tspan>  {escape(NOME[i])}</text>')
    for k in range(4):
        if PAUTA[i][k]:
            px.append(f'        <circle class="dot" cx="{GX + k * CW + CW / 2}" cy="{y + CH / 2}" r="5.5"/>')
    px.append(f'        <text class="b" x="{GX + 4 * CW + 50}" y="{y + 19}" font-size="12" text-anchor="middle" style="font-variant-numeric:tabular-nums">{sum(PAUTA[i])}</text>')
yb = GY + n * CH
px.append(f'        <line class="grid" x1="20" y1="{yb}" x2="{GX + 4 * CW + 100}" y2="{yb}"/>')
for k in range(5):
    px.append(f'        <line class="grid" x1="{GX + k * CW}" y1="{GY}" x2="{GX + k * CW}" y2="{yb}"/>')
px.append(f'        <text class="mono mu" x="{GX - 12}" y="{yb + 22}" font-size="9.5" text-anchor="end">ENTRADAS NA REUNIÃO</text>')
for k in range(4):
    px.append(f'        <text class="b" x="{GX + k * CW + CW / 2}" y="{yb + 22}" font-size="12" text-anchor="middle" style="font-variant-numeric:tabular-nums">{tot[k]}</text>')
px.append("      </svg>")

# ------------------------------------------------------------------ módulo 7: decisões das análises anteriores
H = historico()
ROT = ["Concluídas no prazo", "Concluídas com atraso", "Não concluídas"]
X0, U, TOP, RH, BH = 200, 60, 58, 44, 24
bottom = TOP + RH * len(H)
HH = bottom + 46
vmax = max(sum(r[1:]) for r in H)
ch = [f'      <svg id="bars" viewBox="0 0 900 {HH}" role="img" aria-label="Gráfico de barras empilhadas com as decisões das quatro últimas análises críticas da indústria. '
      + " ".join(f"{r[0]}: {r[1]} concluídas no prazo, {r[2]} concluídas com atraso e {r[3]} não concluídas." for r in H) + '">',
      '        <g font-size="11.5">']
xs = X0
for k, t in enumerate(ROT):
    ch.append(f'          <rect class="f{k + 1}" x="{xs}" y="12" width="14" height="14"/><text x="{xs + 22}" y="24">{t}</text>')
    xs += 40 + len(t) * 6.6
ch.append('        </g>')
for v in range(0, vmax + 2, 2):
    x = X0 + v * U
    ch.append(f'        <line class="grid" x1="{x}" y1="{TOP - 8}" x2="{x}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{x}" y="{bottom + 16}" font-size="11" text-anchor="middle" style="font-variant-numeric:tabular-nums">{v}</text>')
ch.append(f'        <text class="mono mu" x="{X0 + (vmax + 1) * U / 2}" y="{bottom + 36}" font-size="10" text-anchor="middle">DECISÕES</text>')
for k, (rot, a, b, c) in enumerate(H):
    y = TOP + RH * k + (RH - BH) / 2
    t = a + b + c
    ch.append(f'        <text x="20" y="{y + 16:.1f}" font-size="12"><tspan class="b">{rot}</tspan><tspan class="mu"> · {t} decisões</tspan></text>')
    x = X0
    for j, v in enumerate((a, b, c)):
        if not v:
            continue
        ch.append(f'        <rect class="seg f{j + 1}" data-k="{k}" x="{x}" y="{y:.1f}" width="{v * U}" height="{BH}"/>')
        ch.append(f'        <text class="b {"on2" if j == 1 else "on"}" x="{x + v * U / 2}" y="{y + 16.5:.1f}" font-size="12" text-anchor="middle" pointer-events="none">{v}</text>')
        x += v * U
    ch.append(f'        <text class="halo" x="{x + 10}" y="{y + 16:.1f}" font-size="11.5"><tspan class="b">{round(100 * (a + b) / t)}%</tspan><tspan class="mu"> concluídas</tspan></text>')
for k, (rot, a, b, c) in enumerate(H):
    t = a + b + c
    ch.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" '
              f'aria-label="Análise de {rot}: {t} decisões, {a} concluídas no prazo, {b} com atraso e {c} não concluídas" data-k="{k}" data-r="{rot}" '
              f'data-t="{t}" data-a="{a}" data-b="{b}" data-c="{c}" data-pct="{round(100 * (a + b) / t)}%" data-cx="{X0 + t * U / 2:.1f}"/>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>Análise crítica</th><th class="c">Decisões</th>' + "".join(f'<th class="c">{t}</th>' for t in ROT)
      + '<th class="c">Percentual concluído</th></tr></thead>', '          <tbody>']
for rot, a, b, c in H:
    tb.append(f'            <tr><td><strong>{rot}</strong></td><td class="c">{a + b + c}</td><td class="c">{a}</td><td class="c">{b}</td><td class="c">{c}</td>'
              f'<td class="c">{round(100 * (a + b) / (a + b + c))}%</td></tr>')
tb += ['          </tbody>', '        </table>']
EXT = {2: "duas", 3: "três", 4: "quatro"}
d25, d26 = sum(sum(r[1:]) for r in H[:2]), sum(sum(r[1:]) for r in H[2:])
p25, p26 = sum(r[1] for r in H[:2]), sum(r[1] for r in H[2:])
c25, c26 = sum(r[1] + r[2] for r in H[:2]), sum(r[1] + r[2] for r in H[2:])
assert (2 * p25 == d25) and (8 * p26 == 5 * d26) and c25 / d25 > c26 / d26, (p25, d25, p26, d26, c25, c26)  # "metade", "cinco em cada oito" e "caiu"
charttext = (f'  <p>Nas duas análises de 2025, a direção tomou {d25} decisões, e {p25} foram concluídas no prazo. Nas duas de 2026, tomou {d26}, e {p26} foram concluídas no prazo. '
             f'O cumprimento no prazo subiu, de metade das decisões para cinco em cada oito, mas a parte concluída, no prazo ou com atraso, caiu de {c25} em {d25} para {c26} em {d26}. '
             f'As {EXT[H[-1][3]]} decisões não concluídas de agosto de 2026 têm a mesma origem: '
             'foram tomadas sem o recurso aprovado e sem acompanhamento entre uma análise e outra.</p>')

# ------------------------------------------------------------------ módulo 10: os quatro critérios
cr = ['      <svg viewBox="0 0 900 164" role="img" aria-label="Os quatro critérios da avaliação do sistema. '
      + " ".join(f"{n}: {p} {d}" for n, p, d in CRITERIOS) + '">']
for k, (nome, perg, desc) in enumerate(CRITERIOS):
    x = 10 + k * 222
    cr.append(f'        <rect class="bx" x="{x}" y="10" width="214" height="144"/>')
    cr.append(f'        <rect class="hd-ink" x="{x}" y="10" width="214" height="34"/>')
    cr.append(f'        <text class="b t-ground" x="{x + 14}" y="32" font-size="13">{nome}</text>')
    yy = 66
    for l in textwrap.wrap(perg, 30):
        cr.append(f'        <text class="b" x="{x + 14}" y="{yy}" font-size="12">{escape(l)}</text>')
        yy += 16
    yy += 10
    for l in textwrap.wrap(desc, 33):
        cr.append(f'        <text class="mu" x="{x + 14}" y="{yy}" font-size="11.5">{escape(l)}</text>')
        yy += 16
    assert yy < 158, nome
cr.append("      </svg>")

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--ENTRADASTAB-->", entradastab), ("<!--FONTES-->", "\n".join(fo)), ("<!--SAIDASTAB-->", saidastab),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1PAINEL-->", painel(EX1, "pizzaria")), ("<!--EX1ENT-->", ent_tab(EX1)), ("<!--EX1SAI-->", sai_tab(EX1)),
                 ("<!--EX1SIS-->", sis_tab(EX1)), ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2ANT-->", ant_tab(EX2)), ("<!--EX2PAINEL-->", painel(EX2, "indústria")),
                 ("<!--EX2ENT-->", ent_tab(EX2)), ("<!--EX2SAI-->", sai_tab(EX2)), ("<!--EX2SIS-->", sis_tab(EX2)), ("<!--PAUTA-->", "\n".join(px)),
                 ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHARTTEXT-->", charttext), ("<!--CRIT-->", "\n".join(cr)),
                 ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Análise crítica pela direção</title>")
assert "Análise crítica" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| entradas:", len(ENTRADAS),
      "| decisões:", len(EX1["saidas"]), len(EX2["saidas"]), "| histórico:", H)
