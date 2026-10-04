# -*- coding: utf-8 -*-
"""Gera Tecnica-Auditoria-modelo.xlsx no mesmo padrão visual das planilhas anteriores da série."""
import math
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
# funções de formatação compartilhadas com o gerador do PDCA (bloco inicial do arquivo)
_src = open(os.path.join(_here, "build_pdca.py"), encoding="utf-8").read()
exec(_src[: _src.index("STATUS = [")])

from openpyxl.chart import BarChart, Series  # noqa: E402
from openpyxl.chart.label import DataLabelList  # noqa: E402
from openpyxl.utils import get_column_letter as L  # noqa: E402
from tec_data import (ALTO, AM_SITS, BAIXO, BASE, CHECK, CONF, CONFORME, CONSTS, CRITERIOS, ESCALA, EQUIPE, EX1, EX2, FATOR, FORMACAO, FORTE, FRACA,  # noqa: E402
                      INCOMP, ISOL, LIDERAR, MEDIA, MEDIO, MIN_OBS, MINIMO, NC, OM, POUCO, REPET, RISCOS, SEMCORR)

BLUE, TEAL, AMBER, PURPLE, REDC = "2B5C8A", "1E7B73", "A96A12", "7A4A9A", "B0413E"
S2_T = "F8EBCB"
YESNO = ["Sim", "Parcial", "Não"]
YESNO_CF = [("Sim", GREEN), ("Parcial", YELLOW), ("Não", RED)]
NA_, NE, NAUD = 30, 60, 4
A1, A2 = 12, 12 + NA_ - 1        # amostras
E1, E2 = 7, 7 + NE - 1           # evidências
K1, K2 = 8, 8 + len(CRITERIOS) - 1   # critérios do auditor
AUDC = [L(6 + k) for k in range(NAUD)]   # F..I
EPS = "0.000000001"
AM_CF = [(CONF, GREEN), (ISOL, S2_T), (INCOMP, S2_T), (REPET, RED)]
EV_CF = [(FORTE, GREEN), (MEDIA, S2_T), (FRACA, RED)]
NV_CF = [(LIDERAR, GREEN), (EQUIPE, S2_T), (FORMACAO, RED), (POUCO, GRAY)]


def note(ws, ref, text):
    c = Comment(text, "Modelo Técnica de auditoria")
    c.width, c.height = 300, 120
    ws[ref].comment = c


def cf_warn(ws, rng_, first, ok_values=("OK",)):
    cond = ",".join(f'{first}="{v}"' for v in ok_values)
    ws.conditional_formatting.add(rng_, FormulaRule(formula=[f"OR({cond})"], fill=PatternFill("solid", bgColor=GREEN, fgColor=GREEN)))
    ws.conditional_formatting.add(rng_, FormulaRule(formula=[f"AND(LEN({first})>0,NOT(OR({cond})))"],
                                  fill=PatternFill("solid", bgColor=YELLOW, fgColor=YELLOW)))


def cf_texto(ws, rng_, first, pares, resto=None):
    for t, cor in pares:
        ws.conditional_formatting.add(rng_, FormulaRule(formula=[f'{first}="{t}"'], stopIfTrue=True, fill=PatternFill("solid", bgColor=cor, fgColor=cor)))
    if resto:
        ws.conditional_formatting.add(rng_, FormulaRule(formula=[f"LEN({first})>0"], fill=PatternFill("solid", bgColor=resto, fgColor=resto)))


def hint_row(ws, row, cells, height=30):
    for ref, text in cells:
        put(ws, f"{ref}{row}", text, f=font(9, i=True, c=MUTED), bg=GRAY, h="center")
    ws.row_dimensions[row].height = height


def alt(pares, minimo=21.75, linha=12):
    n = max(max(1, math.ceil(len(str(t or "")) / max(c, 1))) for t, c in pares)
    return max(minimo, n * linha + 7)


def dv_whole(ws, rng, a, b, msg):
    dv = DataValidation(type="whole", operator="between", formula1=str(a), formula2=str(b), allow_blank=True)
    dv.errorTitle, dv.error = "Valor inválido", msg
    dv.showErrorMessage = True
    ws.add_data_validation(dv)
    dv.add(rng)


# ------------------------------------------------------------------ fórmulas: amostras (colunas iguais na aba e nos exemplos)
def f_base(pop):
    faixas = [(ate, b) for ate, b in BASE if ate is not None and b is not None]
    expr = str(BASE[-1][1])
    for ate, b in reversed(faixas):
        expr = f"IF({pop}<={ate},{b},{expr})"
    return expr


def f_fator(risco):
    return f'IF({risco}="{ALTO}",{FATOR[ALTO]},IF({risco}="{MEDIO}",{FATOR[MEDIO]},IF({risco}="{BAIXO}",{FATOR[BAIXO]},"")))'


def f_n(r):
    return (f'IF(OR(N(F{r})=0,G{r}=""),"",IF(F{r}<={BASE[0][0]},F{r},IFERROR(MIN(F{r},MAX({MINIMO},ROUNDUP({f_base(f"F{r}")}*{f_fator(f"G{r}")}-{EPS},0))),"")))')


def f_passo(r):
    return f'IF(I{r}="","",INT(F{r}/I{r}))'


def f_amsit(r):
    return f'IF(OR(I{r}="",K{r}="",L{r}=""),"",IF(K{r}<I{r},"{INCOMP}",IF(L{r}=0,"{CONF}",IF(L{r}=1,"{ISOL}","{REPET}"))))'


def f_amconf(r):
    return (f'IF(C{r}="","",IF(N(F{r})=0,"Falta a população",IF(G{r}="","Falta o risco",IF(OR(H{r}="",H{r}<1,H{r}>J{r}),"Início deve ir de 1 a "&J{r},'
            f'IF(K{r}="","Falta quantos foram verificados",IF(K{r}>F{r},"Verificados acima da população",IF(L{r}="","Falta quantos desvios",'
            f'IF(L{r}>K{r},"Mais desvios que verificados","OK"))))))))')


