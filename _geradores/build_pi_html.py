# -*- coding: utf-8 -*-
"""Monta treinamento-partes-interessadas.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pi_data import (ALTA, ATENDE, CHECK, ESTRS, ETAPAS, EX1, EX2, GERIR, INFORM, MONIT, MUDANCA, NAO, NAOAT, PARTE, SATISF, SIM,  # noqa: E402
                     adotados, atendimento, conta, estrategia, pertinente)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# atende, atende em parte e não atende: a mesma paleta de três cores do estudo de Satisfação, validada para daltonismo nos dois modos
LIGHT = ("\n  --s1:#2A6FB0; --s1-tint:#DCE8F3;\n  --s2:#D19A2E; --s2-tint:#F8EBCB;\n  --s3:#B0413E; --s3-tint:#F5DEDC;\n  --on-s2:#16242E;")
DARK = ("\n  --s1:#4F97DB; --s1-tint:#1B2F42;\n  --s2:#B58E14; --s2-tint:#3A2C12;\n  --s3:#D14B45; --s3-tint:#3D1F1E;\n  --on-s2:#0F171C;")
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Situações e estratégias */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.s1{background:var(--s1)} .chip.s2{background:var(--s2);color:var(--on-s2)} .chip.s3{background:var(--s3)}
.chip.sl{background:var(--sunk);color:var(--ink);box-shadow:inset 0 0 0 1px var(--rule)}
.chip.pr{background:var(--ink);color:var(--ground)}
svg .hd-ink{fill:var(--ink)}
svg .f1{fill:var(--s1)} svg .f2{fill:var(--s2)} svg .f3{fill:var(--s3)}
svg .on2{fill:var(--on-s2)}
svg .q1{fill:var(--p-tint)} svg .q2{fill:var(--d-tint)} svg .q3{fill:var(--c-tint)} svg .q4{fill:var(--sunk)}
svg .cell-ln{stroke:var(--surface);stroke-width:2;fill:none}
svg .dotp{fill:var(--ink);stroke:var(--surface);stroke-width:2}
svg .dot-old{fill:var(--surface);stroke:var(--muted);stroke-width:1.5;stroke-dasharray:4 3}
svg .seg{stroke:var(--surface);stroke-width:2}
svg .halo{paint-order:stroke;stroke:var(--surface);stroke-width:5px;stroke-linejoin:round}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas dos exemplos */
table.aud{font-size:.8rem;min-width:900px;line-height:1.4}
table.aud th, table.aud td{padding:8px 9px}
table.aud td.n{white-space:nowrap;font-weight:600;color:var(--muted)}
table.aud td.c, table.aud th.c{text-align:center;font-variant-numeric:tabular-nums}
table.aud td.nw{white-space:nowrap;font-variant-numeric:tabular-nums}
table.aud tr.off td{color:var(--muted)}
table.aud td small, table.aud th small{display:block;color:var(--muted);font-size:.76rem;margin-top:3px;font-weight:400}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha da análise (acima de cada exemplo) */"""
assert css.count("\n.ficha{") == 1
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

TNUM = ' style="font-variant-numeric:tabular-nums"'
QCLS = {GERIR: "q1", SATISF: "q2", INFORM: "q3", MONIT: "q4"}


def dt(d):
    return d.strftime("%d/%m/%Y") if d else "—"


def pc(v):
    """Percentual inteiro, com a metade arredondada para cima, como na planilha."""
    return f"{int(100 * v + 0.5 + 1e-9)}%"


def est(p):
    return estrategia(p["inf"], p["int"])


