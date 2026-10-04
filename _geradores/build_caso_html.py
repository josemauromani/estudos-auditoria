# -*- coding: utf-8 -*-
"""Monta treinamento-caso-integrado.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from datetime import date
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from caso_data import (ANUAL, ATRASO, CADEIA, CHECK, CONT, EMDIA, ESTUDOS, ETAPAS, EX1, EX2, GRUPO, GRUPOS, LINK, MENSAL, MESES, NAOCOMECOU,  # noqa: E402
                       NEC, PERGUNTAS, SEM, TRIM, cal_conf, cal_conta, cal_sit, mes_estado, previstos, rastro_conf, rastro_dias, resumo)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# feito, previsto e atrasado: a mesma paleta de três cores do estudo de Calibração, validada para daltonismo nos dois modos
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
svg .lane{fill:var(--sunk)}
svg .fio{stroke:var(--accent);stroke-width:2;fill:none;stroke-linejoin:round}
svg .now{stroke:var(--ink);stroke-width:1.5;stroke-dasharray:4 3}
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

/* Ficha da organização (acima de cada exemplo) */"""
assert css.count("\n.ficha{") == 1
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

TNUM = ' style="font-variant-numeric:tabular-nums"'
END = ' text-anchor="end"'
MID = ' text-anchor="middle"'
NOMES_MES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


def dt(d, ano=True):
    return d.strftime("%d/%m/%Y" if ano else "%d/%m") if d else "—"


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


# ------------------------------------------------------------------ figura 1 e figura de exemplo: o fio, em raias por grupo de estudos
def raias(ex, idsvg):
    ps = ex["passos"]
    d0, d1 = min(p["data"] for p in ps), max(p["data"] for p in ps)
    X0, X1, Y0, LH = 230, 880, 20, 52
    tx = lambda d: X0 + (d - d0).days * (X1 - X0) / max((d1 - d0).days, 1)  # noqa: E731
    yb = Y0 + LH * 4
    leg_rows = (len(ps) + 2) // 3
    h = yb + 44 + leg_rows * 20 + 4
    o = [f'      <svg viewBox="0 0 900 {h}" role="img" aria-label="O fio {escape(ex["head"]["fio"].lower())}, passo a passo, nas quatro faixas de estudos da série. '
         + " ".join(f'Passo {k}: {dt(p["data"])}, {p["estudo"]}, faixa {GRUPO[p["estudo"]].lower()}.' for k, p in enumerate(ps, 1)) + '">']
    for k, g in enumerate(GRUPOS):
        y = Y0 + k * LH
        o.append(f'        <rect class="lane" x="{X0 - 10}" y="{y + 3}" width="{X1 - X0 + 20}" height="{LH - 6}"/>')
        lines(o, g, 14, y + LH / 2 - 2, 30, fs=11, cls="b", step=13, maxl=2)
    # meses no eixo
    m, a = d0.month, d0.year
    while (a, m) <= (d1.year, d1.month):
        d = date(a, m, 1)
        if d >= d0:
            o.append(f'        <line class="grid" x1="{tx(d):.1f}" y1="{Y0}" x2="{tx(d):.1f}" y2="{yb}"/>')
            if m in (1, 4, 7, 10):
                o.append(f'        <text class="mu" x="{tx(d):.1f}" y="{yb + 15}" font-size="10.5"{MID}>{MESES[m - 1].lower()}/{str(a)[2:]}</text>')
        m += 1
        if m == 13:
            m, a = 1, a + 1
    pts, ultimo = [], {}
    for k, p in enumerate(ps, 1):
        g = GRUPO[p["estudo"]]
        # dois passos próximos na mesma faixa não podem se sobrepor: no mínimo 20 de distância
        x = max(tx(p["data"]), ultimo.get(g, -99) + 20)
        ultimo[g] = x
        y = Y0 + GRUPOS.index(g) * LH + LH / 2
        pts.append((x, y))
    o.append('        <path class="fio" d="M' + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + '"/>')
    for k, (x, y) in enumerate(pts, 1):
        o.append(f'        <circle class="pt" cx="{x:.1f}" cy="{y:.1f}" r="9"/><text class="b on" x="{x:.1f}" y="{y + 3.5:.1f}" font-size="9.5"{MID}{TNUM}>{k}</text>')
    for k, p in enumerate(ps):
        col, lin = k // leg_rows, k % leg_rows
        x, y = 14 + col * 296, yb + 44 + lin * 20
        o.append(f'        <text x="{x}" y="{y}" font-size="10.5"><tspan class="b"{TNUM}>{k + 1}</tspan><tspan dx="6">{escape(p["estudo"])}</tspan>'
                 f'<tspan class="mu" dx="6"{TNUM}>{dt(p["data"], False)}/{str(p["data"].year)[2:]}</tspan></text>')
    o.append("      </svg>")
    return "\n".join(o)


