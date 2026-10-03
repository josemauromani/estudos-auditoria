# -*- coding: utf-8 -*-
"""Monta treinamento-tecnica-auditoria.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import math
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tec_data import (ALTO, BASE, BAIXO, CHECK, CICLO, CONF, CONFORME, CRITERIOS, ESCALA, ETAPAS, EX1, EX2, FATOR, FORMACAO, FORTE, FRACA, FUNIL,  # noqa: E402
                      INCOMP, ISOL, LIDERAR, EQUIPE, MEDIA, MEDIO, MIN_OBS, MINIMO, NC, OM, PERGUNTA, POUCO, REPET, TIPOS_PERG, TRIANGULO, am_conf, am_sit,
                      aud_conta, aud_nivel, aud_pct, ev_conf, forca, passo, resumo, tamanho)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# conforme, isolado e repetido: a mesma paleta de três cores do estudo de Calibração, validada para daltonismo nos dois modos
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
svg .bx-s1{fill:var(--s1-tint);stroke:var(--s1);stroke-width:1.5} svg .bx-s2{fill:var(--s2-tint);stroke:var(--s2);stroke-width:1.5} svg .bx-s3{fill:var(--s3-tint);stroke:var(--s3);stroke-width:1.5}
svg .tick{stroke:var(--ink);stroke-width:2.5}
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
table.aud tr.tot td{font-weight:600;background:var(--sunk)}

/* Ficha da auditoria (acima de cada exemplo) */"""
assert css.count("\n.ficha{") == 1
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

TNUM = ' style="font-variant-numeric:tabular-nums"'
END = ' text-anchor="end"'
MID = ' text-anchor="middle"'
W5, G5 = 164, 14


def dt(d, ano=True):
    return d.strftime("%d/%m/%Y" if ano else "%d/%m") if d else "—"


def num(v):
    return f"{v:,}".replace(",", ".") if isinstance(v, int) else str(v)


