# -*- coding: utf-8 -*-
"""Gera Satisfacao-modelo.xlsx no mesmo padrão visual das planilhas anteriores da série."""
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
from sat_data import CHECK, DETRATOR, EX1, EX2, NEUTRO, PRAZO_RESPOSTA, PRAZO_SOLUCAO, PROMOTOR, SATISFEITO, resumo_mes  # noqa: E402

BLUE, TEAL, AMBER, PURPLE, REDC = "2B5C8A", "1E7B73", "A96A12", "7A4A9A", "B0413E"
BLUE_T, AMBER_T, RED_T = "DCE8F3", "F8EBCB", "F5DEDC"
YESNO = ["Sim", "Parcial", "Não"]
YESNO_CF = [("Sim", GREEN), ("Parcial", YELLOW), ("Não", RED)]
CANAIS = ["Telefone", "Mensagem", "Aplicativo", "E-mail", "Presencial", "Site"]
SITS = ["Aberta", "Respondida", "Resolvida"]
NPER, NRES, NREC = 5, 60, 30
Q1 = 9                       # perguntas, na aba Pesquisa
R1, R2 = 7, 7 + NRES - 1     # respostas
C1, C2 = 7, 7 + NREC - 1     # reclamações
PQ = "Pesquisa"
PC = [chr(ord("E") + k) for k in range(NPER)]   # colunas E a I das notas, na aba Respostas
ESCALA = f"{PQ}!$D$6"
LIM = f"{PQ}!$D$7"


def note(ws, ref, text):
    c = Comment(text, "Modelo Satisfação")
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


def dv_numero(ws, rng_, minimo, maximo, prompt, inteiro=True):
    dv = DataValidation(type="whole" if inteiro else "decimal", operator="between", formula1=str(minimo), formula2=str(maximo), allow_blank=True)
    dv.promptTitle, dv.prompt, dv.showInputMessage = "Número", prompt, True
    dv.errorTitle, dv.error, dv.showErrorMessage = "Número inválido", f"Digite um número de {minimo} a {maximo}.", True
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


def barras(ws, anchor, r1, r2, c_cat, c_val, width=16, height=6.5, maximo=None, fmt="0.0"):
    ch = BarChart()
    ch.type = "bar"
    ch.gapWidth = 60
    ch.height, ch.width = height, width
    chart_style(ch)
    ch.legend = None
    s = Series(Reference(ws, min_col=c_val, min_row=r1, max_row=r2), title="Valor")
    s.graphicalProperties.solidFill = BLUE
    s.graphicalProperties.line.noFill = True
    s.dLbls = DataLabelList()
    s.dLbls.showVal = True
    s.dLbls.numFmt = fmt
    s.dLbls.showSerName = s.dLbls.showCatName = s.dLbls.showLegendKey = False
    ch.append(s)
    ch.set_categories(Reference(ws, min_col=c_cat, min_row=r1, max_row=r2))
    ch.y_axis.scaling.min = 0
    if maximo:
        ch.y_axis.scaling.max = maximo
    ch.y_axis.number_format = "0"
    ch.x_axis.scaling.orientation = "maxMin"
    ws.add_chart(ch, anchor)


# ================================================================== pasta de trabalho
wb = Workbook()
wb.properties.title = "Satisfação do cliente — Modelo"
wb.properties.creator = "Modelo Satisfação"
wb.properties.language = "pt-BR"

# ------------------------------------------------------------------ Instruções
ws = wb.active
ws.title = "Instruções"
widths(ws, {"A": 2, "B": 24, "C": 92, "D": 2})
title(ws, "Satisfação do cliente — Como usar esta planilha",
      "Modelo para definir a pesquisa, lançar as respostas, registrar as reclamações e ler os indicadores do período.", "C")
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
line("Cinza", "Células calculadas ou fixas (rótulos, médias, classificações, indicadores, avisos). Não altere.", vbg=GRAY)
line("Cinza em itálico", "Linha de exemplo (marcada com “Ex.”). Mostra o formato esperado e não entra nas contagens.", vbg=GRAY)
line("Listas suspensas", "Colunas de canal, situação e status aceitam apenas as opções da lista. As notas aceitam números dentro da escala.")
line("Comentários", "Células com triângulo vermelho no canto trazem uma dica de preenchimento. Passe o mouse sobre elas.")
r += 1
section("As regras de cálculo")
for k, text in [
    ("Escala", "As perguntas usam uma escala só, de 1 a 5 ou de 0 a 10, escolhida na aba Pesquisa. A nota máxima define o limite de satisfeito."),
    ("Satisfeito", f"Nota igual ou acima de {round(100 * SATISFEITO)}% da escala: 4 em 5, 8 em 10. Percentual de satisfeitos = notas nesse nível sobre as respostas."),
    ("Indicação", "Pergunta de 0 a 10. Promotor dá 9 ou 10; neutro, 7 ou 8; detrator, de 0 a 6. Indicação = promotores menos detratores, em percentual das respostas."),
    ("Reclamações por 100", "Reclamações do período ÷ pedidos do período × 100. Os pedidos são informados na aba Painel."),
    ("Prazos", f"Primeira resposta em até {PRAZO_RESPOSTA} dias úteis e solução em até {PRAZO_SOLUCAO} dias, neste modelo. A organização define os seus."),
]:
    line(k, text)
r += 1
section("Ordem recomendada de preenchimento")
for k, text in enumerate([
    "Aba Pesquisa: escreva o período, o canal, a escala e as perguntas, uma por coisa que o cliente valoriza.",
    "Aba Respostas: lance cada resposta, com as notas, a indicação e o comentário.",
    "Aba Reclamações: registre cada reclamação, com motivo, datas de resposta e de solução, e situação.",
    "Aba Painel: informe os pedidos ou clientes do período e as metas, e leia os indicadores.",
    "Escolha o motivo mais frequente e decida uma ação. Registre a devolutiva ao cliente.",
    "Aba Checklist: valide o sistema de satisfação.",
], 1):
    line(f"Passo {k}", text)
