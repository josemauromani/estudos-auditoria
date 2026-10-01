# -*- coding: utf-8 -*-
"""Monta treinamento-projeto.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from datetime import date, timedelta
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from proj_data import (APROV, CHECK, CONTROLES, ETAPAS, EX1, EX2, HISTORIA, NAOAT, PENDENTE, REPROV, RESS, TIPOS_INFO, VALID,  # noqa: E402
                       entrada_conf, etapa_conf, mud_conf, resumo)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# no prazo, com atraso e atrasada: a mesma paleta de três cores do estudo de Satisfação, validada para daltonismo nos dois modos
LIGHT = ("\n  --s1:#2A6FB0; --s1-tint:#DCE8F3;\n  --s2:#D19A2E; --s2-tint:#F8EBCB;\n  --s3:#B0413E; --s3-tint:#F5DEDC;\n  --on-s2:#16242E;")
DARK = ("\n  --s1:#4F97DB; --s1-tint:#1B2F42;\n  --s2:#B58E14; --s2-tint:#3A2C12;\n  --s3:#D14B45; --s3-tint:#3D1F1E;\n  --on-s2:#0F171C;")
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Situações */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.s1{background:var(--s1)} .chip.s2{background:var(--s2);color:var(--on-s2)} .chip.s3{background:var(--s3)}
.chip.sl{background:var(--sunk);color:var(--ink);box-shadow:inset 0 0 0 1px var(--rule)}
svg .hd-ink{fill:var(--ink)}
svg .f1{fill:var(--s1)} svg .f2{fill:var(--s2)} svg .f3{fill:var(--s3)} svg .f0{fill:var(--muted)}
svg .o1{fill:var(--surface);stroke:var(--s1);stroke-width:2} svg .o2{fill:var(--surface);stroke:var(--s2);stroke-width:2} svg .o3{fill:var(--surface);stroke:var(--s3);stroke-width:2}
svg .o0{fill:var(--surface);stroke:var(--muted);stroke-width:2}
svg .bx-s1{fill:var(--s1-tint);stroke:var(--s1);stroke-width:1.5} svg .bx-s2{fill:var(--s2-tint);stroke:var(--s2);stroke-width:1.5} svg .bx-s3{fill:var(--s3-tint);stroke:var(--s3);stroke-width:1.5}
svg .lk1{stroke:var(--s1);stroke-width:2} svg .lk2{stroke:var(--s2);stroke-width:2}
svg .halo{paint-order:stroke;stroke:var(--surface);stroke-width:5px;stroke-linejoin:round}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas dos exemplos */
table.aud{font-size:.8rem;min-width:960px;line-height:1.4}
table.aud th, table.aud td{padding:8px 9px}
table.aud td.n{white-space:nowrap;font-weight:600;color:var(--muted)}
table.aud td.c, table.aud th.c{text-align:center;font-variant-numeric:tabular-nums}
table.aud td.no{background:var(--s3-tint)}
table.aud td small, table.aud th small{display:block;color:var(--muted);font-size:.76rem;margin-top:3px;font-weight:400}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha do projeto (acima de cada exemplo) */"""
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
        lines(o, sub, x + 12, y + 41, int(w / 5.6), fs=10.5, cls="t-ground" if ink else "mu", maxl=2, step=13)


# ------------------------------------------------------------------ figura 1: entradas, saídas, verificação e validação
vm = ['      <svg viewBox="0 0 900 300" role="img" aria-label="O projeto em forma de V. À esquerda, de cima para baixo: a necessidade e o uso pretendido viram as entradas do projeto. '
      'Embaixo, o desenvolvimento transforma as entradas em saídas. À direita, de baixo para cima: as saídas viram o produto. A verificação compara as saídas com as entradas. '
      'A validação compara o produto com o uso pretendido. As análises críticas acompanham cada passagem.">',
      "        <defs>" + marker("a1") + marker("a1m", True) + "</defs>"]
