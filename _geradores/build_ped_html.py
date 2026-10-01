# -*- coding: utf-8 -*-
"""Monta treinamento-pedidos.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ped_data import (ACEITO, ALTERADO, CHECK, EMANALISE, ETAPAS, EX1, EX2, FONTES, FONTES_C, L_INC, L_OK, L_PEND, NA, NAO, NQ, PERGUNTAS, RECUSADO, SIM,  # noqa: E402
                      conf, leitura, mud_conf, nao_por_pergunta, oferta_conf, pendencias, resumo)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# aceito, alterado e recusado: a mesma paleta de três cores do estudo de Satisfação, validada para daltonismo nos dois modos
LIGHT = ("\n  --s1:#2A6FB0; --s1-tint:#DCE8F3;\n  --s2:#D19A2E; --s2-tint:#F8EBCB;\n  --s3:#B0413E; --s3-tint:#F5DEDC;\n  --on-s2:#16242E;")
DARK = ("\n  --s1:#4F97DB; --s1-tint:#1B2F42;\n  --s2:#B58E14; --s2-tint:#3A2C12;\n  --s3:#D14B45; --s3-tint:#3D1F1E;\n  --on-s2:#0F171C;")
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Decisões */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.s1{background:var(--s1)} .chip.s2{background:var(--s2);color:var(--on-s2)} .chip.s3{background:var(--s3)}
.chip.sl{background:var(--sunk);color:var(--ink);box-shadow:inset 0 0 0 1px var(--rule)}
svg .hd-ink{fill:var(--ink)}
svg .f1{fill:var(--s1)} svg .f2{fill:var(--s2)} svg .f3{fill:var(--s3)}
svg .bx-s1{fill:var(--s1-tint);stroke:var(--s1);stroke-width:1.5} svg .bx-s2{fill:var(--s2-tint);stroke:var(--s2);stroke-width:1.5} svg .bx-s3{fill:var(--s3-tint);stroke:var(--s3);stroke-width:1.5}
svg .halo{paint-order:stroke;stroke:var(--surface);stroke-width:5px;stroke-linejoin:round}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas dos exemplos */
table.aud{font-size:.8rem;min-width:980px;line-height:1.4}
table.aud th, table.aud td{padding:8px 9px}
table.aud td.n{white-space:nowrap;font-weight:600;color:var(--muted)}
table.aud td.c, table.aud th.c{text-align:center;font-variant-numeric:tabular-nums}
table.aud td.qa, table.aud th.qa{text-align:center;padding:8px 3px;width:26px;font-weight:600}
table.aud td.no{background:var(--s3-tint)}
table.aud td small, table.aud th small{display:block;color:var(--muted);font-size:.76rem;margin-top:3px;font-weight:400}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha do registro (acima de cada exemplo) */"""
assert css.count("\n.ficha{") == 1
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

TNUM = ' style="font-variant-numeric:tabular-nums"'


def dt(d, ano=True):
    return d.strftime("%d/%m/%Y" if ano else "%d/%m") if d else "—"