r += 1
section("Abas da planilha")
for k, text in [
    ("Pesquisa", f"Até {NPER} perguntas, com a escala, o período e o canal. Calcula o limite de satisfeito."),
    ("Respostas", f"Até {NRES} respostas. Calcula a média por pergunta, o percentual de satisfeitos e a classificação da indicação."),
    ("Reclamações", f"Até {NREC} reclamações. Calcula o prazo da primeira resposta e a situação de cada uma, e conta os motivos."),
    ("Painel", "Os indicadores do período, com meta e situação, e o gráfico das perguntas."),
    ("Checklist", "Doze verificações de qualidade do sistema, com percentual de conclusão."),
    ("Exemplo 1 - Pizzaria", "A pesquisa depois da entrega, por mês, com os motivos e as reclamações."),
    ("Exemplo 2 - Indústria", "A pesquisa anual, por segmento, com os motivos das reclamações."),
]:
    line(k, text)
r += 1
section("Regras e premissas do modelo")
for k, text in [
    ("Amostra", "O resultado vale para quem respondeu. A taxa de resposta aparece no Painel ao lado da nota."),
    ("Motivos", "Escreva o motivo da reclamação sempre com as mesmas palavras, para que a contagem por motivo funcione. Use a lista da aba Pesquisa."),
    ("Situação da reclamação", "Aberta: sem resposta. Respondida: com resposta, sem solução. Resolvida: com solução. A situação é calculada pelas datas."),
    ("Exemplos", "Os dados das abas de exemplo são ilustrativos, criados para este material."),
]:
    line(k, text)
setup(ws, INK, f"B1:C{r}", landscape=False, fit_height=True)

# ------------------------------------------------------------------ Pesquisa
ws = wb.create_sheet(PQ)
widths(ws, {"A": 2, "B": 8, "C": 44, "D": 30, "E": 30, "F": 2})
title(ws, "A pesquisa", "Defina o período, o canal, a escala e as perguntas. Uma pergunta por coisa que o cliente valoriza.", "E")
for rr, rot, val in [(4, "Organização", None), (5, "Período e canal", None), (6, "Escala: nota máxima (5 ou 10)", 5)]:
    label(ws, f"B{rr}", rot, merge=f"B{rr}:C{rr}")
    inp(ws, f"D{rr}", val, merge=f"D{rr}:E{rr}", h="left")
    ws.row_dimensions[rr].height = 21.75
dv_numero(ws, "D6", 5, 10, "5 para a escala de 1 a 5; 10 para a escala de 0 a 10.")
label(ws, "B7", "Nota mínima para contar como satisfeito", merge="B7:C7")
calc(ws, "D7", f"=IF(D6=\"\",\"\",CEILING({SATISFEITO}*D6,1))", h="left")
put(ws, "E7", f"{round(100 * SATISFEITO)}% da escala: 4 em 5, 8 em 10.", f=font(9, i=True, c=MUTED), bg=GRAY)
ws.row_dimensions[7].height = 21.75
for col, text in zip("BCDE", ["#", "Pergunta", "O que mede", "Conferência"]):
    head(ws, f"{col}8", text)
ws.row_dimensions[8].height = 21.75
for k in range(NPER):
    rr = Q1 + k
    num(ws, f"B{rr}", f"P{k + 1}")
    inp(ws, f"C{rr}")
    inp(ws, f"D{rr}")
    calc(ws, f"E{rr}", f'=IF(C{rr}="","",IF(LEN(C{rr})>80,"Pergunta longa: encurte",IF(OR(ISNUMBER(SEARCH(" e ",C{rr})),ISNUMBER(SEARCH(",",C{rr}))),"Pode estar juntando dois assuntos","OK")))', b=False, sz=9)
    ws.row_dimensions[rr].height = 27
cf_warn(ws, f"E{Q1}:E{Q1 + NPER - 1}", f"E{Q1}")
note(ws, "C8", 'Uma pergunta, uma coisa: "Como foi a entrega?". Evite juntar assuntos.')
label(ws, f"B{Q1 + NPER + 1}", "Pergunta de indicação, de 0 a 10", merge=f"B{Q1 + NPER + 1}:C{Q1 + NPER + 1}")
put(ws, f"D{Q1 + NPER + 1}", "Você indicaria a um amigo ou colega?", bg=GRAY, merge=f"D{Q1 + NPER + 1}:E{Q1 + NPER + 1}")
label(ws, f"B{Q1 + NPER + 2}", "Campo aberto", merge=f"B{Q1 + NPER + 2}:C{Q1 + NPER + 2}")
put(ws, f"D{Q1 + NPER + 2}", "O que podemos melhorar?", bg=GRAY, merge=f"D{Q1 + NPER + 2}:E{Q1 + NPER + 2}")
M1 = Q1 + NPER + 4
band(ws, M1 - 1, "Motivos de reclamação e de nota baixa: escreva sempre com as mesmas palavras", "E")
for k in range(8):
    rr = M1 + k
    num(ws, f"B{rr}", k + 1)
    inp(ws, f"C{rr}", merge=f"C{rr}:E{rr}")
    ws.row_dimensions[rr].height = 19.5
M2 = M1 + 7
note(ws, f"B{M1 - 1}", 'Ex.: "Entrega atrasada", "Pizza fria", "Pedido errado ou incompleto".')
s = M2 + 2
band(ws, s, "Resumo automático", "E")
label(ws, f"B{s+1}", "Perguntas cadastradas", merge=f"B{s+1}:C{s+1}", h="right")
calc(ws, f"D{s+1}", f"=COUNTA(C{Q1}:C{Q1 + NPER - 1})")
label(ws, f"B{s+2}", "Aviso", merge=f"B{s+2}:C{s+2}", h="right")
calc(ws, f"D{s+2}", f'=IF(D6="","Informe a escala",IF(D{s+1}=0,"Cadastre as perguntas",IF(COUNTIF(E{Q1}:E{Q1 + NPER - 1},"OK")<D{s+1},"Há pergunta a rever",'
     f'IF(COUNTA(C{M1}:C{M2})=0,"Cadastre os motivos","OK"))))', merge=f"D{s+2}:E{s+2}", sz=9, b=False)
