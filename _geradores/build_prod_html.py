# -*- coding: utf-8 -*-
"""Monta treinamento-producao.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prod_data import (BUSCA, CHECK, DENTRO, ETAPAS, EX1, EX2, FORA, PARTES, PRODUTO, SIM, atributo, criterio, leitura, resumo, resumo_k)  # noqa: E402

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# dentro, desvio com reação e desvio sem reação: a mesma paleta de três cores do estudo de Satisfação, validada para daltonismo nos dois modos
LIGHT = ("\n  --s1:#2A6FB0; --s1-tint:#DCE8F3;\n  --s2:#D19A2E; --s2-tint:#F8EBCB;\n  --s3:#B0413E; --s3-tint:#F5DEDC;\n  --on-s2:#16242E;")
DARK = ("\n  --s1:#4F97DB; --s1-tint:#1B2F42;\n  --s2:#B58E14; --s2-tint:#3A2C12;\n  --s3:#D14B45; --s3-tint:#3D1F1E;\n  --on-s2:#0F171C;")
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)
css = "\n".join(l for l in css.split("\n") if not l.startswith(("table.pdca", "/* Ficha do ciclo")))

extra = """
/* Leituras */
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.s1{background:var(--s1)} .chip.s2{background:var(--s2);color:var(--on-s2)} .chip.s3{background:var(--s3)}
.chip.sl{background:var(--sunk);color:var(--ink);box-shadow:inset 0 0 0 1px var(--rule)}
svg .hd-ink{fill:var(--ink)}
svg .zone{fill:var(--s1-tint)}
svg .pt{fill:var(--s1)} svg .pt.out{fill:var(--s3)}
svg .series{stroke:var(--s1)}
svg .halo{paint-order:stroke;stroke:var(--surface);stroke-width:5px;stroke-linejoin:round}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas dos exemplos */
table.aud{font-size:.8rem;min-width:900px;line-height:1.4}
table.aud th, table.aud td{padding:8px 9px}
table.aud td.n{white-space:nowrap;font-weight:600;color:var(--muted)}
table.aud td.c, table.aud th.c{text-align:center;font-variant-numeric:tabular-nums}
table.aud td.no{background:var(--s3-tint)}
table.aud td small, table.aud th small{display:block;color:var(--muted);font-size:.76rem;margin-top:3px;font-weight:400}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha do plano (acima de cada exemplo) */"""
assert css.count("\n.ficha{") == 1
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

TNUM = ' style="font-variant-numeric:tabular-nums"'


def dt(d, ano=True):
    return d.strftime("%d/%m/%Y" if ano else "%d/%m") if d else "—"


def pc(v):
    return f"{int(100 * v + 0.5 + 1e-9)}%"


def num(v):
    if v is None:
        return "—"
    if float(v).is_integer():
        return str(int(v))
    return f"{v:g}".replace(".", ",")


def valor(k, r):
    if atributo(k):
        return "Conforme" if r["conf"] == SIM else "Não conforme"
    return f'{num(r["valor"])} {k["unid"]}'


def marker(i, mu=False):
    return (f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path class="{"ah-mu" if mu else "ah"}" d="M0 0 L10 5 L0 10 z"/></marker>')


def lines(o, txt, x, y, wrap, fs=10.5, cls="", step=13, maxl=3):
    """Texto quebrado em linhas; devolve o y da linha seguinte."""
    ls = textwrap.wrap(txt, wrap)[:maxl]
    attr = f' class="{cls}"' if cls else ""
    for j, l in enumerate(ls):
        o.append(f'        <text{attr} x="{x}" y="{y + j * step}" font-size="{fs}">{escape(l)}</text>')
    return y + step * len(ls)


H1, H2 = EX1["head"], EX2["head"]
K1 = {k["id"]: k for k in EX1["plano"]}

# ------------------------------------------------------------------ figura 1: o plano de controle sobre as etapas do processo
etapas1 = []
for k in EX1["plano"]:
    if k["etapa"] not in etapas1:
        etapas1.append(k["etapa"])
EW, EG = 136, 12
mp = ['      <svg viewBox="0 0 900 282" role="img" aria-label="O plano de controle da pizzaria, sobre as etapas do processo. '
      + " ".join(f'{e}: ' + "; ".join(f'{k["id"]}, {k["caract"].lower()}, {criterio(k)}' for k in EX1["plano"] if k["etapa"] == e) + "." for e in etapas1) + '">',
      "        <defs>" + marker("a1") + "</defs>"]
for j, e in enumerate(etapas1):
    x = 12 + j * (EW + EG)
    mp.append(f'        <rect class="bx-ink" x="{x}" y="14" width="{EW}" height="44"/>')
    ls = textwrap.wrap(e, 20)[:2]
    for i, l in enumerate(ls):
        mp.append(f'        <text class="b t-ground" x="{x + 10}" y="{(40 if len(ls) == 1 else 33) + i * 14}" font-size="11.5">{escape(l)}</text>')
    if j < len(etapas1) - 1:
        mp.append(f'        <line class="ln" x1="{x + EW + 1}" y1="36" x2="{x + EW + EG - 2}" y2="36" marker-end="url(#a1)"/>')
    for i, k in enumerate([k for k in EX1["plano"] if k["etapa"] == e]):
        y = 72 + i * 88
        mp.append(f'        <line class="ln-mu" x1="{x + EW / 2}" y1="{y - 14 if i == 0 else y - 8}" x2="{x + EW / 2}" y2="{y}"/>')
        mp.append(f'        <rect class="{"bx-c" if k["tipo"] == PRODUTO else "bx-d"}" x="{x}" y="{y}" width="{EW}" height="80"/>')
        mp.append(f'        <text class="mono mu" x="{x + 10}" y="{y + 15}" font-size="9.5">{k["id"]} · {k["tipo"].upper()}</text>')
        lines(mp, k["caract"], x + 10, y + 29, 23, fs=10)
        mp.append(f'        <text class="b" x="{x + 10}" y="{y + 72}" font-size="10.5">{escape(criterio(k))}</text>')
mp.append('        <rect class="bx-c" x="250" y="256" width="14" height="14"/><text x="272" y="268" font-size="11.5">Controle do produto</text>')
mp.append('        <rect class="bx-d" x="470" y="256" width="14" height="14"/><text x="492" y="268" font-size="11.5">Controle do processo</text>')
mp.append("      </svg>")

# ------------------------------------------------------------------ figura 2: as cinco etapas
W5, G5 = 164, 14
fl = ['      <svg viewBox="0 0 900 206" role="img" aria-label="As cinco etapas do trabalho. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS) + ' A revisão devolve o trabalho à segunda etapa.">',
      "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
for k, (nome, desc) in enumerate(ETAPAS):
    x = 12 + k * (W5 + G5)
    ink = k == 4
    fl.append(f'        <rect class="{["bx", "bx-p", "bx-p", "bx-c", "bx-ink"][k]}" x="{x}" y="16" width="{W5}" height="124"/>')
    fl.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="36" font-size="10">ETAPA {k + 1}</text>')
    fl.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="58" font-size="13">{escape(nome)}</text>')
    lines(fl, desc, x + 12, 80, 26, cls="t-ground" if ink else "", step=14.5, maxl=4)
    if k < 4:
        fl.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="78" x2="{x + W5 + G5 - 2}" y2="78" marker-end="url(#a2)"/>')
xa, xb = 12 + 4 * (W5 + G5) + W5 / 2, 12 + (W5 + G5) + W5 / 2
fl.append(f'        <path class="ln-mu dash" d="M{xa} 142 V170 H{xb} V146" marker-end="url(#a2m)"/>')
fl.append('        <text class="mu halo" x="540" y="174" font-size="11" text-anchor="middle">a cada mudança, reclamação ou desvio que se repete</text>')
fl.append('        <text x="450" y="198" font-size="11.5" text-anchor="middle">O plano é escrito uma vez e revisto sempre que o processo ensina algo novo.</text>')
fl.append("      </svg>")

# ------------------------------------------------------------------ figura 3: as partes de um controle
k7 = K1["K7"]
BLOCOS = [("E · ESPECIFICAR", "hd-p", "bx-p", [("O QUE CONTROLAR", f'{k7["caract"]}, na etapa “{k7["etapa"]}”'), ("CRITÉRIO", f'No mínimo {num(k7["min"])} {k7["unid"]}')]),
          ("M · MEDIR", "hd-d", "bx-d", [("COMO MEDIR", k7["metodo"]), ("FREQUÊNCIA", k7["freq"]), ("QUEM · REGISTRO", f'{k7["resp"]} · {k7["registro"]}')]),
          ("R · REAGIR", "hd-c", "bx-c", [("REAÇÃO", k7["reacao"]), ("COM O PRODUTO E COM O PROCESSO", "A pizza é reaquecida ou refeita. A bolsa térmica é conferida, para o desvio não se repetir.")])]
an = ['      <svg viewBox="0 0 900 252" role="img" aria-label="As partes do controle K7 da pizzaria, em três blocos. '
      + " ".join(f'{t}: ' + " ".join(f"{a.lower()}: {b}." for a, b in itens) for t, _, _, itens in BLOCOS) + '">']
for j, (tit, hd, bx, itens) in enumerate(BLOCOS):
    x = 20 + j * 290
    an.append(f'        <rect class="{bx}" x="{x}" y="12" width="280" height="190"/>')
    an.append(f'        <rect class="{hd}" x="{x}" y="12" width="280" height="32"/>')
    an.append(f'        <text class="b on" x="{x + 12}" y="33" font-size="12.5">{tit}</text>')
    y = 64
    for rot, txt in itens:
        an.append(f'        <text class="mono mu" x="{x + 12}" y="{y}" font-size="9.5">{rot}</text>')
        y = lines(an, txt, x + 12, y + 16, 46, fs=11, step=14) + 12
an.append('        <text x="450" y="226" font-size="11.5" text-anchor="middle">Um controle completo responde às três perguntas: o que se espera, como se confere e o que fazer se não der certo.</text>')
an.append('        <text class="mu" x="450" y="244" font-size="11" text-anchor="middle">Sem o critério, cada um aceita um resultado. Sem a reação, o registro vira arquivo.</text>')
an.append("      </svg>")

# ------------------------------------------------------------------ figura 4: a cadeia de identificação
ra = ['      <svg viewBox="0 0 900 250" role="img" aria-label="A cadeia de identificação da pizzaria. '
      + " ".join(f"{e}: identificação: {i} Situação: {s}" for e, i, s, _, _ in EX1["rast"]) + ' A cadeia permite ir do pedido entregue ao lote de massa e à nota do insumo, e voltar.">',
      "        <defs>" + marker("a4") + marker("a4m", True) + "</defs>"]
for j, (e, ident, sit, _, _) in enumerate(EX1["rast"]):
    x = 12 + j * (W5 + G5)
    ra.append(f'        <rect class="bx" x="{x}" y="14" width="{W5}" height="170"/>')
    ra.append(f'        <rect class="hd-ink" x="{x}" y="14" width="{W5}" height="40"/>')
    ls = textwrap.wrap(e, 24)[:2]
    for i, l in enumerate(ls):
        ra.append(f'        <text class="b t-ground" x="{x + 10}" y="{(39 if len(ls) == 1 else 31) + i * 14}" font-size="11.5">{escape(l)}</text>')
    ra.append(f'        <text class="mono mu" x="{x + 10}" y="74" font-size="9.5">IDENTIFICAÇÃO</text>')
    lines(ra, ident, x + 10, 89, 27, fs=10.5)
    ra.append(f'        <text class="mono mu" x="{x + 10}" y="136" font-size="9.5">SITUAÇÃO</text>')
    lines(ra, sit, x + 10, 151, 27, fs=10.5)
    if j < 4:
        ra.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="34" x2="{x + W5 + G5 - 2}" y2="34" marker-end="url(#a4)"/>')
ra.append(f'        <path class="ln-mu dash" d="M{12 + 4 * (W5 + G5) + W5 / 2} 186 V212 H{12 + W5 / 2} V190" marker-end="url(#a4m)"/>')
ra.append('        <text class="mu halo" x="450" y="216" font-size="11" text-anchor="middle">rastrear para trás: do pedido entregue ao lote de massa e à nota do insumo</text>')
ra.append('        <text x="450" y="242" font-size="11.5" text-anchor="middle">A identificação diz o que é. A situação diz se já foi verificado e se pode seguir.</text>')
ra.append("      </svg>")

# ------------------------------------------------------------------ figura 5: a busca de rastreabilidade
e3 = ['      <svg viewBox="0 0 900 366" role="img" aria-label="Uma busca de rastreabilidade na indústria. ' + BUSCA["gatilho"] + " Para trás: "
      + " ".join(f"{a}: {b}" for a, b in BUSCA["tras"]) + " Para a frente: " + " ".join(f"{a}: {b}" for a, b in BUSCA["frente"]) + " " + BUSCA["conclusao"] + '">',
      "        <defs>" + marker("a5") + "</defs>",
      '        <rect class="bx-ink" x="230" y="10" width="440" height="46"/>',
      '        <text class="mono t-ground" x="242" y="28" font-size="9.5">O PONTO DE PARTIDA</text>',
      f'        <text class="b t-ground" x="242" y="46" font-size="12">{escape(BUSCA["gatilho"])}</text>']
for j, (tit, itens, cls) in enumerate((("PARA TRÁS · de onde veio", BUSCA["tras"], "bx-p"), ("PARA A FRENTE · para onde foi", BUSCA["frente"], "bx-c"))):
    x = 20 + j * 440
    e3.append(f'        <path class="ln" d="M450 57 V70 H{x + 210} V84" marker-end="url(#a5)"/>')
    e3.append(f'        <text class="mono mu" x="{x}" y="104" font-size="10">{tit}</text>')
    for i, (a, b) in enumerate(itens):
        y = 114 + i * 68
        e3.append(f'        <rect class="{cls}" x="{x}" y="{y}" width="420" height="58"/>')
        e3.append(f'        <text class="b" x="{x + 12}" y="{y + 20}" font-size="11.5">{i + 1}. {escape(a)}</text>')
        lines(e3, b, x + 12, y + 36, 74, fs=10.5, maxl=2)
for i, l in enumerate(textwrap.wrap(BUSCA["conclusao"], 118)[:2]):
    e3.append(f'        <text x="450" y="{334 + i * 16}" font-size="11.5" text-anchor="middle">{escape(l)}</text>')
e3.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Processo</dt><dd>{escape(h["processo"])}</dd></div>',
                      f'    <div><dt>Produto ou serviço</dt><dd>{escape(h["produto"])}</dd></div>',
                      f'    <div><dt>Plano de controle</dt><dd>{escape(h["rev"])}. {escape(h["por"])}.</dd></div>',
                      f'    <div><dt>Registros</dt><dd>{escape(h["periodo"])}, lidos em {dt(h["ref"])}.</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      '  </dl>'])


def tabela(caption, heads, rows, cls="aud"):
    o = ['  <div class="tbl">', f'    <table class="{cls}">', f'      <caption>{caption}</caption>', f'      <thead><tr>{"".join(heads)}</tr></thead>', '      <tbody>']
    o += [f'        <tr>{r}</tr>' for r in rows]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def plano_tab(ex):
    n_et = len({k["etapa"] for k in ex["plano"]})
    rows = [f'<td class="c n">{k["id"]}</td><td>{escape(k["etapa"])}</td><td><strong>{escape(k["caract"])}</strong><small>{k["tipo"]}</small></td><td>{escape(criterio(k))}</td>'
            f'<td>{escape(k["metodo"])}<small>{escape(k["freq"])}</small></td><td>{escape(k["resp"])}<small>{escape(k["registro"])}</small></td><td>{escape(k["reacao"])}</td>' for k in ex["plano"]]
    return tabela(f'Plano de controle · {len(ex["plano"])} controles, em {n_et} etapas',
                  ['<th class="c">#</th>', '<th style="width:13%">Etapa</th>', '<th style="width:19%">O que controlar<small>Produto ou processo</small></th>', '<th style="width:11%">Critério</th>',
                   '<th style="width:18%">Como medir<small>Frequência</small></th>', '<th style="width:13%">Quem<small>Registro</small></th>', '<th>Reação se sair do critério</th>'], rows)


def chip_k(x):
    if x["semr"]:
        return '<span class="chip s3">Fora, sem reação</span>'
    if x["fora"] > 1:
        return '<span class="chip s2">Desvio repetido</span>'
    if x["fora"]:
        return '<span class="chip s2">Um desvio, com reação</span>'
    return '<span class="chip s1">Dentro do critério</span>'


def resumo_tab(ex):
    r = resumo(ex)
    rows = [f'<td class="c n">{x["k"]["id"]}</td><td><strong>{escape(x["k"]["caract"])}</strong></td><td>{escape(criterio(x["k"]))}</td><td class="c">{x["n"]}</td>'
            f'<td class="c{" no" if x["fora"] else ""}">{x["fora"]}</td><td class="c">{pc(x["dentro"])}</td><td>{chip_k(x)}</td>' for x in resumo_k(ex)]
    return tabela(f'Registros · {r["n"]} verificações, {r["fora"]} fora do critério, {r["semr"]} sem reação registrada',
                  ['<th class="c">#</th>', '<th style="width:36%">O que se controla</th>', '<th>Critério</th>', '<th class="c">Verificações</th>', '<th class="c">Fora</th>', '<th class="c">Dentro</th>',
                   '<th>Leitura</th>'], rows)


def fora_tab(ex):
    ks = {k["id"]: k for k in ex["plano"]}
    rows = []
    for r in ex["regs"]:
        k = ks[r["k"]]
        if leitura(k, r) == FORA:
            reac = escape(r["reacao"]) if r["reacao"] else '<span class="chip s3">Sem reação registrada</span>'
            rows.append(f'<td class="c">{dt(r["data"])}</td><td>{escape(r["lote"])}</td><td><strong>{k["id"]}</strong> · {escape(k["caract"])}</td><td>{escape(criterio(k))}</td>'
                        f'<td class="c no">{escape(valor(k, r))}</td><td>{reac}</td>')
    return tabela('Resultados fora do critério',
                  ['<th class="c">Data</th>', '<th style="width:14%">Lote ou pedido</th>', '<th style="width:25%">Controle</th>', '<th>Critério</th>', '<th class="c">Resultado</th>',
                   '<th style="width:34%">Reação registrada</th>'], rows)


def rast_tab(ex):
    rows = [f'<td><strong>{escape(e)}</strong></td><td>{escape(i)}</td><td>{escape(s)}</td><td>{escape(g)}</td><td>{escape(p) or "—"}</td>' for e, i, s, g, p in ex["rast"]]
    return tabela('Identificação, situação e preservação',
                  ['<th style="width:17%">Etapa</th>', '<th style="width:22%">Como o produto é identificado</th>', '<th style="width:21%">Como se sabe a situação</th>',
                   '<th style="width:19%">O que se registra para rastrear</th>', '<th>Como se preserva</th>'], rows)


def prop_tab(ex):
    rows = [f'<td><strong>{escape(a)}</strong></td><td>{escape(b)}</td><td>{escape(c)}</td><td>{escape(d)}</td><td>{escape(e) or "Nenhuma no período."}</td>' for a, b, c, d, e in ex["prop"]]
    return tabela('Propriedade de clientes e de fornecedores',
                  ['<th style="width:22%">Item</th>', '<th style="width:10%">De quem é</th>', '<th style="width:20%">Identificação</th>', '<th style="width:22%">Cuidado</th>',
                   '<th>Ocorrência e comunicação ao dono</th>'], rows)


def mud_conf(m):
    if not m[3]:
        return "Falta a análise"
    if not m[4]:
        return "Falta quem autorizou"
    return "OK"


def mud_tab(ex):
    rows = []
    for m in ex["mud"]:
        c = mud_conf(m)
        rows.append(f'<td class="c">{dt(m[0])}</td><td><strong>{escape(m[1])}</strong><small>{escape(m[2])}</small></td><td>{escape(m[3]) or "—"}</td><td>{escape(m[4]) or "—"}</td>'
                    f'<td>{escape(m[5]) or "—"}</td><td><span class="chip {"s1" if c == "OK" else "s3"}">{c}</span></td>')
    cap = 'Mudanças no processo' + (f' · registro lido em {dt(ex["head"]["mud_ref"])}' if ex["head"].get("mud_ref") else '')
    return tabela(cap,
                  ['<th class="c">Data</th>', '<th style="width:26%">O que mudou<small>Motivo</small></th>', '<th style="width:22%">Análise antes de mudar</th>', '<th style="width:13%">Quem autorizou</th>',
                   '<th>Ações decorrentes</th>', '<th>Conferência</th>'], rows)


rows = [f'<td><strong>{escape(a)}</strong></td><td>{escape(b)}</td><td>{escape(c)}</td>' for a, b, c in PARTES]
partestab = tabela("", ['<th style="width:18%">Campo</th>', '<th style="width:42%">O que responde</th>', '<th>No controle K7 da pizzaria</th>'], rows, cls="").replace("      <caption></caption>\n", "").replace(' class=""', "")

# ------------------------------------------------------------------ módulo 7: as leituras de um controle, em ordem
kc = K1["K1"]
rs = [r for r in EX1["regs"] if r["k"] == "K1"]
X0, X1, Y0, Y1, VMAX = 80, 860, 40, 240, 8
sx = lambda j: X0 + 30 + j * (X1 - X0 - 60) / (len(rs) - 1)  # noqa: E731
sy = lambda v: Y1 - v * (Y1 - Y0) / VMAX  # noqa: E731
fora_k = [r for r in rs if leitura(kc, r) == FORA]
ch = [f'      <svg id="run" viewBox="0 0 900 300" role="img" aria-label="As {len(rs)} leituras da temperatura da câmara fria da pizzaria, de 08 a 14 de março de 2027, com o critério de {criterio(kc)}. '
      + " ".join(f'{dt(r["data"], False)}, {r["lote"].split(", ")[1]}: {num(r["valor"])} °C, {leitura(kc, r).lower()}.' for r in rs) + '">',
      f'        <rect class="zone" x="{X0}" y="{sy(kc["max"])}" width="{X1 - X0}" height="{sy(kc["min"]) - sy(kc["max"])}"/>']
for v in range(0, VMAX + 1, 2):
    ch.append(f'        <line class="grid" x1="{X0}" y1="{sy(v)}" x2="{X1}" y2="{sy(v)}"/>')
    ch.append(f'        <text class="mu" x="{X0 - 10}" y="{sy(v) + 4}" font-size="11" text-anchor="end"{TNUM}>{v}</text>')
ch.append(f'        <line class="goal" x1="{X0}" y1="{sy(kc["max"])}" x2="{X1}" y2="{sy(kc["max"])}"/>')
ch.append(f'        <text class="mu halo" x="{X1 - 6}" y="{sy(kc["max"]) - 6}" font-size="11" text-anchor="end">máximo: {num(kc["max"])} °C</text>')
ch.append(f'        <text class="mono mu" x="{X0}" y="24" font-size="10">TEMPERATURA DA CÂMARA FRIA, EM °C</text>')
ch.append(f'        <rect class="zone" x="560" y="14" width="14" height="14"/><text x="582" y="26" font-size="11.5">Dentro do critério</text>')
ch.append('        <circle class="pt out" cx="730" cy="21" r="6"/><text x="744" y="26" font-size="11.5">Fora do critério</text>')
ch.append('        <polyline class="series" points="' + " ".join(f"{sx(j):.1f},{sy(r['valor']):.1f}" for j, r in enumerate(rs)) + '"/>')
for j, r in enumerate(rs):
    out = leitura(kc, r) == FORA
    ch.append(f'        <circle class="pt{" out" if out else ""}" data-k="{j}" cx="{sx(j):.1f}" cy="{sy(r["valor"]):.1f}" r="{6 if out else 5}"/>')
    if out:
        ch.append(f'        <text class="b halo" x="{sx(j):.1f}" y="{sy(r["valor"]) - 12:.1f}" font-size="11.5" text-anchor="middle">{num(r["valor"])} °C</text>')
    if j % 2 == 0:
        ch.append(f'        <text class="mu" x="{(sx(j) + sx(j + 1)) / 2:.1f}" y="{Y1 + 20}" font-size="11" text-anchor="middle"{TNUM}>{dt(r["data"], False)}</text>')
        if j:
            ch.append(f'        <line class="grid" x1="{(sx(j) + sx(j - 1)) / 2:.1f}" y1="{Y1}" x2="{(sx(j) + sx(j - 1)) / 2:.1f}" y2="{Y1 + 8}"/>')
ch.append(f'        <text class="mono mu" x="{(X0 + X1) / 2}" y="{Y1 + 44}" font-size="10" text-anchor="middle">UMA LEITURA EM CADA TURNO</text>')
w = (X1 - X0 - 60) / (len(rs) - 1)
for j, r in enumerate(rs):
    ch.append(f'        <rect class="hit" x="{sx(j) - w / 2:.1f}" y="{Y0}" width="{w:.1f}" height="{Y1 - Y0}" tabindex="0" role="img" '
              f'aria-label="{dt(r["data"], False)}, {r["lote"].split(", ")[1]}: {num(r["valor"])} °C, {leitura(kc, r).lower()}" data-k="{j}" data-v="{num(r["valor"])} °C" data-s="{leitura(kc, r)}" '
              f'data-d="{dt(r["data"], False)}, {r["lote"].split(", ")[1]}" data-cx="{sx(j):.1f}" data-cy="{sy(r["valor"]):.1f}"/>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th class="c">Data</th><th>Leitura</th><th class="c">Temperatura</th><th>Situação</th><th>Reação registrada</th></tr></thead>', '          <tbody>']
for r in rs:
    tb.append(f'            <tr><td class="c">{dt(r["data"], False)}</td><td>{escape(r["lote"].split(", ")[1])}</td><td class="c">{num(r["valor"])} °C</td><td>{leitura(kc, r)}</td><td>{escape(r["reacao"]) or "—"}</td></tr>')
tb += ['          </tbody>', '        </table>']
assert len(fora_k) == 1
jf = rs.index(fora_k[0])
antes = [num(r["valor"]) for r in rs[jf - 3:jf]]
charttext = (f'  <p>Das {len(rs)} leituras da semana, {len(rs) - 1} ficaram dentro do critério. A de {dt(fora_k[0]["data"], False)}, com {num(fora_k[0]["valor"])} °C, ficou fora, e a reação está registrada: '
             f'os insumos foram protegidos na hora, e a causa, a borracha da porta, foi corrigida no dia seguinte. O gráfico mostra algo que a lista de registros esconde: as três leituras anteriores, '
             f'{antes[0]}, {antes[1]} e {antes[2]} °C, estavam dentro do critério e subindo. Quem lê as leituras em ordem vê o desvio chegar. Quem lê uma a uma só vê o desvio quando ele acontece.</p>')

# ------------------------------------------------------------------ módulo 10: figura da ISO
ISOP = [("8.5.1 · Condições controladas", "Saber o que fazer e o resultado esperado, e conferir nas etapas certas, com recursos e pessoas adequados.", "o plano de controle e os registros"),
        ("8.5.2 · Identificar e rastrear", "Identificar o produto, quando preciso para a conformidade, e a situação dele. Rastrear, com registro, quando for requisito.", "a identificação por etapa e o exemplo 3"),
        ("8.5.3 e 8.5.4 · Cuidar e preservar", "Cuidar do que é do cliente ou do fornecedor, e proteger o produto até a entrega.", "as tabelas de propriedade e de preservação"),
        ("8.5.6 · Controlar as mudanças", "Analisar e controlar a mudança, na medida necessária, e registrar quem autorizou e o que foi feito.", "o registro de mudanças")]
iso = ['      <svg viewBox="0 0 900 200" role="img" aria-label="O que a norma pede sobre o controle da produção e do serviço. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in ISOP) + '">']
for k, (a, b, c) in enumerate(ISOP):
    x = 10 + k * 222
    iso.append(f'        <rect class="bx" x="{x}" y="14" width="214" height="172"/>')
    iso.append(f'        <rect class="hd-ink" x="{x}" y="14" width="214" height="34"/>')
    iso.append(f'        <text class="b t-ground" x="{x + 12}" y="36" font-size="11.5">{escape(a)}</text>')
    lines(iso, b, x + 12, 70, 32, fs=11.5, step=16, maxl=5)
    lines(iso, "Neste estudo: " + c, x + 12, 152, 34, fs=11, cls="mu", step=15, maxl=2)
iso.append("      </svg>")

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--MAPA-->", "\n".join(mp)), ("<!--FLUXO-->", "\n".join(fl)), ("<!--ANATOMIA-->", "\n".join(an)), ("<!--PARTESTAB-->", partestab), ("<!--CADEIA-->", "\n".join(ra)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1PLANO-->", plano_tab(EX1)), ("<!--EX1RESUMO-->", resumo_tab(EX1)), ("<!--EX1FORA-->", fora_tab(EX1)), ("<!--EX1RAST-->", rast_tab(EX1)),
                 ("<!--EX1PROP-->", prop_tab(EX1)), ("<!--EX1MUD-->", mud_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2PLANO-->", plano_tab(EX2)), ("<!--EX2RESUMO-->", resumo_tab(EX2)), ("<!--EX2FORA-->", fora_tab(EX2)), ("<!--EX2RAST-->", rast_tab(EX2)),
                 ("<!--EX2PROP-->", prop_tab(EX2)), ("<!--EX2MUD-->", mud_tab(EX2)),
                 ("<!--EX3FIG-->", "\n".join(e3)), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHARTTEXT-->", charttext),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Controle de produção e de serviço</title>")
assert "Controle de produção" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
r1, r2 = resumo(EX1), resumo(EX2)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", r1, "| indústria", r2)