def marker(i, mu=False):
    return (f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path class="{"ah-mu" if mu else "ah"}" d="M0 0 L10 5 L0 10 z"/></marker>')


# ------------------------------------------------------------------ figura 1: os grupos
GR = [("Clientes", "Produto conforme, no prazo, e resposta quando reclamam."), ("Colaboradores", "Trabalho seguro, pagamento em dia e treinamento."),
      ("Fornecedores e parceiros", "Pedido claro, previsão de compra e pagamento no prazo."), ("Reguladores", "Cumprimento da lei e licenças válidas."),
      ("Proprietários e investidores", "Resultado e continuidade do negócio."), ("Sociedade", "Boa convivência: ruído, trânsito, resíduos e emprego.")]
gf = ['      <svg viewBox="0 0 900 330" role="img" aria-label="Os seis grupos de partes interessadas, ao redor da organização e do seu sistema de gestão. '
      + " ".join(f"{a}: esperam {b[0].lower() + b[1:]}" for a, b in GR) + ' Cada grupo afeta a organização e é afetado por ela.">',
      "        <defs>" + marker("a1") + "</defs>"]
for k, (a, b) in enumerate(GR):
    x, y = 10 + (k % 3) * 300, 14 if k < 3 else 230
    gf.append(f'        <rect class="{["bx-p", "bx-d", "bx-c"][k % 3]}" x="{x}" y="{y}" width="280" height="86"/>')
    gf.append(f'        <text class="b" x="{x + 14}" y="{y + 26}" font-size="13">{escape(a)}</text>')
    gf.append(f'        <text class="mono mu" x="{x + 14}" y="{y + 44}" font-size="9.5">ESPERAM</text>')
    for j, l in enumerate(textwrap.wrap(b, 42)[:2]):
        gf.append(f'        <text x="{x + 14}" y="{y + 60 + j * 14}" font-size="11">{escape(l)}</text>')
    cx = [350, 450, 550][k % 3]
    if k < 3:
        gf.append(f'        <line class="ln" x1="{x + 140}" y1="103" x2="{cx}" y2="133" marker-start="url(#a1)" marker-end="url(#a1)"/>')
    else:
        gf.append(f'        <line class="ln" x1="{cx}" y1="197" x2="{x + 140}" y2="227" marker-start="url(#a1)" marker-end="url(#a1)"/>')
gf.append('        <rect class="bx-ink" x="270" y="136" width="360" height="58"/>')
gf.append('        <text class="b t-ground" x="450" y="160" font-size="13.5" text-anchor="middle">A organização e o seu sistema de gestão</text>')
gf.append('        <text class="t-ground" x="450" y="180" font-size="11" text-anchor="middle">afeta cada parte, e é afetada por ela</text>')
gf.append("      </svg>")

# ------------------------------------------------------------------ figura 2: as cinco etapas
W5, G5 = 164, 14
LET = ["Q", "Q", "E", "A", "A"]
fl = ['      <svg viewBox="0 0 900 206" role="img" aria-label="As cinco etapas do trabalho. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS) + ' A revisão devolve o trabalho à primeira etapa.">',
      "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
for k, (nome, desc) in enumerate(ETAPAS):
    x = 12 + k * (W5 + G5)
    fl.append(f'        <rect class="{["bx-p", "bx-p", "bx-d", "bx-c", "bx-c"][k]}" x="{x}" y="16" width="{W5}" height="124"/>')
    fl.append(f'        <text class="mono mu" x="{x + 12}" y="36" font-size="10">{k + 1} · {LET[k]}</text>')
    fl.append(f'        <text class="b" x="{x + 12}" y="58" font-size="13">{escape(nome)}</text>')
    for j, l in enumerate(textwrap.wrap(desc, 26)[:4]):
        fl.append(f'        <text x="{x + 12}" y="{80 + j * 14.5}" font-size="10.5">{escape(l)}</text>')
    if k < 4:
        fl.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="78" x2="{x + W5 + G5 - 2}" y2="78" marker-end="url(#a2)"/>')
xa, xb = 12 + 4 * (W5 + G5) + W5 / 2, 12 + W5 / 2
fl.append(f'        <path class="ln-mu dash" d="M{xa} 142 V170 H{xb} V146" marker-end="url(#a2m)"/>')
fl.append('        <text class="mu halo" x="450" y="174" font-size="11" text-anchor="middle">todo ano, e sempre que um fato muda a posição de uma parte</text>')
fl.append('        <text x="450" y="198" font-size="11.5" text-anchor="middle">Q: quem são. E: o que esperam. A: como a organização atende.</text>')
fl.append("      </svg>")


# ------------------------------------------------------------------ a matriz de influência e interesse
def matriz(x0, y0, cw, chh, rotulos=True):
    """Grade de 5 por 5: interesse no eixo horizontal, influência no vertical. Devolve as linhas e a função de posição."""
    def pos(inf, int_):
        return x0 + (int_ - 1) * cw + cw / 2, y0 + (5 - inf) * chh + chh / 2

    na = 5 - ALTA + 1   # quantas notas contam como alta
    nb = 5 - na
    o = [f'        <rect class="q2" x="{x0}" y="{y0}" width="{nb * cw}" height="{na * chh}"/>',
         f'        <rect class="q1" x="{x0 + nb * cw}" y="{y0}" width="{na * cw}" height="{na * chh}"/>',
         f'        <rect class="q4" x="{x0}" y="{y0 + na * chh}" width="{nb * cw}" height="{nb * chh}"/>',
         f'        <rect class="q3" x="{x0 + nb * cw}" y="{y0 + na * chh}" width="{na * cw}" height="{nb * chh}"/>']
    for k in range(1, 5):
        o.append(f'        <line class="cell-ln" x1="{x0 + k * cw}" y1="{y0}" x2="{x0 + k * cw}" y2="{y0 + 5 * chh}"/>')
        o.append(f'        <line class="cell-ln" x1="{x0}" y1="{y0 + k * chh}" x2="{x0 + 5 * cw}" y2="{y0 + k * chh}"/>')
    for k in range(5):
        o.append(f'        <text class="mu" x="{x0 + k * cw + cw / 2}" y="{y0 + 5 * chh + 17}" font-size="11" text-anchor="middle"{TNUM}>{k + 1}</text>')
        o.append(f'        <text class="mu" x="{x0 - 10}" y="{y0 + (4 - k) * chh + chh / 2 + 4}" font-size="11" text-anchor="end"{TNUM}>{k + 1}</text>')
    o.append(f'        <text class="mono mu" x="{x0 + 2.5 * cw}" y="{y0 + 5 * chh + 36}" font-size="10" text-anchor="middle">INTERESSE</text>')
    o.append(f'        <text class="mono mu" x="{x0 - 34}" y="{y0 + 2.5 * chh}" font-size="10" text-anchor="middle" transform="rotate(-90 {x0 - 34} {y0 + 2.5 * chh})">INFLUÊNCIA</text>')
    if rotulos:
        for nome, x, y in ((SATISF, x0 + 7, y0 + 14), (GERIR, x0 + nb * cw + 7, y0 + 14), (MONIT, x0 + 7, y0 + na * chh + 14), (INFORM, x0 + nb * cw + 7, y0 + na * chh + 14)):
            o.append(f'        <text class="mono" x="{x}" y="{y}" font-size="9.5">{nome.upper()}</text>')
    return o, pos


P1 = EX1["partes"]
mz = ['      <svg viewBox="0 0 900 390" role="img" aria-label="Matriz de influência e interesse da pizzaria. '
      + " ".join(f'{p["nome"]}: influência {p["inf"]}, interesse {p["int"]}, {est(p).lower()}.' for p in P1) + '">']
g_, pos = matriz(80, 26, 80, 62)
mz += g_
celulas = {}
for p in P1:
    celulas.setdefault((p["inf"], p["int"]), []).append(p)
for (inf, int_), ps in celulas.items():
    cx, cy = pos(inf, int_)
    for j, p in enumerate(ps):
        x = cx + (j - (len(ps) - 1) / 2) * 28
        mz.append(f'        <circle class="dotp" cx="{x}" cy="{cy + 5}" r="12"/>')
        mz.append(f'        <text class="b t-ground" x="{x}" y="{cy + 9}" font-size="11.5" text-anchor="middle"{TNUM}>{p["n"]}</text>')
for p in P1:
    y = 34 + (p["n"] - 1) * 29
    mz.append(f'        <circle class="dotp" cx="528" cy="{y + 6}" r="11"/>')
    mz.append(f'        <text class="b t-ground" x="528" y="{y + 10}" font-size="11" text-anchor="middle"{TNUM}>{p["n"]}</text>')
    mz.append(f'        <text class="b" x="548" y="{y + 10}" font-size="12">{escape(p["curto"])}</text>')
    mz.append(f'        <rect class="{QCLS[est(p)]}" x="740" y="{y - 3}" width="12" height="18"/>')
    mz.append(f'        <text class="mu" x="758" y="{y + 10}" font-size="11.5">{est(p)}</text>')
mz.append("      </svg>")

# tabela das estratégias, com as partes da pizzaria
o = ['  <div class="tbl">', '    <table>',
     '      <thead><tr><th style="width:18%">Estratégia</th><th style="width:24%">Quando</th><th style="width:30%">O que fazer</th><th>Na pizzaria</th></tr></thead>', '      <tbody>']
for nome, quando, fazer in ESTRS:
    o.append(f'        <tr><td><strong>{nome}</strong></td><td>{escape(quando)}</td><td>{escape(fazer)}</td><td>{escape(", ".join(p["curto"] for p in P1 if est(p) == nome))}.</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>']
estrtab = "\n".join(o)

# ------------------------------------------------------------------ figura 4: da expectativa ao requisito
CX = [("bx", 10, 78, 160, 94, "Necessidade ou expectativa", "Levantada em contrato, lei, reclamação ou conversa."),
      ("bx-d", 200, 90, 170, 70, "É exigência de lei, de licença ou de contrato?", ""),
      ("bx-p", 420, 20, 190, 64, "Requisito obrigatório", "Legal ou contratual. Entra sempre."),
      ("bx-d", 420, 150, 190, 70, "A organização decide adotar?", "A decisão é da direção."),
      ("bx-ink", 680, 20, 210, 110, "No sistema de gestão", "Um processo que atende, uma forma de monitorar e a situação avaliada."),
      ("bx-out", 680, 160, 210, 70, "Não adotada", "Registrada, com a justificativa. Revista todo ano.")]
dc = ['      <svg viewBox="0 0 900 250" role="img" aria-label="Da expectativa ao requisito do sistema. Uma necessidade ou expectativa é levantada. Se é exigência de lei, de licença ou de contrato, '
      'é requisito obrigatório e entra no sistema de gestão. Se não é, a organização decide se adota. Se adota, entra no sistema, com um processo que atende, uma forma de monitorar '
      'e a situação avaliada. Se não adota, fica registrada, com a justificativa, e é revista todo ano.">', "        <defs>" + marker("a4") + "</defs>"]
for cls, x, y, w, h, tit, sub_ in CX:
    ink = cls == "bx-ink"
    dc.append(f'        <rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>')
    yy = y + 22
    for l in textwrap.wrap(tit, int(w / 6.6)):
        dc.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{yy}" font-size="12">{escape(l)}</text>')
        yy += 15
    yy += 3
    for l in textwrap.wrap(sub_, int(w / 5.9)):
        dc.append(f'        <text class="{"t-ground" if ink else "mu"}" x="{x + 12}" y="{yy}" font-size="10.5">{escape(l)}</text>')
        yy += 13.5
dc += ['        <line class="ln" x1="172" y1="125" x2="197" y2="125" marker-end="url(#a4)"/>',
       '        <path class="ln" d="M372 108 H396 V52 H417" marker-end="url(#a4)"/><text class="b halo" x="396" y="80" font-size="11" text-anchor="middle">sim</text>',
       '        <path class="ln" d="M372 142 H396 V185 H417" marker-end="url(#a4)"/><text class="b halo" x="396" y="168" font-size="11" text-anchor="middle">não</text>',
       '        <line class="ln" x1="612" y1="52" x2="677" y2="52" marker-end="url(#a4)"/>',
       '        <path class="ln" d="M612 170 H646 V104 H677" marker-end="url(#a4)"/><text class="b halo" x="646" y="140" font-size="11" text-anchor="middle">sim</text>',
       '        <line class="ln" x1="612" y1="204" x2="677" y2="204" marker-end="url(#a4)"/><text class="b halo" x="644" y="199" font-size="11" text-anchor="middle">não</text>',
       "      </svg>"]


# ------------------------------------------------------------------ exemplos
def ficha(h):
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Data e responsáveis</dt><dd>{dt(h["data"])}. {escape(h["por"])}.</dd></div>',
                      f'    <div><dt>Escopo</dt><dd>{escape(h["escopo"])}</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      f'    <div><dt>Revisão</dt><dd>{escape(h["revisao"])}</dd></div>',
                      '  </dl>'])