box(vm, "bx", 20, 20, 240, 64, "Necessidade e uso pretendido", "Para que o cliente vai usar, e em que condições")
box(vm, "bx", 640, 20, 240, 64, "Produto, no uso real", "O que o cliente recebe e usa")
box(vm, "bx-s2", 110, 128, 220, 64, "Entradas do projeto", "O que o projeto precisa atender")
box(vm, "bx-s2", 570, 128, 220, 64, "Saídas do projeto", "Especificação, receita, critérios")
box(vm, "bx-ink", 340, 214, 220, 56, "Desenvolver", "Transformar as entradas em saídas", ink=True)
vm += ['        <path class="ln" d="M140 85 L180 126" marker-end="url(#a1)"/>',
       '        <path class="ln" d="M240 193 L338 232" marker-end="url(#a1)"/>',
       '        <path class="ln" d="M561 232 L660 194" marker-end="url(#a1)"/>',
       '        <path class="ln" d="M720 127 L760 86" marker-end="url(#a1)"/>',
       '        <line class="lk1" x1="331" y1="160" x2="569" y2="160"/>',
       '        <rect class="f1" x="378" y="146" width="144" height="28"/><text class="b on" x="450" y="165" font-size="12" text-anchor="middle">VERIFICAÇÃO</text>',
       '        <text class="mu halo" x="450" y="140" font-size="10.5" text-anchor="middle">as saídas atendem às entradas?</text>',
       '        <line class="lk2" x1="261" y1="52" x2="639" y2="52"/>',
       '        <rect class="f2" x="384" y="38" width="132" height="28"/><text class="b" x="450" y="57" font-size="12" text-anchor="middle" style="fill:var(--on-s2)">VALIDAÇÃO</text>',
       '        <text class="mu halo" x="450" y="86" font-size="10.5" text-anchor="middle">o produto serve para o uso pretendido?</text>',
       '        <text x="450" y="292" font-size="11.5" text-anchor="middle">A verificação olha para o que foi escrito. A validação olha para o que o cliente vai viver.</text>',
       "      </svg>"]