# ------------------------------------------------------------------ figura 2: as cinco etapas
W5, G5 = 164, 14
et = ['      <svg viewBox="0 0 900 236" role="img" aria-label="As cinco etapas do trabalho. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS)
      + ' O que a leitura mostra volta à escolha do próximo fio.">', "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
for k, (nome, desc) in enumerate(ETAPAS):
    x = 12 + k * (W5 + G5)
    ink = k == 4
    et.append(f'        <rect class="{["bx", "bx-p", "bx-d", "bx-c", "bx-ink"][k]}" x="{x}" y="16" width="{W5}" height="152"/>')
    et.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="36" font-size="10">ETAPA {k + 1}</text>')
    tl = textwrap.wrap(nome, 19)
    for j, l in enumerate(tl):
        et.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{58 + j * 15}" font-size="12.5">{escape(l)}</text>')
    lines(et, desc, x + 12, 66 + 15 * len(tl) + 4, 25, cls="t-ground" if ink else "", step=14.5, maxl=5)
    if k < 4:
        et.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="84" x2="{x + W5 + G5 - 2}" y2="84" marker-end="url(#a2)"/>')
xa, xb = 12 + 4 * (W5 + G5) + W5 / 2, 12 + W5 / 2
et.append(f'        <path class="ln-mu dash" d="M{xa} 170 V198 H{xb} V174" marker-end="url(#a2m)"/>')
et.append(f'        <text class="mu halo" x="{(xa + xb) / 2}" y="202" font-size="11"{MID}>o que a leitura mostra aponta o próximo fio a seguir</text>')
et.append(f'        <text x="450" y="228" font-size="11.5"{MID}>As três primeiras etapas olham para trás, pelos registros; as duas últimas, para o ano que vem.</text>')
et.append("      </svg>")

# ------------------------------------------------------------------ figura 3: a saída de um estudo é a entrada do outro
W6, G6 = 134, 14
ca = ['      <svg viewBox="0 0 900 190" role="img" aria-label="Uma cadeia típica de registros. ' + " ".join(f"{a}: {b}." for a, b in CADEIA)
      + ' Cada registro cita o anterior, e é isso que permite seguir o fio.">', "        <defs>" + marker("a3") + "</defs>"]
CLS6 = ["bx-s2", "bx-p", "bx-c", "bx-d", "bx-ink", "bx-s1"]
for k, (est, reg) in enumerate(CADEIA):
    x = 12 + k * (W6 + G6)
    ink = CLS6[k] == "bx-ink"
    ca.append(f'        <rect class="{CLS6[k]}" x="{x}" y="16" width="{W6}" height="96"/>')
    ca.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 10}" y="34" font-size="9.5">PASSO {k + 1}</text>')
    yy = lines(ca, est, x + 10, 54, 18, fs=12, cls="b" + (" t-ground" if ink else ""), step=14.5, maxl=2)
    lines(ca, reg, x + 10, yy + 4, 20, fs=10.5, cls="t-ground" if ink else "mu", step=13.5, maxl=2)
    if k < len(CADEIA) - 1:
        ca.append(f'        <line class="ln" x1="{x + W6 + 1}" y1="64" x2="{x + W6 + G6 - 2}" y2="64" marker-end="url(#a3)"/>')