def marker(i, mu=False):
    return (f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path class="{"ah-mu" if mu else "ah"}" d="M0 0 L10 5 L0 10 z"/></marker>')


def lines(o, txt, x, y, wrap, fs=10.5, cls="", step=13, maxl=3, anchor=None):
    """Texto quebrado em linhas; devolve o y da linha seguinte."""
    ls = textwrap.wrap(txt, wrap, break_on_hyphens=False)
    assert len(ls) <= maxl, txt
    attr = (f' class="{cls}"' if cls else "") + (f' text-anchor="{anchor}"' if anchor else "")
    for j, l in enumerate(ls):
        o.append(f'        <text{attr} x="{x}" y="{y + j * step}" font-size="{fs}">{escape(l)}</text>')
    return y + step * len(ls)


def cinco(o, itens, classes, mk, y0=16, h=140, rotulo=None, maxd=5, mid=None):
    """Cinco caixas em linha, ligadas por setas; devolve as coordenadas x das caixas."""
    xs = []
    for k, (tit, desc) in enumerate(itens):
        x = 12 + k * (W5 + G5)
        xs.append(x)
        ink = classes[k] == "bx-ink"
        o.append(f'        <rect class="{classes[k]}" x="{x}" y="{y0}" width="{W5}" height="{h}"/>')
        if rotulo:
            o.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="{y0 + 20}" font-size="10">{escape(rotulo(k))}</text>')
        tl = textwrap.wrap(tit, 19, break_on_hyphens=False)
        yt = y0 + (42 if rotulo else 24)
        for j, l in enumerate(tl):
            o.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{yt + j * 15}" font-size="12.5">{escape(l)}</text>')
        lines(o, desc, x + 12, yt + 15 * len(tl) + 8, 25, cls="t-ground" if ink else "", step=14.5, maxl=maxd)
        if k < len(itens) - 1:
            ym = mid or (y0 + h / 2)
            o.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="{ym}" x2="{x + W5 + G5 - 2}" y2="{ym}" marker-end="url(#{mk})"/>')
    return xs


# ------------------------------------------------------------------ figura 1: o ciclo da evidência
ci = ['      <svg viewBox="0 0 900 214" role="img" aria-label="O caminho de uma evidência. ' + " ".join(f"{a}: {b}" for a, b in CICLO)
      + ' Sem qualquer um dos cinco, a constatação não se sustenta.">', "        <defs>" + marker("a1") + "</defs>"]
cinco(ci, CICLO, ["bx", "bx-p", "bx-d", "bx-c", "bx-ink"], "a1", h=128, maxd=4)
ci.append(f'        <text x="450" y="176" font-size="11.5"{MID}>Toda constatação passa pelos cinco. Se faltar um, ela é opinião, e não achado de auditoria.</text>')
ci.append(f'        <text class="mu" x="450" y="196" font-size="11"{MID}>A técnica do auditor está nos três do meio: de quem ouvir, quanto ver e contra o que comparar.</text>')
ci.append("      </svg>")

# ------------------------------------------------------------------ figura 2: as cinco etapas em campo
et = ['      <svg viewBox="0 0 900 236" role="img" aria-label="As cinco etapas do trabalho em campo. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS)
      + ' Quando a amostra mostra um desvio isolado, o auditor volta a coletar.">', "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
xs = cinco(et, ETAPAS, ["bx", "bx-p", "bx-d", "bx-c", "bx-ink"], "a2", h=152, rotulo=lambda k: f"ETAPA {k + 1}", mid=84)
xa, xb = xs[3] + W5 / 2, xs[2] + W5 / 2
et.append(f'        <path class="ln-mu dash" d="M{xa} 170 V198 H{xb} V174" marker-end="url(#a2m)"/>')
et.append(f'        <text class="mu halo" x="{(xa + xb) / 2}" y="202" font-size="11"{MID}>desvio isolado: ampliar a amostra</text>')
et.append(f'        <text x="450" y="228" font-size="11.5"{MID}>Coletar e comparar se alternam até a evidência bastar. Só então a constatação é escrita.</text>')
et.append("      </svg>")

# ------------------------------------------------------------------ figura 3: o funil de perguntas
fu = ['      <svg viewBox="0 0 900 250" role="img" aria-label="O funil de perguntas, do aberto ao fechado. ' + " ".join(f"{a}: {b} {c}" for a, b, c in FUNIL) + '">']
CLS4 = ["bx-p", "bx-d", "bx-c", "bx-ink"]
for k, (tipo, ex, para) in enumerate(FUNIL):
    y, w = 14 + k * 54, 360 - k * 70
    x0 = 200 - w / 2
    ink = CLS4[k] == "bx-ink"
    fu.append(f'        <path class="{CLS4[k]}" d="M{x0} {y} H{x0 + w} L{x0 + w - 35} {y + 48} H{x0 + 35} Z"/>')
    fu.append(f'        <text class="b{" t-ground" if ink else ""}" x="200" y="{y + 29}" font-size="12.5"{MID}>{escape(tipo)}</text>')
    fu.append(f'        <text x="400" y="{y + 22}" font-size="12">{escape(ex)}</text>')
    fu.append(f'        <text class="mu" x="400" y="{y + 39}" font-size="10.5">{escape(para)}</text>')
fu.append(f'        <text x="450" y="242" font-size="11.5"{MID}>Do largo ao estreito: a pergunta fechada só aparece no fim, para confirmar o que a evidência já mostrou.</text>')
fu.append("      </svg>")

# ------------------------------------------------------------------ figura 4: a amostragem sistemática, nas notas de recebimento da pizzaria
AM = EX1["ams"][2]
N4, n4, p4, i4 = AM["pop"], tamanho(AM), passo(AM), AM["inicio"]
esc = [i4 + k * p4 for k in range(n4)]
CW4 = 34
am = [f'      <svg viewBox="0 0 900 220" role="img" aria-label="Amostragem sistemática nas {N4} notas de recebimento de fevereiro: amostra de {n4}, '
      f'uma a cada {p4}, a partir da {i4}ª. Notas escolhidas: {", ".join(str(e) for e in esc)}.">']
for k in range(N4):
    lin, col = divmod(k, 24)
    x, y = 42 + col * CW4, 40 + lin * 50
    sel = (k + 1) in esc
    am.append(f'        <rect class="{"f1" if sel else "bx"}" x="{x}" y="{y}" width="{CW4 - 6}" height="{CW4 - 6}"/>')
    am.append(f'        <text class="{"b on" if sel else "mu"}" x="{x + (CW4 - 6) / 2}" y="{y + 18}" font-size="10"{MID}{TNUM}>{k + 1}</text>')
am.append(f'        <text class="mono mu" x="42" y="26" font-size="10">{N4} NOTAS DE RECEBIMENTO DE FEVEREIRO, NA ORDEM DA PASTA</text>')
am.append(f'        <text x="42" y="168" font-size="11.5"><tspan class="b">População {N4}, risco alto:</tspan> amostra de {n4}. Passo de {N4} ÷ {n4} = {p4}. '
          f'Início sorteado entre 1 e {p4}: a {i4}ª nota.</text>')
am.append(f'        <text class="mu" x="42" y="190" font-size="11">Depois, de {p4} em {p4}: {", ".join(str(e) for e in esc)}. O auditado não escolhe, e nenhum dia do mês fica de fora.</text>')
am.append("      </svg>")

# ------------------------------------------------------------------ figura 5: o triângulo da evidência
tr = ['      <svg viewBox="0 0 900 270" role="img" aria-label="O triângulo da evidência. ' + " ".join(f"{a}: {b}" for a, b in TRIANGULO)
      + ' Forte: duas fontes ou mais. Média: só observação ou só registro. Fraca: só entrevista. Toda não conformidade precisa de evidência forte.">']
V = [(230, 30), (80, 220), (380, 220)]
tr.append(f'        <path class="bx-s1" d="M{V[0][0]} {V[0][1]} L{V[1][0]} {V[1][1]} L{V[2][0]} {V[2][1]} Z"/>')
for (x, y), (t, d), cls in zip(V, TRIANGULO, ("hd-p", "hd-d", "hd-c")):
    tr.append(f'        <circle class="{cls}" cx="{x}" cy="{y}" r="9"/>')
for (x, y, anc, dy), (t, d) in zip(((230, 18, MID, -4), (70, 248, END, 0), (390, 248, "", 0)), TRIANGULO):
    tr.append(f'        <text class="b" x="{x}" y="{y + dy}" font-size="12"{anc}>{escape(t)}</text>')
tr.append(f'        <text class="b" x="230" y="160" font-size="13"{MID}>Forte</text>')
tr.append(f'        <text class="mu" x="230" y="177" font-size="10.5"{MID}>duas fontes ou mais</text>')
for k, (f, d, cls, uso) in enumerate(((FORTE, "Duas fontes ou mais, uma delas objetiva.", "bx-s1", "Basta para uma não conformidade."),
                                     (MEDIA, "Só observação, ou só registro.", "bx-s2", "Basta para conforme ou oportunidade."),
                                     (FRACA, "Só o que alguém disse.", "bx-s3", "Pede outra fonte antes de concluir."))):
    y = 22 + k * 76
    tr.append(f'        <rect class="{cls}" x="470" y="{y}" width="418" height="66"/>')
    tr.append(f'        <text class="b" x="486" y="{y + 24}" font-size="12.5">{f}</text>')
    tr.append(f'        <text x="560" y="{y + 24}" font-size="11.5">{escape(d)}</text>')
    tr.append(f'        <text class="mu" x="486" y="{y + 48}" font-size="11">{escape(uso)}</text>')
tr.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h, r = ex["head"], resumo(ex)
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Auditoria</dt><dd>{h["num"]} · {escape(h["processo"])}, em {dt(h["data"])}.</dd></div>',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Auditor líder</dt><dd>{escape(h["lider"])}</dd></div>',
                      f'    <div><dt>Equipe</dt><dd>{escape(h["equipe"])}</dd></div>',
                      f'    <div><dt>Observador</dt><dd>{escape(h["observador"])}</dd></div>',
                      f'    <div><dt>Critérios</dt><dd>{escape(h["criterios"])}</dd></div>',
                      '  </dl>'])