# ------------------------------------------------------------------ figura 2: as cinco etapas
W5, G5 = 164, 14
et = ['      <svg viewBox="0 0 900 222" role="img" aria-label="As cinco etapas do trabalho. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS) + ' A validação reprovada devolve o trabalho às entradas.">',
      "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
for k, (nome, desc) in enumerate(ETAPAS):
    x = 12 + k * (W5 + G5)
    ink = k == 4
    et.append(f'        <rect class="{["bx", "bx-s2", "bx", "bx-s1", "bx-ink"][k]}" x="{x}" y="16" width="{W5}" height="140"/>')
    et.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="36" font-size="10">ETAPA {k + 1}</text>')
    for j, l in enumerate(textwrap.wrap(nome, 22)[:2]):
        et.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{58 + j * 15}" font-size="12.5">{escape(l)}</text>')
    yy = 80 if len(textwrap.wrap(nome, 22)) == 1 else 92
    lines(et, desc, x + 12, yy, 26, cls="t-ground" if ink else "", step=14.5, maxl=4)
    if k < 4:
        et.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="78" x2="{x + W5 + G5 - 2}" y2="78" marker-end="url(#a2)"/>')
xa, xb = 12 + 3 * (W5 + G5) + W5 / 2, 12 + (W5 + G5) + W5 / 2
et.append(f'        <path class="ln-mu dash" d="M{xa} 158 V186 H{xb} V162" marker-end="url(#a2m)"/>')
et.append(f'        <text class="mu halo" x="{(xa + xb) / 2}" y="190" font-size="11" text-anchor="middle">a validação pode revelar uma entrada que faltava</text>')
et.append('        <text x="450" y="214" font-size="11.5" text-anchor="middle">As análises críticas acontecem ao fim de cada etapa: o projeto segue, muda ou para.</text>')
et.append("      </svg>")

# ------------------------------------------------------------------ figura 3: os tipos de entrada
TCLS = ["hd-p", "hd-p", "hd-c", "hd-c", "hd-ink", "hd-a", "hd-d"]
te = ['      <svg viewBox="0 0 900 318" role="img" aria-label="Os sete tipos de entrada de um projeto, com exemplos do filme para congelados. ' + " ".join(f"{a}: {b} Exemplo: {c}" for a, b, c in TIPOS_INFO) + '">']
for k, (tit, oque, exemplo) in enumerate(TIPOS_INFO):
    row = 0 if k < 4 else 1
    col = k if k < 4 else k - 4
    w = 214 if row == 0 else 288
    x = 10 + col * (w + 8)
    y = 10 + row * 154
    te.append(f'        <rect class="bx" x="{x}" y="{y}" width="{w}" height="144"/>')
    te.append(f'        <rect class="{TCLS[k]}" x="{x}" y="{y}" width="{w}" height="30"/>')
    te.append(f'        <text class="b {"t-ground" if TCLS[k] == "hd-ink" else "on"}" x="{x + 12}" y="{y + 20}" font-size="11.5">{escape(tit)}</text>')
    yy = lines(te, oque, x + 12, y + 50, int(w / 6.4), fs=11, step=14, maxl=3)
    te.append(f'        <text class="mono mu" x="{x + 12}" y="{yy + 8}" font-size="9.5">NO FILME PARA CONGELADOS</text>')
    lines(te, exemplo, x + 12, yy + 24, int(w / 6.2), fs=10.5, cls="mu", step=13.5, maxl=3)
te.append("      </svg>")

# ------------------------------------------------------------------ figura 4: os três controles
co = ['      <svg viewBox="0 0 900 262" role="img" aria-label="Os três controles do projeto. ' + " ".join(f"{a}: {b} Quando: {c} Quem: {d} Exemplo: {e}" for a, b, c, d, e in CONTROLES) + '">']
CC = ["hd-ink", "f1", "f2"]
for k, (nome, perg, quando, quem, exemplo) in enumerate(CONTROLES):
    x = 10 + k * 296
    co.append(f'        <rect class="bx" x="{x}" y="10" width="284" height="242"/>')
    co.append(f'        <rect class="{CC[k]}" x="{x}" y="10" width="284" height="56"/>')
    tc = "t-ground" if k == 0 else "on" if k == 1 else ""
    co.append(f'        <text class="b {tc}" x="{x + 12}" y="32" font-size="13"{" style=" + chr(34) + "fill:var(--on-s2)" + chr(34) if k == 2 else ""}>{escape(nome.upper())}</text>')
    co.append(f'        <text class="{tc}" x="{x + 12}" y="52" font-size="11.5"{" style=" + chr(34) + "fill:var(--on-s2)" + chr(34) if k == 2 else ""}>{escape(perg)}</text>')
    y = 86
    for rot, txt in (("QUANDO", quando), ("QUEM", quem), ("NO EXEMPLO DA INDÚSTRIA", exemplo)):
        co.append(f'        <text class="mono mu" x="{x + 12}" y="{y}" font-size="9.5">{rot}</text>')
        y = lines(co, txt, x + 12, y + 15, 44, fs=11, step=14, maxl=3) + 10
co.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Projeto</dt><dd>{escape(h["projeto"])}</dd></div>',
                      f'    <div><dt>Cliente ou usuário</dt><dd>{escape(h["cliente"])}</dd></div>',
                      f'    <div><dt>Objetivo</dt><dd>{escape(h["objetivo"])}</dd></div>',
                      f'    <div><dt>Responsável</dt><dd>{escape(h["resp"])}</dd></div>',
                      f'    <div><dt>Período</dt><dd>De {dt(h["inicio"])} a {dt(h["fim"])}. Situação lida em {dt(h["ref"])}.</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      '  </dl>'])


def tabela(caption, heads, rows):
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{caption}</caption>', f'      <thead><tr>{"".join(heads)}</tr></thead>', '      <tbody>']
    o += [f'        <tr>{r}</tr>' for r in rows]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def conf_chip(c):
    cls = "s1" if c == "OK" else "s2" if c in (PENDENTE, "Não atende: ação em curso") else "s3"
    return f'<span class="chip {cls}">{escape(c)}</span>'


RES_CLS = {APROV: "s1", RESS: "s2", REPROV: "s3"}


def etapa_tab(ex):
    ref, es = ex["head"]["ref"], ex["etps"]
    r = resumo(ex)
    rows = []
    for e in es:
        res = f'<span class="chip {RES_CLS[e["result"]]}">{e["result"]}</span>' if e["result"] else "—"
        rows.append(f'<td class="c n">{e["n"]}</td><td><strong>{escape(e["etapa"])}</strong><small>{escape(e["registro"]) or "—"}</small></td><td>{escape(e["tipo"])}</td>'
                    f'<td>{escape(e["resp"])}<small>{escape(e["part"])}</small></td><td class="c">{dt(e["prazo"], False)}</td>'
                    f'<td class="c{" no" if e["concl"] and e["concl"] > e["prazo"] else ""}">{dt(e["concl"], False)}</td><td>{res}<small>{escape(e["acoes"])}</small></td>'
                    f'<td>{conf_chip(etapa_conf(e, ref, es))}</td>')
    return tabela(f'Plano do projeto · {r["etapas"]} etapas, {r["concl"]} concluídas, {r["atras"]} atrasada{"s" if r["atras"] != 1 else ""} em {dt(ref)}',
                  ['<th class="c">#</th>', '<th style="width:26%">Etapa<small>Registro</small></th>', '<th>Tipo</th>', '<th style="width:16%">Responsável<small>Participantes</small></th>',
                   '<th class="c">Prazo</th>', '<th class="c">Concluída</th>', '<th style="width:22%">Resultado<small>Ações e ressalvas</small></th>', '<th>Conferência</th>'], rows)


def entrada_tab(ex):
    r = resumo(ex)
    rows = []
    for x in ex["ents"]:
        res = f'<span class="chip {"s1" if x["result"] == "Atende" else "s3"}">{x["result"]}</span>' if x["result"] else "—"
        rows.append(f'<td class="n">{x["id"]}</td><td><strong>{escape(x["req"])}</strong><small>{escape(x["tipo"])} · {escape(x["fonte"])}</small></td><td>{escape(x["saida"])}</td>'
                    f'<td>{escape(x["metodo"])}</td><td>{res}<small>{escape(x["evid"])}</small></td><td>{conf_chip(entrada_conf(x))}</td>')
    return tabela(f'Entradas, saídas e verificação · {r["ents"]} entradas: {r["at"]} atendem, {r["nao"]} não atende, {r["pend"]} pendente',
                  ['<th>#</th>', '<th style="width:30%">Entrada<small>Tipo · fonte</small></th>', '<th style="width:20%">Saída que atende</th>', '<th style="width:18%">Como verificar</th>',
                   '<th style="width:18%">Resultado<small>Evidência ou ação</small></th>', '<th>Conferência</th>'], rows)


def mud_tab(ex):
    rows = [f'<td class="c">{dt(m["data"], False)}</td><td><strong>{escape(m["oque"])}</strong><small>{escape(m["motivo"])}</small></td><td>{escape(m["analise"]) or "—"}</td>'
            f'<td>{escape(m["verif"]) or "—"}</td><td>{escape(m["aut"])}</td><td>{conf_chip(mud_conf(m))}</td>' for m in ex["muds"]]
    return tabela(f'Mudanças de projeto · {len(ex["muds"])}', ['<th class="c">Data</th>', '<th style="width:28%">O que mudou<small>Motivo</small></th>', '<th style="width:24%">Análise do impacto</th>',
                                                               '<th style="width:22%">O que foi verificado de novo</th>', '<th>Quem autorizou</th>', '<th>Conferência</th>'], rows)


# ------------------------------------------------------------------ exemplo 3: a validação que revelou uma entrada
hi = ['      <svg viewBox="0 0 900 214" role="img" aria-label="A validação que revelou uma entrada que faltava. ' + " ".join(f"{a}, {b}: {c}" for a, b, c in HISTORIA) + '">',
      "        <defs>" + marker("a5") + "</defs>"]
HCLS = ["bx-s1", "bx", "bx-s3", "bx-s2", "bx"]
for k, (quando, tit, txt) in enumerate(HISTORIA):
    x = 12 + k * (W5 + G5)
    hi.append(f'        <rect class="{HCLS[k]}" x="{x}" y="14" width="{W5}" height="160"/>')
    hi.append(f'        <text class="mono mu" x="{x + 12}" y="34" font-size="9.5">{escape(quando.upper())}</text>')
    for j, l in enumerate(textwrap.wrap(tit, 22)[:2]):
        hi.append(f'        <text class="b" x="{x + 12}" y="{54 + j * 15}" font-size="12">{escape(l)}</text>')
    lines(hi, txt, x + 12, 76 if len(textwrap.wrap(tit, 22)) == 1 else 90, 26, fs=10.5, step=14, maxl=6)
    if k < 4:
        hi.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="94" x2="{x + W5 + G5 - 2}" y2="94" marker-end="url(#a5)"/>')
hi.append('        <text x="450" y="204" font-size="11.5" text-anchor="middle">O lote passou na verificação e falhou na validação. A entrada que faltava só apareceu no uso real.</text>')
hi.append("      </svg>")

# ------------------------------------------------------------------ módulo 7: prazo e conclusão de cada etapa, na indústria
es2, ref2 = EX2["etps"], EX2["head"]["ref"]
D0, D1 = date(2027, 6, 1), date(2027, 9, 30)
X0, X1, TOP, RH = 330, 870, 46, 30
sx = lambda d: X0 + (d - D0).days * (X1 - X0) / (D1 - D0).days  # noqa: E731
bottom = TOP + RH * len(es2)
ch = [f'      <svg id="bars" viewBox="0 0 900 {bottom + 40}" role="img" aria-label="Prazo e conclusão de cada etapa do projeto D-07 da indústria, lidos em 30 de agosto de 2027. '
      + " ".join(f'{e["n"]}, {e["etapa"]}: prazo {dt(e["prazo"], False)}, ' + (f'concluída em {dt(e["concl"], False)}.' if e["concl"] else "não concluída.") for e in es2) + '">',
      '        <g font-size="11.5">',
      f'          <circle class="f1" cx="{X0 + 6}" cy="19" r="6"/><text x="{X0 + 18}" y="23">Concluída no prazo</text>',
      f'          <circle class="f2" cx="{X0 + 166}" cy="19" r="6"/><text x="{X0 + 178}" y="23">Com atraso</text>',
      f'          <circle class="o3" cx="{X0 + 286}" cy="19" r="6"/><text x="{X0 + 298}" y="23">Atrasada</text>',
      f'          <circle class="o0" cx="{X0 + 386}" cy="19" r="6"/><text x="{X0 + 398}" y="23">Prazo futuro</text>', '        </g>']
d = D0
while d <= D1:
    ch.append(f'        <line class="grid" x1="{sx(d):.1f}" y1="{TOP - 6}" x2="{sx(d):.1f}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{sx(d):.1f}" y="{bottom + 16}" font-size="11" text-anchor="middle"{TNUM}>{d:%d/%m}</text>')
    d = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
ch.append(f'        <line class="goal" x1="{sx(ref2):.1f}" y1="{TOP - 10}" x2="{sx(ref2):.1f}" y2="{bottom}"/>')
ch.append(f'        <text class="mu halo" x="{sx(ref2) + 4:.1f}" y="{bottom + 32}" font-size="10.5">leitura: {dt(ref2, False)}</text>')
for k, e in enumerate(es2):
    y = TOP + RH * k + RH / 2
    ch.append(f'        <text x="20" y="{y + 4}" font-size="11.5"><tspan class="mono mu">{e["n"]}</tspan><tspan dx="8">{escape(textwrap.shorten(e["etapa"], 44, placeholder="…"))}</tspan></text>')
    if e["concl"]:
        cls = "f1" if e["concl"] <= e["prazo"] else "f2"
        if e["concl"] > e["prazo"]:
            ch.append(f'        <line class="ln-mu" x1="{sx(e["prazo"]):.1f}" y1="{y}" x2="{sx(e["concl"]):.1f}" y2="{y}"/>')
        if e["concl"] > e["prazo"]:
            ch.append(f'        <circle class="o0" cx="{sx(e["prazo"]):.1f}" cy="{y}" r="4"/>')
        ch.append(f'        <circle class="pt {cls}" data-k="{k}" cx="{sx(e["concl"]):.1f}" cy="{y}" r="6"/>')
    else:
        cls = "o3" if e["prazo"] < ref2 else "o0"
        if e["prazo"] < ref2:
            ch.append(f'        <line class="ln-mu dash" x1="{sx(e["prazo"]):.1f}" y1="{y}" x2="{sx(ref2):.1f}" y2="{y}"/>')
        ch.append(f'        <circle class="pt {cls}" data-k="{k}" cx="{sx(e["prazo"]):.1f}" cy="{y}" r="6"/>')
for k, e in enumerate(es2):
    st = ("no prazo" if e["concl"] <= e["prazo"] else f'com {(e["concl"] - e["prazo"]).days} dias de atraso') if e["concl"] else ("atrasada" if e["prazo"] < ref2 else "prazo futuro")
    ch.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" aria-label="{e["n"]}, {escape(e["etapa"])}: prazo {dt(e["prazo"], False)}, {st}" '
              f'data-k="{k}" data-n="{e["n"]} · {escape(e["etapa"])}" data-p="{dt(e["prazo"], False)}" data-c="{dt(e["concl"], False)}" data-s="{st}" '
              f'data-cx="{sx(e["concl"] or e["prazo"]):.1f}" data-cy="{TOP + RH * k}"/>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>#</th><th>Etapa</th><th class="c">Prazo</th><th class="c">Concluída</th><th>Situação</th></tr></thead>', '          <tbody>']