ca.append(f'        <text x="450" y="146" font-size="11.5"{MID}>Cada registro cita o anterior: o RNC cita a reclamação, a ata cita o RNC, a lição cita a ata.</text>')
ca.append(f'        <text class="mu" x="450" y="166" font-size="11"{MID}>Quando um registro não cita o anterior, o fio se parte, e o auditor não consegue segui-lo.</text>')
ca.append("      </svg>")

# ------------------------------------------------------------------ figura 4: os quatro ritmos do ano
RIT = [(MENSAL, 1), (TRIM, 3), (SEM, 6), (ANUAL, 12)]
GX0, CWm, RH4 = 150, 30, 58
ri = ['      <svg viewBox="0 0 900 340" role="img" aria-label="Os quatro ritmos do sistema ao longo do ano. '
      + " ".join(f'{r}: {", ".join(e[0] for e in ESTUDOS if e[5] == r)}.' for r, _ in RIT)
      + f' Contínuo ou quando necessário: {", ".join(e[0] for e in ESTUDOS if e[5] in (CONT, NEC))}.">']
for j, mm in enumerate(MESES):
    ri.append(f'        <text class="mono mu" x="{GX0 + j * CWm + CWm / 2}" y="22" font-size="9"{MID}>{mm.upper()}</text>')
for i, (r, step) in enumerate(RIT):
    y = 32 + i * RH4
    ri.append(f'        <rect class="lane" x="10" y="{y}" width="880" height="{RH4 - 6}"/>')
    ri.append(f'        <text class="b" x="20" y="{y + 30}" font-size="12">{r}</text>')
    for j in range(12):
        cx = GX0 + j * CWm + CWm / 2
        if j % step == 0:
            ri.append(f'        <rect class="f1" x="{cx - 9}" y="{y + 17}" width="18" height="18"/>')
        else:
            ri.append(f'        <rect class="bx" x="{cx - 4}" y="{y + 22}" width="8" height="8"/>')
    lines(ri, ", ".join(e[0] for e in ESTUDOS if e[5] == r) + ".", GX0 + 12 * CWm + 20, y + 20, 64, fs=10.5, step=13.5, maxl=3)
yn = 32 + 4 * RH4 + 6
ri.append(f'        <text class="b" x="20" y="{yn + 14}" font-size="12">Contínuo ou quando necessário</text>')
lines(ri, ", ".join(e[0] for e in ESTUDOS if e[5] in (CONT, NEC)) + ".", 20, yn + 32, 150, fs=10.5, cls="mu", step=13.5, maxl=2)
ri.append("      </svg>")


# ------------------------------------------------------------------ calendários (exemplos 1 e 2)
EST_CLS = {"feito": "f1", "atrasado": "f3"}


