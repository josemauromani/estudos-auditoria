# -*- coding: utf-8 -*-
"""Gera Objetivos-modelo.xlsx no mesmo padrão visual das planilhas anteriores da série."""
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
from openpyxl.utils import get_column_letter  # noqa: E402
from obj_data import (ALC, ANDA, ANDA_O, CAM, CANC, CHECK, CONC, EX1, EX2, FREQS, MAIOR, MENOR, MESES, NAOALC, NINI, ORIGENS, RISCO, SEMR, STATUS,  # noqa: E402
                      atrasada, caminho, situacao, ultimo)

BLUE, TEAL, AMBER, PURPLE, REDC = "2B5C8A", "1E7B73", "A96A12", "7A4A9A", "B0413E"
S1, S2, S3 = "2A6FB0", "D19A2E", "B0413E"
S1_T, S2_T, S3_T = "DCE8F3", "F8EBCB", "F5DEDC"
YESNO = ["Sim", "Parcial", "Não"]
YESNO_CF = [("Sim", GREEN), ("Parcial", YELLOW), ("Não", RED)]
SIT_CF = [(ALC, S1_T), (CAM, S2_T), (RISCO, S3_T), (NAOALC, S3_T), (ANDA_O, GRAY), (SEMR, GRAY)]
NO, NA, NM = 12, 36, 12
OB, PL, AC = "Objetivos", "Planos", "Acompanhamento"
C1, C2 = 7, 10                  # compromissos da política, na aba Objetivos
O1, O2 = 14, 14 + NO - 1        # objetivos, na aba Objetivos
A1, A2 = 7, 7 + NA - 1          # ações, na aba Planos
M1, M2 = 7, 7 + NO - 1          # objetivos, na aba Acompanhamento
MC = [get_column_letter(8 + j) for j in range(NM)]   # colunas H a S dos períodos
MR = f"{MC[0]}{{r}}:{MC[-1]}{{r}}"
IDS = [f"O{k + 1}" for k in range(NO)]
GERAL = "#,##0.##"


def note(ws, ref, text):
    c = Comment(text, "Modelo Objetivos")
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
    n = max(max(1, math.ceil(len(str(t)) / max(c, 1))) for t, c in pares)
    return max(minimo, n * linha + 7)


def mil(v):
    return f"{v:,}".replace(",", ".")


def f_sit(ult, meta, sentido, base, prazo, ref):
    """Situação de um objetivo: a regra do módulo 7 do treinamento."""
    at = f'IF({sentido}="{MAIOR}",{ult}>={meta},{ult}<={meta})'
    mel = f'IF({sentido}="{MAIOR}",{ult}>{base},{ult}<{base})'
    return (f'IF({ult}="","{SEMR}",IF({at},"{ALC}",IF(AND(ISNUMBER({prazo}),ISNUMBER({ref}),{prazo}<{ref}),"{NAOALC}",'
            f'IF({base}="","{ANDA_O}",IF({mel},"{CAM}","{RISCO}")))))')


def f_cam(ult, meta, sentido, base):
    """Caminho percorrido, de 0 a 1. Objetivo de manutenção: 1 se atende, 0 se não."""
    at = f'IF({sentido}="{MAIOR}",{ult}>={meta},{ult}<={meta})'
    manut = f'IF({sentido}="{MAIOR}",{meta}<={base},{meta}>={base})'
    return f'IF(OR({ult}="",{base}="",{meta}=""),"",IF({manut},IF({at},1,0),MAX(0,MIN(1,({ult}-{base})/({meta}-{base})))))'


def chart_style(ch):
    ch.style = 2
    ch.title = None
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill="D3DBE0", w=9525))
    ch.x_axis.graphicalProperties = GraphicalProperties(ln=LineProperties(solidFill="D3DBE0", w=9525))
    ch.y_axis.graphicalProperties = GraphicalProperties(ln=LineProperties(noFill=True))


def barras(ws, anchor, r1, r2, c_cat, c_val, width=19, height=9.5):
    """Barras horizontais com o caminho percorrido de cada objetivo."""
    ch = BarChart()
    ch.type = "bar"
    ch.gapWidth = 60
    ch.height, ch.width = height, width
    chart_style(ch)
    ch.legend = None
    s = Series(Reference(ws, min_col=c_val, min_row=r1, max_row=r2), title="Caminho percorrido")
    s.graphicalProperties.solidFill = BLUE
    s.graphicalProperties.line.noFill = True
    s.dLbls = DataLabelList()
    s.dLbls.showVal = True
    s.dLbls.numFmt = "0%"
    s.dLbls.showSerName = s.dLbls.showCatName = s.dLbls.showLegendKey = False
    ch.append(s)
    ch.set_categories(Reference(ws, min_col=c_cat, min_row=r1, max_row=r2))
    ch.y_axis.scaling.min, ch.y_axis.scaling.max = 0, 1
    ch.y_axis.majorUnit = 0.25
    ch.y_axis.number_format = "0%"
    ch.x_axis.scaling.orientation = "maxMin"
    ws.add_chart(ch, anchor)


# ================================================================== pasta de trabalho
wb = Workbook()
wb.properties.title = "Objetivos da qualidade — Modelo"
wb.properties.creator = "Modelo Objetivos"
wb.properties.language = "pt-BR"