def chip_est(e):
    return f'<span class="chip {"pr" if e == GERIR else "sl"}">{e}</span>'


def chip_sit(s):
    return f'<span class="chip {({ATENDE: "s1", PARTE: "s2", NAOAT: "s3"})[s]}">{s}</span>'


def partes_tab(ex):
    n = len(ex["partes"])
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>Partes interessadas · {n} listadas, {sum(1 for p in ex["partes"] if pertinente(p))} pertinentes ao sistema</caption>',
         '      <thead><tr><th class="c">#</th><th style="width:27%">Parte interessada<small>Por que importa</small></th><th style="width:13%">Grupo</th>'
         '<th class="c">Influência</th><th class="c">Interesse</th><th>Estratégia</th><th class="c">Pertinente</th><th style="width:24%">Relacionamento<small>Quem cuida</small></th></tr></thead>', '      <tbody>']
    for p in ex["partes"]:
        per = pertinente(p)
        o.append(f'        <tr{"" if per else " class=" + chr(34) + "off" + chr(34)}><td class="c n">{p["n"]}</td><td><strong>{escape(p["nome"])}</strong><small>{escape(p["porque"])}</small></td><td>{escape(p["grupo"])}</td>'
                 f'<td class="c">{p["inf"]}</td><td class="c">{p["int"]}</td><td>{chip_est(est(p))}</td><td class="c">{SIM if per else NAO}{"<small>requisito legal</small>" if p["legal"] else ""}</td>'
                 f'<td>{escape(p["canal"]) or "—"}{"<small>" + escape(p["quem"]) + "</small>" if p["quem"] else ""}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def reqs_tab(ex):
    a = adotados(ex)
    o = ['  <div class="tbl">', '    <table class="aud">',
         f'      <caption>Requisitos · {len(ex["reqs"])} levantados, {len(a)} adotados · atendimento de {pc(atendimento(ex))}</caption>',
         '      <thead><tr><th style="width:13%">Parte</th><th style="width:20%">O que espera</th><th>Tipo</th><th class="c">Adotado</th><th style="width:19%">Como atende, ou por que não adota</th>'
         '<th style="width:15%">Como se monitora</th><th>Situação</th><th style="width:17%">Ação<small>Responsável e prazo</small></th></tr></thead>', '      <tbody>']
    ult = None
    for r in ex["reqs"]:
        sim = r["adotado"] == SIM
        acao = f'{escape(r["acao"])}<small>{escape(r["resp"])} · {dt(r["prazo"])}</small>' if r["acao"] else "—"
        o.append(f'        <tr{"" if sim else " class=" + chr(34) + "off" + chr(34)}><td>{"<strong>" + escape(r["parte"]) + "</strong>" if r["parte"] != ult else ""}</td><td>{escape(r["req"])}</td><td>{r["tipo"]}</td>'
                 f'<td class="c">{r["adotado"]}</td><td>{escape(r["como"])}</td><td>{escape(r["monit"] or "—")}</td><td>{chip_sit(r["sit"]) if sim else "—"}</td><td>{acao}</td></tr>')
        ult = r["parte"]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


# exemplo 3: a parte que muda de posição
M = MUDANCA
e3 = [f'      <svg viewBox="0 0 900 300" role="img" aria-label="As portarias dos condomínios na matriz. Em 23/10/2026: influência {M["antes"][0]} e interesse {M["antes"][1]}, no quadrante de monitorar. '
      f'Em {dt(M["data"])}: influência {M["depois"][0]} e interesse {M["depois"][1]}, no quadrante de manter satisfeito.">', "        <defs>" + marker("a5") + "</defs>"]
g_, pos3 = matriz(80, 20, 70, 46)
e3 += g_
(ax, ay), (bx_, by) = pos3(*M["antes"]), pos3(*M["depois"])
e3.append(f'        <circle class="dot-old" cx="{ax}" cy="{ay + 5}" r="12"/>')
e3.append(f'        <line class="ln" x1="{ax + 11}" y1="{ay - 3}" x2="{bx_ - 14}" y2="{by + 13}" marker-end="url(#a5)"/>')
e3.append(f'        <circle class="dotp" cx="{bx_}" cy="{by + 5}" r="12"/>')
for k, (tit, (inf, int_), data, extra_) in enumerate((("Antes", M["antes"], D_ := EX1["head"]["data"], "Sem requisito e sem canal."),
                                                      ("Depois", M["depois"], M["data"], "Requisito: " + M["requisito"] + " Canal: " + M["canal"]))):
    y = 34 + k * 120
    e3.append(f'        <circle class="{"dot-old" if k == 0 else "dotp"}" cx="500" cy="{y + 3}" r="10"/>')
    e3.append(f'        <text class="b" x="520" y="{y + 8}" font-size="13">{tit} · {dt(data)}</text>')
    e3.append(f'        <text x="520" y="{y + 28}" font-size="11.5">Influência {inf} e interesse {int_}: {estrategia(inf, int_).lower()}.</text>')
    for j, l in enumerate(textwrap.wrap(extra_, 58)):
        e3.append(f'        <text class="mu" x="520" y="{y + 46 + j * 15}" font-size="11">{escape(l)}</text>')
e3.append("      </svg>")
ex3head = "\n".join(['  <dl class="ficha">',
                     f'    <div><dt>Organização</dt><dd>{escape(EX1["head"]["org"])}</dd></div>',
                     f'    <div><dt>Parte interessada</dt><dd>{escape(M["parte"])}</dd></div>',
                     f'    <div><dt>Revisão</dt><dd>{dt(M["data"])}, fora da data anual, depois da RNC 2027-04.</dd></div>',
                     '  </dl>'])
o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Linha do tempo</caption>',
     '      <thead><tr><th class="c">Data</th><th style="width:16%">Momento</th><th>O que aconteceu</th></tr></thead>', '      <tbody>']
