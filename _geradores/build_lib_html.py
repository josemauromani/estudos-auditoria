# -*- coding: utf-8 -*-
"""Monta treinamento-liberacao.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_data import (ABERTO, APOS, AUTORIZADO, CHECK, CONCES, DET, DISP_INFO, DUAS, ENCER, ETAPAS, EX1, EX2, FINAL, L_CONF, L_DESV, L_PEND, LIBERADO,  # noqa: E402
                      PROC, RECEB, REPETE, RETIDO, TRAT, lib_conf, lib_leitura, pnc_conf, pnc_sit, por_det, repeticoes, resumo)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# liberado, aguardando e retido: a mesma paleta de três cores do estudo de Satisfação, validada para daltonismo nos dois modos
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
table.aud{font-size:.8rem;min-width:960px;line-height:1.4}
table.aud th, table.aud td{padding:8px 9px}
table.aud td.n{white-space:nowrap;font-weight:600;color:var(--muted)}
table.aud td.c, table.aud th.c{text-align:center;font-variant-numeric:tabular-nums}
table.aud td.r, table.aud th.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
table.aud td.no{background:var(--s3-tint)}
table.aud td small, table.aud th small{display:block;color:var(--muted);font-size:.76rem;margin-top:3px;font-weight:400}
table.aud caption{caption-side:top;text-align:left;padding:10px 12px;font:500 .72rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:var(--sunk)}

/* Ficha do registro (acima de cada exemplo) */"""
assert css.count("\n.ficha{") == 1
css = css.replace("\n.ficha{", extra + "\n.ficha{", 1)
css += ("\n.quiz .opts{flex-wrap:wrap}\n.quiz .opts button{width:auto;min-width:40px;padding:0 11px;font-size:1rem}\n"
        "@media (min-width:720px){.q{grid-template-columns:minmax(0,1fr) auto}}\n")

TNUM = ' style="font-variant-numeric:tabular-nums"'


def dt(d, ano=True):
    return d.strftime("%d/%m/%Y" if ano else "%d/%m") if d else "—"


def rs(v):
    return "R$ " + f"{v:,.0f}".replace(",", ".")


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


def box(o, cls, x, y, w, h, tit, sub, ink=False, fs=12):
    o.append(f'        <rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>')
    o.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{y + 24}" font-size="{fs}">{escape(tit)}</text>')
    if sub:
        lines(o, sub, x + 12, y + 41, int(w / 6), fs=10.5, cls="t-ground" if ink else "mu", maxl=1)


H1, H2 = EX1["head"], EX2["head"]

# ------------------------------------------------------------------ figura 1: o caminho do produto
fl = ['      <svg viewBox="0 0 900 350" role="img" aria-label="O caminho do produto até o cliente. As verificações planejadas levam à pergunta: atende aos critérios? '
      'Se sim, o produto é liberado, com o registro de quem liberou, e entregue. Se não, é identificado e segregado, e quem tem autoridade decide a disposição. '
      'Retrabalhar ou reclassificar devolve o produto à verificação. Aceitar sob concessão leva à liberação com autorização. Refugar, devolver ou recolher tira o produto do fluxo. '
      'O defeito visto depois da entrega leva a informar o cliente e também passa pela decisão da disposição.">',
      "        <defs>" + marker("a1") + marker("a1m", True) + "</defs>"]
