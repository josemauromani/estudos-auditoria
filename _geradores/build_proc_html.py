# -*- coding: utf-8 -*-
"""Monta treinamento-processos.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from proc_data import (APOIO, CHECK, ELEMENTOS, EX1, EX2, GESTAO, IND, IND_TIPO, INTER, NAO, ORDEM_PARTES, PARCIAL, PARTES, PRINCIPAL,  # noqa: E402
                       SIM, fornece, recebe)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)
# as cores dos três tipos de processo são as do estudo de PDCA: azul (gestão), âmbar (principal) e verde-azulado (apoio)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Tipos de processo */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.p{background:var(--p)} .chip.d{background:var(--d)} .chip.c{background:var(--c)} .chip.sl{background:var(--muted)}
svg .hd-ink{fill:var(--ink)}
svg .bx-out2{fill:var(--sunk);stroke:var(--rule);stroke-width:1.5}
svg .band2{fill:var(--sunk)}
svg .diag{fill:var(--sunk)}
svg .dot{fill:var(--ink)}
svg .seg{fill:var(--accent)}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas dos exemplos */
table.aud{font-size:.8rem;min-width:860px;line-height:1.4}
table.aud th, table.aud td{padding:8px 9px}
table.aud td.n{white-space:nowrap;font-weight:600;color:var(--muted)}
table.aud td.c, table.aud th.c{text-align:center;font-variant-numeric:tabular-nums}
table.aud td.lb{width:17%;font-weight:600}
table.aud td.lb small{display:block;font:500 .66rem/1 var(--mono);letter-spacing:.1em;color:var(--muted);margin-bottom:4px}
table.aud td.v0{background:var(--bad-tint)} table.aud td.v1{background:var(--d-tint)}
table.aud td ul{margin:0;padding-left:1.1em;display:block}
table.aud td li + li{margin-top:3px}
table.aud td small{color:var(--muted);font-size:.76rem}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha do mapa (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr)}}\n")

TCLS = {GESTAO: "p", PRINCIPAL: "d", APOIO: "c"}


def dt(d):
    return d.strftime("%d/%m/%Y")


def br(v, casas=1):
    return f"{v:.{casas}f}".replace(".", ",")


def chip(tipo):
    return f'<span class="chip {TCLS[tipo]}">{tipo}</span>'


# ------------------------------------------------------------------ mapa de processos
def mapa(gestao, principais, apoio, cin, cout, aria):
    o = [f'      <svg viewBox="0 0 900 372" role="img" aria-label="{escape(aria)}">',
         '        <defs><marker id="am" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path class="ah" d="M0 0 L10 5 L0 10 z"/></marker></defs>']
    for x, rot, txt in ((10, "ENTRADA", cin), (810, "RESULTADO", cout)):
        cx = x + 40
        o.append(f'        <rect class="bx-ink" x="{x}" y="20" width="80" height="332"/>')
        o.append(f'        <text class="mono t-ground" x="{cx - 14}" y="186" font-size="10" text-anchor="middle" transform="rotate(-90 {cx - 14} 186)">{rot}</text>')
        o.append(f'        <text class="b t-ground" x="{cx + 10}" y="186" font-size="12.5" text-anchor="middle" transform="rotate(-90 {cx + 10} 186)">{escape(txt)}</text>')
    for y, rot, itens, cls, chev in ((20, "PROCESSOS DE GESTÃO", gestao, "bx-p", False), (138, "PROCESSOS PRINCIPAIS", principais, "bx-d", True),
                                     (256, "PROCESSOS DE APOIO", apoio, "bx-c", False)):
        o.append(f'        <rect class="band2" x="120" y="{y}" width="660" height="96"/>')
        o.append(f'        <text class="mono mu" x="132" y="{y + 17}" font-size="9.5">{rot}</text>')
        n = len(itens)
        w = (636 - 12 * (n - 1)) / n
        for k, (ident, nome) in enumerate(itens):
            x = 132 + k * (w + 12)
            yb = y + 28
            if chev:
                a = 12
                pts = f"{x:.1f},{yb} {x + w - a:.1f},{yb} {x + w:.1f},{yb + 29} {x + w - a:.1f},{yb + 58} {x:.1f},{yb + 58}" + (f" {x + a:.1f},{yb + 29}" if k else "")
                o.append(f'        <polygon class="{cls}" points="{pts}"/>')
                tx = x + (a if k else 0) + (w - a - (a if k else 0)) / 2
            else:
                o.append(f'        <rect class="{cls}" x="{x:.1f}" y="{yb}" width="{w:.1f}" height="58"/>')
                tx = x + w / 2
            linhas = textwrap.wrap(nome, max(10, int((w - (30 if chev else 16)) / 6.4)))[:2]
            y0 = yb + (37 if len(linhas) == 1 else 30) - (0 if not ident else -4)
            if ident:
                o.append(f'        <text class="mono mu" x="{tx:.1f}" y="{yb + 15}" font-size="9.5" text-anchor="middle">{ident}</text>')
            for j, l in enumerate(linhas):
                o.append(f'        <text class="b" x="{tx:.1f}" y="{y0 + j * 15}" font-size="11.5" text-anchor="middle">{escape(l)}</text>')
    o += ['        <line class="ln" x1="92" y1="195" x2="116" y2="195" marker-end="url(#am)"/>',
          '        <line class="ln" x1="782" y1="195" x2="806" y2="195" marker-end="url(#am)"/>',
          '        <line class="ln" x1="450" y1="118" x2="450" y2="134" marker-end="url(#am)"/>',
          '        <text class="mu" x="462" y="131" font-size="10.5">rumo, objetivos e conferência</text>',
          '        <line class="ln" x1="450" y1="254" x2="450" y2="238" marker-end="url(#am)"/>',
          '        <text class="mu" x="462" y="250" font-size="10.5">materiais, equipamentos e pessoas</text>',
          "      </svg>"]
    return "\n".join(o)


mapa0 = mapa([("", "Planejar"), ("", "Analisar criticamente"), ("", "Melhorar")],
             [("", "Vender"), ("", "Desenvolver"), ("", "Produzir"), ("", "Entregar")],
             [("", "Comprar"), ("", "Manter equipamentos"), ("", "Capacitar pessoas")],
             "O que o cliente pede", "O que o cliente recebe",
             "Modelo de mapa de processos. À esquerda, o que o cliente pede. À direita, o que o cliente recebe. No centro, três faixas. "
             "Na faixa de cima, os processos de gestão: planejar, analisar criticamente e melhorar. Na faixa do meio, os processos principais, em sequência: "
             "vender, desenvolver, produzir e entregar. Na faixa de baixo, os processos de apoio: comprar, manter equipamentos e capacitar pessoas.")
P1 = EX1["procs"]
mapa1 = mapa([(p["id"], p["nome"]) for p in P1 if p["tipo"] == GESTAO], [(p["id"], p["nome"]) for p in P1 if p["tipo"] == PRINCIPAL],
             [(p["id"], p["nome"]) for p in P1 if p["tipo"] == APOIO], EX1["head"]["cliente_in"], EX1["head"]["cliente_out"],
             "Mapa de processos da pizzaria, com nove processos. " + " ".join(
                 f'{t}: ' + ", ".join(f'{p["id"]} {p["nome"].lower()}' for p in P1 if p["tipo"] == t) + "." for t in (GESTAO, PRINCIPAL, APOIO)))

# ------------------------------------------------------------------ diagrama de tartaruga
CAIXAS = {"oque": (100, 10, 330, 124), "quem": (470, 10, 330, 124), "entradas": (10, 156, 232, 140), "saidas": (658, 156, 232, 140),
          "como": (10, 318, 285, 124), "riscos": (307, 318, 286, 124), "quanto": (605, 318, 285, 124)}


def tartaruga(nome, dono, conteudo, aria, generica=False):
    o = [f'      <svg viewBox="0 0 900 452" role="img" aria-label="{escape(aria)}">',
         '        <defs><marker id="at" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path class="ah" d="M0 0 L10 5 L0 10 z"/></marker></defs>',
         '        <line class="ln-mu" x1="265" y1="136" x2="362" y2="180"/><line class="ln-mu" x1="635" y1="136" x2="538" y2="180"/>',
         '        <line class="ln-mu" x1="222" y1="316" x2="352" y2="270"/><line class="ln-mu" x1="678" y1="316" x2="548" y2="270"/>',
         '        <line class="ln-mu" x1="450" y1="316" x2="450" y2="286"/>',
         '        <line class="ln" x1="244" y1="226" x2="276" y2="226" marker-end="url(#at)"/>',
         '        <line class="ln" x1="622" y1="226" x2="654" y2="226" marker-end="url(#at)"/>',
         '        <ellipse class="bx-ink" cx="450" cy="226" rx="170" ry="58"/>',
         '        <text class="mono t-ground" x="450" y="200" font-size="10" text-anchor="middle">PROCESSO</text>']
    linhas = textwrap.wrap(nome, 34)[:2]
    for j, l in enumerate(linhas):
        o.append(f'        <text class="b t-ground" x="450" y="{(224 if len(linhas) == 1 else 218) + j * 17}" font-size="13.5" text-anchor="middle">{escape(l)}</text>')
    o.append(f'        <text class="t-ground" x="450" y="{246 if len(linhas) == 1 else 256}" font-size="11.5" text-anchor="middle">{escape(dono)}</text>')
    for k in ORDEM_PARTES:
        x, y, w, h = CAIXAS[k]
        perg, tit, desc = PARTES[k]
        o.append(f'        <rect class="bx" x="{x}" y="{y}" width="{w}" height="{h}"/>')
        o.append(f'        <text class="mono mu" x="{x + 14}" y="{y + 21}" font-size="10">{perg}</text>')
        o.append(f'        <text class="b" x="{x + 14}" y="{y + 41}" font-size="12.5">{tit}</text>')
        larg = int((w - 28) / 5.7)
        yy = y + 61
        if generica:
            for l in textwrap.wrap(desc, larg):
                o.append(f'        <text x="{x + 14}" y="{yy}" font-size="11.5">{escape(l)}</text>')
                yy += 16
            for l in textwrap.wrap(conteudo[k], larg)[:3]:
                o.append(f'        <text class="mu" x="{x + 14}" y="{yy + 4}" font-size="11">{escape(l)}</text>')
                yy += 15
        else:
            n = 0
            for item, _ in conteudo[k]:
                for j, l in enumerate(textwrap.wrap(item, larg - 2)):
                    if n >= (5 if h > 130 else 4):
                        break
                    o.append(f'        <text x="{x + (14 if j == 0 else 23)}" y="{yy}" font-size="11">{"· " if j == 0 else ""}{escape(l)}</text>')
                    yy += 15
                    n += 1
    o.append("      </svg>")
    return "\n".join(o)


GEN = {"entradas": "Ex.: requisição aprovada, plano de produção.", "saidas": "Ex.: pedido emitido, material recebido.",
       "oque": "Ex.: sistema de compras, área de recebimento.", "quem": "Ex.: compradores treinados no procedimento.",
       "como": "Ex.: procedimento de compras e política de alçadas.", "quanto": "Ex.: prazo de atendimento, com meta de 5 dias.",
       "riscos": "Ex.: o fornecedor único deixa de entregar."}
tart0 = tartaruga("Nome, com verbo no infinitivo", "Dono e objetivo do processo", GEN,
                  "As partes do diagrama de tartaruga, ao redor do processo. " + " ".join(f"{PARTES[k][1]}: {PARTES[k][2].lower()}" for k in ORDEM_PARTES),
                  generica=True)
T2 = EX2["tartaruga"]
tart2 = tartaruga(EX2["proc"]["nome"], "Dono: " + EX2["proc"]["dono"], T2,
                  f'Diagrama de tartaruga do processo {EX2["proc"]["nome"].lower()}. '
                  + " ".join(f"{PARTES[k][1]}: " + "; ".join(a.lower() for a, _ in T2[k]) + "." for k in ORDEM_PARTES))


def partes_tab():
    ex = {"entradas": "Requisição aprovada, com especificação.", "saidas": "Material recebido e conferido.", "oque": "Sistema de compras, com campo obrigatório.",
          "quem": "Compradores treinados no procedimento.", "como": "Procedimento PR-SUP-01 rev. 6.", "quanto": "Prazo de atendimento: até 5,0 dias úteis.",
          "riscos": "O fornecedor único deixa de entregar."}
    perg = {"entradas": "O que o processo recebe, e de quem?", "saidas": "O que o processo entrega, e a quem?", "oque": "Que recursos o processo usa?",
            "quem": "Quem executa, e que competência precisa ter?", "como": "Que documentos dizem como fazer?",
            "quanto": "Como se sabe que o processo funciona?", "riscos": "O que pode impedir o resultado?"}
    o = ['  <div class="tbl">', '    <table>',
         '      <thead><tr><th style="width:18%">Parte</th><th style="width:30%">Pergunta</th><th style="width:26%">O que escrever</th><th>Exemplo, em compras</th></tr></thead>',
         '      <tbody>']
    for k in ORDEM_PARTES:
        o.append(f'        <tr><td><strong>{PARTES[k][1]}</strong></td><td>{perg[k]}</td><td>{escape(PARTES[k][2])}</td><td>{escape(ex[k])}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def tart_tab(t, titulo):
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{escape(titulo)}</caption>', '      <tbody>']
    rot = {"entradas": "De onde vem", "saidas": "Para onde vai", "oque": "", "quem": "", "como": "", "quanto": "Meta", "riscos": "Resposta"}
    for k in ORDEM_PARTES:
        itens = "".join(f'<li>{escape(a)} <small>· {escape(b)}</small></li>' for a, b in t[k])
        o.append(f'        <tr><td class="lb"><small>{PARTES[k][0]}</small>{PARTES[k][1]}</td><td><ul>{itens}</ul></td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


h1 = EX1["head"]
ex1head = "\n".join(['  <dl class="ficha">',
                     f'    <div><dt>Organização</dt><dd>{escape(h1["org"])}</dd></div>',
                     f'    <div><dt>Data e participantes</dt><dd>{dt(h1["data"])}. {escape(h1["por"])}</dd></div>',
                     f'    <div><dt>Origem</dt><dd>{escape(h1["origem"])}</dd></div>',
                     '  </dl>'])
o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Processos da pizzaria</caption>',
     '      <thead><tr><th>Nº</th><th style="width:22%">Processo</th><th style="width:11%">Tipo</th><th style="width:16%">Dono</th>'
     '<th style="width:30%">Objetivo</th><th>Indicador</th></tr></thead>', '      <tbody>']
for p in P1:
    ind = escape(p["indicador"]) if p["indicador"] else '<small>Sem indicador</small>'
    o.append(f'        <tr><td class="n">{p["id"]}</td><td><strong>{escape(p["nome"])}</strong></td><td>{chip(p["tipo"])}</td><td>{escape(p["dono"])}</td>'
             f'<td>{escape(p["objetivo"])}</td><td>{ind}</td></tr>')
o += ['      </tbody>', '    </table>', '  </div>']
ex1procs = "\n".join(o)
p3 = next(p for p in P1 if p["id"] == EX1["tartaruga"]["proc"])
ex1tart = tart_tab(EX1["tartaruga"], f'Tartaruga do processo {p3["id"]} · {p3["nome"]} · dono: {p3["dono"]}')
h2 = EX2["head"]
ex2head = "\n".join(['  <dl class="ficha">',
                     f'    <div><dt>Processo</dt><dd>{escape(EX2["proc"]["nome"])}</dd></div>',
                     f'    <div><dt>Objetivo</dt><dd>{escape(EX2["proc"]["objetivo"])}</dd></div>',
                     f'    <div><dt>Data e participantes</dt><dd>{dt(h2["data"])}. {escape(h2["por"])}</dd></div>',
                     f'    <div><dt>Origem</dt><dd>{escape(h2["origem"])}</dd></div>',
                     '  </dl>'])
ex2tart = tart_tab(T2, "As sete partes, com a origem, o destino e a meta")

# ------------------------------------------------------------------ figura 6: matriz de interações
GX, GY, CW, CH = 330, 50, 46, 30
n = len(IND)
mh = GY + n * CH + 58
mx = [f'      <svg viewBox="0 0 900 {mh}" role="img" aria-label="Matriz de interações dos nove processos da indústria. '
      + " ".join(f"{k}, {nome.lower()}: entrega a {len(fornece(k))} processos e recebe de {len(recebe(k))}." for k, nome in enumerate(IND, 1)) + '">',
      f'        <text class="mono mu" x="20" y="{GY - 14}" font-size="9.5">QUEM ENTREGA</text>',
      f'        <text class="mono mu" x="{GX + n * CW / 2}" y="16" font-size="9.5" text-anchor="middle">QUEM RECEBE</text>',
      f'        <text class="mono mu" x="{GX + n * CW + 56}" y="{GY - 14}" font-size="9.5" text-anchor="middle">ENTREGA A</text>']
for j in range(n):
    mx.append(f'        <text class="b" x="{GX + j * CW + CW / 2}" y="{GY - 14}" font-size="12" text-anchor="middle">{j + 1}</text>')
for i, nome in enumerate(IND):
    y = GY + i * CH
    mx.append(f'        <line class="grid" x1="20" y1="{y}" x2="{GX + n * CW + 100}" y2="{y}"/>')
    mx.append(f'        <text x="20" y="{y + 20}" font-size="11.5"><tspan class="b">{i + 1}</tspan> · {escape(nome)}</text>')
    mx.append(f'        <rect class="diag" x="{GX + i * CW + 1}" y="{y + 1}" width="{CW - 2}" height="{CH - 2}"/>')
    for a, b, _ in INTER:
        if a == i + 1:
            mx.append(f'        <circle class="dot" cx="{GX + (b - 1) * CW + CW / 2}" cy="{y + CH / 2}" r="5.5"/>')
    mx.append(f'        <text class="b" x="{GX + n * CW + 56}" y="{y + 20}" font-size="12" text-anchor="middle" style="font-variant-numeric:tabular-nums">{len(fornece(i + 1))}</text>')
yb = GY + n * CH
mx.append(f'        <line class="grid" x1="20" y1="{yb}" x2="{GX + n * CW + 100}" y2="{yb}"/>')
for j in range(n + 1):
    mx.append(f'        <line class="grid" x1="{GX + j * CW}" y1="{GY}" x2="{GX + j * CW}" y2="{yb}"/>')
mx.append(f'        <text class="mono mu" x="{GX - 12}" y="{yb + 22}" font-size="9.5" text-anchor="end">RECEBE DE</text>')
for j in range(n):
    mx.append(f'        <text class="b" x="{GX + j * CW + CW / 2}" y="{yb + 22}" font-size="12" text-anchor="middle" style="font-variant-numeric:tabular-nums">{len(recebe(j + 1))}</text>')
mx.append(f'        <circle class="dot" cx="26" cy="{yb + 44}" r="5.5"/><text x="40" y="{yb + 48}" font-size="11.5">o processo da linha entrega algo ao processo da coluna</text>')
mx.append("      </svg>")
SUP = IND.index("Suprimentos") + 1
it = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>Interações do processo {SUP} · Suprimentos</caption>',
      '      <thead><tr><th style="width:12%">Sentido</th><th style="width:32%">Processo</th><th>O que é entregue</th></tr></thead>', '      <tbody>']
for a, t in recebe(SUP):
    it.append(f'        <tr><td><span class="chip sl">Recebe de</span></td><td><strong>{a} · {escape(IND[a - 1])}</strong></td><td>{escape(t)}</td></tr>')
for b, t in fornece(SUP):
    it.append(f'        <tr><td><span class="chip d">Entrega a</span></td><td><strong>{b} · {escape(IND[b - 1])}</strong></td><td>{escape(t)}</td></tr>')
it += ['      </tbody>', '    </table>', '  </div>']

# ------------------------------------------------------------------ módulo 6: elementos e gráfico
et = ['  <div class="tbl">', '    <table>',
      '      <thead><tr><th style="width:8%">Item</th><th style="width:26%">Elemento</th><th>Pergunta de avaliação</th><th style="width:22%">Na pizzaria</th></tr></thead>',
      '      <tbody>']
for k, (letra, nome, perg) in enumerate(ELEMENTOS):
    v = [p["elem"][k] for p in P1]
    et.append(f'        <tr><td class="num">4.4.1 {letra}</td><td><strong>{nome}</strong></td><td>{escape(perg)}</td>'
              f'<td>{v.count(SIM)} sim, {v.count(PARCIAL)} parcial, {v.count(NAO)} não</td></tr>')
et += ['      </tbody>', '    </table>', '  </div>']

X0, U, TOP, RH, BH = 300, 60, 30, 32, 16
bottom = TOP + RH * len(P1)
HH = bottom + 48
media = sum(p["pct"] for p in P1) / len(P1)
ch = [f'      <svg id="bars" viewBox="0 0 900 {HH}" role="img" aria-label="Gráfico de barras com os elementos definidos em cada processo da pizzaria, de um total de oito. '
      + " ".join(f'{p["id"]}, {p["nome"].lower()}: {br(p["pts"])}.' for p in P1) + f' A média é de {round(media * 100)}%.">']
for v in range(0, 9, 2):
    x = X0 + v * U
    ch.append(f'        <line class="grid" x1="{x}" y1="{TOP - 6}" x2="{x}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{x}" y="{bottom + 16}" font-size="11" text-anchor="middle" style="font-variant-numeric:tabular-nums">{v}</text>')
ch.append(f'        <text class="mono mu" x="{X0 + 4 * U}" y="{bottom + 36}" font-size="10" text-anchor="middle">ELEMENTOS DEFINIDOS, DE 8</text>')
for k, p in enumerate(P1):
    y = TOP + RH * k + (RH - BH) / 2
    ch.append(f'        <text x="20" y="{y + 12:.1f}" font-size="11.5"><tspan class="b">{p["id"]}</tspan> · {escape(p["nome"])}</text>')
    x1 = X0 + p["pts"] * U
    ch.append(f'        <path class="seg" data-k="{k}" d="M{X0} {y:.1f} H{x1 - 4:.1f} Q{x1:.1f} {y:.1f} {x1:.1f} {y + 4:.1f} V{y + BH - 4:.1f} '
              f'Q{x1:.1f} {y + BH:.1f} {x1 - 4:.1f} {y + BH:.1f} H{X0} Z"/>')
    ch.append(f'        <text x="{x1 + 8:.1f}" y="{y + 12:.1f}" font-size="11.5"><tspan class="b">{br(p["pts"])}</tspan><tspan class="mu"> · {round(p["pct"] * 100)}%</tspan></text>')
for k, p in enumerate(P1):
    e = p["elem"]
    ch.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" '
              f'aria-label="{p["id"]}, {escape(p["nome"])}: {br(p["pts"])} de 8 elementos" data-k="{k}" data-id="{p["id"]}" data-n="{escape(p["nome"])}" '
              f'data-t="{p["tipo"].lower()}" data-pts="{br(p["pts"])}" data-s="{e.count(SIM)}" data-p="{e.count(PARCIAL)}" data-x="{e.count(NAO)}" '
              f'data-cx="{X0 + p["pts"] * U / 2:.1f}"/>')
ch.append("      </svg>")
CL = {SIM: "", PARCIAL: " v1", NAO: " v0"}
tb = ['        <table class="aud">', '          <thead><tr><th>Processo</th>' + "".join(f'<th class="c">{l}<br><small>{nome.split(" ")[0]}</small></th>' for l, nome, _ in ELEMENTOS)
      + '<th class="c">Pontos</th><th class="c">Percentual</th></tr></thead>', '          <tbody>']
for p in P1:
    tb.append(f'            <tr><td><strong>{p["id"]} · {escape(p["nome"])}</strong></td>' + "".join(f'<td class="c{CL[x]}">{x}</td>' for x in p["elem"])
              + f'<td class="c">{br(p["pts"])}</td><td class="c">{round(p["pct"] * 100)}%</td></tr>')
tb += ['          </tbody>', '        </table>']

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--MAPA0-->", mapa0), ("<!--TART0-->", tart0), ("<!--PARTES-->", partes_tab()), ("<!--EX1HEAD-->", ex1head), ("<!--MAPA1-->", mapa1),
                 ("<!--EX1PROCS-->", ex1procs), ("<!--EX1TART-->", ex1tart), ("<!--EX2HEAD-->", ex2head), ("<!--TART2-->", tart2), ("<!--EX2TART-->", ex2tart),
                 ("<!--INTER-->", "\n".join(mx)), ("<!--INTERTAB-->", "\n".join(it)), ("<!--ELEMTAB-->", "\n".join(et)),
                 ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Mapa de processos e tartaruga</title>")
assert "Mapa de processos" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| processos:", len(P1),
      "| média", round(media * 100), "% | interações:", len(INTER))