for e in es2:
    st = ("No prazo" if e["concl"] <= e["prazo"] else "Com atraso") if e["concl"] else ("Atrasada" if e["prazo"] < ref2 else "Prazo futuro")
    tb.append(f'            <tr><td>{e["n"]}</td><td>{escape(e["etapa"])}</td><td class="c">{dt(e["prazo"], False)}</td><td class="c">{dt(e["concl"], False)}</td><td>{st}</td></tr>')
tb += ['          </tbody>', '        </table>']
charttext = ('  <p>Até a validação, o projeto andou no prazo: o plano, a especificação, a análise crítica e o lote de teste terminaram no dia previsto ou antes. '
             'A validação no cliente terminou três dias depois do previsto e reprovou o filme. A análise crítica reagiu em três dias, com uma entrada nova e uma mudança analisada. '
             'O lote 2 deveria ter sido ensaiado em 27/08 e, na leitura de 30/08, ainda não tinha sido: a segunda validação e a liberação dependem dele. '
             'O gráfico mostra o que o cronograma em lista esconde: o projeto não está atrasado por acaso, e sim porque a validação encontrou o que a verificação não procurava.</p>')

# ------------------------------------------------------------------ módulo 10: figura da ISO
ISOP = [("8.3.2 · Planejar", "Etapas, análises críticas, verificação, validação, responsáveis, recursos e o cliente."),
        ("8.3.3 · Entradas", "Funcionais e de desempenho, legais, normas, projetos anteriores e falhas possíveis."),
        ("8.3.4 · Controles", "Análises críticas, verificação, validação e ações sobre os problemas."),
        ("8.3.5 · Saídas", "Atender às entradas, servir à produção, trazer os critérios de aceitação e o essencial ao uso seguro."),
        ("8.3.6 · Mudanças", "Identificar, analisar, autorizar e registrar, prevenindo efeitos indesejados.")]