box(fl, "bx", 20, 20, 170, 56, "Verificações", "as planejadas")
box(fl, "bx-ink", 230, 20, 170, 56, "Atende aos critérios?", "de aceitação", ink=True)
box(fl, "bx-s1", 440, 20, 190, 56, "Liberar", "e registrar quem liberou")
box(fl, "bx", 670, 20, 210, 56, "Entregar ao cliente", "produto ou serviço")
box(fl, "bx-s3", 230, 140, 170, 56, "Identificar e segregar", "sai do fluxo")
box(fl, "bx-s2", 440, 140, 190, 56, "Decidir a disposição", "quem tem autoridade")
box(fl, "bx-s3", 670, 140, 210, 56, "Informar o cliente", "defeito visto depois da entrega")
box(fl, "bx", 230, 256, 170, 56, "Retrabalhar", "ou reclassificar")
box(fl, "bx", 440, 256, 190, 56, "Aceitar sob concessão", "com o aceite do cliente")
box(fl, "bx", 670, 256, 210, 56, "Refugar ou devolver", "ou recolher do cliente")
fl += ['        <line class="ln" x1="191" y1="40" x2="228" y2="40" marker-end="url(#a1)"/>',
       '        <line class="ln" x1="401" y1="40" x2="438" y2="40" marker-end="url(#a1)"/>',
       '        <text class="mu halo" x="419" y="34" font-size="10.5" text-anchor="middle">sim</text>',
       '        <line class="ln" x1="631" y1="40" x2="668" y2="40" marker-end="url(#a1)"/>',
       '        <line class="ln" x1="315" y1="77" x2="315" y2="138" marker-end="url(#a1)"/>',
       '        <text class="mu halo" x="323" y="112" font-size="10.5">não</text>',
       '        <line class="ln" x1="401" y1="168" x2="438" y2="168" marker-end="url(#a1)"/>',
       '        <path class="ln-mu dash" d="M775 77 V138" marker-end="url(#a1m)"/>',
       '        <line class="ln" x1="669" y1="168" x2="633" y2="168" marker-end="url(#a1)"/>',
       '        <path class="ln" d="M535 197 V226 H315 V254" marker-end="url(#a1)"/>',
       '        <path class="ln" d="M535 226 V254" marker-end="url(#a1)"/>',
       '        <path class="ln" d="M535 226 H775 V254" marker-end="url(#a1)"/>',
       '        <path class="ln-mu dash" d="M229 284 H210 V64 H228" marker-end="url(#a1m)"/>',
       '        <text class="mu halo" x="205" y="190" font-size="10.5" text-anchor="end">verificar</text>',
       '        <text class="mu halo" x="205" y="204" font-size="10.5" text-anchor="end">de novo</text>',
       '        <path class="ln-mu dash" d="M631 284 H652 V64 H633" marker-end="url(#a1m)"/>',
       '        <text class="mu halo" x="657" y="112" font-size="10.5">com</text>',
       '        <text class="mu halo" x="657" y="126" font-size="10.5">autorização</text>',
       '        <text x="450" y="340" font-size="11.5" text-anchor="middle">O produto que não atende sai do fluxo e só volta a ele por uma decisão de quem tem autoridade.</text>',
       "      </svg>"]

# ------------------------------------------------------------------ figura 2: as cinco etapas
W5, G5 = 164, 14
et = ['      <svg viewBox="0 0 900 206" role="img" aria-label="As cinco etapas do trabalho. ' + " ".join(f"{n}: {d}" for n, d in ETAPAS) + ' Os registros lidos devolvem o trabalho à primeira etapa.">',
      "        <defs>" + marker("a2") + marker("a2m", True) + "</defs>"]
for k, (nome, desc) in enumerate(ETAPAS):
    x = 12 + k * (W5 + G5)
    ink = k == 4
    et.append(f'        <rect class="{["bx-s1", "bx-s1", "bx-s3", "bx-s2", "bx-ink"][k]}" x="{x}" y="16" width="{W5}" height="124"/>')
    et.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="36" font-size="10">ETAPA {k + 1}</text>')
    et.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="58" font-size="13">{escape(nome)}</text>')
    lines(et, desc, x + 12, 80, 26, cls="t-ground" if ink else "", step=14.5, maxl=4)
    if k < 4:
        et.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="78" x2="{x + W5 + G5 - 2}" y2="78" marker-end="url(#a2)"/>')
