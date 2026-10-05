# -*- coding: utf-8 -*-
"""Monta treinamento-competencias.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comp_data import (A_EFICAZ, A_PARCIAL, A_REFAZER, CHECK, COBERTURA, CONSCIENTIZACAO, ETAPAS, EX1, EX2, FONTES, NIVEIS, TRILHA, cobertura, lacunas,  # noqa: E402
                       precisam, requerido, situacao_acao)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# níveis: paleta de quatro cores validada para daltonismo nos dois modos, na ordem em que se empilham (azul, âmbar, vermelho, roxo)
LIGHT = ("\n  --s1:#2A6FB0; --s1-tint:#DCE8F3;\n  --s2:#D19A2E; --s2-tint:#F8EBCB;\n  --s3:#B0413E; --s3-tint:#F5DEDC;\n  --s4:#7A3E9A; --s4-tint:#EADFF0;\n  --on-s2:#16242E;")
DARK = ("\n  --s1:#4F97DB; --s1-tint:#1B2F42;\n  --s2:#B58E14; --s2-tint:#3A2C12;\n  --s3:#D14B45; --s3-tint:#3D1F1E;\n  --s4:#A45BC0; --s4-tint:#33203C;\n  --on-s2:#0F171C;")
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Níveis e situações */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.s1{background:var(--s1)} .chip.s2{background:var(--s2);color:var(--on-s2)} .chip.s3{background:var(--s3)} .chip.s4{background:var(--s4)}
.chip.sl{background:var(--sunk);color:var(--ink);box-shadow:inset 0 0 0 1px var(--rule)}
.lv{display:inline-grid;place-items:center;width:1.9em;height:1.9em;font:700 .9em/1 var(--display);color:var(--on-hue)}
.lv.l3{background:var(--s1)} .lv.l2{background:var(--s2);color:var(--on-s2)} .lv.l1{background:var(--s3)} .lv.l0{background:var(--s4)}
.lv.gap{box-shadow:0 0 0 2px var(--surface),0 0 0 4px var(--ink)}
.lv.na{background:var(--sunk);color:var(--muted);font-weight:500}
svg .hd-ink{fill:var(--ink)}
svg .f1{fill:var(--s1)} svg .f2{fill:var(--s2)} svg .f3{fill:var(--s3)} svg .f4{fill:var(--s4)}
svg .on2{fill:var(--on-s2)}
svg .cell{fill:var(--surface);stroke:var(--rule)}
svg .cell-gap{fill:var(--s3-tint);stroke:var(--s3);stroke-width:1.5}
svg .seg{stroke:var(--surface);stroke-width:2}
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
table.aud.mx td.c{padding:6px 4px}
table.aud tr.req td{background:var(--sunk);font-size:.74rem;color:var(--muted)}

/* Ficha da avaliação (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

ACLS = {A_EFICAZ: "s1", A_PARCIAL: "s2", A_REFAZER: "s3"}


def dt(d):
    return d.strftime("%d/%m/%Y") if d else "—"


def lv(n, gap=False):
    return f'<span class="lv l{n}{" gap" if gap else ""}" title="Nível {n}">{n}</span>'


# ------------------------------------------------------------------ módulo 3: ciclo
W, G = 138, 12
ci = ['      <svg viewBox="0 0 900 214" role="img" aria-label="O ciclo da competência, em seis etapas. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS)
      + ' Da matriz atualizada, o ciclo recomeça na próxima revisão.">',
      '        <defs><marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah" d="M0 0 L10 5 L0 10 z"/></marker>'
      '<marker id="a2m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah-mu" d="M0 0 L10 5 L0 10 z"/></marker></defs>']
for k, (nome, desc) in enumerate(ETAPAS):
    x = 6 + k * (W + G)
    ink = k in (0, 5)
    ci.append(f'        <rect class="{"bx-ink" if ink else "bx"}" x="{x}" y="20" width="{W}" height="120"/>')
    ci.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="40" font-size="10">{k + 1}</text>')
    ci.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="62" font-size="12.5">{escape(nome)}</text>')
    for j, l in enumerate(textwrap.wrap(desc, 22)[:3]):
        ci.append(f'        <text{" class=" + chr(34) + "t-ground" + chr(34) if ink else ""} x="{x + 12}" y="{86 + j * 15}" font-size="10.5">{escape(l)}</text>')
    if k < 5:
        ci.append(f'        <line class="ln" x1="{x + W + 1}" y1="80" x2="{x + W + G - 2}" y2="80" marker-end="url(#a2)"/>')
ci.append(f'        <path class="ln-mu dash" d="M{6 + 5 * (W + G) + W / 2} 142 V172 H{6 + W / 2} V146" marker-end="url(#a2m)"/>')
ci.append('        <text class="mu" x="450" y="166" font-size="11" text-anchor="middle">a cada revisão da matriz, o ciclo recomeça</text>')
ci.append('        <text x="450" y="204" font-size="11.5" text-anchor="middle">Se a eficácia não for confirmada, a ação volta à etapa 2, de outro jeito.</text>')
ci.append("      </svg>")

# ------------------------------------------------------------------ módulo 4: escala e anatomia
o = ['  <div class="tbl">', '    <table>',
     '      <thead><tr><th style="width:8%">Nível</th><th style="width:22%">Nome</th><th style="width:36%">O que a pessoa faz</th><th>Evidência típica</th></tr></thead>', '      <tbody>']
for n, nome, faz, ev in NIVEIS:
    o.append(f'        <tr><td>{lv(n)}</td><td><strong>{nome}</strong></td><td>{escape(faz)}</td><td>{escape(ev)}</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>']
escala = "\n".join(o)

# anatomia: uma matriz pequena, esquemática
AN_P = [("Ana", "Atendente", [3, 2, 0]), ("Beto", "Atendente", [2, 1, 0]), ("Cida", "Pizzaiola", [0, 3, 2]), ("Davi", "Pizzaiolo", [0, 2, 1])]
AN_C = ["Registrar o pedido", "Produzir no padrão", "Regular o forno"]
AN_R = {"Atendente": [2, 0, 0], "Pizzaiola": [0, 3, 2], "Pizzaiolo": [0, 3, 2]}
X0, Y0, CW, CH = 300, 74, 130, 40
an = ['      <svg viewBox="0 0 900 330" role="img" aria-label="Anatomia de uma matriz de competências. As linhas são pessoas, com a função. As colunas são competências. '
      'Cada célula traz o nível atual, e o requerido da função aparece ao lado. Davi tem duas lacunas: produzir no padrão, nível 2 com requerido 3, e regular o forno, nível 1 com requerido 2. '
      'Na coluna regular o forno, só Cida está no nível 2 ou mais: a cobertura é de uma pessoa.">',
      '        <text class="mono mu" x="20" y="30" font-size="10">PESSOA · FUNÇÃO</text>',
      f'        <text class="mono mu" x="{X0 + 1.5 * CW}" y="30" font-size="10" text-anchor="middle">COMPETÊNCIAS · NÍVEL ATUAL, COM O REQUERIDO EMBAIXO</text>',
      f'        <text class="mono mu" x="{X0 + 3 * CW + 60}" y="30" font-size="10" text-anchor="middle">LACUNAS</text>']
for j, c in enumerate(AN_C):
    for i, l in enumerate(textwrap.wrap(c, 16)):
        an.append(f'        <text class="b" x="{X0 + j * CW + CW / 2}" y="{52 + i * 13}" font-size="11" text-anchor="middle">{escape(l)}</text>')
for i, (nome, func, nv) in enumerate(AN_P):
    y = Y0 + i * (CH + 6)
    an.append(f'        <text x="20" y="{y + 25}" font-size="12"><tspan class="b">{nome}</tspan> · {func}</text>')
    req = AN_R[func]
    gaps = 0
    for j, v in enumerate(nv):
        x = X0 + j * CW
        gap = req[j] > v
        gaps += gap
        an.append(f'        <rect class="{"cell-gap" if gap else "cell"}" x="{x + 2}" y="{y}" width="{CW - 4}" height="{CH}"/>')
        cls = {3: "f1", 2: "f2", 1: "f3", 0: "f4"}[v]
        an.append(f'        <rect class="{cls}" x="{x + 10}" y="{y + 7}" width="26" height="26"/>')
        an.append(f'        <text class="b {"on2" if v == 2 else "on"}" x="{x + 23}" y="{y + 25}" font-size="13" text-anchor="middle">{v}</text>')
        an.append(f'        <text class="mu" x="{x + 44}" y="{y + 25}" font-size="10.5">req. {req[j]}{" · lacuna" if gap else ""}</text>')
    an.append(f'        <text class="b" x="{X0 + 3 * CW + 60}" y="{y + 25}" font-size="13" text-anchor="middle">{gaps}</text>')
yb = Y0 + 4 * (CH + 6) + 6
an.append(f'        <line class="grid" x1="20" y1="{yb}" x2="{X0 + 3 * CW + 100}" y2="{yb}"/>')
an.append(f'        <text class="mono mu" x="{X0 - 12}" y="{yb + 24}" font-size="9.5" text-anchor="end">NO NÍVEL 2 OU MAIS</text>')
an.append(f'        <text class="mono mu" x="{X0 - 12}" y="{yb + 46}" font-size="9.5" text-anchor="end">COBERTURA</text>')
for j in range(3):
    n2 = sum(1 for _, _, nv in AN_P if nv[j] >= 2)
    an.append(f'        <text class="b" x="{X0 + j * CW + CW / 2}" y="{yb + 24}" font-size="13" text-anchor="middle">{n2}</text>')
    an.append(f'        <text x="{X0 + j * CW + CW / 2}" y="{yb + 46}" font-size="11" text-anchor="middle">{"ok" if n2 >= COBERTURA else "uma só pessoa"}</text>')
an.append(f'        <text x="450" y="{yb + 76}" font-size="11.5" text-anchor="middle">A célula com borda vermelha é uma lacuna. A coluna com uma só pessoa no nível 2 é uma dependência.</text>')
an.append("      </svg>")

# ------------------------------------------------------------------ módulo 5: linha do tempo do treinamento
li = ['      <svg viewBox="0 0 900 250" role="img" aria-label="A vida de uma ação de treinamento. Necessidade, na matriz. Treinamento, com registro. Avaliação de aprendizado, no mesmo dia. '
      'Acompanhamento no posto, por 30 a 90 dias. Avaliação de eficácia, pelo líder. Matriz atualizada, com o nível novo. Os três losangos marcam as verificações.">',
      '        <defs><marker id="a4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah" d="M0 0 L10 5 L0 10 z"/></marker></defs>',
      '        <line class="ln" x1="30" y1="120" x2="880" y2="120" marker-end="url(#a4)"/>']
PTS = [(60, "Necessidade", "na matriz", False), (200, "Treinamento", "com registro", False), (330, "Aprendizado", "entendeu?", True),
       (500, "Acompanhamento", "30 a 90 dias no posto", False), (670, "Eficácia", "faz sozinho?", True), (820, "Matriz", "nível atualizado", True)]
for k, (x, t, s, ver) in enumerate(PTS):
    up = k % 2 == 0
    if ver:
        li.append(f'        <polygon class="hd-ink" points="{x},106 {x + 14},120 {x},134 {x - 14},120"/>')
    else:
        li.append(f'        <circle class="dot" cx="{x}" cy="120" r="7"/>')
    ty = 66 if up else 176
    li.append(f'        <line class="ln-mu" x1="{x}" y1="{104 if up else 136}" x2="{x}" y2="{ty + (10 if up else -22)}"/>')
    li.append(f'        <text class="b" x="{x}" y="{ty}" font-size="12.5" text-anchor="middle">{t}</text>')
    li.append(f'        <text class="mu" x="{x}" y="{ty + 17}" font-size="11" text-anchor="middle">{s}</text>')
li.append('        <rect class="band" x="360" y="140" width="280" height="18"/>')
li.append('        <text class="mono mu" x="500" y="153" font-size="9.5" text-anchor="middle">PRAZO DA EFICÁCIA: 60 DIAS, NESTE MODELO</text>')
li.append('        <polygon class="hd-ink" points="30,228 40,238 30,248 20,238"/><text x="52" y="242" font-size="11.5">verificação com registro</text>')
li.append('        <circle class="dot" cx="290" cy="238" r="6"/><text x="306" y="242" font-size="11.5">etapa da ação</text>')
li.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Data e participantes</dt><dd>{dt(h["data"])}. {escape(h["por"])}</dd></div>',
                      f'    <div><dt>Revisão da matriz</dt><dd>{escape(h["revisao"])}</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      '  </dl>'])


def comps_tab(ex):
    o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Competências e nível requerido por função</caption>',
         '      <thead><tr><th>Item</th><th style="width:30%">Competência</th><th style="width:18%">Padrão de referência</th>'
         + "".join(f'<th class="c">{escape(f)}</th>' for f in ex["funcoes"]) + '</tr></thead>', '      <tbody>']
    for k, (cod, nome, ref) in enumerate(ex["comps"]):
        o.append(f'        <tr><td class="n">{cod}</td><td><strong>{escape(nome)}</strong></td><td>{escape(ref)}</td>'
                 + "".join(f'<td class="c">{r[k] if r[k] else "—"}</td>' for r in ex["funcoes"].values()) + '</tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def matriz_tab(ex):
    n = len(ex["comps"])
    o = ['  <div class="tbl">', '    <table class="aud mx">', f'      <caption>Matriz de competências · níveis em {dt(ex["head"]["data"])}</caption>',
         '      <thead><tr><th style="width:18%">Pessoa</th><th style="width:16%">Função</th>' + "".join(f'<th class="c">{c[0]}</th>' for c in ex["comps"])
         + '<th class="c">Lacunas</th><th class="c">Atendido</th></tr></thead>', '      <tbody>']
    for p in ex["pessoas"]:
        req = requerido(ex, p)
        gaps = {k for k, _, _ in lacunas(ex, p)}
        need = sum(1 for r in req if r > 0)
        cells = "".join('<td class="c">' + (lv(v, k in gaps) if req[k] else f'<span class="lv na">{v}</span>') + '</td>' for k, v in enumerate(p["niveis"]))
        o.append(f'        <tr><td><strong>{escape(p["nome"])}</strong><small>desde {p["desde"].strftime("%m/%Y")}</small></td><td>{escape(p["funcao"])}</td>{cells}'
                 f'<td class="c">{len(gaps) or "—"}</td><td class="c">{round(100 * (need - len(gaps)) / need)}%</td></tr>')
    o.append('        <tr class="req"><td colspan="2">Pessoas no nível 2 ou mais · pessoas cuja função exige</td>'
             + "".join(f'<td class="c">{cobertura(ex, k)} · {precisam(ex, k)}</td>' for k in range(n)) + '<td colspan="2"></td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>',
          '  <p><small>Célula com contorno escuro: lacuna, nível abaixo do requerido. Célula cinza: a função não exige a competência.</small></p>']
    return "\n".join(o)


def plano_tab(ex):
    ref = ex["head"]["data"]
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>Plano de treinamento · situação em {dt(ref)}</caption>',
         '      <thead><tr><th>Nº</th><th style="width:8%">Pessoa</th><th style="width:6%">Comp.</th><th style="width:26%">Ação</th><th style="width:10%">Quem treina</th>'
         '<th style="width:8%">Prazo</th><th style="width:8%">Feito em</th><th style="width:12%">Situação</th><th>Resultado</th></tr></thead>', '      <tbody>']
    for a in ex["plano"]:
        s = situacao_acao(a, ref)
        cls = ACLS.get(s, "sl")
        o.append(f'        <tr><td class="n">{a["n"]}</td><td>{escape(a["pessoa"])}</td><td class="c">{a["comp"]}</td><td>{escape(a["acao"])}</td><td>{escape(a["quem"])}</td>'
                 f'<td class="nw">{dt(a["prazo"])}</td><td class="nw">{dt(a["feito"])}</td><td><span class="chip {cls}">{s}</span></td><td>{escape(a["obs"]) or "—"}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


tr = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Trilha de formação do auditor interno</caption>',
      '      <thead><tr><th>Etapa</th><th style="width:20%">O que é</th><th style="width:36%">Como</th><th style="width:22%">Evidência</th><th>Nível</th></tr></thead>', '      <tbody>']
for n, nome, como, ev, nv in TRILHA:
    tr.append(f'        <tr><td class="n">{n}</td><td><strong>{escape(nome)}</strong></td><td>{escape(como)}</td><td>{escape(ev)}</td><td>{escape(nv)}</td></tr>')
tr += ['      </tbody>', '    </table>', '  </div>']
co = ['  <div class="tbl">', '    <table class="aud">', '      <caption>As perguntas de conscientização, requisito 7.3</caption>',
      '      <thead><tr><th style="width:40%">Pergunta</th><th>O que se espera ouvir</th></tr></thead>', '      <tbody>']
for perg, resp in CONSCIENTIZACAO:
    co.append(f'        <tr><td><strong>{escape(perg)}</strong></td><td>{escape(resp)}</td></tr>')
co += ['      </tbody>', '    </table>', '  </div>']

# ------------------------------------------------------------------ módulo 7: cobertura (pizzaria)
EX = EX1
ROT = ["Nível 3", "Nível 2", "Nível 1", "Nível 0"]
rows = []
for k, (cod, nome, _) in enumerate(EX["comps"]):
    ps = [p for p in EX["pessoas"] if requerido(EX, p)[k] > 0]
    cnt = [sum(1 for p in ps if p["niveis"][k] == n) for n in (3, 2, 1, 0)]
    rows.append((cod, nome, cnt))
X0, U, TOP, RH, BH = 300, 56, 58, 36, 20
bottom = TOP + RH * len(rows)
HH = bottom + 46
vmax = max(sum(c) for _, _, c in rows)
ch = [f'      <svg id="bars" viewBox="0 0 900 {HH}" role="img" aria-label="Gráfico de barras empilhadas com as pessoas da pizzaria em cada competência, por nível. '
      + " ".join(f"{cod}, {nome.lower()}: {c[0]} no nível 3, {c[1]} no nível 2, {c[2]} no nível 1 e {c[3]} no nível 0." for cod, nome, c in rows) + '">', '        <g font-size="11.5">']
xs = X0
for k, t in enumerate(ROT):
    ch.append(f'          <rect class="f{k + 1}" x="{xs}" y="12" width="14" height="14"/><text x="{xs + 22}" y="24">{t}</text>')
    xs += 40 + len(t) * 6.6
ch.append('        </g>')
for v in range(0, vmax + 1, 2):
    x = X0 + v * U
    ch.append(f'        <line class="grid" x1="{x}" y1="{TOP - 8}" x2="{x}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{x}" y="{bottom + 16}" font-size="11" text-anchor="middle" style="font-variant-numeric:tabular-nums">{v}</text>')
ch.append(f'        <text class="mono mu" x="{X0 + vmax * U / 2}" y="{bottom + 36}" font-size="10" text-anchor="middle">PESSOAS CUJA FUNÇÃO EXIGE A COMPETÊNCIA</text>')
for k, (cod, nome, c) in enumerate(rows):
    y = TOP + RH * k + (RH - BH) / 2
    t = sum(c)
    ch.append(f'        <text x="20" y="{y + 14:.1f}" font-size="11.5"><tspan class="b">{cod}</tspan> · {escape(nome)}</text>')
    x = X0
    for j, v in enumerate(c):
        if not v:
            continue
        ch.append(f'        <rect class="seg f{j + 1}" data-k="{k}" x="{x}" y="{y:.1f}" width="{v * U}" height="{BH}"/>')
        ch.append(f'        <text class="b {"on2" if j == 1 else "on"}" x="{x + v * U / 2}" y="{y + 14.5:.1f}" font-size="11" text-anchor="middle" pointer-events="none">{v}</text>')
        x += v * U
    cob = c[0] + c[1]
    ch.append(f'        <text class="halo" x="{x + 8}" y="{y + 14:.1f}" font-size="11.5"><tspan class="b">{cob}</tspan><tspan class="mu"> no nível 2 ou mais{"" if cob >= COBERTURA else " · dependência"}</tspan></text>')
for k, (cod, nome, c) in enumerate(rows):
    ch.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" '
              f'aria-label="{cod}, {escape(nome)}: {sum(c)} pessoas, {c[0]} no nível 3, {c[1]} no nível 2, {c[2]} no nível 1 e {c[3]} no nível 0" data-k="{k}" data-id="{cod}" data-n="{escape(nome)}" '
              f'data-t="{sum(c)}" data-n3="{c[0]}" data-n2="{c[1]}" data-n1="{c[2]}" data-n0="{c[3]}" data-cob="{c[0] + c[1]}" data-cx="{X0 + sum(c) * U / 2:.1f}"/>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>Competência</th><th class="c">Pessoas</th>' + "".join(f'<th class="c">{t}</th>' for t in ROT)
      + '<th class="c">No nível 2 ou mais</th></tr></thead>', '          <tbody>']
for cod, nome, c in rows:
    tb.append(f'            <tr><td><strong>{cod} · {escape(nome)}</strong></td><td class="c">{sum(c)}</td>' + "".join(f'<td class="c">{v}</td>' for v in c) + f'<td class="c">{c[0] + c[1]}</td></tr>')
tb += ['          </tbody>', '        </table>']
dep = [cod for cod, _, c in rows if c[0] + c[1] < COBERTURA]
NOMEC = {cod: nome for cod, nome, _ in rows}
sem3 = [cod for cod, _, c in rows if c[0] == 0]
charttext = (f'  <p>Na pizzaria, {dep[0]}, {NOMEC[dep[0]].lower()}, continua com uma só pessoa no nível 2 ou mais: o treinamento de Bruno foi eficaz só em parte, e o risco R6 segue aberto. '
             f'A leitura por nível 3 é a próxima: '
             f'{("a competência " + sem3[0] + " não tem" if len(sem3) == 1 else "as competências " + ", ".join(sem3) + " não têm") + " ninguém que treine os outros" if sem3 else "todas as competências têm quem treine"}. '
             'O atendimento no salão, C8, é o caso a observar: a competência ainda não tem padrão escrito, e o nível 2 de duas pessoas foi dado pela experiência, e não pelo padrão. '
             'Quando o padrão de atendimento for aprovado, as duas voltam ao nível 1 até serem treinadas nele.</p>')
assert dep == ["C3"], dep

# ------------------------------------------------------------------ módulo 10: figura da ISO
PASSOS = [("Determinar", "a competência de quem trabalha sob o controle da organização, inclusive terceiros", "Aba Funções: nível requerido por função"),
          ("Assegurar", "que as pessoas sejam competentes, por educação, treinamento ou experiência", "Aba Matriz: nível de cada pessoa, com evidência"),
          ("Agir", "para adquirir a competência que falta, e avaliar a eficácia", "Aba Plano: ação, aprendizado e eficácia"),
          ("Reter", "a evidência da competência", "Aba Registros: treinamentos e avaliações")]
iso = ['      <svg viewBox="0 0 900 190" role="img" aria-label="Os quatro passos do requisito 7.2. ' + " ".join(f"{a}: {b}. Neste estudo: {c}." for a, b, c in PASSOS) + '">',
       '        <defs><marker id="a10" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ah" d="M0 0 L10 5 L0 10 z"/></marker></defs>']
for k, (a, b, c) in enumerate(PASSOS):
    x = 10 + k * 222
    iso.append(f'        <rect class="bx" x="{x}" y="14" width="214" height="162"/>')
    iso.append(f'        <rect class="hd-ink" x="{x}" y="14" width="214" height="34"/>')
    iso.append(f'        <text class="b t-ground" x="{x + 14}" y="36" font-size="13">{k + 1} · {a}</text>')
    yy = 70
    for l in textwrap.wrap(b, 30):
        iso.append(f'        <text x="{x + 14}" y="{yy}" font-size="11.5">{escape(l)}</text>')
        yy += 16
    yy = 130
    for l in textwrap.wrap(c, 32):
        iso.append(f'        <text class="mu" x="{x + 14}" y="{yy}" font-size="11">{escape(l)}</text>')
        yy += 15
    if k < 3:
        iso.append(f'        <line class="ln" x1="{x + 215}" y1="95" x2="{x + 219}" y2="95" marker-end="url(#a10)"/>')
iso.append("      </svg>")

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--CICLO-->", "\n".join(ci)), ("<!--ESCALA-->", escala), ("<!--ANATOMIA-->", "\n".join(an)), ("<!--LINHA-->", "\n".join(li)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1COMPS-->", comps_tab(EX1)), ("<!--EX1MATRIZ-->", matriz_tab(EX1)), ("<!--EX1PLANO-->", plano_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2COMPS-->", comps_tab(EX2)), ("<!--EX2MATRIZ-->", matriz_tab(EX2)), ("<!--EX2PLANO-->", plano_tab(EX2)),
                 ("<!--TRILHA-->", "\n".join(tr)), ("<!--CONSC-->", "\n".join(co)), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)),
                 ("<!--CHARTTEXT-->", charttext), ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Matriz de competências</title>")
assert "Matriz de competências" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'),
      "| lacunas:", sum(len(lacunas(EX1, p)) for p in EX1["pessoas"]), sum(len(lacunas(EX2, p)) for p in EX2["pessoas"]), "| sem nível 3:", sem3)
