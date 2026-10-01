# -*- coding: utf-8 -*-
"""Monta treinamento-objetivos.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from obj_data import (ALC, ANDA, ANDA_O, CAM, CANC, CASCATA, CHECK, CONC, ETAPAS, EX1, EX2, MAIOR, MESES, NAOALC, NINI, PERGUNTAS, PLANO, RISCO, SEMR,  # noqa: E402
                      atende, atrasada, caminho, resumo, situacao, ultimo)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# alcançado, no caminho e em risco: a mesma paleta de três cores do estudo de Satisfação, validada para daltonismo nos dois modos
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
svg .track{fill:var(--sunk)}
svg .halo{paint-order:stroke;stroke:var(--surface);stroke-width:5px;stroke-linejoin:round}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas dos exemplos */
table.aud{font-size:.8rem;min-width:900px;line-height:1.4}
table.aud th, table.aud td{padding:8px 9px}
table.aud td.n{white-space:nowrap;font-weight:600;color:var(--muted)}
table.aud td.c, table.aud th.c{text-align:center;font-variant-numeric:tabular-nums}
table.aud td.ok{background:var(--s1-tint)}
table.aud td small, table.aud th small{display:block;color:var(--muted);font-size:.76rem;margin-top:3px;font-weight:400}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha do quadro (acima de cada exemplo) */"""
assert css.count("\n.ficha{") == 1
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

TNUM = ' style="font-variant-numeric:tabular-nums"'
SCLS = {ALC: "s1", CAM: "s2", RISCO: "s3", NAOALC: "s3", ANDA_O: "sl", SEMR: "sl"}
FCLS = {ALC: "f1", CAM: "f2", RISCO: "f3", NAOALC: "f3", ANDA_O: "f0", SEMR: "f0"}


def dt(d):
    return d.strftime("%d/%m/%Y") if d else "—"


def pc(v):
    return f"{int(100 * v + 0.5 + 1e-9)}%"


def num(v):
    if v is None:
        return "—"
    if float(v).is_integer():
        return str(int(v))
    return f"{v:g}".replace(".", ",")


