# -*- coding: utf-8 -*-
"""Gera Competencias-modelo.xlsx no mesmo padrão visual das planilhas anteriores da série."""
import math
import os
import sys
from datetime import date

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
# funções de formatação compartilhadas com o gerador do PDCA (bloco inicial do arquivo)
_src = open(os.path.join(_here, "build_pdca.py"), encoding="utf-8").read()
exec(_src[: _src.index("STATUS = [")])

from openpyxl.chart import BarChart, Series  # noqa: E402
from openpyxl.chart.label import DataLabelList  # noqa: E402
from openpyxl.utils import get_column_letter as L  # noqa: E402
from comp_data import (A_ACOMP, A_APREND, A_ATRAS, A_AVAL, A_EFICAZ, A_PARCIAL, A_PLAN, A_REFAZER, COBERTURA, CHECK, EFICACIAS, EX1, EX2, NIVEIS,  # noqa: E402
                       PRAZO_EFICACIA, requerido)

BLUE, TEAL, AMBER, PURPLE, REDC = "2B5C8A", "1E7B73", "A96A12", "7A4A9A", "B0413E"
BLUE_T, AMBER_T, RED_T, PURPLE_T = "DCE8F3", "F8EBCB", "F5DEDC", "EADFF0"
NIVEL_CF = [(3, BLUE_T), (2, AMBER_T), (1, RED_T), (0, PURPLE_T)]
YESNO = ["Sim", "Parcial", "Não"]
YESNO_CF = [("Sim", GREEN), ("Parcial", YELLOW), ("Não", RED)]
NFUN, NCOMP, NPES, NPLA, NREG = 10, 12, 20, 25, 25
CC = [L(4 + k) for k in range(NCOMP)]     # colunas D a O, nas abas Funções e Matriz
F1, F2 = 10, 10 + NFUN - 1                # funções
M1, M2 = 10, 10 + NPES - 1                # pessoas, na matriz
H1 = M1 + 46                              # bloco do nível requerido por pessoa, na matriz
P1, P2 = 7, 7 + NPLA - 1                  # plano
R1, R2 = 7, 7 + NREG - 1                  # registros
FUN = "Funções"
REF = f'IF({FUN}!$D$5="",TODAY(),{FUN}!$D$5)'


def note(ws, ref, text):
    c = Comment(text, "Modelo Competências")
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


def cf_niveis(ws, rng_):
    for v, cor in NIVEL_CF:
        ws.conditional_formatting.add(rng_, CellIsRule(operator="equal", formula=[str(v)], fill=PatternFill("solid", bgColor=cor, fgColor=cor)))


def hint_row(ws, row, cells, height=30):
    for ref, text in cells:
        put(ws, f"{ref}{row}", text, f=font(9, i=True, c=MUTED), bg=GRAY, h="center")
    ws.row_dimensions[row].height = height


def alt(pares, minimo=21.75, linha=12):
    n = max(max(1, math.ceil(len(str(t)) / max(c, 1))) for t, c in pares)
    return max(minimo, n * linha + 7)


def dv_nivel(ws, rng_):
    dv = DataValidation(type="whole", operator="between", formula1="0", formula2="3", allow_blank=True)
    dv.promptTitle, dv.prompt, dv.showInputMessage = "Nível", "0 não conhece · 1 com acompanhamento · 2 sozinho · 3 treina os outros", True
    dv.errorTitle, dv.error, dv.showErrorMessage = "Nível inválido", "Digite 0, 1, 2 ou 3.", True
    ws.add_data_validation(dv)
    dv.add(rng_)


def dv_numero(ws, rng_, maximo, prompt):
    dv = DataValidation(type="decimal", operator="between", formula1="0", formula2=str(maximo), allow_blank=True)
    dv.promptTitle, dv.prompt, dv.showInputMessage = "Número", prompt, True
    dv.errorTitle, dv.error, dv.showErrorMessage = "Número inválido", f"Digite um número de 0 a {maximo}.", True
    ws.add_data_validation(dv)
    dv.add(rng_)


def chart_style(ch):
    ch.style = 2
    ch.title = None
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill="D3DBE0", w=9525))
    ch.x_axis.graphicalProperties = GraphicalProperties(ln=LineProperties(solidFill="D3DBE0", w=9525))
    ch.y_axis.graphicalProperties = GraphicalProperties(ln=LineProperties(noFill=True))


def barras(ws, anchor, r1, r2, c_cat, c_val, width=16, height=6.5, titulo="Lacunas"):
    """Barras horizontais: lacunas em cada competência."""
    ch = BarChart()
    ch.type = "bar"
    ch.gapWidth = 60
    ch.height, ch.width = height, width
    chart_style(ch)
    ch.legend = None
    s = Series(Reference(ws, min_col=c_val, min_row=r1, max_row=r2), title=titulo)
    s.graphicalProperties.solidFill = BLUE
    s.graphicalProperties.line.noFill = True
    s.dLbls = DataLabelList()
    s.dLbls.showVal = True
    s.dLbls.showSerName = s.dLbls.showCatName = s.dLbls.showLegendKey = False
    ch.append(s)
    ch.set_categories(Reference(ws, min_col=c_cat, min_row=r1, max_row=r2))
    ch.y_axis.scaling.min = 0
    ch.y_axis.majorUnit = 1
    ch.y_axis.number_format = "0"
    ch.x_axis.scaling.orientation = "maxMin"
    ws.add_chart(ch, anchor)


def f_situacao(r, ref, acao="E", prazo="G", feito="H", aprend="I", efic="J"):
    return (f'=IF({acao}{r}="","",IF({feito}{r}="",IF({prazo}{r}="","Falta o prazo",IF({prazo}{r}<{ref},"{A_ATRAS}","{A_PLAN}")),'
            f'IF({aprend}{r}="","{A_APREND}",IF({aprend}{r}="Não","{A_REFAZER}",IF({efic}{r}="",IF({feito}{r}+{PRAZO_EFICACIA}<={ref},"{A_AVAL}","{A_ACOMP}"),'
            f'IF({efic}{r}="Eficaz","{A_EFICAZ}",IF({efic}{r}="Parcial","{A_PARCIAL}","{A_REFAZER}")))))))')


