# -*- coding: utf-8 -*-
"""Monta treinamento-calibracao.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cal_data import (APROV, CADEIA, CHECK, EMDIA, ETAPAS, EX1, EX2, FORA, GROSSA, IMPACTO, RAZAO, REPROV, SEMCAL, VENCE, VENCIDO,  # noqa: E402
                      adequacao, cal_conf, inst_conf, proxima, resultado, resumo, situacao)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# em dia, vence em breve e vencido: a mesma paleta de três cores do estudo de Satisfação, validada para daltonismo nos dois modos
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
svg .zone{fill:var(--s1-tint)}
svg .err1{stroke:var(--s1);stroke-width:3} svg .err3{stroke:var(--s3);stroke-width:3}
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

/* Ficha dos instrumentos (acima de cada exemplo) */"""
assert css.count("\n.ficha{") == 1
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

TNUM = ' style="font-variant-numeric:tabular-nums"'


def dt(d, ano=True):
    return d.strftime("%d/%m/%Y" if ano else "%d/%m") if d else "—"


def num(v):
    if v is None:
        return "—"
    if float(v).is_integer():
        return str(int(v))
    return f"{v:g}".replace(".", ",")


def sg(v):
    return ("+" if v > 0 else "") + num(v) if v is not None else "—"


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


# ------------------------------------------------------------------ figura 1: a cadeia de rastreabilidade
W5, G5 = 164, 14
ca = ['      <svg viewBox="0 0 900 214" role="img" aria-label="A cadeia de rastreabilidade metrológica. ' + " ".join(f"{a}: {b}" for a, b in CADEIA)
      + ' Cada elo é calibrado pelo anterior, e a incerteza cresce a cada elo.">', "        <defs>" + marker("a1") + marker("a1m", True) + "</defs>"]
for k, (tit, txt) in enumerate(CADEIA):
    x = 12 + k * (W5 + G5)
    ink = k == 4
    ca.append(f'        <rect class="{["bx", "bx", "bx-s1", "bx-s1", "bx-ink"][k]}" x="{x}" y="16" width="{W5}" height="118"/>')
    for j, l in enumerate(textwrap.wrap(tit, 22)[:2]):
        ca.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{40 + j * 15}" font-size="12">{escape(l)}</text>')
    lines(ca, txt, x + 12, 40 + 15 * len(textwrap.wrap(tit, 22)[:2]) + 8, 26, cls="t-ground" if ink else "", step=14, maxl=4)
    if k < 4:
        ca.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="75" x2="{x + W5 + G5 - 2}" y2="75" marker-end="url(#a1)"/>')
ca.append('        <path class="ln-mu dash" d="M94 150 H806" marker-end="url(#a1m)"/>')
ca.append('        <text class="mu halo" x="450" y="154" font-size="11" text-anchor="middle">a incerteza cresce a cada elo</text>')
ca.append('        <text x="450" y="182" font-size="11.5" text-anchor="middle">Rastreabilidade é poder seguir, de elo em elo, até o padrão da unidade.</text>')
ca.append('        <text class="mu" x="450" y="202" font-size="11" text-anchor="middle">O certificado de cada elo diz contra o que o instrumento foi comparado, e com que incerteza.</text>')
ca.append("      </svg>")