for d, etapa, texto in M["linha"]:
    o.append(f'        <tr><td class="nw">{dt(d)}</td><td><strong>{escape(etapa)}</strong></td><td>{escape(texto)}</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>']
ex3linha = "\n".join(o)

# ------------------------------------------------------------------ módulo 7: requisitos por parte e por situação
PP = [p for p in P1 if pertinente(p)]
ROT = ["Atende", "Atende em parte", "Não atende"]
X0, U, TOP, RH, BH = 330, 78, 58, 38, 22
bottom = TOP + RH * len(PP)
HH = bottom + 46
LIN = [dict(p=p, a=conta(EX1, ATENDE, p["nome"]), b=conta(EX1, PARTE, p["nome"]), c=conta(EX1, NAOAT, p["nome"]), at=atendimento(EX1, p["nome"])) for p in PP]
ch = [f'      <svg id="bars" viewBox="0 0 900 {HH}" role="img" aria-label="Gráfico de barras empilhadas com os requisitos adotados de cada parte interessada pertinente da pizzaria, pela situação. '
      + " ".join(f'{l["p"]["nome"]}: {l["a"]} atende, {l["b"]} em parte e {l["c"]} não atende, atendimento de {pc(l["at"])}.' for l in LIN) + '">', '        <g font-size="11.5">']