SIT_CF = [(A_EFICAZ, GREEN), (A_ACOMP, BLUE_T), (A_PLAN, GRAY), (A_PARCIAL, YELLOW), (A_AVAL, YELLOW), (A_APREND, YELLOW), (A_ATRAS, RED), (A_REFAZER, RED)]

# ================================================================== pasta de trabalho
wb = Workbook()
wb.properties.title = "Matriz de competências e treinamento — Modelo"
wb.properties.creator = "Modelo Competências"
wb.properties.language = "pt-BR"

# ------------------------------------------------------------------ Instruções
ws = wb.active
ws.title = "Instruções"
widths(ws, {"A": 2, "B": 24, "C": 92, "D": 2})
title(ws, "Matriz de competências e treinamento — Como usar esta planilha",
      "Modelo para definir o nível requerido por função, avaliar as pessoas, planejar o treinamento e registrar a eficácia.", "C")
r = 4


def section(text):
    global r
    band(ws, r, text, "C", sz=11)
    r += 1


def line(k, v, kbg=GRAY, vbg=None, kf=None, kh="left", height=None):
    global r
    put(ws, f"B{r}", k, f=kf or font(10, True), bg=kbg, h=kh)
    put(ws, f"C{r}", v, bg=vbg)
    ws.row_dimensions[r].height = height or (19.5 if len(v) <= 98 else (31.5 if len(v) <= 196 else 45.75))
    r += 1


section("Legenda: onde preencher")
line("Amarelo-claro", "Células de entrada. É aqui que você digita.", vbg=INPUT)
line("Cinza", "Células calculadas ou fixas (rótulos, requerido por pessoa, lacunas, contagens, avisos). Não altere.", vbg=GRAY)
line("Cinza em itálico", "Linha de exemplo (marcada com “Ex.”). Mostra o formato esperado e não entra nas contagens.", vbg=GRAY)
line("Listas suspensas", "Colunas de função, aprendizado, eficácia e status aceitam apenas as opções da lista. Os níveis aceitam 0, 1, 2 ou 3.")
line("Comentários", "Células com triângulo vermelho no canto trazem uma dica de preenchimento. Passe o mouse sobre elas.")
r += 1
section("A escala de níveis")
for n, nome, faz, ev in NIVEIS:
    line(f"Nível {n} · {nome}", f"{faz} Evidência: {ev[0].lower()}{ev[1:]}", kbg=[PURPLE_T, RED_T, AMBER_T, BLUE_T][n])
r += 1
section("Ordem recomendada de preenchimento")
for k, text in enumerate([
    "Aba Funções: escreva a organização, a data de referência, as competências e as funções, e o nível requerido de cada cruzamento.",
    "Aba Matriz: cadastre as pessoas, com a função, e o nível atual em cada competência.",
    "Aba Matriz: leia as lacunas de cada pessoa e a cobertura de cada competência.",
    "Aba Plano: escreva uma ação para cada lacuna, com quem treina e o prazo.",
    "Aba Plano: depois do treinamento, registre a data, o aprendizado e, no prazo, a eficácia.",
    "Aba Matriz: quando a eficácia for confirmada, atualize o nível da pessoa.",
    "Aba Registros: cadastre os treinamentos realizados, com a evidência. Aba Checklist: valide a matriz.",
], 1):
    line(f"Passo {k}", text)
r += 1
section("Abas da planilha")
for k, text in [
    ("Funções", f"Até {NFUN} funções e {NCOMP} competências, com o nível requerido de cada cruzamento."),
    ("Matriz", f"Até {NPES} pessoas, com o nível atual, as lacunas, o percentual atendido, a cobertura de cada competência e o gráfico."),
    ("Plano", f"Até {NPLA} ações de treinamento, com a situação de cada uma na data de referência."),
    ("Registros", f"Até {NREG} treinamentos realizados, com tema, instrutor, carga horária e participantes."),
    ("Checklist", "Doze verificações de qualidade da matriz, com percentual de conclusão."),
    ("Exemplo 1 - Pizzaria", "A matriz e o plano de uma loja, com oito pessoas e oito competências."),
    ("Exemplo 2 - Compras", "A matriz e o plano do processo de aquisição de uma indústria."),
]:
    line(k, text)
r += 1
section("Regras e premissas do modelo")
for k, text in [
    ("Lacuna", "Nível atual abaixo do nível requerido pela função da pessoa. Nível em branco vale zero."),
    ("Requerido por pessoa", "É lido da aba Funções, pela função escrita na aba Matriz. A função precisa estar escrita do mesmo jeito nas duas abas: use a lista."),
    ("Cobertura", f"Pessoas no nível 2 ou mais em uma competência. Menos de {COBERTURA} é dependência de uma só pessoa. É uma convenção deste modelo."),
    ("Eficácia", f"Depois do treinamento, a eficácia é avaliada no posto. A planilha pede a avaliação {PRAZO_EFICACIA} dias após a data de realização."),
    ("Data de referência", "A situação das ações é calculada pela data de referência da aba Funções. Se ela estiver em branco, a planilha usa a data de hoje."),
    ("Escala", "Os quatro níveis e as evidências são uma convenção deste modelo. A norma não define escala."),
    ("Exemplos", "Os dados das abas de exemplo são ilustrativos, criados para este material."),
]:
    line(k, text)
setup(ws, INK, f"B1:C{r}", landscape=False, fit_height=True)

