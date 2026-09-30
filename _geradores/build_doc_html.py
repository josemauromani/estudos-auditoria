# -*- coding: utf-8 -*-
"""Monta treinamento-informacao-documentada.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doc_data import (CHECK, CICLO, EX1, EX2, EXT, IND_DOCS, S_APROV, S_CODIGO, S_EMREV, S_OBS, S_REV, S_VENC, S_VIG, TIPOS, proxima,  # noqa: E402
                      situacao)
from iso_data import DOCS, MANTER, RETER  # noqa: E402

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# situações: paleta validada para daltonismo nos dois modos (azul, âmbar e vermelho), a mesma dos estudos de Indicadores e de Análise crítica
LIGHT = ("\n  --s1:#2A6FB0; --s1-tint:#DCE8F3;\n  --s2:#D19A2E; --s2-tint:#F8EBCB;\n  --s3:#B0413E; --s3-tint:#F5DEDC;\n  --on-s2:#16242E;")
DARK = ("\n  --s1:#4F97DB; --s1-tint:#1B2F42;\n  --s2:#B58E14; --s2-tint:#3A2C12;\n  --s3:#D14B45; --s3-tint:#3D1F1E;\n  --on-s2:#0F171C;")
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Situação do documento e tipo de informação */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.s1{background:var(--s1)} .chip.s2{background:var(--s2);color:var(--on-s2)} .chip.s3{background:var(--s3)}
.chip.p{background:var(--p)} .chip.d{background:var(--d)} .chip.c{background:var(--c)}
.chip.sl{background:var(--sunk);color:var(--ink);box-shadow:inset 0 0 0 1px var(--rule)}
svg .hd-ink{fill:var(--ink)}
svg .f1{fill:var(--s1)} svg .f2{fill:var(--s2)} svg .f3{fill:var(--s3)}
svg .on2{fill:var(--on-s2)}
svg .seg{stroke:var(--surface);stroke-width:2}
svg .halo{paint-order:stroke;stroke:var(--surface);stroke-width:5px;stroke-linejoin:round}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas dos exemplos */
table.aud{font-size:.8rem;min-width:860px;line-height:1.4}
table.aud th, table.aud td{padding:8px 9px}
table.aud td.n{white-space:nowrap;font-weight:600;color:var(--muted)}
table.aud td.c, table.aud th.c{text-align:center;font-variant-numeric:tabular-nums}
table.aud td.nw{white-space:nowrap;font-variant-numeric:tabular-nums}
table.aud td.cod{white-space:nowrap;font:500 .78rem var(--mono)}
table.aud td small{display:block;color:var(--muted);font-size:.76rem;margin-top:3px}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha do levantamento (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

SCLS = {S_VIG: "s1", S_VENC: "s2", S_EMREV: "sl", S_OBS: "sl", S_CODIGO: "s3", S_APROV: "s3", S_REV: "s3"}
TNOME = {t[0]: t[1] for t in TIPOS}
TCURTO = {"PO": "POLÍTICA", "MP": "MAPA", "PR": "PROCEDIMENTO", "IT": "INSTRUÇÃO", "ES": "ESPECIFICAÇÃO", "FR": "FORMULÁRIO", "DE": "EXTERNO"}


def dt(d):
    return d.strftime("%d/%m/%Y") if d else "—"


def mes(d):
    return d.strftime("%m/%Y")


def chip(s):
    return f'<span class="chip {SCLS[s]}">{s}</span>'


def meses(v):
    if v < 12:
        return "1 mês" if v == 1 else f"{v} meses"
    return "1 ano" if v == 12 else (f"{v // 12} anos" if v % 12 == 0 else f"{v} meses")


# ------------------------------------------------------------------ módulo 1: tipos
o = ['  <div class="tbl">', '    <table>',
     '      <thead><tr><th style="width:8%">Sigla</th><th style="width:22%">Tipo</th><th style="width:36%">O que é</th><th>Exemplos</th></tr></thead>', '      <tbody>']
for sigla, nome, oque, ex in TIPOS:
    o.append(f'        <tr><td class="num">{sigla}</td><td><strong>{nome}</strong></td><td>{escape(oque)}</td><td>{escape(ex)}</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>']
tipos = "\n".join(o)

# ------------------------------------------------------------------ módulo 3: ciclo de vida
W, G = 138, 12
ci = ['      <svg viewBox="0 0 900 214" role="img" aria-label="O ciclo de vida de um documento, em seis etapas. ' + " ".join(f"{n}: {d}" for n, d in CICLO)
      + ' Da revisão, o ciclo volta à elaboração. A versão anterior vira obsoleta e sai de circulação.">',
      '        <defs><marker id="a3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah" d="M0 0 L10 5 L0 10 z"/></marker>'
      '<marker id="a3m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah-mu" d="M0 0 L10 5 L0 10 z"/></marker></defs>']
for k, (nome, desc) in enumerate(CICLO):
    x = 6 + k * (W + G)
    cls = "bx-ink" if k == 2 else "bx"
    tc = ' class="t-ground"' if k == 2 else ""
    ci.append(f'        <rect class="{cls}" x="{x}" y="20" width="{W}" height="120"/>')
    ci.append(f'        <text class="mono {"t-ground" if k == 2 else "mu"}" x="{x + 12}" y="40" font-size="10">{k + 1}</text>')
    ci.append(f'        <text class="b{" t-ground" if k == 2 else ""}" x="{x + 12}" y="62" font-size="12.5">{escape(nome)}</text>')
    for j, l in enumerate(textwrap.wrap(desc, 22)[:3]):
        ci.append(f'        <text{tc} x="{x + 12}" y="{86 + j * 15}" font-size="10.5">{escape(l)}</text>')
    if k < 5:
        ci.append(f'        <line class="ln" x1="{x + W + 1}" y1="80" x2="{x + W + G - 2}" y2="80" marker-end="url(#a3)"/>')
ci.append(f'        <path class="ln-mu dash" d="M{6 + 5 * (W + G) + W / 2} 142 V172 H{6 + W / 2} V146" marker-end="url(#a3m)"/>')
ci.append('        <text class="mu" x="450" y="166" font-size="11" text-anchor="middle">na data prevista, ou quando o processo muda, o ciclo recomeça</text>')
ci.append('        <text x="450" y="204" font-size="11.5" text-anchor="middle">A aprovação é o momento em que a revisão passa a valer. Antes dela, o documento é um rascunho.</text>')
ci.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Data e participantes</dt><dd>{dt(h["data"])}. {escape(h["por"])}</dd></div>',
                      f'    <div><dt>Regra de revisão</dt><dd>{escape(h["regra"])}</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      '  </dl>'])


def docs_tab(ex, titulo):
    ref = ex["head"]["data"]
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{escape(titulo)}</caption>',
         '      <thead><tr><th>Código</th><th style="width:20%">Título</th><th style="width:9%">Tipo</th><th style="width:13%">Processo</th><th style="width:9%">Revisão</th>'
         '<th style="width:14%">Elaborou · aprovou</th><th style="width:12%">Meio e local</th><th style="width:8%">Próxima</th><th>Situação</th></tr></thead>', '      <tbody>']
    for d in ex["docs"]:
        s = situacao(d, ref)
        rev = f'{d["rev"]}<small>{dt(d["data"])}</small>' if d["rev"] else "—"
        apr = escape(d["aprovou"]) if d["aprovou"] else "<small>sem aprovação</small>"
        prox = mes(proxima(d)) if d["data"] and d["status"] != "Obsoleto" else "—"
        o.append(f'        <tr><td class="cod">{escape(d["codigo"]) or "—"}</td><td><strong>{escape(d["titulo"])}</strong></td><td>{TNOME[d["tipo"]]}</td><td>{escape(d["processo"])}</td>'
                 f'<td class="c">{rev}</td><td>{escape(d["elaborou"])}<small>{apr}</small></td><td>{d["meio"]}<small>{escape(d["onde"])}</small></td><td class="c">{prox}</td><td>{chip(s)}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def regs_tab(ex, titulo):
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{escape(titulo)}</caption>',
         '      <thead><tr><th style="width:20%">Registro</th><th style="width:13%">Formulário</th><th style="width:14%">Processo</th><th style="width:13%">Gerado em</th>'
         '<th style="width:15%">Guardado em</th><th class="c">Retenção</th><th style="width:13%">Acesso</th><th>Disposição</th></tr></thead>', '      <tbody>']
    for r in ex["regs"]:
        o.append(f'        <tr><td><strong>{escape(r["nome"])}</strong></td><td>{escape(r["form"])}</td><td>{escape(r["processo"])}</td><td>{escape(r["gerado"])}</td>'
                 f'<td>{escape(r["guardado"])}<small>{r["meio"]}</small></td><td class="c">{meses(r["meses"])}</td><td>{escape(r["acesso"])}</td><td>{escape(r["disposicao"])}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


# figura 6: documentos ligados à IT-EXP-01
lg = ['      <svg viewBox="0 0 900 236" role="img" aria-label="A instrução IT-EXP-01, expedição e agrupamento por zona, e os quatro documentos ligados a ela: '
      + "; ".join(f"{a}, {b.lower()}" for a, b in EX1["ligados"]) + '. Quando a instrução muda, os quatro precisam ser conferidos.">',
      '        <defs><marker id="a6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah-mu" d="M0 0 L10 5 L0 10 z"/></marker></defs>',
      '        <rect class="bx-ink" x="320" y="16" width="260" height="66"/>',
      '        <text class="mono t-ground" x="336" y="38" font-size="10">IT-EXP-01 · REV. 2 · 10/07/2026</text>',
      '        <text class="b t-ground" x="336" y="62" font-size="13">Expedição e agrupamento por zona</text>',
      '        <text class="mu" x="450" y="112" font-size="11" text-anchor="middle">quando a instrução muda, estes quatro precisam ser conferidos</text>']
n = len(EX1["ligados"])
bw = (880 - (n - 1) * 16) / n
for k, (a, b) in enumerate(EX1["ligados"]):
    x = 10 + k * (bw + 16)
    cx = x + bw / 2
    lg.append(f'        <line class="ln-mu" x1="{cx:.1f}" y1="84" x2="{cx:.1f}" y2="130" marker-end="url(#a6)"/>')
    lg.append(f'        <rect class="bx" x="{x:.1f}" y="134" width="{bw:.1f}" height="64"/>')
    lg.append(f'        <text class="mono mu" x="{x + 14:.1f}" y="156" font-size="10">{escape(a.upper())}</text>')
    lg.append(f'        <text class="b" x="{x + 14:.1f}" y="180" font-size="12">{escape(b)}</text>')
lg.append('        <text x="450" y="226" font-size="11.5" text-anchor="middle">Foi o roteiro, à esquerda, que ficou na revisão antiga e gerou o RNC 2026-05.</text>')
lg.append("      </svg>")

# figura 7: documentos no fluxo de compras
by_code = {d["codigo"]: d for d in EX2["docs"] if d["codigo"]}
by_title = {d["titulo"]: d for d in EX2["docs"]}
etapas = EX2["fluxo"]
n = len(etapas)
ew = (880 - (n - 1) * 10) / n
fx = ['      <svg viewBox="0 0 900 236" role="img" aria-label="Os documentos do processo de aquisição, por etapa. '
      + " ".join(f"{e}: " + ", ".join(cs) + "." for e, cs in etapas) + '">']
for k, (etapa, cods) in enumerate(etapas):
    x = 10 + k * (ew + 10)
    a = 12
    pts = f"{x:.1f},20 {x + ew - a:.1f},20 {x + ew:.1f},44 {x + ew - a:.1f},68 {x:.1f},68" + (f" {x + a:.1f},44" if k else "")
    fx.append(f'        <polygon class="bx-d" points="{pts}"/>')
    fx.append(f'        <text class="b" x="{x + ew / 2 + (a / 2 if k else 0):.1f}" y="49" font-size="12.5" text-anchor="middle">{escape(etapa)}</text>')
    for j, c in enumerate(cods):
        d = by_code.get(c) or next(v for t, v in by_title.items() if t.startswith(c))
        y = 82 + j * 70
        fx.append(f'        <rect class="bx" x="{x:.1f}" y="{y}" width="{ew:.1f}" height="60"/>')
        fx.append(f'        <text class="mono mu" x="{x + 10:.1f}" y="{y + 19}" font-size="10">{escape(d["codigo"] or "SEM CÓDIGO")} · {TCURTO[d["tipo"]]}</text>')
        for i, l in enumerate(textwrap.wrap(d["titulo"], 26)[:2]):
            fx.append(f'        <text x="{x + 10:.1f}" y="{y + 38 + i * 14}" font-size="10.5">{escape(l)}</text>')
fx.append("      </svg>")

# exemplo 3: documentos externos
ref3 = EX2["head"]["data"]
et = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Documentos de origem externa</caption>',
      '      <thead><tr><th style="width:20%">Documento</th><th style="width:11%">Origem</th><th style="width:11%">Versão em uso</th><th style="width:14%">Onde se aplica</th>'
      '<th style="width:20%">Como se sabe da atualização</th><th class="c">Verificado em</th><th class="c">Próxima</th><th>Situação</th></tr></thead>', '      <tbody>']
for e in EXT:
    prox = proxima({"data": e["verificado"], "meses": e["meses"]})
    s = "Verificado" if prox >= ref3 else "Verificação vencida"
    et.append(f'        <tr><td><strong>{escape(e["nome"])}</strong></td><td>{escape(e["origem"])}</td><td>{escape(e["versao"])}</td><td>{escape(e["onde"])}</td>'
              f'<td>{escape(e["como"])}</td><td class="c">{dt(e["verificado"])}</td><td class="c">{mes(prox)}</td>'
              f'<td><span class="chip {"s1" if s == "Verificado" else "s2"}">{s}</span></td></tr>')
et += ['      </tbody>', '    </table>', '  </div>']

# ------------------------------------------------------------------ módulo 7: documentos por processo
ROT = ["Em dia", "Revisão vencida", "Sem controle"]
X0, U, TOP, RH, BH = 300, 26, 58, 36, 20
H = IND_DOCS
bottom = TOP + RH * len(H)
HH = bottom + 46
vmax = max(a + b + c for _, a, b, c in H)
ch = [f'      <svg id="bars" viewBox="0 0 900 {HH}" role="img" aria-label="Gráfico de barras empilhadas com os documentos de cada processo da indústria, por situação. '
      + " ".join(f"{p}: {a} em dia, {b} com revisão vencida e {c} sem controle." for p, a, b, c in H) + '">', '        <g font-size="11.5">']
xs = X0
for k, t in enumerate(ROT):
    ch.append(f'          <rect class="f{k + 1}" x="{xs}" y="12" width="14" height="14"/><text x="{xs + 22}" y="24">{t}</text>')
    xs += 40 + len(t) * 6.6
ch.append('        </g>')
for v in range(0, vmax + 3, 2):
    x = X0 + v * U
    ch.append(f'        <line class="grid" x1="{x}" y1="{TOP - 8}" x2="{x}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{x}" y="{bottom + 16}" font-size="11" text-anchor="middle" style="font-variant-numeric:tabular-nums">{v}</text>')
ch.append(f'        <text class="mono mu" x="{X0 + (vmax + 2) * U / 2}" y="{bottom + 36}" font-size="10" text-anchor="middle">DOCUMENTOS</text>')
for k, (p, a, b, c) in enumerate(H):
    y = TOP + RH * k + (RH - BH) / 2
    t = a + b + c
    ch.append(f'        <text x="20" y="{y + 14:.1f}" font-size="11.5">{escape(p)}</text>')
    x = X0
    for j, v in enumerate((a, b, c)):
        if not v:
            continue
        ch.append(f'        <rect class="seg f{j + 1}" data-k="{k}" x="{x}" y="{y:.1f}" width="{v * U}" height="{BH}"/>')
        if v >= 2:
            ch.append(f'        <text class="b {"on2" if j == 1 else "on"}" x="{x + v * U / 2}" y="{y + 14.5:.1f}" font-size="11" text-anchor="middle" pointer-events="none">{v}</text>')
        x += v * U
    ch.append(f'        <text class="halo" x="{x + 8}" y="{y + 14:.1f}" font-size="11.5"><tspan class="b">{round(100 * a / t)}%</tspan><tspan class="mu"> em dia</tspan></text>')
for k, (p, a, b, c) in enumerate(H):
    t = a + b + c
    ch.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" '
              f'aria-label="{escape(p)}: {t} documentos, {a} em dia, {b} com revisão vencida e {c} sem controle" data-k="{k}" data-r="{escape(p)}" '
              f'data-t="{t}" data-a="{a}" data-b="{b}" data-c="{c}" data-pct="{round(100 * a / t)}%" data-cx="{X0 + t * U / 2:.1f}"/>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>Processo</th><th class="c">Documentos</th>' + "".join(f'<th class="c">{t}</th>' for t in ROT)
      + '<th class="c">Em dia</th></tr></thead>', '          <tbody>']
for p, a, b, c in H:
    tb.append(f'            <tr><td><strong>{escape(p)}</strong></td><td class="c">{a + b + c}</td><td class="c">{a}</td><td class="c">{b}</td><td class="c">{c}</td><td class="c">{round(100 * a / (a + b + c))}%</td></tr>')
TA, TB, TC = (sum(r[i] for r in H) for i in (1, 2, 3))
tb.append(f'            <tr class="tot"><td>Total</td><td class="c">{TA + TB + TC}</td><td class="c">{TA}</td><td class="c">{TB}</td><td class="c">{TC}</td><td class="c">{round(100 * TA / (TA + TB + TC))}%</td></tr>')
tb += ['          </tbody>', '        </table>']
pior = min(H, key=lambda r: r[1] / (r[1] + r[2] + r[3]))
mais = max(H, key=lambda r: r[2] + r[3])
charttext = (f'  <p>A indústria tem {TA + TB + TC} documentos na lista mestra, e {round(100 * TA / (TA + TB + TC))}% estão em dia. A leitura por processo muda a conversa: '
             f'a Manutenção tem {pior[1]} documentos em dia de {sum(pior[1:])}, e é o processo que mais precisa de ajuda, porque os documentos sem controle são os que foram '
             f'criados pela própria área, sem passar pelo ciclo. A Produção tem o maior número de pendências, {mais[2] + mais[3]}, mas em um conjunto de {sum(mais[1:])} documentos. '
             f'As {TB} revisões vencidas são, na maior parte, instruções escritas na implantação e nunca relidas.</p>')

# ------------------------------------------------------------------ módulo 10: o que a norma pede
CH = {MANTER: "p", RETER: "d"}
dt_ = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Informação documentada exigida pela ISO 9001:2015, em resumo</caption>',
       '      <thead><tr><th>Requisito</th><th style="width:12%">Tipo</th><th style="width:48%">O que precisa existir</th><th>Exemplo</th></tr></thead>', '      <tbody>']
for num, tipo, oque, ex in DOCS:
    cls = CH.get(tipo, "c")
    dt_.append(f'        <tr><td class="n">{num}</td><td><span class="chip {cls}">{tipo}</span></td><td>{escape(oque)}</td><td>{escape(ex)}</td></tr>')
dt_ += ['      </tbody>', '    </table>', '  </div>']
nm, nr = sum(1 for d in DOCS if d[1] == MANTER), sum(1 for d in DOCS if d[1] == RETER)

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--TIPOS-->", tipos), ("<!--CICLO-->", "\n".join(ci)), ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1DOCS-->", docs_tab(EX1, "Lista mestra da pizzaria")),
                 ("<!--LIGADOS-->", "\n".join(lg)), ("<!--EX1REGS-->", regs_tab(EX1, "Tabela de retenção da pizzaria")), ("<!--EX2HEAD-->", ficha(EX2)),
                 ("<!--FLUXO-->", "\n".join(fx)), ("<!--EX2DOCS-->", docs_tab(EX2, "Lista mestra do processo de compras")), ("<!--EX2REGS-->", regs_tab(EX2, "Registros do processo de compras")),
                 ("<!--EXT-->", "\n".join(et)), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHARTTEXT-->", charttext),
                 ("<!--DOCSTAB-->", "\n".join(dt_)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Informação documentada</title>")
assert "Informação documentada" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| documentos:", len(EX1["docs"]), len(EX2["docs"]),
      "| exigidos:", len(DOCS), f"({nm} manter, {nr} reter)", "| indústria:", TA + TB + TC)