xa, xb = 12 + 4 * (W5 + G5) + W5 / 2, 12 + W5 / 2
et.append(f'        <path class="ln-mu dash" d="M{xa} 142 V170 H{xb} V146" marker-end="url(#a2m)"/>')
et.append('        <text class="mu halo" x="450" y="174" font-size="11" text-anchor="middle">o defeito que se repete muda o critério, a verificação ou o processo</text>')
et.append('        <text x="450" y="198" font-size="11.5" text-anchor="middle">As duas primeiras etapas são a liberação (8.6). As três últimas, o controle do produto não conforme (8.7).</text>')
et.append("      </svg>")

# ------------------------------------------------------------------ figura 3: as seis disposições
ds = ['      <svg viewBox="0 0 900 330" role="img" aria-label="As seis disposições. ' + " ".join(f"{n}: {o} Quando: {q} Cuidado: {c}" for n, o, q, c, _ in DISP_INFO) + '">']
for k, (nome, oque, quando, cuidado, _) in enumerate(DISP_INFO):
    x, y = 10 + (k % 3) * 296, 10 + (k // 3) * 158
    ds.append(f'        <rect class="bx" x="{x}" y="{y}" width="284" height="148"/>')
    ds.append(f'        <rect class="hd-ink" x="{x}" y="{y}" width="284" height="32"/>')
    ds.append(f'        <text class="mono t-ground" x="{x + 12}" y="{y + 21}" font-size="10">{k + 1}</text>')
    ds.append(f'        <text class="b t-ground" x="{x + 30}" y="{y + 21}" font-size="12.5">{escape(nome)}</text>')
    yy = lines(ds, oque, x + 12, y + 52, 46, fs=11, step=14, maxl=2)
    ds.append(f'        <text class="mono mu" x="{x + 12}" y="{yy + 8}" font-size="9.5">CUIDADO</text>')
    lines(ds, cuidado, x + 12, yy + 24, 46, fs=10.5, step=13, maxl=3)
ds.append("      </svg>")

dispTab = ['  <div class="tbl">', '    <table>', '      <thead><tr><th style="width:18%">Disposição</th><th style="width:30%">Quando usar</th><th style="width:28%">Cuidado</th><th>Exemplo da série</th></tr></thead>', '      <tbody>']
for nome, _, quando, cuidado, exemplo in DISP_INFO:
    dispTab.append(f'        <tr><td><strong>{escape(nome)}</strong></td><td>{escape(quando)}</td><td>{escape(cuidado)}</td><td>{escape(exemplo)}</td></tr>')
dispTab += ['      </tbody>', '    </table>', '  </div>']

# ------------------------------------------------------------------ figura 4: as três situações do produto
SITU = [("bx-s1", "f1", "LIBERADO", "Etiqueta verde, carimbo ou rubrica", "Pode seguir para a etapa seguinte ou para o cliente.", "As verificações planejadas foram feitas e atendidas, e alguém com autoridade liberou."),
        ("bx-s2", "f2", "AGUARDANDO", "Etiqueta amarela, ou área de espera", "Não pode seguir, salvo liberação autorizada.", "Uma verificação está pendente: o laudo, o ensaio, a conferência."),
        ("bx-s3", "f3", "RETIDO", "Etiqueta vermelha e área separada", "Não pode seguir. Espera a disposição.", "Um resultado saiu do critério. Só quem tem autoridade decide o destino.")]
st = ['      <svg viewBox="0 0 900 236" role="img" aria-label="As três situações de um produto. ' + " ".join(f"{t}: marca: {m} {p} Quando: {q}" for _, _, t, m, p, q in SITU) + '">']
for k, (bx, f, tit, marca, pode, quando) in enumerate(SITU):
    x = 10 + k * 296
    st.append(f'        <rect class="{bx}" x="{x}" y="10" width="284" height="190"/>')
    st.append(f'        <rect class="{f}" x="{x + 12}" y="24" width="22" height="22"/>')
    st.append(f'        <text class="b" x="{x + 44}" y="41" font-size="13">{tit}</text>')
    st.append(f'        <text class="mono mu" x="{x + 12}" y="70" font-size="9.5">MARCA</text>')
    lines(st, marca, x + 12, 85, 44, fs=11)
    st.append(f'        <text class="mono mu" x="{x + 12}" y="112" font-size="9.5">PODE SEGUIR?</text>')
    lines(st, pode, x + 12, 127, 44, fs=11, maxl=2)
    st.append(f'        <text class="mono mu" x="{x + 12}" y="158" font-size="9.5">QUANDO</text>')
    lines(st, quando, x + 12, 173, 46, fs=10.5, maxl=2)
st.append('        <text x="450" y="226" font-size="11.5" text-anchor="middle">A situação está no produto, e não só no registro: quem pega a caixa ou a bobina sabe, na hora, se ela pode seguir.</text>')
st.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h = ex["head"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Processo</dt><dd>{escape(h["processo"])}</dd></div>',
                      f'    <div><dt>Produto</dt><dd>{escape(h["produto"])}</dd></div>',
                      f'    <div><dt>Quem libera</dt><dd>{escape(h["libera"])}</dd></div>',
                      f'    <div><dt>Quem decide a disposição</dt><dd>{escape(h["decide"])}</dd></div>',
                      f'    <div><dt>Registros</dt><dd>{escape(h["periodo"])}, lidos em {dt(h["ref"])}.</dd></div>',
                      f'    <div><dt>Origem</dt><dd>{escape(h["origem"])}</dd></div>',
                      '  </dl>'])


