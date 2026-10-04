# -*- coding: utf-8 -*-
"""Monta treinamento-escopo.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from esc_data import (CAMPOS, CHECK, COMPROMISSOS, DECLARACOES, DEM, ETAPAS, EX1, EX2, EXCLUIVEL, NAO, NDEM, OBRIG, PARC, REFORCADA,  # noqa: E402
                      aplicabilidade, escopo_conf, lider_conf, resumo)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# demonstrado, parcial e não demonstrado: a mesma paleta de três cores do estudo de Satisfação, validada para daltonismo nos dois modos
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
svg .f1{fill:var(--s1)} svg .f2{fill:var(--s2)} svg .f3{fill:var(--s3)}
svg .bx-s1{fill:var(--s1-tint);stroke:var(--s1);stroke-width:1.5} svg .bx-s2{fill:var(--s2-tint);stroke:var(--s2);stroke-width:1.5} svg .bx-s3{fill:var(--s3-tint);stroke:var(--s3);stroke-width:1.5}
svg .on-s2{fill:var(--on-s2)}
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

/* Ficha do escopo (acima de cada exemplo) */"""
assert css.count("\n.ficha{") == 1
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")


def dt(d, ano=True):
    return d.strftime("%d/%m/%Y" if ano else "%d/%m") if d else "—"


