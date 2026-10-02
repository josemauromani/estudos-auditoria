# -*- coding: utf-8 -*-
"""Monta treinamento-conhecimento.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from con_data import (ABERTO, ATRASADO, CABECA, CHECK, CICLO, CON_SITS, CONSIDERA, CONTROLE, CRITICO, ESCADA, ESCRITO, ETAPAS, EX1, EX2, FORAPRAZO,  # noqa: E402
                      FORMAS, INCORP, NOPRAZO, PEND, PRAZO_LICAO, PTS_FORMA, REPETE, RISCO, SIM, TRANSFERIR, TREINADO, at_conf, at_dias, at_sit, con_conf,
                      con_sit, lic_conf, lic_dias, lic_sit, pol_conf, pontos, prazo_at, pts_pessoas, resumo)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# protegido, em risco e crítico: a mesma paleta de três cores do estudo de Calibração, validada para daltonismo nos dois modos
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
svg .tick{stroke:var(--ink);stroke-width:2.5}
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


def dt(d, ano=True):
    return d.strftime("%d/%m/%Y" if ano else "%d/%m") if d else "—"


def brl(v):
    return "—" if v is None else "R$ " + f"{v:,.0f}".replace(",", ".")


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


def cinco(o, itens, classes, y0=16, h=140, wrap_t=19, wrap_d=25, rotulo=None, maxd=5, mid=None):
    """Cinco caixas em linha, ligadas por setas; devolve as coordenadas x das caixas."""
    xs = []
    for k, it in enumerate(itens):
        x = 12 + k * (W5 + G5)
        xs.append(x)
        ink = classes[k] == "bx-ink"
        o.append(f'        <rect class="{classes[k]}" x="{x}" y="{y0}" width="{W5}" height="{h}"/>')
        if rotulo:
            o.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="{y0 + 20}" font-size="10">{escape(rotulo(k, it))}</text>')
        tit, desc = it[-2], it[-1]
        tl = textwrap.wrap(tit, wrap_t, break_on_hyphens=False)
        yt = y0 + (42 if rotulo else 24)
        for j, l in enumerate(tl):
            o.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{yt + j * 15}" font-size="12.5">{escape(l)}</text>')
        lines(o, desc, x + 12, yt + 15 * len(tl) + 8, wrap_d, cls="t-ground" if ink else "", step=14.5, maxl=maxd)
        if k < len(itens) - 1:
            ym = mid or (y0 + h / 2)
            o.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="{ym}" x2="{x + W5 + G5 - 2}" y2="{ym}" marker-end="url(#{MK})"/>')
    return xs


W5, G5 = 164, 14

# ------------------------------------------------------------------ figura 1: o ciclo do aprendizado
MK = "a1"
ci = ['      <svg viewBox="0 0 900 222" role="img" aria-label="O ciclo do aprendizado. ' + " ".join(f"{a}: {b}" for a, b in CICLO)
      + ' O conhecimento atualizado volta ao processo.">', "        <defs>" + marker("a1") + marker("a1m", True) + "</defs>"]
xs = cinco(ci, CICLO, ["bx", "bx", "bx-c", "bx-d", "bx-p"], h=118, wrap_d=24, maxd=4)
xa, xb = xs[4] + W5 / 2, xs[0] + W5 / 2
ci.append(f'        <path class="ln-mu dash" d="M{xa} 136 V164 H{xb} V140" marker-end="url(#a1m)"/>')
ci.append(f'        <text class="mu halo" x="{(xa + xb) / 2}" y="168" font-size="11" text-anchor="middle">o conhecimento atualizado muda o jeito de fazer</text>')
ci.append('        <text x="450" y="200" font-size="11.5" text-anchor="middle">O pós-entrega é a parte do ciclo que mais ensina, porque mostra o produto no uso real.</text>')
ci.append('        <text class="mu" x="450" y="216" font-size="11" text-anchor="middle">Sem a lição aprendida, a reclamação é resolvida e o processo continua igual.</text>')
ci.append("      </svg>")

# ------------------------------------------------------------------ figura 2: as cinco etapas
MK = "a2"
et = ['      <svg viewBox="0 0 900 236" role="img" aria-label="As cinco etapas do trabalho. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS)
      + ' A lição aprendida volta ao mapa do conhecimento.">', "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
xs = cinco(et, ETAPAS, ["bx", "bx-p", "bx-d", "bx-c", "bx-ink"], h=152, rotulo=lambda k, it: f"ETAPA {k + 1}", mid=84)
xa, xb = xs[4] + W5 / 2, xs[0] + W5 / 2
et.append(f'        <path class="ln-mu dash" d="M{xa} 170 V198 H{xb} V174" marker-end="url(#a2m)"/>')
et.append(f'        <text class="mu halo" x="{(xa + xb) / 2}" y="202" font-size="11" text-anchor="middle">a lição aprendida atualiza o mapa do conhecimento</text>')
et.append('        <text x="450" y="228" font-size="11.5" text-anchor="middle">As duas primeiras etapas olham para dentro; as três últimas, para o que acontece com o cliente.</text>')
et.append("      </svg>")

# ------------------------------------------------------------------ figura 3: a matriz de exposição
GX0, GY0, CW, CH = 250, 64, 200, 74
PESS = [(1, "1 pessoa ou ninguém"), (2, "2 pessoas"), (3, "3 pessoas ou mais")]
mx = ['      <svg viewBox="0 0 900 360" role="img" aria-label="Matriz de exposição do conhecimento. Os pontos somam a forma, de 2 para só na cabeça a 0 para escrito e treinado, '
      'e as pessoas que sabem, de 2 para uma pessoa a 0 para três ou mais. Uma saída prevista soma 1 ponto. '
      + " ".join(f'{k["cod"]}: {pontos(k)} pontos, {con_sit(k).lower()}.' for ex in (EX1, EX2) for k in ex["cons"]) + '">']
for j, f in enumerate(FORMAS):
    x = GX0 + j * CW
    mx.append(f'        <text class="b" x="{x + CW / 2}" y="34" font-size="12" text-anchor="middle">{escape(f)}</text>')
    mx.append(f'        <text class="mono mu" x="{x + CW / 2}" y="50" font-size="9.5" text-anchor="middle">+{PTS_FORMA[f]} PONTO{"S" if PTS_FORMA[f] != 1 else ""}</text>')
for i, (n, rot) in enumerate(PESS):
    y = GY0 + i * CH
    mx.append(f'        <text class="b" x="{GX0 - 14}" y="{y + CH / 2}" font-size="12"{END}>{rot}</text>')
    mx.append(f'        <text class="mono mu" x="{GX0 - 14}" y="{y + CH / 2 + 16}" font-size="9.5"{END}>+{pts_pessoas(n)} PONTO{"S" if pts_pessoas(n) != 1 else ""}</text>')
    for j, f in enumerate(FORMAS):
        x = GX0 + j * CW
        p = PTS_FORMA[f] + pts_pessoas(n)
        cls = "bx-s3" if p >= 3 else "bx-s2" if p == 2 else "bx-s1"
        mx.append(f'        <rect class="{cls}" x="{x + 2}" y="{y + 2}" width="{CW - 4}" height="{CH - 4}"/>')
        mx.append(f'        <text class="disp mu" x="{x + CW - 12}" y="{y + 24}" font-size="16"{END}{TNUM}>{p}</text>')
        dentro = [k for ex in (EX1, EX2) for k in ex["cons"] if k["forma"] == f and min(k["pessoas"], 3) == n]
        for q, k in enumerate(dentro):
            mx.append(f'        <text class="b" x="{x + 12 + (q % 3) * 56}" y="{y + 42 + (q // 3) * 18}" font-size="11.5"{TNUM}>{k["cod"]}{"+1" if k["saida"] == SIM else ""}</text>')
mx.append(f'        <text class="mu" x="{GX0 - 14}" y="34" font-size="10.5"{END}>Pessoas que sabem ↓ · forma →</text>')
yl = GY0 + 3 * CH + 26
for k, (cls, t) in enumerate((("bx-s3", "3 ou mais: crítico (alta) ou em risco (média)"), ("bx-s2", "2: em risco (alta ou média)"), ("bx-s1", "0 ou 1, ou criticidade baixa: sob controle"))):
    mx.append(f'        <rect class="{cls}" x="{20 + k * 290}" y="{yl - 11}" width="14" height="14"/><text x="{40 + k * 290}" y="{yl}" font-size="11">{t}</text>')
mx.append(f'        <text class="mu" x="450" y="{yl + 26}" font-size="11" text-anchor="middle">“+1”: quem sabe tem saída prevista, e o ponto a mais está somado na situação. K são os conhecimentos da pizzaria; C, os da indústria.</text>')
mx.append("      </svg>")

# ------------------------------------------------------------------ figura 4: do tácito ao escrito e treinado
es = ['      <svg viewBox="0 0 900 252" role="img" aria-label="Os três degraus do conhecimento. ' + " ".join(f"{a}: {b} Exemplo: {c}" for a, b, c in ESCADA)
      + ' Para subir do primeiro ao segundo, escrever. Do segundo ao terceiro, acompanhar, gravar e fazer rodízio.">', "        <defs>" + marker("a4") + "</defs>"]
CLS3 = ["bx-s3", "bx-s2", "bx-s1"]
for k, (t, d, e) in enumerate(ESCADA):
    x, y = 12 + k * 296, 120 - k * 46
    h = 100 + k * 46
    es.append(f'        <rect class="{CLS3[k]}" x="{x}" y="{y}" width="284" height="{h}"/>')
    es.append(f'        <text class="b" x="{x + 14}" y="{y + 24}" font-size="13">{escape(t)}</text>')
    yy = lines(es, d, x + 14, y + 44, 44, fs=11, step=14.5, maxl=2)
    lines(es, "Ex.: " + e, x + 14, yy + 4, 46, fs=10.5, cls="mu", step=14, maxl=2)
for k, t in enumerate(("escrever", "acompanhar, gravar, rodízio")):
    x = 12 + (k + 1) * 296 - 6
    es.append(f'        <text class="mu halo" x="{x - 2}" y="{100 - k * 46}" font-size="11"{END}>{t} →</text>')
es.append('        <text x="450" y="244" font-size="11.5" text-anchor="middle">Escrito não basta: o conhecimento só está protegido quando outra pessoa já fez sozinha.</text>')
es.append("      </svg>")

# ------------------------------------------------------------------ figura 5: o que considerar no pós-entrega
po = ['      <svg viewBox="0 0 900 280" role="img" aria-label="O que considerar ao definir o pós-entrega. ' + " ".join(f"{a}: {b}" for a, b in CONSIDERA)
      + ' As cinco considerações definem a política de pós-entrega de cada produto: o que se faz, o prazo para reclamar e o prazo de resposta.">',
      "        <defs>" + marker("a5") + "</defs>"]
for k, (t, d) in enumerate(CONSIDERA):
    y = 12 + k * 48
    po.append(f'        <rect class="bx" x="12" y="{y}" width="520" height="42"/>')
    po.append(f'        <text class="b" x="26" y="{y + 26}" font-size="12">{escape(t)}</text>')
    po.append(f'        <text class="mu" x="210" y="{y + 26}" font-size="10.5">{escape(d)}</text>')
    po.append(f'        <path class="ln-mu" d="M533 {y + 21} H560 V130"/>')
po.append('        <line class="ln" x1="560" y1="130" x2="586" y2="130" marker-end="url(#a5)"/>')
po.append('        <rect class="bx-ink" x="590" y="40" width="298" height="180"/>')
po.append('        <text class="b t-ground" x="606" y="68" font-size="13">Política de pós-entrega</text>')
yy = 96
for t in ("O que se faz depois da entrega", "O prazo para o cliente reclamar", "O prazo para responder", "O que se quer evitar no uso"):
    po.append(f'        <rect class="f2" x="606" y="{yy - 9}" width="8" height="8"/><text class="t-ground" x="622" y="{yy}" font-size="11.5">{t}</text>')
    yy += 26
po.append('        <text x="450" y="272" font-size="11.5" text-anchor="middle">Uma política por produto ou serviço. O prazo aceito nunca é menor que o da lei ou o do contrato.</text>')
po.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Responsável</dt><dd>{escape(h["resp"])}</dd></div>',
                      f'    <div><dt>Leitura</dt><dd>{dt(h["ref"])}.</dd></div>',
                      f'    <div><dt>Mudança prevista</dt><dd>{escape(h["mudanca"])}</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      '  </dl>'])


def tabela(caption, heads, rows):
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{caption}</caption>', f'      <thead><tr>{"".join(heads)}</tr></thead>', '      <tbody>']
    o += [f'        <tr>{r}</tr>' for r in rows]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def chip(c, ok=("OK",)):
    return f'<span class="chip {"s1" if c in ok else "s3"}">{escape(c)}</span>'


CON_CLS = {CRITICO: "s3", RISCO: "s2", CONTROLE: "s1"}
AT_CLS = {NOPRAZO: "s1", FORAPRAZO: "s3", ABERTO: "s2", ATRASADO: "s3"}


def con_tab(ex):
    ref, r = ex["head"]["ref"], resumo(ex)
    rows = []
    for k in ex["cons"]:
        s = con_sit(k)
        acao = f'{escape(k["acao"])}<small>prazo: {dt(k["prazo"])}</small>' if k["acao"] else "—"
        rows.append(f'<td class="n">{k["cod"]}</td><td><strong>{escape(k["nome"])}</strong><small>{escape(k["proc"])} · criticidade {k["crit"].lower()}</small></td>'
                    f'<td>{k["forma"]}<small>{escape(k["onde"]) or "sem documento"}</small></td><td class="c{" no" if k["pessoas"] <= 1 else ""}">{k["pessoas"]}</td>'
                    f'<td class="c">{k["saida"]}</td><td class="c"><strong>{pontos(k)}</strong></td><td><span class="chip {CON_CLS[s]}">{s}</span></td>'
                    f'<td>{acao}</td><td>{chip(con_conf(k, ref))}</td>')
    sits = r["sits"]
    return tabela(f'Mapa do conhecimento · {r["cons"]} conhecimentos: {sits[CRITICO]} crítico{"s" if sits[CRITICO] != 1 else ""}, {sits[RISCO]} em risco, {sits[CONTROLE]} sob controle',
                  ['<th>Código</th>', '<th style="width:24%">Conhecimento<small>Processo · criticidade</small></th>', '<th style="width:16%">Forma<small>Onde está</small></th>',
                   '<th class="c">Quem sabe</th>', '<th class="c">Saída prevista</th>', '<th class="c">Pontos</th>', '<th>Situação</th>',
                   '<th style="width:24%">Ação de transferência</th>', '<th>Conferência</th>'], rows)


def lic_tab(ex):
    ref, r = ex["head"]["ref"], resumo(ex)
    rows = []
    for l in ex["lics"]:
        s = lic_sit(l)
        sit = f'<span class="chip s1">{s}</span><small>em {dt(l["incorp"], False)}</small>' if s == INCORP else f'<span class="chip s2">{s}</span><small>há {lic_dias(l, ref)} dias</small>'
        rows.append(f'<td class="n">{l["num"]}</td><td class="c">{dt(l["data"], False)}</td><td>{l["origem"]}</td><td>{escape(l["oque"])}</td>'
                    f'<td>{escape(l["aprend"]) or "—"}</td><td>{escape(l["onde"]) or "—"}<small>{escape(l["resp"]) or "sem responsável"}{" · " + l["cod"] if l["cod"] else ""}</small></td>'
                    f'<td>{sit}</td><td>{chip(lic_conf(l, ex["cons"], ref))}</td>')
    return tabela(f'Lições aprendidas · {r["lics"]} registradas, {r["pend"]} pendentes, {r["velhas"]} há mais de {PRAZO_LICAO} dias',
                  ['<th>Nº</th>', '<th class="c">Data</th>', '<th>Origem</th>', '<th style="width:20%">O que aconteceu</th>', '<th style="width:22%">O que aprendemos</th>',
                   '<th style="width:16%">Onde incorporar<small>Responsável · conhecimento</small></th>', '<th>Situação</th>', '<th>Conferência</th>'], rows)


def pol_tab(ex):
    rows = []
    for p in ex["pols"]:
        menor = p["aceito"] is not None and p["minimo"] is not None and p["aceito"] < p["minimo"]
        rows.append(f'<td><strong>{escape(p["prod"])}</strong><small>{escape(p["vida"])}</small></td><td class="c">{p["minimo"]} dias</td>'
                    f'<td class="c{" no" if menor else ""}">{p["aceito"]} dia{"s" if p["aceito"] != 1 else ""}</td><td>{escape(p["ativ"])}</td>'
                    f'<td class="c">{p["resp"]} dia{"s" if p["resp"] != 1 else ""}</td><td>{escape(p["conseq"]) or "—"}</td><td>{chip(pol_conf(p))}</td>')
    return tabela(f'Política de pós-entrega · {len(ex["pols"])} produtos',
                  ['<th style="width:18%">Produto<small>Vida útil</small></th>', '<th class="c">Mínimo para reclamar<small>Lei ou contrato</small></th>',
                   '<th class="c">Prazo aceito</th>', '<th style="width:26%">O que se faz</th>', '<th class="c">Prazo de resposta</th>',
                   '<th style="width:18%">O que se quer evitar</th>', '<th>Conferência</th>'], rows)


def at_tab(ex):
    ref, r = ex["head"]["ref"], resumo(ex)
    rows = []
    for a in ex["ats"]:
        s = at_sit(a, ex["pols"], ref)
        resol = dt(a["resol"], False) if a["resol"] else "aberto"
        rows.append(f'<td class="n">{a["num"]}</td><td class="c">{dt(a["abert"], False)}</td><td><strong>{escape(a["relato"])}</strong><small>{escape(a["cliente"])} · {escape(a["prod"])}</small></td>'
                    f'<td>{a["tipo"]}</td><td class="c">{resol}<small>{at_dias(a, ref)} de {prazo_at(a, ex["pols"])} dias</small></td><td><span class="chip {AT_CLS[s]}">{s}</span></td>'
                    f'<td>{escape(a["causa"]) or "—"}{"<small>Lição " + a["licao"] + "</small>" if a["licao"] else ""}</td><td class="c">{brl(a["custo"])}</td>'
                    f'<td>{chip(at_conf(a, ex["pols"], ex["lics"]))}</td>')
    pz = "—" if r["noprazo"] is None else f'{r["noprazo"] * 100:.0f} %'
    return tabela(f'Atendimentos depois da entrega · {r["ats"]} no período, {r["abertos"]} abertos, {pz} dos resolvidos no prazo, custo de {brl(r["custo"])}',
                  ['<th>Nº</th>', '<th class="c">Abertura</th>', '<th style="width:24%">Relato<small>Cliente · produto</small></th>', '<th>Tipo</th>',
                   '<th class="c">Resolução<small>Dias de prazo</small></th>', '<th>Situação</th>', '<th style="width:22%">Causa<small>Lição</small></th>', '<th class="c">Custo</th>',
                   '<th>Conferência</th>'], rows)


# ------------------------------------------------------------------ exemplo 3: a mesma reclamação, duas vezes
MK = "a6"
im = ['      <svg viewBox="0 0 900 222" role="img" aria-label="A mesma reclamação, duas vezes. ' + " ".join(f"{a}, {b}: {c}" for a, b, c in REPETE) + '">',
      "        <defs>" + marker("a6") + "</defs>"]
cinco(im, [(b, c) for a, b, c in REPETE], ["bx-s2", "bx", "bx-s2", "bx-s3", "bx-ink"], y0=14, h=168, rotulo=lambda k, it: REPETE[k][0].upper(), maxd=6, mid=96)
im.append('        <text x="450" y="210" font-size="11.5" text-anchor="middle">A lição estava escrita desde março. Faltou o destino com dono: a etiqueta continuou a mesma.</text>')
im.append("      </svg>")

# ------------------------------------------------------------------ módulo 8: dias para resolver, nos dois exemplos
DMAX = 10
X0, X1, TOP, RH = 330, 860, 46, 26
dx = lambda d: X0 + min(d, DMAX) * (X1 - X0) / DMAX  # noqa: E731
rows_c = []
for nome, ex in (("PIZZARIA", EX1), ("INDÚSTRIA", EX2)):
    rows_c.append(("grupo", nome, ex))
    rows_c += [("at", a, ex) for a in ex["ats"]]
bottom = TOP + RH * len(rows_c)
COR = {NOPRAZO: "f1", FORAPRAZO: "f3", ABERTO: "f2", ATRASADO: "f3"}
ch = [f'      <svg id="bars" viewBox="0 0 900 {bottom + 44}" role="img" aria-label="Dias para resolver cada atendimento, contra o prazo de resposta do produto. '
      + " ".join(f'{r[1]["num"]}: {at_dias(r[1], r[2]["head"]["ref"])} dias, prazo de {prazo_at(r[1], r[2]["pols"])}, {at_sit(r[1], r[2]["pols"], r[2]["head"]["ref"]).lower()}.'
                 for r in rows_c if r[0] == "at") + '">', '        <g font-size="11.5">']
for k, (t, cls) in enumerate(((NOPRAZO, "f1"), ("Aberto, ainda no prazo", "f2"), ("Fora do prazo", "f3"))):
    ch.append(f'          <rect class="{cls}" x="{X0 + k * 150}" y="12" width="14" height="14"/><text x="{X0 + 22 + k * 150}" y="24">{t}</text>')
ch.append(f'          <line class="tick" x1="{X0 + 460}" y1="11" x2="{X0 + 460}" y2="27"/><text x="{X0 + 470}" y="24">Prazo</text>')
ch.append('        </g>')
for d in range(0, DMAX + 1, 2):
    ch.append(f'        <line class="{"ln" if d == 0 else "grid"}" x1="{dx(d):.1f}" y1="{TOP - 6}" x2="{dx(d):.1f}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{dx(d):.1f}" y="{bottom + 16}" font-size="11" text-anchor="middle"{TNUM}>{d}</text>')
ch.append(f'        <text class="mono mu" x="{(X0 + X1) / 2}" y="{bottom + 36}" font-size="10" text-anchor="middle">DIAS DA ABERTURA À RESOLUÇÃO, OU ATÉ A LEITURA SE ABERTO</text>')
hits = []
for k, row in enumerate(rows_c):
    y = TOP + RH * k
    if row[0] == "grupo":
        ch.append(f'        <text class="mono mu" x="20" y="{y + 17}" font-size="10">{row[1]}</text>')
        continue
    a, ex = row[1], row[2]
    ref = ex["head"]["ref"]
    d, pz, s = at_dias(a, ref), prazo_at(a, ex["pols"]), at_sit(a, ex["pols"], ref)
    ch.append(f'        <text x="36" y="{y + 17}" font-size="11.5"><tspan class="b">{a["num"]}</tspan><tspan class="mu" dx="8">{escape(textwrap.shorten(a["relato"], 34, placeholder="…"))}</tspan></text>')
    ch.append(f'        <rect class="bar {COR[s]}" data-k="{k}" x="{X0}" y="{y + 6}" width="{max(dx(d) - X0, 3):.1f}" height="{RH - 12}"/>')
    ch.append(f'        <line class="tick" x1="{dx(pz):.1f}" y1="{y + 2}" x2="{dx(pz):.1f}" y2="{y + RH - 2}"/>')
    ch.append(f'        <text class="mu halo" x="{max(dx(d), dx(pz)) + 8:.1f}" y="{y + 17}" font-size="10.5"{TNUM}>{d} d</text>')
    hits.append(f'        <rect class="hit" x="14" y="{y}" width="872" height="{RH}" tabindex="0" role="img" aria-label="{a["num"]}, {escape(a["relato"])}: {d} dias, prazo de {pz}, {s.lower()}" '
                f'data-k="{k}" data-n="{a["num"]} · {escape(a["relato"])}" data-s="{s}" data-d="{d} de {pz} dias" data-p="{escape(a["tipo"])}" data-cx="{dx(d):.1f}" data-cy="{y}"/>')
ch += hits + ["      </svg>"]
tb = ['        <table class="aud">', '          <thead><tr><th>Nº</th><th>Relato</th><th>Tipo</th><th class="c">Dias</th><th class="c">Prazo</th><th>Situação</th></tr></thead>', '          <tbody>']
for row in rows_c:
    if row[0] == "at":
        a, ex = row[1], row[2]
        ref = ex["head"]["ref"]
        tb.append(f'            <tr><td>{a["num"]}</td><td>{escape(a["relato"])}</td><td>{a["tipo"]}</td><td class="c">{at_dias(a, ref)}</td>'
                  f'<td class="c">{prazo_at(a, ex["pols"])}</td><td>{at_sit(a, ex["pols"], ref)}</td></tr>')
tb += ['          </tbody>', '        </table>']

# ------------------------------------------------------------------ módulo 11: figura da ISO
ISOP = [("7.1.6 · Determinar", "Determinar o conhecimento necessário para operar os processos e obter produtos conformes.", "o mapa do conhecimento"),
        ("7.1.6 · Manter", "Manter esse conhecimento e torná-lo disponível na medida necessária.", "a forma e quem sabe"),
        ("7.1.6 · Obter o que falta", "Diante de mudanças, considerar o que se sabe e como obter o conhecimento adicional.", "a ação de transferência"),
        ("8.5.5 · Pós-entrega", "Atender às atividades pós-entrega, definidas pela lei, pelos riscos, pela vida útil, pelo cliente e pelo retorno.", "a política e os atendimentos")]
iso = ['      <svg viewBox="0 0 900 200" role="img" aria-label="O que a norma pede sobre conhecimento organizacional e pós-entrega. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in ISOP) + '">']
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
for tag, val in (("<!--CICLO-->", "\n".join(ci)), ("<!--FLUXO-->", "\n".join(et)), ("<!--MATRIZ-->", "\n".join(mx)), ("<!--ESCADA-->", "\n".join(es)),
                 ("<!--POS-->", "\n".join(po)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1CON-->", con_tab(EX1)), ("<!--EX1LIC-->", lic_tab(EX1)), ("<!--EX1POL-->", pol_tab(EX1)), ("<!--EX1AT-->", at_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2CON-->", con_tab(EX2)), ("<!--EX2LIC-->", lic_tab(EX2)), ("<!--EX2POL-->", pol_tab(EX2)), ("<!--EX2AT-->", at_tab(EX2)),
                 ("<!--EX3FIG-->", "\n".join(im)), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Conhecimento e pós-entrega</title>")
assert "Conhecimento" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", resumo(EX1), "| indústria", resumo(EX2))
