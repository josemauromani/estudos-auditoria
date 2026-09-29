# -*- coding: utf-8 -*-
"""Monta treinamento-riscos.html: CSS herdado do estudo de PDCA + corpo próprio + tabelas e figuras geradas dos dados."""
import os
import re
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from risk_data import (ACEITAR, ACEITE, CHECK, CONDUTA, EX1, EX2, IMPACTO, NIVEIS, OPORT, PROB, RESP_TXT, contagem, nivel,  # noqa: E402
                       prioridade)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# níveis de risco: paleta validada para daltonismo nos dois modos (azul, âmbar, vermelho e roxo)
LIGHT = ("\n  --l1:#2A6FB0; --l1-tint:#DCE8F3;\n  --l2:#D19A2E; --l2-tint:#F8EBCB;\n  --l3:#B0413E; --l3-tint:#F5DEDC;"
         "\n  --l4:#7A3E9A; --l4-tint:#E9DEF1;\n  --on-l2:#16242E;\n  --tp:#1E7B73; --ti:#5B6B76;")
DARK = ("\n  --l1:#4F97DB; --l1-tint:#1B2F42;\n  --l2:#B58E14; --l2-tint:#3A2C12;\n  --l3:#D14B45; --l3-tint:#3D1F1E;"
        "\n  --l4:#A45BC0; --l4-tint:#2E2140;\n  --on-l2:#0F171C;\n  --tp:#5FC6BA; --ti:#9BABB6;")
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Probabilidade, impacto e níveis */
.tiles .tp{background:var(--tp)} .tiles .ti{background:var(--ti)}
.k.tp{background:var(--tp)} .k.ti{background:var(--ti)}
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.l1{background:var(--l1)} .chip.l2{background:var(--l2);color:var(--on-l2)} .chip.l3{background:var(--l3)} .chip.l4{background:var(--l4)}
.chip.sl{background:var(--muted)}
svg .hd-ink{fill:var(--ink)}
svg .bx-out2{fill:var(--sunk);stroke:var(--rule);stroke-width:1.5}
svg .cl1{fill:var(--l1-tint)} svg .cl2{fill:var(--l2-tint)} svg .cl3{fill:var(--l3-tint)} svg .cl4{fill:var(--l4-tint)}
svg .cell{stroke:var(--surface);stroke-width:2}
svg .sw1{fill:var(--l1)} svg .sw2{fill:var(--l2)} svg .sw3{fill:var(--l3)} svg .sw4{fill:var(--l4)}
svg .bx-l1{fill:var(--l1-tint);stroke:var(--l1);stroke-width:1.5}
svg .bx-l3{fill:var(--l3-tint);stroke:var(--l3);stroke-width:1.5}
svg .ini{fill:var(--surface);stroke:var(--ink);stroke-width:2}
svg .res{fill:var(--accent);stroke:var(--surface);stroke-width:2}
svg .lk{stroke:var(--muted);stroke-width:2}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas dos exemplos */
table.aud{font-size:.8rem;min-width:860px;line-height:1.4}
table.aud th, table.aud td{padding:8px 9px}
table.aud td.n{white-space:nowrap;font-weight:600;color:var(--muted)}
table.aud td.c{text-align:center;font-variant-numeric:tabular-nums}
table.aud td small{display:block;color:var(--muted);font-size:.76rem;margin-top:3px}
table.aud td .chip + .chip{margin-left:4px}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha da matriz (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += "\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"

LV = {n: k for k, n in enumerate(NIVEIS, 1)}


def dt(d):
    return d.strftime("%d/%m/%Y")


def br(v, casas=1):
    s = f"{v:.{casas}f}".replace(".", ",")
    return s[:-2] if s.endswith(",0") else s


def chip(pts):
    n = nivel(pts)
    return f'<span class="chip l{LV[n]}">{pts} · {n}</span>'


def escalas():
    o = ['  <div class="tbl">', '    <table>',
         '      <thead><tr><th style="width:8%">Nota</th><th style="width:16%">Probabilidade</th><th style="width:30%">O evento acontece</th>'
         '<th style="width:14%">Impacto</th><th>Se acontecer</th></tr></thead>', '      <tbody>']
    for (n, pn, pd), (_, im, idesc) in zip(PROB, IMPACTO):
        o.append(f'        <tr><td class="num">{n}</td><td><strong>{pn}</strong></td><td>{escape(pd)}</td><td><strong>{im}</strong></td><td>{escape(idesc)}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def conduta():
    o = ['  <div class="tbl">', '    <table>',
         '      <thead><tr><th style="width:18%">Nível</th><th style="width:16%">Pontos</th><th>Conduta</th></tr></thead>', '      <tbody>']
    for n, faixa, txt in CONDUTA:
        o.append(f'        <tr><td><span class="chip l{LV[n]}">{n}</span></td><td class="num">{faixa}</td><td>{escape(txt)}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def respostas():
    o = ['  <div class="tbl">', '    <table>',
         '      <thead><tr><th style="width:15%">Resposta</th><th style="width:34%">O que é</th><th style="width:22%">Efeito no risco</th><th>Exemplo</th></tr></thead>',
         '      <tbody>']
    for r, oque, efeito, exemplo in RESP_TXT:
        o.append(f'        <tr><td><strong>{r}</strong></td><td>{escape(oque)}</td><td>{escape(efeito)}</td><td>{escape(exemplo)}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def exemplo(ex):
    h, rs = ex["head"], ex["riscos"]
    ci, cr = contagem(ex), contagem(ex, "nivelr")
    o = ['  <dl class="ficha">',
         f'    <div><dt>Processo</dt><dd>{escape(h["processo"])}</dd></div>',
         f'    <div><dt>Objetivo</dt><dd>{escape(h["objetivo"])}</dd></div>',
         f'    <div><dt>Data e participantes</dt><dd>{dt(h["data"])}. {escape(h["por"])}</dd></div>',
         f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
         '  </dl>',
         '  <div class="tbl">', '    <table class="aud">',
         '      <thead><tr><th>Nº</th><th style="width:15%">Causa</th><th style="width:15%">Evento</th><th style="width:16%">Consequência</th>'
         '<th>P</th><th>I</th><th style="width:10%">Nível inicial</th><th style="width:25%">Resposta e ação</th><th style="width:10%">Nível residual</th></tr></thead>',
         '      <tbody>']
    for r in rs:
        if r["resp"] == ACEITAR:
            acao = f'<strong>Aceitar.</strong> {escape(ACEITE[r["id"]])}<small>{escape(r["quem"])}</small>'
        else:
            acao = f'<strong>{r["resp"]}.</strong> {escape(r["acao"])}<small>{escape(r["quem"])}, até {dt(r["prazo"])}</small>'
        o.append(f'        <tr><td class="n">{r["id"]}</td><td>{escape(r["causa"])}</td><td>{escape(r["evento"])}</td><td>{escape(r["conseq"])}</td>'
                 f'<td class="c">{r["p"]}</td><td class="c">{r["i"]}</td><td>{chip(r["pts"])}</td><td>{acao}</td>'
                 f'<td>{chip(r["ptsr"])}<small>P {r["pr"]} × I {r["ir"]}</small></td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    altos = ci["Alto"] + ci["Crítico"]
    o.append(f'  <p><strong>Resultado.</strong> Dos {len(rs)} riscos, {altos} começam nas faixas alta ou crítica, e {cr["Alto"] + cr["Crítico"] or "nenhum"} '
             f'fica nelas depois das respostas. A média cai de {br(sum(r["pts"] for r in rs) / len(rs))} para '
             f'{br(sum(r["ptsr"] for r in rs) / len(rs))} pontos. A revisão da matriz está marcada para {dt(h["revisao"])}.</p>')
    return "\n".join(o)


def oport():
    o = ['  <div class="tbl">', '    <table class="aud">',
         '      <thead><tr><th>Nº</th><th style="width:26%">Oportunidade</th><th>Probabilidade</th><th>Benefício</th><th style="width:11%">Prioridade</th>'
         '<th style="width:12%">Decisão</th><th style="width:26%">Ação</th><th>Responsável</th></tr></thead>', '      <tbody>']
    cls = {"Alta": "l1", "Média": "sl", "Baixa": "sl"}
    for i, txt, p, b, dec, acao, quem in OPORT:
        pr = prioridade(p * b)
        o.append(f'        <tr><td class="n">{i}</td><td>{escape(txt)}</td><td class="c">{p}</td><td class="c">{b}</td>'
                 f'<td><span class="chip {cls[pr]}">{p * b} · {pr}</span></td><td><strong>{dec}</strong></td><td>{escape(acao)}</td><td>{escape(quem)}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


# ---- matriz 5 × 5 (figuras 4 e 5)
GX, GY, CW, CH = 190, 34, 106, 56


def heat(conteudo, aria, ident=""):
    o = [f'      <svg {ident}viewBox="0 0 900 392" role="img" aria-label="{escape(aria)}">']
    o.append(f'        <text class="mono mu" x="24" y="{GY + 2.5 * CH}" font-size="10" text-anchor="middle" transform="rotate(-90 24 {GY + 2.5 * CH})">IMPACTO</text>')
    for row, (n, nome, _) in enumerate(reversed(IMPACTO)):
        y = GY + row * CH
        o.append(f'        <text x="{GX - 12}" y="{y + CH / 2 + 4}" font-size="11.5" text-anchor="end"><tspan class="b">{n}</tspan> · {nome}</text>')
        for col, (p, _, _) in enumerate(PROB):
            x = GX + col * CW
            pts = p * n
            o.append(f'        <rect class="cell cl{LV[nivel(pts)]}" x="{x}" y="{y}" width="{CW}" height="{CH}"/>')
            o += conteudo(p, n, pts, x, y)
    yb = GY + 5 * CH
    for col, (p, nome, _) in enumerate(PROB):
        x = GX + col * CW + CW / 2
        o.append(f'        <text class="b" x="{x}" y="{yb + 20}" font-size="11.5" text-anchor="middle">{p}</text>')
        o.append(f'        <text class="mu" x="{x}" y="{yb + 36}" font-size="11" text-anchor="middle">{nome}</text>')
    o.append(f'        <text class="mono mu" x="{GX + 2.5 * CW}" y="{yb + 62}" font-size="10" text-anchor="middle">PROBABILIDADE</text>')
    for k, (n, faixa, _) in enumerate(reversed(CONDUTA)):
        y = GY + 30 + k * 50
        o.append(f'        <rect class="sw{LV[n]}" x="748" y="{y}" width="14" height="14"/>')
        o.append(f'        <text class="b" x="770" y="{y + 12}" font-size="12">{n}</text>')
        o.append(f'        <text class="mu" x="770" y="{y + 29}" font-size="11">{faixa} pontos</text>')
    o.append("      </svg>")
    return "\n".join(o)


def cel_pontos(p, i, pts, x, y):
    return [f'        <text class="b" x="{x + CW / 2}" y="{y + 27}" font-size="15" text-anchor="middle" style="font-variant-numeric:tabular-nums">{pts}</text>',
            f'        <text class="mu" x="{x + CW / 2}" y="{y + 44}" font-size="10.5" text-anchor="middle">{nivel(pts)}</text>']


def cel_riscos(ex):
    def f(p, i, pts, x, y):
        ids = [r["id"] for r in ex["riscos"] if r["p"] == p and r["i"] == i]
        o = [f'        <text class="mono mu" x="{x + 8}" y="{y + 15}" font-size="9.5">{pts}</text>']
        if ids:
            o.append(f'        <text class="b" x="{x + CW / 2}" y="{y + 36}" font-size="13.5" text-anchor="middle">{" · ".join(ids)}</text>')
        return o
    return f


matriz = heat(cel_pontos, "Matriz de probabilidade e impacto, com cinco níveis em cada eixo. Os pontos são o produto das duas notas. "
              "De 1 a 4 pontos, o nível é baixo. De 5 a 9, médio. De 10 a 16, alto. De 20 a 25, crítico.")
mapa2 = heat(cel_riscos(EX2), "Os oito riscos do exemplo 2 na matriz, antes das respostas. "
             + " ".join(f'{r["id"]}: probabilidade {r["p"]}, impacto {r["i"]}, {r["pts"]} pontos, nível {r["nivel"].lower()}.' for r in EX2["riscos"]))

# ---- figura 7: risco inicial e risco residual do exemplo 2
RS = EX2["riscos"]
X0, U, TOP, RH = 340, 20, 44, 34
bottom = TOP + RH * len(RS)
HH = bottom + 74
sx = lambda v: X0 + v * U  # noqa: E731
ch = [f'      <svg id="dots" viewBox="0 0 900 {HH}" role="img" aria-label="Gráfico com o risco inicial e o risco residual dos oito riscos do exemplo 2, em pontos de 1 a 25. '
      + " ".join(f'{r["id"]}: de {r["pts"]} para {r["ptsr"]}.' for r in RS) + '">']
for k, (a, b, nome) in enumerate([(0.5, 4.5, "BAIXO"), (4.5, 9.5, "MÉDIO"), (9.5, 18, "ALTO"), (18, 25.5, "CRÍTICO")], 1):
    ch.append(f'        <rect class="cl{k}" x="{sx(a):.1f}" y="{TOP - 8}" width="{sx(b) - sx(a) - 2:.1f}" height="{bottom - TOP + 8}"/>')
    ch.append(f'        <text class="mono mu" x="{(sx(a) + sx(b)) / 2:.1f}" y="{TOP - 16}" font-size="9.5" text-anchor="middle">{nome}</text>')
for v in (1, 5, 10, 15, 20, 25):
    ch.append(f'        <text class="mu" x="{sx(v)}" y="{bottom + 16}" font-size="11" text-anchor="middle" style="font-variant-numeric:tabular-nums">{v}</text>')
ch.append(f'        <text class="mono mu" x="{sx(13)}" y="{bottom + 36}" font-size="10" text-anchor="middle">PONTOS · PROBABILIDADE × IMPACTO</text>')
for k, r in enumerate(RS):
    y = TOP + RH * k + RH / 2
    ch.append(f'        <text x="20" y="{y + 4:.1f}" font-size="11.5"><tspan class="b">{r["id"]}</tspan> · {escape(r["evento"])}</text>')
    xa, xb = sx(r["pts"]), sx(r["ptsr"])
    if r["pts"] == r["ptsr"]:
        ch.append(f'        <circle class="mk ini" data-k="{k}" cx="{xa}" cy="{y:.1f}" r="9"/>')
        ch.append(f'        <circle class="mk res" data-k="{k}" cx="{xa}" cy="{y:.1f}" r="5.5"/>')
        ch.append(f'        <text class="b" x="{xa + 16}" y="{y + 4:.1f}" font-size="11.5">{r["pts"]}<tspan class="mu" font-weight="400"> · aceito</tspan></text>')
    else:
        ch.append(f'        <line class="mk lk" data-k="{k}" x1="{xb + 8}" y1="{y:.1f}" x2="{xa - 8}" y2="{y:.1f}"/>')
        ch.append(f'        <circle class="mk ini" data-k="{k}" cx="{xa}" cy="{y:.1f}" r="6"/>')
        ch.append(f'        <circle class="mk res" data-k="{k}" cx="{xb}" cy="{y:.1f}" r="6.5"/>')
        ch.append(f'        <text x="{xa + 13}" y="{y + 4:.1f}" font-size="11.5">{r["pts"]}</text>')
        ch.append(f'        <text class="b" x="{xb - 13}" y="{y + 4:.1f}" font-size="11.5" text-anchor="end">{r["ptsr"]}</text>')
ly = bottom + 62
ch += [f'        <circle class="ini" cx="28" cy="{ly - 4}" r="6"/><text x="42" y="{ly}" font-size="11.5">risco inicial</text>',
       f'        <circle class="res" cx="158" cy="{ly - 4}" r="6.5"/><text x="172" y="{ly}" font-size="11.5">risco residual, depois da resposta</text>']
for k, r in enumerate(RS):
    ch.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" '
              f'aria-label="{r["id"]}, {escape(r["evento"])}: de {r["pts"]} para {r["ptsr"]} pontos" data-k="{k}" data-id="{r["id"]}" '
              f'data-ev="{escape(r["evento"])}" data-a="{r["pts"]}" data-b="{r["ptsr"]}" data-na="{r["nivel"].lower()}" data-nb="{r["nivelr"].lower()}" '
              f'data-r="{r["resp"].lower()}" data-cx="{(sx(r["pts"]) + sx(r["ptsr"])) / 2:.1f}"/>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>Nº</th><th>Evento</th><th>Resposta</th><th>Inicial</th><th>Residual</th><th>Redução</th></tr></thead>',
      '          <tbody>']
for r in RS:
    tb.append(f'            <tr><td class="n">{r["id"]}</td><td>{escape(r["evento"])}</td><td>{r["resp"]}</td><td>{chip(r["pts"])}</td><td>{chip(r["ptsr"])}</td>'
              f'<td class="c">{r["pts"] - r["ptsr"]}</td></tr>')
tb += ['          </tbody>', '        </table>']

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--ESCALAS-->", escalas()), ("<!--MATRIZ-->", matriz), ("<!--CONDUTA-->", conduta()), ("<!--EX1-->", exemplo(EX1)),
                 ("<!--EX2-->", exemplo(EX2)), ("<!--MAPA2-->", mapa2), ("<!--OPORT-->", oport()), ("<!--RESPOSTAS-->", respostas()),
                 ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Matriz de riscos na prática</title>")
assert "Matriz de riscos" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'),
      "| EX1", contagem(EX1), "->", contagem(EX1, "nivelr"), "| EX2", contagem(EX2), "->", contagem(EX2, "nivelr"))