def marker(i, mu=False):
    return (f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path class="{"ah-mu" if mu else "ah"}" d="M0 0 L10 5 L0 10 z"/></marker>')


def lines(o, txt, x, y, wrap, fs=10.5, cls="", step=13, maxl=3, anchor=None):
    """Texto quebrado em linhas; devolve o y da linha seguinte."""
    ls = textwrap.wrap(txt, wrap)[:maxl]
    attr = (f' class="{cls}"' if cls else "") + (f' text-anchor="{anchor}"' if anchor else "")
    for j, l in enumerate(ls):
        o.append(f'        <text{attr} x="{x}" y="{y + j * step}" font-size="{fs}">{escape(l)}</text>')
    return y + step * len(ls)


def box(o, cls, x, y, w, h, tit, sub, ink=False, fs=12, maxl=2):
    o.append(f'        <rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>')
    o.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{y + 24}" font-size="{fs}">{escape(tit)}</text>')
    if sub:
        lines(o, sub, x + 12, y + 41, int(w / 5.6), fs=10.5, cls="t-ground" if ink else "mu", maxl=maxl, step=13)


# ------------------------------------------------------------------ figura 1: do contexto ao sistema
cx = ['      <svg viewBox="0 0 900 312" role="img" aria-label="Do contexto ao sistema. As questões internas e externas, as partes interessadas e os produtos e serviços entram no escopo, '
      'que define os limites e a aplicabilidade. O escopo delimita o sistema de gestão: os processos e os requisitos que se aplicam. Por baixo de tudo, a liderança: a direção responde pelo sistema.">',
      "        <defs>" + marker("a1") + "</defs>"]
for k, (tit, sub) in enumerate((("4.1 · Questões internas e externas", "O que acontece dentro e fora"), ("4.2 · Partes interessadas", "Quem espera o quê"),
                                ("Produtos e serviços", "O que a organização fornece"))):
    y = 14 + k * 70
    box(cx, "bx", 20, y, 230, 58, tit, sub)
    cx.append(f'        <path class="ln" d="M251 {y + 29} H290 V114 H316" marker-end="url(#a1)"/>')
box(cx, "bx-ink", 320, 70, 240, 88, "4.3 · Escopo", "Os limites e a aplicabilidade: o que está dentro, e que requisito não se aplica", ink=True, maxl=3)
cx.append('        <line class="ln" x1="561" y1="114" x2="606" y2="114" marker-end="url(#a1)"/>')
box(cx, "bx-s1", 610, 70, 270, 88, "4.4 · O sistema de gestão", "Os processos e os requisitos que se aplicam a eles", maxl=3)
cx.append('        <rect class="bx-s2" x="20" y="226" width="860" height="56"/>')
cx.append('        <text class="b" x="34" y="250" font-size="12.5">5.1 · Liderança</text>')
cx.append('        <text x="34" y="268" font-size="11">A direção responde pelo sistema: dá o rumo, os recursos e o exemplo. Sem ela, o escopo é só um papel.</text>')
for x in (135, 440, 745):
    cx.append(f'        <line class="ln-mu dash" x1="{x}" y1="225" x2="{x}" y2="{218 if x == 135 else 162}" marker-end="url(#a1)"/>')
cx.append('        <text x="450" y="304" font-size="11.5" text-anchor="middle">O escopo diz onde o sistema vale. A liderança faz o sistema valer.</text>')
cx.append("      </svg>")

# ------------------------------------------------------------------ figura 2: as cinco etapas
W5, G5 = 164, 14
et = ['      <svg viewBox="0 0 900 222" role="img" aria-label="As cinco etapas do trabalho. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS) + ' A revisão do escopo volta ao contexto quando ele muda.">',
      "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
for k, (nome, desc) in enumerate(ETAPAS):
    x = 12 + k * (W5 + G5)
    ink = k == 2
    et.append(f'        <rect class="{["bx", "bx", "bx-ink", "bx-s1", "bx-s2"][k]}" x="{x}" y="16" width="{W5}" height="140"/>')
    et.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="36" font-size="10">ETAPA {k + 1}</text>')
    tl = textwrap.wrap(nome, 22)[:2]
    for j, l in enumerate(tl):
        et.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{58 + j * 15}" font-size="12.5">{escape(l)}</text>')
    lines(et, desc, x + 12, 80 if len(tl) == 1 else 92, 26, cls="t-ground" if ink else "", step=14.5, maxl=5)
    if k < 4:
        et.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="78" x2="{x + W5 + G5 - 2}" y2="78" marker-end="url(#a2)"/>')
xa, xb = 12 + 3 * (W5 + G5) + W5 / 2, 12 + W5 / 2
et.append(f'        <path class="ln-mu dash" d="M{xa} 158 V186 H{xb} V162" marker-end="url(#a2m)"/>')
et.append(f'        <text class="mu halo" x="{(xa + xb) / 2}" y="190" font-size="11" text-anchor="middle">quando o contexto muda: unidade nova, produto novo, terceirização</text>')
et.append('        <text x="450" y="214" font-size="11.5" text-anchor="middle">As quatro primeiras etapas são o 4.3. A quinta é o 5.1, e acompanha o sistema o tempo todo.</text>')
et.append("      </svg>")

# ------------------------------------------------------------------ figura 3: a fronteira do escopo, na indústria
PROCS = ["Vender e programar", "Desenvolver", "Extrusar", "Imprimir", "Cortar", "Inspecionar e expedir"]
fr = ['      <svg viewBox="0 0 900 270" role="img" aria-label="A fronteira do escopo da indústria. Dentro do escopo: vender e programar, desenvolver, extrusar, imprimir, cortar, inspecionar e expedir, '
      'com a gestão e os processos de apoio. Na fronteira: o armazém externo, operado por empresa contratada, entra no escopo como processo terceirizado, controlado pela avaliação de fornecedores. '
      'Fora do escopo: os fornecedores e os clientes.">',
      "        <defs>" + marker("a3") + "</defs>",
      '        <rect class="bx-out" x="120" y="14" width="640" height="210"/>',
      '        <text class="mono mu" x="134" y="34" font-size="10">DENTRO DO ESCOPO · A FÁBRICA</text>']
for k, p in enumerate(PROCS):
    x = 134 + k * 100
    fr.append(f'        <rect class="bx" x="{x}" y="50" width="92" height="56"/>')
    lines(fr, p, x + 8, 72, 14, fs=10.5, maxl=2)
    if k < len(PROCS) - 1:
        fr.append(f'        <line class="ln" x1="{x + 93}" y1="78" x2="{x + 99}" y2="78"/>')
box(fr, "bx", 134, 122, 276, 50, "Gestão do sistema", "Política, objetivos, auditoria, análise crítica", fs=11.5, maxl=1)
box(fr, "bx", 422, 122, 258, 50, "Apoio", "Suprimentos, manutenção, laboratório, pessoas", fs=11.5, maxl=1)
fr.append('        <rect class="bx-s2" x="690" y="184" width="190" height="62"/>')
fr.append('        <text class="b" x="702" y="204" font-size="11.5">Armazém externo</text>')
lines(fr, "Terceirizado: dentro do escopo, controlado pelo 8.4.", 702, 220, 32, fs=10.5, maxl=2)
fr.append('        <path class="ln" d="M712 107 V182" marker-end="url(#a3)"/>')
box(fr, "bx", 10, 50, 96, 56, "Fornecedores", None, fs=11)
box(fr, "bx", 790, 50, 100, 56, "Clientes", None, fs=11)
fr.append('        <line class="ln" x1="107" y1="78" x2="132" y2="78" marker-end="url(#a3)"/>')
fr.append('        <line class="ln" x1="727" y1="78" x2="788" y2="78" marker-end="url(#a3)"/>')
fr.append('        <text x="450" y="262" font-size="11.5" text-anchor="middle">Terceirizar não tira do escopo: a organização continua respondendo pelo que o terceiro faz por ela.</text>')
fr.append("      </svg>")

# ------------------------------------------------------------------ figura 4: a árvore da não aplicabilidade
ar = ['      <svg viewBox="0 0 900 262" role="img" aria-label="Como decidir se um requisito pode ser declarado não aplicável. Primeira pergunta: alguma atividade da organização está ligada ao requisito? '
      'Se sim, ele se aplica. Se não, segunda pergunta: deixar de aplicá-lo afeta a conformidade do produto ou a satisfação do cliente? Se sim, ele se aplica. Se não, pode ser declarado não aplicável, '
      'com a justificativa no escopo. Os requisitos das seções 4, 5, 6, 9 e 10 se aplicam sempre.">',
      "        <defs>" + marker("a4") + "</defs>"]
box(ar, "bx-ink", 20, 20, 250, 70, "Alguma atividade se liga a ele?", "Projetar, medir, guardar algo do cliente, atender depois da entrega", ink=True, fs=11.5)
box(ar, "bx-ink", 330, 20, 250, 70, "Deixar de aplicá-lo afeta o cliente?", "A conformidade do produto, ou a satisfação do cliente", ink=True, fs=11.5)
box(ar, "bx-s1", 640, 20, 240, 70, "Pode ser não aplicável", "Com a justificativa escrita no escopo")
box(ar, "bx-s3", 20, 150, 250, 56, "Aplica-se", "Mesmo que a organização não queira")
box(ar, "bx-s3", 330, 150, 250, 56, "Aplica-se", "Excluir seria esconder um risco")
ar += ['        <line class="ln" x1="271" y1="55" x2="328" y2="55" marker-end="url(#a4)"/>', '        <text class="mu halo" x="299" y="48" font-size="10.5" text-anchor="middle">não</text>',
       '        <line class="ln" x1="581" y1="55" x2="638" y2="55" marker-end="url(#a4)"/>', '        <text class="mu halo" x="609" y="48" font-size="10.5" text-anchor="middle">não</text>',
       '        <line class="ln" x1="145" y1="91" x2="145" y2="148" marker-end="url(#a4)"/>', '        <text class="mu halo" x="153" y="124" font-size="10.5">sim</text>',
       '        <line class="ln" x1="455" y1="91" x2="455" y2="148" marker-end="url(#a4)"/>', '        <text class="mu halo" x="463" y="124" font-size="10.5">sim</text>',
       '        <rect class="bx" x="640" y="150" width="240" height="56"/>',
       '        <text class="mono mu" x="652" y="170" font-size="9.5">SE APLICAM SEMPRE</text>',
       '        <text x="652" y="188" font-size="10.5">As seções 4, 5, 6, 9 e 10, e quase</text>', '        <text x="652" y="201" font-size="10.5">todo o restante da 7 e da 8.</text>',
       '        <text x="450" y="240" font-size="11.5" text-anchor="middle">Na prática, os candidatos são poucos: a rastreabilidade do 7.1.5, o 8.3, o 8.5.3 e o 8.5.5. E mesmo eles costumam se aplicar.</text>',
       "      </svg>"]

excltab = ['  <div class="tbl">', '    <table>', '      <thead><tr><th style="width:10%">Requisito</th><th style="width:44%">Pode não se aplicar quando</th><th>Mas costuma se aplicar porque</th></tr></thead>', '      <tbody>']
PORQUE = {"7.1.5": "Quase toda organização mede algo de que o cliente depende: temperatura, peso, espessura, tempo. E conferir documentos também é monitorar.",
          "8.3": "Quem cria sabores, adapta produtos ou desenvolve sob encomenda está projetando.",
          "8.5.3": "Dados do cliente, cilindros, embalagens retornáveis e bolsas da plataforma são propriedade de terceiros.",
          "8.5.5": "Troca, garantia e assistência técnica são atividades pós-entrega."}
for num, quando in EXCLUIVEL.items():
    excltab.append(f'        <tr><td class="num">{num}</td><td>{escape(quando)}</td><td>{escape(PORQUE[num])}</td></tr>')
excltab += ['      </tbody>', '    </table>', '  </div>']


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Escopo escrito em</dt><dd>{dt(h["data"])}. {escape(h["por"])}.</dd></div>',
                      f'    <div><dt>Leitura</dt><dd>{dt(h["ref"])}.</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      '  </dl>'])


def tabela(caption, heads, rows):
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{caption}</caption>', f'      <thead><tr>{"".join(heads)}</tr></thead>', '      <tbody>']
    o += [f'        <tr>{r}</tr>' for r in rows]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def conf_chip(c):
    return f'<span class="chip {"s1" if c == "OK" else "s2" if c == REFORCADA else "s3"}">{escape(c)}</span>'


def escopo_tab(ex):
    e = ex["escopo"]
    falta = escopo_conf(e)
    rows = []
    for k, rot in CAMPOS:
        c = "OK" if e[k] or k not in OBRIG else f"Falta: {rot.lower()}"
        rows.append(f'<td><strong>{escape(rot)}</strong></td><td>{escape(e[k]) or "—"}</td><td>{conf_chip(c) if k in OBRIG else ""}</td>')
    return tabela(f'Escopo · {len(falta)} campo{"s" if len(falta) != 1 else ""} obrigatório{"s" if len(falta) != 1 else ""} em branco',
                  ['<th style="width:20%">Campo</th>', '<th>Conteúdo</th>', '<th style="width:18%">Conferência</th>'], rows)


def aplic_tab(ex):
    r = resumo(ex)
    rows = [f'<td class="n">{a["num"]}</td><td><strong>{escape(a["tit"])}</strong></td><td>{escape(a["just"])}</td><td class="c{" no" if a["afeta"] == "Sim" else ""}">{a["afeta"]}</td>'
            f'<td>{conf_chip(a["conf"])}</td>' for a in aplicabilidade(ex) if a["aplica"] == NAO]
    return tabela(f'Aplicabilidade · {r["reqs"]} requisitos: {r["aplic"]} aplicáveis, {r["naoap"]} declarado{"s" if r["naoap"] != 1 else ""} não aplicáve{"is" if r["naoap"] != 1 else "l"}',
                  ['<th>Requisito</th>', '<th style="width:28%">Título</th>', '<th style="width:30%">Justificativa</th>', '<th class="c">Afeta o cliente?</th>', '<th>Conferência</th>'], rows)


SIT_CLS = {DEM: "s1", PARC: "s2", NDEM: "s3"}


def lider_tab(ex):
    r = resumo(ex)
    rows = []
    for k, ((tit, _), c) in enumerate(zip(COMPROMISSOS, ex["lid"]), 1):
        acao = (escape(c["acao"]) + f'<small>{escape(c["resp"])} · até {dt(c["prazo"], False)}</small>') if c["acao"] else "—"
        rows.append(f'<td class="c n">{k}</td><td><strong>{escape(tit)}</strong></td><td>{escape(c["faz"])}<small>{escape(c["freq"]) or "—"} · {escape(c["reg"]) or "sem registro"}</small></td>'
                    f'<td><span class="chip {SIT_CLS[c["sit"]]}">{c["sit"]}</span></td><td>{acao}</td><td>{conf_chip(lider_conf(c))}</td>')
    return tabela(f'Liderança · {r["dem"]} demonstrados, {r["parc"]} parciais, {r["ndem"]} não demonstrado{"s" if r["ndem"] != 1 else ""}',
                  ['<th class="c">#</th>', '<th style="width:16%">Compromisso</th>', '<th style="width:34%">O que a direção faz<small>Frequência · registro</small></th>', '<th>Situação</th>',
                   '<th style="width:24%">Ação</th>', '<th>Conferência</th>'], rows)


# ------------------------------------------------------------------ exemplo 3: três declarações de escopo
DCLS = ["bx-s3", "bx-s2", "bx-s1"]
dc = ['      <svg viewBox="0 0 900 222" role="img" aria-label="Três declarações de escopo para a mesma fábrica. ' + " ".join(f"{a}: {b} {c}" for a, b, c in DECLARACOES) + '">']
for k, (tit, txt, leit) in enumerate(DECLARACOES):
    x = 10 + k * 296
    dc.append(f'        <rect class="{DCLS[k]}" x="{x}" y="10" width="284" height="202"/>')
    dc.append(f'        <text class="mono mu" x="{x + 12}" y="30" font-size="10">{escape(tit.upper())}</text>')
    yy = lines(dc, f"“{txt}”", x + 12, 52, 44, fs=11.5, cls="b", step=15, maxl=5)
    lines(dc, leit, x + 12, max(yy + 12, 132), 46, fs=10.5, step=14, maxl=5)
dc.append("      </svg>")

# ------------------------------------------------------------------ módulo 7: os dez compromissos, nos dois exemplos
FC = {DEM: "f1", PARC: "f2", NDEM: "f3"}
X0, CW, TOP, RH = 290, 160, 52, 30
bottom = TOP + RH * len(COMPROMISSOS)
hm = [f'      <svg id="bars" viewBox="0 0 900 {bottom + 20}" role="img" aria-label="Os dez compromissos da direção, na pizzaria e na indústria. '
      + " ".join(f'{t}: pizzaria {a["sit"].lower()}, indústria {b["sit"].lower()}.' for (t, _), a, b in zip(COMPROMISSOS, EX1["lid"], EX2["lid"])) + '">', '        <g font-size="11.5">']
XL = X0 + 2 * (CW + 10) + 20
for k, (t, cls) in enumerate(((DEM, "f1"), (PARC, "f2"), (NDEM, "f3"))):
    hm.append(f'          <rect class="{cls}" x="{XL}" y="{TOP + 4 + k * 24}" width="14" height="14"/><text x="{XL + 22}" y="{TOP + 16 + k * 24}">{t}</text>')
hm.append('        </g>')
for j, nome in enumerate(("Pizzaria", "Indústria")):
    hm.append(f'        <text class="mono mu" x="{X0 + j * (CW + 10) + CW / 2}" y="{TOP - 14}" font-size="10" text-anchor="middle">{nome.upper()}</text>')
for k, ((t, _), a, b) in enumerate(zip(COMPROMISSOS, EX1["lid"], EX2["lid"])):
    y = TOP + RH * k
    hm.append(f'        <text x="20" y="{y + 19}" font-size="12"><tspan class="mono mu">{k + 1}</tspan><tspan dx="8">{escape(t)}</tspan></text>')
    for j, c in enumerate((a, b)):
        x = X0 + j * (CW + 10)
        hm.append(f'        <rect class="bar {FC[c["sit"]]}" data-k="{k}" x="{x}" y="{y + 3}" width="{CW}" height="{RH - 6}"/>')
        hm.append(f'        <text class="b {"on-s2" if c["sit"] == PARC else "on"}" x="{x + CW / 2}" y="{y + 19}" font-size="10.5" text-anchor="middle">{c["sit"]}</text>')
for k, ((t, _), a, b) in enumerate(zip(COMPROMISSOS, EX1["lid"], EX2["lid"])):
    hm.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="{X0 + 2 * CW + 4}" height="{RH}" tabindex="0" role="img" aria-label="{escape(t)}: pizzaria {a["sit"].lower()}, indústria {b["sit"].lower()}" '
              f'data-k="{k}" data-n="{k + 1} · {escape(t)}" data-a="{a["sit"]}" data-b="{b["sit"]}" data-cx="{X0 + CW}" data-cy="{TOP + RH * k}"/>')
hm.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>Compromisso</th><th>Pizzaria</th><th>Indústria</th></tr></thead>', '          <tbody>']
for k, ((t, _), a, b) in enumerate(zip(COMPROMISSOS, EX1["lid"], EX2["lid"]), 1):
    tb.append(f'            <tr><td>{k} · {escape(t)}</td><td>{a["sit"]}</td><td>{b["sit"]}</td></tr>')
tb += ['          </tbody>', '        </table>']
r1, r2 = resumo(EX1), resumo(EX2)
charttext = (f'  <p>As duas direções demonstram a maior parte dos compromissos: {r1["dem"]} na pizzaria e {r2["dem"]} na indústria. As diferenças estão onde o tamanho pesa. '
             'Na pizzaria, tudo passa pelo gerente, e os líderes não decidem nada no seu processo: o compromisso de apoiar os outros gestores não aparece. '
             'Na indústria, os gerentes conduzem os seus processos, mas o turno da noite fica longe da direção, e uma compra aprovada em fevereiro ainda não tinha sido feita em maio. '
             'Em nenhum dos dois casos a direção está ausente. O que falta é chegar a quem está mais longe dela: os líderes da loja, o turno da noite da fábrica.</p>')

# ------------------------------------------------------------------ módulo 10: figura da ISO
ISOP = [("4.3 · Escopo", "Limites e aplicabilidade do sistema, com produtos, serviços e justificativas.", "a aba Escopo e a Aplicabilidade"),
        ("5.1.1 · Liderança", "A direção demonstra liderança e comprometimento com o sistema.", "os dez compromissos"),
        ("5.1.2 · Foco no cliente", "A direção garante que os requisitos do cliente são conhecidos e atendidos.", "o estudo de Satisfação do cliente"),
        ("5.3 · Papéis", "Responsabilidades e autoridades atribuídas, comunicadas e entendidas.", "o estudo da Matriz RACI")]
iso = ['      <svg viewBox="0 0 900 200" role="img" aria-label="O que a norma pede sobre escopo e liderança. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in ISOP) + '">']
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
for tag, val in (("<!--CONTEXTO-->", "\n".join(cx)), ("<!--FLUXO-->", "\n".join(et)), ("<!--FRONTEIRA-->", "\n".join(fr)), ("<!--ARVORE-->", "\n".join(ar)), ("<!--EXCLTAB-->", "\n".join(excltab)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1ESCOPO-->", escopo_tab(EX1)), ("<!--EX1APLIC-->", aplic_tab(EX1)), ("<!--EX1LIDER-->", lider_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2ESCOPO-->", escopo_tab(EX2)), ("<!--EX2APLIC-->", aplic_tab(EX2)), ("<!--EX2LIDER-->", lider_tab(EX2)),
                 ("<!--EX3FIG-->", "\n".join(dc)), ("<!--CHART-->", "\n".join(hm)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHARTTEXT-->", charttext),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Escopo e liderança</title>")
assert "Escopo e liderança" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", r1, "| indústria", r2)