iso = ['      <svg viewBox="0 0 900 180" role="img" aria-label="O que a norma pede sobre projeto e desenvolvimento. ' + " ".join(f"{a}: {b}" for a, b in ISOP) + '">']
for k, (a, b) in enumerate(ISOP):
    x = 10 + k * 178
    iso.append(f'        <rect class="bx" x="{x}" y="14" width="170" height="152"/>')
    iso.append(f'        <rect class="hd-ink" x="{x}" y="14" width="170" height="34"/>')
    iso.append(f'        <text class="b t-ground" x="{x + 10}" y="36" font-size="11.5">{escape(a)}</text>')
    lines(iso, b, x + 10, 68, 26, fs=11, step=15, maxl=6)
iso.append("      </svg>")

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--VMODEL-->", "\n".join(vm)), ("<!--FLUXO-->", "\n".join(et)), ("<!--TIPOS-->", "\n".join(te)), ("<!--CONTROLES-->", "\n".join(co)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1ETAPAS-->", etapa_tab(EX1)), ("<!--EX1ENTRADAS-->", entrada_tab(EX1)), ("<!--EX1MUD-->", mud_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2ETAPAS-->", etapa_tab(EX2)), ("<!--EX2ENTRADAS-->", entrada_tab(EX2)), ("<!--EX2MUD-->", mud_tab(EX2)),
                 ("<!--EX3FIG-->", "\n".join(hi)), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHARTTEXT-->", charttext),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Projeto e desenvolvimento</title>")
assert "Projeto e desenvolvimento" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", resumo(EX1), "| indústria", resumo(EX2))