def am_formulas(ws, r):
    calc(ws, f"I{r}", "=" + f_n(r))
    calc(ws, f"J{r}", "=" + f_passo(r), b=False)
    calc(ws, f"N{r}", "=" + f_amsit(r), sz=9)
    calc(ws, f"O{r}", "=" + f_amconf(r), b=False, sz=9)


# ------------------------------------------------------------------ fórmulas: evidências (C pergunta, D requisito, E a G fontes, H constatação)
def f_fontes(r):
    return f'IF(AND(C{r}="",D{r}=""),"",COUNTA(E{r}:G{r}))'


def f_forca(r):
    return f'IF(N(I{r})=0,"",IF(I{r}>=2,"{FORTE}",IF(OR(F{r}<>"",G{r}<>""),"{MEDIA}","{FRACA}")))'


def f_evconf(r):
    return (f'IF(AND(C{r}="",D{r}="",COUNTA(E{r}:H{r})=0),"",IF(D{r}="","Falta o requisito",IF(C{r}="","Falta a pergunta",IF(N(I{r})=0,"Falta a evidência",'
            f'IF(H{r}="","Falta a constatação",IF(AND(H{r}="{NC}",J{r}="{FRACA}"),"{SEMCORR}","OK"))))))')


def ev_formulas(ws, r, merge=None):
    calc(ws, f"I{r}", "=" + f_fontes(r))
    calc(ws, f"J{r}", "=" + f_forca(r), sz=9)
    calc(ws, f"K{r}", "=" + f_evconf(r), b=False, sz=9, merge=merge)


# ------------------------------------------------------------------ fórmulas: auditores (critérios nas linhas k1..k2, crítico na coluna E)
def aud_formulas(ws, col, nome, k1, k2, r):
    """r: primeira das cinco linhas de resultado (observados, pontos, percentual, nível, conferência)."""
    rng = f"{col}{k1}:{col}{k2}"
    calc(ws, f"{col}{r}", f'=IF({nome}="","",COUNT({rng}))', b=False)
    calc(ws, f"{col}{r + 1}", f'=IF({nome}="","",SUM({rng}))', b=False)
    calc(ws, f"{col}{r + 2}", f'=IF(OR({nome}="",N({col}{r})=0),"",{col}{r + 1}/(3*{col}{r}))', fmt="0%")
    calc(ws, f"{col}{r + 3}", f'=IF({nome}="","",IF({col}{r}=0,"",IF({col}{r}<{MIN_OBS},"{POUCO}",'
                              f'IF(SUMPRODUCT(($E${k1}:$E${k2}="Sim")*({rng}<>"")*({rng}<=1))>0,"{FORMACAO}",'
                              f'IF({col}{r + 2}>=0.8-{EPS},"{LIDERAR}",IF({col}{r + 2}>=0.6-{EPS},"{EQUIPE}","{FORMACAO}"))))))', sz=9)
    calc(ws, f"{col}{r + 4}", f'=IF({nome}="",IF(COUNT({rng})>0,"Falta o nome",""),IF({col}{r}=0,"Faltam as notas",IF({col}{r}<{MIN_OBS},"Observar mais critérios","OK")))',
         b=False, sz=9)


def criterios(ws, k1):
    for k, (etapa, crit, critico) in enumerate(CRITERIOS):
        rr = k1 + k
        num(ws, f"B{rr}", k + 1)
        put(ws, f"C{rr}", crit, bg=GRAY, f=font(9))
        put(ws, f"D{rr}", etapa, bg=GRAY, f=font(9), h="center")
        put(ws, f"E{rr}", "Sim" if critico else "—", bg=GRAY, f=font(9, critico), h="center")
        ws.row_dimensions[rr].height = 30


def chart_style(ch):
    ch.style = 2
    ch.title = None
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill="D3DBE0", w=9525))
    ch.x_axis.graphicalProperties = GraphicalProperties(ln=LineProperties(solidFill="D3DBE0", w=9525))
    ch.y_axis.graphicalProperties = GraphicalProperties(ln=LineProperties(noFill=True))


def colunas(ws, anchor, r1, r2, c_cat, c_val, width=16, height=7.5):
    ch = BarChart()
    ch.type = "col"
    ch.gapWidth = 70
    ch.height, ch.width = height, width
    chart_style(ch)
    ch.legend = None
    s = Series(Reference(ws, min_col=c_val, min_row=r1, max_row=r2), title="Amostras")
    s.graphicalProperties.solidFill = BLUE
    s.graphicalProperties.line.noFill = True
    s.dLbls = DataLabelList()
    s.dLbls.showVal = True
    s.dLbls.showSerName = s.dLbls.showCatName = s.dLbls.showLegendKey = False
    ch.append(s)
    ch.set_categories(Reference(ws, min_col=c_cat, min_row=r1, max_row=r2))
    ch.y_axis.scaling.min = 0
    ch.y_axis.majorUnit = 1
    ws.add_chart(ch, anchor)


def resumo_aba(ws, s, itens, last, merge_lab="D"):
    band(ws, s, "Resumo automático", last)
    col = chr(ord(merge_lab) + 1)
    for k, (text, formula) in enumerate(itens, 1):
        aviso = text == "Aviso"
        label(ws, f"B{s+k}", text, merge=f"B{s+k}:{merge_lab}{s+k}", h="right")
        calc(ws, f"{col}{s+k}", formula, merge=f"{col}{s+k}:{last}{s+k}", sz=9 if aviso else 10, b=not aviso, h="left")
        ws.row_dimensions[s + k].height = 21.75
    av = s + len(itens)
    cf_warn(ws, f"{col}{av}:{last}{av}", f"{col}{av}")
    return av


def conta_por(rng, valores):
    return "=" + '&", "&'.join(f'COUNTIF({rng},"{x}")&" {x.lower()}"' for x in valores)


AM_W = {"A": 2, "B": 5, "C": 36, "D": 10, "E": 22, "F": 11, "G": 10, "H": 9, "I": 10, "J": 9, "K": 11, "L": 9, "M": 32, "N": 22, "O": 28, "P": 2}

