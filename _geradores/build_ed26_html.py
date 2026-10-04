# -*- coding: utf-8 -*-
"""Monta treinamento-iso-9001-2026.html: CSS herdado do estudo de PDCA + corpo próprio + figuras e tabelas geradas dos dados."""
import os
import re
import sys
import textwrap
from datetime import date
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ed26_data import (ATRAS, CHECK, CONCL, CULTURA, ESCLAR, ETAPAS, EX1, EX2, FIM_TRANSICAO, INCORP, MUDANCAS, NAO_MUDOU, NOPRAZO, NOVO,  # noqa: E402
                       OPORT_IND, P_ALTA, P_ATRAS, P_BAIXA, P_FORA, P_MEDIA, P_PREV, P_REAL, P_SEM, P_VENCE, PASSOS, PUBLICACAO, REESTR, REFORCADO, RISCOS_IND,
                       SEMACAO, SO_2026, acao_sit, diag_conf, limite_passo, passo_sit, prioridade, prioridade_pts, resumo)

SRC, BODY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>\n(.*?)</style>", src, re.S).group(1)

# sem lacuna, lacuna média e lacuna alta: a mesma paleta de três cores do estudo de Calibração, validada para daltonismo nos dois modos
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
svg .lane{fill:var(--sunk)}
svg .now{stroke:var(--ink);stroke-width:1.5;stroke-dasharray:4 3}
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
MID = ' text-anchor="middle"'
W5, G5 = 164, 14
LINKS = {"swot": "../SWOT/treinamento-swot.html", "esc": "../Escopo/treinamento-escopo.html", "obj": "../Objetivos/treinamento-objetivos.html",
         "riscos": "../Riscos/treinamento-riscos.html", "caso": "../Caso-Integrado/treinamento-caso-integrado.html", "comp": "../Competencias/treinamento-competencias.html",
         "doc": "../Informacao-Documentada/treinamento-informacao-documentada.html", "iso": "../ISO-9001/treinamento-iso-9001.html"}
NOMES = {"swot": "Matriz SWOT", "esc": "Escopo e liderança", "obj": "Objetivos da qualidade", "riscos": "Matriz de riscos", "caso": "Caso integrado",
         "comp": "Matriz de competências", "doc": "Informação documentada", "iso": "ISO 9001 requisito a requisito"}


def dt(d, ano=True):
    return d.strftime("%d/%m/%Y" if ano else "%d/%m") if d else "—"


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


def cinco(o, itens, classes, mk, y0=16, h=140, rotulo=None, maxd=5, mid=None, wrap_d=25):
    xs = []
    for k, (tit, desc) in enumerate(itens):
        x = 12 + k * (W5 + G5)
        xs.append(x)
        ink = classes[k] == "bx-ink"
        o.append(f'        <rect class="{classes[k]}" x="{x}" y="{y0}" width="{W5}" height="{h}"/>')
        if rotulo:
            o.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="{y0 + 20}" font-size="10">{escape(rotulo(k))}</text>')
        tl = textwrap.wrap(tit, 19, break_on_hyphens=False)
        yt = y0 + (42 if rotulo else 24)
        for j, l in enumerate(tl):
            o.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{yt + j * 15}" font-size="12.5">{escape(l)}</text>')
        lines(o, desc, x + 12, yt + 15 * len(tl) + 8, wrap_d, cls="t-ground" if ink else "", step=14.5, maxl=maxd)
        if mk and k < len(itens) - 1:
            ym = mid or (y0 + h / 2)
            o.append(f'        <line class="ln" x1="{x + W5 + 1}" y1="{ym}" x2="{x + W5 + G5 - 2}" y2="{ym}" marker-end="url(#{mk})"/>')
    return xs