# ------------------------------------------------------------------ Funções
ws = wb.create_sheet(FUN)
widths(ws, dict({"A": 2, "B": 5, "C": 26, "P": 12, "Q": 2}, **{c: 13 for c in CC}))
title(ws, "Funções e nível requerido", "Escreva as competências nas colunas e as funções nas linhas. Em cada cruzamento, o nível mínimo que a função exige: 0 quando não usa.", "P")
label(ws, "B4", "Organização", merge="B4:C4")
inp(ws, "D4", merge="D4:G4")
label(ws, "B5", "Data de referência", merge="B5:C5")
inp(ws, "D5", fmt=DATE, h="left")
put(ws, "E5", "Data da avaliação. Em branco, vale a data de hoje.", f=font(9, i=True, c=MUTED), bg=GRAY, merge="E5:G5")
dv_date(ws, "D5")
for rr in (4, 5):
    ws.row_dimensions[rr].height = 21.75
put(ws, "B7", "", bg=GRAY)
label(ws, "C7", "Código")
for k, c in enumerate(CC):
    put(ws, f"{c}7", f"C{k + 1}", f=font(10, True, c=MUTED), bg=GRAY, h="center")
put(ws, "P7", "", bg=GRAY)
label(ws, "C8", "Competência")
for c in CC:
    inp(ws, f"{c}8", h="center")
put(ws, "B8", "", bg=GRAY)
put(ws, "P8", "", bg=GRAY)
ws.row_dimensions[8].height = 45
head(ws, "B9", "#")
head(ws, "C9", "Função")
for c in CC:
    head(ws, f"{c}9", "Nível requerido")
head(ws, "P9", "Competências exigidas")
ws.row_dimensions[9].height = 33
for k in range(NFUN):
    rr = F1 + k
    num(ws, f"B{rr}", k + 1)
    inp(ws, f"C{rr}")
    for c in CC:
        inp(ws, f"{c}{rr}", h="center")
    calc(ws, f"P{rr}", f'=IF(C{rr}="","",COUNTIF({CC[0]}{rr}:{CC[-1]}{rr},">0"))', b=False)
    ws.row_dimensions[rr].height = 21.75
dv_nivel(ws, f"{CC[0]}{F1}:{CC[-1]}{F2}")
cf_niveis(ws, f"{CC[0]}{F1}:{CC[-1]}{F2}")
note(ws, "C8", "O que precisa ser sabido fazer no processo: a parte “com quem” da tartaruga e os procedimentos. Seis a doze por processo.")
note(ws, "C9", "As funções que afetam o resultado, e não os cargos. Uma pessoa pode ter mais de uma função.")
s = F2 + 2
band(ws, s, "Resumo automático", "P")
for k, (text, formula) in enumerate([
    ("Funções cadastradas", f"=COUNTA(C{F1}:C{F2})"),
    ("Competências cadastradas", f"=COUNTA({CC[0]}8:{CC[-1]}8)"),
    ("Aviso", f'=IF(E{s+1}=0,"Cadastre as funções",IF(E{s+2}=0,"Cadastre as competências",IF(COUNTIF(P{F1}:P{F2},0)>0,"Há função sem nenhuma competência exigida",'
              f'IF(SUMPRODUCT(({CC[0]}8:{CC[-1]}8="")*({CC[0]}{F1}:{CC[-1]}{F2}>0))>0,"Há nível requerido em competência sem nome","OK"))))'),
], 1):
    label(ws, f"B{s+k}", text, merge=f"B{s+k}:D{s+k}", h="right")
    calc(ws, f"E{s+k}", formula, merge=f"E{s+k}:G{s+k}", sz=9 if text == "Aviso" else 10, b=text != "Aviso")
    ws.row_dimensions[s + k].height = 21.75
cf_warn(ws, f"E{s+3}:G{s+3}", f"E{s+3}")
ws.freeze_panes = "D10"
setup(ws, BLUE, f"B1:P{s+3}", fit_height=True)

# ------------------------------------------------------------------ Matriz
ws = wb.create_sheet("Matriz")
widths(ws, dict({"A": 2, "B": 5, "C": 22, "P": 8, "Q": 10, "R": 10, "S": 10, "T": 20, "U": 2}, **{c: 9 for c in CC}))
# a coluna D da matriz é a função; as competências ocupam E a P
MC = [L(5 + k) for k in range(NCOMP)]
widths(ws, dict({"D": 20}, **{c: 9 for c in MC}))
title(ws, "Matriz de competências", "Uma pessoa por linha, com a função e o nível atual em cada competência. O requerido vem da função, e a lacuna é calculada.", "T")
label(ws, "B4", "Organização", merge="B4:C4")
calc(ws, "D4", f'=IF({FUN}!D4="","",{FUN}!D4)', h="left", b=False, merge="D4:G4")
label(ws, "B5", "Data de referência", merge="B5:C5")
calc(ws, "D5", f'=IF({FUN}!D5="","",{FUN}!D5)', fmt=DATE, h="left", b=False)
for rr in (4, 5):
    ws.row_dimensions[rr].height = 21.75
for col, text in zip("BCD", ["#", "Pessoa", "Função"]):
    head(ws, f"{col}7", text)
for k, c in enumerate(MC):
    head(ws, f"{c}7", f"C{k + 1}")
    calc(ws, f"{c}8", f'=IF({FUN}!{CC[k]}8="","",{FUN}!{CC[k]}8)', b=False, sz=8)
for col, text in zip("QRST", ["Exigidas", "Lacunas", "Atendido", "Conferência"]):
    head(ws, f"{col}7", text)
for col in "BCD":
    put(ws, f"{col}8", "", bg=GRAY)
put(ws, "C8", "Os nomes das competências vêm da aba Funções", f=font(9, i=True, c=MUTED), bg=GRAY, h="center", merge="C8:D8")
for col in "QRST":
    put(ws, f"{col}8", "", bg=GRAY)