def marker(i, mu=False):
    return (f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path class="{"ah-mu" if mu else "ah"}" d="M0 0 L10 5 L0 10 z"/></marker>')


def box(o, cls, x, y, w, h, tit, sub=None, fs=11.5, wrap=None, ink=False, tcls=""):
    """Caixa com título e, abaixo, linhas de texto quebradas."""
    o.append(f'        <rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>')
    t = " t-ground" if ink else ""
    yy = y + 20
    if tit:
        o.append(f'        <text class="b{t}{tcls}" x="{x + 10}" y="{yy}" font-size="{fs}">{escape(tit)}</text>')
        yy += 16
    for l in textwrap.wrap(sub or "", wrap or int(w / 5.8)):
        o.append(f'        <text class="{"t-ground" if ink else "mu"}" x="{x + 10}" y="{yy}" font-size="{fs - 1}">{escape(l)}</text>')
        yy += 14


H1, H2 = EX1["head"], EX2["head"]
O1 = EX1["objs"]
OBJ = {o["id"]: o for o in O1}

# ------------------------------------------------------------------ figura 1: a cadeia da política à ação
ROWS = [("POLÍTICA", "A que nos comprometemos?", [(c, t, c == "C1") for c, t in EX1["comps"]], "—"),
        ("OBJETIVO", "Quanto, e até quando?", [(o["id"], o["texto"], o["id"] == "O1") for o in O1 if o["comp"] == "C1"], "Entregas em até 40 minutos, todo mês"),
        ("PROCESSO", "Quem entrega o quê?", [(n.split(" (")[1][:-1], m, n.startswith("Entregar")) for n, m, _ in CASCATA["procs"]], "A medida de cada processo, todo mês"),
        ("AÇÃO", "O que será feito?", [(f"A{a['n']}", a["oque"], a["n"] == 1) for a in OBJ["O1"]["acoes"]], "Entregas no pico, por semana")]
ca = ['      <svg viewBox="0 0 900 350" role="img" aria-label="A cadeia da política à ação, com um fio da pizzaria. Política: ' + EX1["comps"][0][1]
      + ' Objetivo: ' + OBJ["O1"]["texto"] + ' Processo: ' + CASCATA["procs"][2][1] + ' Ação: ' + OBJ["O1"]["acoes"][0]["oque"] + ' Cada nível tem a sua medida.">',
      "        <defs>" + marker("a1") + "</defs>"]
prev = None
for k, (rot, perg, itens, medida) in enumerate(ROWS):
    y = 14 + k * 84
    ca.append(f'        <text class="mono mu" x="10" y="{y + 18}" font-size="10">{rot}</text>')
    ca.append(f'        <text class="mu" x="10" y="{y + 36}" font-size="10.5">{escape(perg)}</text>')
    xx = 160
    for cod, txt, hi in itens:
        w = 196
        cls = "bx-ink" if hi else "bx"
        ca.append(f'        <rect class="{cls}" x="{xx}" y="{y}" width="{w}" height="62"/>')
        ca.append(f'        <text class="mono {"t-ground" if hi else "mu"}" x="{xx + 10}" y="{y + 16}" font-size="9.5">{escape(cod)}</text>')
        for j, l in enumerate(textwrap.wrap(txt, 34)[:3]):
            ca.append(f'        <text class="{"t-ground" if hi else ""}" x="{xx + 10}" y="{y + 31 + j * 13}" font-size="10.5">{escape(l)}</text>')
        if hi:
            if prev:
                ca.append(f'        <line class="ln" x1="{prev}" y1="{y - 22}" x2="{xx + w / 2}" y2="{y - 3}" marker-end="url(#a1)"/>')
            prev = xx + w / 2
        xx += w + 10
    ca.append(f'        <text class="mono mu" x="782" y="{y + 16}" font-size="9.5">COMO SE MEDE</text>')
    for j, l in enumerate(textwrap.wrap(medida, 20)[:3]):
        ca.append(f'        <text class="mu" x="782" y="{y + 31 + j * 13}" font-size="10.5">{escape(l)}</text>')
ca.append('        <text x="450" y="344" font-size="11.5" text-anchor="middle">A caixa escura é um fio da pizzaria: do compromisso C1 ao plano do objetivo O1. Cada nível tem a sua medida.</text>')
ca.append("      </svg>")

# ------------------------------------------------------------------ figura 2: as cinco etapas
W5, G5 = 164, 14
fl = ['      <svg viewBox="0 0 900 206" role="img" aria-label="As cinco etapas do trabalho. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS) + ' A revisão devolve o trabalho à primeira etapa.">',
      "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
for k, (nome, desc) in enumerate(ETAPAS):
    x = 12 + k * (W5 + G5)
    fl.append(f'        <rect class="{["bx-p", "bx-d", "bx-d", "bx-c", "bx-ink"][k]}" x="{x}" y="16" width="{W5}" height="124"/>')
    ink = k == 4
    fl.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="36" font-size="10">{k + 1} · {"POA"[min(k, 2) if k < 3 else 2] if k != 1 else "O"}</text>')
    fl.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="58" font-size="13">{escape(nome)}</text>')
    for j, l in enumerate(textwrap.wrap(desc, 26)[:4]):
        fl.append(f'        <text{" class=" + chr(34) + "t-ground" + chr(34) if ink else ""} x="{x + 12}" y="{80 + j * 14.5}" font-size="10.5">{escape(l)}</text>')
    if k < 4:
        fl.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="78" x2="{x + W5 + G5 - 2}" y2="78" marker-end="url(#a2)"/>')
xa, xb = 12 + 4 * (W5 + G5) + W5 / 2, 12 + W5 / 2
fl.append(f'        <path class="ln-mu dash" d="M{xa} 142 V170 H{xb} V146" marker-end="url(#a2m)"/>')
fl.append('        <text class="mu halo" x="450" y="174" font-size="11" text-anchor="middle">na análise crítica, os objetivos do ano seguinte saem dos resultados deste</text>')
fl.append('        <text x="450" y="198" font-size="11.5" text-anchor="middle">P: política. O: objetivo. A: ação.</text>')
fl.append("      </svg>")

# ------------------------------------------------------------------ figura 3: as partes de um objetivo
o2 = OBJ["O2"]
PARTES_F = [("O QUÊ · verbo", "Reduzir", "bx-p", 110), ("O QUÊ · indicador", "as reclamações", "bx-p", 150), ("QUANTO · meta, a partir da base", "para no máximo 1,5 por 100 pedidos", "bx-d", 300),
            ("ATÉ QUANDO · prazo", "até 31/12/2027", "bx-c", 170)]
an = ['      <svg viewBox="0 0 900 262" role="img" aria-label="As partes do objetivo O2 da pizzaria. A frase: reduzir as reclamações para no máximo 1,5 por 100 pedidos até 31 de dezembro de 2027. '
      'O quê: o verbo reduzir e o indicador reclamações. Quanto: a meta de 1,5, a partir da base de 1,9. Até quando: o prazo. Na ficha: quem, o atendente líder; como se mede, '
      'reclamações por 100 pedidos, no registro, todo mês; e o plano, com duas ações.">']
x = 20
for rot, txt, cls, w in PARTES_F:
    an.append(f'        <text class="mono mu" x="{x + 2}" y="38" font-size="9.5">{escape(rot)}</text>')
    an.append(f'        <rect class="{cls}" x="{x}" y="48" width="{w}" height="44"/>')
    an.append(f'        <text class="b" x="{x + 12}" y="75" font-size="13">{escape(txt)}</text>')
    x += w + 14
an.append(f'        <text class="mu" x="{x - 14 + 6}" y="75" font-size="11">base: {num(o2["base"])}</text>')
box(an, "bx", 20, 120, 270, 70, "QUEM", f'{o2["resp"]}, no processo {o2["processo"].split(" (")[0].lower()}.', fs=11, tcls=" mono mu")
box(an, "bx", 304, 120, 290, 70, "COMO SE MEDE", f'{o2["ind"]}, no registro de reclamações, {o2["freq"].lower()}.', fs=11, tcls=" mono mu")
box(an, "bx-ink", 608, 120, 282, 70, "PLANO", "; ".join(a["oque"][:-1] for a in o2["acoes"]) + ".", fs=11, ink=True, tcls=" mono")
an.append('        <text x="450" y="226" font-size="11.5" text-anchor="middle">A frase responde a três perguntas. A ficha responde às outras duas, e traz o plano.</text>')
an.append('        <text class="mu" x="450" y="246" font-size="11" text-anchor="middle">Sem a base, não se sabe o tamanho do passo. Sem o plano, a meta é um desejo.</text>')
an.append("      </svg>")

# ------------------------------------------------------------------ figura 4: a ficha do objetivo O1
o1 = OBJ["O1"]
fi = [f'      <svg viewBox="0 0 900 326" role="img" aria-label="A ficha do objetivo O1 da pizzaria: {o1["texto"]} Compromisso {o1["comp"]}. Origem: {o1["origem"]}. '
      f'Indicador {o1["ind"]}, base {num(o1["base"])}, meta {num(o1["meta"])}, prazo {dt(o1["prazo"])}. Responsável: {o1["resp"]}, no processo {o1["processo"]}. '
      + "Ações: " + " ".join(f'{a["oque"]} Recursos: {a["rec"]}. Responsável: {a["resp"]}. Prazo: {dt(a["prazo"])}. Avaliação: {a["avalia"]}' for a in o1["acoes"]) + '">',
      '        <rect class="bx" x="20" y="10" width="860" height="306"/>',
      '        <rect class="hd-ink" x="20" y="10" width="860" height="36"/>',
      f'        <text class="b t-ground" x="36" y="33" font-size="13">{o1["id"]} · {escape(o1["texto"])}</text>']
cells = [("COMPROMISSO", f'{o1["comp"]} · {dict(EX1["comps"])[o1["comp"]]}'), ("ORIGEM", o1["origem"]), ("INDICADOR", f'{o1["ind"]}, {o1["freq"].lower()}'),
         ("BASE → META · PRAZO", f'{num(o1["base"])}% → {num(o1["meta"])}% · até {dt(o1["prazo"])}'), ("RESPONSÁVEL", o1["resp"]), ("PROCESSO", o1["processo"])]
for k, (rot, txt) in enumerate(cells):
    x, y = 36 + (k % 3) * 286, 62 + (k // 3) * 52
    fi.append(f'        <text class="mono mu" x="{x}" y="{y}" font-size="9.5">{rot}</text>')
    for j, l in enumerate(textwrap.wrap(txt, 46)[:2]):
        fi.append(f'        <text x="{x}" y="{y + 16 + j * 13}" font-size="11">{escape(l)}</text>')
fi.append('        <rect class="band" x="20" y="166" width="860" height="24"/>')
COLS = [("O QUE SERÁ FEITO", 36, 270), ("RECURSOS", 316, 170), ("QUEM", 496, 120), ("ATÉ QUANDO", 626, 86), ("COMO SE AVALIA", 722, 150)]
for rot, x, w in COLS:
    fi.append(f'        <text class="mono mu" x="{x}" y="182" font-size="9.5">{rot}</text>')
for k, a in enumerate(o1["acoes"]):
    y = 206 + k * 52
    fi.append(f'        <line class="grid" x1="20" y1="{y + 38}" x2="880" y2="{y + 38}"/>')
    for (rot, x, w), txt in zip(COLS, (a["oque"], a["rec"], a["resp"], dt(a["prazo"]), a["avalia"])):
        for j, l in enumerate(textwrap.wrap(txt, int(w / 5.6))[:3]):
            fi.append(f'        <text x="{x}" y="{y + 3 + j * 13}" font-size="10.5">{escape(l)}</text>')
fi.append("      </svg>")

# ------------------------------------------------------------------ figura 5: o desdobramento
e3 = ['      <svg viewBox="0 0 900 318" role="img" aria-label="O desdobramento do objetivo O1 da pizzaria. Compromisso: ' + CASCATA["comp"] + ' Objetivo: ' + CASCATA["obj"] + " "
      + " ".join(f"{n}: {m} Ação: {a}" for n, m, a in CASCATA["procs"]) + '">', "        <defs>" + marker("a5") + "</defs>"]
box(e3, "bx", 250, 10, 400, 46, None, None)
e3.append(f'        <text class="mono mu" x="262" y="28" font-size="9.5">POLÍTICA</text><text x="262" y="45" font-size="11.5">{escape(CASCATA["comp"])}</text>')
e3.append('        <line class="ln" x1="450" y1="57" x2="450" y2="72" marker-end="url(#a5)"/>')
e3.append('        <rect class="bx-ink" x="250" y="76" width="400" height="50"/>')
e3.append(f'        <text class="mono t-ground" x="262" y="94" font-size="9.5">OBJETIVO DA LOJA</text><text class="b t-ground" x="262" y="113" font-size="12">{escape(CASCATA["obj"])}</text>')
for k, (n, m, a) in enumerate(CASCATA["procs"]):
    x = 20 + k * 294
    e3.append(f'        <path class="ln" d="M450 127 V146 H{x + 133} V160" marker-end="url(#a5)"/>')
    e3.append(f'        <rect class="bx-p" x="{x}" y="164" width="266" height="68"/>')
    e3.append(f'        <text class="mono mu" x="{x + 10}" y="182" font-size="9.5">OBJETIVO DO PROCESSO · {escape(n.split(" (")[1][:-1])}</text>')
    e3.append(f'        <text class="b" x="{x + 10}" y="199" font-size="11.5">{escape(n.split(" (")[0])}</text>')
    for j, l in enumerate(textwrap.wrap(m, 44)[:2]):
        e3.append(f'        <text x="{x + 10}" y="{215 + j * 13}" font-size="10.5">{escape(l)}</text>')
    e3.append(f'        <line class="ln" x1="{x + 133}" y1="233" x2="{x + 133}" y2="248" marker-end="url(#a5)"/>')
    e3.append(f'        <rect class="bx-c" x="{x}" y="252" width="266" height="54"/>')
    e3.append(f'        <text class="mono mu" x="{x + 10}" y="270" font-size="9.5">AÇÃO</text>')
    for j, l in enumerate(textwrap.wrap(a, 44)[:2]):
        e3.append(f'        <text x="{x + 10}" y="{286 + j * 13}" font-size="10.5">{escape(l)}</text>')
e3.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Definição</dt><dd>{dt(h["data"])}. {escape(h["por"])}. {escape(h["periodo"])}.</dd></div>',
                      f'    <div><dt>Política da qualidade</dt><dd>{escape(h["politica"])}</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      f'    <div><dt>Acompanhamento</dt><dd>Resultados até {escape(MESES[h["meses"] - 1])}/2027, lidos em {dt(h["ref"])}.</dd></div>',
                      '  </dl>'])


def chip(s):
    return f'<span class="chip {SCLS[s]}">{s}</span>'


def objs_tab(ex):
    ref = ex["head"]["ref"]
    comps = dict(ex["comps"])
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>Quadro de objetivos · {len(ex["objs"])} objetivos, {len(ex["comps"])} compromissos da política</caption>',
         '      <thead><tr><th class="c">#</th><th style="width:26%">Objetivo<small>Compromisso · origem</small></th><th style="width:16%">Indicador<small>Unidade</small></th>'
         '<th class="c">Base</th><th class="c">Meta</th><th class="c">Prazo</th><th style="width:14%">Processo<small>Responsável</small></th><th class="c">Último</th><th>Situação</th><th class="c">Caminho</th></tr></thead>',
         '      </tbody>'.replace("</tbody>", "<tbody>")]
    for ob in ex["objs"]:
        s, c = situacao(ob, ref), caminho(ob)
        o.append(f'        <tr><td class="c n">{ob["id"]}</td><td><strong>{escape(ob["texto"])}</strong><small>{ob["comp"]} · {escape(comps[ob["comp"]])} · {escape(ob["origem"])}</small></td>'
                 f'<td>{escape(ob["ind"])}<small>{escape(ob["unid"])} · {"maior" if ob["sentido"] == MAIOR else "menor"} é melhor</small></td><td class="c">{num(ob["base"])}</td><td class="c">{num(ob["meta"])}</td>'
                 f'<td class="c">{dt(ob["prazo"])}</td><td>{escape(ob["processo"])}<small>{escape(ob["resp"])}</small></td><td class="c">{num(ultimo(ob))}</td><td>{chip(s)}</td>'
                 f'<td class="c">{"—" if c is None else pc(c)}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def plano_tab(ex):
    ref = ex["head"]["ref"]
    r = resumo(ex)
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>Planos · {r["acoes"]} ações, {r["conc"]} concluídas, {r["atras"]} atrasadas em {dt(ref)}</caption>',
         '      <thead><tr><th class="c">Obj.</th><th style="width:30%">O que será feito</th><th style="width:17%">Recursos</th><th>Quem</th><th class="c">Até quando</th><th>Status</th><th style="width:20%">Como se avalia</th></tr></thead>',
         '      <tbody>']
    for ob in ex["objs"]:
        for a in ob["acoes"]:
            if a["status"] == CONC:
                st = f'<span class="chip s1">{CONC}</span><small>{dt(a["feito"])}</small>'
            elif atrasada(a, ref):
                st = f'<span class="chip s3">Atrasada</span><small>{a["status"].lower()}</small>'
            else:
                st = f'<span class="chip sl">{a["status"]}</span>'
            o.append(f'        <tr><td class="c n">{ob["id"]}</td><td>{escape(a["oque"])}</td><td>{escape(a["rec"]) or "—"}</td><td>{escape(a["resp"])}</td><td class="c">{dt(a["prazo"])}</td>'
                     f'<td>{st}</td><td>{escape(a["avalia"])}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def acomp_tab(ex):
    n = ex["head"]["meses"]
    o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Acompanhamento · resultados de 2027</caption>',
         '      <thead><tr><th class="c">#</th><th style="width:28%">Indicador</th><th class="c">Base</th>' + "".join(f'<th class="c">{m}</th>' for m in MESES[:n]) + '<th class="c">Meta</th><th>Situação</th></tr></thead>',
         '      <tbody>']
    for ob in ex["objs"]:
        cells = "".join(f'<td class="c{" ok" if v is not None and atende(v, ob["meta"], ob["sentido"]) else ""}">{num(v)}</td>' for v in ob["res"])
        o.append(f'        <tr><td class="c n">{ob["id"]}</td><td><strong>{escape(ob["ind"])}</strong><small>{escape(ob["unid"])}</small></td><td class="c">{num(ob["base"])}</td>{cells}'
                 f'<td class="c">{num(ob["meta"])}</td><td>{chip(situacao(ob, ex["head"]["ref"]))}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>', '  <p><small>Célula em azul-claro: resultado que atende à meta.</small></p>']
    return "\n".join(o)


