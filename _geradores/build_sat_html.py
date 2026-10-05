# -*- coding: utf-8 -*-
"""Monta treinamento-satisfacao.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sat_data import CHECK, ETAPAS, EX1, EX2, FONTES, PRAZO_RESPOSTA, PRAZO_SOLUCAO, RECLAMACAO, SATISFEITO, nps, resumo_mes  # noqa: E402

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# promotores, neutros e detratores: paleta de três cores validada para daltonismo nos dois modos (azul, âmbar, vermelho)
LIGHT = ("\n  --s1:#2A6FB0; --s1-tint:#DCE8F3;\n  --s2:#D19A2E; --s2-tint:#F8EBCB;\n  --s3:#B0413E; --s3-tint:#F5DEDC;\n  --on-s2:#16242E;")
DARK = ("\n  --s1:#4F97DB; --s1-tint:#1B2F42;\n  --s2:#B58E14; --s2-tint:#3A2C12;\n  --s3:#D14B45; --s3-tint:#3D1F1E;\n  --on-s2:#0F171C;")
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Situações e famílias */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.s1{background:var(--s1)} .chip.s2{background:var(--s2);color:var(--on-s2)} .chip.s3{background:var(--s3)}
.chip.sl{background:var(--sunk);color:var(--ink);box-shadow:inset 0 0 0 1px var(--rule)}
svg .hd-ink{fill:var(--ink)}
svg .f1{fill:var(--s1)} svg .f2{fill:var(--s2)} svg .f3{fill:var(--s3)}
svg .on2{fill:var(--on-s2)}
svg .cell{fill:var(--surface)}
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
table.aud td.lo{background:var(--s3-tint)}
table.aud td small, table.aud th small{display:block;color:var(--muted);font-size:.76rem;margin-top:3px;font-weight:400}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha da pesquisa (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")


def dt(d):
    return d.strftime("%d/%m/%Y") if d else "—"


def br(v, casas=1):
    return f"{v:.{casas}f}".replace(".", ",")


# ------------------------------------------------------------------ figura 1: as três famílias
fo = ['      <svg viewBox="0 0 900 270" role="img" aria-label="As três famílias de fontes. ' + " ".join(f"{a}: {b} Mede: {c}" for a, b, c in FONTES)
      + ' As três levam à percepção do cliente, que é analisada e vira ação.">',
      '        <defs><marker id="a1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah" d="M0 0 L10 5 L0 10 z"/></marker></defs>']
for k, (a, b, c) in enumerate(FONTES):
    y = 20 + k * 74
    cls = ["bx-p", "bx-d", "bx-c"][k]
    fo.append(f'        <rect class="{cls}" x="10" y="{y}" width="330" height="62"/>')
    fo.append(f'        <text class="mono mu" x="24" y="{y + 20}" font-size="10">O CLIENTE {a.upper()}</text>')
    for j, l in enumerate(textwrap.wrap(b, 50)[:2]):
        fo.append(f'        <text x="24" y="{y + 39 + j * 14}" font-size="11">{escape(l)}</text>')
    fo.append(f'        <rect class="bx" x="370" y="{y}" width="250" height="62"/>')
    fo.append(f'        <text class="mono mu" x="384" y="{y + 20}" font-size="10">MEDE</text>')
    for j, l in enumerate(textwrap.wrap(c, 38)[:2]):
        fo.append(f'        <text x="384" y="{y + 39 + j * 14}" font-size="11">{escape(l)}</text>')
    fo.append(f'        <line class="ln" x1="342" y1="{y + 31}" x2="366" y2="{y + 31}" marker-end="url(#a1)"/>')
    fo.append(f'        <path class="ln" d="M622 {y + 31} H648 V125 H676" marker-end="url(#a1)"/>' if k == 1 else f'        <path class="ln" d="M622 {y + 31} H648 V125"/>')
fo.append('        <rect class="bx-ink" x="680" y="80" width="210" height="90"/>')
fo.append('        <text class="mono t-ground" x="694" y="104" font-size="10">PERCEPÇÃO</text>')
fo.append('        <text class="b t-ground" x="694" y="128" font-size="13">Analisada e decidida</text>')
fo.append('        <text class="t-ground" x="694" y="152" font-size="11">Reunião, ação e devolutiva.</text>')
fo.append('        <text x="450" y="258" font-size="11.5" text-anchor="middle">Uma fonte só engana. Quando as três apontam para o mesmo lugar, a decisão é segura.</text>')
fo.append("      </svg>")

# ------------------------------------------------------------------ figura 2: ciclo
CI = [("Ouvir", "Pesquisa, reclamações e comportamento, registrados."), ("Medir", "Indicadores com meta: nota, satisfeitos, indicação, reclamações."),
      ("Agir", "Motivo principal escolhido, ação com responsável e prazo."), ("Devolver", "O cliente sabe o que mudou. A pesquisa seguinte confere.")]
W, G = 200, 20
ci = ['      <svg viewBox="0 0 900 214" role="img" aria-label="O ciclo de ouvir, medir, agir e devolver. ' + " ".join(f"{n}: {d}" for n, d in CI) + ' Da devolutiva, o ciclo recomeça.">',
      '        <defs><marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah" d="M0 0 L10 5 L0 10 z"/></marker>'
      '<marker id="a2m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah-mu" d="M0 0 L10 5 L0 10 z"/></marker></defs>']
for k, (nome, desc) in enumerate(CI):
    x = 10 + k * (W + G)
    cls = ["bx-p", "bx-d", "bx-c", "bx-ink"][k]
    tg = ' class="t-ground"' if k == 3 else ""
    ci.append(f'        <rect class="{cls}" x="{x}" y="20" width="{W}" height="120"/>')
    ci.append(f'        <text class="mono {"t-ground" if k == 3 else "mu"}" x="{x + 14}" y="42" font-size="10">{k + 1}{" · O" if k == 0 else " · M" if k == 1 else " · A" if k == 2 else ""}</text>')
    ci.append(f'        <text class="b{" t-ground" if k == 3 else ""}" x="{x + 14}" y="66" font-size="13">{escape(nome)}</text>')
    for j, l in enumerate(textwrap.wrap(desc, 30)[:3]):
        ci.append(f'        <text{tg} x="{x + 14}" y="{90 + j * 15}" font-size="11">{escape(l)}</text>')
    if k < 3:
        ci.append(f'        <line class="ln" x1="{x + W + 1}" y1="80" x2="{x + W + G - 2}" y2="80" marker-end="url(#a2)"/>')
ci.append(f'        <path class="ln-mu dash" d="M{10 + 3 * (W + G) + W / 2} 142 V172 H{10 + W / 2} V146" marker-end="url(#a2m)"/>')
ci.append('        <text class="mu" x="450" y="166" font-size="11" text-anchor="middle">a pesquisa seguinte mostra se a ação chegou ao cliente</text>')
ci.append('        <text x="450" y="204" font-size="11.5" text-anchor="middle">Devolver é a etapa que separa medir a satisfação de gerir a satisfação.</text>')
ci.append("      </svg>")

# ------------------------------------------------------------------ figura 3: a pesquisa da pizzaria
pq = ['      <svg viewBox="0 0 900 300" role="img" aria-label="A pesquisa da pizzaria, como aparece no celular. Três perguntas com escala de 1 a 5: como foi a entrega, como estava a pizza, como foi o atendimento. '
      'Uma pergunta de indicação, de 0 a 10: você indicaria a pizzaria a um amigo? Um campo aberto: o que podemos melhorar? E o botão enviar.">',
      '        <rect class="bx" x="260" y="10" width="380" height="280"/>',
      '        <rect class="hd-ink" x="260" y="10" width="380" height="40"/>',
      '        <text class="b t-ground" x="278" y="35" font-size="13">Como foi o seu pedido? Leva menos de um minuto.</text>']
for k, (cod, perg, _) in enumerate(EX1["perguntas"]):
    y = 66 + k * 50
    pq.append(f'        <text class="b" x="278" y="{y}" font-size="12">{escape(perg)}</text>')
    for j in range(5):
        x = 278 + j * 34
        pq.append(f'        <rect class="{"hd-ink" if (k, j) == (1, 4) or (k, j) == (0, 3) or (k, j) == (2, 4) else "band"}" x="{x}" y="{y + 8}" width="28" height="22"/>')
        pq.append(f'        <text class="{"t-ground" if (k, j) in ((1, 4), (0, 3), (2, 4)) else "mu"} b" x="{x + 14}" y="{y + 23}" font-size="11" text-anchor="middle">{j + 1}</text>')
    pq.append(f'        <text class="mu" x="460" y="{y + 23}" font-size="10">1 muito insatisfeito · 5 muito satisfeito</text>')
y = 216
pq.append(f'        <text class="b" x="278" y="{y}" font-size="12">Você indicaria a pizzaria a um amigo?</text>')
for j in range(11):
    x = 278 + j * 31
    pq.append(f'        <rect class="{"hd-ink" if j == 9 else "band"}" x="{x}" y="{y + 8}" width="26" height="20"/>')
    pq.append(f'        <text class="{"t-ground" if j == 9 else "mu"} b" x="{x + 13}" y="{y + 22}" font-size="10" text-anchor="middle">{j}</text>')
pq.append('        <rect class="band" x="278" y="254" width="240" height="24"/><text class="mu" x="286" y="270" font-size="10.5">O que podemos melhorar?</text>')
pq.append('        <rect class="hd-ink" x="530" y="254" width="90" height="24"/><text class="b t-ground" x="575" y="270" font-size="11" text-anchor="middle">Enviar</text>')
pq.append('        <text class="mu" x="20" y="80" font-size="11">Uma pergunta por</text><text class="mu" x="20" y="95" font-size="11">coisa valorizada:</text>')
pq.append('        <text class="mu" x="20" y="110" font-size="11">entrega, pizza,</text><text class="mu" x="20" y="125" font-size="11">atendimento.</text>')
pq.append('        <text class="mu" x="20" y="225" font-size="11">A indicação resume</text><text class="mu" x="20" y="240" font-size="11">a relação em um</text><text class="mu" x="20" y="255" font-size="11">número comparável.</text>')
pq.append('        <text class="mu" x="660" y="80" font-size="11">Uma escala só,</text><text class="mu" x="660" y="95" font-size="11">com os extremos</text><text class="mu" x="660" y="110" font-size="11">escritos.</text>')
pq.append('        <text class="mu" x="660" y="262" font-size="11">O campo aberto é</text><text class="mu" x="660" y="277" font-size="11">onde os motivos</text><text class="mu" x="660" y="292" font-size="11">aparecem.</text>')
pq.append("      </svg>")

# ------------------------------------------------------------------ figura 4: o caminho da reclamação
W6, G6 = 138, 12
rc = ['      <svg viewBox="0 0 900 190" role="img" aria-label="O caminho de uma reclamação, em seis etapas. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS) + '">',
      '        <defs><marker id="a4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah" d="M0 0 L10 5 L0 10 z"/></marker></defs>']
for k, (nome, desc) in enumerate(ETAPAS):
    x = 6 + k * (W6 + G6)
    ink = k in (2, 5)
    rc.append(f'        <rect class="{"bx-ink" if ink else "bx"}" x="{x}" y="20" width="{W6}" height="136"/>')
    rc.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="40" font-size="10">{k + 1}</text>')
    rc.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="62" font-size="12.5">{escape(nome)}</text>')
    for j, l in enumerate(textwrap.wrap(desc, 22)[:5]):
        rc.append(f'        <text{" class=" + chr(34) + "t-ground" + chr(34) if ink else ""} x="{x + 12}" y="{84 + j * 14}" font-size="10.5">{escape(l)}</text>')
    if k < 5:
        rc.append(f'        <line class="ln" x1="{x + W6 + 1}" y1="88" x2="{x + W6 + G6 - 2}" y2="88" marker-end="url(#a4)"/>')
rc.append(f'        <text x="450" y="180" font-size="11.5" text-anchor="middle">Os prazos deste material: primeira resposta em {PRAZO_RESPOSTA} dias úteis, solução em {PRAZO_SOLUCAO} dias. A organização define os seus e os mede.</text>')
rc.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Data e período</dt><dd>{dt(h["data"])}. {escape(h["periodo"])}</dd></div>',
                      f'    <div><dt>Pesquisa</dt><dd>{escape(h["canal"])}</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      '  </dl>'])


M1 = [resumo_mes(m) for m in EX1["meses"]]
o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Resultado por mês · escala de 1 a 5</caption>',
     '      <thead><tr><th>Mês</th><th class="c">Pedidos</th><th class="c">Respostas</th><th class="c">Taxa</th>'
     + "".join(f'<th class="c">{cod}<small>{escape(p)}</small></th>' for cod, p, _ in EX1["perguntas"])
     + '<th class="c">Média</th><th class="c">Indicação</th><th class="c">Reclamações</th><th class="c">Por 100 pedidos</th></tr></thead>', '      <tbody>']
for r in M1:
    o.append(f'        <tr><td><strong>{r["rot"]}</strong></td><td class="c">{r["pedidos"]}</td><td class="c">{r["respostas"]}</td><td class="c">{round(100 * r["taxa"])}%</td>'
             + "".join(f'<td class="c{" lo" if v < EX1["metas"]["media"] else ""}">{br(v)}</td>' for v in r["medias"])
             + f'<td class="c"><strong>{br(r["media"], 2)}</strong></td><td class="c">{r["nps"]}</td><td class="c">{r["reclamacoes"]}</td><td class="c">{br(r["por100"])}</td></tr>')
mt = EX1["metas"]
o.append(f'        <tr class="tot"><td>Meta</td><td class="c">—</td><td class="c">—</td><td class="c">—</td><td class="c" colspan="3">{br(mt["media"])} em cada pergunta</td>'
         f'<td class="c">{br(mt["media"])}</td><td class="c">{mt["nps"]}</td><td class="c">—</td><td class="c">{br(mt["reclamacoes"])}</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>', '  <p><small>Célula em vermelho-claro: nota abaixo da meta.</small></p>']
ex1meses = "\n".join(o)


def motivos_tab(mot, titulo, base):
    tot = sum(v for _, v in mot)
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{escape(titulo)}</caption>',
         f'      <thead><tr><th style="width:44%">Motivo</th><th class="c">{escape(base)}</th><th class="c">Percentual</th><th class="c">Acumulado</th></tr></thead>', '      <tbody>']
    acc = 0
    for m, v in mot:
        acc += v
        o.append(f'        <tr><td><strong>{escape(m)}</strong></td><td class="c">{v}</td><td class="c">{round(100 * v / tot)}%</td><td class="c">{round(100 * acc / tot)}%</td></tr>')
    o.append(f'        <tr class="tot"><td>Total</td><td class="c">{tot}</td><td class="c">100%</td><td class="c"></td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def recl_tab(ex):
    o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Reclamações registradas · amostra do período</caption>',
         '      <thead><tr><th class="c">Data</th><th style="width:9%">Pedido</th><th style="width:9%">Canal</th><th style="width:15%">Motivo</th><th>Descrição</th>'
         '<th class="c">Respondida</th><th class="c">Resolvida</th><th style="width:9%">Registro</th><th>Situação</th></tr></thead>', '      <tbody>']
    for d, ped, canal, motivo, desc, resp, res, rnc, sit in ex["reclamacoes"]:
        prazo = (resp - d).days
        cls = "s1" if sit == "Resolvida" else "s2"
        o.append(f'        <tr><td class="nw">{dt(d)}</td><td>{escape(ped)}</td><td>{escape(canal)}</td><td>{escape(motivo)}</td><td>{escape(desc)}</td>'
                 f'<td class="c">{dt(resp)}<small>{"no mesmo dia" if prazo == 0 else str(prazo) + (" dia" if prazo == 1 else " dias")}</small></td><td class="c">{dt(res)}</td><td>{escape(rnc) or "—"}</td><td><span class="chip {cls}">{sit}</span></td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


S2 = EX2["segmentos"]
n2 = sum(s[2] for s in S2)
geral = [sum(s[3][k] * s[2] for s in S2) / n2 for k in range(5)]
o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Resultado por segmento · escala de 0 a 10</caption>',
     '      <thead><tr><th>Segmento</th><th class="c">Clientes</th><th class="c">Respostas</th>'
     + "".join(f'<th class="c">{cod}<small>{escape(p)}</small></th>' for cod, p, _ in EX2["perguntas"])
     + '<th class="c">Média</th><th class="c" title="Promotores">Prom.</th><th class="c" title="Detratores">Detr.</th><th class="c">Indicação</th></tr></thead>', '      <tbody>']
for rot, cli, resp, medias, prom, neu, det in S2:
    o.append(f'        <tr><td><strong>{rot}</strong></td><td class="c">{cli}</td><td class="c">{resp}</td>'
             + "".join(f'<td class="c{" lo" if v < EX2["metas"]["media"] else ""}">{br(v)}</td>' for v in medias)
             + f'<td class="c"><strong>{br(sum(medias) / 5, 2)}</strong></td><td class="c">{prom}</td><td class="c">{det}</td><td class="c">{nps(prom, neu, det)}</td></tr>')
P, N, Dt = (sum(s[i] for s in S2) for i in (4, 5, 6))
o.append(f'        <tr class="tot"><td>Todos</td><td class="c">{sum(s[1] for s in S2)}</td><td class="c">{n2}</td>' + "".join(f'<td class="c">{br(g)}</td>' for g in geral)
         + f'<td class="c">{br(sum(geral) / 5, 2)}</td><td class="c">{P}</td><td class="c">{Dt}</td><td class="c">{nps(P, N, Dt)}</td></tr>')
o.append(f'        <tr class="tot"><td>Meta</td><td class="c">—</td><td class="c">—</td><td class="c" colspan="5">{br(EX2["metas"]["media"])} em cada dimensão</td>'
         f'<td class="c">{br(EX2["metas"]["media"])}</td><td class="c">—</td><td class="c">—</td><td class="c">{EX2["metas"]["nps"]}</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>', '  <p><small>Célula em vermelho-claro: nota abaixo da meta.</small></p>']
ex2seg = "\n".join(o)
cx = EX2["cliente_x"]
ex2mot = motivos_tab(EX2["motivos"], f'Reclamações de 2026 por motivo · {cx["reclamacoes"]} das {cx["total"]} são do {cx["nome"].lower()}', "Reclamações")

R = RECLAMACAO
ex3head = "\n".join(['  <dl class="ficha">',
                     f'    <div><dt>Cliente e data</dt><dd>{escape(R["cliente"])}. {dt(R["data"])}</dd></div>',
                     f'    <div><dt>Motivo</dt><dd>{escape(R["motivo"])}</dd></div>',
                     f'    <div><dt>Descrição</dt><dd>{escape(R["descricao"])}</dd></div>',
                     '  </dl>'])
o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Linha do tempo da reclamação</caption>',
     '      <thead><tr><th class="c">Data</th><th style="width:14%">Etapa</th><th>O que aconteceu</th></tr></thead>', '      <tbody>']
for d, etapa, texto in R["linha"]:
    o.append(f'        <tr><td class="nw">{dt(d)}</td><td><strong>{escape(etapa)}</strong></td><td>{escape(texto)}</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>']
ex3linha = "\n".join(o)

# ------------------------------------------------------------------ módulo 7: indicação por mês
ROT = ["Promotores", "Neutros", "Detratores"]
X0, U, TOP, RH, BH = 200, 5.0, 58, 44, 24
bottom = TOP + RH * len(M1)
HH = bottom + 46
vmax = max(r["respostas"] for r in M1)
ch = [f'      <svg id="bars" viewBox="0 0 900 {HH}" role="img" aria-label="Gráfico de barras empilhadas com as respostas à pergunta de indicação da pizzaria, por mês. '
      + " ".join(f'{r["rot"]}: {r["prom"]} promotores, {r["neu"]} neutros e {r["det"]} detratores, indicação {r["nps"]}.' for r in M1) + '">', '        <g font-size="11.5">']
xs = X0
for k, t in enumerate(ROT):
    ch.append(f'          <rect class="f{k + 1}" x="{xs}" y="12" width="14" height="14"/><text x="{xs + 22}" y="24">{t}</text>')
    xs += 40 + len(t) * 6.6
ch.append('        </g>')
for v in range(0, vmax + 20, 20):
    x = X0 + v * U
    ch.append(f'        <line class="grid" x1="{x}" y1="{TOP - 8}" x2="{x}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{x}" y="{bottom + 16}" font-size="11" text-anchor="middle" style="font-variant-numeric:tabular-nums">{v}</text>')
ch.append(f'        <text class="mono mu" x="{X0 + (vmax + 10) * U / 2}" y="{bottom + 36}" font-size="10" text-anchor="middle">RESPOSTAS</text>')
for k, r in enumerate(M1):
    y = TOP + RH * k + (RH - BH) / 2
    ch.append(f'        <text x="20" y="{y + 16:.1f}" font-size="12"><tspan class="b">{r["rot"]}</tspan><tspan class="mu"> · {r["respostas"]} respostas</tspan></text>')
    x = X0
    for j, v in enumerate((r["prom"], r["neu"], r["det"])):
        ch.append(f'        <rect class="seg f{j + 1}" data-k="{k}" x="{x}" y="{y:.1f}" width="{v * U}" height="{BH}"/>')
        ch.append(f'        <text class="b {"on2" if j == 1 else "on"}" x="{x + v * U / 2}" y="{y + 16.5:.1f}" font-size="12" text-anchor="middle" pointer-events="none">{v}</text>')
        x += v * U
    ch.append(f'        <text class="halo" x="{x + 10}" y="{y + 16:.1f}" font-size="11.5"><tspan class="b">{r["nps"]}</tspan><tspan class="mu"> de indicação</tspan></text>')
for k, r in enumerate(M1):
    ch.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" '
              f'aria-label="{r["rot"]}: {r["respostas"]} respostas, {r["prom"]} promotores, {r["neu"]} neutros e {r["det"]} detratores, indicação {r["nps"]}" data-k="{k}" data-r="{r["rot"]}" '
              f'data-t="{r["respostas"]}" data-ped="{r["pedidos"]}" data-a="{r["prom"]}" data-b="{r["neu"]}" data-c="{r["det"]}" data-nps="{r["nps"]}" data-cx="{X0 + r["respostas"] * U / 2:.1f}"/>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>Mês</th><th class="c">Respostas</th>' + "".join(f'<th class="c">{t}</th>' for t in ROT) + '<th class="c">Indicação</th></tr></thead>',
      '          <tbody>']
for r in M1:
    tb.append(f'            <tr><td><strong>{r["rot"]}</strong></td><td class="c">{r["respostas"]}</td><td class="c">{r["prom"]}</td><td class="c">{r["neu"]}</td><td class="c">{r["det"]}</td><td class="c">{r["nps"]}</td></tr>')
tb += ['          </tbody>', '        </table>']
charttext = (f'  <p>A indicação subiu de {M1[0]["nps"]} para {M1[-1]["nps"]} em três meses, e a composição diz como: os detratores caíram de {M1[0]["det"]} para {M1[-1]["det"]}, e os promotores '
             f'subiram de {M1[0]["prom"]} para {M1[-1]["prom"]}, com {M1[0]["respostas"]} e {M1[-1]["respostas"]} respostas. É a leitura que confirma as reclamações: o motivo “entrega atrasada” caiu junto. '
             f'A taxa de resposta ficou entre {round(100 * min(r["taxa"] for r in M1))}% e {round(100 * max(r["taxa"] for r in M1))}% dos pedidos, medida do mesmo jeito nos três meses, e é isso que permite comparar.</p>')

# ------------------------------------------------------------------ módulo 10: figura da ISO
PARTES = [("9.1.2 · Monitorar a percepção", "Como o cliente percebe o atendimento das suas necessidades e expectativas.", "As três famílias de fontes"),
          ("9.1.2 · Definir os métodos", "Como a informação é obtida, monitorada e analisada.", "Pesquisa, registro de reclamações e painel"),
          ("8.2.1 · Comunicar-se com o cliente", "Canal para o retorno do cliente e para as reclamações.", "O caminho da reclamação, com prazos"),
          ("9.3 · Levar à direção", "A satisfação é entrada da análise crítica.", "Entrada “c1”, com resultado e motivos")]
iso = ['      <svg viewBox="0 0 900 190" role="img" aria-label="O que a norma pede sobre satisfação do cliente. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in PARTES) + '">']
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
for tag, val in (("<!--FONTESFIG-->", "\n".join(fo)), ("<!--CICLO-->", "\n".join(ci)), ("<!--PESQFIG-->", "\n".join(pq)), ("<!--RECLFIG-->", "\n".join(rc)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1MESES-->", ex1meses), ("<!--EX1MOTIVOS-->", motivos_tab(EX1["motivos"], "Motivos das notas 1 e 2 e das reclamações · fevereiro a abril", "Ocorrências")),
                 ("<!--EX1RECL-->", recl_tab(EX1)), ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2SEG-->", ex2seg), ("<!--EX2MOTIVOS-->", ex2mot),
                 ("<!--EX3HEAD-->", ex3head), ("<!--EX3LINHA-->", ex3linha), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)),
                 ("<!--CHARTTEXT-->", charttext), ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Satisfação do cliente</title>")
assert "Satisfação do cliente" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| respostas:", sum(r["respostas"] for r in M1),
      "| indústria média", br(sum(geral) / 5, 2), "NPS", nps(P, N, Dt))
