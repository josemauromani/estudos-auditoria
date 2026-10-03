# -*- coding: utf-8 -*-
"""Monta treinamento-certificacao.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from datetime import date
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cert_data import (ABERTA, AGUARDA, ATRASADA, CADEIA, CHECK, CONSIDERAR, CRITERIOS, E2015, ETAPAS, EVENTOS, EX1, EX2, FASES, FECHADA, FIM_TRANSICAO,  # noqa: E402
                       FORAPRAZO, MAIOR, MAIOR_DIAS, MAIOR_FIO, MENOR, NA, NAOPRONTA, NOPRAZO, OM, PLANO_DIAS, PLANOATR, PONTO, PREVISTA, PRONTA1, PRONTA2,
                       PUBLICACAO, REALIZADA, TRANSICAO, TRATAR, VENCE, VENCIDA, ct_conf, ct_sit, evento_sit, limites, prazo_fech, prazo_plano, pront_conf,
                       pront_res, resumo, validade)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# em dia, perto do prazo e atrasado: a mesma paleta de três cores do estudo de Calibração, validada para daltonismo nos dois modos
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
W5, G5 = 164, 14


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


def cinco(o, itens, classes, mk, y0=16, h=140, rotulo=None, maxd=5, mid=None, wrap_d=25):
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
        lines(o, desc, x + 12, yt + 15 * len(tl) + 8, wrap_d, cls="t-ground" if ink else "", step=14.5, maxl=maxd)
        if k < len(itens) - 1:
            ym = mid or (y0 + h / 2)
            o.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="{ym}" x2="{x + W5 + G5 - 2}" y2="{ym}" marker-end="url(#{mk})"/>')
    return xs


# ------------------------------------------------------------------ figura 1: o ciclo de três anos
X0, X1 = 230, 860
mx = lambda m: X0 + m * (X1 - X0) / 36 if m >= 0 else X0 + m * 40  # noqa: E731  antes da decisão, os meses ganham mais espaço
MARCOS = [(-3, "Fase 1", "prontidão", "f2"), (-1.5, "Fase 2", "no local", "f2"), (0, "Decisão", "certificado emitido", "f1"), (12, "1ª manutenção", "até 12 meses", "f1"),
          (24, "2ª manutenção", "até 24 meses", "f1"), (33, "Recertificação", "antes de vencer", "f3")]
ci = ['      <svg viewBox="0 0 900 230" role="img" aria-label="O ciclo do certificado em três anos. Antes da decisão, a fase 1 e a fase 2. Depois da decisão, o certificado vale três anos, '
      'com uma auditoria de manutenção a cada ano e a auditoria de recertificação antes do vencimento, para que um novo ciclo comece sem interrupção.">']
ci.append(f'        <rect class="bx-s1" x="{mx(0):.1f}" y="92" width="{mx(36) - mx(0):.1f}" height="26"/>')
ci.append(f'        <text class="b" x="{(mx(0) + mx(36)) / 2:.1f}" y="110" font-size="12"{MID}>Certificado válido por três anos</text>')
for a in range(0, 37, 12):
    ci.append(f'        <line class="grid" x1="{mx(a):.1f}" y1="84" x2="{mx(a):.1f}" y2="130"/>')
    ci.append(f'        <text class="mono mu" x="{mx(a):.1f}" y="146" font-size="10"{MID}>{a} MESES</text>')
for k, (m, t, s, cls) in enumerate(MARCOS):
    x = mx(m)
    y = 46 if k % 2 == 0 else 176
    ci.append(f'        <line class="ln-mu" x1="{x:.1f}" y1="{62 if y < 100 else 120}" x2="{x:.1f}" y2="{90 if y < 100 else 160}"/>')
    ci.append(f'        <circle class="{cls}" cx="{x:.1f}" cy="{105}" r="7"/>')
    ci.append(f'        <text class="b" x="{x:.1f}" y="{y}" font-size="12"{MID}>{t}</text>')
    ci.append(f'        <text class="mu" x="{x:.1f}" y="{y + 15}" font-size="10.5"{MID}>{s}</text>')
ci.append(f'        <text x="450" y="220" font-size="11.5"{MID}>O certificado não termina na decisão: a cada ano o organismo volta, e a cada três o ciclo recomeça.</text>')
ci.append("      </svg>")

# ------------------------------------------------------------------ figura 2: as cinco etapas
et = ['      <svg viewBox="0 0 900 236" role="img" aria-label="As cinco etapas até o certificado. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS)
      + ' Depois da decisão, as auditorias de manutenção mantêm o ciclo.">', "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
xs = cinco(et, ETAPAS, ["bx", "bx-p", "bx-d", "bx-c", "bx-ink"], "a2", h=152, rotulo=lambda k: f"ETAPA {k + 1}", mid=84)
xa, xb = xs[4] + W5 / 2, xs[3] + W5 / 2
et.append(f'        <path class="ln-mu dash" d="M{xa} 170 V198 H{xb} V174" marker-end="url(#a2m)"/>')
et.append(f'        <text class="mu halo" x="{(xa + xb) / 2}" y="202" font-size="11"{MID}>manutenção anual</text>')
et.append(f'        <text x="450" y="228" font-size="11.5"{MID}>A primeira etapa é a mais longa, e é da organização. As outras quatro seguem o regulamento do organismo.</text>')
et.append("      </svg>")

# ------------------------------------------------------------------ figura 3: a cadeia de confiança
cc = ['      <svg viewBox="0 0 900 214" role="img" aria-label="A cadeia de confiança do certificado. ' + " ".join(f"{a}: {b}" for a, b in CADEIA) + '">',
      "        <defs>" + marker("a3") + "</defs>"]
cinco(cc, CADEIA, ["bx", "bx-p", "bx-d", "bx-c", "bx-ink"], "a3", h=136, maxd=5)
cc.append(f'        <text x="450" y="182" font-size="11.5"{MID}>Um certificado vale o que vale o organismo. Organismo sem acreditação emite papel, não confiança.</text>')
cc.append(f'        <text class="mu" x="450" y="202" font-size="11"{MID}>Confira a acreditação no site do acreditador, e se o escopo dela cobre o seu setor.</text>')
cc.append("      </svg>")

# ------------------------------------------------------------------ figura 4: as duas fases
fa = ['      <svg viewBox="0 0 900 236" role="img" aria-label="O que cada fase da auditoria inicial olha. ' + " ".join(f'{t}: {", ".join(l)}. {s}' for t, l, s in FASES) + '">',
      "        <defs>" + marker("a4") + "</defs>"]
for k, (t, l, s) in enumerate(FASES):
    x = 12 + k * 450
    cls, hd = ("bx-d", "hd-d") if k == 0 else ("bx-c", "hd-c")
    fa.append(f'        <rect class="{cls}" x="{x}" y="14" width="426" height="206"/>')
    fa.append(f'        <rect class="{hd}" x="{x}" y="14" width="426" height="34"/>')
    fa.append(f'        <text class="b on" x="{x + 14}" y="36" font-size="13">{t}</text>')
    fa.append(f'        <text class="on" x="{x + 412}" y="36" font-size="10.5"{END}>{"Está pronto?" if k == 0 else "Funciona e é eficaz?"}</text>')
    for j, it in enumerate(l):
        fa.append(f'        <rect class="{hd}" x="{x + 16}" y="{66 + j * 24}" width="7" height="7"/><text x="{x + 32}" y="{73 + j * 24}" font-size="11.5">{escape(it)}</text>')
    fa.append(f'        <text class="mu" x="{x + 16}" y="206" font-size="11">{escape(s)}</text>')
fa.append('        <line class="ln" x1="440" y1="117" x2="460" y2="117" marker-end="url(#a4)"/>')
fa.append("      </svg>")

# ------------------------------------------------------------------ figura 5: os prazos das constatações
PX0, PX1 = 160, 860
px = lambda d: PX0 + d * (PX1 - PX0) / 180  # noqa: E731
pz = ['      <svg viewBox="0 0 900 236" role="img" aria-label="Os prazos das constatações, na convenção deste material. Não conformidade maior: plano em até '
      f'{PLANO_DIAS} dias e fechamento com evidência aceita em até {MAIOR_DIAS} dias, antes da decisão. Se o organismo não conseguir verificar em até seis meses, a fase 2 é refeita. '
      f'Não conformidade menor: plano em até {PLANO_DIAS} dias, e a eficácia é verificada na auditoria seguinte.">']
for d in (0, 30, 60, 90, 120, 150, 180):
    pz.append(f'        <line class="grid" x1="{px(d):.1f}" y1="40" x2="{px(d):.1f}" y2="170"/>')
    pz.append(f'        <text class="mu" x="{px(d):.1f}" y="186" font-size="10.5"{MID}{TNUM}>{d}</text>')
pz.append(f'        <text class="mono mu" x="{(PX0 + PX1) / 2}" y="204" font-size="10"{MID}>DIAS DEPOIS DA AUDITORIA</text>')
for k, (t, cls, segs) in enumerate(((MAIOR, "f3", [(0, PLANO_DIAS, "plano"), (PLANO_DIAS, MAIOR_DIAS, "ação e evidência aceita")]),
                                   (MENOR, "f2", [(0, PLANO_DIAS, "plano"), (PLANO_DIAS, 180, "verificação na auditoria seguinte")]))):
    y = 56 + k * 62
    pz.append(f'        <text class="b" x="20" y="{y + 16}" font-size="12.5">{t}</text>')
    for j, (a, b, lab) in enumerate(segs):
        op = "" if j == 0 else ' fill-opacity=".55"'
        pz.append(f'        <rect class="{cls}" x="{px(a):.1f}" y="{y}" width="{px(b) - px(a) - 2:.1f}" height="26"{op}/>')
        pz.append(f'        <text class="b {"on" if j == 0 else ""}" x="{px(a) + 8:.1f}" y="{y + 17}" font-size="10.5">{lab}</text>')
pz.append(f'        <line class="now" x1="{px(180):.1f}" y1="40" x2="{px(180):.1f}" y2="170"/>')
pz.append(f'        <text class="mu halo" x="{px(180) - 6:.1f}" y="52" font-size="10.5"{END}>6 meses: maior sem verificar, refaz-se a fase 2</text>')
pz.append(f'        <text x="450" y="228" font-size="11.5"{MID}>Os prazos de 30 e 90 dias são uma convenção deste material, comum entre organismos. Vale o regulamento do seu.</text>')
pz.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h, c, r = ex["head"], ex["ciclo"], resumo(ex)
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Escopo</dt><dd>{escape(h["escopo"])}</dd></div>',
                      f'    <div><dt>Organismo</dt><dd>{escape(h["organismo"])}</dd></div>',
                      f'    <div><dt>Por que certificar</dt><dd>{escape(h["motivo"])}</dd></div>',
                      f'    <div><dt>Certificado</dt><dd>{c["edicao"]}, decisão em {dt(c["decisao"])}, válido até {dt(r["validade"])}.</dd></div>',
                      '  </dl>'])


def tabela(caption, heads, rows):
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{caption}</caption>', f'      <thead><tr>{"".join(heads)}</tr></thead>', '      <tbody>']
    o += [f'        <tr>{r}</tr>' for r in rows]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def chip(c, ok=("OK",)):
    return f'<span class="chip {"s1" if c in ok else "s3"}">{escape(c)}</span>'


ST_CLS = {"Sim": "s1", "Parcial": "s2", "Não": "s3"}
RES_CLS = {PRONTA2: "s1", PRONTA1: "s2", NAOPRONTA: "s3"}
EV_CLS = {REALIZADA: "s1", NOPRAZO: "s1", FORAPRAZO: "s3", PREVISTA: "sl", VENCE: "s2", ATRASADA: "s3", NA: "sl"}
CT_CLS = {FECHADA: "s1", PLANOATR: "s3", VENCIDA: "s3", AGUARDA: "s2", ABERTA: "s2", CONSIDERAR: "sl", TRATAR: "s2"}
TP_CLS = {MAIOR: "s3", MENOR: "s2", OM: "sl", PONTO: "sl"}


def pront_tab(ex):
    p = ex["pront"]
    res = pront_res(p["itens"])
    rows = []
    for k, (c, i) in enumerate(zip(CRITERIOS, p["itens"]), 1):
        imp = c[1] and i["status"] != "Sim"
        acao = f'{escape(i["acao"])}<small>{escape(i["resp"])} · até {dt(i["prazo"])}</small>' if i["acao"] else "—"
        rows.append(f'<td class="n">{k}</td><td>{escape(c[2])}<small>Antes da {c[0].lower()}{" · impeditivo" if c[1] else ""}</small></td>'
                    f'<td class="{"no" if imp else ""}"><span class="chip {ST_CLS[i["status"]]}">{i["status"]}</span></td><td>{escape(i["evid"]) or "—"}</td><td>{acao}</td>'
                    f'<td>{chip(pront_conf(c, i))}</td>')
    return tabela(f'Prontidão em {dt(p["data"])} · {res["pct"] * 100:.0f} % atendido, {res["imp1"]} impeditivo{"s" if res["imp1"] != 1 else ""} antes da fase 1 e '
                  f'{res["imp2"]} antes da fase 2 · <span class="chip {RES_CLS[res["res"]]}">{res["res"]}</span>',
                  ['<th>#</th>', '<th style="width:34%">Critério<small>Quando · impeditivo</small></th>', '<th>Status</th>', '<th style="width:22%">Evidência</th>',
                   '<th style="width:26%">Ação<small>Responsável · prazo</small></th>', '<th>Conferência</th>'], rows)


def ciclo_tab(ex):
    c = ex["ciclo"]
    rows = []
    for k, (ev, lim) in enumerate(zip(EVENTOS, limites(c))):
        s = evento_sit(c, k)
        rows.append(f'<td><strong>{ev}</strong></td><td class="c">{dt(lim)}</td><td class="c">{dt(c["feito"][k])}</td><td><span class="chip {EV_CLS[s]}">{s}</span></td>')
    return tabela(f'O ciclo do certificado · {c["edicao"]}, lido em {dt(c["ref"])}',
                  ['<th style="width:34%">Evento</th>', '<th class="c">Limite</th>', '<th class="c">Realizado em</th>', '<th>Situação</th>'], rows)


def ct_tab(ex):
    ref, r = ex["ciclo"]["ref"], resumo(ex)
    rows = []
    for x in ex["cts"]:
        s = ct_sit(x, ref)
        pr = f'plano até {dt(prazo_plano(x), False)}' if prazo_plano(x) else "sem prazo"
        if prazo_fech(x):
            pr += f' · fechar até {dt(prazo_fech(x), False)}'
        datas = " · ".join(f"{n} {dt(x[k], False)}" for n, k in (("plano", "plano"), ("ação", "concl"), ("evidência", "evid")) if x[k]) or "—"
        rows.append(f'<td class="n">{x["num"]}</td><td>{x["aud"]}<small>{dt(x["data"])}</small></td><td><span class="chip {TP_CLS[x["tipo"]]}">{x["tipo"]}</span></td>'
                    f'<td class="c">{x["req"]}</td><td>{escape(x["desc"])}</td><td>{datas}<small>{pr}</small></td><td><span class="chip {CT_CLS[s]}">{escape(s)}</span></td>'
                    f'<td>{chip(ct_conf(x))}</td>')
    t = r["tipos"]
    return tabela(f'Constatações do organismo · {t[MAIOR]} maior, {t[MENOR]} menores, {t[OM]} oportunidade, {t[PONTO]} ponto{"s" if t[PONTO] != 1 else ""} de atenção',
                  ['<th>Nº</th>', '<th>Auditoria</th>', '<th>Tipo</th>', '<th class="c">Requisito</th>', '<th style="width:30%">Constatação</th>', '<th style="width:18%">Datas<small>Prazos</small></th>',
                   '<th>Situação</th>', '<th>Conferência</th>'], rows)


# ------------------------------------------------------------------ exemplo 3: da maior à decisão
im = ['      <svg viewBox="0 0 900 214" role="img" aria-label="Da não conformidade maior à decisão de certificação, na indústria. ' + " ".join(f"{a}, {b}: {c}" for a, b, c in MAIOR_FIO) + '">',
      "        <defs>" + marker("a6") + "</defs>"]
for k, (quando, tit, txt) in enumerate(MAIOR_FIO):
    x = 12 + k * (W5 + G5)
    ink = k == 4
    im.append(f'        <rect class="{["bx-s3", "bx", "bx-d", "bx-s1", "bx-ink"][k]}" x="{x}" y="14" width="{W5}" height="164"/>')
    im.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="34" font-size="9.5">{quando}/2027</text>')
    im.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="54" font-size="12">{escape(tit)}</text>')
    lines(im, txt, x + 12, 76, 25, fs=10.5, cls="t-ground" if ink else "", step=14, maxl=7)
    if k < 4:
        im.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="96" x2="{x + W5 + G5 - 2}" y2="96" marker-end="url(#a6)"/>')
im.append(f'        <text x="450" y="204" font-size="11.5"{MID}>24 dias da constatação à decisão. A maior só não adiou o certificado porque a ação foi feita, e comprovada, a tempo.</text>')
im.append("      </svg>")

# ------------------------------------------------------------------ módulo 8: o ciclo dos dois certificados
G0, G1 = date(2027, 7, 1), date(2031, 7, 1)
GX0, GX1 = 200, 860
gx = lambda d: GX0 + (d - G0).days * (GX1 - GX0) / (G1 - G0).days  # noqa: E731
LAN = [("Indústria", EX2), ("Pizzaria", EX1)]
gt = [f'      <svg id="bars" viewBox="0 0 900 250" role="img" aria-label="Os dois certificados no tempo. '
      + " ".join(f'{n}: decisão em {dt(e["ciclo"]["decisao"])}, válido até {dt(validade(e["ciclo"]))}, {e["ciclo"]["edicao"]}.' for n, e in LAN)
      + f' A transição dos certificados de 2015 termina em {dt(FIM_TRANSICAO)}.">']
for a in range(2028, 2032):
    d = date(a, 1, 1)
    gt.append(f'        <line class="grid" x1="{gx(d):.1f}" y1="30" x2="{gx(d):.1f}" y2="190"/>')
    gt.append(f'        <text class="mu" x="{gx(d):.1f}" y="206" font-size="11"{MID}{TNUM}>{a}</text>')
gt.append(f'        <line class="now" x1="{gx(FIM_TRANSICAO):.1f}" y1="24" x2="{gx(FIM_TRANSICAO):.1f}" y2="190"/>')
gt.append(f'        <text class="b halo" x="{gx(FIM_TRANSICAO) + 6:.1f}" y="30" font-size="10.5">fim da transição, {dt(FIM_TRANSICAO)}</text>')
hits = []
for k, (n, e) in enumerate(LAN):
    c = e["ciclo"]
    y = 56 + k * 70
    gt.append(f'        <text class="b" x="20" y="{y + 18}" font-size="12.5">{n}</text>')
    gt.append(f'        <text class="mu" x="20" y="{y + 34}" font-size="10.5">{c["edicao"]}</text>')
    gt.append(f'        <rect class="bar {"f2" if c["edicao"] == E2015 else "f1"}" data-k="{k}" x="{gx(c["decisao"]):.1f}" y="{y + 4}" width="{gx(validade(c)) - gx(c["decisao"]):.1f}" height="24" fill-opacity=".35"/>')
    for j, (ev, lim) in enumerate(zip(EVENTOS, limites(c))):
        dd = c["feito"][j] or lim
        if not dd or dd < G0 or j in (0, 1):
            continue
        cx = gx(dd)
        gt.append(f'        <circle class="{"f1" if c["feito"][j] else "f0"}" cx="{cx:.1f}" cy="{y + 16}" r="6"/>')
        gt.append(f'        <text class="mu" x="{cx:.1f}" y="{y + 46}" font-size="9.5"{MID}>{["", "", "decisão", "1ª man.", "2ª man.", "recert.", "transição"][j]}</text>')
        hits.append(f'        <circle class="hit" cx="{cx:.1f}" cy="{y + 16}" r="11" tabindex="0" role="img" aria-label="{n}, {ev}: {dt(dd)}" data-k="{k}" data-n="{n}" '
                    f'data-s="{escape(ev)}" data-d="{dt(dd)}" data-p="{"realizado" if c["feito"][j] else "limite"}" data-cx="{cx:.1f}" data-cy="{y}"/>')
gt.append(f'        <text x="450" y="232" font-size="11.5"{MID}>Círculo cheio: realizado. Círculo cinza: o limite do evento. A barra é a validade do certificado.</text>')
gt += hits + ["      </svg>"]
tb = ['        <table class="aud">', '          <thead><tr><th>Organização</th><th>Evento</th><th class="c">Limite</th><th class="c">Realizado</th><th>Situação</th></tr></thead>', '          <tbody>']
for n, e in LAN:
    c = e["ciclo"]
    for k, (ev, lim) in enumerate(zip(EVENTOS, limites(c))):
        tb.append(f'            <tr><td>{n}</td><td>{ev}</td><td class="c">{dt(lim)}</td><td class="c">{dt(c["feito"][k])}</td><td>{evento_sit(c, k)}</td></tr>')
tb += ['          </tbody>', '        </table>']

# ------------------------------------------------------------------ módulo 9: a transição
T0, T1 = date(2026, 7, 1), date(2029, 12, 31)
tx = lambda d: 40 + (d - T0).days * (860 - 40) / (T1 - T0).days  # noqa: E731
tr = ['      <svg viewBox="0 0 900 236" role="img" aria-label="A janela de transição para a ISO 9001:2026. ' + " ".join(f"{dt(d)}: {t}." for d, t in TRANSICAO) + '">']
tr.append(f'        <rect class="bx-s2" x="{tx(PUBLICACAO):.1f}" y="86" width="{tx(FIM_TRANSICAO) - tx(PUBLICACAO):.1f}" height="28"/>')
for a in range(2027, 2030):
    d = date(a, 1, 1)
    tr.append(f'        <line class="grid" x1="{tx(d):.1f}" y1="80" x2="{tx(d):.1f}" y2="120"/>')
    tr.append(f'        <text class="mu" x="{tx(d):.1f}" y="134" font-size="10.5"{MID}{TNUM}>{a}</text>')
for k, (d, t) in enumerate(TRANSICAO):
    x = tx(d)
    y = 42 if k % 2 == 0 else 176
    tr.append(f'        <line class="ln-mu" x1="{x:.1f}" y1="{56 if y < 100 else 118}" x2="{x:.1f}" y2="{84 if y < 100 else 164}"/>')
    tr.append(f'        <circle class="{"f3" if d == FIM_TRANSICAO else "f1"}" cx="{x:.1f}" cy="100" r="6"/>')
    anc = MID if 0 < k < len(TRANSICAO) - 1 else ("" if k == 0 else END)
    xt = x if anc == MID else (x - 6 if k == 0 else x + 6)
    tr.append(f'        <text class="b" x="{xt:.1f}" y="{y}" font-size="11"{anc}>{dt(d)}</text>')
    lines(tr, t, xt, y + 14, 34, fs=10.5, cls="mu", step=13, maxl=2, anchor=None if anc == "" else anc.split('"')[1])
tr.append(f'        <text x="450" y="228" font-size="11.5"{MID}>Três anos de transição, da publicação ao fim da janela, fixado pela Global ACI.</text>')
tr.append("      </svg>")

# ------------------------------------------------------------------ módulo 12: figura das normas
ISOP = [("ISO/IEC 17021-1", "Requisitos para os organismos que auditam e certificam sistemas de gestão.", "o ciclo e as fases"),
        ("Acreditação", "O acreditador avalia o organismo, e a Global ACI dá valor ao certificado lá fora.", "a cadeia de confiança"),
        ("ISO 9001 · 4.3", "O escopo do sistema, que o certificado repete, com a justificativa do que não se aplica.", "a prontidão"),
        ("Transição", "Cada nova edição abre um prazo para os certificados migrarem.", "o ciclo e a transição")]
iso = ['      <svg viewBox="0 0 900 200" role="img" aria-label="As referências da certificação. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in ISOP) + '">']
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
for tag, val in (("<!--CICLO-->", "\n".join(ci)), ("<!--FLUXO-->", "\n".join(et)), ("<!--CADEIA-->", "\n".join(cc)), ("<!--FASES-->", "\n".join(fa)),
                 ("<!--PRAZOS-->", "\n".join(pz)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1PRONT-->", pront_tab(EX1)), ("<!--EX1CICLO-->", ciclo_tab(EX1)), ("<!--EX1CT-->", ct_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2PRONT-->", pront_tab(EX2)), ("<!--EX2CICLO-->", ciclo_tab(EX2)), ("<!--EX2CT-->", ct_tab(EX2)),
                 ("<!--EX3FIG-->", "\n".join(im)), ("<!--CHART-->", "\n".join(gt)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--TRANSICAO-->", "\n".join(tr)),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Processo de certificação</title>")
assert "certificação" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", resumo(EX1), "| indústria", resumo(EX2))