def calendario(ex):
    h, cal = ex["head"], ex["cal"]
    X0, CW, TOP, RH = 330, 40, 40, 24
    bottom = TOP + RH * len(cal)
    o = [f'      <svg viewBox="0 0 900 {bottom + 50}" role="img" aria-label="Calendário de {h["ano"]} de {escape(h["org"].lower())}, lido no fim de {NOMES_MES[h["ref"] - 1]}. '
         + " ".join(f'{a["ativ"]}: {cal_sit(a, h["ref"]).lower()}, {cal_conta(a, h["ref"])["feitos"]} de {cal_conta(a, h["ref"])["prev"]} feitas até {NOMES_MES[h["ref"] - 1]}.' for a in cal) + '">']
    for j, mm in enumerate(MESES):
        o.append(f'        <text class="mono mu" x="{X0 + j * CW + CW / 2}" y="30" font-size="9.5"{MID}>{mm.upper()}</text>')
    for i, a in enumerate(cal):
        y = TOP + i * RH
        o.append(f'        <text x="14" y="{y + 16}" font-size="11"><tspan>{escape(textwrap.shorten(a["ativ"], 40, placeholder="…"))}</tspan></text>')
        for m in range(1, 13):
            cx = X0 + (m - 1) * CW + CW / 2
            e = mes_estado(a, m, h["ref"])
            if e in EST_CLS:
                o.append(f'        <rect class="{EST_CLS[e]}" x="{cx - 14}" y="{y + 4}" width="28" height="{RH - 8}"/>')
            elif e == "previsto":
                o.append(f'        <rect class="bx" x="{cx - 14}" y="{y + 4}" width="28" height="{RH - 8}"/>')
            elif e == "extra":
                o.append(f'        <circle class="f1" cx="{cx}" cy="{y + RH / 2}" r="5"/>')
        o.append(f'        <line class="grid" x1="14" y1="{y + RH}" x2="{X0 + 12 * CW}" y2="{y + RH}"/>')
    xr = X0 + h["ref"] * CW
    o.append(f'        <line class="now" x1="{xr}" y1="{TOP - 4}" x2="{xr}" y2="{bottom + 4}"/>')
    o.append(f'        <text class="mono mu halo" x="{xr + 4}" y="{bottom + 16}" font-size="9.5">LEITURA</text>')
    yl = bottom + 38
    for k, (cls, t) in enumerate((("f1", "Feita"), ("f3", "Atrasada"), ("bx", "Prevista"), ("dot", "Feita fora do plano"))):
        x = 14 + k * 150
        if cls == "dot":
            o.append(f'        <circle class="f1" cx="{x + 7}" cy="{yl - 4}" r="5"/><text x="{x + 20}" y="{yl}" font-size="11">{t}</text>')
        else:
            o.append(f'        <rect class="{cls}" x="{x}" y="{yl - 11}" width="14" height="14"/><text x="{x + 20}" y="{yl}" font-size="11">{t}</text>')
    o.append("      </svg>")
    return "\n".join(o)


def ficha(ex):
    h, r = ex["head"], resumo(ex)
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>O fio</dt><dd>{escape(h["fio"])}.</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      f'    <div><dt>Duração do fio</dt><dd>{r["total"]} dias, {r["passos"]} passos, {r["estudos"]} estudos.</dd></div>',
                      f'    <div><dt>Calendário</dt><dd>{h["ano"]}, lido no fim de {NOMES_MES[h["ref"] - 1]}. Responsável: {escape(h["resp"])}.</dd></div>',
                      '  </dl>'])


def tabela(caption, heads, rows):
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{caption}</caption>', f'      <thead><tr>{"".join(heads)}</tr></thead>', '      <tbody>']
    o += [f'        <tr>{r}</tr>' for r in rows]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def chip(c, ok=("OK",)):
    return f'<span class="chip {"s1" if c in ok else "s3"}">{escape(c)}</span>'


def rastro_tab(ex):
    ps, r = ex["passos"], resumo(ex)
    rows = []
    for k, (p, d, c) in enumerate(zip(ps, rastro_dias(ps), rastro_conf(ps)), 1):
        seg = f'{escape(p["saida"])}<small>→ {escape(p["prox"])}</small>' if p["saida"] else "—<small>fim do fio, por enquanto</small>"
        longo = d is not None and d == r["maior"]
        rows.append(f'<td class="n">{k}</td><td class="c">{dt(p["data"])}</td><td><a href="{LINK[p["estudo"]]}"><strong>{escape(p["estudo"])}</strong></a></td>'
                    f'<td>{escape(p["oque"])}</td><td>{escape(p["reg"])}</td><td>{seg}</td><td class="c{" no" if longo else ""}">{"—" if d is None else d}</td><td>{chip(c)}</td>')
    return tabela(f'O fio · {r["passos"]} passos em {r["total"]} dias, por {r["estudos"]} estudos. Maior intervalo: {r["maior"]} dias',
                  ['<th>Passo</th>', '<th class="c">Data</th>', '<th style="width:13%">Estudo</th>', '<th style="width:32%">O que aconteceu</th>', '<th style="width:14%">Registro</th>',
                   '<th style="width:18%">O que seguiu<small>Para qual estudo</small></th>', '<th class="c">Dias</th>', '<th>Conferência</th>'], rows)


