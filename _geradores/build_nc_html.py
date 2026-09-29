# -*- coding: utf-8 -*-
"""Monta treinamento-nao-conformidade.html: CSS herdado do estudo de PDCA + corpo próprio + tabelas e gráficos dos exemplos."""
import os
import re
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nc_data import AC, ANTES, CHECK, COR, DEPOIS, EX1, EX2, LINHA, dentro, media  # noqa: E402

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

css, n = re.subn(r"\n\s*--[pdca]:#\w+; --[pdca]-tint:#\w+;", "", css)
assert n == 12, n
LIGHT = ("\n  --c:#1E7B73; --c-tint:#D9EEEB;\n  --n:#B0413E; --n-tint:#F5DEDC;\n  --o:#A96A12; --o-tint:#F6E8CF;"
         "\n  --s:#5B6B76; --s-tint:#E3E8EB;")
DARK = ("\n  --c:#5FC6BA; --c-tint:#15332F;\n  --n:#EC8E89; --n-tint:#3D1F1E;\n  --o:#E2AC4F; --o-tint:#3A2C12;"
        "\n  --s:#9BABB6; --s-tint:#25323A;")
assert css.count("--accent:#2B5C8A;") == 1 and css.count("--accent:#86B7E3;") == 2
css = css.replace("--accent:#2B5C8A;", "--accent:#2B5C8A;" + LIGHT).replace("--accent:#86B7E3;", "--accent:#86B7E3;" + DARK)

drop = (".tiles .p{", ".k.p{", "svg .bx-p{", "svg .bx-d{", "svg .bx-c{", "svg .bx-a{", "table.pdca", "svg .root{", "/* Ficha do ciclo")
css = "\n".join(l for l in css.split("\n") if not l.startswith(drop))
for v in ("var(--p)", "var(--d)", "var(--a)"):
    assert v not in css, v

extra = """
/* Não conformidade, correção e ação corretiva */
.tiles .c{background:var(--c)} .tiles .n{background:var(--n)} .tiles .o{background:var(--o)}
.tiles span{width:auto;min-width:44px;padding:0 9px}
.chip{display:inline-block;padding:2px 8px;font:600 .76rem/1.45 var(--body);color:var(--on-hue);white-space:nowrap}
.chip.c{background:var(--c)} .chip.n{background:var(--n)} .chip.o{background:var(--o)} .chip.s{background:var(--s)}
svg .bx-c{fill:var(--c-tint);stroke:var(--c);stroke-width:1.5} svg .hd-c{fill:var(--c)}
svg .bx-n{fill:var(--n-tint);stroke:var(--n);stroke-width:1.5} svg .hd-n{fill:var(--n)}
svg .bx-o{fill:var(--o-tint);stroke:var(--o);stroke-width:1.5} svg .hd-o{fill:var(--o)}
svg .hd-ink{fill:var(--ink)}
svg .bx-out2{fill:var(--sunk);stroke:var(--rule);stroke-width:1.5}
svg .hit:focus-visible{stroke:var(--accent);stroke-width:2}
.quiz .opts{flex-wrap:wrap}
.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}

/* Tabelas dos exemplos */
table.aud{font-size:.82rem;min-width:840px;line-height:1.4}
table.aud th, table.aud td{padding:8px 10px}
table.aud td.n{width:4%;font-weight:600;color:var(--muted)}
table.aud td.lb{width:17%;font-weight:600}
table.aud td.dt{white-space:nowrap;font:400 .78rem var(--mono)}
table.aud tr.om td{background:var(--o-tint)}
table.aud tr.rz td{background:var(--c-tint)}
table.aud td.good{background:var(--good-tint);font-weight:600}
table.aud td.bad{background:var(--bad-tint);font-weight:600}
table.aud td ol{margin:0;padding-left:1.2em;display:block}
table.aud td ol li + li{margin-top:4px}
table.aud td small{color:var(--muted);font-size:.78rem}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha da não conformidade (acima de cada exemplo) */"""
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)


def dt(d):
    return d.strftime("%d/%m/%Y")


def br(v, casas=1):
    s = f"{v:.{casas}f}".replace(".", ",")
    return s[:-2] if s.endswith(",0") else s