TOT = ' class="tot"'


def tabela(caption, heads, rows):
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{caption}</caption>', f'      <thead><tr>{"".join(heads)}</tr></thead>', '      <tbody>']
    # linhas marcadas com "!" são de total
    o += [f'        <tr{TOT if r.startswith("!") else ""}>{r.lstrip("!")}</tr>' for r in rows]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def chip(c, ok=("OK",)):
    return f'<span class="chip {"s1" if c in ok else "s3"}">{escape(c)}</span>'


AM_CLS = {CONF: "s1", ISOL: "s2", REPET: "s3", INCOMP: "s2"}
EV_CLS = {FORTE: "s1", MEDIA: "s2", FRACA: "s3"}
CT_CLS = {CONFORME: "s1", NC: "s3", OM: "s2"}
NV_CLS = {LIDERAR: "s1", EQUIPE: "s2", FORMACAO: "s3", POUCO: "sl"}


def am_tab(ex):
    r = resumo(ex)
    rows = []
    for a in ex["ams"]:
        n, s = tamanho(a), am_sit(a)
        rows.append(f'<td><strong>{escape(a["oque"])}</strong><small>{a["req"]} · {escape(a["periodo"])}</small></td><td class="c">{num(a["pop"])}</td><td>{a["risco"]}</td>'
                    f'<td class="c"><strong>{n}</strong><small>1 a cada {passo(a)}, a partir da {a["inicio"]}ª</small></td>'
                    f'<td class="c{" no" if a["verif"] < n else ""}">{a["verif"]}</td><td class="c{" no" if a["desv"] else ""}">{a["desv"]}</td>'
                    f'<td><span class="chip {AM_CLS[s]}">{escape(s)}</span>{"<small>" + escape(a["nota"]) + "</small>" if a["nota"] else ""}</td><td>{chip(am_conf(a))}</td>')
    return tabela(f'Amostras · {r["ams"]} populações, {r["verif"]} registros verificados, {r["desv"]} desvios',
                  ['<th style="width:30%">O que se verifica<small>Requisito · período</small></th>', '<th class="c">População</th>', '<th>Risco</th>',
                   '<th class="c">Amostra<small>Sistemática</small></th>', '<th class="c">Verificados</th>', '<th class="c">Desvios</th>', '<th style="width:26%">Conclusão</th>',
                   '<th>Conferência</th>'], rows)