def marker(i, mu=False):
    return (f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path class="{"ah-mu" if mu else "ah"}" d="M0 0 L10 5 L0 10 z"/></marker>')


def lines(o, txt, x, y, wrap, fs=10.5, cls="", step=13, maxl=3, anchor=None):
    """Texto quebrado em linhas; devolve o y da linha seguinte."""
    ls = textwrap.wrap(txt, wrap)[:maxl]
    attr = (f' class="{cls}"' if cls else "") + (f' text-anchor="{anchor}"' if anchor else "")
    for j, l in enumerate(ls):
        o.append(f'        <text{attr} x="{x}" y="{y + j * step}" font-size="{fs}">{escape(l)}</text>')
    return y + step * len(ls)


def box(o, cls, x, y, w, h, tit, sub, ink=False, fs=12):
    o.append(f'        <rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>')
    o.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{y + 24}" font-size="{fs}">{escape(tit)}</text>')
    if sub:
        lines(o, sub, x + 12, y + 41, int(w / 5.6), fs=10.5, cls="t-ground" if ink else "mu", maxl=1)


# ------------------------------------------------------------------ figura 1: do pedido à confirmação
fl = ['      <svg viewBox="0 0 900 262" role="img" aria-label="O caminho do pedido. A organização define a oferta, recebe o pedido pelos canais definidos e analisa antes de aceitar. '
      'Depois decide: aceitar, negociar uma alteração com o cliente ou recusar com o motivo. O pedido aceito é confirmado com o cliente e segue para a produção e a entrega. '
      'Quando o pedido muda, a mudança volta para a análise.">',
      "        <defs>" + marker("a1") + marker("a1m", True) + "</defs>"]
box(fl, "bx", 20, 30, 170, 56, "Definir a oferta", "8.2.2 · o que se oferece")
box(fl, "bx", 230, 30, 170, 56, "Receber o pedido", "8.2.1 · pelos canais")
box(fl, "bx-ink", 440, 30, 190, 56, "Analisar antes de aceitar", "8.2.3 · as sete perguntas", ink=True)
box(fl, "bx-s2", 670, 30, 210, 56, "Decidir", "aceitar, alterar ou recusar")
box(fl, "bx-s2", 20, 160, 170, 56, "Mudança no pedido", "8.2.4 · analisar de novo")
box(fl, "bx", 230, 160, 170, 56, "Produzir e entregar", "o plano de controle")
box(fl, "bx-s1", 440, 160, 190, 56, "Confirmar com o cliente", "o que foi aceito")
box(fl, "bx-s3", 670, 160, 210, 56, "Recusar", "com o motivo, ao cliente")
fl += ['        <line class="ln" x1="191" y1="58" x2="228" y2="58" marker-end="url(#a1)"/>',
       '        <line class="ln" x1="401" y1="58" x2="438" y2="58" marker-end="url(#a1)"/>',
       '        <line class="ln" x1="631" y1="58" x2="668" y2="58" marker-end="url(#a1)"/>',
       '        <line class="ln" x1="775" y1="87" x2="775" y2="158" marker-end="url(#a1)"/>',
       '        <text class="mu halo" x="783" y="130" font-size="10.5">recusar</text>',
       '        <path class="ln" d="M700 87 V122 H560 V158" marker-end="url(#a1)"/>',
       '        <text class="mu halo" x="630" y="116" font-size="10.5" text-anchor="middle">aceitar</text>',
       '        <path class="ln-mu dash" d="M775 29 V14 H315 V28" marker-end="url(#a1m)"/>',
       '        <text class="mu halo" x="545" y="18" font-size="10.5" text-anchor="middle">alterar: a proposta volta ao cliente, que decide</text>',
       '        <line class="ln" x1="439" y1="188" x2="402" y2="188" marker-end="url(#a1)"/>',
       '        <line class="ln-mu dash" x1="229" y1="188" x2="192" y2="188" marker-end="url(#a1m)"/>',
       '        <path class="ln-mu dash" d="M105 159 V130 H500 V88" marker-end="url(#a1m)"/>',
       '        <text class="mu halo" x="300" y="126" font-size="10.5" text-anchor="middle">o pedido mudou: analisar de novo</text>',
       '        <text x="450" y="250" font-size="11.5" text-anchor="middle">A análise vem antes do compromisso. Depois de aceito, o pedido só muda passando de novo por ela.</text>',
       "      </svg>"]

# ------------------------------------------------------------------ figura 2: as cinco etapas
W5, G5 = 164, 14
et = ['      <svg viewBox="0 0 900 206" role="img" aria-label="As cinco etapas do trabalho. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS) + ' A mudança devolve o pedido à análise.">',
      "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
for k, (nome, desc) in enumerate(ETAPAS):
    x = 12 + k * (W5 + G5)
    ink = k == 2
    et.append(f'        <rect class="{["bx", "bx", "bx-ink", "bx-s1", "bx-s2"][k]}" x="{x}" y="16" width="{W5}" height="124"/>')
    et.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="36" font-size="10">ETAPA {k + 1}</text>')
    et.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="58" font-size="12.5">{escape(nome)}</text>')
    lines(et, desc, x + 12, 80, 26, cls="t-ground" if ink else "", step=14.5, maxl=4)
    if k < 4:
        et.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="78" x2="{x + W5 + G5 - 2}" y2="78" marker-end="url(#a2)"/>')
xa, xb = 12 + 4 * (W5 + G5) + W5 / 2, 12 + 2 * (W5 + G5) + W5 / 2
et.append(f'        <path class="ln-mu dash" d="M{xa} 142 V170 H{xb} V146" marker-end="url(#a2m)"/>')
et.append(f'        <text class="mu halo" x="{(xa + xb) / 2}" y="174" font-size="11" text-anchor="middle">o pedido que muda volta à análise</text>')
et.append('        <text x="450" y="198" font-size="11.5" text-anchor="middle">A etapa escura é o centro do requisito: nenhum compromisso antes da análise.</text>')
et.append("      </svg>")

# ------------------------------------------------------------------ figura 3: as quatro fontes de requisitos
FCLS = ["hd-p", "hd-d", "hd-c", "hd-ink"]
fo = ['      <svg viewBox="0 0 900 214" role="img" aria-label="As quatro fontes de requisitos de um pedido, com exemplos da pizzaria. ' + " ".join(f"{a}: {b} Exemplo: {c}" for a, b, c in FONTES) + '">']
for k, (tit, oque, exemplo) in enumerate(FONTES):
    x = 10 + k * 222
    fo.append(f'        <rect class="bx" x="{x}" y="10" width="214" height="194"/>')
    fo.append(f'        <rect class="{FCLS[k]}" x="{x}" y="10" width="214" height="40"/>')
    ls = textwrap.wrap(tit, 28)
    for j, l in enumerate(ls):
        fo.append(f'        <text class="b {"t-ground" if k == 3 else "on"}" x="{x + 12}" y="{(35 if len(ls) == 1 else 27) + j * 15}" font-size="12">{escape(l)}</text>')
    yy = lines(fo, oque, x + 12, 72, 32, fs=11, step=15, maxl=3)
    fo.append(f'        <text class="mono mu" x="{x + 12}" y="{yy + 10}" font-size="9.5">NA PIZZARIA</text>')
    lines(fo, exemplo, x + 12, yy + 26, 34, fs=10.5, cls="mu", step=14, maxl=5)
fo.append("      </svg>")

# ------------------------------------------------------------------ figura 4: as sete perguntas no pedido E-32
p32 = [p for p in EX1["peds"] if p["num"] == "E-32"][0]
NOTA32 = {1: "Sábado às 21h é o pico, e o forno é único.", 4: "Cerveja pedida para uma turma com menores de idade."}
an = [f'      <svg viewBox="0 0 900 {112 + NQ * 34}" role="img" aria-label="As sete perguntas aplicadas à encomenda E-32 da pizzaria: {escape(p32["pede"])} '
      + " ".join(f"{t}: {a}." for (t, _), a in zip(PERGUNTAS, p32["q"])) + f' Decisão: {p32["dec"]}. {escape(p32["neg"])}">',
      '        <rect class="bx" x="10" y="10" width="880" height="' + str(94 + NQ * 34) + '"/>',
      '        <rect class="hd-ink" x="10" y="10" width="880" height="34"/>',
      f'        <text class="b t-ground" x="24" y="32" font-size="12.5">E-32 · {escape(p32["pede"])}</text>']
for k, ((tit, perg), ans) in enumerate(zip(PERGUNTAS, p32["q"])):
    y = 52 + k * 34
    an.append(f'        <line class="grid" x1="10" y1="{y + 32}" x2="890" y2="{y + 32}"/>')
    an.append(f'        <text class="mono mu" x="24" y="{y + 20}" font-size="10">{k + 1}</text>')
    an.append(f'        <text class="b" x="44" y="{y + 20}" font-size="11.5">{escape(tit)}</text>')
    an.append(f'        <text x="196" y="{y + 20}" font-size="11">{escape(perg)}</text>')
    cls = "f3" if ans == NAO else "f1"
    an.append(f'        <rect class="{cls}" x="760" y="{y + 7}" width="44" height="20"/><text class="b on" x="782" y="{y + 21}" font-size="11" text-anchor="middle">{ans}</text>')
    if k in NOTA32:
        an.append(f'        <text class="mu" x="812" y="{y + 15}" font-size="9.5">ver</text><text class="mu" x="812" y="{y + 27}" font-size="9.5">abaixo</text>')
yb = 52 + NQ * 34
an.append(f'        <text class="mono mu" x="24" y="{yb + 18}" font-size="9.5">O QUE A ANÁLISE ENCONTROU</text>')
an.append(f'        <text x="196" y="{yb + 18}" font-size="11">{escape(" ".join(NOTA32[k] for k in sorted(NOTA32)))}</text>')
an.append(f'        <text class="mono mu" x="24" y="{yb + 36}" font-size="9.5">DECISÃO</text>')
an.append(f'        <text class="b" x="196" y="{yb + 36}" font-size="11">{escape(p32["dec"])}: {escape(p32["neg"])}</text>')
an.append("      </svg>")

pergtab = ['  <div class="tbl">', '    <table>', '      <thead><tr><th style="width:4%">#</th><th style="width:20%">Pergunta</th><th style="width:44%">O que confere</th><th>Quem costuma responder</th></tr></thead>', '      <tbody>']
QUEM = ["Engenharia, ou quem conhece o produto.", "Programação da produção, ou o gerente.", "Expedição e atendimento.", "Engenharia e Qualidade, conversando com o cliente.",
        "Qualidade, ou quem acompanha a legislação.", "Comercial, comparando com a proposta.", "Comercial e financeiro."]
for k, ((tit, perg), quem) in enumerate(zip(PERGUNTAS, QUEM), 1):
    pergtab.append(f'        <tr><td class="num">{k}</td><td><strong>{escape(tit)}</strong></td><td>{escape(perg)}</td><td>{escape(quem)}</td></tr>')
pergtab += ['      </tbody>', '    </table>', '  </div>']


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Processo</dt><dd>{escape(h["processo"])}</dd></div>',
                      f'    <div><dt>Quem analisa</dt><dd>{escape(h["analisa"])}</dd></div>',
                      f'    <div><dt>Registros</dt><dd>{escape(h["periodo"])}, lidos em {dt(h["ref"])}.</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      '  </dl>'])


def tabela(caption, heads, rows):
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{caption}</caption>', f'      <thead><tr>{"".join(heads)}</tr></thead>', '      <tbody>']
    o += [f'        <tr>{r}</tr>' for r in rows]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def conf_chip(c):
    return f'<span class="chip {"s1" if c == "OK" else "s3"}">{escape(c)}</span>'


DEC_CLS = {ACEITO: "s1", ALTERADO: "s2", RECUSADO: "s3", EMANALISE: "sl"}
LEIT_CLS = {L_OK: "s1", L_PEND: "s2", L_INC: "s3"}


def oferta_tab(ex):
    rows = [f'<td><strong>{escape(o["item"])}</strong></td><td>{escape(o["espec"])}</td><td>{escape(o["legal"])}</td><td>{escape(o["naogar"])}</td><td>{escape(o["onde"])}</td>'
            f'<td class="c{" no" if o["cap"] != SIM else ""}">{o["cap"]}</td><td>{conf_chip(oferta_conf(o))}</td>' for o in ex["ofertas"]]
    return tabela(f'A oferta · {len(ex["ofertas"])} itens', ['<th style="width:13%">Item</th>', '<th style="width:25%">O que se oferece</th>', '<th style="width:18%">Requisitos legais</th>',
                                                             '<th style="width:18%">O que não se garante</th>', '<th>Onde o cliente é informado</th>', '<th class="c">Capacidade confirmada?</th>',
                                                             '<th>Conferência</th>'], rows)


def ped_tab(ex):
    r = resumo(ex)
    rows = []
    for p in ex["peds"]:
        qs = "".join(f'<td class="qa{" no" if a == NAO else ""}">{"S" if a == SIM else "N" if a == NAO else "—"}</td>' for a in p["q"])
        pede = f'<strong>{escape(p["pede"])}</strong>' + (f'<small>{escape(p["naodecl"])}</small>' if p["naodecl"] else "")
        datas = f'{escape(p["quem"])}<small>Análise {dt(p["analise"], False)} · confirmação {dt(p["confirm"], False)}</small>'
        rows.append(f'<td class="n">{p["num"]}<small>{dt(p["data"], False)}</small></td><td>{escape(p["cliente"])}<small>{escape(p["canal"])}</small></td><td>{pede}</td>'
                    f'<td class="c">{dt(p["prazo"], False)}</td>{qs}<td><span class="chip {DEC_CLS[p["dec"]]}">{p["dec"]}</span><small>{escape(p["neg"])}</small></td>'
                    f'<td>{datas}</td><td>{conf_chip(conf(p))}</td>')
    d = r["dec"]
    heads = (['<th style="width:6%">Nº<small>Data</small></th>', '<th style="width:10%">Cliente<small>Canal</small></th>',
              '<th style="width:22%">O que pede<small>Requisitos não declarados e legais identificados</small></th>', '<th class="c">Prazo</th>']
             + [f'<th class="qa" title="{escape(t)}">{k}</th>' for k, (t, _) in enumerate(PERGUNTAS, 1)]
             + ['<th style="width:20%">Decisão<small>O que foi negociado, ou o motivo</small></th>', '<th style="width:12%">Quem analisou<small>Datas</small></th>', '<th>Conferência</th>'])
    pl = lambda n, um, varios: f"{n} {um if n == 1 else varios}"  # noqa: E731
    return tabela(f'Pedidos · {r["peds"]} analisados: {pl(d[ACEITO], "aceito", "aceitos")}, {d[ALTERADO]} com alteração, {pl(d[RECUSADO], "recusado", "recusados")}'
                  + (f', {d[EMANALISE]} em análise' if d[EMANALISE] else "")
                  + f' · {r["rever"]} a rever', heads, rows) + \
        '\n  <p><small>Perguntas: ' + " · ".join(f"{k} {t.lower()}" for k, (t, _) in enumerate(PERGUNTAS, 1)) + '. S: sim. N: não. —: não se aplica.</small></p>'


def mud_tab(ex):
    rows = [f'<td class="c">{dt(m["data"], False)}</td><td class="n">{m["ped"]}</td><td><strong>{escape(m["oque"])}</strong><small>Pedida por: {escape(m["pediu"])}</small></td>'
            f'<td>{escape(m["analise"]) or "—"}</td><td class="c{" no" if m["docs"] != SIM else ""}">{m["docs"]}</td><td>{escape(m["inform"]) or "—"}</td><td>{conf_chip(mud_conf(m))}</td>'
            for m in ex["muds"]]
    return tabela(f'Mudanças nos pedidos aceitos · {len(ex["muds"])}', ['<th class="c">Data</th>', '<th>Pedido</th>', '<th style="width:28%">O que mudou<small>Quem pediu</small></th>',
                                                                        '<th style="width:26%">Análise da mudança</th>', '<th class="c">Documentos atualizados?</th>', '<th>Quem foi informado</th>',
                                                                        '<th>Conferência</th>'], rows)


# ------------------------------------------------------------------ exemplo 3: as quatro fontes de um pedido novo
e3 = ['      <svg viewBox="0 0 900 330" role="img" aria-label="As quatro fontes de requisitos do pedido ' + escape(FONTES_C["ped"]) + ". "
      + " ".join(f"{a}: {b}" for a, b in FONTES_C["fontes"]) + " " + escape(FONTES_C["decisao"]) + '">', "        <defs>" + marker("a5") + "</defs>",
      '        <rect class="bx-ink" x="300" y="112" width="300" height="68"/>',
      '        <text class="mono t-ground" x="314" y="132" font-size="9.5">O PEDIDO</text>']
_ped = FONTES_C["ped"].split(" · ")
e3.append(f'        <text class="b t-ground" x="314" y="151" font-size="12">{escape(" · ".join(_ped[:2]))}</text>')
e3.append(f'        <text class="t-ground" x="314" y="168" font-size="11">{escape(" · ".join(_ped[2:]))}</text>')
POS = [(20, 10), (640, 10), (20, 188), (640, 188)]
for k, ((tit, txt), (x, y)) in enumerate(zip(FONTES_C["fontes"], POS)):
    e3.append(f'        <rect class="bx" x="{x}" y="{y}" width="240" height="94"/>')
    e3.append(f'        <rect class="{FCLS[k]}" x="{x}" y="{y}" width="6" height="94"/>')
    e3.append(f'        <text class="b" x="{x + 16}" y="{y + 20}" font-size="11.5">{escape(tit)}</text>')
    lines(e3, txt, x + 16, y + 38, 38, fs=10.5, step=13.5, maxl=4)
    left = x < 450
    e3.append(f'        <path class="ln" d="M{x + 240 if left else x} {y + 47} H{280 if left else 620} V{130 if y < 100 else 162} H{300 if left else 600}"/>')
e3.append('        <line class="ln" x1="450" y1="181" x2="450" y2="284" marker-end="url(#a5)"/>')
e3.append('        <rect class="bx-s2" x="250" y="286" width="400" height="38"/>')
lines(e3, FONTES_C["decisao"], 262, 301, 72, fs=10.5, maxl=2)
e3.append("      </svg>")

# ------------------------------------------------------------------ módulo 7: onde a análise encontra problema
n1, n2 = nao_por_pergunta(EX1), nao_por_pergunta(EX2)
X0, W, TOP, RH, BH = 210, 520, 48, 40, 14
VMAX = max(max(n1), max(n2), 3)
bottom = TOP + RH * NQ
ch = [f'      <svg id="bars" viewBox="0 0 900 {bottom + 40}" role="img" aria-label="Respostas “não” por pergunta da análise, nos pedidos dos dois exemplos. '
      + " ".join(f'{t}: pizzaria {a}, indústria {b}.' for (t, _), a, b in zip(PERGUNTAS, n1, n2)) + '">', '        <g font-size="11.5">',
      f'          <rect class="f1" x="{X0}" y="12" width="14" height="14"/><text x="{X0 + 22}" y="24">Pizzaria · {len(EX1["peds"])} pedidos</text>',
      f'          <rect class="f2" x="{X0 + 190}" y="12" width="14" height="14"/><text x="{X0 + 212}" y="24">Indústria · {len(EX2["peds"])} pedidos</text>', '        </g>']
for v in range(0, VMAX + 1):
    x = X0 + v * W / VMAX
    ch.append(f'        <line class="grid" x1="{x}" y1="{TOP - 6}" x2="{x}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{x}" y="{bottom + 16}" font-size="11" text-anchor="middle"{TNUM}>{v}</text>')
ch.append(f'        <text class="mono mu" x="{X0 + W / 2}" y="{bottom + 34}" font-size="10" text-anchor="middle">PEDIDOS COM RESPOSTA “NÃO”</text>')
for k, ((t, _), a, b) in enumerate(zip(PERGUNTAS, n1, n2)):
    y = TOP + RH * k + 5
    ch.append(f'        <text x="20" y="{y + 18}" font-size="12"><tspan class="mono mu">{k + 1}</tspan><tspan dx="8">{escape(t)}</tspan></text>')
    for j, (v, cls) in enumerate(((a, "f1"), (b, "f2"))):
        yy = y + j * (BH + 2)
        if v:
            ch.append(f'        <rect class="bar {cls}" data-k="{k}" x="{X0}" y="{yy}" width="{v * W / VMAX:.1f}" height="{BH}"/>')
        ch.append(f'        <text class="mu" x="{X0 + v * W / VMAX + 6:.1f}" y="{yy + 11}" font-size="10.5"{TNUM}>{v}</text>')
for k, ((t, _), a, b) in enumerate(zip(PERGUNTAS, n1, n2)):
    ch.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" aria-label="{escape(t)}: pizzaria {a}, indústria {b}" '
              f'data-k="{k}" data-n="{k + 1} · {escape(t)}" data-a="{a}" data-b="{b}" data-cx="{X0 + W / 2}" data-cy="{TOP + RH * k}"/>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>Pergunta</th><th class="c">Pizzaria</th><th class="c">Indústria</th></tr></thead>', '          <tbody>']
for k, ((t, _), a, b) in enumerate(zip(PERGUNTAS, n1, n2), 1):
    tb.append(f'            <tr><td>{k} · {escape(t)}</td><td class="c">{a}</td><td class="c">{b}</td></tr>')
tb += ['          </tbody>', '        </table>']
charttext = (f'  <p>Na pizzaria, a pergunta que mais encontra problema é a da capacidade: {n1[1]} das {len(EX1["peds"])} encomendas pediam mais do que a loja consegue no horário pedido. '
             f'Duas foram resolvidas na análise, com outro horário ou outro dia. A terceira, a E-34, foi aceita pela atendente sem a análise do gerente, para o mesmo sábado da formatura. '
             f'Na indústria, os problemas se espalham: a especificação que o processo não alcança, o uso que o cliente não contou, a lei, a diferença entre o pedido e a proposta. '
             f'É por isso que a análise da fábrica envolve a Engenharia e a Qualidade, e não só o Comercial. Em nenhum dos dois casos a pergunta do preço pegou alguma coisa: '
             f'é a que todos já fazem sem precisar de lista.</p>')

# ------------------------------------------------------------------ módulo 10: figura da ISO
ISOP = [("8.2.1 · Comunicar", "Informar o cliente sobre o que se oferece, tratar consultas, pedidos, mudanças e reclamações.", "os canais e o que não se garante"),
        ("8.2.2 · Definir", "Definir os requisitos do que se oferece, inclusive os legais, e confirmar que é possível cumprir.", "a aba Oferta"),
        ("8.2.3 · Analisar", "Antes de se comprometer, analisar o pedido: declarados, não declarados, legais, diferenças.", "as sete perguntas e o registro"),
        ("8.2.4 · Mudar", "Quando o pedido muda, atualizar os documentos e informar as pessoas envolvidas.", "a aba Mudanças")]
iso = ['      <svg viewBox="0 0 900 200" role="img" aria-label="O que a norma pede sobre os requisitos do cliente. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in ISOP) + '">']
for k, (a, b, c) in enumerate(ISOP):
    x = 10 + k * 222
    iso.append(f'        <rect class="bx" x="{x}" y="14" width="214" height="172"/>')
    iso.append(f'        <rect class="hd-ink" x="{x}" y="14" width="214" height="34"/>')
    iso.append(f'        <text class="b t-ground" x="{x + 12}" y="36" font-size="11.5">{escape(a)}</text>')
    lines(iso, b, x + 12, 70, 32, fs=11.5, step=16, maxl=5)
    lines(iso, "Neste estudo: " + c, x + 12, 152, 34, fs=11, cls="mu", step=15, maxl=2)
iso.append("      </svg>")

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--CAMINHO-->", "\n".join(fl)), ("<!--FLUXO-->", "\n".join(et)), ("<!--FONTES-->", "\n".join(fo)), ("<!--PERGUNTAS-->", "\n".join(an)), ("<!--PERGTAB-->", "\n".join(pergtab)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1OFERTA-->", oferta_tab(EX1)), ("<!--EX1PED-->", ped_tab(EX1)), ("<!--EX1MUD-->", mud_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2OFERTA-->", oferta_tab(EX2)), ("<!--EX2PED-->", ped_tab(EX2)), ("<!--EX2MUD-->", mud_tab(EX2)),
                 ("<!--EX3FIG-->", "\n".join(e3)), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHARTTEXT-->", charttext),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Requisitos do cliente e análise de pedidos</title>")
assert "Requisitos do cliente" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", resumo(EX1), "| indústria", resumo(EX2))