def exemplo(ex):
    h, d, e, f = ex["head"], ex["desc"], ex["eficacia"], ex["encerr"]
    cor = [a for a in ex["acoes"] if a["tipo"] == COR]
    o = ['  <dl class="ficha">',
         f'    <div><dt>Registro</dt><dd>RNC {h["num"]}, aberto em {dt(h["aberta"])}</dd></div>',
         f'    <div><dt>Origem</dt><dd>{escape(h["ref"])}</dd></div>',
         f'    <div><dt>Processo</dt><dd>{escape(h["processo"])}</dd></div>',
         f'    <div><dt>Responsável</dt><dd>{escape(h["resp"])}</dd></div>',
         '  </dl>',
         '  <div class="tbl">', '    <table class="aud">', '      <caption>Etapas 1 a 3 · Registro, correção e abrangência</caption>', '      <tbody>',
         f'        <tr><td class="lb">Requisito</td><td>{escape(d["req"])}</td></tr>',
         f'        <tr><td class="lb">Evidência</td><td>{escape(d["evid"])}</td></tr>',
         f'        <tr><td class="lb">Declaração</td><td>{escape(d["decl"])}</td></tr>',
         '        <tr class="om"><td class="lb"><span class="chip o">Correção</span></td><td><ol>'
         + "".join(f'<li>{escape(a["oque"])} <small>{escape(a["resp"])}, {dt(a["feito"])}. {escape(a["evid"])}</small></li>' for a in cor)
         + '</ol></td></tr>',
         f'        <tr><td class="lb">Abrangência</td><td>{escape(ex["abrang"]["texto"])}</td></tr>',
         f'        <tr><td class="lb">Consequências</td><td>{escape(ex["abrang"]["conseq"])}</td></tr>',
         f'        <tr><td class="lb">Decisão</td><td>Ação corretiva necessária. {escape(ex["decisao"]["just"])}</td></tr>',
         '      </tbody>', '    </table>', '  </div>',
         '  <div class="tbl">', '    <table class="aud">', '      <caption>Etapa 4 · Análise da causa</caption>',
         '      <thead><tr><th>#</th><th style="width:28%">Pergunta</th><th style="width:34%">Resposta</th><th>Como foi confirmada</th></tr></thead>', '      <tbody>']
    for p in ex["porques"]:
        o.append(f'        <tr><td class="n">{p["n"]}</td><td>{escape(p["perg"])}</td><td>{escape(p["resp"])}</td><td>{escape(p["conf"])}</td></tr>')
    o += [f'        <tr class="rz"><td></td><td><strong>Causa raiz</strong></td><td colspan="2">{escape(ex["raiz"])}</td></tr>',
          '      </tbody>', '    </table>', '  </div>',
          '  <div class="tbl">', '    <table class="aud">', '      <caption>Etapa 5 · Ações corretivas</caption>',
          '      <thead><tr><th>#</th><th style="width:33%">O que foi feito</th><th style="width:22%">Causa tratada</th><th style="width:14%">Responsável</th>'
          '<th>Prazo</th><th style="width:20%">Evidência de implantação</th></tr></thead>', '      <tbody>']
    for k, a in enumerate([a for a in ex["acoes"] if a["tipo"] == AC], 1):
        o.append(f'        <tr><td class="n">{k}</td><td>{escape(a["oque"])}</td><td>{escape(a["causa"])}</td><td>{escape(a["resp"])}</td>'
                 f'<td class="dt">{dt(a["prazo"])}</td><td>{escape(a["evid"])}</td></tr>')
    grupos = " · ".join(f'<strong>{m}:</strong> ' + ", ".join(f"{v}%" for _, mm, v in e["medicoes"] if mm == m)
                        for m in ("Antes", "Durante", "Depois"))
    o += ['      </tbody>', '    </table>', '  </div>',
          '  <div class="tbl">', '    <table class="aud">', '      <caption>Etapas 6 e 7 · Eficácia e encerramento</caption>', '      <tbody>',
          f'        <tr><td class="lb">Indicador</td><td>{escape(e["indicador"])}, em percentual. {escape(e["metodo"])}</td></tr>',
          f'        <tr><td class="lb">Meta e critério</td><td>Até {e["meta"]}%, por {e["criterio"]} {e["periodo"]} seguidos. Verificação por: {escape(e["quem"])}.</td></tr>',
          f'        <tr><td class="lb">Medições</td><td>{grupos}<br><small>Média antes: {br(media(ex, ANTES))}%. Média depois: {br(media(ex, DEPOIS))}%. '
          f'{escape(e["obs"])}</small></td></tr>',
          f'        <tr><td class="lb">Conclusão</td><td class="good">{escape(e["conclusao"])}. Verificação em {dt(e["data"])}, sem reincidência.</td></tr>',
          f'        <tr><td class="lb">Mudanças no sistema</td><td>{escape(f["mudanca"])}</td></tr>',
          f'        <tr><td class="lb">Riscos</td><td>{escape(f["riscos"])}</td></tr>',
          f'        <tr><td class="lb">Encerramento</td><td>Encerrado em {dt(f["data"])}, com aprovação de: {escape(f["aprov"])}.</td></tr>',
          '      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


# ---- figura 4: linha do tempo do exemplo 2, em escala
T0, TN = LINHA[0][1], LINHA[-1][2]
TOTAL = (TN - T0).days
PX = 790 / TOTAL
X = lambda d: 55 + (d - T0).days * PX  # noqa: E731
CLS = ["hd-o gap2", "hd-c gap2", "hd-c gap2", "bx-out2", "hd-ink gap2"]
ln = [f'      <svg viewBox="0 0 900 150" role="img" aria-label="Linha do tempo do tratamento do exemplo 2, de {dt(T0)} a {dt(TN)}, com {TOTAL} dias: '
      + "; ".join(f"{n.lower()}, {(b - a).days} dias" for n, a, b in LINHA) + '.">']
for (nome, a, b), cls in zip(LINHA, CLS):
    ln.append(f'        <rect class="{cls}" x="{X(a):.1f}" y="56" width="{X(b) - X(a):.1f}" height="44"/>')
dias = [(b - a).days for _, a, b in LINHA]
xm = [(X(a) + X(b)) / 2 for _, a, b in LINHA]
ln += [
    f'        <line class="ln-mu" x1="{xm[0]:.1f}" y1="30" x2="{xm[0]:.1f}" y2="54" stroke-width="1"/>',
    f'        <text x="{X(T0):.1f}" y="22" font-size="11.5"><tspan class="b">Correção</tspan> · {dias[0]} dias</text>',
    f'        <line class="ln-mu" x1="{xm[1]:.1f}" y1="44" x2="{xm[1]:.1f}" y2="54" stroke-width="1"/>',
    f'        <text x="{xm[1] - 6:.1f}" y="40" font-size="11.5"><tspan class="b">Análise da causa</tspan> · {dias[1]} dias</text>',
    f'        <text class="on b" x="{xm[2]:.1f}" y="76" font-size="11.5" text-anchor="middle">Ações</text>',
    f'        <text class="on" x="{xm[2]:.1f}" y="91" font-size="11" text-anchor="middle">{dias[2]} dias</text>',
    f'        <text class="b" x="{xm[3]:.1f}" y="76" font-size="11.5" text-anchor="middle">Observação do indicador</text>',
    f'        <text class="mu" x="{xm[3]:.1f}" y="91" font-size="11" text-anchor="middle">{dias[3]} dias</text>',
    f'        <line class="ln-mu" x1="{xm[4]:.1f}" y1="44" x2="{xm[4]:.1f}" y2="54" stroke-width="1"/>',
    f'        <text x="{X(TN):.1f}" y="40" font-size="11.5" text-anchor="end"><tspan class="b">Verificação da eficácia</tspan> · {dias[4]} dias</text>',
]
from datetime import date  # noqa: E402

marcos = [(T0, T0.strftime("%d/%m")), (date(2026, 11, 1), "1º nov"), (date(2026, 12, 1), "1º dez"), (date(2027, 1, 1), "1º jan"),
          (TN, TN.strftime("%d/%m"))]
ln.append('        <g class="ln-mu" stroke-width="1">' + "".join(f'<line x1="{X(d):.1f}" y1="102" x2="{X(d):.1f}" y2="112"/>' for d, _ in marcos) + "</g>")
ln.append('        <g class="mono" font-size="10.5" text-anchor="middle">' + "".join(f'<text class="mu" x="{X(d):.1f}" y="130">{t}</text>' for d, t in marcos) + "</g>")
ln.append("      </svg>")

# ---- figura 5: gráfico do indicador do exemplo 2
E = EX2["eficacia"]
M = E["medicoes"]
X0, DX, YB, YT, VMAX = 100, 80, 270, 40, 40
cx = lambda i: X0 + i * DX  # noqa: E731
cy = lambda v: YB - v * (YB - YT) / VMAX  # noqa: E731
ia = [i for i, m in enumerate(M) if m[1] == ANTES]
idur = [i for i, m in enumerate(M) if m[1] not in (ANTES, DEPOIS)]
idp = [i for i, m in enumerate(M) if m[1] == DEPOIS]
ma, md = media(EX2, ANTES), media(EX2, DEPOIS)
rot = lambda p: p.split("/")[0]  # noqa: E731
ch = [f'      <svg id="run" viewBox="0 0 900 340" role="img" aria-label="Gráfico de linha com o percentual de requisições com especificação ausente ou insuficiente, '
      f'de {M[0][0]} a {M[-1][0]}. Antes das ações, o indicador fica entre {min(M[i][2] for i in ia)}% e {max(M[i][2] for i in ia)}%, com média de {br(ma)}%. '
      f'No mês das ações, cai para {M[idur[0]][2]}%. Nos três meses seguintes, fica em ' + ", ".join(f"{M[i][2]}%" for i in idp)
      + f', dentro da meta de até {E["meta"]}%.">',
      f'        <rect class="band" x="{cx(idur[0]) - DX / 2}" y="{YT}" width="{DX * len(idur)}" height="{YB - YT}"/>',
      f'        <text class="mu" x="{(cx(ia[0]) + cx(ia[-1])) / 2}" y="28" font-size="11.5" text-anchor="middle">antes · média de {br(ma)}%</text>',
      f'        <text class="mu" x="{cx(idur[0])}" y="28" font-size="11.5" text-anchor="middle">ações</text>',
      f'        <text class="mu" x="{(cx(idp[0]) + cx(idp[-1])) / 2}" y="28" font-size="11.5" text-anchor="middle">depois · média de {br(md)}%</text>']
for v in range(0, VMAX + 1, 10):
    ch.append(f'        <line class="grid" x1="70" y1="{cy(v):.1f}" x2="860" y2="{cy(v):.1f}"/>')
    ch.append(f'        <text class="mu" x="62" y="{cy(v) + 4:.1f}" font-size="11" text-anchor="end" style="font-variant-numeric:tabular-nums">{v}%</text>')
ch.append('        <g font-size="11" text-anchor="middle">' + "".join(f'<text class="mu" x="{cx(i)}" y="290">{rot(p)}</text>' for i, (p, _, _) in enumerate(M)) + "</g>")
ch += [f'        <line class="goal" x1="70" y1="{cy(E["meta"]):.1f}" x2="860" y2="{cy(E["meta"]):.1f}"/>',
       f'        <text x="74" y="{cy(E["meta"]) - 8:.1f}" font-size="11.5"><tspan class="b">meta</tspan> até {E["meta"]}%</text>',
       f'        <line class="xh" id="run-xh" x1="0" y1="{YT}" x2="0" y2="{YB}" visibility="hidden"/>',
       '        <polyline class="series" points="' + " ".join(f"{cx(i)},{cy(v):.1f}" for i, (_, _, v) in enumerate(M)) + '"/>',
       '        <g id="run-pts">' + "".join(f'<circle class="pt" cx="{cx(i)}" cy="{cy(v):.1f}" r="5"/>' for i, (_, _, v) in enumerate(M)) + "</g>"]
imax = max(ia, key=lambda i: M[i][2])
ch += [f'        <text class="b" x="{cx(imax)}" y="{cy(M[imax][2]) - 12:.1f}" font-size="12" text-anchor="middle">{M[imax][2]}%</text>',
       f'        <text class="b" x="{cx(idur[0]) + 12}" y="{cy(M[idur[0]][2]) - 6:.1f}" font-size="12">{M[idur[0]][2]}%</text>',
       f'        <text class="b" x="{cx(idp[-1]) + 12}" y="{cy(M[idp[-1]][2]) + 4:.1f}" font-size="12">{M[idp[-1]][2]}%</text>',
       '        <line class="series" x1="70" y1="322" x2="98" y2="322"/><circle class="pt" cx="84" cy="322" r="4"/>',
       '        <text x="106" y="326" font-size="11.5">requisições com especificação ausente ou insuficiente</text>',
       '        <line class="goal" x1="470" y1="322" x2="498" y2="322"/>',
       '        <text x="506" y="326" font-size="11.5">meta</text>']
NOME = {ANTES: "antes das ações", DEPOIS: "depois das ações"}
for i, (p, m, v) in enumerate(M):
    momento = NOME.get(m, "durante as ações")
    sit = "atingida" if dentro(v, E["meta"], E["sentido"]) else "não atingida"
    ch.append(f'        <rect class="hit" x="{cx(i) - DX / 2}" y="{YT}" width="{DX}" height="{YB - YT}" tabindex="0" role="img" '
              f'aria-label="{p}, {momento}: {v}%" data-i="{i}" data-v="{v}" data-p="{p}" data-m="{momento}" data-g="{E["meta"]}" data-s="{sit}"/>')
ch.append("      </svg>")
tb = ['        <table>', '          <thead><tr><th>Mês</th><th>Momento</th><th>Requisições com falha de especificação</th>'
      f'<th>Dentro da meta de até {E["meta"]}%?</th></tr></thead>', '          <tbody>']
for p, m, v in M:
    tb.append(f'            <tr><td>{p}</td><td>{m}</td><td class="num">{v}%</td><td>{"Sim" if dentro(v, E["meta"], E["sentido"]) else "Não"}</td></tr>')
tb += ['          </tbody>', '        </table>']

check = "\n".join(f'    <li><label><input type="checkbox" id="ck-{k}"><span>{escape(t)}</span></label></li>' for k, t in enumerate(CHECK, 1))

body = open(BODY, encoding="utf-8").read()
for tag, val in (("<!--EX1-->", exemplo(EX1)), ("<!--EX2-->", exemplo(EX2)), ("<!--LINHA-->", "\n".join(ln)),
                 ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Não conformidade e ação corretiva</title>")
assert "Não conformidade" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'),
      "| linha do tempo:", TOTAL, "dias | médias", br(ma), br(md))