SIT_CLS = {EMDIA: "s1", ATRASO: "s3", NAOCOMECOU: "sl"}


def cal_tab(ex):
    h, r = ex["head"], resumo(ex)
    rows = []
    for a in ex["cal"]:
        c, s = cal_conta(a, h["ref"]), cal_sit(a, h["ref"])
        meses = ", ".join(MESES[m - 1].lower() for m in sorted(previstos(a)))
        rows.append(f'<td><strong>{escape(a["ativ"])}</strong><small>{escape(a["estudo"])} · {escape(a["req"])}</small></td><td>{escape(a["resp"])}</td>'
                    f'<td>{a["freq"]}<small>{meses}</small></td><td class="c">{c["feitos"]} de {c["prev"]}{"<small>e 1 fora do plano</small>" if c["fora"] == 1 else ""}</td>'
                    f'<td class="c{" no" if c["atras"] else ""}">{c["atras"]}</td><td><span class="chip {SIT_CLS[s]}">{s}</span></td><td>{chip(cal_conf(a))}</td>')
    pz = f'{r["cumpr"] * 100:.0f} %'
    return tabela(f'Calendário de {h["ano"]} · {r["ativ"]} atividades. Até {NOMES_MES[h["ref"] - 1]}: {r["feitos"]} de {r["prev"]} feitas ({pz}), {r["atras"]} atrasadas',
                  ['<th style="width:30%">Atividade<small>Estudo · requisito</small></th>', '<th>Responsável</th>', '<th style="width:20%">Frequência<small>Meses previstos</small></th>',
                   '<th class="c">Feitas</th>', '<th class="c">Atrasadas</th>', '<th>Situação</th>', '<th>Conferência</th>'], rows)


# ------------------------------------------------------------------ exemplo 3: onde o fio da indústria demorou
ps2 = EX2["passos"]
gaps = [(k, d) for k, d in enumerate(rastro_dias(ps2)) if d is not None]
GMAX = 160
X0, X1, TOP, RH = 330, 840, 40, 24
gx = lambda d: X0 + d * (X1 - X0) / GMAX  # noqa: E731
bottom = TOP + RH * len(gaps)
mx = max(d for _, d in gaps)
de = ['      <svg viewBox="0 0 900 ' + str(bottom + 64) + '" role="img" aria-label="Dias entre cada passo do fio da indústria e o seguinte. '
      + " ".join(f'Do passo {k} ao {k + 1}, {ps2[k - 1]["estudo"]} para {ps2[k]["estudo"]}: {d} dias.' for k, d in gaps) + '">']
for d in range(0, GMAX + 1, 40):
    de.append(f'        <line class="{"ln" if d == 0 else "grid"}" x1="{gx(d):.1f}" y1="{TOP - 6}" x2="{gx(d):.1f}" y2="{bottom}"/>')
    de.append(f'        <text class="mu" x="{gx(d):.1f}" y="{bottom + 16}" font-size="11"{MID}{TNUM}>{d}</text>')
de.append(f'        <text class="mono mu" x="{(X0 + X1) / 2}" y="{bottom + 36}" font-size="10"{MID}>DIAS ATÉ O PASSO SEGUINTE</text>')
de.append(f'        <text class="mono mu" x="14" y="24" font-size="10">DE UM PASSO AO SEGUINTE</text>')
for i, (k, d) in enumerate(gaps):
    y = TOP + i * RH
    a, b = ps2[k - 1]["estudo"], ps2[k]["estudo"]
    de.append(f'        <text x="14" y="{y + 16}" font-size="11"><tspan class="b"{TNUM}>{k}→{k + 1}</tspan><tspan class="mu" dx="6">{escape(textwrap.shorten(a + " → " + b, 44, placeholder="…"))}</tspan></text>')
    de.append(f'        <rect class="{"f3" if d == mx else "f1"}" x="{X0}" y="{y + 5}" width="{max(gx(d) - X0, 2):.1f}" height="{RH - 10}"/>')
    de.append(f'        <text class="mu halo" x="{gx(d) + 6:.1f}" y="{y + 16}" font-size="10.5"{TNUM}>{d}</text>')