ws.row_dimensions[7].height = 21.75
ws.row_dimensions[8].height = 48
hint_row(ws, 9, [("B", ""), ("C", "Nome"), ("D", "Escolha na lista"), ("Q", "Calculada"), ("R", "Calculada"), ("S", "Calculada"), ("T", "Calculada")] + [(c, "0 a 3") for c in MC])
HREQ = lambda r: f"{MC[0]}{H1 + r - M1}:{MC[-1]}{H1 + r - M1}"  # noqa: E731  # linha do requerido da pessoa
for k in range(NPES):
    rr = M1 + k
    num(ws, f"B{rr}", k + 1)
    inp(ws, f"C{rr}")
    inp(ws, f"D{rr}")
    for c in MC:
        inp(ws, f"{c}{rr}", h="center")
    calc(ws, f"Q{rr}", f'=IF(C{rr}="","",COUNTIF({HREQ(rr)},">0"))', b=False)
    calc(ws, f"R{rr}", f'=IF(C{rr}="","",SUMPRODUCT(({HREQ(rr)}>{MC[0]}{rr}:{MC[-1]}{rr})*1))', b=False)
    calc(ws, f"S{rr}", f'=IF(OR(C{rr}="",Q{rr}=0),"",1-R{rr}/Q{rr})', fmt="0%", b=False)
    calc(ws, f"T{rr}", f'=IF(C{rr}="","",IF(D{rr}="","Falta a função",IF(ISNA(MATCH(D{rr},{FUN}!$C${F1}:$C${F2},0)),"Função não cadastrada",'
         f'IF(R{rr}=0,"Sem lacunas","Com lacunas"))))', b=False, sz=9)
    ws.row_dimensions[rr].height = 21.75
dv = DataValidation(type="list", formula1=f"={FUN}!$C${F1}:$C${F2}", allow_blank=True)
dv.promptTitle, dv.prompt, dv.showInputMessage = "Função", "Escolha uma função da aba Funções.", True
dv.errorTitle, dv.error, dv.showErrorMessage = "Função inválida", "Escolha uma função cadastrada na aba Funções.", True
ws.add_data_validation(dv)
dv.add(f"D{M1}:D{M2}")
dv_nivel(ws, f"{MC[0]}{M1}:{MC[-1]}{M2}")
cf_niveis(ws, f"{MC[0]}{M1}:{MC[-1]}{M2}")
# lacuna: contorno escuro na célula (fonte em negrito escura) quando o nível fica abaixo do requerido
ws.conditional_formatting.add(f"{MC[0]}{M1}:{MC[-1]}{M2}", FormulaRule(formula=[f'AND($C{M1}<>"",{MC[0]}{H1}>N({MC[0]}{M1}))'],
                              font=Font(name="Arial", size=10, bold=True, color=REDC), border=Border(left=Side(style="medium", color=REDC), right=Side(style="medium", color=REDC),
                                                                                                    top=Side(style="medium", color=REDC), bottom=Side(style="medium", color=REDC))))
cf_texto(ws, f"T{M1}:T{M2}", f"T{M1}", [("Sem lacunas", GREEN), ("Com lacunas", YELLOW)], resto=RED)
note(ws, "D7", "A função precisa estar cadastrada na aba Funções. É ela que define o nível requerido.")
note(ws, "R7", "Competências em que o nível atual está abaixo do requerido pela função. Célula com borda vermelha na matriz.")
# leitura por competência
s = M2 + 2
band(ws, s, "Leitura por competência", "T")
for k, (rot, f_) in enumerate([
    ("Pessoas cuja função exige", f'=IF({{c}}8="","",SUMPRODUCT(({FUN}!{{f}}${F1}:{{f}}${F2}>0)*COUNTIF($D${M1}:$D${M2},{FUN}!$C${F1}:$C${F2})))'),
    ("Com lacuna", f'=IF({{c}}8="","",SUMPRODUCT(({{c}}${H1}:{{c}}${H1 + NPES - 1}>{{c}}${M1}:{{c}}${M2})*1))'),
    ("No nível 2 ou mais", f'=IF({{c}}8="","",COUNTIF({{c}}${M1}:{{c}}${M2},">=2"))'),
    ("No nível 3", f'=IF({{c}}8="","",COUNTIF({{c}}${M1}:{{c}}${M2},3))'),
    ("Cobertura", f'=IF(OR({{c}}8="",{{c}}{s+1}=0),"",IF({{c}}{s+3}=0,"Ninguém no nível 2",IF({{c}}{s+3}<{COBERTURA},"Uma só pessoa","Coberta")))'),
], 1):
    rr = s + k
    label(ws, f"B{rr}", rot, merge=f"B{rr}:D{rr}", h="right")
    for c, f in zip(MC, CC):
        calc(ws, f"{c}{rr}", f_.replace("{c}", c).replace("{f}", f), b=k == 5, sz=8 if k == 5 else 10)
    for col in "QRST":
        put(ws, f"{col}{rr}", "", bg=GRAY)
    ws.row_dimensions[rr].height = 27 if k == 5 else 21.75