cf_warn(ws, f"D{s+2}:E{s+2}", f"D{s+2}")
for k in (1, 2):
    ws.row_dimensions[s + k].height = 21.75
setup(ws, BLUE, f"B1:E{s+2}", landscape=False, fit_height=True)

# ------------------------------------------------------------------ Respostas
ws = wb.create_sheet("Respostas")
widths(ws, dict({"A": 2, "B": 5, "C": 12, "D": 20, "J": 11, "K": 12, "L": 40, "M": 22, "N": 2}, **{c: 9 for c in PC}))
title(ws, "Respostas da pesquisa", "Uma linha por resposta. As notas seguem a escala da aba Pesquisa. A indicação é sempre de 0 a 10.", "M")
for col, text in zip("BCD", ["#", "Data", "Cliente ou pedido"]):
    head(ws, f"{col}4", text)
for k, c in enumerate(PC):
    head(ws, f"{c}4", f"P{k + 1}")
    calc(ws, f"{c}5", f'=IF({PQ}!C{Q1 + k}="","",{PQ}!C{Q1 + k})', b=False, sz=8)
for col, text in zip("JKLM", ["Indicação (0 a 10)", "Classificação", "Comentário", "Conferência"]):
    head(ws, f"{col}4", text)
for col in "BCDJKLM":
    put(ws, f"{col}5", "", bg=GRAY)
put(ws, "C5", "As perguntas vêm da aba Pesquisa", f=font(9, i=True, c=MUTED), bg=GRAY, h="center", merge="C5:D5")
ws.row_dimensions[4].height = 33
ws.row_dimensions[5].height = 40
hint_row(ws, 6, [("B", ""), ("C", "Da resposta"), ("D", "Identificação"), ("J", "0 a 10"), ("K", "Calculada"), ("L", "Campo aberto"), ("M", "Calculada")] + [(c, "Nota") for c in PC])
for k in range(NRES):
    rr = R1 + k
    num(ws, f"B{rr}", k + 1)
    inp(ws, f"C{rr}", h="center", fmt=DATE)
    inp(ws, f"D{rr}")
    for c in PC:
        inp(ws, f"{c}{rr}", h="center")
    inp(ws, f"J{rr}", h="center")
    calc(ws, f"K{rr}", f'=IF(J{rr}="","",IF(J{rr}>=9,"{PROMOTOR}",IF(J{rr}>=7,"{NEUTRO}","{DETRATOR}")))', b=False, sz=9)
    inp(ws, f"L{rr}")
    calc(ws, f"M{rr}", f'=IF(AND(D{rr}="",COUNT({PC[0]}{rr}:J{rr})=0),"",IF(COUNT({PC[0]}{rr}:{PC[-1]}{rr})=0,"Sem notas",'
         f'IF(MAX({PC[0]}{rr}:{PC[-1]}{rr})>{ESCALA},"Nota acima da escala",IF(COUNT({PC[0]}{rr}:{PC[-1]}{rr})<{PQ}!$D${M2 + 3},"Faltam notas","Completa"))))', b=False, sz=9)
    ws.row_dimensions[rr].height = 19.5
dv_date(ws, f"C{R1}:C{R2}")
dv_numero(ws, f"{PC[0]}{R1}:{PC[-1]}{R2}", 0, 10, "Nota, na escala da aba Pesquisa.")
dv_numero(ws, f"J{R1}:J{R2}", 0, 10, "Indicação, de 0 a 10.")
cf_texto(ws, f"K{R1}:K{R2}", f"K{R1}", [(PROMOTOR, BLUE_T), (NEUTRO, AMBER_T), (DETRATOR, RED_T)])
cf_texto(ws, f"M{R1}:M{R2}", f"M{R1}", [("Completa", GREEN)], resto=YELLOW)
s = R2 + 2
band(ws, s, "Leitura por pergunta", "M")
for k, (rot, f_) in enumerate([
    ("Respostas", f'=IF({{c}}5="","",COUNT({{c}}{R1}:{{c}}{R2}))'),
    ("Média", f'=IF(OR({{c}}5="",COUNT({{c}}{R1}:{{c}}{R2})=0),"",AVERAGE({{c}}{R1}:{{c}}{R2}))'),
    ("Satisfeitos", f'=IF(OR({{c}}5="",COUNT({{c}}{R1}:{{c}}{R2})=0),"",COUNTIF({{c}}{R1}:{{c}}{R2},">="&{LIM})/COUNT({{c}}{R1}:{{c}}{R2}))'),
], 1):
    rr = s + k
    label(ws, f"B{rr}", rot, merge=f"B{rr}:D{rr}", h="right")
    for c in PC:
        calc(ws, f"{c}{rr}", f_.replace("{c}", c), fmt="0.0" if k == 2 else ("0%" if k == 3 else None))
    for col in "JKLM":
        put(ws, f"{col}{rr}", "", bg=GRAY)
    ws.row_dimensions[rr].height = 21.75