# ================================================================== pasta de trabalho
wb = Workbook()
wb.properties.title = "Técnica de auditoria — Modelo"
wb.properties.creator = "Modelo Técnica de auditoria"
wb.properties.language = "pt-BR"

# ------------------------------------------------------------------ Instruções
ws = wb.active
ws.title = "Instruções"
widths(ws, {"A": 2, "B": 26, "C": 90, "D": 2})
title(ws, "Técnica de auditoria — Como usar esta planilha", "Modelo para dimensionar as amostras, pesar as evidências e avaliar os auditores em campo.", "C")
r = 4


def section(text):
    global r
    band(ws, r, text, "C", sz=11)
    r += 1


def line(k, v, kbg=GRAY, vbg=None, kf=None, kh="left", height=None):
    global r
    put(ws, f"B{r}", k, f=kf or font(10, True), bg=kbg, h=kh)
    put(ws, f"C{r}", v, bg=vbg)
    ws.row_dimensions[r].height = height or (19.5 if len(v) <= 96 else (31.5 if len(v) <= 192 else 45.75))
    r += 1


section("Legenda: onde preencher")
line("Amarelo-claro", "Células de entrada. É aqui que você digita.", vbg=INPUT)
line("Cinza", "Células calculadas ou fixas (amostra, passo, conclusão, fontes, força, nível, conferências). Não altere.", vbg=GRAY)
line("Cinza em itálico", "Linha de exemplo (marcada com “Ex.”). Mostra o formato esperado e não entra nas contagens.", vbg=GRAY)
line("Listas suspensas", "Risco, constatação e checklist aceitam apenas as opções da lista. As notas aceitam de 0 a 3.")
line("Comentários", "Células com triângulo vermelho no canto trazem uma dica de preenchimento. Passe o mouse sobre elas.")
r += 1
section("O tamanho da amostra")
ant = 0
for ate, b in BASE:
    faixa = f"Até {ate}" if ant == 0 else (f"De {ant + 1} a {ate}" if ate else f"Acima de {ant}")
    txt = "Todos os casos." if b is None else f"Amostra-base de {b}. Risco alto: {max(MINIMO, math.ceil(b * FATOR[ALTO] - 1e-9))}. Médio: {b}. Baixo: {max(MINIMO, math.ceil(b * FATOR[BAIXO] - 1e-9))}."
    line(f"População {faixa.lower()}", txt)
    ant = ate or ant
line("Regra", f"A amostra-base vezes o fator de risco (alto {FATOR[ALTO]}, médio {FATOR[MEDIO]}, baixo {FATOR[BAIXO]}), arredondada para cima, com mínimo de {MINIMO} e máximo igual à população.".replace(".5", ",5").replace("0.6", "0,6"))
line("Passo e início", "O passo é a população dividida pela amostra. O auditor sorteia o início entre 1 e o passo e verifica um caso a cada passo.")
r += 1
section("As outras regras de cálculo")
for k, text in [
    (CONF, "Amostra completa, sem desvio."),
    (ISOL, "Amostra completa, com um desvio. Já é não conformidade; amplie a amostra para saber se é pontual ou repetido."),
    (REPET, "Amostra completa, com dois desvios ou mais."),
    (INCOMP, "Menos verificados do que a amostra calculada."),
    ("Força da evidência", f"{FORTE}: duas fontes ou mais. {MEDIA}: só observação ou só registro. {FRACA}: só entrevista. Não conformidade pede ao menos uma fonte objetiva (força média ou forte); a que só tem entrevista pede corroboração."),
    ("Nível do auditor", f"Com pelo menos {MIN_OBS} critérios observados: 80% ou mais, {LIDERAR.lower()}; de 60% a 79%, {EQUIPE.lower()}; abaixo, {FORMACAO.lower()}. "
                         "Um critério crítico com nota 0 ou 1 leva a em formação."),
    ("Notas", " ".join(f"{n}: {t.lower()}." for n, t in ESCALA) + " Em branco: não observado."),
]:
    line(k, text)
r += 1
section("Ordem recomendada de preenchimento")
for k, text in enumerate([
    "Aba Amostras: os dados da auditoria e, para cada registro a verificar, a população e o risco. Sorteie o início entre 1 e o passo.",
    "Aba Amostras, durante a auditoria: quantos foram verificados e quantos desvios.",
    "Aba Evidências: cada pergunta, o requisito, as fontes e a constatação.",
    "Aba Auditores, se houver observador: o nome, o papel e as notas de cada auditor.",
    "Aba Painel: leia os avisos. Depois, valide na aba Checklist.",
], 1):
    line(f"Passo {k}", text)
r += 1
section("Abas da planilha")
for k, text in [
    ("Amostras", f"Os dados da auditoria e até {NA_} amostras. Calcula o tamanho, o passo, a conclusão e a conferência."),
    ("Evidências", f"Até {NE} perguntas. Calcula as fontes, a força e a conferência."),
    ("Auditores", f"Até {NAUD} auditores, com notas nos {len(CRITERIOS)} critérios. Calcula os pontos, o percentual, o nível e a conferência."),
    ("Painel", "Os números das três abas, o gráfico das amostras e o aviso."),
    ("Checklist", "Doze verificações da técnica de auditoria, com percentual de conclusão."),
    ("Exemplo 1 - Pizzaria", "A auditoria do salão e do recebimento, em 18/03/2027."),
    ("Exemplo 2 - Indústria", "A auditoria da produção, em 06/10/2027."),
]:
    line(k, text)
r += 1
section("Premissas do modelo")
for k, text in [
    ("Convenção", "A ISO 19011 descreve a amostragem por julgamento e a estatística, mas não fixa tamanhos. A tabela, a força e os níveis são uma convenção deste material."),
    ("Exemplos", "Os dados das abas de exemplo são ilustrativos, criados para este material."),
]:
    line(k, text)
setup(ws, INK, f"B1:C{r}", landscape=False, fit_height=True)