def tabela(caption, heads, rows):
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{caption}</caption>', f'      <thead><tr>{"".join(heads)}</tr></thead>', '      <tbody>']
    o += [f'        <tr>{r}</tr>' for r in rows]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


DEC_CLS = {LIBERADO: "s1", AUTORIZADO: "s2", RETIDO: "s3"}
LEIT_CLS = {L_CONF: "s1", L_PEND: "s2", L_DESV: "s3"}
SIT_CLS = {ABERTO: "s3", TRAT: "s2", ENCER: "s1"}


def conf_chip(c):
    return f'<span class="chip {"s1" if c == "OK" else "s3"}">{escape(c)}</span>'


def lib_tab(ex):
    r = resumo(ex)
    rows = []
    for l in ex["libs"]:
        quem = escape(l["quem"]) or "—"
        if l["aut"]:
            quem += f'<small>Autorizou: {escape(l["aut"])}</small>'
        rows.append(f'<td class="c">{dt(l["data"], False)}</td><td><strong>{escape(l["lote"])}</strong><small>{escape(l["prod"])}</small></td>'
                    f'<td class="c{" no" if l["feitas"] < l["prev"] else ""}">{l["feitas"]} de {l["prev"]}</td><td class="c{" no" if l["fora"] else ""}">{l["fora"]}</td>'
                    f'<td><span class="chip {LEIT_CLS[lib_leitura(l)]}">{lib_leitura(l)}</span></td><td><span class="chip {DEC_CLS[l["dec"]]}">{l["dec"]}</span></td>'
                    f'<td>{quem}</td><td>{escape(l["pnc"]) or "—"}{"<small>" + escape(l["obs"]) + "</small>" if l["obs"] else ""}</td><td>{conf_chip(lib_conf(l))}</td>')
    return tabela(f'Liberações · {r["libs"]} registros, {r["aut"]} com autorização, {r["ret"]} {"retido" if r["ret"] == 1 else "retidos"}, {r["lib_rever"]} a rever',
                  ['<th class="c">Data</th>', '<th style="width:13%">Lote<small>Quantidade</small></th>', '<th class="c">Verificações</th>', '<th class="c">Fora</th>', '<th>Leitura</th>',
                   '<th style="width:12%">Decisão</th>', '<th style="width:17%">Quem liberou</th>', '<th style="width:22%">Registro de não conforme<small>Observação</small></th>', '<th>Conferência</th>'], rows)