t = s + 5
band(ws, t, "Resumo automático", "M")
for k, (text, formula, fmt) in enumerate([
    ("Respostas registradas", f"=COUNTA(D{R1}:D{R2})", None),
    ("Média geral", f'=IF(COUNT({PC[0]}{R1}:{PC[-1]}{R2})=0,"",AVERAGE({PC[0]}{R1}:{PC[-1]}{R2}))', "0.00"),
    ("Satisfeitos", f'=IF(COUNT({PC[0]}{R1}:{PC[-1]}{R2})=0,"",COUNTIF({PC[0]}{R1}:{PC[-1]}{R2},">="&{LIM})/COUNT({PC[0]}{R1}:{PC[-1]}{R2}))', "0%"),
    ("Promotores, neutros e detratores", f'=COUNTIF(K{R1}:K{R2},"{PROMOTOR}")&", "&COUNTIF(K{R1}:K{R2},"{NEUTRO}")&" e "&COUNTIF(K{R1}:K{R2},"{DETRATOR}")', None),
    ("Indicação", f'=IF(COUNT(J{R1}:J{R2})=0,"",ROUND(100*(COUNTIF(K{R1}:K{R2},"{PROMOTOR}")-COUNTIF(K{R1}:K{R2},"{DETRATOR}"))/COUNT(J{R1}:J{R2}),0))', None),
    ("Aviso", f'=IF(E{t+1}=0,"Lance as respostas",IF(COUNTIF(M{R1}:M{R2},"Nota acima da escala")>0,"Há nota acima da escala",'
              f'IF(COUNTIF(M{R1}:M{R2},"Faltam notas")+COUNTIF(M{R1}:M{R2},"Sem notas")>0,"Há resposta incompleta: veja a coluna Conferência","OK")))', None),
], 1):
    label(ws, f"B{t+k}", text, merge=f"B{t+k}:D{t+k}", h="right")
    calc(ws, f"E{t+k}", formula, fmt=fmt, merge=f"E{t+k}:H{t+k}", sz=9 if text == "Aviso" else 10, b=text != "Aviso")
    ws.row_dimensions[t + k].height = 21.75
cf_warn(ws, f"E{t+6}:H{t+6}", f"E{t+6}")
ws.freeze_panes = "E7"
setup(ws, AMBER, f"B1:M{t+6}", fit_height=True)

# ------------------------------------------------------------------ Reclamações
ws = wb.create_sheet("Reclamações")
widths(ws, {"A": 2, "B": 5, "C": 12, "D": 18, "E": 12, "F": 26, "G": 40, "H": 12, "I": 12, "J": 11, "K": 30, "L": 12, "M": 24, "N": 2})
title(ws, "Reclamações", "Uma linha por reclamação, de qualquer canal. O prazo da primeira resposta e a situação são calculados pelas datas.", "M")
for col, text in zip("BCDEFGHIJKLM", ["#", "Data", "Cliente ou pedido", "Canal", "Motivo", "Descrição", "Respondida em", "Resolvida em", "Dias até a resposta",
                                       "Tratamento", "RNC nº", "Situação"]):
    head(ws, f"{col}4", text)
ws.row_dimensions[4].height = 33
hint_row(ws, 5, [("B", ""), ("C", "Do registro"), ("D", "Identificação"), ("E", "Escolha na lista"), ("F", "Da lista da aba Pesquisa"), ("G", "O que aconteceu e o que o cliente pede"),
                 ("H", "Primeira resposta"), ("I", "Solução"), ("J", "Calculada"), ("K", "O que foi feito"), ("L", "Se virou RNC"), ("M", "Calculada")])
ex(ws, "B6", "Ex.", h="center")
for col, v, h_, fmt in [("C", date(2027, 2, 20), "center", DATE), ("D", "Pedido 2.671", "left", None), ("E", "Telefone", "center", None), ("F", "Pizza fria", "left", None),
                        ("G", "Pizza fria em condomínio: 15 minutos na portaria.", "left", None), ("H", date(2027, 2, 20), "center", DATE), ("I", date(2027, 2, 22), "center", DATE),
                        ("J", 0, "center", None), ("K", "Pizza reposta. Entrega na porta combinada com a portaria.", "left", None), ("L", "", "center", None), ("M", "Resolvida", "center", None)]:
    ex(ws, f"{col}6", v, h=h_, fmt=fmt)
ws.row_dimensions[6].height = 30
for k in range(NREC):
    rr = C1 + k
    num(ws, f"B{rr}", k + 1)
    inp(ws, f"C{rr}", h="center", fmt=DATE)
    inp(ws, f"D{rr}")
    inp(ws, f"E{rr}", h="center")
    inp(ws, f"F{rr}")
    inp(ws, f"G{rr}")
    inp(ws, f"H{rr}", h="center", fmt=DATE)
    inp(ws, f"I{rr}", h="center", fmt=DATE)
    calc(ws, f"J{rr}", f'=IF(OR(C{rr}="",H{rr}=""),"",H{rr}-C{rr})', b=False)
    inp(ws, f"K{rr}")
    inp(ws, f"L{rr}", h="center", fmt="@")
    calc(ws, f"M{rr}", f'=IF(G{rr}="","",IF(C{rr}="","Falta a data",IF(F{rr}="","Falta o motivo",IF(I{rr}<>"","Resolvida",IF(H{rr}<>"","Respondida","Aberta")))))', b=False, sz=9)
    ws.row_dimensions[rr].height = 30
