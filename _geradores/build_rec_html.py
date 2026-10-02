# -*- coding: utf-8 -*-
"""Monta treinamento-recursos.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rec_data import (ALTA, ATRAS, BLOCOS, CAMARA, CHECK, CORR, DENTRO, EMDIA, ETAPAS, EX1, EX2, FALTA, FATOR_EX, FATORES, FOLGA, FORA, JANELA,  # noqa: E402
                      JUSTO, POR_ENTREGADOR, SEMMED, SEMPLANO, SEXTA, SIM, VENCE, amb_conf, amb_sit, cap_conf, cap_sit, disp, infra_conf, limite, mtbf, mttr,
                      necessarias, num, oc_conf, paradas, prev_sit, proxima, resumo)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# em dia, vence em breve e atrasado: a mesma paleta de três cores do estudo de Calibração, validada para daltonismo nos dois modos
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


def dt(d, ano=True):
    return d.strftime("%d/%m/%Y" if ano else "%d/%m") if d else "—"


def pc(v, casas=1):
    return "—" if v is None else f"{v * 100:.{casas}f} %".replace(".", ",")


def h1(v):
    return "—" if v is None else f"{v:.1f}".replace(".", ",").replace(",0", "")


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


W5, G5 = 164, 14
HD3 = ["hd-p", "hd-d", "hd-c"]
BX3 = ["bx-p", "bx-d", "bx-c"]

# ------------------------------------------------------------------ figura 1: os três blocos de recursos
bl = ['      <svg viewBox="0 0 900 236" role="img" aria-label="O que o processo precisa para funcionar. ' + " ".join(f"{t}, requisito {n}: {d}" for n, t, d in BLOCOS)
      + ' Os três sustentam o processo, que transforma as entradas em produto conforme.">', "        <defs>" + marker("a0") + "</defs>"]
for k, (n, t, d) in enumerate(BLOCOS):
    x = 12 + k * 296
    bl.append(f'        <rect class="{BX3[k]}" x="{x}" y="14" width="284" height="112"/>')
    bl.append(f'        <rect class="{HD3[k]}" x="{x}" y="14" width="284" height="32"/>')
    bl.append(f'        <text class="b on" x="{x + 12}" y="35" font-size="12.5">{escape(t)}</text>')
    bl.append(f'        <text class="mono on" x="{x + 272}" y="34" font-size="10" text-anchor="end">{escape(n)}</text>')
    lines(bl, d, x + 12, 66, 44, fs=11, step=15, maxl=3)
    bl.append(f'        <line class="ln" x1="{x + 142}" y1="127" x2="{x + 142}" y2="150" marker-end="url(#a0)"/>')
bl.append('        <rect class="bx-ink" x="12" y="154" width="876" height="44"/>')
bl.append('        <text class="b t-ground" x="450" y="181" font-size="12.5" text-anchor="middle">O processo: transforma as entradas em produto conforme, todos os dias, também no pico.</text>')
bl.append('        <text class="mu" x="450" y="224" font-size="11" text-anchor="middle">Sem gente suficiente, sem equipamento funcionando ou num ambiente fora do limite, o mesmo processo produz outro resultado.</text>')
bl.append("      </svg>")

# ------------------------------------------------------------------ figura 2: as cinco etapas
et = ['      <svg viewBox="0 0 900 236" role="img" aria-label="As cinco etapas do trabalho. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS)
      + ' O que a leitura mostra volta ao dimensionamento, à manutenção e ao controle do ambiente.">',
      "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
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
xa, xb = 12 + 4 * (W5 + G5) + W5 / 2, 12 + (W5 + G5) + W5 / 2
et.append(f'        <path class="ln-mu dash" d="M{xa} 170 V198 H{xb} V174" marker-end="url(#a2m)"/>')
et.append(f'        <text class="mu halo" x="{(xa + xb) / 2}" y="202" font-size="11" text-anchor="middle">o que a leitura mostra muda a escala, o plano de manutenção e o controle</text>')
et.append('        <text x="450" y="228" font-size="11.5" text-anchor="middle">A etapa escura é a que fecha o ciclo: a falta de gente, a parada e o ambiente fora viram ação.</text>')
et.append("      </svg>")

# ------------------------------------------------------------------ figura 3: a sexta-feira da pizzaria
YMAX = 35
X0, X1, YT, YB = 120, 860, 44, 214
sy = lambda v: YB - v * (YB - YT) / YMAX  # noqa: E731
SW = (X1 - X0) / len(SEXTA)
sx = ['      <svg viewBox="0 0 900 270" role="img" aria-label="Entregas pedidas por hora na sexta-feira 16/04/2027 e a capacidade da escala, de '
      f'{POR_ENTREGADOR} entregas por entregador por hora. '
      + " ".join(f"{h}: {d} entregas pedidas, {e} entregadores, capacidade de {e * POR_ENTREGADOR}." for h, d, e in SEXTA)
      + ' Às 20h e às 21h, os pedidos passam da capacidade.">', '        <g font-size="11.5">',
      '          <rect class="f1" x="120" y="12" width="14" height="14"/><text x="142" y="24">Dentro da capacidade</text>',
      '          <rect class="f3" x="300" y="12" width="14" height="14"/><text x="322" y="24">Acima da capacidade</text>',
      '          <line class="ln-bold" x1="480" y1="19" x2="508" y2="19"/><text x="516" y="24">Capacidade da escala</text>',
      '        </g>']
for v in range(0, YMAX + 1, 5):
    sx.append(f'        <line class="grid" x1="{X0}" y1="{sy(v):.1f}" x2="{X1}" y2="{sy(v):.1f}"/>')
    sx.append(f'        <text class="mu" x="{X0 - 10}" y="{sy(v) + 4:.1f}" font-size="11" text-anchor="end"{TNUM}>{v}</text>')
sx.append(f'        <text class="mono mu" x="20" y="{(YT + YB) / 2}" font-size="10">ENTREGAS</text><text class="mono mu" x="20" y="{(YT + YB) / 2 + 14}" font-size="10">POR HORA</text>')
pts = []
for k, (h, d, e) in enumerate(SEXTA):
    cap = e * POR_ENTREGADOR
    x = X0 + k * SW
    cls = "f3" if d > cap else "f1"
    sx.append(f'        <rect class="{cls}" x="{x + SW * .22:.1f}" y="{sy(d):.1f}" width="{SW * .56:.1f}" height="{YB - sy(d):.1f}"/>')
    sx.append(f'        <text class="b halo" x="{x + SW / 2:.1f}" y="{sy(d) - 8:.1f}" font-size="11.5" text-anchor="middle"{TNUM}>{d}</text>')
    sx.append(f'        <text class="mu" x="{x + SW / 2:.1f}" y="{YB + 18}" font-size="11" text-anchor="middle">{h} · {e} entregadores</text>')
    pts += [(x, sy(cap)), (x + SW, sy(cap))]
sx.append('        <path class="ln-bold" d="M' + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts) + '"/>')
sx.append(f'        <line class="ln" x1="{X0}" y1="{YB}" x2="{X1}" y2="{YB}"/>')
pk = max(SEXTA, key=lambda r: r[1])
sx.append(f'        <text class="mu halo" x="{X0 + 2 * SW - 8:.1f}" y="{sy(pk[2] * POR_ENTREGADOR) + 4:.1f}" font-size="10.5" text-anchor="end">capacidade no pico: {pk[2] * POR_ENTREGADOR}</text>')
sx.append(f'        <text x="450" y="258" font-size="11.5" text-anchor="middle">No pico, {pk[1]} entregas por hora pedem {-(-pk[1] // POR_ENTREGADOR)} entregadores. A escala tinha {pk[2]}: o atraso já estava na escala.</text>')
sx.append("      </svg>")

# ------------------------------------------------------------------ figura 4: um mês da extrusora 3
E3 = next(i for i in EX2["infra"] if i["cod"] == "EXT-03")
H2 = EX2["head"]
OC3 = [o for o in EX2["ocs"] if o["cod"] == "EXT-03" and o["tipo"] == CORR and H2["ini"] <= o["data"] <= H2["fim"]]
INICIO = {6: 8, 18: 2, 27: 15}  # hora em que cada parada começou, só para o desenho
q3, hp3 = paradas(E3, EX2["ocs"], H2["ini"], H2["fim"])
TX0, TX1 = 40, 860
td = lambda dia, hora=0: TX0 + ((dia - 1) + hora / 24) * (TX1 - TX0) / 31  # noqa: E731
tl_ = ['      <svg viewBox="0 0 900 262" role="img" aria-label="Um mês da extrusora 3, em julho de 2027: '
       f'{E3["prog"]} horas programadas e {q3} quebras, que somam {num(hp3)} horas paradas: '
       + ", ".join(f'{dt(o["data"], False)}, {num(o["horas"])} horas' for o in OC3)
       + f'. Disponibilidade de {pc(disp(E3, EX2["ocs"], H2["ini"], H2["fim"]))}, contra a meta de {pc(H2["meta"], 0)}. '
       f'Tempo médio entre quebras de {h1(mtbf(E3, EX2["ocs"], H2["ini"], H2["fim"]))} horas e tempo médio de reparo de {h1(mttr(E3, EX2["ocs"], H2["ini"], H2["fim"]))} horas.">']
tl_.append(f'        <rect class="f1" x="{TX0}" y="56" width="{TX1 - TX0}" height="34"/>')
for o in OC3:
    d0 = o["data"].day
    a, b = td(d0, INICIO[d0]), td(d0, INICIO[d0] + o["horas"])
    tl_.append(f'        <rect class="f3 gap2" x="{a:.1f}" y="50" width="{b - a:.1f}" height="46"/>')
    tl_.append(f'        <text class="b halo" x="{(a + b) / 2:.1f}" y="40" font-size="11" text-anchor="middle">{dt(o["data"], False)} · {num(o["horas"])} h</text>')
for dia in (1, 8, 15, 22, 29):
    tl_.append(f'        <line class="grid" x1="{td(dia):.1f}" y1="96" x2="{td(dia):.1f}" y2="104"/>')
    tl_.append(f'        <text class="mu" x="{td(dia):.1f}" y="118" font-size="10.5" text-anchor="middle"{TNUM}>{dia:02d}/07</text>')
tl_.append(f'        <line class="grid" x1="{TX1}" y1="96" x2="{TX1}" y2="104"/>')
STATS = [("Disponibilidade", pc(disp(E3, EX2["ocs"], H2["ini"], H2["fim"])), f'({E3["prog"]} − {num(hp3)}) ÷ {E3["prog"]}. Meta: {pc(H2["meta"], 0)}.', "bx-s3"),
         ("Tempo médio entre quebras", f'{h1(mtbf(E3, EX2["ocs"], H2["ini"], H2["fim"]))} h', f'{E3["prog"] - hp3} horas funcionando ÷ {q3} quebras.', "bx"),
         ("Tempo médio de reparo", f'{h1(mttr(E3, EX2["ocs"], H2["ini"], H2["fim"]))} h', f'{num(hp3)} horas paradas ÷ {q3} quebras.', "bx")]
for k, (t, v, d, c) in enumerate(STATS):
    x = 40 + k * 280
    tl_.append(f'        <rect class="{c}" x="{x}" y="136" width="260" height="84"/>')
    tl_.append(f'        <text class="mono mu" x="{x + 14}" y="156" font-size="9.5">{escape(t.upper())}</text>')
    tl_.append(f'        <text class="disp" x="{x + 14}" y="186" font-size="24"{TNUM}>{v}</text>')
    tl_.append(f'        <text class="mu" x="{x + 14}" y="208" font-size="10.5">{escape(d)}</text>')
tl_.append('        <text x="450" y="248" font-size="11.5" text-anchor="middle">As três quebras de julho vieram de peças que a preventiva atrasada teria trocado ou medido.</text>')
tl_.append("      </svg>")

# ------------------------------------------------------------------ figura 5: os fatores do ambiente
fa = ['      <svg viewBox="0 0 900 222" role="img" aria-label="Os fatores do ambiente, em três grupos. '
      + " ".join(f'{t}: {", ".join(FATOR_EX[t])}.' for t in FATORES) + ' Um fator entra no controle quando afeta o produto ou o serviço.">']
for k, t in enumerate(FATORES):
    x = 12 + k * 296
    fa.append(f'        <rect class="{BX3[k]}" x="{x}" y="14" width="284" height="160"/>')
    fa.append(f'        <rect class="{HD3[k]}" x="{x}" y="14" width="284" height="32"/>')
    fa.append(f'        <text class="b on" x="{x + 12}" y="35" font-size="12.5">{escape(t)}</text>')
    for j, it in enumerate(FATOR_EX[t]):
        fa.append(f'        <rect class="{HD3[k]}" x="{x + 14}" y="{67 + j * 27}" width="7" height="7"/>')
        fa.append(f'        <text x="{x + 30}" y="{74 + j * 27}" font-size="11.5">{escape(it)}</text>')
fa.append('        <text x="450" y="200" font-size="11.5" text-anchor="middle">A norma não pede conforto: pede o ambiente de que o processo precisa para o produto sair conforme.</text>')
fa.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Responsável</dt><dd>{escape(h["resp"])}</dd></div>',
                      f'    <div><dt>Período</dt><dd>{dt(h["ini"])} a {dt(h["fim"])}. Meta de disponibilidade: {pc(h["meta"], 0)}.</dd></div>',
                      f'    <div><dt>Horas programadas</dt><dd>{escape(h["horario"])}</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      '  </dl>'])


def tabela(caption, heads, rows):
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{caption}</caption>', f'      <thead><tr>{"".join(heads)}</tr></thead>', '      <tbody>']
    o += [f'        <tr>{r}</tr>' for r in rows]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def chip(c, ok=("OK",), neutro=()):
    return f'<span class="chip {"s1" if c in ok else "sl" if c in neutro else "s3"}">{escape(c)}</span>'


CAP_CLS = {FALTA: "s3", JUSTO: "s2", FOLGA: "s1"}
PREV_CLS = {EMDIA: "s1", VENCE: "s2", ATRAS: "s3", SEMPLANO: "sl"}
AMB_CLS = {DENTRO: "s1", FORA: "s3", SEMMED: "s2"}


def per(m):
    return "todo mês" if m == 1 else "uma vez por ano" if m == 12 else f"a cada {m} meses"


def cap_tab(ex):
    r = resumo(ex)
    rows = []
    for c in ex["caps"]:
        s = cap_sit(c)
        rows.append(f'<td><strong>{escape(c["funcao"])}</strong><small>{escape(c["periodo"])}</small></td><td class="c">{num(c["dem"])}<small>{escape(c["unid"])}</small></td>'
                    f'<td class="c">{num(c["prod"])}<small>por pessoa</small></td><td class="c"><strong>{necessarias(c)}</strong></td><td class="c{" no" if s == FALTA else ""}">{c["esc"]}</td>'
                    f'<td class="c{" no" if c["qual"] == 0 else ""}">{c["qual"]}</td><td><span class="chip {CAP_CLS[s]}">{s}</span></td><td>{chip(cap_conf(c))}</td>')
    return tabela(f'Pessoas no pico · {r["caps"]} funções e períodos, {r["cap_falta"]} com falta de gente: {r["pessoas"]} pessoa{"s" if r["pessoas"] != 1 else ""} a menos',
                  ['<th style="width:22%">Função<small>Período</small></th>', '<th class="c">Demanda no pico</th>', '<th class="c">Produtividade</th>', '<th class="c">Necessárias</th>',
                   '<th class="c">Escaladas</th>', '<th class="c">Qualificadas</th>', '<th>Situação</th>', '<th>Conferência</th>'], rows)


def infra_tab(ex):
    h, r = ex["head"], resumo(ex)
    rows = []
    for i in ex["infra"]:
        s = prev_sit(i, h["ref"])
        q, hp = paradas(i, ex["ocs"], h["ini"], h["fim"])
        d = disp(i, ex["ocs"], h["ini"], h["fim"])
        prev = f'{per(i["interv"])}<small>última: {dt(i["ultima"])}</small>' if i["interv"] else '—<small>sem preventiva</small>'
        dd = f'{pc(d)}<small>{q} quebra{"s" if q != 1 else ""} · {num(hp)} h</small>' if d is not None else "—"
        sem_cont = ' class="no"' if i["crit"] == ALTA and not i["cont"] else ""
        rows.append(f'<td class="n">{i["cod"]}</td><td><strong>{escape(i["nome"])}</strong><small>{escape(i["tipo"])} · {escape(i["local"])}</small></td><td>{i["crit"]}</td>'
                    f'<td>{prev}</td><td class="c">{dt(proxima(i))}</td><td><span class="chip {PREV_CLS[s]}">{s}</span></td>'
                    f'<td{sem_cont}>{escape(i["cont"]) or "—"}</td>'
                    f'<td class="c{" no" if d is not None and d < h["meta"] - 1e-9 else ""}">{dd}</td><td>{chip(infra_conf(i, ex))}</td>')
    sits = r["sits"]
    return tabela(f'Infraestrutura · {r["infra"]} itens, {r["criticos"]} críticos. Preventivas: {sits[EMDIA]} em dia, {sits[VENCE]} vencem em {JANELA} dias, '
                  f'{sits[ATRAS]} atrasada{"s" if sits[ATRAS] != 1 else ""}, {sits[SEMPLANO]} sem plano',
                  ['<th>Código</th>', '<th style="width:20%">Item<small>Tipo · local</small></th>', '<th>Criticidade</th>', '<th style="width:12%">Preventiva</th>', '<th class="c">Próxima</th>',
                   '<th>Situação</th>', '<th style="width:22%">Contingência</th>', '<th class="c">Disponibilidade<small>Quebras · horas paradas</small></th>', '<th>Conferência</th>'], rows)


def oc_tab(ex):
    h, r = ex["head"], resumo(ex)
    rows = []
    for o in sorted(ex["ocs"], key=lambda o: o["data"]):
        fora = not (h["ini"] <= o["data"] <= h["fim"])
        prod = "—" if o["tipo"] != CORR else (f'Sim<small>{escape(o["trat"]) or "sem tratamento registrado"}</small>' if o["afetou"] == SIM else "Não")
        acao = escape(o["acao"]) or "—"
        causa = f'<small>Causa: {escape(o["causa"])}</small>' if o["causa"] else ("<small>Causa: não registrada</small>" if o["tipo"] == CORR else "")
        sem_trat = ' class="no"' if o["afetou"] == SIM and not o["trat"] else ""
        rows.append(f'<td class="c">{dt(o["data"], False)}{"<small>fora do período</small>" if fora else ""}</td><td class="n">{o["cod"]}</td><td>{o["tipo"]}</td>'
                    f'<td class="c">{num(o["horas"])} h</td><td>{escape(o["oque"])}{causa}</td>'
                    f'<td>{acao}</td><td{sem_trat}>{prod}</td><td>{chip(oc_conf(o, ex["infra"]))}</td>')
    return tabela(f'Manutenções · {r["ocs"]} registros. No período, {r["corr"]} corretivas, {num(r["horas"])} horas paradas, {r["afetou"]} com produto afetado',
                  ['<th class="c">Data</th>', '<th>Código</th>', '<th>Tipo</th>', '<th class="c">Parado</th>', '<th style="width:26%">O que aconteceu<small>Causa</small></th>',
                   '<th style="width:22%">Ação</th>', '<th style="width:16%">Produto afetado<small>Tratamento</small></th>', '<th>Conferência</th>'], rows)


def amb_tab(ex):
    r = resumo(ex)
    rows = []
    for a in ex["amb"]:
        s = amb_sit(a)
        med = f'{num(a["valor"])} {a["unid"]}' if a["valor"] is not None else "—"
        rows.append(f'<td><strong>{escape(a["fator"])}</strong><small>{a["tipo"]} · {escape(a["local"])}</small></td><td>{escape(a["porque"])}</td><td>{escape(limite(a))}</td>'
                    f'<td>{escape(a["controle"])}</td><td class="c{" no" if s == FORA else ""}">{med}</td><td><span class="chip {AMB_CLS[s]}">{s}</span></td>'
                    f'<td>{escape(a["acao"]) or "—"}</td><td>{chip(amb_conf(a))}</td>')
    return tabela(f'Ambiente · {r["amb"]} fatores, {r["fora"]} fora do limite, {r["semmed"]} sem medição',
                  ['<th style="width:16%">Fator<small>Tipo · local</small></th>', '<th style="width:20%">Por que afeta o produto</th>', '<th>Limite</th>', '<th style="width:16%">Controle</th>',
                   '<th class="c">Medido</th>', '<th>Situação</th>', '<th style="width:18%">Ação</th>', '<th>Conferência</th>'], rows)


# ------------------------------------------------------------------ exemplo 3: a quebra da câmara fria
HCLS = ["bx-s2", "bx-s3", "bx", "bx-s1", "bx-ink"]
im = ['      <svg viewBox="0 0 900 222" role="img" aria-label="A quebra da câmara fria da pizzaria. ' + " ".join(f"{a}, {b}: {c}" for a, b, c in CAMARA) + '">',
      "        <defs>" + marker("a5") + "</defs>"]
for k, (quando, tit, txt) in enumerate(CAMARA):
    x = 12 + k * (W5 + G5)
    ink = k == 4
    im.append(f'        <rect class="{HCLS[k]}" x="{x}" y="14" width="{W5}" height="168"/>')
    im.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="34" font-size="9.5">{escape(quando.upper())}</text>')
    tl = textwrap.wrap(tit, 22)
    for j, l in enumerate(tl):
        im.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{54 + j * 15}" font-size="12">{escape(l)}</text>')
    lines(im, txt, x + 12, 76 if len(tl) == 1 else 90, 25, fs=10.5, cls="t-ground" if ink else "", step=14, maxl=7)
    if k < 4:
        im.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="96" x2="{x + W5 + G5 - 2}" y2="96" marker-end="url(#a5)"/>')
im.append('        <text x="450" y="210" font-size="11.5" text-anchor="middle">A contingência funcionou porque alguém improvisou bem. Escrita, ela funciona em qualquer turno.</text>')
im.append("      </svg>")

# ------------------------------------------------------------------ módulo 8: disponibilidade, nos dois exemplos
VMIN, VMAX = 0.90, 1.0
X0, X1, TOP, RH = 330, 860, 46, 26
vx = lambda v: X0 + (max(VMIN, v) - VMIN) * (X1 - X0) / (VMAX - VMIN)  # noqa: E731
rows_c = []
for nome, ex in (("PIZZARIA", EX1), ("INDÚSTRIA", EX2)):
    rows_c.append(("grupo", nome, ex))
    for i in ex["infra"]:
        if i["prog"]:
            rows_c.append(("item", i, ex))
bottom = TOP + RH * len(rows_c)


def _d(i, ex):
    h = ex["head"]
    return disp(i, ex["ocs"], h["ini"], h["fim"])


ch = [f'      <svg id="bars" viewBox="0 0 900 {bottom + 44}" role="img" aria-label="Disponibilidade de cada item com horas programadas, no mês de cada exemplo. Meta de '
      f'{pc(EX1["head"]["meta"], 0)} na pizzaria e de {pc(EX2["head"]["meta"], 0)} na indústria. '
      + " ".join(f'{r[1]["cod"]}: {pc(_d(r[1], r[2]))}.' for r in rows_c if r[0] == "item") + '">', '        <g font-size="11.5">']
for k, (t, cls) in enumerate((("Na meta ou acima", "f1"), ("Abaixo da meta", "f3"))):
    ch.append(f'          <rect class="{cls}" x="{X0 + k * 180}" y="12" width="14" height="14"/><text x="{X0 + 22 + k * 180}" y="24">{t}</text>')
ch.append(f'          <line class="goal" x1="{X0 + 360}" y1="19" x2="{X0 + 388}" y2="19"/><text x="{X0 + 396}" y="24">Meta</text>')
ch.append('        </g>')
for p in range(90, 101, 2):
    ch.append(f'        <line class="grid" x1="{vx(p / 100):.1f}" y1="{TOP - 6}" x2="{vx(p / 100):.1f}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{vx(p / 100):.1f}" y="{bottom + 16}" font-size="11" text-anchor="middle"{TNUM}>{p} %</text>')
ch.append(f'        <text class="mono mu" x="{(X0 + X1) / 2}" y="{bottom + 36}" font-size="10" text-anchor="middle">DISPONIBILIDADE NO MÊS · O EIXO COMEÇA EM 90 %</text>')
hits = []
grp0 = None
for k, row in enumerate(rows_c):
    y = TOP + RH * k
    if row[0] == "grupo":
        ch.append(f'        <text class="mono mu" x="20" y="{y + 17}" font-size="10">{row[1]}</text>')
        if grp0 is not None:
            ch.append(grp0(y))
        meta = row[2]["head"]["meta"]
        y0 = y + RH
        grp0 = (lambda m, a: (lambda b: f'        <line class="goal" x1="{vx(m):.1f}" y1="{a + 2}" x2="{vx(m):.1f}" y2="{b - 2}"/>'))(meta, y0)
        continue
    i, ex = row[1], row[2]
    h = ex["head"]
    d = _d(i, ex)
    q, hp = paradas(i, ex["ocs"], h["ini"], h["fim"])
    cls = "f3" if d < h["meta"] - 1e-9 else "f1"
    ch.append(f'        <text x="36" y="{y + 17}" font-size="11.5"><tspan class="b">{i["cod"]}</tspan><tspan class="mu" dx="8">{escape(textwrap.shorten(i["nome"], 34, placeholder="…"))}</tspan></text>')
    ch.append(f'        <rect class="bar {cls}" data-k="{k}" x="{X0}" y="{y + 6}" width="{max(vx(d) - X0, 2):.1f}" height="{RH - 12}"/>')
    # rótulo dentro da barra, para não cruzar a linha da meta
    ch.append(f'        <text class="b on" x="{vx(d) - 6:.1f}" y="{y + 17}" font-size="10.5" text-anchor="end"{TNUM}>{pc(d)}</text>')
    paro = f'{q} quebra{"s" if q != 1 else ""}, {num(hp)} h parado' if q else "sem quebras"
    hits.append(f'        <rect class="hit" x="14" y="{y}" width="872" height="{RH}" tabindex="0" role="img" aria-label="{i["cod"]}, {escape(i["nome"])}: {pc(d)}, {paro}" '
                f'data-k="{k}" data-n="{i["cod"]} · {escape(i["nome"])}" data-s="{pc(d)}" data-p="meta de {pc(h["meta"], 0)}" data-d="{paro}" data-cx="{vx(d):.1f}" data-cy="{y}"/>')
ch.append(grp0(bottom))
ch += hits + ["      </svg>"]
tb = ['        <table class="aud">', '          <thead><tr><th>Código</th><th>Item</th><th class="c">Programadas</th><th class="c">Quebras</th><th class="c">Horas paradas</th>'
      '<th class="c">Disponibilidade</th><th class="c">Meta</th></tr></thead>', '          <tbody>']
for row in rows_c:
    if row[0] == "item":
        i, ex = row[1], row[2]
        h = ex["head"]
        q, hp = paradas(i, ex["ocs"], h["ini"], h["fim"])
        tb.append(f'            <tr><td>{i["cod"]}</td><td>{escape(i["nome"])}</td><td class="c">{i["prog"]} h</td><td class="c">{q}</td><td class="c">{num(hp)} h</td>'
                  f'<td class="c">{pc(_d(i, ex))}</td><td class="c">{pc(h["meta"], 0)}</td></tr>')
tb += ['          </tbody>', '        </table>']

# ------------------------------------------------------------------ módulo 11: figura da ISO
ISOP = [("7.1.1 · Recursos", "Determinar e prover os recursos do sistema, pensando no que existe dentro e no que precisa vir de fora.", "a demanda e a escala"),
        ("7.1.2 · Pessoas", "Determinar e prover as pessoas necessárias para operar os processos e o sistema.", "as pessoas no pico"),
        ("7.1.3 · Infraestrutura", "Determinar, prover e manter prédios, equipamentos, transporte e tecnologia da informação.", "a preventiva e a contingência"),
        ("7.1.4 · Ambiente", "Determinar, prover e manter o ambiente necessário: fatores físicos, sociais e psicológicos.", "os fatores com limite")]
iso = ['      <svg viewBox="0 0 900 200" role="img" aria-label="O que a norma pede sobre recursos, infraestrutura e ambiente. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in ISOP) + '">']
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
for tag, val in (("<!--BLOCOS-->", "\n".join(bl)), ("<!--FLUXO-->", "\n".join(et)), ("<!--SEXTA-->", "\n".join(sx)), ("<!--EXT3-->", "\n".join(tl_)), ("<!--FATORES-->", "\n".join(fa)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1CAP-->", cap_tab(EX1)), ("<!--EX1INFRA-->", infra_tab(EX1)), ("<!--EX1OC-->", oc_tab(EX1)), ("<!--EX1AMB-->", amb_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2CAP-->", cap_tab(EX2)), ("<!--EX2INFRA-->", infra_tab(EX2)), ("<!--EX2OC-->", oc_tab(EX2)), ("<!--EX2AMB-->", amb_tab(EX2)),
                 ("<!--EX3FIG-->", "\n".join(im)), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Recursos, infraestrutura e ambiente</title>")
assert "Recursos" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", resumo(EX1), "| indústria", resumo(EX2))