# ------------------------------------------------------------------ Amostras
ws = wb.create_sheet("Amostras")
widths(ws, AM_W)
title(ws, "Amostras da auditoria", "Uma amostra por linha: o que se verifica, de que população, com que risco. O tamanho e o passo saem da tabela.", "O")
for rr, text in [(4, "Auditoria nº"), (5, "Processo auditado"), (6, "Data"), (7, "Auditor líder")]:
    label(ws, f"B{rr}", text, merge=f"B{rr}:C{rr}")
    inp(ws, f"D{rr}", merge=f"D{rr}:G{rr}", h="center" if rr in (4, 6) else "left", fmt=DATE if rr == 6 else None)
dv_date(ws, "D6")
for col, text in zip("BCDEFGHIJKLMNO", ["#", "O que se verifica", "Requisito", "Período", "População", "Risco", "Início", "Amostra", "Passo", "Verificados", "Desvios",
                                        "Observação", "Conclusão", "Conferência"]):
    head(ws, f"{col}9", text)
ws.row_dimensions[9].height = 33
hint_row(ws, 10, [("B", ""), ("C", "Registro e o que conferir"), ("D", "Ex.: 8.4"), ("E", ""), ("F", "Quantos existem"), ("G", "Lista"), ("H", "Sorteado"), ("I", "Calculada"),
                  ("J", "Calculado"), ("K", "Número"), ("L", "Número"), ("M", "O que se viu"), ("N", "Calculada"), ("O", "Calculada")])
ex(ws, "B11", "Ex.", h="center")
for col, v, h_ in [("C", "Notas de recebimento com a temperatura", "left"), ("D", "8.4", "center"), ("E", "Fevereiro", "left"), ("F", 48, "center"), ("G", ALTO, "center"),
                   ("H", 3, "center"), ("I", 12, "center"), ("J", 4, "center"), ("K", 12, "center"), ("L", 0, "center"), ("M", "", "left"), ("N", CONF, "center"), ("O", "OK", "center")]:
    ex(ws, f"{col}11", v, h=h_)
ws.row_dimensions[11].height = 21.75
for k in range(NA_):
    rr = A1 + k
    num(ws, f"B{rr}", k + 1)
    for col in "CEM":
        inp(ws, f"{col}{rr}")
    for col in "DG":
        inp(ws, f"{col}{rr}", h="center")
    for col in "FHKL":
        inp(ws, f"{col}{rr}", h="center", fmt="#,##0")
    am_formulas(ws, rr)
    ws.row_dimensions[rr].height = 21.75
dv_list(ws, f"G{A1}:G{A2}", RISCOS, "Alto, médio ou baixo: o quanto um desvio nesse registro afeta o produto ou o cliente")
dv_whole(ws, f"F{A1}:F{A2}", 1, 1000000000, "Digite quantos registros existem na população.")
dv_whole(ws, f"H{A1}:H{A2}", 1, 1000000, "Digite o número sorteado, entre 1 e o passo.")
dv_whole(ws, f"K{A1}:L{A2}", 0, 1000000000, "Digite um número inteiro.")
cf_texto(ws, f"N{A1}:N{A2}", f"N{A1}", AM_CF)
cf_warn(ws, f"O{A1}:O{A2}", f"O{A1}")
note(ws, "F9", "Quantos registros existem no período: todas as comandas de fevereiro, todas as notas de recebimento, todos os instrumentos do posto.")
note(ws, "H9", "Sorteie um número entre 1 e o passo, com um dado ou um sorteio no celular. Depois verifique um caso a cada passo, a partir dele.")
s = A2 + 2
N_ = f"N{A1}:N{A2}"
AAV = resumo_aba(ws, s, [
    ("Amostras", f'=COUNTA(C{A1}:C{A2})&" amostras, "&SUM(K{A1}:K{A2})&" registros verificados, "&SUM(L{A1}:L{A2})&" desvios"'),
    ("Conclusões", conta_por(N_, AM_SITS)),
    ("Aviso", f'=IF(COUNTA(C{A1}:C{A2})=0,"Liste as amostras da auditoria",IF(COUNTIF({N_},"{ISOL}")>0,"Há desvio pontual: amplie a amostra para medir a extensão",'
              f'IF(COUNTIF({N_},"{INCOMP}")>0,"Há amostra incompleta: complete ou registre por quê",'
              f'IF(SUMPRODUCT((O{A1}:O{A2}<>"")*(O{A1}:O{A2}<>"OK"))>0,"Há amostra a completar: veja a coluna Conferência","OK"))))'),
], "O")
ws.freeze_panes = f"D{A1}"
setup(ws, BLUE, f"B1:O{AAV}")

# ------------------------------------------------------------------ Evidências
ws = wb.create_sheet("Evidências")
widths(ws, {"A": 2, "B": 5, "C": 40, "D": 10, "E": 30, "F": 30, "G": 34, "H": 22, "I": 8, "J": 10, "K": 30, "L": 2})
title(ws, "Evidências", "Uma pergunta por linha, com as três fontes possíveis e a constatação. A força sai do número e do tipo de fontes.", "K")
for col, text in zip("BCDEFGHIJK", ["#", "Pergunta", "Requisito", "Entrevista", "Observação", "Registro", "Constatação", "Fontes", "Força", "Conferência"]):
    head(ws, f"{col}4", text)
ws.row_dimensions[4].height = 33
hint_row(ws, 5, [("B", ""), ("C", "Aberta"), ("D", "Ex.: 7.1.5"), ("E", "Quem disse o quê"), ("F", "O que o auditor viu"), ("G", "Qual registro, com a amostra"),
                 ("H", "Lista"), ("I", "Calculado"), ("J", "Calculada"), ("K", "Calculada")])
ex(ws, "B6", "Ex.", h="center")
for col, v, h_ in [("C", "Como o recebimento confere a temperatura?", "left"), ("D", "8.4", "center"), ("E", "Atendente que recebe", "left"),
                   ("F", "Recebimento das 15h: temperatura anotada", "left"), ("G", "12 notas de fevereiro com a temperatura", "left"), ("H", CONFORME, "center"),
                   ("I", 3, "center"), ("J", FORTE, "center"), ("K", "OK", "center")]:
    ex(ws, f"{col}6", v, h=h_)