def pnc_tab(ex):
    r = resumo(ex)
    regs = ex["pncs"]
    rows = []
    for p in regs:
        s = pnc_sit(p)
        rep = repeticoes(p, regs)
        defe = f'<strong>{escape(p["defeito"])}</strong>' + (f' · {rep}×' if rep > 1 else "") + f'<small>{escape(p["desc"])}</small>'
        disp = (escape(p["disp"]) + f'<small>{escape(p["quem"])}</small>') if p["disp"] else "—"
        extra = []
        if p["cliente"]:
            extra.append(escape(p["cliente"]))
        if p["rev"]:
            extra.append("Reverificação: " + escape(p["rev"].lower()) + ".")
        if p["acao"]:
            extra.append("Ação corretiva: " + escape(p["acao"]) + ".")
        rows.append(f'<td class="n">{p["num"]}<small>{dt(p["data"], False)}</small></td><td>{escape(p["lote"])}<small>{escape(p["qtd"])}</small></td><td>{defe}</td><td>{escape(p["det"])}</td>'
                    f'<td>{escape(p["seg"]) or "—"}</td><td>{disp}</td><td>{" ".join(extra) or "—"}</td>'
                    f'<td><span class="chip {SIT_CLS[s]}">{s}</span>{"<small>" + dt(p["enc"], False) + "</small>" if p["enc"] else ""}</td>'
                    f'<td class="r">{rs(p["custo"]) if p["custo"] is not None else "—"}</td><td>{conf_chip(pnc_conf(p, regs))}</td>')
    ab = r["sits"][ABERTO]
    return tabela(f'Produto não conforme · {r["pncs"]} registros, {ab} {"aberto" if ab == 1 else "abertos"}, {r["sits"][TRAT]} em tratamento, custo de {rs(r["custo"])}',
                  ['<th style="width:6%">Nº<small>Data</small></th>', '<th style="width:10%">Lote<small>Quantidade</small></th>', '<th style="width:20%">Defeito</th>', '<th>Onde foi visto</th>',
                   '<th style="width:13%">Identificação e segregação</th>', '<th style="width:11%">Disposição<small>Quem decidiu</small></th>', '<th style="width:15%">Cliente, reverificação e ação</th>',
                   '<th>Situação</th>', '<th class="r">Custo</th>', '<th>Conferência</th>'], rows)


def det_tab(ex):
    pd = por_det(ex)
    tot = sum(x["custo"] for x in pd)
    rows = [f'<td><strong>{x["det"]}</strong></td><td class="c">{x["n"]}</td><td class="r">{rs(x["custo"])}</td><td class="r">{rs(x["medio"]) if x["medio"] is not None else "—"}</td>'
            f'<td class="c">{(str(int(100 * x["custo"] / tot + 0.5)) + "%") if tot else "—"}</td>' for x in pd]
    return tabela('Onde o defeito foi visto, e quanto custou',
                  ['<th style="width:30%">Ponto de detecção</th>', '<th class="c">Registros</th>', '<th class="r">Custo</th>', '<th class="r">Custo por registro</th>', '<th class="c">Parte do custo</th>'], rows)


# ------------------------------------------------------------------ exemplo 3: duas liberações com verificação pendente
e3 = ['      <svg viewBox="0 0 900 372" role="img" aria-label="Duas liberações com verificação pendente na indústria. ' + DUAS["a"]["tit"] + ": "
      + " ".join(f"{a}, {b}: {c}" for a, b, c in DUAS["a"]["passos"]) + " " + DUAS["b"]["tit"] + ": " + " ".join(f"{a}, {b}: {c}" for a, b, c in DUAS["b"]["passos"]) + " " + DUAS["conclusao"] + '">',
      "        <defs>" + marker("a5") + "</defs>"]