de.append(f'        <text x="450" y="{bottom + 58}" font-size="11.5"{MID}>A proposta dos dois medidores esperou {mx} dias pela análise crítica semestral, com a inspeção de 100% contendo o problema.</text>')
de.append("      </svg>")

# ------------------------------------------------------------------ módulo 7: cumprimento do calendário por atividade
X0, X1, TOP, RH = 330, 860, 46, 24
px = lambda v: X0 + v * (X1 - X0)  # noqa: E731
rows_c = []
for nome, ex in (("PIZZARIA", EX1), ("INDÚSTRIA", EX2)):
    rows_c.append(("grupo", nome, ex))
    rows_c += [("a", a, ex) for a in ex["cal"] if cal_conta(a, ex["head"]["ref"])["prev"]]
bottom = TOP + RH * len(rows_c)
ch = [f'      <svg id="bars" viewBox="0 0 900 {bottom + 44}" role="img" aria-label="Cumprimento do calendário por atividade, até o mês da leitura de cada exemplo. '
      + " ".join(f'{r[1]["ativ"]}: {cal_conta(r[1], r[2]["head"]["ref"])["feitos"]} de {cal_conta(r[1], r[2]["head"]["ref"])["prev"]}.' for r in rows_c if r[0] == "a")
      + '">', '        <g font-size="11.5">']
for k, (t, cls) in enumerate((("Todas as previstas feitas", "f1"), ("Com atividade atrasada", "f3"))):
    ch.append(f'          <rect class="{cls}" x="{X0 + k * 220}" y="12" width="14" height="14"/><text x="{X0 + 22 + k * 220}" y="24">{t}</text>')
ch.append('        </g>')
for p in range(0, 101, 25):
    ch.append(f'        <line class="{"ln" if p == 0 else "grid"}" x1="{px(p / 100):.1f}" y1="{TOP - 6}" x2="{px(p / 100):.1f}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{px(p / 100):.1f}" y="{bottom + 16}" font-size="11"{MID}{TNUM}>{p} %</text>')
ch.append(f'        <text class="mono mu" x="{(X0 + X1) / 2}" y="{bottom + 36}" font-size="10"{MID}>FEITAS ÷ PREVISTAS ATÉ O MÊS DA LEITURA</text>')
hits = []
for k, row in enumerate(rows_c):
    y = TOP + RH * k
    if row[0] == "grupo":
        ch.append(f'        <text class="mono mu" x="20" y="{y + 16}" font-size="10">{row[1]}</text>')
        continue
    a, ex = row[1], row[2]
    c = cal_conta(a, ex["head"]["ref"])
    v = c["feitos"] / c["prev"]
    ch.append(f'        <text x="36" y="{y + 16}" font-size="11"><tspan>{escape(textwrap.shorten(a["ativ"], 40, placeholder="…"))}</tspan></text>')
    ch.append(f'        <rect class="bar {"f1" if c["atras"] == 0 else "f3"}" data-k="{k}" x="{X0}" y="{y + 5}" width="{max(px(v) - X0, 2):.1f}" height="{RH - 10}"/>')
    ch.append(f'        <text class="b on" x="{px(v) - 6:.1f}" y="{y + 16}" font-size="10"{END}{TNUM}>{c["feitos"]} de {c["prev"]}</text>')
    hits.append(f'        <rect class="hit" x="14" y="{y}" width="872" height="{RH}" tabindex="0" role="img" aria-label="{escape(a["ativ"])}: {c["feitos"]} de {c["prev"]} feitas" '
                f'data-k="{k}" data-n="{escape(a["ativ"])}" data-s="{v * 100:.0f} %" data-d="{c["feitos"]} de {c["prev"]} feitas" data-p="{escape(a["resp"])}" data-cx="{px(v):.1f}" data-cy="{y}"/>')