# ------------------------------------------------------------------ Instruções
ws = wb.active
ws.title = "Instruções"
widths(ws, {"A": 2, "B": 24, "C": 92, "D": 2})
title(ws, "Objetivos da qualidade — Como usar esta planilha",
      "Modelo para escrever a política, definir os objetivos com medida, meta e prazo, planejar as ações e acompanhar o resultado.", "C")
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
line("Cinza", "Células calculadas ou fixas (rótulos, tipos, situações, caminho percorrido, avisos). Não altere.", vbg=GRAY)
line("Cinza em itálico", "Linha de exemplo (marcada com “Ex.”). Mostra o formato esperado e não entra nas contagens.", vbg=GRAY)
line("Listas suspensas", "Compromisso, origem, sentido, frequência, objetivo da ação, status e checklist aceitam apenas as opções da lista.")
line("Comentários", "Células com triângulo vermelho no canto trazem uma dica de preenchimento. Passe o mouse sobre elas.")
r += 1
section("As regras de cálculo")
for k, text in [
    ("Tipo do objetivo", "Melhorar: a meta é melhor do que a base. Manter: a meta é igual à base, ou pior. Realizar: o indicador conta etapas concluídas, e a base é zero."),
    ("Último resultado", "O último período preenchido na aba Acompanhamento. Períodos vazios no meio são ignorados."),
    (ALC, "O último resultado atende à meta, no sentido definido: maior ou menor é melhor."),
    (CAM, "Não atende à meta, e está melhor do que a base."),
    (RISCO, "Não atende à meta, e não está melhor do que a base."),
    (ANDA_O, "Não atende à meta, e não há base para comparar."),
    (NAOALC, "O prazo do objetivo é anterior à data da análise, e a meta não foi atendida."),
    ("Caminho percorrido", "(Último − base) ÷ (meta − base), de 0% a 100%. Para o objetivo de manutenção: 100% se atende, 0% se não."),
    ("Ação atrasada", "Ação não iniciada ou em andamento com prazo anterior à data da análise, informada na aba Painel."),
]:
    line(k, text)
r += 1
section("Ordem recomendada de preenchimento")
for k, text in enumerate([
    "Aba Objetivos: escreva a política da qualidade e os seus compromissos, em até quatro frases.",
    "Aba Objetivos: escreva cada objetivo, com compromisso, origem, indicador, unidade, sentido, base, meta, prazo, processo, responsável e frequência.",
    "Aba Planos: para cada objetivo, as ações, com recursos, responsável, prazo, status e como se avalia.",
    "Aba Acompanhamento: escreva os nomes dos períodos e lance os resultados conforme chegam.",
    "Aba Painel: informe a data da análise e leia a situação de cada objetivo, o caminho percorrido e as ações atrasadas.",
    "Aba Checklist: valide o quadro.",
], 1):
    line(f"Passo {k}", text)
r += 1
section("Abas da planilha")
for k, text in [
    (OB, f"A política, com até 4 compromissos, e até {NO} objetivos. Calcula o tipo e a conferência de cada um."),
    (PL, f"Até {NA} ações, ligadas aos objetivos pelo código. Calcula a conferência e as contagens."),
    (AC, f"Os resultados de cada objetivo em até {NM} períodos. Calcula o último resultado, o caminho e a situação."),
    ("Painel", "Os indicadores gerais, a leitura de cada objetivo, as ações atrasadas e o gráfico do caminho percorrido."),
    ("Checklist", "Doze verificações de qualidade do quadro, com percentual de conclusão."),
    ("Exemplo 1 - Pizzaria", "Os sete objetivos de 2027 da loja, com os planos e quatro meses de resultados."),
    ("Exemplo 2 - Indústria", "Os sete objetivos de 2027 da fábrica, com os planos e seis meses de resultados."),
]:
    line(k, text)
r += 1
section("Regras e premissas do modelo")
for k, text in [
    ("Poucos objetivos", f"O modelo aceita {NO}. O usual é de quatro a oito: o que não cabe vira indicador de rotina, ou fica para o ano seguinte."),
    ("Código do objetivo", "Os códigos O1 a O12 são fixos. Na aba Planos, cada ação é ligada ao objetivo pelo código."),
    ("Objetivo de realização", "Escreva as etapas no indicador (“etapas concluídas, de seis”), base 0 e meta igual ao número de etapas. Lance a cada mês quantas foram concluídas."),
    ("Exemplos", "Os dados das abas de exemplo são ilustrativos, criados para este material."),
]:
    line(k, text)
setup(ws, INK, f"B1:C{r}", landscape=False, fit_height=True)

# ------------------------------------------------------------------ Objetivos
ws = wb.create_sheet(OB)
widths(ws, {"A": 2, "B": 6, "C": 40, "D": 13, "E": 20, "F": 26, "G": 11, "H": 15, "I": 9, "J": 9, "K": 12, "L": 20, "M": 18, "N": 12, "O": 12, "P": 26, "Q": 2})
title(ws, "Política e objetivos da qualidade", "A política no alto, com os compromissos. Abaixo, os objetivos: cada um responde a um compromisso e a uma fonte.", "P")
label(ws, "B4", "Organização e período", merge="B4:C4")
inp(ws, "D4", merge="D4:P4", h="left")
label(ws, "B5", "Política da qualidade", merge="B5:C5")
inp(ws, "D5", merge="D5:P5", h="left")
ws.row_dimensions[4].height = 21.75
ws.row_dimensions[5].height = 36
for k in range(4):
    rr = C1 + k
    num(ws, f"B{rr}", f"C{k + 1}")
    label(ws, f"C{rr}", f"Compromisso {k + 1}", merge=None)
    inp(ws, f"D{rr}", merge=f"D{rr}:P{rr}", h="left")
    ws.row_dimensions[rr].height = 21.75
note(ws, "B5", "Os compromissos são as frases da política que podem virar objetivos. Escreva de um a quatro.")
for col, text in zip("BCDEFGHIJKLMNOP", ["#", "Objetivo", "Compromisso", "Origem", "Indicador", "Unidade", "Sentido", "Base", "Meta", "Prazo", "Processo ou área", "Responsável",
                                          "Frequência", "Tipo", "Conferência"]):
    head(ws, f"{col}12", text)