for j, (k, cls, hd) in enumerate((("a", "bx-s1", "f1"), ("b", "bx-s3", "f3"))):
    x = 20 + j * 440
    d = DUAS[k]
    e3.append(f'        <rect class="{hd}" x="{x}" y="10" width="420" height="34"/>')
    e3.append(f'        <text class="b on" x="{x + 12}" y="32" font-size="12.5">{escape(d["tit"])}</text>')
    for i, (quando, tit, txt) in enumerate(d["passos"]):
        y = 56 + i * 70
        last = i == len(d["passos"]) - 1
        e3.append(f'        <rect class="{cls if last else "bx"}" x="{x}" y="{y}" width="420" height="60"/>')
        e3.append(f'        <text class="mono mu" x="{x + 12}" y="{y + 20}" font-size="9.5">{escape(quando.upper())}</text>')
        e3.append(f'        <text class="b" x="{x + 96}" y="{y + 20}" font-size="11.5">{escape(tit)}</text>')
        lines(e3, txt, x + 96, y + 37, 54, fs=10.5, maxl=2)
        if not last:
            e3.append(f'        <line class="ln" x1="{x + 40}" y1="{y + 61}" x2="{x + 40}" y2="{y + 68}" marker-end="url(#a5)"/>')
for i, l in enumerate(textwrap.wrap(DUAS["conclusao"], 118)[:2]):
    e3.append(f'        <text x="450" y="{348 + i * 16}" font-size="11.5" text-anchor="middle">{escape(l)}</text>')
e3.append("      </svg>")

# ------------------------------------------------------------------ módulo 7: custo por ponto de detecção, na indústria
pd2 = por_det(EX2)
VMAX = 3500
X0, X1, Y0, Y1 = 90, 860, 50, 250
BW = 120
cx = lambda k: X0 + (X1 - X0) * (k + 0.5) / len(pd2)  # noqa: E731
sy = lambda v: Y1 - v * (Y1 - Y0) / VMAX  # noqa: E731
ch = ['      <svg id="bars" viewBox="0 0 900 312" role="img" aria-label="Custo por registro de produto não conforme, por ponto de detecção, na indústria, de 11 a 26 de maio de 2027. '
      + " ".join(f'{x["det"]}: {x["n"]} registros, {rs(x["medio"]) if x["medio"] is not None else "sem registro"} por registro.' for x in pd2) + '">']
for v in range(0, VMAX + 1, 500):
    ch.append(f'        <line class="grid" x1="{X0}" y1="{sy(v)}" x2="{X1}" y2="{sy(v)}"/>')
    ch.append(f'        <text class="mu" x="{X0 - 10}" y="{sy(v) + 4}" font-size="11" text-anchor="end"{TNUM}>{rs(v)[3:]}</text>')
ch.append(f'        <text class="mono mu" x="{X0}" y="28" font-size="10">CUSTO POR REGISTRO, EM R$</text>')
for k, x in enumerate(pd2):
    m = x["medio"] or 0
    cls = ["f1", "f1", "f2", "f3"][k]
    if m > 0:
        ch.append(f'        <rect class="bar {cls}" data-k="{k}" x="{cx(k) - BW / 2}" y="{sy(m):.1f}" width="{BW}" height="{Y1 - sy(m):.1f}"/>')
    ch.append(f'        <text class="b halo" x="{cx(k)}" y="{sy(m) - 8:.1f}" font-size="12" text-anchor="middle"{TNUM}>{rs(m)}</text>')
    ch.append(f'        <text x="{cx(k)}" y="{Y1 + 20}" font-size="11.5" text-anchor="middle">{escape(x["det"])}</text>')
    ch.append(f'        <text class="mu" x="{cx(k)}" y="{Y1 + 36}" font-size="10.5" text-anchor="middle">{x["n"]} registro{"s" if x["n"] != 1 else ""}</text>')