def ev_tab(ex):
    r = resumo(ex)
    rows = []
    for e in ex["evs"]:
        f = forca(e)
        fon = "".join(f'<small><b>{k}:</b> {escape(e[c])}</small>' for k, c in (("Entrevista", "ent"), ("Observação", "obs"), ("Registro", "reg")) if e[c])
        const = f'<span class="chip {CT_CLS[e["const"]]}">{escape(e["const"])}</span>' if e["const"] else "—"
        fc = f'<span class="chip {EV_CLS[f]}">{f}</span>' if f else "—"
        rows.append(f'<td class="n">{e["req"]}</td><td><strong>{escape(e["perg"])}</strong>{fon}</td><td>{const}</td><td>{fc}</td><td>{chip(ev_conf(e))}</td>')
    c = r["consts"]
    return tabela(f'Evidências · {r["evs"]} perguntas: {c[CONFORME]} conformes, {c[NC]} não conformidades, {c[OM]} oportunidade{"s" if c[OM] != 1 else ""}',
                  ['<th>Requisito</th>', '<th style="width:56%">Pergunta<small>As fontes de evidência</small></th>', '<th>Constatação</th>', '<th>Força</th>', '<th>Conferência</th>'], rows)


def aud_tab(ex):
    auds = ex["auds"]
    rows = []
    for k, (etapa, crit, critico) in enumerate(CRITERIOS):
        cel = "".join(f'<td class="c{" no" if critico and a["notas"][k] is not None and a["notas"][k] <= 1 else ""}">{"—" if a["notas"][k] is None else a["notas"][k]}</td>' for a in auds)
        rows.append(f'<td>{etapa}</td><td>{escape(crit)}{"<small>Critério crítico</small>" if critico else ""}</td>{cel}')
    pts = "".join(f'<td class="c">{aud_conta(a["notas"])[1]} de {3 * aud_conta(a["notas"])[0]}<small>{aud_conta(a["notas"])[0]} observados</small></td>' for a in auds)
    pct = "".join(f'<td class="c">{aud_pct(a["notas"]) * 100:.0f} %</td>' for a in auds)
    niv = "".join(f'<td class="c"><span class="chip {NV_CLS[aud_nivel(a["notas"])]}">{aud_nivel(a["notas"])}</span></td>' for a in auds)
    rows += [f'!<td></td><td>Pontos</td>{pts}', f'!<td></td><td>Percentual</td>{pct}', f'!<td></td><td>Nível</td>{niv}']
    heads = ['<th>Etapa</th>', '<th style="width:42%">Critério</th>'] + [f'<th class="c">{escape(a["nome"])}<small>{escape(a["papel"])}</small></th>' for a in auds]
    return tabela(f'Avaliação dos auditores em campo · notas de 0 a 3, “—” para não observado', heads, rows)