ws.row_dimensions[12].height = 33
hint_row(ws, 13, [("B", ""), ("C", "Verbo, resultado, meta e prazo"), ("D", "Lista"), ("E", "Lista"), ("F", "O que se mede"), ("G", "%, dias, etapas"), ("H", "Lista"),
                  ("I", "Partida"), ("J", "Alvo"), ("K", "Data"), ("L", "Quem entrega"), ("M", "Uma pessoa"), ("N", "Lista"), ("O", "Calculado"), ("P", "Calculada")])
for k in range(NO):
    rr = O1 + k
    num(ws, f"B{rr}", IDS[k])
    inp(ws, f"C{rr}")
    inp(ws, f"D{rr}", h="center")
    inp(ws, f"E{rr}")
    inp(ws, f"F{rr}")
    inp(ws, f"G{rr}", h="center")
    inp(ws, f"H{rr}", h="center")
    inp(ws, f"I{rr}", h="center", fmt=GERAL)
    inp(ws, f"J{rr}", h="center", fmt=GERAL)
    inp(ws, f"K{rr}", h="center", fmt=DATE)
    inp(ws, f"L{rr}")
    inp(ws, f"M{rr}")
    inp(ws, f"N{rr}", h="center")
    calc(ws, f"O{rr}", f'=IF(OR(C{rr}="",J{rr}="",H{rr}=""),"",IF(I{rr}="","Sem base",IF(IF(H{rr}="{MAIOR}",J{rr}>I{rr},J{rr}<I{rr}),"Melhorar","Manter")))', b=False, sz=9)
    calc(ws, f"P{rr}", f'=IF(C{rr}="","",IF(D{rr}="","Falta o compromisso",IF(F{rr}="","Falta o indicador",IF(J{rr}="","Falta a meta",IF(H{rr}="","Falta o sentido",'
         f'IF(K{rr}="","Falta o prazo",IF(M{rr}="","Falta o responsável",IF(COUNTIF({PL}!$C${A1}:$C${A2},B{rr})=0,"Sem ação no plano","OK"))))))))', b=False, sz=9)
    ws.row_dimensions[rr].height = 30
dv_list(ws, f"D{O1}:D{O2}", ["C1", "C2", "C3", "C4"], "O compromisso da política a que o objetivo responde")
dv_list(ws, f"E{O1}:E{O2}", ORIGENS, "De onde o objetivo veio")
dv_list(ws, f"H{O1}:H{O2}", [MAIOR, MENOR], "Maior é melhor, ou menor é melhor")
dv_list(ws, f"N{O1}:N{O2}", FREQS, "Com que frequência o resultado é lido")
dv_number(ws, f"I{O1}:J{O2}")
dv_date(ws, f"K{O1}:K{O2}")
cf_warn(ws, f"P{O1}:P{O2}", f"P{O1}")
cf_texto(ws, f"O{O1}:O{O2}", f"O{O1}", [("Sem base", YELLOW)])
note(ws, "C12", "Com verbo, resultado e número: “Reduzir as reclamações para no máximo 1,5 por 100 pedidos.”")
note(ws, "I12", "O valor de partida do indicador. Para um objetivo de realização, zero.")
note(ws, "J12", "O valor a alcançar. Para um objetivo de realização, o número de etapas.")
s = O2 + 2
band(ws, s, "Resumo automático", "P")
for k, (text, formula) in enumerate([
    ("Compromissos escritos", f"=COUNTA(D{C1}:D{C2})"),
    ("Objetivos escritos", f"=COUNTA(C{O1}:C{O2})"),
    ("Por tipo", f'=IF(D{s+2}=0,"",COUNTIF(O{O1}:O{O2},"Melhorar")&" de melhorar, "&COUNTIF(O{O1}:O{O2},"Manter")&" de manter, "&COUNTIF(O{O1}:O{O2},"Sem base")&" sem base")'),
    ("Aviso", f'=IF(D5="","Escreva a política da qualidade",IF(D{s+1}=0,"Escreva os compromissos",IF(D{s+2}=0,"Escreva os objetivos",'
              f'IF(COUNTIF(P{O1}:P{O2},"OK")<D{s+2},"Há objetivo a rever: veja a coluna Conferência",IF(D{s+2}>8,"Muitos objetivos: o usual é de quatro a oito","OK")))))'),
], 1):
    label(ws, f"B{s+k}", text, merge=f"B{s+k}:C{s+k}", h="right")
    calc(ws, f"D{s+k}", formula, merge=f"D{s+k}:P{s+k}", sz=9 if text == "Aviso" else 10, b=text != "Aviso", h="left")
    ws.row_dimensions[s + k].height = 21.75
cf_warn(ws, f"D{s+4}:P{s+4}", f"D{s+4}")
OAV = s + 4
ws.freeze_panes = "D14"
setup(ws, BLUE, f"B1:P{s+4}", fit_height=True)

# ------------------------------------------------------------------ Planos
ws = wb.create_sheet(PL)
widths(ws, {"A": 2, "B": 5, "C": 9, "D": 30, "E": 38, "F": 26, "G": 18, "H": 12, "I": 14, "J": 12, "K": 30, "L": 26, "M": 2})
title(ws, "Planos para alcançar os objetivos", "Uma linha por ação. As cinco respostas do requisito 6.2.2: o quê, recursos, quem, até quando e como se avalia.", "L")
for col, text in zip("BCDEFGHIJKL", ["#", "Objetivo", "Objetivo (texto)", "O que será feito", "Recursos", "Responsável", "Até quando", "Status", "Concluída em", "Como se avalia o resultado",
                                      "Conferência"]):
    head(ws, f"{col}4", text)