ch.append(f'        <line class="ln-mu" x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}"/>')
for k, x in enumerate(pd2):
    ch.append(f'        <rect class="hit" x="{cx(k) - (X1 - X0) / 8}" y="{Y0 - 10}" width="{(X1 - X0) / 4}" height="{Y1 - Y0 + 50}" tabindex="0" role="img" '
              f'aria-label="{x["det"]}: {x["n"]} registros, custo total {rs(x["custo"])}, {rs(x["medio"] or 0)} por registro" data-k="{k}" data-n="{escape(x["det"])}" '
              f'data-c="{rs(x["custo"])}" data-r="{x["n"]}" data-m="{rs(x["medio"] or 0)}" data-cx="{cx(k)}" data-cy="{sy(x["medio"] or 0):.1f}"/>')
ch.append("      </svg>")
tb = ['        <table class="aud">', '          <thead><tr><th>Ponto de detecção</th><th class="c">Registros</th><th class="r">Custo</th><th class="r">Custo por registro</th></tr></thead>', '          <tbody>']
for x in pd2:
    tb.append(f'            <tr><td>{x["det"]}</td><td class="c">{x["n"]}</td><td class="r">{rs(x["custo"])}</td><td class="r">{rs(x["medio"]) if x["medio"] is not None else "—"}</td></tr>')
tb += ['          </tbody>', '        </table>']
dd = {x["det"]: x for x in pd2}
charttext = (f'  <p>Na fábrica, o registro encontrado no recebimento não custou nada: a resina úmida voltou ao fornecedor antes de entrar no estoque. No processo, cada registro custou, em média, '
             f'{rs(dd[PROC]["medio"])}: a bobina refugada, reclassificada ou refilada. Na inspeção final, {rs(dd[FINAL]["medio"])}: o lote inteiro já estava feito e foi para o cliente com desconto. '
             f'Depois da entrega, {rs(dd[APOS]["medio"])} por registro, com o frete, a reposição e uma conversa difícil. Os {dd[APOS]["n"]} registros achados no cliente são '
             f'{int(100 * dd[APOS]["custo"] / sum(x["custo"] for x in pd2) + 0.5)}% do custo do período. O gráfico é o argumento mais forte para controlar o processo e liberar com cuidado: '
             f'o mesmo defeito custa mais a cada etapa em que passa sem ser visto.</p>')

# ------------------------------------------------------------------ módulo 10: figura da ISO
ISOP = [("8.6 · Liberar", "Liberar só depois das verificações planejadas, salvo aprovação de quem tem autoridade e, se for o caso, do cliente.", "o registro de liberação"),
        ("8.7.1 · Controlar", "Identificar e controlar o que não atende. Corrigir, segregar, devolver, informar o cliente ou obter concessão.", "as seis disposições"),
        ("8.7.2 · Registrar", "Descrever o defeito, as ações, as concessões e quem decidiu.", "o registro de produto não conforme"),
        ("10.2 · Tratar a causa", "Quando o defeito se repete ou é grave, analisar a causa e agir sobre ela.", "o defeito repetido na planilha")]
iso = ['      <svg viewBox="0 0 900 200" role="img" aria-label="O que a norma pede sobre a liberação e o produto não conforme. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in ISOP) + '">']
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
for tag, val in (("<!--CAMINHO-->", "\n".join(fl)), ("<!--FLUXO-->", "\n".join(et)), ("<!--DISP-->", "\n".join(ds)), ("<!--DISPTAB-->", "\n".join(dispTab)), ("<!--SITUACAO-->", "\n".join(st)),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1LIB-->", lib_tab(EX1)), ("<!--EX1PNC-->", pnc_tab(EX1)), ("<!--EX1DET-->", det_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2LIB-->", lib_tab(EX2)), ("<!--EX2PNC-->", pnc_tab(EX2)), ("<!--EX2DET-->", det_tab(EX2)),
                 ("<!--EX3FIG-->", "\n".join(e3)), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)), ("<!--CHARTTEXT-->", charttext),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check), ("<!--REPETE-->", str(REPETE))):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>Liberação e produto não conforme</title>")
assert "Liberação e produto" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", resumo(EX1), "| indústria", resumo(EX2))