ws.row_dimensions[6].height = 30
for k in range(NE):
    rr = E1 + k
    num(ws, f"B{rr}", k + 1)
    for col in "CEFG":
        inp(ws, f"{col}{rr}")
    inp(ws, f"D{rr}", h="center")
    inp(ws, f"H{rr}", h="center")
    ev_formulas(ws, rr)
    ws.row_dimensions[rr].height = 30
dv_list(ws, f"H{E1}:H{E2}", CONSTS, "Conforme, não conformidade ou oportunidade de melhoria")
cf_texto(ws, f"J{E1}:J{E2}", f"J{E1}", EV_CF)
cf_texto(ws, f"H{E1}:H{E2}", f"H{E1}", [(CONFORME, GREEN), (NC, RED), (OM, S2_T)])
cf_texto(ws, f"K{E1}:K{E2}", f"K{E1}", [("OK", GREEN), (SEMCORR, RED)], resto=YELLOW)
note(ws, "G4", "O registro visto, com a amostra: “3 de 20 comandas de fevereiro sem horário”. Sem o tamanho, a evidência perde força.")
note(ws, "J4", f"{FORTE}: duas fontes ou mais. {MEDIA}: só observação ou só registro. {FRACA}: só entrevista.")
s = E2 + 2
H_ = f"H{E1}:H{E2}"
EAV = resumo_aba(ws, s, [
    ("Perguntas", f'=COUNTA(C{E1}:C{E2})&" perguntas: "&' + conta_por(H_, CONSTS)[1:]),
    ("Força", conta_por(f"J{E1}:J{E2}", (FORTE, MEDIA, FRACA))),
    ("Aviso", f'=IF(COUNTA(C{E1}:C{E2})=0,"Registre as perguntas e as evidências",IF(COUNTIF(K{E1}:K{E2},"{SEMCORR}")>0,"Há não conformidade sem evidência objetiva: busque registro ou observação",'
              f'IF(SUMPRODUCT((K{E1}:K{E2}<>"")*(K{E1}:K{E2}<>"OK"))>0,"Há pergunta a completar: veja a coluna Conferência","OK")))'),
], "K")
ws.freeze_panes = f"D{E1}"
setup(ws, TEAL, f"B1:K{EAV}")

# ------------------------------------------------------------------ Auditores
ws = wb.create_sheet("Auditores")
widths(ws, {"A": 2, "B": 5, "C": 60, "D": 14, "E": 9, "F": 20, "G": 20, "H": 20, "I": 20, "J": 2})
title(ws, "Avaliação dos auditores em campo", "Uma coluna por auditor observado. Notas de 0 a 3; em branco, não observado.", "I")
label(ws, "B5", "Auditor", merge="B5:E5", h="right")
label(ws, "B6", "Papel na auditoria", merge="B6:E6", h="right")
for c in AUDC:
    inp(ws, f"{c}5", h="center")
    inp(ws, f"{c}6", h="center")
for col, text in zip("BCDE", ["#", "Critério", "Etapa", "Crítico"]):
    head(ws, f"{col}7", text)
for k, c in enumerate(AUDC):
    head(ws, f"{c}7", f"Auditor {k + 1}")
ws.row_dimensions[7].height = 21.75
criterios(ws, K1)
for c in AUDC:
    for rr in range(K1, K2 + 1):
        inp(ws, f"{c}{rr}", h="center")
dv_whole(ws, f"{AUDC[0]}{K1}:{AUDC[-1]}{K2}", 0, 3, "Digite uma nota de 0 a 3, ou deixe em branco se não observou.")
RS = K2 + 2
for k, t in enumerate(["Critérios observados", "Pontos", "Percentual", "Nível", "Conferência"]):
    label(ws, f"B{RS + k}", t, merge=f"B{RS + k}:E{RS + k}", h="right")
    ws.row_dimensions[RS + k].height = 21.75
for c in AUDC:
    aud_formulas(ws, c, f"{c}$5", K1, K2, RS)
cf_texto(ws, f"{AUDC[0]}{RS + 3}:{AUDC[-1]}{RS + 3}", f"{AUDC[0]}{RS + 3}", NV_CF)
cf_warn(ws, f"{AUDC[0]}{RS + 4}:{AUDC[-1]}{RS + 4}", f"{AUDC[0]}{RS + 4}")
ws.conditional_formatting.add(f"{AUDC[0]}{K1}:{AUDC[-1]}{K2}", FormulaRule(formula=[f'AND($E{K1}="Sim",{AUDC[0]}{K1}<>"",{AUDC[0]}{K1}<=1)'],
                              fill=PatternFill("solid", bgColor=RED, fgColor=RED)))
note(ws, "E7", "Um critério crítico com nota 0 ou 1 deixa o auditor em formação, qualquer que seja o percentual.")
note(ws, f"{AUDC[0]}7", " ".join(f"{n}: {t.lower()}." for n, t in ESCALA) + " Em branco: não observado.")
s = RS + 6
UAV = resumo_aba(ws, s, [
    ("Auditores avaliados", f'=COUNTA({AUDC[0]}5:{AUDC[-1]}5)'),
    ("Por nível", conta_por(f"{AUDC[0]}{RS + 3}:{AUDC[-1]}{RS + 3}", (LIDERAR, EQUIPE, FORMACAO, POUCO))),
    ("Aviso", f'=IF(F{s+1}=0,"Informe os auditores observados",IF(SUMPRODUCT(({AUDC[0]}{RS + 4}:{AUDC[-1]}{RS + 4}<>"")*({AUDC[0]}{RS + 4}:{AUDC[-1]}{RS + 4}<>"OK"))>0,'
              f'"Há auditor a completar: veja a linha Conferência",IF(COUNTIF({AUDC[0]}{RS + 3}:{AUDC[-1]}{RS + 3},"{FORMACAO}")>0,"Há auditor em formação: planeje o acompanhamento","OK")))'),
], "I", merge_lab="E")
setup(ws, PURPLE, f"B1:I{UAV}", landscape=False, fit_height=True)