dv_date(ws, f"C{C1}:C{C2}")
dv_date(ws, f"H{C1}:H{C2}")
dv_date(ws, f"I{C1}:I{C2}")
dv_list(ws, f"E{C1}:E{C2}", CANAIS, "Canal por onde a reclamação chegou")
dv = DataValidation(type="list", formula1=f"={PQ}!$C${M1}:$C${M2}", allow_blank=True)
dv.promptTitle, dv.prompt, dv.showInputMessage = "Motivo", "Escolha um motivo da lista da aba Pesquisa.", True
dv.errorTitle, dv.error, dv.showErrorMessage = "Motivo inválido", "Escolha um motivo cadastrado na aba Pesquisa.", True
ws.add_data_validation(dv)
dv.add(f"F{C1}:F{C2}")
cf_texto(ws, f"M{C1}:M{C2}", f"M{C1}", [("Resolvida", GREEN), ("Respondida", BLUE_T), ("Aberta", RED)], resto=YELLOW)
ws.conditional_formatting.add(f"J{C1}:J{C2}", FormulaRule(formula=[f"AND(ISNUMBER(J{C1}),J{C1}>{PRAZO_RESPOSTA})"], fill=PatternFill("solid", bgColor=YELLOW, fgColor=YELLOW)))
note(ws, "H4", f"Data em que o cliente recebeu a primeira resposta: quem cuida e o que vai ser feito. Prazo do modelo: {PRAZO_RESPOSTA} dias úteis.")
note(ws, "L4", "Reclamação procedente é não conformidade e recebe correção. A grave ou repetida abre registro de não conformidade, com análise de causa.")
s = C2 + 2
band(ws, s, "Resumo automático", "G")
put(ws, f"I{s}", "Reclamações por motivo", f=font(10, True, c=WHITE), bg=INK, box=False, merge=f"I{s}:M{s}")
for k, (text, formula, fmt) in enumerate([
    ("Reclamações registradas", f"=COUNTA(G{C1}:G{C2})", None),
    ("Abertas, sem resposta", f'=COUNTIF(M{C1}:M{C2},"Aberta")', None),
    ("Respondidas no prazo", f'=IF(COUNT(J{C1}:J{C2})=0,"",COUNTIF(J{C1}:J{C2},"<={PRAZO_RESPOSTA}")/COUNT(J{C1}:J{C2}))', "0%"),
    ("Dias até a resposta, em média", f'=IF(COUNT(J{C1}:J{C2})=0,"",AVERAGE(J{C1}:J{C2}))', "0.0"),
    ("Resolvidas", f'=COUNTIF(M{C1}:M{C2},"Resolvida")', None),
    ("Aviso", f'=IF(E{s+1}=0,"Registre as reclamações",IF(COUNTIF(M{C1}:M{C2},"Falta*")>0,"Há reclamação com campos em branco: veja a coluna Situação",'
              f'IF(E{s+2}>0,"Há reclamação sem resposta",IF(COUNTIF(J{C1}:J{C2},">{PRAZO_RESPOSTA}")>0,"Há resposta fora do prazo","OK"))))', None),
], 1):
    label(ws, f"B{s+k}", text, merge=f"B{s+k}:D{s+k}", h="right")
    calc(ws, f"E{s+k}", formula, fmt=fmt, merge=f"E{s+k}:G{s+k}", sz=9 if text == "Aviso" else 10, b=text != "Aviso")
    ws.row_dimensions[s + k].height = 21.75
cf_warn(ws, f"E{s+6}:G{s+6}", f"E{s+6}")
for k in range(8):
    rr = s + 1 + k
    calc(ws, f"I{rr}", f'=IF({PQ}!C{M1 + k}="","",{PQ}!C{M1 + k})', h="left", b=False, sz=9, merge=f"I{rr}:L{rr}")
    calc(ws, f"M{rr}", f'=IF({PQ}!C{M1 + k}="","",COUNTIF(F{C1}:F{C2},{PQ}!C{M1 + k}))')
    ws.row_dimensions[rr].height = 21.75 if k < 6 else 18
ws.freeze_panes = "E7"
setup(ws, REDC, f"B1:M{s+9}", fit_height=True)

# ------------------------------------------------------------------ Painel
ws = wb.create_sheet("Painel")
widths(ws, {"A": 2, "B": 36, "C": 16, "D": 14, "E": 22, "F": 30, "G": 2})
title(ws, "Painel da satisfação", "Os indicadores do período, com meta e situação. Informe os pedidos do período e as metas.", "F")
label(ws, "B4", "Pedidos ou clientes atendidos no período")
inp(ws, "C4", h="center")
put(ws, "D4", "Base da taxa de resposta e das reclamações por 100.", f=font(9, i=True, c=MUTED), bg=GRAY, merge="D4:F4")
label(ws, "B5", "Período")
calc(ws, "C5", f'=IF({PQ}!D5="","",{PQ}!D5)', h="left", b=False, merge="C5:F5")
for rr in (4, 5):
    ws.row_dimensions[rr].height = 21.75
dv_numero(ws, "C4", 1, 10000000, "Quantidade de pedidos, entregas ou clientes do período.")
for col, text in zip("BCDEF", ["Indicador", "Resultado", "Meta", "Situação", "Como se lê"]):
    head(ws, f"{col}7", text)
ws.row_dimensions[7].height = 21.75
RS = "Respostas"
RC = "Reclamações"
t_res = R2 + 7   # linha do resumo das respostas: t+1 = Respostas registradas
IND = [
    ("Taxa de resposta", f'=IF(OR(C4="",{RS}!E{t_res+1}=0),"",{RS}!E{t_res+1}/C4)', "0%", 0.10, "maior", "Respostas sobre pedidos. Leia a nota junto com ela."),
    ("Nota média das perguntas", f'=IF({RS}!E{t_res+2}="","",{RS}!E{t_res+2})', "0.00", None, "maior", "Média de todas as notas, na escala da pesquisa."),
    ("Satisfeitos", f'=IF({RS}!E{t_res+3}="","",{RS}!E{t_res+3})', "0%", 0.80, "maior", "Notas iguais ou acima do limite, sobre as notas."),
    ("Indicação", f'=IF({RS}!E{t_res+5}="","",{RS}!E{t_res+5})', "0", 50, "maior", "Promotores menos detratores, de −100 a 100."),
    ("Reclamações por 100 pedidos", f'=IF(OR(C4="",{RC}!E{C2+3}=0),"",100*{RC}!E{C2+3}/C4)', "0.0", 2.0, "menor", "Reclamações sobre pedidos, vezes 100."),
    ("Respondidas no prazo", f'=IF({RC}!E{C2+5}="","",{RC}!E{C2+5})', "0%", 0.90, "maior", f"Respostas em até {PRAZO_RESPOSTA} dias, sobre as respondidas."),
    ("Dias até a resposta, em média", f'=IF({RC}!E{C2+6}="","",{RC}!E{C2+6})', "0.0", 1.0, "menor", "Da data do registro à primeira resposta."),
]
for k, (nome, formula, fmt, meta, sentido, leitura) in enumerate(IND):
    rr = 8 + k
    label(ws, f"B{rr}", nome)
    calc(ws, f"C{rr}", formula, fmt=fmt)
    inp(ws, f"D{rr}", meta, h="center", fmt=fmt)
    op = ">=" if sentido == "maior" else "<="
    calc(ws, f"E{rr}", f'=IF(C{rr}="","Sem dados",IF(D{rr}="","Sem meta",IF(C{rr}{op}D{rr},"Na meta","Fora da meta")))', b=False, sz=9)
    put(ws, f"F{rr}", leitura, f=font(9, c=MUTED), bg=GRAY)
    ws.row_dimensions[rr].height = 27