ws.row_dimensions[4].height = 33
hint_row(ws, 5, [("B", ""), ("C", "Código"), ("D", "Vem da aba Objetivos"), ("E", "Com verbo"), ("F", "Pessoas, dinheiro, tempo"), ("G", "Uma pessoa"), ("H", "Data"), ("I", "Lista"),
                 ("J", "Data"), ("K", "A medida que dirá se funcionou"), ("L", "Calculada")])
ex(ws, "B6", "Ex.", h="center")
for col, v, h_, fmt in [("C", "O1", "center", None), ("D", "Entregar 96% dos pedidos em até 40 minutos.", "left", None), ("E", "Rever a escala do pico em março.", "left", None),
                        ("F", "Mais dois entregadores extras nas sextas e nos sábados", "left", None), ("G", "Líder da expedição", "left", None), ("H", date(2027, 3, 31), "center", DATE),
                        ("I", CONC, "center", None), ("J", date(2027, 3, 26), "center", DATE), ("K", "Entregas no prazo nas noites de pico, por semana.", "left", None), ("L", "OK", "center", None)]:
    ex(ws, f"{col}6", v, h=h_, fmt=fmt)
ws.row_dimensions[6].height = 30
for k in range(NA):
    rr = A1 + k
    num(ws, f"B{rr}", k + 1)
    inp(ws, f"C{rr}", h="center")
    calc(ws, f"D{rr}", f'=IF(C{rr}="","",IFERROR(INDEX({OB}!$C${O1}:$C${O2},MATCH(C{rr},{OB}!$B${O1}:$B${O2},0)),"Código inválido"))', h="left", b=False, sz=9)
    inp(ws, f"E{rr}")
    inp(ws, f"F{rr}")
    inp(ws, f"G{rr}")
    inp(ws, f"H{rr}", h="center", fmt=DATE)
    inp(ws, f"I{rr}", h="center")
    inp(ws, f"J{rr}", h="center", fmt=DATE)
    inp(ws, f"K{rr}")
    calc(ws, f"L{rr}", f'=IF(E{rr}="","",IF(C{rr}="","Falta o objetivo",IF(D{rr}="","Objetivo sem texto na aba Objetivos",IF(G{rr}="","Falta o responsável",IF(H{rr}="","Falta o prazo",'
         f'IF(I{rr}="","Falta o status",IF(AND(I{rr}="{CONC}",J{rr}=""),"Falta a data de conclusão",IF(K{rr}="","Falta como se avalia",'
         f'IF(AND(ISNUMBER(H{rr}),IFERROR(H{rr}>INDEX({OB}!$K${O1}:$K${O2},MATCH(C{rr},{OB}!$B${O1}:$B${O2},0)),FALSE)),"Prazo depois do prazo do objetivo","OK")))))))))', b=False, sz=9)
    ws.row_dimensions[rr].height = 30
dv_list(ws, f"C{A1}:C{A2}", IDS, "Código do objetivo, da aba Objetivos")
dv_list(ws, f"I{A1}:I{A2}", STATUS, "Status da ação")
dv_date(ws, f"H{A1}:H{A2}")
dv_date(ws, f"J{A1}:J{A2}")
cf_texto(ws, f"I{A1}:I{A2}", f"I{A1}", [(CONC, GREEN), (ANDA, S1_T), (NINI, YELLOW), (CANC, GRAY)])
cf_warn(ws, f"L{A1}:L{A2}", f"L{A1}")
note(ws, "H4", "O prazo da ação vem antes do prazo do objetivo. A conferência avisa quando não vem.")
note(ws, "K4", "A medida que dirá se a ação funcionou: um indicador, um registro ou uma verificação, com frequência.")
s = A2 + 2
band(ws, s, "Resumo automático", "L")
for k, (text, formula) in enumerate([
    ("Ações escritas", f"=COUNTA(E{A1}:E{A2})"),
    ("Concluídas", f'=COUNTIF(I{A1}:I{A2},"{CONC}")'),
    ("Em andamento e não iniciadas", f'=COUNTIF(I{A1}:I{A2},"{ANDA}")+COUNTIF(I{A1}:I{A2},"{NINI}")'),
    ("Aviso", f'=IF(E{s+1}=0,"Escreva as ações",IF(COUNTIF(L{A1}:L{A2},"OK")<E{s+1},"Há ação a rever: veja a coluna Conferência","OK"))'),
], 1):
    label(ws, f"B{s+k}", text, merge=f"B{s+k}:D{s+k}", h="right")
    calc(ws, f"E{s+k}", formula, merge=f"E{s+k}:G{s+k}", sz=9 if text == "Aviso" else 10, b=text != "Aviso", h="left")
    ws.row_dimensions[s + k].height = 21.75
cf_warn(ws, f"E{s+4}:G{s+4}", f"E{s+4}")
PAV = s + 4
ws.freeze_panes = "E7"
setup(ws, AMBER, f"B1:L{s+4}", fit_height=True)

# ------------------------------------------------------------------ Acompanhamento
ws = wb.create_sheet(AC)
widths(ws, dict({"A": 2, "B": 6, "C": 30, "D": 10, "E": 9, "F": 9, "G": 9, "T": 10, "U": 11, "V": 15, "W": 2}, **{c: 8 for c in MC}))
title(ws, "Acompanhamento dos objetivos", "Lance o resultado de cada objetivo a cada período. O último resultado, o caminho e a situação são calculados.", "V")
label(ws, "B4", "Data da análise", merge="B4:C4")
inp(ws, "D4", h="center", fmt=DATE)
put(ws, "E4", "Usada para ler o prazo dos objetivos e das ações. Também aparece no Painel.", f=font(9, i=True, c=MUTED), bg=GRAY, merge="E4:V4")
dv_date(ws, "D4")
ws.row_dimensions[4].height = 21.75
for col, text in zip("BCDEFG", ["#", "Indicador", "Unidade", "Sentido", "Base", "Meta"]):
    head(ws, f"{col}6", text)