cf_texto(ws, f"{MC[0]}{s+5}:{MC[-1]}{s+5}", f"{MC[0]}{s+5}", [("Coberta", GREEN), ("Uma só pessoa", YELLOW), ("Ninguém no nível 2", RED)])
# resumo
t = s + 7
band(ws, t, "Resumo automático", "H")
put(ws, f"J{t}", "Lacunas por competência", f=font(10, True, c=WHITE), bg=INK, box=False, merge=f"J{t}:P{t}")
for k, (text, formula, fmt) in enumerate([
    ("Pessoas avaliadas", f"=COUNTA(C{M1}:C{M2})", None),
    ("Lacunas", f"=SUM(R{M1}:R{M2})", None),
    ("Percentual do requerido atendido", f'=IF(SUM(Q{M1}:Q{M2})=0,"",1-E{t+2}/SUM(Q{M1}:Q{M2}))', "0%"),
    ("Competências com uma só pessoa, ou nenhuma", f'=COUNTIF({MC[0]}{s+5}:{MC[-1]}{s+5},"Uma só pessoa")+COUNTIF({MC[0]}{s+5}:{MC[-1]}{s+5},"Ninguém no nível 2")', None),
    ("Aviso", f'=IF(E{t+1}=0,"Cadastre as pessoas",IF(COUNTIF(T{M1}:T{M2},"Falta*")+COUNTIF(T{M1}:T{M2},"Função não cadastrada")>0,"Há pessoa sem função válida: veja a coluna Conferência",'
              f'IF(E{t+4}>0,"Há competência que depende de uma só pessoa",IF(E{t+2}>0,"Há lacunas: leve ao plano de treinamento","OK"))))', None),
], 1):
    label(ws, f"B{t+k}", text, merge=f"B{t+k}:D{t+k}", h="right")
    calc(ws, f"E{t+k}", formula, fmt=fmt, merge=f"E{t+k}:H{t+k}", sz=9 if text == "Aviso" else 10, b=text != "Aviso")
    ws.row_dimensions[t + k].height = 21.75
cf_warn(ws, f"E{t+5}:H{t+5}", f"E{t+5}")
for k, c in enumerate(MC):
    calc(ws, f"J{t+1+k}", f'=IF({c}8="","C{k+1}","C{k+1} · "&{c}8)', h="left", b=False, sz=9, merge=f"J{t+1+k}:O{t+1+k}")
    calc(ws, f"P{t+1+k}", f'=IF({c}8="","",{c}{s+2})')
    ws.row_dimensions[t + 1 + k].height = 18
barras(ws, f"Q{t}", t + 1, t + NCOMP, 10, 16, width=14, height=8.5)
# bloco do nível requerido por pessoa (calculado)
assert H1 > t + NCOMP + 1
band(ws, H1 - 2, "Nível requerido por pessoa, lido da aba Funções pela função de cada uma. Bloco calculado, usado nas lacunas.", "T", color=MUTED)
put(ws, f"B{H1-1}", "#", f=font(10, True), bg=GRAY, h="center")
put(ws, f"C{H1-1}", "Pessoa", f=font(10, True), bg=GRAY, h="center")
put(ws, f"D{H1-1}", "Função", f=font(10, True), bg=GRAY, h="center")
for k, c in enumerate(MC):
    put(ws, f"{c}{H1-1}", f"C{k + 1}", f=font(10, True), bg=GRAY, h="center")
for k in range(NPES):
    rr = H1 + k
    num(ws, f"B{rr}", k + 1)
    calc(ws, f"C{rr}", f'=IF(C{M1+k}="","",C{M1+k})', h="left", b=False, sz=9)
    calc(ws, f"D{rr}", f'=IF(D{M1+k}="","",D{M1+k})', h="left", b=False, sz=9)
    for c, f in zip(MC, CC):
        calc(ws, f"{c}{rr}", f'=IF($D{M1+k}="",0,IFERROR(N(INDEX({FUN}!{f}${F1}:{f}${F2},MATCH($D{M1+k},{FUN}!$C${F1}:$C${F2},0))),0))', b=False, sz=9)
    ws.row_dimensions[rr].height = 18
ws.freeze_panes = "E10"
setup(ws, TEAL, f"B1:T{H1 - 3}", fit_height=True)

# ------------------------------------------------------------------ Plano
ws = wb.create_sheet("Plano")
widths(ws, {"A": 2, "B": 5, "C": 16, "D": 12, "E": 44, "F": 18, "G": 12, "H": 12, "I": 12, "J": 12, "K": 12, "L": 30, "M": 24, "N": 2})
title(ws, "Plano de treinamento", "Uma ação para cada lacuna. Depois do treinamento, registre a data, o aprendizado e, no prazo, a eficácia no posto.", "M")
for col, text in zip("BCDEFGHIJKLM", ["#", "Pessoa", "Competência", "Ação", "Quem treina", "Prazo", "Realizada em", "Aprendizado", "Eficácia", "Eficácia avaliada em",
                                       "Observação", "Situação"]):
    head(ws, f"{col}4", text)
ws.row_dimensions[4].height = 33
hint_row(ws, 5, [("B", ""), ("C", "Nome, como na matriz"), ("D", "Código, C1 a C12"), ("E", "Curso, instrução no posto, acompanhamento"), ("F", "Nome ou cargo"),
                 ("G", "Combinado"), ("H", "Data do treinamento"), ("I", "Sim ou Não"), ("J", "No posto, após o prazo"), ("K", "Data da avaliação"),
                 ("L", "Resultado, indicador"), ("M", "Calculada")])
ex(ws, "B6", "Ex.", h="center")
for col, v, h_, fmt in [("C", "Bruno", "left", None), ("D", "C3", "center", "@"), ("E", "Instrução no posto: regular o forno com o pizzaiolo líder, uma semana por turno.", "left", None),
                        ("F", "Rafael", "left", None), ("G", date(2027, 1, 22), "center", DATE), ("H", date(2027, 1, 20), "center", DATE), ("I", "Sim", "center", None),
                        ("J", "Parcial", "center", None), ("K", date(2027, 2, 12), "center", DATE), ("L", "Regula a temperatura; ainda não regula a chama do lastro.", "left", None),
                        ("M", A_PARCIAL, "center", None)]:
    ex(ws, f"{col}6", v, h=h_, fmt=fmt)