def tab3(rows, caption, heads):
    o = ['  <div class="tbl">', '    <table>', f'      <thead><tr>{"".join(f"<th{w}>{h}</th>" for h, w in heads)}</tr></thead>', '      <tbody>']
    for a, b, c in rows:
        o.append(f'        <tr><td><strong>{escape(a)}</strong></td><td>{escape(b)}</td><td>{escape(c)}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


pergtab = tab3(PERGUNTAS, "", [("Pergunta", ' style="width:18%"'), ("O que responde", ' style="width:40%"'), ("No exemplo O2 da pizzaria", "")])
planotab = tab3(PLANO, "", [("Resposta do 6.2.2", ' style="width:18%"'), ("O que é", ' style="width:36%"'), ("No exemplo O2 da pizzaria", "")])

# ------------------------------------------------------------------ módulo 7: o caminho percorrido
X0, W, TOP, RH, BH = 300, 360, 50, 40, 20
bottom = TOP + RH * len(O1)
ch = [f'      <svg id="bars" viewBox="0 0 900 {bottom + 48}" role="img" aria-label="O caminho percorrido por cada objetivo da pizzaria, da base até a meta, em maio de 2027. '
      + " ".join(f'{ob["id"]}, {ob["ind"]}: base {num(ob["base"])}, último {num(ultimo(ob))}, meta {num(ob["meta"])}, {situacao(ob, H1["ref"]).lower()}'
                 + (f', {pc(caminho(ob))} do caminho.' if caminho(ob) is not None else ".") for ob in O1) + '">', '        <g font-size="11.5">']
xs = X0
for k, (t, cls) in enumerate(((ALC, "f1"), (CAM, "f2"), (RISCO, "f3"))):
    ch.append(f'          <rect class="{cls}" x="{xs}" y="12" width="14" height="14"/><text x="{xs + 22}" y="24">{t}</text>')
    xs += 40 + len(t) * 6.6
ch.append('        </g>')
for v in (0, 0.25, 0.5, 0.75, 1):
    x = X0 + v * W
    ch.append(f'        <line class="{"goal" if v == 1 else "grid"}" x1="{x}" y1="{TOP - 8}" x2="{x}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{x}" y="{bottom + 16}" font-size="11" text-anchor="middle"{TNUM}>{"base" if v == 0 else "meta" if v == 1 else pc(v)}</text>')
ch.append(f'        <text class="mono mu" x="{X0 + W / 2}" y="{bottom + 36}" font-size="10" text-anchor="middle">CAMINHO PERCORRIDO</text>')
for k, ob in enumerate(O1):
    y = TOP + RH * k + (RH - BH) / 2
    s, c = situacao(ob, H1["ref"]), caminho(ob)
    v = 1.0 if s == ALC else (c or 0)
    ch.append(f'        <text x="20" y="{y + 15}" font-size="12"><tspan class="b">{ob["id"]}</tspan><tspan> · {escape(ob["ind"])}</tspan></text>')
    ch.append(f'        <rect class="track" x="{X0}" y="{y}" width="{W}" height="{BH}"/>')
    if v > 0:
        ch.append(f'        <rect class="bar {FCLS[s]}" data-k="{k}" x="{X0}" y="{y}" width="{v * W:.1f}" height="{BH}"/>')
    lab = f'{num(ob["base"])} → {num(ultimo(ob))} · meta {num(ob["meta"])}' if ob["base"] is not None else f'{num(ultimo(ob))} · meta {num(ob["meta"])}, sem base'
    ch.append(f'        <text class="halo" x="{X0 + W + 10}" y="{y + 15}" font-size="10.5"><tspan class="b">{escape(s)}</tspan><tspan class="mu"> · {escape(lab)}</tspan></text>')
for k, ob in enumerate(O1):
    s, c = situacao(ob, H1["ref"]), caminho(ob)
    ch.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" aria-label="{ob["id"]}, {escape(ob["ind"])}: {s}, base {num(ob["base"])}, último {num(ultimo(ob))}, meta {num(ob["meta"])}" '
              f'data-k="{k}" data-n="{ob["id"]} · {escape(ob["ind"])}" data-s="{s}" data-p="{"" if c is None else pc(c)[:-1]}" data-b="{num(ob["base"])}" data-u="{num(ultimo(ob))}" data-m="{num(ob["meta"])}" data-un="{escape(ob["unid"])}" data-cx="{X0 + W / 2}"/>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>Objetivo</th><th>Indicador</th><th class="c">Base</th><th class="c">Último</th><th class="c">Meta</th><th class="c">Caminho</th><th>Situação</th></tr></thead>', '          <tbody>']