for j, c in enumerate(MC):
    inp(ws, f"{c}6", MESES[j], h="center")
    ws[f"{c}6"].font = font(10, True)
for col, text in zip("TUV", ["Último", "Caminho", "Situação"]):
    head(ws, f"{col}6", text)
ws.row_dimensions[6].height = 33
note(ws, f"{MC[0]}6", "Os nomes dos períodos: meses, trimestres ou semestres. Edite conforme a frequência.")
for k in range(NO):
    rr = M1 + k
    orow = O1 + k
    rng = MR.format(r=rr)
    num(ws, f"B{rr}", IDS[k])
    calc(ws, f"C{rr}", f'=IF({OB}!F{orow}="","",{OB}!F{orow})', h="left", b=False, sz=9)
    calc(ws, f"D{rr}", f'=IF({OB}!G{orow}="","",{OB}!G{orow})', b=False, sz=9)
    calc(ws, f"E{rr}", f'=IF({OB}!H{orow}="","",IF({OB}!H{orow}="{MAIOR}","Maior","Menor"))', b=False, sz=9)
    calc(ws, f"F{rr}", f'=IF({OB}!I{orow}="","",{OB}!I{orow})', b=False, fmt=GERAL)
    calc(ws, f"G{rr}", f'=IF({OB}!J{orow}="","",{OB}!J{orow})', b=False, fmt=GERAL)
    for c in MC:
        inp(ws, f"{c}{rr}", h="center", fmt=GERAL)
    calc(ws, f"T{rr}", f'=IF(COUNT({rng})=0,"",LOOKUP(2,1/ISNUMBER({rng}),{rng}))', fmt=GERAL)
    calc(ws, f"U{rr}", "=" + f_cam(f"T{rr}", f"G{rr}", f"{OB}!H{orow}", f"F{rr}"), fmt="0%", b=False)
    calc(ws, f"V{rr}", f'=IF(OR(C{rr}="",G{rr}=""),"",{f_sit(f"T{rr}", f"G{rr}", f"{OB}!H{orow}", f"F{rr}", f"{OB}!K{orow}", "$D$4")})', b=False, sz=9)
    ws.row_dimensions[rr].height = 21.75
dv_number(ws, f"{MC[0]}{M1}:{MC[-1]}{M2}")
cf_texto(ws, f"V{M1}:V{M2}", f"V{M1}", SIT_CF)
# resultado que atende à meta, em azul-claro
ws.conditional_formatting.add(f"{MC[0]}{M1}:{MC[-1]}{M2}", FormulaRule(formula=[f'AND(ISNUMBER({MC[0]}{M1}),$G{M1}<>"",IF($E{M1}="Maior",{MC[0]}{M1}>=$G{M1},{MC[0]}{M1}<=$G{M1}))'],
                              fill=PatternFill("solid", bgColor=S1_T, fgColor=S1_T)))
s = M2 + 2
band(ws, s, "Resumo automático", "V")
for k, (text, formula) in enumerate([
    ("Objetivos com resultado", f'=COUNTIF(V{M1}:V{M2},"<>{SEMR}")-COUNTBLANK(V{M1}:V{M2})'),
    ("Por situação", f'=IF(COUNTA(C{M1}:C{M2})=0,"",COUNTIF(V{M1}:V{M2},"{ALC}")&" alcançados, "&COUNTIF(V{M1}:V{M2},"{CAM}")&" no caminho, "&COUNTIF(V{M1}:V{M2},"{RISCO}")&" em risco, "'
                     f'&COUNTIF(V{M1}:V{M2},"{ANDA_O}")&" em andamento, "&COUNTIF(V{M1}:V{M2},"{NAOALC}")&" não alcançados, "&COUNTIF(V{M1}:V{M2},"{SEMR}")&" sem resultado")'),
    ("Aviso", f'=IF(COUNTA(C{M1}:C{M2})=0,"Escreva os objetivos na aba Objetivos",IF(D4="","Informe a data da análise",IF(COUNTIF(V{M1}:V{M2},"{SEMR}")>0,"Há objetivo sem resultado",'
              f'IF(COUNTIF(V{M1}:V{M2},"{NAOALC}")>0,"Há objetivo com prazo vencido sem alcançar a meta: decida na análise crítica",IF(COUNTIF(V{M1}:V{M2},"{RISCO}")>0,"Há objetivo em risco: veja as ações","OK")))))'),
], 1):
    label(ws, f"B{s+k}", text, merge=f"B{s+k}:C{s+k}", h="right")
    calc(ws, f"D{s+k}", formula, merge=f"D{s+k}:V{s+k}", sz=9 if text == "Aviso" else 10, b=text != "Aviso", h="left")
    ws.row_dimensions[s + k].height = 21.75
cf_warn(ws, f"D{s+3}:V{s+3}", f"D{s+3}")
AAV = s + 3
ws.freeze_panes = f"{MC[0]}7"
setup(ws, TEAL, f"B1:V{s+3}", fit_height=True)