# ------------------------------------------------------------------ Painel
ws = wb.create_sheet("Painel")
widths(ws, {"A": 2, "B": 38, "C": 14, "D": 14, "E": 14, "F": 34, "G": 2})
title(ws, "Painel da técnica de auditoria", "Nada a preencher: tudo vem das outras abas.", "F")
label(ws, "B3", "Auditoria")
calc(ws, "C3", '=IF(Amostras!D4="","",Amostras!D4&IF(Amostras!D5="",""," · "&Amostras!D5))', merge="C3:F3", h="left")
for col, text, m in [("B", "Indicador", None), ("C", "Resultado", None), ("D", "Como se lê", "D5:F5")]:
    put(ws, f"{col}5", text, f=font(10, True, c=WHITE), bg=INK, h="center", merge=m)
ws.row_dimensions[5].height = 21.75
An, Ao, Ak, Al = (f"Amostras!{c}{A1}:{c}{A2}" for c in "NOKL")
Eh, Ej, Ek = (f"'Evidências'!{c}{E1}:{c}{E2}" for c in "HJK")
Un = f"Auditores!{AUDC[0]}{RS + 3}:{AUDC[-1]}{RS + 3}"
IND = [
    ("AMOSTRAS", None, None),
    ("Amostras", f"=COUNTA(Amostras!C{A1}:C{A2})", "Da aba Amostras."),
    ("Registros verificados", f"=SUM({Ak})", "A soma das amostras."),
    ("Desvios", f"=SUM({Al})", "Em todas as amostras."),
    (CONF, f'=COUNTIF({An},"{CONF}")', "Amostras sem desvio."),
    ("Desvio pontual", f'=COUNTIF({An},"{ISOL}")', "Não conformidade; ampliar para medir a extensão."),
    ("Desvio repetido", f'=COUNTIF({An},"{REPET}")', "Não conformidade sustentada."),
    (INCOMP, f'=COUNTIF({An},"{INCOMP}")', "Completar ou registrar por quê."),
    ("EVIDÊNCIAS", None, None),
    ("Perguntas", f"=COUNTA('Evidências'!C{E1}:C{E2})", "Da aba Evidências."),
    ("Não conformidades", f'=COUNTIF({Eh},"{NC}")', "Constatações de não conformidade."),
    ("Evidências fortes", f'=COUNTIF({Ej},"{FORTE}")', "Duas fontes ou mais."),
    ("Evidências fracas", f'=COUNTIF({Ej},"{FRACA}")', "Só entrevista."),
    ("Não conformidades sem evidência objetiva", f'=COUNTIF({Ek},"{SEMCORR}")', "Buscar registro ou observação antes do relatório."),
    ("AUDITORES", None, None),
    ("Auditores avaliados", f"=COUNTA(Auditores!{AUDC[0]}5:{AUDC[-1]}5)", "Da aba Auditores."),
    (LIDERAR, f'=COUNTIF({Un},"{LIDERAR}")', "Podem conduzir auditorias."),
    (EQUIPE, f'=COUNTIF({Un},"{EQUIPE}")', "Auditam com um líder."),
    (FORMACAO, f'=COUNTIF({Un},"{FORMACAO}")', "Acompanhamento até a próxima observação."),
    ("Linhas a completar", f'=SUMPRODUCT(({Ao}<>"")*({Ao}<>"OK"))+SUMPRODUCT(({Ek}<>"")*({Ek}<>"OK"))', "Conferências diferentes de OK nas amostras e nas evidências."),
]
IR = {}
rr = 6
for nome, formula, leit in IND:
    if formula is None:
        put(ws, f"B{rr}", nome, f=font(9, True, c=MUTED), bg=None, box=False, merge=f"B{rr}:F{rr}")
        ws.row_dimensions[rr].height = 21.75
        rr += 1
        continue
    label(ws, f"B{rr}", nome)
    calc(ws, f"C{rr}", formula)
    put(ws, f"D{rr}", leit, f=font(9, c=MUTED), bg=GRAY, merge=f"D{rr}:F{rr}")
    ws.row_dimensions[rr].height = 21.75
    IR[nome] = rr
    rr += 1
s = rr + 1
band(ws, s, "Resumo automático", "F")
label(ws, f"B{s+1}", "Aviso")
C = lambda n: f"C{IR[n]}"  # noqa: E731
calc(ws, f"C{s+1}", f'=IF({C("Amostras")}+{C("Perguntas")}=0,"Preencha as abas Amostras e Evidências",IF({C("Não conformidades sem evidência objetiva")}>0,"Há não conformidade sem evidência objetiva",'
     f'IF({C("Desvio pontual")}>0,"Há desvio pontual: amplie a amostra",IF({C(INCOMP)}>0,"Há amostra incompleta",'
     f'IF({C("Linhas a completar")}>0,"Há linha a completar: veja as conferências",IF({C(FORMACAO)}>0,"Há auditor em formação: planeje o acompanhamento","OK"))))))',
     merge=f"C{s+1}:F{s+1}", sz=9, b=False, h="left")
cf_warn(ws, f"C{s+1}:F{s+1}", f"C{s+1}")
ws.row_dimensions[s + 1].height = 21.75
NAV = s + 1
GS = s + 4
put(ws, f"B{GS - 1}", "Amostras por conclusão", f=font(9, True, c=MUTED), bg=None, box=False)
for k, sit in enumerate(AM_SITS):
    put(ws, f"B{GS + k}", sit, f=font(9), bg=GRAY)
    calc(ws, f"C{GS + k}", f'=COUNTIF({An},B{GS + k})', b=False)
colunas(ws, f"D{GS - 1}", GS, GS + len(AM_SITS) - 1, 2, 3, width=12, height=7)
setup(ws, REDC, f"B1:F{GS + 14}", landscape=False, fit_height=True)