ws.row_dimensions[6].height = 30
for k in range(NPLA):
    rr = P1 + k
    num(ws, f"B{rr}", k + 1)
    inp(ws, f"C{rr}")
    inp(ws, f"D{rr}", h="center", fmt="@")
    inp(ws, f"E{rr}")
    inp(ws, f"F{rr}")
    inp(ws, f"G{rr}", h="center", fmt=DATE)
    inp(ws, f"H{rr}", h="center", fmt=DATE)
    inp(ws, f"I{rr}", h="center")
    inp(ws, f"J{rr}", h="center")
    inp(ws, f"K{rr}", h="center", fmt=DATE)
    inp(ws, f"L{rr}")
    calc(ws, f"M{rr}", f_situacao(rr, REF), b=False, sz=9)
    ws.row_dimensions[rr].height = 30
for col in "GHK":
    dv_date(ws, f"{col}{P1}:{col}{P2}")
dv_list(ws, f"I{P1}:I{P2}", ["Sim", "Não"], "Sim ou Não")
dv_list(ws, f"J{P1}:J{P2}", EFICACIAS, "Eficaz, Parcial ou Não eficaz")
cf_texto(ws, f"M{P1}:M{P2}", f"M{P1}", SIT_CF, resto=YELLOW)
note(ws, "I4", "A pessoa entendeu? Prova, exercício ou demonstração, no fim do treinamento.")
note(ws, "J4", f"A pessoa passou a fazer no padrão? Avaliada pelo líder, no posto, {PRAZO_EFICACIA} dias depois do treinamento.\nEficaz sobe o nível na matriz.")
s = P2 + 2
band(ws, s, "Resumo automático", "M")
for k, (text, formula) in enumerate([
    ("Ações registradas", f"=COUNTA(E{P1}:E{P2})"),
    ("Planejadas, no prazo", f'=COUNTIF(M{P1}:M{P2},"{A_PLAN}")'),
    ("Atrasadas", f'=COUNTIF(M{P1}:M{P2},"{A_ATRAS}")'),
    ("Realizadas, a avaliar", f'=COUNTIF(M{P1}:M{P2},"{A_AVAL}")+COUNTIF(M{P1}:M{P2},"{A_APREND}")'),
    ("Eficazes", f'=COUNTIF(M{P1}:M{P2},"{A_EFICAZ}")'),
    ("A reforçar ou refazer", f'=COUNTIF(M{P1}:M{P2},"{A_PARCIAL}")+COUNTIF(M{P1}:M{P2},"{A_REFAZER}")'),
    ("Aviso", f'=IF(E{s+1}=0,"Registre as ações",IF(COUNTIF(M{P1}:M{P2},"Falta o prazo")>0,"Há ação sem prazo",IF(E{s+3}>0,"Há ação atrasada",'
              f'IF(E{s+4}>0,"Há treinamento realizado com avaliação pendente",IF(E{s+6}>0,"Há ação a reforçar ou refazer","OK")))))'),
], 1):
    label(ws, f"B{s+k}", text, merge=f"B{s+k}:D{s+k}", h="right")
    calc(ws, f"E{s+k}", formula, merge=f"E{s+k}:F{s+k}", sz=9 if text == "Aviso" else 10, b=text != "Aviso")
    ws.row_dimensions[s + k].height = 21.75
cf_warn(ws, f"E{s+7}:F{s+7}", f"E{s+7}")
ws.freeze_panes = "E7"
setup(ws, AMBER, f"B1:M{s+7}", fit_height=True)

# ------------------------------------------------------------------ Registros
ws = wb.create_sheet("Registros")
widths(ws, {"A": 2, "B": 5, "C": 13, "D": 40, "E": 22, "F": 12, "G": 13, "H": 14, "I": 34, "J": 22, "K": 2})
title(ws, "Registros de treinamento", "Um treinamento por linha, com a evidência de que aconteceu e de que o aprendizado foi avaliado.", "J")
for col, text in zip("BCDEFGHIJ", ["#", "Data", "Tema", "Instrutor", "Carga horária", "Participantes", "Aprendizado avaliado?", "Evidência", "Conferência"]):
    head(ws, f"{col}4", text)
ws.row_dimensions[4].height = 33
hint_row(ws, 5, [("B", ""), ("C", "Do treinamento"), ("D", "Assunto e padrão"), ("E", "Nome ou cargo"), ("F", "Em horas"), ("G", "Número de pessoas"),
                 ("H", "Sim ou Não"), ("I", "Lista de presença, prova, certificado"), ("J", "Calculada")])
ex(ws, "B6", "Ex.", h="center")
for col, v, h_, fmt in [("C", date(2026, 10, 28), "center", DATE), ("D", "IT-EXP-01: agrupamento por zona e conferência do pedido", "left", None),
                        ("E", "Sérgio, líder da expedição", "left", None), ("F", 2, "center", None), ("G", 1, "center", None), ("H", "Sim", "center", None),
                        ("I", "Lista de presença e demonstração no posto", "left", None), ("J", "Completo", "center", None)]:
    ex(ws, f"{col}6", v, h=h_, fmt=fmt)
ws.row_dimensions[6].height = 24
for k in range(NREG):
    rr = R1 + k
    num(ws, f"B{rr}", k + 1)
    inp(ws, f"C{rr}", h="center", fmt=DATE)
    inp(ws, f"D{rr}")
    inp(ws, f"E{rr}")
    inp(ws, f"F{rr}", h="center")
    inp(ws, f"G{rr}", h="center")
    inp(ws, f"H{rr}", h="center")
    inp(ws, f"I{rr}")
    calc(ws, f"J{rr}", f'=IF(D{rr}="","",IF(C{rr}="","Falta a data",IF(I{rr}="","Falta a evidência",IF(H{rr}="","Falta a avaliação de aprendizado",'
         f'IF(H{rr}="Não","Sem avaliação de aprendizado","Completo")))))', b=False, sz=9)
    ws.row_dimensions[rr].height = 24
