# -*- coding: utf-8 -*-
"""Monta treinamento-fornecedores.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from forn_data import (CHECK, CICLO, CLASSES, CRITERIOS, CRITICO, EX1, EX2, HOMOLOG, PESOS, S_DOC, S_HOM, S_VENC, SIM, VALIDADE, pct, proxima)  # noqa: E402

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# classes: paleta de quatro cores validada para daltonismo nos dois modos (azul, âmbar, vermelho, roxo)
LIGHT = ("\n  --s1:#2A6FB0; --s1-tint:#DCE8F3;\n  --s2:#D19A2E; --s2-tint:#F8EBCB;\n  --s3:#B0413E; --s3-tint:#F5DEDC;\n  --s4:#7A3E9A; --s4-tint:#EADFF0;\n  --on-s2:#16242E;")
DARK = ("\n  --s1:#4F97DB; --s1-tint:#1B2F42;\n  --s2:#B58E14; --s2-tint:#3A2C12;\n  --s3:#D14B45; --s3-tint:#3D1F1E;\n  --s4:#A45BC0; --s4-tint:#33203C;\n  --on-s2:#0F171C;")
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Classes e situações */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.s1{background:var(--s1)} .chip.s2{background:var(--s2);color:var(--on-s2)} .chip.s3{background:var(--s3)} .chip.s4{background:var(--s4)}
.chip.sl{background:var(--sunk);color:var(--ink);box-shadow:inset 0 0 0 1px var(--rule)}
.cl{display:inline-grid;place-items:center;width:1.9em;height:1.9em;font:700 .9em/1 var(--display);color:var(--on-hue)}
.cl.A{background:var(--s1)} .cl.B{background:var(--s2);color:var(--on-s2)} .cl.C{background:var(--s3)} .cl.D{background:var(--s4)}
svg .hd-ink{fill:var(--ink)}
svg .f1{fill:var(--s1)} svg .f2{fill:var(--s2)} svg .f3{fill:var(--s3)} svg .f4{fill:var(--s4)}
svg .z1{fill:var(--s1-tint)} svg .z2{fill:var(--s2-tint)} svg .z3{fill:var(--s3-tint)} svg .z4{fill:var(--s4-tint)}
svg .on2{fill:var(--on-s2)}
svg .cell{fill:var(--surface)}
svg .seg{fill:var(--ink)}
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

/* Ficha da avaliação (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

CCLS = {"A": "s1", "B": "s2", "C": "s3", "D": "s4"}
COND = {c: cond for c, _, _, cond in CLASSES}
NOME_CL = {c: nome for c, _, nome, _ in CLASSES}


def dt(d):
    return d.strftime("%d/%m/%Y") if d else "—"


def br(v, casas=1):
    return f"{v:.{casas}f}".replace(".", ",")


def cl(c):
    return f'<span class="cl {c}" title="Classe {c}">{c}</span>'


def situacao(f, ref):
    if not f["homologado"]:
        return S_DOC
    if f["docs"] != SIM:
        return "Documentos pendentes"
    return S_VENC if proxima(f["homologado"], VALIDADE) < ref else S_HOM


# ------------------------------------------------------------------ figura 1: ciclo
W, G = 200, 20
ci = ['      <svg viewBox="0 0 900 214" role="img" aria-label="O ciclo do fornecedor, em quatro etapas. ' + " ".join(f"{n}: {d}" for n, d in CICLO)
      + ' Da reavaliação, o ciclo volta ao controle, ou termina na desqualificação.">',
      '        <defs><marker id="a1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah" d="M0 0 L10 5 L0 10 z"/></marker>'
      '<marker id="a1m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah-mu" d="M0 0 L10 5 L0 10 z"/></marker></defs>']
for k, (nome, desc) in enumerate(CICLO):
    x = 10 + k * (W + G)
    cls = ["bx-p", "bx", "bx-d", "bx-c"][k]
    ci.append(f'        <rect class="{cls}" x="{x}" y="20" width="{W}" height="120"/>')
    ci.append(f'        <text class="mono mu" x="{x + 14}" y="42" font-size="10">{k + 1}{" · S" if k == 0 else " · A" if k == 2 else " · R" if k == 3 else ""}</text>')
    ci.append(f'        <text class="b" x="{x + 14}" y="66" font-size="13">{escape(nome)}</text>')
    for j, l in enumerate(textwrap.wrap(desc, 30)[:3]):
        ci.append(f'        <text x="{x + 14}" y="{90 + j * 15}" font-size="11">{escape(l)}</text>')
    if k < 3:
        ci.append(f'        <line class="ln" x1="{x + W + 1}" y1="80" x2="{x + W + G - 2}" y2="80" marker-end="url(#a1)"/>')
ci.append(f'        <path class="ln-mu dash" d="M{10 + 3 * (W + G) + W / 2} 142 V172 H{10 + W + G + W / 2} V146" marker-end="url(#a1m)"/>')
ci.append('        <text class="mu" x="450" y="166" font-size="11" text-anchor="middle">quem continua volta ao controle; quem não continua sai da lista</text>')
ci.append('        <text x="450" y="204" font-size="11.5" text-anchor="middle">Os dados da avaliação nascem no controle: sem registro no recebimento, a avaliação é opinião.</text>')
ci.append("      </svg>")

# ------------------------------------------------------------------ módulo 4: critérios e ficha
o = ['  <div class="tbl">', '    <table>',
     '      <thead><tr><th style="width:22%">Critério</th><th style="width:38%">O que se confere</th><th>Evidência</th></tr></thead>', '      <tbody>']
for nome, oque, ev in CRITERIOS:
    o.append(f'        <tr><td><strong>{escape(nome)}</strong></td><td>{escape(oque)}</td><td>{escape(ev)}</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>']
criterios = "\n".join(o)

hf = ['      <svg viewBox="0 0 900 300" role="img" aria-label="A ficha de homologação. No cabeçalho: fornecedor, o que fornece, data e quem avaliou. No corpo, os seis critérios, cada um com o resultado, atende, não atende ou pendente, e a evidência. No rodapé, a decisão: homologado, com validade, ou não homologado.">',
      '        <rect class="bx" x="80" y="16" width="740" height="268"/>',
      '        <rect class="hd-ink" x="80" y="16" width="740" height="52"/>',
      '        <g font-size="11">',
      '          <text class="mono t-ground" x="98" y="36" font-size="10">FORNECEDOR</text><text class="b t-ground" x="98" y="56" font-size="13">F-13 · Resinas Atlântico · resina de polietileno</text>',
      '          <text class="mono t-ground" x="620" y="36" font-size="10">DATA · AVALIADORES</text><text class="t-ground" x="620" y="56" font-size="11.5">05/03/2027 · Compras e Qualidade</text>',
      '        </g>']
for k, (nome, res, ev) in enumerate(HOMOLOG["itens"]):
    y = 84 + k * 28
    hf.append(f'        <rect class="{"band" if k % 2 else "cell"}" x="98" y="{y}" width="704" height="26" style="stroke:none"/>')
    hf.append(f'        <text class="b" x="108" y="{y + 17}" font-size="11">{escape(nome)}</text>')
    cls = "s1" if res == "Atende" else ("s2" if res == "Pendente" else "s3")
    hf.append(f'        <rect class="f{cls[1]}" x="300" y="{y + 5}" width="{62 if res == "Pendente" else 52}" height="16"/>')
    hf.append(f'        <text class="b {"on2" if cls == "s2" else "on"}" x="{331 if res == "Pendente" else 326}" y="{y + 17}" font-size="10" text-anchor="middle">{escape(res)}</text>')
    hf.append(f'        <text class="mu" x="380" y="{y + 17}" font-size="10.5">{escape(textwrap.shorten(ev, 82))}</text>')
hf.append('        <rect class="band" x="80" y="256" width="740" height="28"/>')
hf.append('        <text class="mono mu" x="98" y="274" font-size="10">DECISÃO</text>')
hf.append('        <text class="b" x="170" y="274" font-size="11.5">Em homologação: aguarda o laudo do ensaio e o lote piloto. Validade, quando homologado: 24 meses.</text>')
hf.append("      </svg>")

# ------------------------------------------------------------------ módulo 5: pesos, cálculo e classes
o = ['  <div class="tbl">', '    <table>',
     '      <thead><tr><th style="width:20%">Componente</th><th style="width:10%">Peso</th><th style="width:40%">Como se mede</th><th>De onde vem o dado</th></tr></thead>', '      <tbody>']
for nome, peso, como in PESOS:
    fonte = {"Qualidade": "Registro de recebimento: lotes aceitos e recusados.", "Prazo": "Registro de recebimento: data combinada e data da entrega.",
             "Atendimento": "Nota dada pelo comprador no fim do período."}[nome]
    o.append(f'        <tr><td><strong>{nome}</strong></td><td class="num">{peso}%</td><td>{escape(como)}</td><td>{fonte}</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>']
pesos = "\n".join(o)

EXF = next(a for a in EX1["avals"] if a["cod"] == "F-07")
q, p, a_ = pct(EXF["aceitos"], EXF["recebidos"]), pct(EXF["no_prazo"], EXF["entregas"]), EXF["nota"] / 10
ff = [f'      <svg viewBox="0 0 900 236" role="img" aria-label="O cálculo do índice para o fornecedor de caixas de papelão. Qualidade: {EXF["aceitos"]} lotes aceitos de {EXF["recebidos"]}, '
      f'{round(100 * q)}%, com peso 50, vale {br(50 * q)} pontos. Prazo: {EXF["no_prazo"]} entregas no prazo de {EXF["entregas"]}, {round(100 * p)}%, com peso 30, vale {br(30 * p)} pontos. '
      f'Atendimento: nota {EXF["nota"]}, {round(100 * a_)}%, com peso 20, vale {br(20 * a_)} pontos. Índice: {br(EXF["indice"])}, classe {EXF["classe"]}, {NOME_CL[EXF["classe"]].lower()}.">',
      '        <defs><marker id="a4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah" d="M0 0 L10 5 L0 10 z"/></marker></defs>']
comp = [("QUALIDADE · PESO 50", f'{EXF["aceitos"]} de {EXF["recebidos"]} lotes aceitos', f"{round(100 * q)}% × 50", br(50 * q), "bx-p"),
        ("PRAZO · PESO 30", f'{EXF["no_prazo"]} de {EXF["entregas"]} entregas no prazo', f"{round(100 * p)}% × 30", br(30 * p), "bx-d"),
        ("ATENDIMENTO · PESO 20", f'nota {EXF["nota"]} de 10', f"{round(100 * a_)}% × 20", br(20 * a_), "bx-c")]
for k, (t, d, f, v, cls) in enumerate(comp):
    x = 10 + k * 208
    ff.append(f'        <rect class="{cls}" x="{x}" y="20" width="196" height="120"/>')
    ff.append(f'        <text class="mono mu" x="{x + 14}" y="42" font-size="10">{t}</text>')
    ff.append(f'        <text x="{x + 14}" y="68" font-size="11.5">{escape(d)}</text>')
    ff.append(f'        <text class="mu" x="{x + 14}" y="90" font-size="11">{f}</text>')
    ff.append(f'        <text class="b" x="{x + 14}" y="124" font-size="20">{v}</text>')
    if k < 2:
        ff.append(f'        <text class="b" x="{x + 202}" y="86" font-size="18" text-anchor="middle">+</text>')
ff.append('        <text class="b" x="638" y="86" font-size="18" text-anchor="middle">=</text>')
ff.append('        <rect class="bx-ink" x="654" y="20" width="236" height="120"/>')
ff.append('        <text class="mono t-ground" x="668" y="42" font-size="10">ÍNDICE DE DESEMPENHO</text>')
ff.append(f'        <text class="b t-ground" x="668" y="90" font-size="30">{br(EXF["indice"])}</text>')
ff.append(f'        <text class="t-ground" x="668" y="124" font-size="11.5">Classe {EXF["classe"]} · {NOME_CL[EXF["classe"]]}</text>')
ff.append(f'        <text x="450" y="176" font-size="11.5" text-anchor="middle">{escape(COND[EXF["classe"]])}</text>')
ff.append('        <text class="mu" x="450" y="200" font-size="11" text-anchor="middle">Índice = 50 × qualidade + 30 × prazo + 20 × atendimento, com os três em percentual.</text>')
ff.append('        <text class="mu" x="450" y="220" font-size="11" text-anchor="middle">O prazo, e não a qualidade, é o que derruba este fornecedor: é sobre logística que a conversa precisa ser.</text>')
ff.append("      </svg>")

o = ['  <div class="tbl">', '    <table>',
     '      <thead><tr><th style="width:8%">Classe</th><th style="width:14%">Índice</th><th style="width:22%">Nome</th><th>Conduta</th></tr></thead>', '      <tbody>']
for k, (c, minimo, nome, cond) in enumerate(CLASSES):
    faixa = f"{minimo} ou mais" if k == 0 else f"de {minimo} a {CLASSES[k - 1][1] - 0.1:g}".replace(".", ",") if minimo else f"abaixo de {CLASSES[k - 1][1]}"
    o.append(f'        <tr><td>{cl(c)}</td><td>{faixa}</td><td><strong>{nome}</strong></td><td>{escape(cond)}</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>']
classes = "\n".join(o)


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Data e período</dt><dd>{dt(h["data"])}. {escape(h["periodo"])}</dd></div>',
                      f'    <div><dt>Quem avaliou</dt><dd>{escape(h["por"])}</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      '  </dl>'])


def forns_tab(ex):
    ref = ex["head"]["data"]
    o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Cadastro e homologação</caption>',
         '      <thead><tr><th>Código</th><th style="width:20%">Fornecedor</th><th style="width:24%">O que fornece</th><th style="width:14%">Tipo</th><th style="width:10%">Criticidade</th>'
         '<th class="c">Homologado em</th><th class="c">Válida até</th><th>Situação</th></tr></thead>', '      <tbody>']
    for f in ex["forns"]:
        s = situacao(f, ref)
        cls = {S_HOM: "s1", S_VENC: "s2", S_DOC: "s3", "Documentos pendentes": "s2"}[s]
        o.append(f'        <tr><td class="n">{f["cod"]}</td><td><strong>{escape(f["nome"])}</strong></td><td>{escape(f["fornece"])}</td><td>{f["tipo"]}</td><td>{f["crit"]}</td>'
                 f'<td class="c">{dt(f["homologado"])}</td><td class="c">{proxima(f["homologado"], VALIDADE).strftime("%m/%Y") if f["homologado"] else "—"}</td>'
                 f'<td><span class="chip {cls}">{s}</span></td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def aval_tab(ex):
    nomes = {f["cod"]: f["nome"] for f in ex["forns"]}
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>Avaliação de desempenho · {escape(ex["head"]["periodo"].lower())}</caption>',
         '      <thead><tr><th>Código</th><th style="width:16%">Fornecedor</th><th class="c">Lotes aceitos</th><th class="c">Qualidade</th><th class="c">Entregas no prazo</th><th class="c">Prazo</th>'
         '<th class="c">Nota</th><th class="c">Índice</th><th class="c">Classe</th><th>Observação e conduta</th></tr></thead>', '      <tbody>']
    for a in ex["avals"]:
        q, p = pct(a["aceitos"], a["recebidos"]), pct(a["no_prazo"], a["entregas"])
        obs = (escape(a["obs"]) + " " if a["obs"] else "") + f"<small>{escape(COND[a['classe']])}</small>"
        o.append(f'        <tr><td class="n">{a["cod"]}</td><td><strong>{escape(nomes[a["cod"]])}</strong></td><td class="c">{a["aceitos"]} de {a["recebidos"]}</td><td class="c">{round(100 * q)}%</td>'
                 f'<td class="c">{a["no_prazo"]} de {a["entregas"]}</td><td class="c">{round(100 * p)}%</td><td class="c">{a["nota"]}</td><td class="c"><strong>{br(a["indice"])}</strong></td>'
                 f'<td class="c">{cl(a["classe"])}</td><td>{obs}</td></tr>')
    cont = {c: sum(1 for a in ex["avals"] if a["classe"] == c) for c, _, _, _ in CLASSES}
    o.append('        <tr class="tot"><td colspan="8">Fornecedores por classe</td><td colspan="2">' + " · ".join(f"{c}: {n}" for c, n in cont.items()) + '</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


ex3head = "\n".join(['  <dl class="ficha">',
                     f'    <div><dt>Fornecedor</dt><dd>{HOMOLOG["cod"]} · {escape(HOMOLOG["nome"])} · {escape(HOMOLOG["fornece"].lower())}</dd></div>',
                     f'    <div><dt>Data e avaliadores</dt><dd>{dt(HOMOLOG["data"])}. {escape(HOMOLOG["por"])}</dd></div>',
                     f'    <div><dt>Origem</dt><dd>{escape(HOMOLOG["origem"])}</dd></div>',
                     '  </dl>'])
o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Ficha de homologação</caption>',
     '      <thead><tr><th style="width:22%">Critério</th><th style="width:12%">Resultado</th><th>Evidência</th></tr></thead>', '      <tbody>']
for nome, res, ev in HOMOLOG["itens"]:
    cls = "s1" if res == "Atende" else ("s2" if res == "Pendente" else "s3")
    o.append(f'        <tr><td><strong>{escape(nome)}</strong></td><td><span class="chip {cls}">{res}</span></td><td>{escape(ev)}</td></tr>')
o.append(f'        <tr class="tot"><td>Decisão</td><td colspan="2">{escape(HOMOLOG["resultado"])}</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>']
ex3itens = "\n".join(o)

# ------------------------------------------------------------------ módulo 7: carteira
EX = EX1
nomes = {f["cod"]: f["nome"] for f in EX["forns"]}
ordem = sorted(EX["avals"], key=lambda a: -a["indice"])
X0, U, TOP, RH, BH = 300, 5.6, 58, 32, 18   # 100 pontos = 560 px
bottom = TOP + RH * len(ordem)
HH = bottom + 46
ch = [f'      <svg id="bars" viewBox="0 0 900 {HH}" role="img" aria-label="Gráfico de barras com o índice de desempenho dos doze fornecedores críticos da indústria, em ordem decrescente, sobre as faixas das classes. '
      + " ".join(f'{a["cod"]}, {nomes[a["cod"]]}: {br(a["indice"])}, classe {a["classe"]}.' for a in ordem) + '">']
zonas = [(0, 60, "z4", "D"), (60, 75, "z3", "C"), (75, 90, "z2", "B"), (90, 100, "z1", "A")]
for a0, b0, z, c in zonas:
    ch.append(f'        <rect class="{z}" x="{X0 + a0 * U}" y="{TOP - 8}" width="{(b0 - a0) * U}" height="{bottom - TOP + 8}"/>')
    ch.append(f'        <text class="b" x="{X0 + (a0 + b0) / 2 * U}" y="{TOP - 16}" font-size="12" text-anchor="middle">Classe {c}</text>')
for v in (0, 60, 75, 90, 100):
    x = X0 + v * U
    ch.append(f'        <line class="grid" x1="{x}" y1="{TOP - 8}" x2="{x}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{x}" y="{bottom + 16}" font-size="11" text-anchor="middle" style="font-variant-numeric:tabular-nums">{v}</text>')
ch.append(f'        <text class="mono mu" x="{X0 + 50 * U}" y="{bottom + 36}" font-size="10" text-anchor="middle">ÍNDICE DE DESEMPENHO</text>')
for k, a in enumerate(ordem):
    y = TOP + RH * k + (RH - BH) / 2
    x1 = X0 + a["indice"] * U
    ch.append(f'        <text x="20" y="{y + 13:.1f}" font-size="11.5"><tspan class="b">{a["cod"]}</tspan> · {escape(nomes[a["cod"]])}</text>')
    ch.append(f'        <path class="seg" data-k="{k}" d="M{X0} {y:.1f} H{x1 - 4:.1f} Q{x1:.1f} {y:.1f} {x1:.1f} {y + 4:.1f} V{y + BH - 4:.1f} Q{x1:.1f} {y + BH:.1f} {x1 - 4:.1f} {y + BH:.1f} H{X0} Z"/>')
    ch.append(f'        <text class="halo" x="{x1 + 8:.1f}" y="{y + 13:.1f}" font-size="11.5"><tspan class="b">{br(a["indice"])}</tspan></text>')
for k, a in enumerate(ordem):
    q, p = pct(a["aceitos"], a["recebidos"]), pct(a["no_prazo"], a["entregas"])
    ch.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" '
              f'aria-label="{a["cod"]}, {escape(nomes[a["cod"]])}: índice {br(a["indice"])}, classe {a["classe"]}" data-k="{k}" data-id="{a["cod"]}" data-n="{escape(nomes[a["cod"]])}" '
              f'data-i="{br(a["indice"])}" data-c="{a["classe"]}" data-q="{round(100 * q)}%" data-p="{round(100 * p)}%" data-a="{a["nota"]} de 10" data-cx="{X0 + a["indice"] * U / 2:.1f}"/>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>Fornecedor</th><th class="c">Qualidade</th><th class="c">Prazo</th><th class="c">Atendimento</th><th class="c">Índice</th><th class="c">Classe</th></tr></thead>',
      '          <tbody>']
for a in ordem:
    tb.append(f'            <tr><td><strong>{a["cod"]} · {escape(nomes[a["cod"]])}</strong></td><td class="c">{round(100 * pct(a["aceitos"], a["recebidos"]))}%</td>'
              f'<td class="c">{round(100 * pct(a["no_prazo"], a["entregas"]))}%</td><td class="c">{a["nota"]}</td><td class="c">{br(a["indice"])}</td><td class="c">{a["classe"]}</td></tr>')
tb += ['          </tbody>', '        </table>']
borda = [a for a in ordem if a["classe"] == "A" and a["indice"] < 92]
charttext = (f'  <p>Oito dos doze fornecedores estão na classe A, e a leitura fácil seria “a carteira é boa”. As bordas contam outra história: {" e ".join(a["cod"] for a in borda)} estão a menos de dois pontos da classe B, '
             'e os dois fornecedores de classe C caíram por prazo e por lotes recusados que o recebimento registrou lote a lote. O fornecedor único de resina, F-01, tem 93,7 pontos e é, ainda assim, o maior risco da carteira: '
             'o índice mede o que ele entregou, e não o que acontece se ele parar.</p>')

# ------------------------------------------------------------------ módulo 10: figura da ISO
PARTES = [("8.4.1 · Critérios", "Avaliar, selecionar, monitorar e reavaliar os provedores externos, com critérios definidos e evidência retida.", "Cadastro, Homologação e Avaliação"),
          ("8.4.2 · Controle", "Controle proporcional ao efeito do fornecimento. Processos terceirizados sob controle. Verificação do que é recebido.", "Criticidade, recebimento e ocorrências"),
          ("8.4.3 · Informação", "Comunicar ao fornecedor os requisitos do produto, da aprovação, da competência e do controle.", "Pedido de compra com os requisitos")]
iso = ['      <svg viewBox="0 0 900 214" role="img" aria-label="As três partes do requisito 8.4. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in PARTES) + '">']
for k, (a, b, c) in enumerate(PARTES):
    x = 10 + k * 298
    iso.append(f'        <rect class="bx" x="{x}" y="14" width="284" height="186"/>')
    iso.append(f'        <rect class="hd-ink" x="{x}" y="14" width="284" height="34"/>')
    iso.append(f'        <text class="b t-ground" x="{x + 14}" y="36" font-size="13">{escape(a)}</text>')
    yy = 70
    for l in textwrap.wrap(b, 42):
        iso.append(f'        <text x="{x + 14}" y="{yy}" font-size="11.5">{escape(l)}</text>')
        yy += 16
    iso.append(f'        <text class="mu" x="{x + 14}" y="186" font-size="11">Neste estudo: {escape(c)}</text>')
iso.append("      </svg>")

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--CICLO-->", "\n".join(ci)), ("<!--CRITERIOS-->", criterios), ("<!--HOMOLOGFIG-->", "\n".join(hf)), ("<!--PESOS-->", pesos),
                 ("<!--INDICEFIG-->", "\n".join(ff)), ("<!--CLASSES-->", classes), ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1FORNS-->", forns_tab(EX1)),
                 ("<!--EX1AVAL-->", aval_tab(EX1)), ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2FORNS-->", forns_tab(EX2)), ("<!--EX2AVAL-->", aval_tab(EX2)),
                 ("<!--EX3HEAD-->", ex3head), ("<!--EX3ITENS-->", ex3itens), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)),
                 ("<!--CHARTTEXT-->", charttext), ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Avaliação de fornecedores</title>")
assert "Avaliação de fornecedores" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| classes:",
      {c: sum(1 for a in EX1["avals"] if a["classe"] == c) for c, _, _, _ in CLASSES}, "| borda:", [a["cod"] for a in borda])
