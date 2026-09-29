# -*- coding: utf-8 -*-
"""Monta treinamento-indicadores.html: CSS herdado do estudo de PDCA + corpo próprio + tabelas e gráficos gerados dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ind_data import (ATENCAO, CHECK, EX1, EX2, FORA, LEITURAS, MAIOR, MESES, NA_META, QUADRO, acao, atende, seguidos, situacao,  # noqa: E402
                      tendencia)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# situações: paleta validada para daltonismo nos dois modos (azul, âmbar e vermelho)
LIGHT = ("\n  --s1:#2A6FB0; --s1-tint:#DCE8F3;\n  --s2:#D19A2E; --s2-tint:#F8EBCB;\n  --s3:#B0413E; --s3-tint:#F5DEDC;\n  --on-s2:#16242E;")
DARK = ("\n  --s1:#4F97DB; --s1-tint:#1B2F42;\n  --s2:#B58E14; --s2-tint:#3A2C12;\n  --s3:#D14B45; --s3-tint:#3D1F1E;\n  --on-s2:#0F171C;")
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Situação do indicador */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.s1{background:var(--s1)} .chip.s2{background:var(--s2);color:var(--on-s2)} .chip.s3{background:var(--s3)}
svg .hd-ink{fill:var(--ink)}
svg .bx-out2{fill:var(--sunk);stroke:var(--rule);stroke-width:1.5}
svg .z1{fill:var(--s1-tint);stroke:var(--surface);stroke-width:2}
svg .z2{fill:var(--s2-tint);stroke:var(--surface);stroke-width:2}
svg .z3{fill:var(--s3-tint);stroke:var(--surface);stroke-width:2}
svg .goal2{stroke:var(--muted);stroke-width:1.5;stroke-dasharray:2 4;fill:none}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas dos exemplos */
table.aud{font-size:.8rem;min-width:860px;line-height:1.4}
table.aud th, table.aud td{padding:8px 9px}
table.aud td.n{white-space:nowrap;font-weight:600;color:var(--muted)}
table.aud td.c{text-align:center;font-variant-numeric:tabular-nums;white-space:nowrap}
table.aud th.c{text-align:center}
table.aud td.out{background:var(--sunk)}
table.aud td small{display:block;color:var(--muted);font-size:.76rem;margin-top:3px}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha do painel (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += "\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"

CHIP = {NA_META: "s1", ATENCAO: "s2", FORA: "s3"}


def dt(d):
    return d.strftime("%d/%m/%Y")


def casas(ind):
    return 0 if all(float(v).is_integer() for v in ind["valores"] + [ind["meta"], ind["limite"]]) else 1


def num(v, c):
    return f"{v:.{c}f}".replace(".", ",")


def meta_txt(ind):
    c = casas(ind)
    pre = "No mínimo" if ind["sentido"] == MAIOR else "Até"
    un = "%" if ind["unidade"] == "%" else ""
    return f"{pre} {num(ind['meta'], c)}{un}"


def chip(s):
    return f'<span class="chip {CHIP[s]}">{s}</span>'


def exemplo(ex):
    h = ex["head"]
    o = ['  <dl class="ficha">',
         f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
         f'    <div><dt>Período</dt><dd>{escape(h["periodo"])}</dd></div>',
         f'    <div><dt>Reunião de análise</dt><dd>{escape(h["reuniao"])}</dd></div>',
         f'    <div><dt>Responsável</dt><dd>{escape(h["por"])}</dd></div>',
         '  </dl>',
         '  <div class="tbl">', '    <table class="aud">', '      <caption>Fichas dos indicadores</caption>',
         '      <thead><tr><th>Nº</th><th style="width:22%">Indicador e objetivo</th><th style="width:27%">Fórmula</th><th style="width:11%">Meta</th>'
         '<th style="width:9%">Limite de atenção</th><th style="width:17%">Fonte dos dados</th><th>Responsável</th></tr></thead>', '      <tbody>']
    for i in ex["inds"]:
        c = casas(i)
        un = "%" if i["unidade"] == "%" else ""
        o.append(f'        <tr><td class="n">{i["id"]}</td><td><strong>{escape(i["nome"])}</strong><small>{escape(i["objetivo"])}</small></td>'
                 f'<td>{escape(i["formula"])}<small>{escape(i["unidade"]).capitalize() if not un else "Percentual"} · {i["sentido"].lower()}</small></td>'
                 f'<td>{meta_txt(i)}</td><td class="c">{num(i["limite"], c)}{un}</td><td>{escape(i["fonte"])}</td><td>{escape(i["resp"])}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>',
          '  <div class="tbl">', '    <table class="aud">', f'      <caption>Resultados · situação em {dt(h["data"])}</caption>',
          '      <thead><tr><th>Nº</th>' + "".join(f'<th class="c">{m}</th>' for m in MESES[-6:])
          + '<th class="c" style="width:7%">Média do ano</th><th style="width:11%">Situação</th><th class="c" style="width:8%">Seguidos fora</th>'
            '<th style="width:10%">Tendência</th><th style="width:28%">Decisão</th></tr></thead>', '      <tbody>']
    for i in ex["inds"]:
        c = casas(i)
        v = i["valores"]
        cel = "".join(f'<td class="c{"" if atende(x, i) else " out"}">{num(x, c)}</td>' for x in v[-6:])
        o.append(f'        <tr><td class="n">{i["id"]}</td>{cel}<td class="c">{num(sum(v) / 12, 1)}</td><td>{chip(situacao(v[-1], i))}</td>'
                 f'<td class="c">{seguidos(i)}</td><td>{tendencia(i)}</td><td><strong>{acao(i)}.</strong> {escape(i["decisao"])}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>',
          '  <p class="leg"><small>As células com fundo cinza são os meses em que o resultado não atendeu à meta.</small></p>']
    if "analise" in ex:
        o += ['  <div class="tbl">', '    <table class="aud">', '      <caption>Registro da reunião de análise</caption>',
              '      <thead><tr><th>Nº</th><th style="width:27%">O que os dados mostram</th><th style="width:25%">Causa provável</th>'
              '<th style="width:25%">Decisão</th><th>Responsável e prazo</th></tr></thead>', '      <tbody>']
        for d, ident, mostra, causa, dec, quem, prazo in ex["analise"]:
            o.append(f'        <tr><td class="n">{ident}</td><td>{escape(mostra)}</td><td>{escape(causa)}</td><td>{escape(dec)}</td>'
                     f'<td>{escape(quem)}<small>até {dt(prazo)}</small></td></tr>')
        o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def quadro():
    o = ['  <div class="tbl">', '    <table class="aud">',
         '      <thead><tr><th style="width:20%">Objetivo</th><th style="width:22%">Indicador</th><th style="width:13%">Meta</th><th class="c">Resultado</th>'
         '<th style="width:12%">Situação</th><th>Decisão</th></tr></thead>', '      <tbody>']
    for obj, ind, meta, res, sit, dec in QUADRO:
        o.append(f'        <tr><td><strong>{escape(obj)}</strong></td><td>{escape(ind)}</td><td>{escape(meta)}</td><td class="c">{res}</td>'
                 f'<td>{chip(sit)}</td><td>{escape(dec)}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


# ---- figura 6: prazo de atendimento das requisições (exemplo 2, indicador C1)
C1 = EX2["inds"][0]
V = C1["valores"]
X0, DX, YB, YT, VMIN, VMAX = 100, 66, 270, 40, 3, 7
cx = lambda i: X0 + i * DX  # noqa: E731
cy = lambda v: YB - (v - VMIN) * (YB - YT) / (VMAX - VMIN)  # noqa: E731
fora = [i for i, v in enumerate(V) if not atende(v, C1)]
n_seg = seguidos(C1)
ini = len(V) - n_seg
ch = [f'      <svg id="run" viewBox="0 0 900 340" role="img" aria-label="Gráfico de linha com o prazo médio de atendimento das requisições, em dias úteis, '
      f'de {MESES[0]} a {MESES[-1]}. A meta é de até {num(C1["meta"], 1)} dias, e o limite de atenção, de {num(C1["limite"], 1)}. '
      f'Em {MESES[2]}, o resultado foi de {num(V[2], 1)}, acima da meta, e voltou no mês seguinte. De {MESES[ini]} a {MESES[-1]}, o resultado ficou acima da meta '
      f'por {n_seg} meses seguidos, com pico de {num(max(V), 1)} em {MESES[V.index(max(V))]}.">',
      f'        <rect class="band" x="70" y="{cy(C1["limite"]):.1f}" width="790" height="{cy(C1["meta"]) - cy(C1["limite"]):.1f}"/>']
for v in range(VMIN, VMAX + 1):
    ch.append(f'        <line class="grid" x1="70" y1="{cy(v):.1f}" x2="860" y2="{cy(v):.1f}"/>')
    ch.append(f'        <text class="mu" x="62" y="{cy(v) + 4:.1f}" font-size="11" text-anchor="end" style="font-variant-numeric:tabular-nums">{v}</text>')
ch.append('        <g font-size="10.5" text-anchor="middle">' + "".join(f'<text class="mu" x="{cx(i)}" y="290">{m}</text>' for i, m in enumerate(MESES)) + "</g>")
ch += [f'        <line class="goal" x1="70" y1="{cy(C1["meta"]):.1f}" x2="860" y2="{cy(C1["meta"]):.1f}"/>',
       f'        <text x="856" y="{cy(C1["meta"]) + 17:.1f}" font-size="11.5" text-anchor="end"><tspan class="b">meta</tspan> até {num(C1["meta"], 1)}</text>',
       f'        <line class="goal2" x1="70" y1="{cy(C1["limite"]):.1f}" x2="860" y2="{cy(C1["limite"]):.1f}"/>',
       f'        <text x="74" y="{cy(C1["limite"]) - 8:.1f}" font-size="11.5"><tspan class="b">limite de atenção</tspan> {num(C1["limite"], 1)}</text>',
       f'        <text class="mu" x="430" y="{cy(C1["limite"]) + 18:.1f}" font-size="11">faixa de atenção</text>',
       f'        <line class="xh" id="run-xh" x1="0" y1="{YT}" x2="0" y2="{YB}" visibility="hidden"/>',
       '        <polyline class="series" points="' + " ".join(f"{cx(i)},{cy(v):.1f}" for i, v in enumerate(V)) + '"/>',
       '        <g id="run-pts">' + "".join(f'<circle class="pt" cx="{cx(i)}" cy="{cy(v):.1f}" r="5"/>' for i, v in enumerate(V)) + "</g>"]
imax = V.index(max(V))
ch += [f'        <text x="{cx(2) + 12}" y="{cy(V[2]) - 6:.1f}" font-size="12"><tspan class="b">{num(V[2], 1)}</tspan> · ponto isolado</text>',
       f'        <text class="b" x="{cx(imax)}" y="{cy(V[imax]) - 12:.1f}" font-size="12" text-anchor="middle">{num(V[imax], 1)}</text>',
       f'        <text class="b" x="{cx(11) + 12}" y="{cy(V[11]) + 4:.1f}" font-size="12">{num(V[11], 1)}</text>',
       f'        <path class="ln-mu" d="M{cx(ini) - 22} 58 V50 H{cx(11) + 22} V58" stroke-width="1"/>',
       f'        <text x="{(cx(ini) + cx(11)) / 2}" y="40" font-size="11.5" text-anchor="middle"><tspan class="b">{n_seg} meses seguidos</tspan> acima da meta</text>',
       '        <line class="series" x1="70" y1="322" x2="98" y2="322"/><circle class="pt" cx="84" cy="322" r="4"/>',
       '        <text x="106" y="326" font-size="11.5">prazo médio de atendimento, em dias úteis</text>',
       '        <line class="goal" x1="400" y1="322" x2="428" y2="322"/><text x="436" y="326" font-size="11.5">meta</text>',
       '        <line class="goal2" x1="500" y1="322" x2="528" y2="322"/><text x="536" y="326" font-size="11.5">limite de atenção</text>']
run = 0
linhas = []
for i, (m, v) in enumerate(zip(MESES, V)):
    run = 0 if atende(v, C1) else run + 1
    s = situacao(v, C1)
    linhas.append((m, v, s, run))
    ch.append(f'        <rect class="hit" x="{cx(i) - DX / 2}" y="{YT}" width="{DX}" height="{YB - YT}" tabindex="0" role="img" '
              f'aria-label="{m}: {num(v, 1)} dias úteis, {s.lower()}" data-i="{i}" data-v="{num(v, 1)}" data-p="{m}" data-s="{s.lower()}" data-n="{run}"/>')
ch.append("      </svg>")
tb = ['        <table>', '          <thead><tr><th>Mês</th><th>Prazo médio, em dias úteis</th><th>Situação</th><th>Meses seguidos fora da meta</th></tr></thead>',
      '          <tbody>']
for m, v, s, run in linhas:
    tb.append(f'            <tr><td>{m}</td><td class="num">{num(v, 1)}</td><td>{s}</td><td class="num">{run}</td></tr>')
tb += ['          </tbody>', '        </table>']

# ---- figura 7: três leituras
PW, PX = 280, [20, 310, 600]
ly = lambda v: 150 - (v - 3.5) * (110 / 3)  # noqa: E731
lt = ['      <svg viewBox="0 0 900 262" role="img" aria-label="Três leituras de um gráfico com meta de no máximo 5. '
      + " ".join(f"{t}: {d.lower()} {a}" for t, d, a, _ in LEITURAS) + '">']
for x0, (t, d, a, vals) in zip(PX, LEITURAS):
    lt.append(f'        <rect class="bx" x="{x0}" y="10" width="{PW}" height="242"/>')
    lt.append(f'        <text class="b" x="{x0 + 16}" y="34" font-size="13">{t}</text>')
    lt.append(f'        <line class="goal" x1="{x0 + 16}" y1="{ly(5):.1f}" x2="{x0 + PW - 16}" y2="{ly(5):.1f}"/>')
    lt.append(f'        <text class="mu" x="{x0 + 16}" y="{ly(5) - 6:.1f}" font-size="10.5">meta</text>')
    pts = [(x0 + 30 + k * 30, ly(v)) for k, v in enumerate(vals)]
    lt.append('        <polyline class="series" points="' + " ".join(f"{x},{y:.1f}" for x, y in pts) + '"/>')
    lt += [f'        <circle class="pt" cx="{x}" cy="{y:.1f}" r="4.5"/>' for x, y in pts]
    yy = 184
    for k, texto in enumerate((d, a)):
        for linha in textwrap.wrap(texto, 44):
            lt.append(f'        <text{" class=" + chr(34) + "mu" + chr(34) if k == 0 else ""} x="{x0 + 16}" y="{yy}" font-size="11.5">{escape(linha)}</text>')
            yy += 16
        yy += 4
lt.append("      </svg>")

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--EX1-->", exemplo(EX1)), ("<!--EX2-->", exemplo(EX2)), ("<!--QUADRO-->", quadro()), ("<!--CHART-->", "\n".join(ch)),
                 ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--LEITURAS-->", "\n".join(lt)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Indicadores na prática</title>")
assert "Indicadores" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'),
      "| C1:", n_seg, "meses seguidos, pico", max(V))