xs = X0
for k, t in enumerate(ROT):
    ch.append(f'          <rect class="f{k + 1}" x="{xs}" y="12" width="14" height="14"/><text x="{xs + 22}" y="24">{t}</text>')
    xs += 40 + len(t) * 6.6
ch.append('        </g>')
vmax = max(l["a"] + l["b"] + l["c"] for l in LIN)
for v in range(0, vmax + 1):
    x = X0 + v * U
    ch.append(f'        <line class="grid" x1="{x}" y1="{TOP - 8}" x2="{x}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{x}" y="{bottom + 16}" font-size="11" text-anchor="middle"{TNUM}>{v}</text>')
ch.append(f'        <text class="mono mu" x="{X0 + vmax * U / 2}" y="{bottom + 36}" font-size="10" text-anchor="middle">REQUISITOS ADOTADOS</text>')
for k, l in enumerate(LIN):
    y = TOP + RH * k + (RH - BH) / 2
    ch.append(f'        <text x="20" y="{y + 15:.1f}" font-size="12"><tspan class="b">{escape(l["p"]["curto"])}</tspan><tspan class="mu"> · {est(l["p"]).lower()}</tspan></text>')
    x = X0
    for j, v in enumerate((l["a"], l["b"], l["c"])):
        if v:
            ch.append(f'        <rect class="seg f{j + 1}" data-k="{k}" x="{x}" y="{y:.1f}" width="{v * U}" height="{BH}"/>')
            ch.append(f'        <text class="b {"on2" if j == 1 else "on"}" x="{x + v * U / 2}" y="{y + 15.5:.1f}" font-size="12" text-anchor="middle" pointer-events="none">{v}</text>')
            x += v * U
    ch.append(f'        <text class="halo" x="{x + 10}" y="{y + 15:.1f}" font-size="11.5"><tspan class="b">{pc(l["at"])}</tspan><tspan class="mu"> de atendimento</tspan></text>')