# ------------------------------------------------------------------ exemplo 3: o fio de uma pergunta
im = ['      <svg viewBox="0 0 900 236" role="img" aria-label="O fio de uma pergunta, na auditoria da pizzaria. ' + " ".join(f"{a}: {b} Resposta: {c}" for a, b, c in PERGUNTA) + '">',
      "        <defs>" + marker("a6") + "</defs>"]
for k, (tipo, perg, resp) in enumerate(PERGUNTA):
    x = 12 + k * (W5 + G5)
    ink = k == 4
    im.append(f'        <rect class="{["bx-p", "bx-d", "bx-c", "bx-d", "bx-ink"][k]}" x="{x}" y="14" width="{W5}" height="186"/>')
    im.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="34" font-size="9.5">{escape(tipo.upper())}</text>')
    yy = lines(im, perg, x + 12, 54, 24, fs=11, cls="b" + (" t-ground" if ink else ""), step=14, maxl=4)
    lines(im, resp, x + 12, yy + 8, 25, fs=10.5, cls="t-ground" if ink else "mu", step=13.5, maxl=6)
    if k < 4:
        im.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="100" x2="{x + W5 + G5 - 2}" y2="100" marker-end="url(#a6)"/>')
im.append(f'        <text x="450" y="226" font-size="11.5"{MID}>Quatro perguntas, nenhuma indutora. A não conformidade saiu dos registros, e não da opinião do auditor.</text>')
im.append("      </svg>")

# ------------------------------------------------------------------ módulo 8: as amostras dos dois exemplos
XMAX = 32
X0, X1, TOP, RH = 380, 860, 46, 28
vx = lambda v: X0 + v * (X1 - X0) / XMAX  # noqa: E731
rows_c = []
for nome, ex in (("PIZZARIA", EX1), ("INDÚSTRIA", EX2)):
    rows_c.append(("grupo", nome, ex))
    rows_c += [("a", a, ex) for a in ex["ams"]]
bottom = TOP + RH * len(rows_c)
COR = {CONF: "f1", ISOL: "f2", INCOMP: "f2", REPET: "f3"}
ch = [f'      <svg id="bars" viewBox="0 0 900 {bottom + 44}" role="img" aria-label="Registros verificados em cada amostra, com o tamanho planejado e os desvios. '
      + " ".join(f'{r[1]["oque"]}: {r[1]["verif"]} de {tamanho(r[1])}, {r[1]["desv"]} desvios, {am_sit(r[1]).lower()}.' for r in rows_c if r[0] == "a") + '">',
      '        <g font-size="11.5">']