# ------------------------------------------------------------------ Painel
ws = wb.create_sheet("Painel")
widths(ws, {"A": 2, "B": 6, "C": 36, "D": 16, "E": 11, "F": 11, "G": 11, "H": 13, "I": 11, "J": 11, "K": 11, "L": 28, "M": 2})
title(ws, "Painel dos objetivos", "A situação de cada objetivo, o caminho percorrido e as ações. A data da análise vem da aba Acompanhamento.", "L")
label(ws, "B4", "Data da análise", merge="B4:C4")
calc(ws, "D4", f'=IF({AC}!D4="","",{AC}!D4)', fmt=DATE)
put(ws, "E4", "Informe na aba Acompanhamento.", f=font(9, i=True, c=MUTED), bg=GRAY, merge="E4:L4")
ws.row_dimensions[4].height = 21.75
for col, text, m in [("B", "Indicador", "B6:C6"), ("D", "Resultado", None), ("E", "Como se lê", "E6:L6")]:
    put(ws, f"{col}6", text, f=font(10, True, c=WHITE), bg=INK, h="center", merge=m)
ws.row_dimensions[6].height = 21.75
V_ = f"{AC}!V{M1}:V{M2}"
I_, H_, C_ = (f"{PL}!{c}{A1}:{c}{A2}" for c in "IHC")
ATR = f'SUMPRODUCT((({I_}="{NINI}")+({I_}="{ANDA}"))*ISNUMBER({H_})*({H_}<$D$4))'
IND = [
    ("Objetivos escritos", f"=COUNTA({OB}!C{O1}:C{O2})", None, "Da aba Objetivos. O usual é de quatro a oito."),
    (ALC, f'=COUNTIF({V_},"{ALC}")', None, "O último resultado atende à meta."),
    (CAM, f'=COUNTIF({V_},"{CAM}")', None, "Não atende, mas está melhor do que a base."),
    (RISCO, f'=COUNTIF({V_},"{RISCO}")', None, "Não atende, e não está melhor do que a base: olhar as ações."),
    ("Não alcançados ou sem resultado", f'=COUNTIF({V_},"{NAOALC}")+COUNTIF({V_},"{SEMR}")', None, "Prazo vencido sem a meta, ou nenhum resultado lançado."),
    ("Caminho percorrido, em média", f'=IF(COUNT({AC}!U{M1}:U{M2})=0,"",AVERAGE({AC}!U{M1}:U{M2}))', "0%", "Média dos objetivos com base e resultado."),
    ("Ações: escritas, concluídas", f'=COUNTA({PL}!E{A1}:E{A2})&" escritas, "&COUNTIF({I_},"{CONC}")&" concluídas"', None, "Da aba Planos."),
    ("Ações atrasadas", f'=IF($D$4="","",{ATR})', None, "Não iniciadas ou em andamento, com prazo anterior à data da análise."),
]
for k, (nome, formula, fmt, leitura) in enumerate(IND):
    rr = 7 + k
    label(ws, f"B{rr}", nome, merge=f"B{rr}:C{rr}")
    calc(ws, f"D{rr}", formula, fmt=fmt)
    put(ws, f"E{rr}", leitura, f=font(9, c=MUTED), bg=GRAY, merge=f"E{rr}:L{rr}")
    ws.row_dimensions[rr].height = 21.75
I2 = 7 + len(IND) - 1
T0 = I2 + 2
band(ws, T0, "Leitura de cada objetivo", "L")
for col, text in zip("BCDEFGHIJKL", ["#", "Objetivo", "Compromisso", "Base", "Último", "Meta", "Situação", "Caminho", "Ações", "Atrasadas", "Leitura"]):
    head(ws, f"{col}{T0+1}", text)
ws.row_dimensions[T0 + 1].height = 33
T1, T2 = T0 + 2, T0 + 1 + NO
for k in range(NO):
    rr = T1 + k
    orow, arow = O1 + k, M1 + k
    num(ws, f"B{rr}", IDS[k])
    calc(ws, f"C{rr}", f'=IF({OB}!C{orow}="","",{OB}!C{orow})', h="left", b=False, sz=9)
    calc(ws, f"D{rr}", f'=IF(C{rr}="","",{OB}!D{orow})', b=False)
    calc(ws, f"E{rr}", f'=IF(C{rr}="","",{AC}!F{arow})', b=False, fmt=GERAL)
    calc(ws, f"F{rr}", f'=IF(C{rr}="","",{AC}!T{arow})', fmt=GERAL)
    calc(ws, f"G{rr}", f'=IF(C{rr}="","",{AC}!G{arow})', b=False, fmt=GERAL)
    calc(ws, f"H{rr}", f'=IF(C{rr}="","",{AC}!V{arow})', b=False, sz=9)
    calc(ws, f"I{rr}", f'=IF(C{rr}="","",{AC}!U{arow})', fmt="0%", b=False)
    calc(ws, f"J{rr}", f'=IF(C{rr}="","",COUNTIF({C_},B{rr}))', b=False)
    calc(ws, f"K{rr}", f'=IF(OR(C{rr}="",$D$4=""),"",SUMPRODUCT(({C_}=B{rr})*(({I_}="{NINI}")+({I_}="{ANDA}"))*ISNUMBER({H_})*({H_}<$D$4)))', b=False)
    calc(ws, f"L{rr}", f'=IF(C{rr}="","",IF(J{rr}=0,"Sem plano",IF(H{rr}="{ALC}","Manter até o prazo",IF(H{rr}="{NAOALC}","Decidir na análise crítica",'
         f'IF(N(K{rr})>0,"Ação atrasada: cobrar",IF(H{rr}="{RISCO}","Ação feita e não bastou? Rever o plano",IF(H{rr}="{SEMR}","Lançar o resultado","Acompanhar o ritmo")))))))', b=False, sz=9, h="left")
    ws.row_dimensions[rr].height = 27