for k, l in enumerate(LIN):
    tot = l["a"] + l["b"] + l["c"]
    ch.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" '
              f'aria-label="{escape(l["p"]["nome"])}: {tot} requisitos adotados, {l["a"]} atende, {l["b"]} em parte e {l["c"]} não atende, atendimento de {pc(l["at"])}" data-k="{k}" '
              f'data-r="{escape(l["p"]["nome"])}" data-e="{est(l["p"])}" data-a="{l["a"]}" data-b="{l["b"]}" data-c="{l["c"]}" data-p="{pc(l["at"])[:-1]}" data-cx="{X0 + tot * U / 2:.1f}"/>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>Parte interessada</th><th>Estratégia</th>' + "".join(f'<th class="c">{t}</th>' for t in ROT) + '<th class="c">Atendimento</th></tr></thead>',
      '          <tbody>']
for l in LIN:
    tb.append(f'            <tr><td><strong>{escape(l["p"]["nome"])}</strong></td><td>{est(l["p"])}</td><td class="c">{l["a"]}</td><td class="c">{l["b"]}</td><td class="c">{l["c"]}</td><td class="c">{pc(l["at"])}</td></tr>')
tb.append(f'            <tr><td><strong>Todas</strong></td><td></td><td class="c">{conta(EX1, ATENDE)}</td><td class="c">{conta(EX1, PARTE)}</td><td class="c">{conta(EX1, NAOAT)}</td><td class="c">{pc(atendimento(EX1))}</td></tr>')
tb += ['          </tbody>', '        </table>']
ger = [l for l in LIN if est(l["p"]) == GERIR]
outras = [l for l in LIN if est(l["p"]) != GERIR]
pend = lambda ls: sum(l["b"] + l["c"] for l in ls)  # noqa: E731
leg = [r for r in adotados(EX1) if r["tipo"] == "Legal"]
charttext = (f'  <p>O atendimento geral é de {pc(atendimento(EX1))}: dos {len(adotados(EX1))} requisitos adotados, {conta(EX1, ATENDE)} são atendidos, {conta(EX1, PARTE)} em parte, e {conta(EX1, NAOAT)} não é. '
             f'O número sozinho diz pouco. A distribuição diz mais: das {pend(LIN)} pendências, {pend(ger)} estão nas quatro partes de gerir de perto, e {pend(outras)} nas outras cinco. '
             f'As pendências se concentram onde a influência e o interesse são maiores, e é nelas que a loja deve pôr o esforço. '
             f'A pendência de fora desse grupo é a licença sanitária, em renovação: dos {len(leg)} requisitos legais, é o único que não está atendido por completo, e o que tem o prazo mais curto.</p>')