# ------------------------------------------------------------------ figura 1: o mapa das mudanças
TCLS = {NOVO: "f3", REFORCADO: "f2", REESTR: "f2", INCORP: "f1", ESCLAR: "f1"}
MUD_ONDE = {"4.1": "M1", "4.2": "M1", "5.1.1": "M2", "5.2": "M3", "6.1": "M4", "6.3": "M5", "7.3": "M6", "Termos": "M7", "Anexo A": "M9"}
COLS = [("3", "Termos", ["Termos"]), ("4", "Contexto", ["4.1", "4.2", "4.3", "4.4"]), ("5", "Liderança", ["5.1.1", "5.1.2", "5.2", "5.3"]),
        ("6", "Planejamento", ["6.1", "6.2", "6.3"]), ("7", "Apoio", ["7.1", "7.2", "7.3", "7.4", "7.5"]), ("8", "Operação", ["8.1", "8.2", "8.3", "8.4", "8.5", "8.6", "8.7"]),
        ("9", "Avaliação", ["9.1", "9.2", "9.3"]), ("10", "Melhoria", ["10.1", "10.2", "10.3"]), ("A", "Anexo", ["Anexo A"])]
mud = {m[0]: m for m in MUDANCAS}
CW = 96
ma = ['      <svg viewBox="0 0 900 330" role="img" aria-label="Onde a ISO 9001:2026 muda, seção por seção. '
      + " ".join(f'{m[1]}, {m[2]}: {m[3].lower()}.' for m in MUDANCAS) + ' As seções 8, 9 e 10 não têm mudança de requisito.">']
for j, (n, t, itens) in enumerate(COLS):
    x = 12 + j * (CW + 2)
    ma.append(f'        <rect class="hd-ink" x="{x}" y="14" width="{CW}" height="40"/>')
    ma.append(f'        <text class="disp t-ground" x="{x + CW / 2}" y="36" font-size="16"{MID}>{n}</text>')
    ma.append(f'        <text class="mono t-ground" x="{x + CW / 2}" y="49" font-size="8.5"{MID}>{escape(t.upper())}</text>')
    for i, it in enumerate(itens):
        y = 62 + i * 28
        cod = MUD_ONDE.get(it)
        cls = TCLS[mud[cod][3]] if cod else "lane"
        ma.append(f'        <rect class="{cls}" x="{x + 6}" y="{y}" width="{CW - 12}" height="22"/>')
        ma.append(f'        <text class="{"b on" if cod and cls != "f2" else "b" if cod else "mu"}" x="{x + CW / 2}" y="{y + 15}" font-size="11"{MID}{TNUM}>{escape(it)}</text>')
ma.append('        <rect class="bx-s1" x="12" y="268" width="876" height="24"/>')
ma.append(f'        <text class="b" x="450" y="285" font-size="11.5"{MID}>Estrutura harmonizada atualizada, comum às normas de sistema de gestão</text>')
for k, (t, cls) in enumerate((("Novo", "f3"), ("Reforçado ou reestruturado", "f2"), ("Incorporado ou esclarecimento", "f1"), ("Sem mudança de requisito", "lane"))):
    ma.append(f'        <rect class="{cls}" x="{60 + k * 210}" y="306" width="14" height="14"/><text x="{80 + k * 210}" y="318" font-size="11">{t}</text>')
ma.append("      </svg>")

# ------------------------------------------------------------------ figura 2: as datas da transição
T0, T1 = date(2026, 7, 1), date(2029, 12, 31)
tx = lambda d: 40 + (d - T0).days * (860 - 40) / (T1 - T0).days  # noqa: E731
EVT = [(PUBLICACAO, "Publicação da ISO 9001:2026"), (EX1["plano"]["audit"], "Fase 1 da pizzaria, já pela edição de 2026"),
       (SO_2026, "Certificados novos só pela edição de 2026"), (EX2["plano"]["audit"], "Transição da indústria, na 1ª manutenção"),
       (FIM_TRANSICAO, "Fim da transição: certificados de 2015 deixam de valer")]
