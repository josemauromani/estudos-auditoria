# -*- coding: utf-8 -*-
"""Monta treinamento-iso-9001.html: CSS herdado do estudo de PDCA + corpo próprio + tabelas e figuras geradas dos dados."""
import os
import re
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iso_data import A, CHECK, DOCS, ESTUDOS, EX1, EX2, FASE, N, P, REQ, SECOES, geral, resumo  # noqa: E402

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# as cores do ciclo PDCA são a identidade deste estudo: os tokens --p, --d, --c e --a são mantidos
LIGHT = "\n  --s1:#2A6FB0; --s2:#D19A2E; --s3:#B0413E; --on-s2:#16242E;"
DARK = "\n  --s1:#4F97DB; --s2:#B58E14; --s3:#D14B45; --on-s2:#0F171C;"
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Seções e situação */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.p{background:var(--p)} .chip.c{background:var(--c)} .chip.d{background:var(--d)} .chip.sl{background:var(--muted)}
.chip.s1{background:var(--s1)} .chip.s2{background:var(--s2);color:var(--on-s2)} .chip.s3{background:var(--s3)}
.k.base{background:var(--ink);color:var(--ground)}
.k.w{width:auto;padding:0 .3em}
svg .hd-ink{fill:var(--ink)}
svg .bx-out2{fill:var(--sunk);stroke:var(--rule);stroke-width:1.5}
svg .sg1{fill:var(--s1)} svg .sg2{fill:var(--s2)} svg .sg3{fill:var(--s3)}
svg .on-s2{fill:var(--on-s2)}
svg .cell{fill:var(--sunk)}
svg a text{fill:var(--accent);text-decoration:underline}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas de requisitos e dos exemplos */
table.req, table.aud{font-size:.82rem;min-width:860px;line-height:1.4}
table.req th, table.req td, table.aud th, table.aud td{padding:8px 10px}
table.req td.rq{width:22%}
table.req td.rq b{display:block;font:500 .8rem var(--mono);color:var(--muted);margin-bottom:2px}
table.req td.rq strong{display:block}
table.req td.rq small{display:block;margin-top:5px;color:var(--muted);font-size:.76rem}
table.req td.pg{font-style:italic}
table.aud td.n{white-space:nowrap;font:500 .8rem var(--mono);color:var(--muted)}
table.aud td.c{text-align:center;font-variant-numeric:tabular-nums}
table.aud td.good{background:var(--good-tint);font-weight:600}
table.aud td.bad{background:var(--bad-tint);font-weight:600}
table.aud tr.tot td{background:var(--sunk);font-weight:600}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha do diagnóstico (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += "\n.quiz .opts{flex-wrap:wrap}\n"

NOME = {s: t for s, t, _ in SECOES}
FASE_TXT = {"base": ("base", "Base"), "p": ("p", "P"), "d": ("d", "D"), "c": ("c", "C"), "a": ("a", "A")}
CHIP = {A: '<span class="chip s1">Atende</span>', P: '<span class="chip s2">Em parte</span>', N: '<span class="chip s3">Não atende</span>'}


def dt(d):
    return d.strftime("%d/%m/%Y")


def pc(v):
    return f"{round(v * 100)}%"


def links(keys):
    return ", ".join(f'<a href="{ESTUDOS[k][1]}">{escape(ESTUDOS[k][0])}</a>' for k in keys)


def secoes_table():
    o = ['  <div class="tbl">', '    <table>',
         '      <thead><tr><th style="width:9%">Seção</th><th style="width:24%">Título</th><th style="width:15%">Requisitos neste estudo</th>'
         '<th>Pergunta que a seção responde</th><th style="width:11%">Fase</th></tr></thead>', '      <tbody>']
    for s, t, q in SECOES:
        cls, txt = FASE_TXT[FASE[s]]
        n = sum(1 for r in REQ if r["secao"] == s)
        tile = f'<span class="k {cls}{" w" if cls == "base" else ""}">{txt}</span>'
        o.append(f'        <tr><td class="num">{s}</td><td><strong>{escape(t)}</strong></td><td class="num">{n}</td><td>{escape(q)}</td><td>{tile}</td></tr>')
    o.append(f'        <tr><td></td><td><strong>Total</strong></td><td class="num">{len(REQ)}</td><td>Os requisitos 7.1.1 e 7.1.2 foram reunidos, '
             'e os itens dos requisitos 8.3 e 9.3 foram tratados em conjunto.</td><td></td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def req_table(sec):
    o = ['  <div class="tbl">', '    <table class="req">',
         '      <thead><tr><th>Requisito</th><th style="width:36%">O que pede, em resumo</th><th style="width:20%">Pergunta do auditor</th>'
         '<th style="width:22%">Evidências típicas</th></tr></thead>', '      <tbody>']
    for r in REQ:
        if r["secao"] != sec:
            continue
        est = f'<small>Estudo: {links(r["estudos"])}</small>' if r["estudos"] else ""
        o.append(f'        <tr><td class="rq"><b>{r["num"]}</b><strong>{escape(r["titulo"])}</strong>{est}</td><td>{escape(r["pede"])}</td>'
                 f'<td class="pg">{escape(r["pergunta"])}</td><td>{escape(r["evid"])}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def docs_table():
    o = ['  <div class="tbl">', '    <table class="aud">',
         '      <thead><tr><th style="width:10%">Requisito</th><th style="width:14%">Verbo</th><th>O que precisa existir</th>'
         '<th style="width:28%">Exemplo</th></tr></thead>', '      <tbody>']
    for num, tipo, texto, exemplo in DOCS:
        cls = "p" if tipo == "Manter" else ("c" if tipo == "Reter" else "d")
        o.append(f'        <tr><td class="n">{num}</td><td><span class="chip {cls}">{tipo}</span></td><td>{escape(texto)}</td><td>{escape(exemplo)}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def ficha(ex):
    h = ex["head"]
    t, a, p, n, v = geral(ex["itens"])
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Data e responsável</dt><dd>{dt(h["data"])}. {escape(h["por"])}</dd></div>',
                      f'    <div><dt>Método</dt><dd>{escape(h["metodo"])}</dd></div>',
                      f'    <div><dt>Resultado</dt><dd>{pc(v)} de atendimento, em {t} requisitos: {a} atendidos, {p} em parte e {n} não atendidos</dd></div>',
                      '  </dl>'])


DESTAQUE = {4: "Escopo não escrito (4.3)", 5: "Política inexistente (5.2)", 6: "Mudanças sem planejamento (6.3)",
            7: "Termômetro da câmara fria sem verificação (7.1.5)", 8: "Mudanças de receita sem registro (8.5.6)",
            9: "Análise crítica não realizada (9.3)", 10: "Reclamações tratadas sem análise de causa (10.2)"}


def ex1_tables():
    res = resumo(EX1["itens"])
    t, a, p, n, v = geral(EX1["itens"])
    o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Requisitos não atendidos</caption>',
         '      <thead><tr><th style="width:9%">Requisito</th><th style="width:25%">Título</th><th style="width:30%">Evidência encontrada</th>'
         '<th>O que falta</th></tr></thead>', '      <tbody>']
    for r in REQ:
        sit, ev, falta = EX1["itens"][r["num"]]
        if sit == N:
            o.append(f'        <tr><td class="n">{r["num"]}</td><td><strong>{escape(r["titulo"])}</strong></td><td>{escape(ev)}</td><td>{escape(falta)}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o), res, (t, a, p, n, v)


def ex2_block():
    o = [ficha(EX2), '  <div class="tbl">', '    <table class="aud">',
         '      <thead><tr><th style="width:8%">Requisito</th><th style="width:22%">Título</th><th style="width:11%">Situação</th>'
         '<th style="width:28%">Evidência encontrada</th><th>O que falta</th></tr></thead>', '      <tbody>']
    tit = {r["num"]: r["titulo"] for r in REQ}
    for num, (sit, ev, falta) in EX2["itens"].items():
        o.append(f'        <tr><td class="n">{num}</td><td><strong>{escape(tit[num])}</strong></td><td>{CHIP[sit]}</td><td>{escape(ev)}</td>'
                 f'<td>{escape(falta)}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


# ---- figura 8: situação dos requisitos por seção
ex1_nao, RES, GERAL = ex1_tables()
X0, U, TOP, RH, BH = 250, 34, 30, 36, 20
bottom = TOP + RH * len(SECOES)
H = bottom + 78
ch = [f'      <svg id="bars" viewBox="0 0 900 {H}" role="img" aria-label="Gráfico de barras empilhadas com a situação dos {GERAL[0]} requisitos da pizzaria, por seção da norma. '
      f'No total, {GERAL[1]} requisitos atendidos, {GERAL[2]} atendidos em parte e {GERAL[3]} não atendidos, com {pc(GERAL[4])} de atendimento. '
      + "; ".join(f"seção {s}, {NOME[s].lower()}: {v[1]} atendidos, {v[2]} em parte e {v[3]} não atendidos" for s, v in RES.items()) + '.">']
for v in range(0, 18, 5):
    x = X0 + v * U
    ch.append(f'        <line class="grid" x1="{x}" y1="{TOP - 6}" x2="{x}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{x}" y="{bottom + 16}" font-size="11" text-anchor="middle" style="font-variant-numeric:tabular-nums">{v}</text>')
ch.append(f'        <text class="mono mu" x="{X0 + 8.5 * U}" y="{bottom + 36}" font-size="10" text-anchor="middle">REQUISITOS</text>')
for k, (s, (t, a, p, n, v)) in enumerate(RES.items()):
    y = TOP + RH * k + (RH - BH) / 2
    ch.append(f'        <text x="20" y="{y + 14:.1f}" font-size="11.5"><tspan class="b">{s}</tspan> · {escape(NOME[s])}</text>')
    x = X0
    partes = [(c, q) for c, q in (("1", a), ("2", p), ("3", n)) if q]
    for j, (c, q) in enumerate(partes):
        w = q * U - 2
        if j == len(partes) - 1:
            x1 = x + w
            ch.append(f'        <path class="seg sg{c}" data-k="{k}" d="M{x} {y:.1f} H{x1 - 4} Q{x1} {y:.1f} {x1} {y + 4:.1f} V{y + BH - 4:.1f} '
                      f'Q{x1} {y + BH:.1f} {x1 - 4} {y + BH:.1f} H{x} Z"/>')
        else:
            ch.append(f'        <rect class="seg sg{c}" data-k="{k}" x="{x}" y="{y:.1f}" width="{w}" height="{BH}"/>')
        ch.append(f'        <text class="{"on-s2" if c == "2" else "on"} b" x="{x + w / 2:.1f}" y="{y + 14:.1f}" font-size="11" text-anchor="middle">{q}</text>')
        x += q * U
    ch.append(f'        <text class="b" x="{x + 8}" y="{y + 14:.1f}" font-size="11.5">{pc(v)}</text>')
lx, ly = 20, bottom + 66
for c, nome, dx in (("1", "Atende", 110), ("2", "Atende em parte", 170), ("3", "Não atende", 130)):
    ch.append(f'        <rect class="sg{c}" x="{lx}" y="{ly - 10}" width="14" height="12"/>')
    ch.append(f'        <text x="{lx + 21}" y="{ly}" font-size="11.5">{nome}</text>')
    lx += dx
ch.append(f'        <text class="mu" x="880" y="{ly}" font-size="11.5" text-anchor="end">o percentual conta 1 ponto para “atende” e meio ponto para “em parte”</text>')
for k, (s, (t, a, p, n, v)) in enumerate(RES.items()):
    ch.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" '
              f'aria-label="Seção {s}, {escape(NOME[s])}: {a} atendidos, {p} em parte e {n} não atendidos, de {t} requisitos" data-k="{k}" '
              f'data-s="{s}" data-n="{escape(NOME[s])}" data-t="{t}" data-a="{a}" data-p="{p}" data-x="{n}" data-pc="{round(v * 100)}" '
              f'data-cx="{X0 + t * U / 2:.1f}"/>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>Seção</th><th>Requisitos</th><th>Atende</th><th>Atende em parte</th><th>Não atende</th>'
      '<th>Atendimento</th><th>Principal lacuna</th></tr></thead>', '          <tbody>']
for s, (t, a, p, n, v) in RES.items():
    tb.append(f'            <tr><td><strong>{s} · {escape(NOME[s])}</strong></td><td class="c">{t}</td><td class="c">{a}</td><td class="c">{p}</td>'
              f'<td class="c">{n}</td><td class="c">{pc(v)}</td><td>{escape(DESTAQUE[s])}</td></tr>')
tb.append(f'            <tr class="tot"><td>Total</td><td class="c">{GERAL[0]}</td><td class="c">{GERAL[1]}</td><td class="c">{GERAL[2]}</td>'
          f'<td class="c">{GERAL[3]}</td><td class="c">{pc(GERAL[4])}</td><td></td></tr>')
tb += ['          </tbody>', '        </table>']

# ---- figura 9: estudos da série × seções da norma
ORDEM = ["esc", "pi", "swot", "obj", "ped", "proj", "proc", "sipoc", "raci", "riscos", "prod", "lib", "ind", "gut", "par", "ishikawa", "w5h2", "pdca", "auditoria", "nc", "ac", "doc", "comp", "forn", "sat"]
CX = lambda j: 350 + j * 80  # noqa: E731
HD = {"base": "hd-ink", "p": "hd-p", "d": "hd-d", "c": "hd-c", "a": "hd-a"}
RY, R0 = 32, 70
mh = R0 + RY * len(ORDEM) + 14
mz = [f'      <svg viewBox="0 0 900 {mh}" role="img" aria-label="Matriz com os estudos da série nas linhas e as seções da norma nas colunas. '
      + " ".join(f'{ESTUDOS[k][0]}: requisitos ' + ", ".join(r["num"] for r in REQ if k in r["estudos"]) + "." for k in ORDEM) + '">']
for j, (s, t, _) in enumerate(SECOES):
    fase = FASE[s]
    mz.append(f'        <rect class="{HD[fase]}" x="{CX(j) - 36}" y="14" width="72" height="30"/>')
    mz.append(f'        <text class="disp {"t-ground" if fase == "base" else "on"}" x="{CX(j)}" y="36" font-size="18" text-anchor="middle">{s}</text>')
    mz.append(f'        <text class="mono mu" x="{CX(j)}" y="60" font-size="8.5" text-anchor="middle">{escape(t.split(" ")[0].upper())}</text>')
for i, k in enumerate(ORDEM):
    y = R0 + RY * i
    mz.append(f'        <line class="grid" x1="20" y1="{y}" x2="880" y2="{y}"/>')
    mz.append(f'        <a href="{ESTUDOS[k][1]}"><text class="b" x="20" y="{y + 21}" font-size="12">{escape(ESTUDOS[k][0])}</text></a>')
    for j, (s, _, _) in enumerate(SECOES):
        nums = [r["num"] for r in REQ if r["secao"] == s and k in r["estudos"]]
        if nums:
            mz.append(f'        <rect class="cell" x="{CX(j) - 36}" y="{y + 5}" width="72" height="22"/>')
            # três itens ou mais não cabem na célula: mostra a seção comum e a contagem, com a lista completa na dica
            txt = " · ".join(nums) if len(nums) < 3 else f'{os.path.commonprefix(nums).rstrip(".")} · {len(nums)} itens'
            mz.append(f'        <text x="{CX(j)}" y="{y + 20}" font-size="10.5" text-anchor="middle" style="font-variant-numeric:tabular-nums"><title>{" · ".join(nums)}</title>{txt}</text>')
mz.append(f'        <line class="grid" x1="20" y1="{R0 + RY * len(ORDEM)}" x2="880" y2="{R0 + RY * len(ORDEM)}"/>')
mz.append("      </svg>")

AJUDA = {
    "4.1": "Organiza as questões internas e externas em forças, fraquezas, oportunidades e ameaças.",
    "4.2": "O estudo de Partes interessadas lista as partes pertinentes e os requisitos de cada uma. A SWOT leva as expectativas para as oportunidades e as ameaças.",
    "4.3": "Traz a declaração de escopo, a fronteira, os processos terceirizados e a aplicabilidade de cada requisito, com as duas perguntas da não aplicabilidade.",
    "5.1.1": "Traz os dez compromissos da direção, com o que ela faz, o registro e a ação para o que é parcial.",
    "4.4": "O Mapa de processos mostra os processos e as ligações entre eles. O SIPOC e a tartaruga descrevem cada processo.",
    "5.3": "Mostra quem executa, quem responde, quem é consultado e quem é informado.",
    "6.1": "A SWOT levanta os riscos e as oportunidades. A Matriz de riscos avalia o nível e define a resposta.",
    "5.2": "Traz os compromissos da política e a ligação de cada objetivo a um deles.",
    "6.2": "O estudo de Objetivos da qualidade liga a política ao objetivo, com base, meta, prazo e plano. Os Indicadores medem; o 5W2H detalha o plano.",
    "6.3": "A Matriz de riscos avalia o que a mudança pode causar. O 5W2H planeja a execução.",
    "7.5": "Traz a lista mestra, a tabela de retenção dos registros e a lista de documentos externos.",
    "7.2": "Traz a matriz por função, a escala de níveis, o plano de treinamento e a avaliação da eficácia.",
    "7.3": "Traz as perguntas de conscientização e o que se espera ouvir.",
    "5.1.2": "Traz os indicadores de satisfação e de reclamações que a direção acompanha.",
    "7.4": "As letras C e I da matriz mostram quem precisa ser consultado e informado.",
    "8.1": "Mostra as entradas e as saídas que a operação precisa controlar.",
    "8.3": "Traz o plano do projeto, as entradas ligadas às saídas e às verificações, a validação no uso real e o registro das mudanças.",
    "8.4.1": "Traz os critérios de homologação, o índice de desempenho e as classes com conduta.",
    "8.4.2": "Classifica os fornecedores por criticidade e registra o recebimento e as ocorrências.",
    "8.4.3": "Mostra o que o pedido de compra precisa informar ao fornecedor.",
    "8.2.1": "O estudo de Satisfação traz o caminho da reclamação. O de Requisitos do cliente traz os canais de pedido e o que se informa ao cliente.",
    "8.2.2": "Traz a oferta: a especificação, os requisitos legais, o que não se garante e a capacidade confirmada.",
    "8.2.3": "Traz as sete perguntas da análise antes do aceite, a decisão com o cliente e o registro.",
    "8.2.4": "Traz o registro das mudanças nos pedidos aceitos, com a análise, os documentos e quem foi informado.",
    "8.5.1": "Traz o plano de controle: o que conferir em cada etapa, com critério, medição, registro e reação.",
    "8.5.2": "Mostra a identificação e a situação do produto em cada etapa, e uma busca de rastreabilidade.",
    "8.5.3": "Lista o que pertence a clientes e a fornecedores, com o cuidado e a comunicação das ocorrências.",
    "8.5.4": "Registra como o produto é protegido em cada etapa, até a entrega.",
    "8.5.6": "Traz o registro de mudanças, com a análise, a autorização e as ações decorrentes.",
    "8.6": "Traz o registro de liberação, com as verificações, a decisão e quem liberou, e a liberação com verificação pendente.",
    "8.7": "O estudo de Liberação traz a segregação, as seis disposições, a concessão e o registro. O de Não conformidade separa a correção da ação sobre a causa.",
    "9.1.1": "O estudo de Indicadores define o que medir, como e quando. O PDCA compara o resultado com a meta.",
    "9.1.2": "O estudo de Satisfação do cliente traz a pesquisa, o registro de reclamações e a devolutiva. O de Indicadores põe o resultado no painel.",
    "9.1.3": "O painel mostra a situação e a tendência. O Pareto mostra onde o problema se concentra. A GUT prioriza, e o Ishikawa procura as causas.",
    "9.2": "Entrega o programa, o plano, a lista de verificação e as constatações.",
    "9.3": "Traz a pauta das doze entradas, o registro das decisões e o acompanhamento das ações.",
    "10.1": "Conduz a melhoria, do problema até a padronização.",
    "10.2": "Traz o tratamento em sete etapas, com análise de causa, plano e verificação da eficácia.",
    "10.3": "Um ciclo concluído é o ponto de partida do seguinte.",
}
com_estudo = [r for r in REQ if r["estudos"]]
assert {r["num"] for r in com_estudo} == set(AJUDA), {r["num"] for r in com_estudo} ^ set(AJUDA)
mp = ['  <div class="tbl">', '    <table class="aud">',
      '      <thead><tr><th style="width:9%">Requisito</th><th style="width:27%">Título</th><th style="width:24%">Estudo da série</th><th>Como ajuda</th></tr></thead>',
      '      <tbody>']
for r in com_estudo:
    mp.append(f'        <tr><td class="n">{r["num"]}</td><td><strong>{escape(r["titulo"])}</strong></td><td>{links(r["estudos"])}</td><td>{escape(AJUDA[r["num"]])}</td></tr>')
mp += ['      </tbody>', '    </table>', '  </div>']

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
subs = [("<!--SECOES-->", secoes_table()), ("<!--DOCS-->", docs_table()), ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1-->", ex1_nao),
        ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--EX2-->", ex2_block()),
        ("<!--MATRIZ-->", "\n".join(mz)), ("<!--MAPA-->", "\n".join(mp)), ("<!--CHECK-->", check)]
subs += [(f"<!--REQ{s}-->", req_table(s)) for s, _, _ in SECOES]
for tag, val in subs:
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>ISO 9001 requisito a requisito</title>")
assert "ISO 9001" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| requisitos:", len(REQ),
      "| pizzaria:", GERAL[:4], pc(GERAL[4]), "| compras:", geral(EX2["itens"])[:4], pc(geral(EX2["itens"])[4]))