# ------------------------------------------------------------------ Checklist
ws = wb.create_sheet("Checklist")
widths(ws, {"A": 2, "B": 5, "C": 70, "D": 14, "E": 44, "F": 2})
title(ws, "Checklist da técnica de auditoria", "Escolha o status de cada item na lista suspensa (coluna em amarelo-claro).", "E")
for col, text in zip("BCDE", ["#", "Item de verificação", "Status", "Observações"]):
    head(ws, f"{col}4", text)
ws.row_dimensions[4].height = 21.75
for k, text in enumerate(CHECK):
    rr = 5 + k
    num(ws, f"B{rr}", k + 1)
    put(ws, f"C{rr}", text, bg=GRAY)
    inp(ws, f"D{rr}", h="center")
    inp(ws, f"E{rr}")
    ws.row_dimensions[rr].height = 30
dv_list(ws, "D5:D16", YESNO, "Sim, Parcial ou Não")
cf_equal(ws, "D5:D16", YESNO_CF)
band(ws, 18, "Resumo automático", "E")
summary(ws, 19, "Itens atendidos (Sim)", '=COUNTIF(D5:D16,"Sim")', "C", "D")
summary(ws, 20, "Itens parciais", '=COUNTIF(D5:D16,"Parcial")', "C", "D")
summary(ws, 21, "Itens não atendidos", '=COUNTIF(D5:D16,"Não")', "C", "D")
summary(ws, 22, "Itens sem resposta", "=COUNTBLANK(D5:D16)", "C", "D")
summary(ws, 23, "Percentual atendido", "=D19/ROWS(D5:D16)", "C", "D", fmt="0%")
summary(ws, 24, "Situação", '=IF(D19=ROWS(D5:D16),"Validado",IF(D22>0,"Em andamento","Com pendências"))', "C", "D")
setup(ws, PURPLE, "B1:E24", landscape=False, fit_height=True)


# ------------------------------------------------------------------ Exemplos
def sub(ws, rr, cells, height=30):
    for a, b, t in cells:
        put(ws, f"{a}{rr}", t, f=font(10, True), bg=GRAY, h="center", merge=b and f"{a}{rr}:{b}{rr}")
    ws.row_dimensions[rr].height = height