for k, (t, cls) in enumerate(((CONF, "f1"), ("Isolado ou incompleta", "f2"), ("Desvio repetido", "f3"))):
    ch.append(f'          <rect class="{cls}" x="{X0 + k * 165}" y="12" width="14" height="14"/><text x="{X0 + 22 + k * 165}" y="24">{t}</text>')
ch.append('        </g>')
for d in range(0, XMAX + 1, 8):
    ch.append(f'        <line class="{"ln" if d == 0 else "grid"}" x1="{vx(d):.1f}" y1="{TOP - 6}" x2="{vx(d):.1f}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{vx(d):.1f}" y="{bottom + 16}" font-size="11"{MID}{TNUM}>{d}</text>')
ch.append(f'        <text class="mono mu" x="{(X0 + X1) / 2}" y="{bottom + 36}" font-size="10"{MID}>REGISTROS VERIFICADOS · O TRAÇO É O TAMANHO PLANEJADO</text>')
hits = []
for k, row in enumerate(rows_c):
    y = TOP + RH * k
    if row[0] == "grupo":
        ch.append(f'        <text class="mono mu" x="20" y="{y + 18}" font-size="10">{row[1]}</text>')
        continue
    a = row[1]
    n, s = tamanho(a), am_sit(a)
    ch.append(f'        <text x="36" y="{y + 18}" font-size="11"><tspan>{escape(textwrap.shorten(a["oque"], 46, placeholder="…"))}</tspan></text>')
    ch.append(f'        <rect class="bar {COR[s]}" data-k="{k}" x="{X0}" y="{y + 6}" width="{max(vx(a["verif"]) - X0, 2):.1f}" height="{RH - 12}"/>')
    ch.append(f'        <line class="tick" x1="{vx(n):.1f}" y1="{y + 2}" x2="{vx(n):.1f}" y2="{y + RH - 2}"/>')
    rot = f'{a["desv"]} desvio{"s" if a["desv"] != 1 else ""} em {a["verif"]}'
    xr = max(vx(a["verif"]), vx(n))
    if xr > 760:  # perto da borda: o rótulo vai para dentro da barra
        ch.append(f'        <text class="b on" x="{vx(a["verif"]) - 8:.1f}" y="{y + 18}" font-size="10.5"{END}{TNUM}>{rot}</text>')
    else:
        ch.append(f'        <text class="mu halo" x="{xr + 8:.1f}" y="{y + 18}" font-size="10.5"{TNUM}>{rot}</text>')
    hits.append(f'        <rect class="hit" x="14" y="{y}" width="872" height="{RH}" tabindex="0" role="img" aria-label="{escape(a["oque"])}: {a["verif"]} de {n}, {a["desv"]} desvios, {escape(s.lower())}" '
                f'data-k="{k}" data-n="{escape(a["oque"])}" data-s="{escape(s)}" data-d="{a["desv"]} desvios em {a["verif"]} de {n}" data-p="população {num(a["pop"])}" '
                f'data-cx="{vx(a["verif"]):.1f}" data-cy="{y}"/>')
ch += hits + ["      </svg>"]
tb = ['        <table class="aud">', '          <thead><tr><th>O que se verifica</th><th class="c">População</th><th class="c">Planejada</th><th class="c">Verificados</th>'
      '<th class="c">Desvios</th><th>Conclusão</th></tr></thead>', '          <tbody>']
for row in rows_c:
    if row[0] == "a":
        a = row[1]
        tb.append(f'            <tr><td>{escape(a["oque"])}</td><td class="c">{num(a["pop"])}</td><td class="c">{tamanho(a)}</td><td class="c">{a["verif"]}</td>'
                  f'<td class="c">{a["desv"]}</td><td>{escape(am_sit(a))}</td></tr>')
tb += ['          </tbody>', '        </table>']