dv_date(ws, f"C{R1}:C{R2}")
dv_numero(ws, f"F{R1}:F{R2}", 200, "Carga horária, em horas.")
dv_numero(ws, f"G{R1}:G{R2}", 500, "Número de participantes.")
dv_list(ws, f"H{R1}:H{R2}", ["Sim", "Não"], "Sim ou Não")
cf_texto(ws, f"J{R1}:J{R2}", f"J{R1}", [("Completo", GREEN)], resto=YELLOW)
s = R2 + 2
band(ws, s, "Resumo automático", "J")
for k, (text, formula, fmt) in enumerate([
    ("Treinamentos registrados", f"=COUNTA(D{R1}:D{R2})", None),
    ("Horas de treinamento", f"=SUM(F{R1}:F{R2})", None),
    ("Pessoas-hora", f"=SUMPRODUCT(F{R1}:F{R2},G{R1}:G{R2})", None),
    ("Aviso", f'=IF(E{s+1}=0,"Registre os treinamentos",IF(COUNTIF(J{R1}:J{R2},"Falta*")>0,"Há treinamento com campos em branco: veja a coluna Conferência",'
              f'IF(COUNTIF(J{R1}:J{R2},"Sem avaliação*")>0,"Há treinamento sem avaliação de aprendizado","OK")))', None),
], 1):
    label(ws, f"B{s+k}", text, merge=f"B{s+k}:D{s+k}", h="right")
    calc(ws, f"E{s+k}", formula, fmt=fmt, merge=f"E{s+k}:F{s+k}", sz=9 if text == "Aviso" else 10, b=text != "Aviso")
    ws.row_dimensions[s + k].height = 21.75
cf_warn(ws, f"E{s+4}:F{s+4}", f"E{s+4}")
ws.freeze_panes = "D7"
setup(ws, PURPLE, f"B1:J{s+4}", fit_height=True)

# ------------------------------------------------------------------ Checklist
ws = wb.create_sheet("Checklist")
widths(ws, {"A": 2, "B": 5, "C": 70, "D": 14, "E": 44, "F": 2})
title(ws, "Checklist da matriz de competências", "Escolha o status de cada item na lista suspensa (coluna em amarelo-claro).", "E")
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