for ob in O1:
    c = caminho(ob)
    tb.append(f'            <tr><td><strong>{ob["id"]}</strong></td><td>{escape(ob["ind"])}</td><td class="c">{num(ob["base"])}</td><td class="c">{num(ultimo(ob))}</td><td class="c">{num(ob["meta"])}</td>'
              f'<td class="c">{"—" if c is None else pc(c)}</td><td>{situacao(ob, H1["ref"])}</td></tr>')
tb += ['          </tbody>', '        </table>']
r1 = resumo(EX1)
charttext = (f'  <p>Em {dt(H1["ref"])}, {r1["sits"][ALC]} dos {r1["n"]} objetivos estão alcançados, {r1["sits"][CAM]} está no caminho e {r1["sits"][RISCO]} estão em risco. '
             f'Os dois em risco têm o mesmo caminho percorrido, zero, e causas diferentes: no desperdício, a ação não começou; nas entregas no prazo, a ação foi feita e não bastou. '
             f'O quadro não distingue os dois casos; a reunião distingue, lendo o plano ao lado do indicador. A cobertura da matriz de competências está em {pc(caminho(OBJ["O7"]))} do caminho em maio, '
             f'com prazo em outubro: adiantada. O objetivo da pesquisa não tem base, porque a pesquisa não existia em 2026; a planilha o lê só pela meta.</p>')

