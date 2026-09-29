# -*- coding: utf-8 -*-
"""Monta treinamento-auditoria.html: CSS herdado do estudo de PDCA + corpo próprio + tabelas e gráfico dos exemplos."""
import os
import re
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aud_data import C, EX1, EX2, FREQ, NC, OM, PROG, RESULT, pontos, prioridade  # noqa: E402

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

css, n = re.subn(r"\n\s*--[pdca]:#\w+; --[pdca]-tint:#\w+;", "", css)
assert n == 12, n
LIGHT = "\n  --c:#1E7B73; --c-tint:#D9EEEB;\n  --n:#B0413E; --n-tint:#F5DEDC;\n  --o:#A96A12; --o-tint:#F6E8CF;"
DARK = "\n  --c:#5FC6BA; --c-tint:#15332F;\n  --n:#EC8E89; --n-tint:#3D1F1E;\n  --o:#E2AC4F; --o-tint:#3A2C12;"
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)

drop = (".tiles .p{", ".k.p{", "svg .bx-p{", "svg .bx-d{", "svg .bx-c{", "svg .bx-a{", "table.pdca",
        "svg .band{", "svg .series{", "svg .pt{", "svg .pt.on-hit{", "svg .goal{", "svg .xh{", "svg .root{",
        "/* Ficha do ciclo")
css = "\n".join(l for l in css.split("\n") if not l.startswith(drop))
for v in ("var(--p)", "var(--d)", "var(--a)"):
    assert v not in css, v