def exemplo(ws, data):
    n = len(data["comps"])
    EC = [L(4 + k) for k in range(n)]  # D em diante
    last = L(4 + n + 3)                 # lacunas, atendido, situação
    widths(ws, dict({"A": 2, "B": 14, "C": 22, L(4 + n): 10, L(5 + n): 11, L(6 + n): 16, L(7 + n): 20, L(8 + n): 2}, **{c: 9.5 for c in EC}))
    title(ws, "Matriz de competências e treinamento", "Exemplo preenchido, para consulta. Use as abas Funções, Matriz, Plano e Registros para a sua equipe.", last)
    H = data["head"]
    rr = 4
    for rot, val, fmt in [("Organização", H["org"], None), ("Data de referência", H["data"], DATE), ("Participantes", H["por"], None), ("Revisão", H["revisao"], None),
                          ("Origem", H["origem"], None)]:
        label(ws, f"B{rr}", rot)
        inp(ws, f"C{rr}", val, merge=f"C{rr}:{last}{rr}", bg=WHITE, fmt=fmt, h="left")
        ws.row_dimensions[rr].height = 19.5
        rr += 1
    rr += 1
    # competências e requerido por função
    band(ws, rr, "Competências e nível requerido por função", last, color=BLUE)
    rr += 1
    sub(ws, rr, [("B", None, "Função"), ("C", None, "Competência →")] + [(c, None, cod) for c, (cod, _, _) in zip(EC, data["comps"])], height=21.75)
    rr += 1
    put(ws, f"B{rr}", "", bg=GRAY)
    put(ws, f"C{rr}", "Nome da competência", f=font(9, i=True, c=MUTED), bg=GRAY, h="center")
    for c, (_, nome, _) in zip(EC, data["comps"]):
        put(ws, f"{c}{rr}", nome, f=font(8), bg=GRAY, h="center")
    ws.row_dimensions[rr].height = 48
    fr = {}
    for fn, req in data["funcoes"].items():
        rr += 1
        put(ws, f"B{rr}", fn, f=font(10, True), merge=f"B{rr}:C{rr}")
        for c, v in zip(EC, req):
            put(ws, f"{c}{rr}", v, h="center")
        fr[fn] = rr
        ws.row_dimensions[rr].height = 19.5
    cf_niveis(ws, f"{EC[0]}{rr - len(fr) + 1}:{EC[-1]}{rr}")
    rr += 2
    # matriz
    band(ws, rr, f'Matriz · níveis em {H["data"]:%d/%m/%Y}', last, color=TEAL)
    rr += 1
    sub(ws, rr, [("B", None, "Pessoa"), ("C", None, "Função")] + [(c, None, cod) for c, (cod, _, _) in zip(EC, data["comps"])]
        + [(L(4 + n), None, "Lacunas"), (L(5 + n), None, "Atendido"), (L(6 + n), L(7 + n), "Situação")], height=21.75)
    m1 = rr + 1
    for p in data["pessoas"]:
        rr += 1
        req_row = fr[p["funcao"]]
        put(ws, f"B{rr}", p["nome"], f=font(10, True))
        put(ws, f"C{rr}", p["funcao"])
        for c, v in zip(EC, p["niveis"]):
            put(ws, f"{c}{rr}", v, h="center")
        calc(ws, f"{L(4 + n)}{rr}", f"=SUMPRODUCT(({EC[0]}{req_row}:{EC[-1]}{req_row}>{EC[0]}{rr}:{EC[-1]}{rr})*1)", b=False)
        calc(ws, f"{L(5 + n)}{rr}", f'=1-{L(4 + n)}{rr}/COUNTIF({EC[0]}{req_row}:{EC[-1]}{req_row},">0")', fmt="0%", b=False)
        calc(ws, f"{L(6 + n)}{rr}", f'=IF({L(4 + n)}{rr}=0,"Sem lacunas","Com lacunas")', b=False, sz=9, merge=f"{L(6 + n)}{rr}:{L(7 + n)}{rr}")
        for c, v, r_ in zip(EC, p["niveis"], requerido(data, p)):
            if r_ > v:
                ws[f"{c}{rr}"].font = font(10, True, c=REDC)
                ws[f"{c}{rr}"].border = Border(left=Side(style="medium", color=REDC), right=Side(style="medium", color=REDC), top=Side(style="medium", color=REDC),
                                               bottom=Side(style="medium", color=REDC))
        ws.row_dimensions[rr].height = 19.5
    m2 = rr
    cf_niveis(ws, f"{EC[0]}{m1}:{EC[-1]}{m2}")
    cf_texto(ws, f"{L(6 + n)}{m1}:{L(6 + n)}{m2}", f"{L(6 + n)}{m1}", [("Sem lacunas", GREEN), ("Com lacunas", YELLOW)])
    for rot, f_ in [("No nível 2 ou mais", '=COUNTIF({c}%d:{c}%d,">=2")' % (m1, m2)), ("No nível 3", "=COUNTIF({c}%d:{c}%d,3)" % (m1, m2))]:
        rr += 1
        label(ws, f"B{rr}", rot, merge=f"B{rr}:C{rr}", h="right")
        for c in EC:
            calc(ws, f"{c}{rr}", f_.replace("{c}", c))
        for col in (L(4 + n), L(5 + n), L(6 + n), L(7 + n)):
            put(ws, f"{col}{rr}", "", bg=GRAY)
        ws.row_dimensions[rr].height = 21.75
    c2 = rr - 1
    rr += 1
    put(ws, f"B{rr}", "Célula com borda vermelha: lacuna, nível abaixo do requerido pela função.", f=font(9, i=True, c=MUTED), merge=f"B{rr}:{last}{rr}", box=False)
    rr += 2
    ws.row_breaks.append(Break(id=rr - 1))
    # plano
    band(ws, rr, "Plano de treinamento", last, color=AMBER)
    rr += 1
    pl = [("B", None, "Pessoa"), ("C", None, "Comp."), (EC[0], EC[3], "Ação"), (EC[4], EC[5], "Quem treina"), (EC[6], EC[7], "Prazo"),
          (L(4 + n), None, "Realizada"), (L(5 + n), None, "Aprendizado"), (L(6 + n), None, "Eficácia"), (L(7 + n), None, "Situação")]
    sub(ws, rr, pl, height=24)
    p1 = rr + 1
    for a in data["plano"]:
        rr += 1
        put(ws, f"B{rr}", a["pessoa"], f=font(10, True))
        put(ws, f"C{rr}", a["comp"], h="center")
        put(ws, f"{EC[0]}{rr}", a["acao"], merge=f"{EC[0]}{rr}:{EC[3]}{rr}")
        put(ws, f"{EC[4]}{rr}", a["quem"], merge=f"{EC[4]}{rr}:{EC[5]}{rr}")
        put(ws, f"{EC[6]}{rr}", a["prazo"], h="center", fmt=DATE, merge=f"{EC[6]}{rr}:{EC[7]}{rr}")
        put(ws, f"{L(4 + n)}{rr}", a["feito"], h="center", fmt=DATE)
        put(ws, f"{L(5 + n)}{rr}", a["aprend"], h="center")
        put(ws, f"{L(6 + n)}{rr}", a["eficacia"], h="center")
        calc(ws, f"{L(7 + n)}{rr}", f_situacao(rr, "$C$5", acao=EC[0], prazo=EC[6], feito=L(4 + n), aprend=L(5 + n), efic=L(6 + n)), b=False, sz=9)
        ws.row_dimensions[rr].height = alt([(a["acao"], 40), (a["quem"], 20)], minimo=24)
    p2 = rr
    cf_texto(ws, f"{L(7 + n)}{p1}:{L(7 + n)}{p2}", f"{L(7 + n)}{p1}", SIT_CF, resto=YELLOW)
    rr += 2
    band(ws, rr, "Resumo automático", last)
    for k, (text, formula, fmt) in enumerate([
        ("Pessoas avaliadas", f"=COUNTA(B{m1}:B{m2})", None),
        ("Lacunas", f"=SUM({L(4 + n)}{m1}:{L(4 + n)}{m2})", None),
        ("Competências com uma só pessoa no nível 2, ou nenhuma", f'=COUNTIF({EC[0]}{c2}:{EC[-1]}{c2},"<{COBERTURA}")', None),
        ("Competências sem ninguém no nível 3", f"=COUNTIF({EC[0]}{c2 + 1}:{EC[-1]}{c2 + 1},0)", None),
        ("Ações no plano", f"=COUNTA(B{p1}:B{p2})", None),
        ("Ações eficazes", f'=COUNTIF({L(7 + n)}{p1}:{L(7 + n)}{p2},"{A_EFICAZ}")', None),
        ("Ações atrasadas, ou a refazer", f'=COUNTIF({L(7 + n)}{p1}:{L(7 + n)}{p2},"{A_ATRAS}")+COUNTIF({L(7 + n)}{p1}:{L(7 + n)}{p2},"{A_REFAZER}")', None),
    ], 1):
        label(ws, f"B{rr+k}", text, merge=f"B{rr+k}:{EC[1]}{rr+k}", h="right")
        calc(ws, f"{EC[2]}{rr+k}", formula, fmt=fmt)
        ws.row_dimensions[rr + k].height = 21.75
    setup(ws, MUTED, f"B1:{last}{rr + 7}")


exemplo(wb.create_sheet("Exemplo 1 - Pizzaria"), EX1)
exemplo(wb.create_sheet("Exemplo 2 - Compras"), EX2)

wb.active = 1
wb.save(OUT)
print("ok", OUT)