tr = ['      <svg viewBox="0 0 900 236" role="img" aria-label="As datas da transição. ' + " ".join(f"{dt(d)}: {t}." for d, t in EVT) + '">']
tr.append(f'        <rect class="bx-s2" x="{tx(PUBLICACAO):.1f}" y="86" width="{tx(FIM_TRANSICAO) - tx(PUBLICACAO):.1f}" height="28"/>')
for a in range(2027, 2030):
    d = date(a, 1, 1)
    tr.append(f'        <line class="grid" x1="{tx(d):.1f}" y1="80" x2="{tx(d):.1f}" y2="120"/>')
    tr.append(f'        <text class="mu" x="{tx(d):.1f}" y="134" font-size="10.5"{MID}{TNUM}>{a}</text>')
for k, (d, t) in enumerate(EVT):
    x = tx(d)
    y = 42 if k % 2 == 0 else 176
    tr.append(f'        <line class="ln-mu" x1="{x:.1f}" y1="{56 if y < 100 else 118}" x2="{x:.1f}" y2="{84 if y < 100 else 164}"/>')
    tr.append(f'        <circle class="{"f3" if d in (FIM_TRANSICAO, SO_2026) else "f1"}" cx="{x:.1f}" cy="100" r="6"/>')
    anc = MID if 0 < k < len(EVT) - 1 else ("" if k == 0 else END)
    xt = x if anc == MID else (x - 6 if k == 0 else x + 6)
    tr.append(f'        <text class="b" x="{xt:.1f}" y="{y}" font-size="11"{anc}>{dt(d)}</text>')
    lines(tr, t, xt, y + 14, 30, fs=10.5, cls="mu", step=13, maxl=2, anchor=None if anc == "" else anc.split('"')[1])
tr.append(f'        <text x="450" y="228" font-size="11.5"{MID}>Datas do documento de transição da Global ACI, publicado junto com a norma.</text>')
tr.append("      </svg>")

# ------------------------------------------------------------------ figura 3: as oito etapas, em duas linhas de quatro
W8, G8, H8, Y8 = 196, 24, 118, (16, 170)
et = ['      <svg viewBox="0 0 900 340" role="img" aria-label="As oito etapas da transição. ' + " ".join(f"Etapa {k}, {n}: {d}" for k, (n, d) in enumerate(ETAPAS, 1))
      + ' O que a auditoria do organismo encontrar volta às ações.">', "        <defs>" + marker("a3") + marker("a3m", True) + "</defs>"]