# ------------------------------------------------------------------ figura 2: as cinco etapas
et = ['      <svg viewBox="0 0 900 222" role="img" aria-label="As cinco etapas do trabalho. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS) + ' O instrumento reprovado volta à escolha.">',
      "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
for k, (nome, desc) in enumerate(ETAPAS):
    x = 12 + k * (W5 + G5)
    ink = k == 4
    et.append(f'        <rect class="{["bx", "bx-s2", "bx-s1", "bx", "bx-ink"][k]}" x="{x}" y="16" width="{W5}" height="140"/>')
    et.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="36" font-size="10">ETAPA {k + 1}</text>')
    et.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="58" font-size="12.5">{escape(nome)}</text>')
    lines(et, desc, x + 12, 80, 26, cls="t-ground" if ink else "", step=14.5, maxl=5)
    if k < 4:
        et.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="78" x2="{x + W5 + G5 - 2}" y2="78" marker-end="url(#a2)"/>')
xa, xb = 12 + 4 * (W5 + G5) + W5 / 2, 12 + (W5 + G5) + W5 / 2
et.append(f'        <path class="ln-mu dash" d="M{xa} 158 V186 H{xb} V162" marker-end="url(#a2m)"/>')
et.append(f'        <text class="mu halo" x="{(xa + xb) / 2}" y="190" font-size="11" text-anchor="middle">o instrumento reprovado, ou grosso demais, é trocado</text>')
et.append('        <text x="450" y="214" font-size="11.5" text-anchor="middle">A etapa escura é a que mais se esquece: o que fazer quando o instrumento estava errado.</text>')
et.append("      </svg>")

# ------------------------------------------------------------------ figura 3: erro, incerteza e critério
EMA = 1.0
X0, X1 = 250, 830
sx = lambda v: X0 + (v + 3) * (X1 - X0) / 6  # noqa: E731
CASOS = [("TER-01, verificado em 05/03", 0.3, 0.2), ("TER-02, verificado em 15/03", -2.0, 0.3)]
er = ['      <svg viewBox="0 0 900 236" role="img" aria-label="Como ler o resultado de uma calibração. O critério é o erro máximo admissível de mais ou menos 1 grau. '
      'TER-01: erro de mais 0,3 grau, incerteza de 0,2: o intervalo inteiro cabe no critério, aprovado. TER-02: erro de menos 2 graus, incerteza de 0,3: fora do critério, reprovado.">',
      f'        <rect class="zone" x="{sx(-EMA)}" y="30" width="{sx(EMA) - sx(-EMA)}" height="128"/>',
      f'        <text class="mono mu" x="{(sx(-EMA) + sx(EMA)) / 2}" y="22" font-size="10" text-anchor="middle">ERRO MÁXIMO ADMISSÍVEL: ±1 °C</text>']
for v in range(-3, 4):
    er.append(f'        <line class="grid" x1="{sx(v)}" y1="30" x2="{sx(v)}" y2="158"/>')
    er.append(f'        <text class="mu" x="{sx(v)}" y="176" font-size="11" text-anchor="middle"{TNUM}>{sg(v) if v else "0"}</text>')
er.append(f'        <line class="ln" x1="{sx(0)}" y1="30" x2="{sx(0)}" y2="158"/>')
er.append(f'        <text class="mono mu" x="{(X0 + X1) / 2}" y="196" font-size="10" text-anchor="middle">ERRO ENCONTRADO, EM °C</text>')
for k, (rot, e, u) in enumerate(CASOS):
    y = 64 + k * 56
    ok = abs(e) + u <= EMA
    cls = "err1" if ok else "err3"
    er.append(f'        <text x="20" y="{y + 4}" font-size="11.5"><tspan class="b">{escape(rot)}</tspan></text>')
    er.append(f'        <text class="mu" x="20" y="{y + 20}" font-size="10.5">erro {sg(e)} °C · incerteza {num(u)} °C</text>')
    er.append(f'        <line class="{cls}" x1="{sx(e - u)}" y1="{y}" x2="{sx(e + u)}" y2="{y}"/>')
    er.append(f'        <line class="{cls}" x1="{sx(e - u)}" y1="{y - 6}" x2="{sx(e - u)}" y2="{y + 6}"/><line class="{cls}" x1="{sx(e + u)}" y1="{y - 6}" x2="{sx(e + u)}" y2="{y + 6}"/>')
    er.append(f'        <circle class="{"f1" if ok else "f3"}" cx="{sx(e)}" cy="{y}" r="6"/>')
    er.append(f'        <text class="b halo" x="{sx(e + u) + 10 if e >= 0 else sx(e - u) - 10}" y="{y + 4}" font-size="11.5"{" text-anchor=" + chr(34) + "end" + chr(34) if e < 0 else ""}>{APROV if ok else REPROV}</text>')
er.append('        <text x="450" y="226" font-size="11.5" text-anchor="middle">Aprovado só quando o erro, somado à incerteza, cabe no critério. A incerteza é a dúvida do próprio laboratório.</text>')
er.append("      </svg>")

# ------------------------------------------------------------------ figura 4: resolução e tolerância
re_ = ['      <svg viewBox="0 0 900 222" role="img" aria-label="Resolução e tolerância, no exemplo da espessura de 38 a 42 micrômetros. Com resolução de 1 micrômetro, a faixa '
       f'cabe em apenas 4 passos, e o micrômetro não distingue 41,6 de 42,4. Com 0,1 micrômetro, são 40 passos. A regra deste material pede ao menos {RAZAO} passos dentro da tolerância.">']
T0, T1 = 37, 43
tx = lambda v: 200 + (v - T0) * (860 - 200) / (T1 - T0)  # noqa: E731
for k, (rot, res, sub) in enumerate((("Resolução de 1 µm", 1.0, "4 passos na tolerância: grossa"), ("Resolução de 0,1 µm", 0.1, "40 passos na tolerância: adequada"))):
    y = 40 + k * 78
    re_.append(f'        <text class="b" x="20" y="{y + 10}" font-size="12">{rot}</text>')
    re_.append(f'        <text class="mu" x="20" y="{y + 27}" font-size="10.5">{sub}</text>')
    re_.append(f'        <rect class="zone" x="{tx(38)}" y="{y - 6}" width="{tx(42) - tx(38)}" height="34"/>')
    re_.append(f'        <line class="ln-mu" x1="{tx(T0)}" y1="{y + 22}" x2="{tx(T1)}" y2="{y + 22}"/>')
    v = T0
    while v <= T1 + 1e-9:
        major = abs(v - round(v)) < 1e-9
        re_.append(f'        <line class="{"ln" if major else "ln-mu"}" x1="{tx(v):.1f}" y1="{y + (4 if major else 12)}" x2="{tx(v):.1f}" y2="{y + 22}"/>')
        v += res
for v in range(T0, T1 + 1):
    re_.append(f'        <text class="mu" x="{tx(v)}" y="{40 + 78 + 50}" font-size="11" text-anchor="middle"{TNUM}>{v}</text>')
re_.append(f'        <text class="mono mu" x="{(tx(38) + tx(42)) / 2}" y="24" font-size="10" text-anchor="middle">TOLERÂNCIA: 38 A 42 µm</text>')
re_.append(f'        <text x="450" y="210" font-size="11.5" text-anchor="middle">Regra deste material: a resolução deve caber ao menos {RAZAO} vezes na tolerância.</text>')
re_.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Responsável</dt><dd>{escape(h["resp"])}</dd></div>',
                      f'    <div><dt>Padrões próprios</dt><dd>{escape(h["padrao"])}</dd></div>',
                      f'    <div><dt>Leitura</dt><dd>{dt(h["ref"])}.</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      '  </dl>'])


def tabela(caption, heads, rows):
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{caption}</caption>', f'      <thead><tr>{"".join(heads)}</tr></thead>', '      <tbody>']
    o += [f'        <tr>{r}</tr>' for r in rows]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


SIT_CLS = {EMDIA: "s1", VENCE: "s2", VENCIDO: "s3", SEMCAL: "s3", FORA: "sl"}


def per(m):
    return "todo mês" if m == 1 else f"a cada {m} meses"


def conf_chip(c):
    return f'<span class="chip {"s1" if c == "OK" else "sl" if c == FORA else "s3"}">{escape(c)}</span>'


def inst_tab(ex):
    ref, r = ex["head"]["ref"], resumo(ex)
    rows = []
    for i in ex["insts"]:
        s, a = situacao(i, ref), adequacao(i)
        tol = f'{num(i["tol"])} {i["unid"]}' if i["tol"] is not None else "—"
        rows.append(f'<td class="n">{i["cod"]}</td><td><strong>{escape(i["nome"])}</strong><small>{escape(i["local"])} · {escape(i["uso"])}</small></td>'
                    f'<td class="c">{tol}</td><td class="c{" no" if a == GROSSA else ""}">{num(i["res"])} {i["unid"]}<small>{a or "—"}</small></td>'
                    f'<td>{escape(i["tipo"])}<small>{per(i["interv"])} · ±{num(i["ema"])} {i["unid"]}</small></td>'
                    f'<td class="c">{dt(i["ultima"])}</td><td class="c">{dt(proxima(i))}</td><td><span class="chip {SIT_CLS[s]}">{s}</span></td>'
                    f'<td>{conf_chip(inst_conf(i, ref))}</td>')
    sits = r["sits"]
    h = ex["head"]
    quantos = f'{r["insts"]} dos {h["total"]} cadastrados' if h["total"] else f'{r["insts"]} cadastrados'
    return tabela(f'{h["lista"]} · {quantos}: {sits[EMDIA]} em dia, {sits[VENCE]} vence{"m" if sits[VENCE] != 1 else ""} em breve, '
                  f'{sits[VENCIDO]} vencido{"s" if sits[VENCIDO] != 1 else ""}, {sits[SEMCAL]} sem calibração, {sits[FORA]} fora de uso',
                  ['<th>Código</th>', '<th style="width:28%">Instrumento<small>Local · o que mede</small></th>', '<th class="c">Tolerância</th>', '<th class="c">Resolução</th>',
                   '<th style="width:15%">Controle<small>Intervalo · erro máximo</small></th>', '<th class="c">Última</th>', '<th class="c">Próxima</th>', '<th>Situação</th>',
                   '<th>Conferência</th>'], rows)


def cal_tab(ex):
    insts, r = ex["insts"], resumo(ex)
    ema = {i["cod"]: (i["ema"], i["unid"]) for i in insts}
    rows = []
    for c in sorted(ex["cals"], key=lambda c: c["data"]):
        res = resultado(c, insts)
        u = ema[c["cod"]][1]
        extra = ""
        if c["acao"]:
            extra += f'<strong>Ação:</strong> {escape(c["acao"])}'
        if res == REPROV:
            extra += f'<small>Resultados anteriores: {escape(c["impacto"]) or "não avaliados."}</small>'
        rows.append(f'<td class="c">{dt(c["data"], False)}</td><td class="n">{c["cod"]}</td><td>{escape(c["tipo"])}<small>{escape(c["reg"])}</small></td><td>{escape(c["ponto"])}</td>'
                    f'<td class="c">{sg(c["erro"])} {u}<small>± {num(c["inc"])}</small></td><td class="c">±{num(ema[c["cod"]][0])} {u}</td>'
                    f'<td><span class="chip {"s1" if res == APROV else "s3"}">{res}</span></td><td>{extra or "—"}</td><td>{conf_chip(cal_conf(c, insts))}</td>')
    return tabela(f'Calibrações e verificações · {r["cals"]} registros, {r["reprov"]} reprovado{"s" if r["reprov"] != 1 else ""}',
                  ['<th class="c">Data</th>', '<th>Código</th>', '<th style="width:18%">Tipo<small>Registro</small></th>', '<th style="width:12%">Ponto medido</th>',
                   '<th class="c">Erro<small>Incerteza</small></th>', '<th class="c">Critério</th>', '<th>Resultado</th>', '<th style="width:28%">Ação e resultados anteriores</th>',
                   '<th>Conferência</th>'], rows)


# ------------------------------------------------------------------ exemplo 3: a avaliação dos resultados anteriores
HCLS = ["bx-s1", "bx", "bx-s2", "bx-s3", "bx-ink"]
im = ['      <svg viewBox="0 0 900 222" role="img" aria-label="A avaliação dos resultados anteriores do micrômetro MIC-07. ' + " ".join(f"{a}, {b}: {c}" for a, b, c in IMPACTO) + '">',
      "        <defs>" + marker("a5") + "</defs>"]
for k, (quando, tit, txt) in enumerate(IMPACTO):
    x = 12 + k * (W5 + G5)
    ink = k == 4
    im.append(f'        <rect class="{HCLS[k]}" x="{x}" y="14" width="{W5}" height="168"/>')
    im.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="34" font-size="9.5">{escape(quando.upper())}</text>')
    tl = textwrap.wrap(tit, 22)[:2]
    for j, l in enumerate(tl):
        im.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{54 + j * 15}" font-size="12">{escape(l)}</text>')
    lines(im, txt, x + 12, 76 if len(tl) == 1 else 90, 26, fs=10.5, cls="t-ground" if ink else "", step=14, maxl=6)
    if k < 4:
        im.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="96" x2="{x + W5 + G5 - 2}" y2="96" marker-end="url(#a5)"/>')
im.append('        <text x="450" y="210" font-size="11.5" text-anchor="middle">O instrumento errado não estraga só a medição de hoje: todas, desde a última calibração boa, ficam em dúvida.</text>')
im.append("      </svg>")

# ------------------------------------------------------------------ módulo 7: dias até o vencimento, nos dois exemplos
DMIN, DMAX = -60, 360
X0, X1, TOP, RH = 330, 860, 46, 26
dx = lambda d: X0 + (d - DMIN) * (X1 - X0) / (DMAX - DMIN)  # noqa: E731
rows_c = []
for nome, ex in (("PIZZARIA", EX1), ("INDÚSTRIA", EX2)):
    rows_c.append(("grupo", nome))
    for i in ex["insts"]:
        rows_c.append(("inst", i, ex["head"]["ref"]))
bottom = TOP + RH * len(rows_c)
ch = [f'      <svg id="bars" viewBox="0 0 900 {bottom + 44}" role="img" aria-label="Dias até o vencimento da calibração ou da verificação de cada instrumento, na data da leitura de cada exemplo. '
      + " ".join(f'{r[1]["cod"]}: ' + (f'{(proxima(r[1]) - r[2]).days} dias.' if situacao(r[1], r[2]) not in (FORA, SEMCAL) else situacao(r[1], r[2]).lower() + ".") for r in rows_c if r[0] == "inst")
      + '">', '        <g font-size="11.5">']
for k, (t, cls) in enumerate(((EMDIA, "f1"), (VENCE, "f2"), (VENCIDO, "f3"))):
    ch.append(f'          <rect class="{cls}" x="{X0 + k * 160}" y="12" width="14" height="14"/><text x="{X0 + 22 + k * 160}" y="24">{t}</text>')
ch.append('        </g>')
for d in range(-60, DMAX + 1, 60):
    ch.append(f'        <line class="{"ln" if d == 0 else "grid"}" x1="{dx(d):.1f}" y1="{TOP - 6}" x2="{dx(d):.1f}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{dx(d):.1f}" y="{bottom + 16}" font-size="11" text-anchor="middle"{TNUM}>{d}</text>')
ch.append(f'        <text class="mono mu" x="{(X0 + X1) / 2}" y="{bottom + 36}" font-size="10" text-anchor="middle">DIAS ATÉ O VENCIMENTO, NA DATA DA LEITURA</text>')
hits = []
for k, row in enumerate(rows_c):
    y = TOP + RH * k
    if row[0] == "grupo":
        ch.append(f'        <text class="mono mu" x="20" y="{y + 17}" font-size="10">{row[1]}</text>')
        continue
    i, ref = row[1], row[2]
    s = situacao(i, ref)
    ch.append(f'        <text x="36" y="{y + 17}" font-size="11.5"><tspan class="b">{i["cod"]}</tspan><tspan class="mu" dx="8">{escape(textwrap.shorten(i["nome"], 34, placeholder="…"))}</tspan></text>')
    if s in (FORA, SEMCAL):
        ch.append(f'        <text class="b halo" x="{dx(0) + 8:.1f}" y="{y + 17}" font-size="11"{"" if s == SEMCAL else " fill-opacity=" + chr(34) + ".75" + chr(34)}>{s.lower()}</text>')
        dias = s
    else:
        d = (proxima(i) - ref).days
        cls = "f3" if s == VENCIDO else "f2" if s == VENCE else "f1"
        a, b = sorted((dx(0), dx(max(DMIN, min(DMAX, d)))))
        ch.append(f'        <rect class="bar {cls}" data-k="{k}" x="{a:.1f}" y="{y + 6}" width="{max(b - a, 2):.1f}" height="{RH - 12}"/>')
        ch.append(f'        <text class="mu halo" x="{(b + 6) if d >= 0 else (a - 6):.1f}" y="{y + 17}" font-size="10.5"{" text-anchor=" + chr(34) + "end" + chr(34) if d < 0 else ""}{TNUM}>{d}</text>')
        dias = f"{d} dias"
    hits.append(f'        <rect class="hit" x="14" y="{y}" width="872" height="{RH}" tabindex="0" role="img" aria-label="{i["cod"]}, {escape(i["nome"])}: {s.lower()}, próxima {dt(proxima(i), False)}" '
                f'data-k="{k}" data-n="{i["cod"]} · {escape(i["nome"])}" data-s="{s}" data-p="{dt(proxima(i))}" data-d="{dias}" data-cx="{dx(0):.1f}" data-cy="{y}"/>')
ch += hits + ["      </svg>"]
tb = ['        <table class="aud">', '          <thead><tr><th>Código</th><th>Instrumento</th><th class="c">Próxima</th><th class="c">Dias</th><th>Situação</th></tr></thead>', '          <tbody>']
for row in rows_c:
    if row[0] == "inst":
        i, ref = row[1], row[2]
        s = situacao(i, ref)
        tb.append(f'            <tr><td>{i["cod"]}</td><td>{escape(i["nome"])}</td><td class="c">{dt(proxima(i))}</td>'
                  f'<td class="c">{(proxima(i) - ref).days if s not in (FORA, SEMCAL) else "—"}</td><td>{s}</td></tr>')
tb += ['          </tbody>', '        </table>']
charttext = ('  <p>Na pizzaria, dois instrumentos vencem em menos de uma semana: a balança da bancada no dia seguinte, e o termômetro de espeto em cinco dias. Verificação mensal é assim: '
             'a lista de vencimentos precisa ser lida toda semana, ou a verificação vira atraso. O termômetro do recebimento nunca foi verificado, e foi ele que recusou a muçarela a 9 °C '
             'no estudo de liberação: a decisão provavelmente estava certa, mas ninguém pode provar. Na indústria, o termômetro da câmara de condicionamento venceu há 15 dias, '
             'às vésperas dos ensaios a -18 °C do projeto de filme para congelados, em julho. Os ensaios precisam esperar a verificação, ou não valem.</p>')

# ------------------------------------------------------------------ módulo 10: figura da ISO
ISOP = [("7.1.5.1 · Recursos", "Instrumentos adequados ao que medem, e mantidos, quando a medição verifica a conformidade.", "a adequação e a manutenção"),
        ("7.1.5.2 · Calibrar", "Calibrar ou verificar, em intervalos, contra padrões rastreáveis; sem padrão, registrar a base usada.", "o cadastro e o registro"),
        ("7.1.5.2 · Identificar", "Identificar a situação de cada instrumento e protegê-lo de ajustes, danos e desgaste.", "a situação e a etiqueta"),
        ("7.1.5.2 · Reagir", "Quando o instrumento estava errado, avaliar se os resultados anteriores foram afetados e agir.", "o exemplo 3")]
iso = ['      <svg viewBox="0 0 900 200" role="img" aria-label="O que a norma pede sobre os recursos de medição. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in ISOP) + '">']
for k, (a, b, c) in enumerate(ISOP):
    x = 10 + k * 222
    iso.append(f'        <rect class="bx" x="{x}" y="14" width="214" height="172"/>')
    iso.append(f'        <rect class="hd-ink" x="{x}" y="14" width="214" height="34"/>')
    iso.append(f'        <text class="b t-ground" x="{x + 12}" y="36" font-size="11.5">{escape(a)}</text>')
    lines(iso, b, x + 12, 70, 32, fs=11.5, step=16, maxl=5)
    lines(iso, "Neste estudo: " + c, x + 12, 160, 34, fs=11, cls="mu", step=15, maxl=2)
iso.append("      </svg>")

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--CADEIA-->", "\n".join(ca)), ("<!--FLUXO-->", "\n".join(et)), ("<!--ERRO-->", "\n".join(er)), ("<!--RESOLUCAO-->", "\n".join(re_)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1INST-->", inst_tab(EX1)), ("<!--EX1CAL-->", cal_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2INST-->", inst_tab(EX2)), ("<!--EX2CAL-->", cal_tab(EX2)),
                 ("<!--EX3FIG-->", "\n".join(im)), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHARTTEXT-->", charttext),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Calibração e recursos de medição</title>")
assert "Calibração" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", resumo(EX1), "| indústria", resumo(EX2))