ch += hits + ["      </svg>"]
tb = ['        <table class="aud">', '          <thead><tr><th>Atividade</th><th>Responsável</th><th class="c">Previstas</th><th class="c">Feitas</th><th class="c">Atrasadas</th></tr></thead>', '          <tbody>']
for row in rows_c:
    if row[0] == "a":
        a, ex = row[1], row[2]
        c = cal_conta(a, ex["head"]["ref"])
        tb.append(f'            <tr><td>{escape(a["ativ"])}</td><td>{escape(a["resp"])}</td><td class="c">{c["prev"]}</td><td class="c">{c["feitos"]}</td><td class="c">{c["atras"]}</td></tr>')
tb += ['          </tbody>', '        </table>']

# ------------------------------------------------------------------ módulo 5: tabela das frequências dos 34 estudos
fq = ['  <div class="tbl">', '    <table>', '      <thead><tr><th style="width:30%">Estudo</th><th style="width:16%">Ritmo</th><th>O que se faz</th></tr></thead>', '      <tbody>']
for g in GRUPOS:
    fq.append(f'        <tr><td colspan="3"><span class="eyebrow" style="margin:0">{escape(g)}</span></td></tr>')
    for e in ESTUDOS:
        if e[2] == g:
            fq.append(f'        <tr><td><a href="../{e[3]}"><strong>{escape(e[1])}</strong></a></td><td>{e[5]}</td><td>{escape(e[4])}</td></tr>')
fq += ['      </tbody>', '    </table>', '  </div>']

# ------------------------------------------------------------------ módulo 10: figura da ISO
ISOP = [("4.4 · Processos", "Determinar os processos do sistema, a sequência e as interações entre eles.", "o fio entre os estudos"),
        ("9.1.1 · Monitorar", "Decidir o que monitorar e medir, como, quando, e quando analisar os resultados.", "o calendário do ano"),
        ("9.3 · Análise crítica", "A direção recebe as entradas de todo o sistema e decide melhorias, mudanças e recursos.", "o fim de cada fio"),
        ("10.3 · Melhorar", "Melhorar continuamente o sistema, usando as análises e as decisões da direção.", "o próximo fio")]
iso = ['      <svg viewBox="0 0 900 200" role="img" aria-label="O que a norma pede sobre o sistema como um todo. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in ISOP) + '">']
for k, (a, b, c) in enumerate(ISOP):
    x = 10 + k * 222
    iso.append(f'        <rect class="bx" x="{x}" y="14" width="214" height="172"/>')
    iso.append(f'        <rect class="hd-ink" x="{x}" y="14" width="214" height="34"/>')
    iso.append(f'        <text class="b t-ground" x="{x + 12}" y="36" font-size="11.5">{escape(a)}</text>')
    lines(iso, b, x + 12, 70, 32, fs=11.5, step=16, maxl=5)
    lines(iso, "Neste estudo: " + c, x + 12, 160, 34, fs=11, cls="mu", step=15, maxl=2)
iso.append("      </svg>")

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))
perg = "\n".join(f'        <tr><td><strong>{escape(a)}</strong></td><td>{escape(b)}</td><td>{escape(c)}</td></tr>' for a, b, c in PERGUNTAS)

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--FIO-->", raias(EX2, "f1")), ("<!--FLUXO-->", "\n".join(et)), ("<!--CADEIA-->", "\n".join(ca)), ("<!--PERGUNTAS-->", perg),
                 ("<!--RITMOS-->", "\n".join(ri)), ("<!--FREQ-->", "\n".join(fq)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1RASTRO-->", rastro_tab(EX1)), ("<!--EX1FIO-->", raias(EX1, "f5")), ("<!--EX1CAL-->", calendario(EX1)),
                 ("<!--EX1CALTAB-->", cal_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2RASTRO-->", rastro_tab(EX2)), ("<!--EX2CAL-->", calendario(EX2)), ("<!--EX2CALTAB-->", cal_tab(EX2)),
                 ("<!--EX3FIG-->", "\n".join(de)), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Caso integrado</title>")
assert "Caso integrado" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", resumo(EX1), "| indústria", resumo(EX2))