P2 = 8 + len(IND) - 1
cf_texto(ws, f"E8:E{P2}", "E8", [("Na meta", GREEN), ("Fora da meta", RED), ("Sem meta", YELLOW), ("Sem dados", GRAY)])
note(ws, "D7", "A meta da nota média depende da escala: 4,3 em 5, 8,0 em 10. Informe a sua.")
s = P2 + 2
band(ws, s, "Resumo automático", "F")
label(ws, f"B{s+1}", "Indicadores na meta", h="right")
calc(ws, f"C{s+1}", f'=COUNTIF(E8:E{P2},"Na meta")&" de "&COUNTIF(E8:E{P2},"<>Sem dados")')
label(ws, f"B{s+2}", "Motivo mais frequente", h="right")
calc(ws, f"C{s+2}", f'=IF(SUM({RC}!M{C2+3}:M{C2+10})=0,"",INDEX({RC}!I{C2+3}:I{C2+10},MATCH(MAX({RC}!M{C2+3}:M{C2+10}),{RC}!M{C2+3}:M{C2+10},0)))', h="left", b=False, merge=f"C{s+2}:F{s+2}")
label(ws, f"B{s+3}", "Aviso", h="right")
calc(ws, f"C{s+3}", f'=IF(C4="","Informe os pedidos do período",IF(COUNTIF(E8:E{P2},"Sem dados")={len(IND)},"Lance as respostas e as reclamações",'
     f'IF(COUNTIF(E8:E{P2},"Fora da meta")>0,"Há indicador fora da meta: decida sobre o motivo mais frequente","OK")))', sz=9, b=False, merge=f"C{s+3}:F{s+3}")
cf_warn(ws, f"C{s+3}:F{s+3}", f"C{s+3}")
for k in (1, 2, 3):
    ws.row_dimensions[s + k].height = 21.75
band(ws, s + 5, "Média por pergunta", "F")
for k in range(NPER):
    rr = s + 6 + k
    calc(ws, f"B{rr}", f'=IF({PQ}!C{Q1 + k}="","P{k + 1}","P{k + 1} · "&{PQ}!C{Q1 + k})', h="left", b=False, sz=9)
    calc(ws, f"C{rr}", f'=IF({RS}!{PC[k]}{R2+4}="","",{RS}!{PC[k]}{R2+4})', fmt="0.0")
    ws.row_dimensions[rr].height = 18
barras(ws, f"D{s+5}", s + 6, s + 5 + NPER, 2, 3, width=14, height=6, maximo=None)
setup(ws, TEAL, f"B1:F{s+18}", landscape=False, fit_height=True)

# ------------------------------------------------------------------ Checklist
ws = wb.create_sheet("Checklist")
widths(ws, {"A": 2, "B": 5, "C": 70, "D": 14, "E": 44, "F": 2})
title(ws, "Checklist da satisfação do cliente", "Escolha o status de cada item na lista suspensa (coluna em amarelo-claro).", "E")
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


def cabecalho(ws, data, last):
    H = data["head"]
    rr = 4
    for rot, val, fmt in [("Organização", H["org"], None), ("Data e período", f'{H["data"]:%d/%m/%Y}. {H["periodo"]}', None), ("Pesquisa", H["canal"], None),
                          ("Origem", H["origem"], None)]:
        label(ws, f"B{rr}", rot, merge=f"B{rr}:C{rr}")
        inp(ws, f"D{rr}", val, merge=f"D{rr}:{last}{rr}", bg=WHITE, fmt=fmt, h="left")
        ws.row_dimensions[rr].height = alt([(val, 100)], minimo=19.5)
        rr += 1
    return rr + 1


def motivos(ws, rr, mot, last, titulo, base):
    band(ws, rr, titulo, last, color=REDC)
    rr += 1
    sub(ws, rr, [("B", "E", "Motivo"), ("F", None, base), ("G", None, "Percentual"), ("H", None, "Acumulado")], height=24)
    m1 = rr + 1
    for m, v in mot:
        rr += 1
        put(ws, f"B{rr}", m, f=font(10, True), merge=f"B{rr}:E{rr}")
        put(ws, f"F{rr}", v, h="center")
        calc(ws, f"G{rr}", f"=F{rr}/SUM(F${m1}:F${m1 + len(mot) - 1})", fmt="0%", b=False)
        calc(ws, f"H{rr}", f"=SUM(F${m1}:F{rr})/SUM(F${m1}:F${m1 + len(mot) - 1})", fmt="0%", b=False)
        ws.row_dimensions[rr].height = 19.5
    return rr + 2