cf_texto(ws, f"H{T1}:H{T2}", f"H{T1}", SIT_CF)
cf_texto(ws, f"L{T1}:L{T2}", f"L{T1}", [("Manter até o prazo", GREEN), ("Acompanhar o ritmo", S1_T), ("Sem plano", RED), ("Ação atrasada: cobrar", RED), ("Decidir na análise crítica", RED)], resto=YELLOW)
s = T2 + 2
band(ws, s, "Resumo automático", "L")
label(ws, f"B{s+1}", "Objetivos por compromisso", merge=f"B{s+1}:C{s+1}", h="right")
calc(ws, f"D{s+1}", f'=IF(D7=0,"",COUNTIF(D{T1}:D{T2},"C1")&" em C1, "&COUNTIF(D{T1}:D{T2},"C2")&" em C2, "&COUNTIF(D{T1}:D{T2},"C3")&" em C3, "&COUNTIF(D{T1}:D{T2},"C4")&" em C4")', h="left", merge=f"D{s+1}:L{s+1}")
label(ws, f"B{s+2}", "Aviso", merge=f"B{s+2}:C{s+2}", h="right")
calc(ws, f"D{s+2}", f'=IF(D7=0,"Escreva os objetivos na aba Objetivos",IF(D4="","Informe a data da análise na aba Acompanhamento",IF(COUNTIF(L{T1}:L{T2},"Sem plano")>0,"Há objetivo sem plano",'
     f'IF(N(D14)>0,"Há ação atrasada: veja a aba Planos",IF(D11>0,"Há objetivo não alcançado ou sem resultado",IF(D10>0,"Há objetivo em risco: leve à reunião","OK"))))))',
     sz=9, b=False, h="left", merge=f"D{s+2}:L{s+2}")
cf_warn(ws, f"D{s+2}:L{s+2}", f"D{s+2}")
for k in (1, 2):
    ws.row_dimensions[s + k].height = 21.75
NAV = s + 2
barras(ws, f"B{s + 4}", T1, T2, 2, 9, width=24, height=10)
setup(ws, REDC, f"B1:L{s + 25}", landscape=False, fit_height=True)

# ------------------------------------------------------------------ Checklist
ws = wb.create_sheet("Checklist")
widths(ws, {"A": 2, "B": 5, "C": 70, "D": 14, "E": 44, "F": 2})
title(ws, "Checklist dos objetivos da qualidade", "Escolha o status de cada item na lista suspensa (coluna em amarelo-claro).", "E")
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