# ------------------------------------------------------------------ módulo 5: a tabela de tamanhos
tam = ['  <div class="tbl">', '    <table>', '      <thead><tr><th style="width:28%">População</th><th class="c">Amostra-base</th>'
       + "".join(f'<th class="c">Risco {r.lower()}<small>× {str(FATOR[r]).replace(".", ",")}</small></th>' for r in (ALTO, MEDIO, BAIXO)) + '</tr></thead>', '      <tbody>']
ant = 0
for ate, b in BASE:
    faixa = f"Até {ate}" if ant == 0 else (f"De {ant + 1} a {ate}" if ate else f"Acima de {ant}")
    if b is None:
        cel = '<td class="c">Todos</td>' * 4
    else:
        cel = f'<td class="c">{b}</td>' + "".join(f'<td class="c">{max(MINIMO, math.ceil(b * FATOR[r] - 1e-9))}</td>' for r in (ALTO, MEDIO, BAIXO))
    tam.append(f'        <tr><td><strong>{faixa}</strong></td>{cel}</tr>')
    ant = ate or ant
tam += ['      </tbody>', '    </table>', '  </div>']

tipos = "\n".join(f'        <tr><td><strong>{escape(a)}</strong></td><td>{escape(b)}</td><td>{escape(c)}</td><td>{escape(d)}</td></tr>' for a, b, c, d in TIPOS_PERG)
escala = " ".join(f"<b>{n}</b> {escape(t.lower())}." for n, t in ESCALA)

# ------------------------------------------------------------------ módulo 11: figura da ISO
ISOP = [("Princípios", "Integridade, apresentação justa, devido cuidado, confidencialidade, independência, evidência e risco.", "o tom da entrevista"),
        ("Coletar e verificar", "A informação só vira evidência quando pode ser verificada, por amostra, ligada ao critério.", "a amostra e a força"),
        ("Amostragem", "Por julgamento ou estatística; a conclusão sempre carrega a incerteza da amostra.", "a tabela e o passo"),
        ("Competência", "Comportamento, conhecimento e habilidade, avaliados e mantidos ao longo do tempo.", "a auditoria testemunhada")]
iso = ['      <svg viewBox="0 0 900 200" role="img" aria-label="O que a ISO 19011 orienta sobre a técnica de auditoria. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in ISOP) + '">']
for k, (a, b, c) in enumerate(ISOP):
    x = 10 + k * 222
    iso.append(f'        <rect class="bx" x="{x}" y="14" width="214" height="172"/>')
    iso.append(f'        <rect class="hd-ink" x="{x}" y="14" width="214" height="34"/>')
    iso.append(f'        <text class="b t-ground" x="{x + 12}" y="36" font-size="11.5">{escape(a)}</text>')
    lines(iso, b, x + 12, 70, 32, fs=11.5, step=16, maxl=5)
    lines(iso, "Neste estudo: " + c, x + 12, 160, 34, fs=11, cls="mu", step=15, maxl=2)
iso.append("      </svg>")

crit = "\n".join(f'        <tr><td>{escape(e)}</td><td>{escape(c)}</td><td>{"Sim" if k else "—"}</td></tr>' for e, c, k in CRITERIOS)
check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--CICLO-->", "\n".join(ci)), ("<!--FLUXO-->", "\n".join(et)), ("<!--FUNIL-->", "\n".join(fu)), ("<!--TIPOS-->", tipos),
                 ("<!--AMOSTRA-->", "\n".join(am)), ("<!--TAMANHOS-->", "\n".join(tam)), ("<!--TRIANGULO-->", "\n".join(tr)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1AM-->", am_tab(EX1)), ("<!--EX1EV-->", ev_tab(EX1)), ("<!--EX1AUD-->", aud_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2AM-->", am_tab(EX2)), ("<!--EX2EV-->", ev_tab(EX2)), ("<!--EX2AUD-->", aud_tab(EX2)),
                 ("<!--EX3FIG-->", "\n".join(im)), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CRITERIOS-->", crit), ("<!--ESCALA-->", escala), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Técnica de auditoria</title>")
assert "Técnica" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", resumo(EX1), "| indústria", resumo(EX2))