extra = """
/* Tipos de constatação */
.tiles .c{background:var(--c)} .tiles .n{background:var(--n)} .tiles .o{background:var(--o)}
.tiles span{width:auto;min-width:44px;padding:0 9px}
.k.c{background:var(--c)} .k.n{background:var(--n)} .k.o{background:var(--o)}
.k.n,.k.o{width:auto;padding:0 .32em}
svg .bx-c{fill:var(--c-tint);stroke:var(--c);stroke-width:1.5} svg .hd-c{fill:var(--c)}
svg .bx-n{fill:var(--n-tint);stroke:var(--n);stroke-width:1.5} svg .hd-n{fill:var(--n)}
svg .bx-o{fill:var(--o-tint);stroke:var(--o);stroke-width:1.5} svg .hd-o{fill:var(--o)}
svg .hd-ink{fill:var(--ink)}
svg .bx-out2{fill:var(--sunk);stroke:var(--rule);stroke-width:1.5}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}

/* Tabelas dos exemplos */
table.aud{font-size:.82rem;min-width:840px;line-height:1.35}
table.aud th, table.aud td{padding:8px 10px}
table.aud td.n{width:4%;font-weight:600;color:var(--muted)}
table.aud td.r{white-space:nowrap}
table.aud td.r small{color:var(--muted);font:400 .78rem var(--mono);margin-left:6px}
table.aud tr.nc td{background:var(--n-tint)}
table.aud tr.om td{background:var(--o-tint)}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}
table.prog{font-size:.78rem;min-width:850px;line-height:1.3}
table.prog th, table.prog td{padding:7px 8px}
table.prog td.c{text-align:center}
table.prog td.alta{background:var(--n-tint);font-weight:600}
table.prog td.media{background:var(--o-tint)}
table.prog td.baixa{background:var(--c-tint)}

/* Ficha da auditoria (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)

TILE = {C: '<span class="k c">C</span>', NC: '<span class="k n">NC</span>', OM: '<span class="k o">OM</span>'}
ROW = {C: "", NC: ' class="nc"', OM: ' class="om"'}


def lista(ex):
    o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Lista de verificação</caption>',
         '      <thead><tr><th>#</th><th style="width:14%">Requisito</th><th style="width:24%">O que verificar</th>'
         '<th style="width:18%">Amostra</th><th>Evidência encontrada</th><th style="width:11%">Resultado</th></tr></thead>', '      <tbody>']
    for i in ex["lista"]:
        ref = f'<small>nº {i["ref"]}</small>' if i["ref"] else ""
        o.append(f'        <tr{ROW[i["res"]]}><td class="n">{i["n"]}</td><td>{escape(i["req"])}</td><td>{escape(i["verificar"])}</td>'
                 f'<td>{escape(i["amostra"])}</td><td>{escape(i["evid"])}</td><td class="r">{TILE[i["res"]]}{ref}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def const(ex):
    o = ['  <div class="tbl">', '    <table class="aud">', '      <caption>Constatações</caption>',
         '      <thead><tr><th>Nº</th><th style="width:13%">Tipo</th><th style="width:24%">Requisito</th>'
         '<th style="width:24%">Evidência</th><th>Declaração</th><th style="width:13%">Responsável</th></tr></thead>', '      <tbody>']
    for c in ex["const"]:
        tile = TILE[OM] if c["tipo"].startswith("Oportunidade") else TILE[NC]
        o.append(f'        <tr><td class="n">{c["n"]}</td><td>{tile} {escape(c["tipo"].replace("NC ", "").replace("Oportunidade de melhoria", "").capitalize())}</td>'
                 f'<td>{escape(c["req"])}</td><td>{escape(c["evid"])}</td><td>{escape(c["decl"])}</td><td>{escape(c["resp"])}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>',
          f'  <p><strong>Conclusão da auditoria.</strong> {escape(ex["conclusao"])}</p>']
    return "\n".join(o)


def prog():
    o = ['  <div class="tbl">', '    <table class="prog">',
         '      <thead><tr><th style="width:19%">Processo</th><th style="width:14%">Dono</th><th>Importância</th><th>Mudanças</th>'
         '<th>Resultado anterior</th><th>Pontos</th><th>Prioridade</th><th>Frequência</th><th>Mês</th><th style="width:15%">Auditor líder</th></tr></thead>',
         '      <tbody>']
    for p in PROG:
        v = pontos(p)
        pr = prioridade(v)
        cls = {"Alta": "alta", "Média": "media", "Baixa": "baixa"}[pr]
        o.append(f'        <tr><td><strong>{escape(p["proc"])}</strong></td><td>{escape(p["dono"])}</td><td class="c">{p["imp"]}</td><td class="c">{p["mud"]}</td>'
                 f'<td>{p["ant"]}</td><td class="num c">{v}</td><td class="c {cls}">{pr}</td><td>{FREQ[pr]}</td><td>{p["mes"]}</td><td>{escape(p["lider"])}</td></tr>')
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


# ---- gráfico: constatações por processo
X0, U, TOP, RH, BH = 300, 84, 30, 32, 18
bottom = TOP + RH * len(RESULT)
H = bottom + 70
tn, to = sum(r[1] for r in RESULT), sum(r[2] for r in RESULT)
out = [f'      <svg id="bars" viewBox="0 0 900 {H}" role="img" aria-label="Gráfico de barras empilhadas com as constatações do ciclo anual, por processo. '
       f'No total, {tn} não conformidades e {to} oportunidades de melhoria. '
       + "; ".join(f"{p}: {n} não conformidades e {o} oportunidades" for p, n, o in RESULT) + '.">']
for v in range(0, 7):
    x = X0 + v * U
    out.append(f'        <line class="grid" x1="{x}" y1="{TOP - 6}" x2="{x}" y2="{bottom}"/>')
    out.append(f'        <text class="mu" x="{x}" y="{bottom + 16}" font-size="11" text-anchor="middle" style="font-variant-numeric:tabular-nums">{v}</text>')
out.append(f'        <text class="mono mu" x="{X0 + 3 * U}" y="{bottom + 36}" font-size="10" text-anchor="middle">CONSTATAÇÕES NO ANO</text>')
for k, (p, n_, o_) in enumerate(RESULT):
    y = TOP + RH * k + (RH - BH) / 2
    out.append(f'        <text x="20" y="{y + 13:.1f}" font-size="11.5">{escape(p)}</text>')
    x = X0
    partes = [(l, v) for l, v in (("n", n_), ("o", o_)) if v]
    for j, (l, v) in enumerate(partes):
        w = v * U - 2
        if j == len(partes) - 1:
            x1 = x + w
            out.append(f'        <path class="seg hd-{l}" data-k="{k}" d="M{x} {y:.1f} H{x1 - 4} Q{x1} {y:.1f} {x1} {y + 4:.1f} V{y + BH - 4:.1f} '
                       f'Q{x1} {y + BH:.1f} {x1 - 4} {y + BH:.1f} H{x} Z"/>')
        else:
            out.append(f'        <rect class="seg hd-{l}" data-k="{k}" x="{x}" y="{y:.1f}" width="{w}" height="{BH}"/>')
        out.append(f'        <text class="on b" x="{x + w / 2:.1f}" y="{y + 13:.1f}" font-size="11" text-anchor="middle">{"NC" if l == "n" else "OM"} {v}</text>')
        x += v * U
lx, ly = 20, bottom + 60
for l, nome in (("n", "NC · Não conformidade"), ("o", "OM · Oportunidade de melhoria")):
    out.append(f'        <rect class="hd-{l}" x="{lx}" y="{ly - 10}" width="14" height="12"/>')
    out.append(f'        <text x="{lx + 21}" y="{ly}" font-size="11.5">{nome}</text>')
    lx += 220
for k, (p, n_, o_) in enumerate(RESULT):
    out.append(f'        <rect class="hit" x="14" y="{TOP + RH * k}" width="872" height="{RH}" tabindex="0" role="img" '
               f'aria-label="{escape(p)}: {n_} não conformidades e {o_} oportunidades de melhoria" data-k="{k}" data-p="{escape(p)}" '
               f'data-n="{n_}" data-o="{o_}" data-t="{n_ + o_}" data-x="{X0 + (n_ + o_) * U / 2:.1f}"/>')
out.append("      </svg>")
tb = ['        <table>', '          <thead><tr><th>Processo</th><th>Não conformidades</th><th>Oportunidades de melhoria</th><th>Total</th></tr></thead>', '          <tbody>']
for p, n_, o_ in RESULT:
    tb.append(f'            <tr><td>{escape(p)}</td><td class="num">{n_}</td><td class="num">{o_}</td><td class="num">{n_ + o_}</td></tr>')
tb.append(f'            <tr><td><strong>Total</strong></td><td class="num">{tn}</td><td class="num">{to}</td><td class="num">{tn + to}</td></tr>')
tb += ['          </tbody>', '        </table>']

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--RESULT-->", "\n".join(out)), ("<!--RESULTTABLE-->", "\n".join(tb)),
                 ("<!--LV1-->", lista(EX1)), ("<!--CT1-->", const(EX1)), ("<!--LV2-->", lista(EX2)), ("<!--CT2-->", const(EX2)),
                 ("<!--PROG-->", prog())):
    assert tag in body, tag
    body = body.replace(tag, val)

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Auditoria interna na prática</title>")
assert "Auditoria interna" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
for name, ex in (("EX1", EX1), ("EX2", EX2)):
    print(name, {r: sum(1 for i in ex["lista"] if i["res"] == r) for r in (C, NC, OM)}, len(ex["const"]), "constatações")
print("programa:", [(p["proc"].split()[0], pontos(p), prioridade(pontos(p))) for p in PROG], "| NC", tn, "OM", to)