def exemplo1(ws, data):
    widths(ws, {"A": 2, "B": 11, "C": 10, "D": 11, "E": 9, "F": 10, "G": 10, "H": 10, "I": 9, "J": 11, "K": 11, "L": 11, "M": 13, "N": 2})
    title(ws, "Satisfação do cliente", "Exemplo preenchido, para consulta. Use as abas Pesquisa, Respostas, Reclamações e Painel para a sua organização.", "M")
    rr = cabecalho(ws, data, "M")
    band(ws, rr, "Resultado por mês · escala de 1 a 5", "M", color=BLUE)
    rr += 1
    sub(ws, rr, [("B", None, "Mês"), ("C", None, "Pedidos"), ("D", None, "Respostas"), ("E", None, "Taxa")] + [(c, None, cod) for c, (cod, _, _) in zip("FGH", data["perguntas"])]
        + [("I", None, "Média"), ("J", None, "Promotores"), ("K", None, "Detratores"), ("L", None, "Indicação"), ("M", None, "Reclamações por 100")], height=33)
    m1 = rr + 1
    for m in data["meses"]:
        r_ = resumo_mes(m)
        rr += 1
        put(ws, f"B{rr}", r_["rot"], f=font(10, True))
        put(ws, f"C{rr}", r_["pedidos"], h="center")
        put(ws, f"D{rr}", r_["respostas"], h="center")
        calc(ws, f"E{rr}", f"=D{rr}/C{rr}", fmt="0%", b=False)
        for c, v in zip("FGH", r_["medias"]):
            put(ws, f"{c}{rr}", v, h="center", fmt="0.0")
        calc(ws, f"I{rr}", f"=AVERAGE(F{rr}:H{rr})", fmt="0.00")
        put(ws, f"J{rr}", r_["prom"], h="center")
        put(ws, f"K{rr}", r_["det"], h="center")
        calc(ws, f"L{rr}", f"=ROUND(100*(J{rr}-K{rr})/D{rr},0)")
        put(ws, f"M{rr}", r_["reclamacoes"], h="center")
        calc(ws, f"M{rr}", f"=100*{r_['reclamacoes']}/C{rr}", fmt="0.0", b=False)
        ws.row_dimensions[rr].height = 21.75
    m2 = rr
    mt = data["metas"]
    rr += 1
    label(ws, f"B{rr}", "Meta")
    for c in "CDE":
        put(ws, f"{c}{rr}", "—", bg=GRAY, h="center")
    for c in "FGHI":
        put(ws, f"{c}{rr}", mt["media"], bg=GRAY, h="center", fmt="0.0")
    put(ws, f"J{rr}", "—", bg=GRAY, h="center")
    put(ws, f"K{rr}", "—", bg=GRAY, h="center")
    put(ws, f"L{rr}", mt["nps"], bg=GRAY, h="center")
    put(ws, f"M{rr}", mt["reclamacoes"], bg=GRAY, h="center", fmt="0.0")
    ws.row_dimensions[rr].height = 19.5
    for c in "FGHI":
        ws.conditional_formatting.add(f"{c}{m1}:{c}{m2}", FormulaRule(formula=[f"{c}{m1}<{c}${rr}"], fill=PatternFill("solid", bgColor=RED_T, fgColor=RED_T)))
    rr += 2
    rr = motivos(ws, rr, data["motivos"], "M", "Motivos das notas 1 e 2 e das reclamações", "Ocorrências")
    ws.row_breaks.append(Break(id=rr - 1))
    band(ws, rr, "Reclamações registradas · amostra", "M", color=AMBER)
    rr += 1
    sub(ws, rr, [("B", None, "Data"), ("C", None, "Pedido"), ("D", None, "Canal"), ("E", "F", "Motivo"), ("G", "I", "Descrição"), ("J", None, "Respondida"), ("K", None, "Resolvida"),
                 ("L", None, "Registro"), ("M", None, "Situação")], height=24)
    for d, ped, canal, motivo, desc, resp, res, rnc, sit in data["reclamacoes"]:
        rr += 1
        put(ws, f"B{rr}", d, h="center", fmt=DATE)
        put(ws, f"C{rr}", ped)
        put(ws, f"D{rr}", canal)
        put(ws, f"E{rr}", motivo, merge=f"E{rr}:F{rr}")
        put(ws, f"G{rr}", desc, merge=f"G{rr}:I{rr}")
        put(ws, f"J{rr}", resp, h="center", fmt=DATE)
        put(ws, f"K{rr}", res, h="center", fmt=DATE)
        put(ws, f"L{rr}", rnc or None, h="center")
        calc(ws, f"M{rr}", f'=IF(K{rr}<>"","Resolvida",IF(J{rr}<>"","Respondida","Aberta"))', b=False, sz=9)
        ws.row_dimensions[rr].height = alt([(desc, 30)], minimo=21.75)
    cf_texto(ws, f"M{rr - len(data['reclamacoes']) + 1}:M{rr}", f"M{rr - len(data['reclamacoes']) + 1}", [("Resolvida", GREEN), ("Respondida", BLUE_T), ("Aberta", RED)])
    rr += 2
    band(ws, rr, "Resumo automático", "M")
    for k, (text, formula, fmt) in enumerate([
        ("Respostas no período", f"=SUM(D{m1}:D{m2})", None),
        ("Média das três perguntas", f"=AVERAGE(I{m1}:I{m2})", "0.00"),
        ("Indicação, do primeiro ao último mês", f'=L{m1}&" → "&L{m2}', None),
        ("Reclamações por 100 pedidos, do primeiro ao último mês", f'=TEXT(M{m1},"0,0")&" → "&TEXT(M{m2},"0,0")', None),
        ("Motivo mais frequente", f"=INDEX(B{m2 + 4}:B{m2 + 3 + len(data['motivos'])},MATCH(MAX(F{m2 + 4}:F{m2 + 3 + len(data['motivos'])}),F{m2 + 4}:F{m2 + 3 + len(data['motivos'])},0))", None),
    ], 1):
        label(ws, f"B{rr+k}", text, merge=f"B{rr+k}:F{rr+k}", h="right")
        calc(ws, f"G{rr+k}", formula, fmt=fmt, merge=f"G{rr+k}:I{rr+k}")
        ws.row_dimensions[rr + k].height = 21.75
    setup(ws, MUTED, f"B1:M{rr + 5}")