# ------------------------------------------------------------------ módulo 10: figura da ISO
PARTES = [("5.2 · Partir da política", "A política da qualidade é a base dos objetivos.", "Compromissos C1 a C4 e a ligação de cada objetivo"),
          ("6.2.1 · Objetivos mensuráveis", "Coerentes com a política, nos processos pertinentes, monitorados e comunicados.", "Indicador, base, meta, prazo e desdobramento"),
          ("6.2.2 · Planejar como alcançar", "O que será feito, recursos, responsável, prazo e avaliação.", "A ficha do objetivo e a aba Planos"),
          ("9.3 · Avaliar o alcance", "A análise crítica considera quanto de cada objetivo foi alcançado.", "Situação, caminho percorrido e fechamento do ano")]
iso = ['      <svg viewBox="0 0 900 190" role="img" aria-label="O que a norma pede sobre objetivos da qualidade. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in PARTES) + '">']
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
for tag, val in (("<!--CASCATA-->", "\n".join(ca)), ("<!--FLUXO-->", "\n".join(fl)), ("<!--ANATOMIA-->", "\n".join(an)), ("<!--PERGTAB-->", pergtab), ("<!--FICHA-->", "\n".join(fi)),
                 ("<!--PLANOTAB-->", planotab), ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1OBJS-->", objs_tab(EX1)), ("<!--EX1PLANO-->", plano_tab(EX1)), ("<!--EX1ACOMP-->", acomp_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2OBJS-->", objs_tab(EX2)), ("<!--EX2PLANO-->", plano_tab(EX2)), ("<!--EX2ACOMP-->", acomp_tab(EX2)),
                 ("<!--EX3FIG-->", "\n".join(e3)), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHARTTEXT-->", charttext),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Objetivos da qualidade</title>")
assert "Objetivos da qualidade" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", r1["sits"], "| indústria", resumo(EX2)["sits"])