assert pend(outras) == 1 and sum(1 for r in leg if r["sit"] != ATENDE) == 1

# ------------------------------------------------------------------ módulo 10: figura da ISO
PARTES = [("4.2 · Determinar as partes", "As partes interessadas pertinentes ao sistema de gestão da qualidade.", "Lista por grupo e matriz de influência e interesse"),
          ("4.2 · Determinar os requisitos", "Os requisitos pertinentes de cada parte.", "Registro de requisitos, com tipo e decisão"),
          ("4.2 · Monitorar e analisar", "Acompanhar e rever as informações sobre as partes e os requisitos.", "Situação de cada requisito e revisão anual"),
          ("4.3, 6.1 e 9.3 · Usar", "Levar o resultado ao escopo, aos riscos e à análise crítica.", "Ligação com a SWOT, os riscos e a direção")]
iso = ['      <svg viewBox="0 0 900 190" role="img" aria-label="O que a norma pede sobre partes interessadas. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in PARTES) + '">']
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
for tag, val in (("<!--GRUPOSFIG-->", "\n".join(gf)), ("<!--FLUXO-->", "\n".join(fl)), ("<!--MATRIZFIG-->", "\n".join(mz)), ("<!--ESTRTAB-->", estrtab), ("<!--DECFIG-->", "\n".join(dc)),
                 ("<!--EX1HEAD-->", ficha(EX1["head"])), ("<!--EX1PARTES-->", partes_tab(EX1)), ("<!--EX1REQS-->", reqs_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2["head"])), ("<!--EX2PARTES-->", partes_tab(EX2)), ("<!--EX2REQS-->", reqs_tab(EX2)),
                 ("<!--EX3HEAD-->", ex3head), ("<!--EX3FIG-->", "\n".join(e3)), ("<!--EX3LINHA-->", ex3linha),
                 ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHARTTEXT-->", charttext),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Partes interessadas</title>")
assert "Partes interessadas" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", pc(atendimento(EX1)), "| indústria", pc(atendimento(EX2)))