def exemplo(ws, ex_):
    H = ex_["head"]
    widths(ws, AM_W)
    widths(ws, {"F": 15, "G": 15, "H": 15})  # as notas dos auditores ficam nestas colunas
    title(ws, "Técnica de auditoria", "Exemplo preenchido, para consulta. Use as abas Amostras, Evidências e Auditores para a sua auditoria.", "O")
    rr = 4
    for rot, val in [("Auditoria", f'{H["num"]} · {H["processo"]}'), ("Organização", H["org"]), ("Auditor líder", H["lider"]), ("Equipe", H["equipe"]),
                     ("Observador", H["observador"]), ("Critérios", H["criterios"])]:
        label(ws, f"B{rr}", rot, merge=f"B{rr}:C{rr}")
        inp(ws, f"D{rr}", val, merge=f"D{rr}:O{rr}", bg=WHITE, h="left")
        ws.row_dimensions[rr].height = 19.5
        rr += 1
    label(ws, f"B{rr}", "Data", merge=f"B{rr}:C{rr}")
    inp(ws, f"D{rr}", H["data"], bg=WHITE, h="center", fmt=DATE)

    # ---- amostras (mesmas colunas da aba Amostras)
    rr += 2
    band(ws, rr, "Amostras", "O", color=BLUE)
    rr += 1
    sub(ws, rr, [(c, None, t) for c, t in zip("BCDEFGHIJKLMNO", ["#", "O que se verifica", "Requisito", "Período", "População", "Risco", "Início", "Amostra", "Passo",
                                                                  "Verificados", "Desvios", "Observação", "Conclusão", "Conferência"])])
    a1 = rr + 1
    for k, a in enumerate(ex_["ams"]):
        rr += 1
        num(ws, f"B{rr}", k + 1)
        put(ws, f"C{rr}", a["oque"], f=font(10, True))
        put(ws, f"D{rr}", a["req"], h="center")
        put(ws, f"E{rr}", a["periodo"], f=font(9))
        for col, key in (("F", "pop"), ("H", "inicio"), ("K", "verif"), ("L", "desv")):
            put(ws, f"{col}{rr}", a[key], h="center", fmt="#,##0")
        put(ws, f"G{rr}", a["risco"], h="center")
        put(ws, f"M{rr}", a["nota"] or None, f=font(9))
        am_formulas(ws, rr)
        ws.row_dimensions[rr].height = alt([(a["oque"], 36), (a["nota"], 34), (a["periodo"], 22)], minimo=21.75)
    a2 = rr
    cf_texto(ws, f"N{a1}:N{a2}", f"N{a1}", AM_CF)
    cf_warn(ws, f"O{a1}:O{a2}", f"O{a1}")

    # ---- evidências (C pergunta, D requisito, E a G fontes, H constatação, I fontes, J força, K a O conferência)
    rr += 2
    ws.row_breaks.append(Break(id=rr - 1))
    band(ws, rr, "Evidências", "O", color=TEAL)
    rr += 1
    sub(ws, rr, [("B", None, "#"), ("C", None, "Pergunta"), ("D", None, "Requisito"), ("E", None, "Entrevista"), ("F", "G", "Observação"), ("H", "J", "Registro"),
                 ("K", "L", "Constatação"), ("M", None, "Força"), ("N", "O", "Conferência")])
    # nos exemplos, as colunas são mais largas: as fórmulas usam um mapa próprio
    e1 = rr + 1
    for k, e in enumerate(ex_["evs"]):
        rr += 1
        num(ws, f"B{rr}", k + 1)
        put(ws, f"C{rr}", e["perg"], f=font(9, True))
        put(ws, f"D{rr}", e["req"], h="center")
        put(ws, f"E{rr}", e["ent"] or None, f=font(9))
        put(ws, f"F{rr}", e["obs"] or None, f=font(9), merge=f"F{rr}:G{rr}")
        put(ws, f"H{rr}", e["reg"] or None, f=font(9), merge=f"H{rr}:J{rr}")
        put(ws, f"K{rr}", e["const"] or None, h="center", f=font(9), merge=f"K{rr}:L{rr}")
        fontes = f'COUNTA(E{rr},F{rr},H{rr})'
        calc(ws, f"M{rr}", f'=IF({fontes}=0,"",IF({fontes}>=2,"{FORTE}",IF(OR(F{rr}<>"",H{rr}<>""),"{MEDIA}","{FRACA}")))', sz=9)
        calc(ws, f"N{rr}", f'=IF(D{rr}="","Falta o requisito",IF(C{rr}="","Falta a pergunta",IF({fontes}=0,"Falta a evidência",IF(K{rr}="","Falta a constatação",'
                           f'IF(AND(K{rr}="{NC}",M{rr}="{FRACA}"),"{SEMCORR}","OK")))))', b=False, sz=9, merge=f"N{rr}:O{rr}")
        ws.row_dimensions[rr].height = alt([(e["perg"], 36), (e["ent"], 24), (e["obs"], 34), (e["reg"], 46)], minimo=21.75)
    e2 = rr
    cf_texto(ws, f"M{e1}:M{e2}", f"M{e1}", EV_CF)
    cf_texto(ws, f"K{e1}:L{e2}", f"$K{e1}", [(CONFORME, GREEN), (NC, RED), (OM, S2_T)])
    cf_texto(ws, f"N{e1}:O{e2}", f"$N{e1}", [("OK", GREEN), (SEMCORR, RED)], resto=YELLOW)

    # ---- auditores (C critério, D etapa, E crítico, F em diante as notas)
    rr += 2
    ws.row_breaks.append(Break(id=rr - 1))
    band(ws, rr, "Avaliação dos auditores em campo", "O", color=PURPLE)
    rr += 1
    cols = [L(6 + k) for k in range(len(ex_["auds"]))]
    sub(ws, rr, [("B", None, "#"), ("C", None, "Critério"), ("D", None, "Etapa"), ("E", None, "Crítico")] + [(c, None, a["nome"]) for c, a in zip(cols, ex_["auds"])], height=42)
    rr += 1
    put(ws, f"B{rr}", "Papel", f=font(9, True), bg=GRAY, merge=f"B{rr}:E{rr}", h="right")
    for c, a in zip(cols, ex_["auds"]):
        put(ws, f"{c}{rr}", a["papel"], f=font(9), h="center")
    nome_row = rr - 1
    k1 = rr + 1
    criterios(ws, k1)
    for c, a in zip(cols, ex_["auds"]):
        for k, n in enumerate(a["notas"]):
            put(ws, f"{c}{k1 + k}", n, h="center")
    k2 = k1 + len(CRITERIOS) - 1
    rs = k2 + 1
    for k, t in enumerate(["Critérios observados", "Pontos", "Percentual", "Nível", "Conferência"]):
        label(ws, f"B{rs + k}", t, merge=f"B{rs + k}:E{rs + k}", h="right")
        ws.row_dimensions[rs + k].height = 21.75
    for c in cols:
        aud_formulas(ws, c, f"{c}${nome_row}", k1, k2, rs)
    ws.row_dimensions[rs + 3].height = 30
    cf_texto(ws, f"{cols[0]}{rs + 3}:{cols[-1]}{rs + 3}", f"{cols[0]}{rs + 3}", NV_CF)
    cf_warn(ws, f"{cols[0]}{rs + 4}:{cols[-1]}{rs + 4}", f"{cols[0]}{rs + 4}")
    ws.conditional_formatting.add(f"{cols[0]}{k1}:{cols[-1]}{k2}", FormulaRule(formula=[f'AND($E{k1}="Sim",{cols[0]}{k1}<>"",{cols[0]}{k1}<=1)'],
                                  fill=PatternFill("solid", bgColor=RED, fgColor=RED)))
    rr = rs + 4

    # ---- resumo
    rr += 2
    band(ws, rr, "Resumo automático", "O")
    for k, (text, formula) in enumerate([
        ("Amostras", f'=SUM(K{a1}:K{a2})&" registros verificados em "&COUNTA(C{a1}:C{a2})&" amostras, "&SUM(L{a1}:L{a2})&" desvios. "&' + conta_por(f"N{a1}:N{a2}", AM_SITS)[1:]),
        ("Evidências", conta_por(f"K{e1}:L{e2}", CONSTS) + '&". Força: "&' + conta_por(f"M{e1}:M{e2}", (FORTE, MEDIA, FRACA))[1:]),
        ("Auditores", conta_por(f"{cols[0]}{rs + 3}:{cols[-1]}{rs + 3}", (LIDERAR, EQUIPE, FORMACAO, POUCO))),
        ("Linhas a completar", f'=SUMPRODUCT((O{a1}:O{a2}<>"OK")*1)+SUMPRODUCT((N{e1}:N{e2}<>"OK")*1)'),
    ], 1):
        label(ws, f"B{rr+k}", text, merge=f"B{rr+k}:D{rr+k}", h="right")
        calc(ws, f"E{rr+k}", formula, merge=f"E{rr+k}:O{rr+k}", h="left")
        ws.row_dimensions[rr + k].height = 21.75
    setup(ws, MUTED, f"B1:O{rr + 4}")
    return dict(a=(a1, a2), e=(e1, e2), k=(k1, k2), rs=rs, cols=cols, res=rr + 1)


POS = {}
POS["ex1"] = exemplo(wb.create_sheet("Exemplo 1 - Pizzaria"), EX1)
POS["ex2"] = exemplo(wb.create_sheet("Exemplo 2 - Indústria"), EX2)

wb.active = 1
wb.save(OUT)
print("ok", OUT, "| avisos: Amostras E%d, Evidências E%d, Auditores F%d, Painel C%d | auditores RS %d | painel %s | exemplos %s" % (AAV, EAV, UAV, NAV, RS, IR, POS))