CL8 = ["bx", "bx-p", "bx-p", "bx-d", "bx-d", "bx-c", "bx-c", "bx-ink"]
for k, (tit, desc) in enumerate(ETAPAS):
    x, y0 = 12 + (k % 4) * (W8 + G8), Y8[k // 4]
    ink = CL8[k] == "bx-ink"
    et.append(f'        <rect class="{CL8[k]}" x="{x}" y="{y0}" width="{W8}" height="{H8}"/>')
    et.append(f'        <text class="mono {"t-ground" if ink else "mu"}" x="{x + 12}" y="{y0 + 20}" font-size="10">ETAPA {k + 1}</text>')
    tl = textwrap.wrap(tit, 22, break_on_hyphens=False)
    assert len(tl) <= 2, tit
    for j, l in enumerate(tl):
        et.append(f'        <text class="b{" t-ground" if ink else ""}" x="{x + 12}" y="{y0 + 42 + j * 15}" font-size="12.5">{escape(l)}</text>')
    lines(et, desc, x + 12, y0 + 42 + 15 * len(tl) + 6, 30, cls="t-ground" if ink else "", step=14, maxl=3)
    if k % 4 < 3:
        ym = y0 + H8 / 2
        et.append(f'        <line class="ln" x1="{x + W8 + 1}" y1="{ym}" x2="{x + W8 + G8 - 2}" y2="{ym}" marker-end="url(#a3)"/>')
c4, c5 = 12 + 3 * (W8 + G8) + W8 / 2, 12 + W8 / 2
et.append(f'        <path class="ln" d="M{c4} {Y8[0] + H8 + 1} V{Y8[0] + H8 + 18} H{c5} V{Y8[1] - 2}" marker-end="url(#a3)"/>')
xr = 12 + 3 * (W8 + G8) + W8
et.append(f'        <path class="ln-mu dash" d="M{xr + 1} {Y8[1] + H8 / 2} H{xr + 18} V{Y8[0] + H8 / 2} H{xr + 2}" marker-end="url(#a3m)"/>')
et.append(f'        <text class="mu" x="{xr + 18}" y="{Y8[1] + H8 + 18}" font-size="11"{END}>constatações da auditoria do organismo voltam às ações</text>')
et.append(f'        <text x="450" y="{Y8[1] + H8 + 44}" font-size="11.5"{MID}>A transição não pede um sistema novo: pede ajustes em poucos pontos, feitos e auditados antes da data.</text>')
et.append("      </svg>")

# ------------------------------------------------------------------ figura 4: a cultura da qualidade em três camadas
cu = ['      <svg viewBox="0 0 900 236" role="img" aria-label="A cultura da qualidade na edição de 2026, em três camadas. ' + " ".join(f"{a}, requisito {c}: {b}" for a, b, c in CULTURA) + '">',
      "        <defs>" + marker("a4") + "</defs>"]
for k, (a, b, c) in enumerate(CULTURA):
    y = 14 + k * 72
    cls, hd = (("bx-s3", "f3"), ("bx-s2", "f2"), ("bx-s1", "f1"))[k]
    cu.append(f'        <rect class="{cls}" x="12" y="{y}" width="560" height="60"/>')
    cu.append(f'        <rect class="{hd}" x="12" y="{y}" width="8" height="60"/>')
    cu.append(f'        <text class="b" x="34" y="{y + 25}" font-size="13">{escape(a)}</text>')
    cu.append(f'        <text class="mono mu" x="560" y="{y + 25}" font-size="10.5"{END}>{c}</text>')
    lines(cu, b, 34, y + 44, 84, fs=11, step=14, maxl=1)
    if k < 2:
        cu.append(f'        <line class="ln" x1="292" y1="{y + 61}" x2="292" y2="{y + 71}" marker-end="url(#a4)"/>')
cu.append('        <rect class="bx-ink" x="596" y="14" width="292" height="204"/>')
yy = lines(cu, "Cultura não é cartaz", 612, 42, 30, fs=13, cls="b t-ground", step=16, maxl=1)
lines(cu, "O auditor vai procurar a cultura nas decisões: o que a direção fez quando o prazo apertou e a qualidade estava em jogo, e o que as pessoas dizem que se espera delas.",
      612, yy + 8, 40, fs=11, cls="t-ground", step=15, maxl=8)
cu.append("      </svg>")

# ------------------------------------------------------------------ figura 5: riscos e oportunidades, antes e depois
ro = ['      <svg viewBox="0 0 900 206" role="img" aria-label="Riscos e oportunidades na edição de 2015 e na de 2026. Em 2015, um requisito tratava dos dois juntos. '
      'Em 2026, os riscos e as oportunidades têm requisitos próprios, cada um com determinação, ações e avaliação da eficácia.">', "        <defs>" + marker("a5") + "</defs>"]
ro.append('        <rect class="bx" x="12" y="40" width="300" height="120"/>')
ro.append('        <text class="mono mu" x="24" y="30" font-size="10">EDIÇÃO DE 2015</text>')
ro.append('        <text class="b" x="28" y="72" font-size="13">6.1 Riscos e oportunidades</text>')
lines(ro, "Um requisito para os dois. Muitas organizações listavam tudo junto, e as oportunidades ficavam sem ação.", 28, 98, 42, fs=11, cls="mu", step=15, maxl=3)
ro.append('        <line class="ln" x1="316" y1="100" x2="380" y2="100" marker-end="url(#a5)"/>')
ro.append('        <text class="mono mu" x="396" y="30" font-size="10">EDIÇÃO DE 2026</text>')
for k, (t, d, cls) in enumerate((("Riscos", "Determinar o que pode dar errado, agir conforme o efeito e avaliar a ação.", "bx-s3"),
                                 ("Oportunidades", "Determinar o que aproveitar, decidir o que fazer e avaliar o resultado.", "bx-s1"))):
    y = 40 + k * 64
    ro.append(f'        <rect class="{cls}" x="396" y="{y}" width="492" height="56"/>')
    ro.append(f'        <text class="b" x="412" y="{y + 22}" font-size="12.5">{t}</text>')
    lines(ro, d, 412, y + 40, 80, fs=11, step=14, maxl=1)
ro.append(f'        <text x="450" y="194" font-size="11.5"{MID}>A ideia não é nova; a separação é. A oportunidade passa a ter a mesma disciplina do risco.</text>')
ro.append("      </svg>")

# ------------------------------------------------------------------ figura 6: o que não mudou
nm = ['      <svg viewBox="0 0 900 184" role="img" aria-label="O que não mudou na ISO 9001:2026. ' + " ".join(f"{a}: {b}" for a, b in NAO_MUDOU) + '">']
cinco(nm, NAO_MUDOU, ["bx-s1", "bx-s1", "bx-s1", "bx-s1", "bx"], None, h=156, maxd=6)
nm.append("      </svg>")


# ------------------------------------------------------------------ exemplos
def ficha(ex):
    h, pl = ex["head"], ex["plano"]
    return "\n".join(['  <dl class="ficha">',
                      f'    <div><dt>Organização</dt><dd>{escape(h["org"])}</dd></div>',
                      f'    <div><dt>Situação</dt><dd>{escape(h["situacao"])}</dd></div>',
                      f'    <div><dt>Auditoria</dt><dd>{escape(h["auditoria"])}, em {dt(pl["audit"])}.</dd></div>',
                      f'    <div><dt>Responsável</dt><dd>{escape(h["resp"])}</dd></div>',
                      f'    <div><dt>Leitura</dt><dd>{dt(h["ref"])}.</dd></div>',
                      '  </dl>'])


def tabela(caption, heads, rows):
    o = ['  <div class="tbl">', '    <table class="aud">', f'      <caption>{caption}</caption>', f'      <thead><tr>{"".join(heads)}</tr></thead>', '      <tbody>']
    o += [f'        <tr>{r}</tr>' for r in rows]
    o += ['      </tbody>', '    </table>', '  </div>']
    return "\n".join(o)


def chip(c, ok=("OK",)):
    return f'<span class="chip {"s1" if c in ok else "s3"}">{escape(c)}</span>'


SIT_CLS = {"Atende": "s1", "Atende em parte": "s2", "Não atende": "s3", "Não se aplica": "sl"}
PRI_CLS = {P_ALTA: "s3", P_MEDIA: "s2", P_BAIXA: "sl", P_SEM: "s1"}
AC_CLS = {CONCL: "s1", NOPRAZO: "s2", ATRAS: "s3"}
PL_CLS = {P_REAL: "s1", P_FORA: "s3", P_PREV: "sl", P_VENCE: "s2", P_ATRAS: "s3"}


def diag_tab(ex):
    ref, r = ex["head"]["ref"], resumo(ex)
    rows = []
    for m, d in zip(MUDANCAS, ex["diag"]):
        p, a = prioridade(m, d["sit"]), acao_sit(d, ref)
        ac = "—" if a == SEMACAO else f'<span class="chip {AC_CLS[a]}">{a}</span>'
        acao = f'{escape(d["acao"])}<small>{escape(d["resp"])} · até {dt(d["prazo"])}{" · concluída em " + dt(d["concl"]) if d["concl"] else ""}</small>' if d["acao"] else "—"
        rows.append(f'<td class="n">{m[0]}</td><td><strong>{escape(m[2])}</strong><small>{m[1]} · {m[3].lower()} · impacto {m[4].lower()}</small></td>'
                    f'<td><span class="chip {SIT_CLS[d["sit"]]}">{d["sit"]}</span><small>{escape(d["evid"]) or "sem evidência"}</small></td>'
                    f'<td class="c">{prioridade_pts(m, d["sit"])}</td><td><span class="chip {PRI_CLS[p]}">{p}</span></td><td>{acao}</td>'
                    f'<td>{ac}</td><td>{chip(diag_conf(d))}</td>')
    s = r["sits"]
    return tabela(f'Diagnóstico das mudanças · {s["Atende"]} atende, {s["Atende em parte"]} em parte, {s["Não atende"]} não atende · {r["pts"]} pontos de lacuna',
                  ['<th>Código</th>', '<th style="width:20%">Mudança<small>Onde · tipo · impacto</small></th>', '<th style="width:20%">Situação<small>Evidência</small></th>',
                   '<th class="c">Pontos</th>', '<th>Prioridade</th>', '<th style="width:26%">Ação<small>Responsável · prazo</small></th>', '<th>Ação</th>', '<th>Conferência</th>'], rows)


def plano_tab(ex):
    pl = ex["plano"]
    rows = []
    for k, (p, dias) in enumerate(PASSOS):
        s = passo_sit(pl, k)
        rows.append(f'<td class="n">{k + 1}</td><td><strong>{escape(p)}</strong></td><td class="c">{dias}</td><td class="c">{dt(limite_passo(pl["audit"], k))}</td>'
                    f'<td class="c">{dt(pl["feito"][k])}</td><td><span class="chip {PL_CLS[s]}">{s}</span></td>')
    return tabela(f'Plano de transição · auditoria em {dt(pl["audit"])}, lido em {dt(pl["ref"])}',
                  ['<th>#</th>', '<th style="width:40%">Etapa</th>', '<th class="c">Dias antes da auditoria</th>', '<th class="c">Limite</th>', '<th class="c">Feito em</th>',
                   '<th>Situação</th>'], rows)


# ------------------------------------------------------------------ exemplo 3: riscos e oportunidades da indústria em duas listas
ex3 = ['      <svg viewBox="0 0 900 290" role="img" aria-label="A matriz de riscos de Suprimentos da indústria, com os riscos e as oportunidades em listas separadas. Riscos: '
       + ", ".join(f"{a}, {b}" for a, b in RISCOS_IND) + ". Oportunidades: " + ", ".join(f"{a}, {b}" for a, b in OPORT_IND) + '.">']
for k, (tit, req, itens, cls, hd, x, w) in enumerate((("Riscos", "6.1.2", RISCOS_IND, "bx-s3", "f3", 12, 470), ("Oportunidades", "6.1.3", OPORT_IND, "bx-s1", "f1", 498, 390))):
    ex3.append(f'        <rect class="{cls}" x="{x}" y="14" width="{w}" height="240"/>')
    ex3.append(f'        <rect class="{hd}" x="{x}" y="14" width="{w}" height="32"/>')
    ex3.append(f'        <text class="b on" x="{x + 14}" y="35" font-size="13">{tit}</text>')
    ex3.append(f'        <text class="mono on" x="{x + w - 14}" y="35" font-size="10.5"{END}>{req}</text>')
    for i, (c, t) in enumerate(itens):
        y = 70 + i * 23
        ex3.append(f'        <text x="{x + 14}" y="{y}" font-size="11.5"><tspan class="b"{TNUM}>{c}</tspan><tspan dx="10">{escape(t)}</tspan></text>')
ex3.append(f'        <text x="450" y="280" font-size="11.5"{MID}>A matriz de outubro de 2026, feita pela edição de 2015, já separava as listas. A edição nova confirma o trabalho.</text>')
ex3.append("      </svg>")

# ------------------------------------------------------------------ módulo 9: os pontos de lacuna por mudança, nos dois exemplos
X0, X1, TOP, RH = 380, 860, 46, 24
px = lambda v: X0 + v * (X1 - X0) / 6  # noqa: E731
rows_c = []
for nome, ex in (("PIZZARIA", EX1), ("INDÚSTRIA", EX2)):
    rows_c.append(("grupo", nome, ex))
    rows_c += [("m", (m, d), ex) for m, d in zip(MUDANCAS, ex["diag"])]
bottom = TOP + RH * len(rows_c)
PCOR = {P_ALTA: "f3", P_MEDIA: "f2", P_BAIXA: "f0", P_SEM: "f1"}
ch = [f'      <svg id="bars" viewBox="0 0 900 {bottom + 44}" role="img" aria-label="Pontos de lacuna por mudança, nos dois exemplos: impacto vezes lacuna, de 0 a 6. '
      + " ".join(f'{r[1][0][0]}: {prioridade_pts(r[1][0], r[1][1]["sit"])} pontos.' for r in rows_c if r[0] == "m") + '">', '        <g font-size="11.5">']
for k, (t, cls) in enumerate(((P_ALTA, "f3"), (P_MEDIA, "f2"), (P_BAIXA, "f0"))):
    ch.append(f'          <rect class="{cls}" x="{X0 + k * 110}" y="12" width="14" height="14"/><text x="{X0 + 22 + k * 110}" y="24">{t}</text>')
ch.append('        </g>')
for v in range(0, 7):
    ch.append(f'        <line class="{"ln" if v == 0 else "grid"}" x1="{px(v):.1f}" y1="{TOP - 6}" x2="{px(v):.1f}" y2="{bottom}"/>')
    ch.append(f'        <text class="mu" x="{px(v):.1f}" y="{bottom + 16}" font-size="11"{MID}{TNUM}>{v}</text>')
ch.append(f'        <text class="mono mu" x="{(X0 + X1) / 2}" y="{bottom + 36}" font-size="10"{MID}>PONTOS DE LACUNA · IMPACTO × LACUNA</text>')
hits = []
for k, row in enumerate(rows_c):
    y = TOP + RH * k
    if row[0] == "grupo":
        ch.append(f'        <text class="mono mu" x="20" y="{y + 16}" font-size="10">{row[1]}</text>')
        continue
    m, d = row[1]
    v, p = prioridade_pts(m, d["sit"]), prioridade(m, d["sit"])
    ch.append(f'        <text x="36" y="{y + 16}" font-size="11"><tspan class="b">{m[0]}</tspan><tspan dx="8">{escape(m[2])}</tspan></text>')
    if v:
        ch.append(f'        <rect class="bar {PCOR[p]}" data-k="{k}" x="{X0}" y="{y + 5}" width="{px(v) - X0:.1f}" height="{RH - 10}"/>')
    ch.append(f'        <text class="mu halo" x="{px(v) + 8:.1f}" y="{y + 16}" font-size="10.5"{TNUM}>{v if v else "sem lacuna"}</text>')
    hits.append(f'        <rect class="hit" x="14" y="{y}" width="872" height="{RH}" tabindex="0" role="img" aria-label="{m[0]}, {escape(m[2])}: {d["sit"].lower()}, {v} pontos" '
                f'data-k="{k}" data-n="{m[0]} · {escape(m[2])}" data-s="{p}" data-d="{v} pontos" data-p="{d["sit"].lower()}" data-cx="{px(v):.1f}" data-cy="{y}"/>')
ch += hits + ["      </svg>"]
tb = ['        <table class="aud">', '          <thead><tr><th>Organização</th><th>Mudança</th><th>Situação</th><th class="c">Pontos</th><th>Prioridade</th></tr></thead>', '          <tbody>']
for row in rows_c:
    if row[0] == "m":
        m, d = row[1]
        tb.append(f'            <tr><td>{"Pizzaria" if row[2] is EX1 else "Indústria"}</td><td>{m[0]} · {escape(m[2])}</td><td>{d["sit"]}</td>'
                  f'<td class="c">{prioridade_pts(m, d["sit"])}</td><td>{prioridade(m, d["sit"])}</td></tr>')
tb += ['          </tbody>', '        </table>']

# ------------------------------------------------------------------ módulo 1: a tabela das mudanças
mt = ['  <div class="tbl">', '    <table>', '      <thead><tr><th style="width:7%">Código</th><th style="width:22%">Mudança<small>Onde</small></th><th style="width:14%">Tipo · impacto</th>'
      '<th>O que mudou, em resumo</th><th style="width:16%">Estudo da série</th></tr></thead>', '      <tbody>']
for m in MUDANCAS:
    mt.append(f'        <tr><td class="num">{m[0]}</td><td><strong>{escape(m[2])}</strong><br><small>{m[1]}</small></td><td>{m[3]}<br><small>impacto {m[4].lower()}</small></td>'
              f'<td>{escape(m[5])}</td><td><a href="{LINKS[m[8]]}">{NOMES[m[8]]}</a></td></tr>')
mt += ['      </tbody>', '    </table>', '  </div>']
perg = "\n".join(f'        <tr><td class="num">{m[0]}</td><td><strong>{escape(m[2])}</strong></td><td>{escape(m[6])}</td><td>{escape(m[7])}</td></tr>' for m in MUDANCAS)

# ------------------------------------------------------------------ módulo 12: figura das normas
ISOP = [("Publicação", "A ISO 9001:2026 foi publicada em 16/09/2026 e substitui a edição de 2015.", "o mapa das mudanças"),
        ("Transição", "Certificados de 2015 valem até 30/09/2029; certificados novos, só pela de 2026 desde 31/03/2028.", "o plano de transição"),
        ("Global ACI", "Desde 2026, a cooperação de acreditação que fixa as regras de transição para os organismos.", "as datas"),
        ("ISO 9000:2026", "A norma de vocabulário revisada, de onde vêm os termos que entraram na ISO 9001.", "os termos")]
iso = ['      <svg viewBox="0 0 900 200" role="img" aria-label="As referências da edição nova. ' + " ".join(f"{a}: {b} Neste estudo: {c}." for a, b, c in ISOP) + '">']
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
for tag, val in (("<!--MAPA-->", "\n".join(ma)), ("<!--MUDANCAS-->", "\n".join(mt)), ("<!--DATAS-->", "\n".join(tr)), ("<!--FLUXO-->", "\n".join(et)),
                 ("<!--CULTURA-->", "\n".join(cu)), ("<!--RISCOS-->", "\n".join(ro)), ("<!--NAOMUDOU-->", "\n".join(nm)), ("<!--PERGUNTAS-->", perg),
                 ("<!--EX1HEAD-->", ficha(EX1)), ("<!--EX1DIAG-->", diag_tab(EX1)), ("<!--EX1PLANO-->", plano_tab(EX1)),
                 ("<!--EX2HEAD-->", ficha(EX2)), ("<!--EX2DIAG-->", diag_tab(EX2)), ("<!--EX2PLANO-->", plano_tab(EX2)),
                 ("<!--EX3FIG-->", "\n".join(ex3)), ("<!--CHART-->", "\n".join(ch)), ("<!--CHARTTABLE-->", "\n".join(tb)),
                 ("<!--ISOFIG-->", "\n".join(iso)), ("<!--CHECK-->", check)):
    assert body.count(tag) == 1, tag
    body = body.replace(tag, val)
assert "<!--" not in body.replace("<!-- ====", ""), "marcador sem substituição"

head = src[: src.index("<style>")].replace("<title>PDCA na prática</title>", "<title>ISO 9001:2026: o que muda</title>")
assert "2026" in head
open(OUT, "w", encoding="utf-8").write(head + "<style>\n" + css + "</style>\n</head>\n" + body)
print("ok", OUT, "| figuras:", body.count("<figure"), "| módulos:", body.count('class="eyebrow">Módulo'), "| pizzaria", resumo(EX1), "| indústria", resumo(EX2))