def exemplo(ws, ex):
    H = ex["head"]
    n = H["meses"]
    widths(ws, {"A": 2, "B": 6, "C": 34, "D": 14, "E": 12, "F": 9, "G": 9, "H": 11, "I": 18, "J": 16, "K": 13, "L": 11, "M": 2})
    title(ws, "Objetivos da qualidade", "Exemplo preenchido, para consulta. Use as abas Objetivos, Planos e Acompanhamento para a sua organização.", "L")
    rr = 4
    for rot, val in [("Organização", H["org"]), ("Definição", f'{H["data"]:%d/%m/%Y}. {H["por"]}. {H["periodo"]}.'), ("Política da qualidade", H["politica"]), ("Origem", H["origem"]),
                     ("Data da análise", H["ref"])]:
        label(ws, f"B{rr}", rot, merge=f"B{rr}:C{rr}")
        inp(ws, f"D{rr}", val, merge=f"D{rr}:L{rr}", bg=WHITE, h="left", fmt=DATE if rot == "Data da análise" else None)
        ws.row_dimensions[rr].height = alt([(val, 120)], minimo=19.5)
        rr += 1
    REF = f"$D${rr - 1}"
    for c, t in ex["comps"]:
        label(ws, f"B{rr}", c, merge=f"B{rr}:C{rr}", h="right")
        put(ws, f"D{rr}", t, merge=f"D{rr}:L{rr}")
        ws.row_dimensions[rr].height = 19.5
        rr += 1
    rr += 1
    band(ws, rr, "Quadro de objetivos", "L", color=BLUE)
    rr += 1
    sub(ws, rr, [("B", None, "#"), ("C", None, "Objetivo"), ("D", None, "Compromisso"), ("E", None, "Origem"), ("F", None, "Base"), ("G", None, "Meta"), ("H", None, "Prazo"),
                 ("I", None, "Indicador"), ("J", None, "Responsável"), ("K", None, "Sentido"), ("L", None, "Tipo")])
    o1 = rr + 1
    for o in ex["objs"]:
        rr += 1
        num(ws, f"B{rr}", o["id"])
        put(ws, f"C{rr}", o["texto"], f=font(10, True))
        put(ws, f"D{rr}", o["comp"], h="center")
        put(ws, f"E{rr}", o["origem"])
        put(ws, f"F{rr}", o["base"] if o["base"] is not None else "—", h="center", fmt=GERAL)
        put(ws, f"G{rr}", o["meta"], h="center", fmt=GERAL)
        put(ws, f"H{rr}", o["prazo"], h="center", fmt=DATE)
        put(ws, f"I{rr}", f'{o["ind"]} ({o["unid"]})')
        put(ws, f"J{rr}", o["resp"])
        put(ws, f"K{rr}", "Maior" if o["sentido"] == MAIOR else "Menor", h="center")
        calc(ws, f"L{rr}", f'=IF(ISNUMBER(F{rr})=FALSE,"Sem base",IF(IF(K{rr}="Maior",G{rr}>F{rr},G{rr}<F{rr}),"Melhorar","Manter"))', b=False, sz=9)
        ws.row_dimensions[rr].height = alt([(o["texto"], 36), (o["ind"] + o["unid"], 18), (o["origem"], 12)], minimo=21.75)
    o2 = rr
    rr += 2
    ws.row_breaks.append(Break(id=rr - 1))
    band(ws, rr, "Planos", "L", color=AMBER)
    rr += 1
    sub(ws, rr, [("B", None, "Obj."), ("C", None, "O que será feito"), ("D", "E", "Recursos"), ("F", "G", "Até quando"), ("H", None, "Status"), ("I", None, "Concluída em"),
                 ("J", None, "Responsável"), ("K", "L", "Como se avalia")])
    a1 = rr + 1
    for o in ex["objs"]:
        for a in o["acoes"]:
            rr += 1
            num(ws, f"B{rr}", o["id"])
            put(ws, f"C{rr}", a["oque"])
            put(ws, f"D{rr}", a["rec"] or "—", merge=f"D{rr}:E{rr}")
            put(ws, f"F{rr}", a["prazo"], h="center", fmt=DATE, merge=f"F{rr}:G{rr}")
            calc(ws, f"H{rr}", f'=IF(AND(OR(I{rr}="{NINI}",I{rr}="{ANDA}"),F{rr}<{REF}),"Atrasada",I{rr})', b=False, sz=9)
            put(ws, f"I{rr}", a["status"], h="center")
            ws[f"I{rr}"].number_format = "@"
            put(ws, f"J{rr}", a["resp"])
            put(ws, f"K{rr}", a["avalia"], merge=f"K{rr}:L{rr}")
            ws.row_dimensions[rr].height = alt([(a["oque"], 36), (a["rec"] or "", 26), (a["avalia"], 26)], minimo=21.75)
    # a coluna I guarda o status informado; a H mostra a leitura na data da análise
    a2 = rr
    cf_texto(ws, f"H{a1}:H{a2}", f"H{a1}", [(CONC, GREEN), ("Atrasada", RED), (ANDA, S1_T), (NINI, YELLOW)])
    sub(ws, a1 - 1, [("H", None, "Leitura"), ("I", None, "Status")], height=30)
    rr += 2
    ws.row_breaks.append(Break(id=rr - 1))
    band(ws, rr, "Acompanhamento", "L", color=TEAL)
    rr += 1
    cols = [get_column_letter(4 + j) for j in range(n)]       # D em diante, um por período
    assert n <= 6
    cu, cc, cs = get_column_letter(4 + n), get_column_letter(5 + n), get_column_letter(6 + n)
    sub(ws, rr, [("B", None, "#"), ("C", None, "Indicador")] + [(c, None, MESES[j]) for j, c in enumerate(cols)] + [(cu, None, "Último"), (cc, None, "Caminho"), (cs, "L", "Situação")])
    m1 = rr + 1
    for k, o in enumerate(ex["objs"]):
        rr += 1
        orow = o1 + k
        num(ws, f"B{rr}", o["id"])
        put(ws, f"C{rr}", o["ind"], f=font(10, True))
        for c, v in zip(cols, o["res"]):
            put(ws, f"{c}{rr}", v if v is not None else "—", h="center", fmt=GERAL)
        rng = f"{cols[0]}{rr}:{cols[-1]}{rr}"
        calc(ws, f"{cu}{rr}", f'=IF(COUNT({rng})=0,"",LOOKUP(2,1/ISNUMBER({rng}),{rng}))', fmt=GERAL)
        sent = f'IF(K{orow}="Maior","{MAIOR}","{MENOR}")'
        base = f'IF(ISNUMBER(F{orow}),F{orow},"")'
        calc(ws, f"{cc}{rr}", "=" + f_cam(f"{cu}{rr}", f"G{orow}", sent, base), fmt="0%", b=False)
        calc(ws, f"{cs}{rr}", "=" + f_sit(f"{cu}{rr}", f"G{orow}", sent, base, f"H{orow}", REF), b=False, sz=9, merge=f"{cs}{rr}:L{rr}" if cs != "L" else None)
        ws.row_dimensions[rr].height = 21.75
    m2 = rr
    cf_texto(ws, f"{cs}{m1}:L{m2}", f"{cs}{m1}", SIT_CF)
    rr += 2
    band(ws, rr, "Resumo automático", "L")
    for k, (text, formula, fmt) in enumerate([
        ("Objetivos", f"=COUNTA(C{o1}:C{o2})", None),
        ("Por situação", f'=COUNTIF({cs}{m1}:{cs}{m2},"{ALC}")&" alcançados, "&COUNTIF({cs}{m1}:{cs}{m2},"{CAM}")&" no caminho, "&COUNTIF({cs}{m1}:{cs}{m2},"{RISCO}")&" em risco"', None),
        ("Ações: escritas, concluídas, atrasadas", f'=COUNTA(C{a1}:C{a2})&" escritas, "&COUNTIF(H{a1}:H{a2},"{CONC}")&" concluídas, "&COUNTIF(H{a1}:H{a2},"Atrasada")&" atrasadas"', None),
        ("Caminho percorrido, em média", f"=AVERAGE({cc}{m1}:{cc}{m2})", "0%"),
    ], 1):
        label(ws, f"B{rr+k}", text, merge=f"B{rr+k}:E{rr+k}", h="right")
        calc(ws, f"F{rr+k}", formula, fmt=fmt, merge=f"F{rr+k}:L{rr+k}", h="left")
        ws.row_dimensions[rr + k].height = 21.75
    setup(ws, MUTED, f"B1:L{rr + 4}")


exemplo(wb.create_sheet("Exemplo 1 - Pizzaria"), EX1)
exemplo(wb.create_sheet("Exemplo 2 - Indústria"), EX2)

wb.active = 1
wb.save(OUT)
print("ok", OUT, "| avisos: Objetivos D%d, Planos E%d, Acompanhamento D%d, Painel D%d" % (OAV, PAV, AAV, NAV))