def exemplo2(ws, data):
    widths(ws, {"A": 2, "B": 14, "C": 10, "D": 11, "E": 10, "F": 10, "G": 10, "H": 10, "I": 10, "J": 9, "K": 11, "L": 11, "M": 11, "N": 2})
    title(ws, "Satisfação do cliente", "Exemplo preenchido, para consulta. Use as abas Pesquisa, Respostas, Reclamações e Painel para a sua organização.", "M")
    rr = cabecalho(ws, data, "M")
    band(ws, rr, "Resultado por segmento · escala de 0 a 10", "M", color=BLUE)
    rr += 1
    sub(ws, rr, [("B", None, "Segmento"), ("C", None, "Clientes"), ("D", None, "Respostas")] + [(c, None, cod) for c, (cod, _, _) in zip("EFGHI", data["perguntas"])]
        + [("J", None, "Média"), ("K", None, "Promotores"), ("L", None, "Detratores"), ("M", None, "Indicação")], height=24)
    rr += 1
    put(ws, f"B{rr}", "", bg=GRAY)
    put(ws, f"C{rr}", "", bg=GRAY, merge=f"C{rr}:D{rr}")
    for c, (_, p, _) in zip("EFGHI", data["perguntas"]):
        put(ws, f"{c}{rr}", p, f=font(8), bg=GRAY, h="center")
    for c in "JKLM":
        put(ws, f"{c}{rr}", "", bg=GRAY)
    ws.row_dimensions[rr].height = 36
    s1 = rr + 1
    for rot, cli, resp, medias, prom, neu, det in data["segmentos"]:
        rr += 1
        put(ws, f"B{rr}", rot, f=font(10, True))
        put(ws, f"C{rr}", cli, h="center")
        put(ws, f"D{rr}", resp, h="center")
        for c, v in zip("EFGHI", medias):
            put(ws, f"{c}{rr}", v, h="center", fmt="0.0")
        calc(ws, f"J{rr}", f"=AVERAGE(E{rr}:I{rr})", fmt="0.00")
        put(ws, f"K{rr}", prom, h="center")
        put(ws, f"L{rr}", det, h="center")
        calc(ws, f"M{rr}", f"=ROUND(100*(K{rr}-L{rr})/D{rr},0)")
        ws.row_dimensions[rr].height = 21.75
    s2 = rr
    rr += 1
    label(ws, f"B{rr}", "Todos")
    calc(ws, f"C{rr}", f"=SUM(C{s1}:C{s2})")
    calc(ws, f"D{rr}", f"=SUM(D{s1}:D{s2})")
    for c in "EFGHI":
        calc(ws, f"{c}{rr}", f"=SUMPRODUCT({c}{s1}:{c}{s2},$D{s1}:$D{s2})/$D{rr}", fmt="0.0")
    calc(ws, f"J{rr}", f"=AVERAGE(E{rr}:I{rr})", fmt="0.00")
    calc(ws, f"K{rr}", f"=SUM(K{s1}:K{s2})")
    calc(ws, f"L{rr}", f"=SUM(L{s1}:L{s2})")
    calc(ws, f"M{rr}", f"=ROUND(100*(K{rr}-L{rr})/D{rr},0)")
    ws.row_dimensions[rr].height = 21.75
    tot = rr
    rr += 1
    label(ws, f"B{rr}", "Meta")
    for c in "CD":
        put(ws, f"{c}{rr}", "—", bg=GRAY, h="center")
    for c in "EFGHIJ":
        put(ws, f"{c}{rr}", data["metas"]["media"], bg=GRAY, h="center", fmt="0.0")
    for c in "KL":
        put(ws, f"{c}{rr}", "—", bg=GRAY, h="center")
    put(ws, f"M{rr}", data["metas"]["nps"], bg=GRAY, h="center")
    ws.row_dimensions[rr].height = 19.5
    for c in "EFGHIJ":
        ws.conditional_formatting.add(f"{c}{s1}:{c}{tot}", FormulaRule(formula=[f"{c}{s1}<{c}${rr}"], fill=PatternFill("solid", bgColor=RED_T, fgColor=RED_T)))
    rr += 2
    cx = data["cliente_x"]
    rr = motivos(ws, rr, data["motivos"], "M", f'Reclamações de 2026 por motivo · {cx["reclamacoes"]} das {cx["total"]} são do {cx["nome"].lower()}', "Reclamações")
    band(ws, rr, "Resumo automático", "M")
    for k, (text, formula, fmt) in enumerate([
        ("Taxa de resposta", f"=D{tot}/C{tot}", "0%"),
        ("Média geral", f"=J{tot}", "0.00"),
        ("Dimensão com a menor nota", f"=INDEX(E{s1 - 1}:I{s1 - 1},MATCH(MIN(E{tot}:I{tot}),E{tot}:I{tot},0))", None),
        ("Segmento com a menor média", f"=INDEX(B{s1}:B{s2},MATCH(MIN(J{s1}:J{s2}),J{s1}:J{s2},0))", None),
        ("Indicação geral", f"=M{tot}", None),
    ], 1):
        label(ws, f"B{rr+k}", text, merge=f"B{rr+k}:F{rr+k}", h="right")
        calc(ws, f"G{rr+k}", formula, fmt=fmt, merge=f"G{rr+k}:I{rr+k}")
        ws.row_dimensions[rr + k].height = 21.75
    setup(ws, MUTED, f"B1:M{rr + 5}")


exemplo1(wb.create_sheet("Exemplo 1 - Pizzaria"), EX1)
exemplo2(wb.create_sheet("Exemplo 2 - Indústria"), EX2)

wb.active = 1
wb.save(OUT)
print("ok", OUT)
