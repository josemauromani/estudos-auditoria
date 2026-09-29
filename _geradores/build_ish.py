# -*- coding: utf-8 -*-
"""Gera Ishikawa-modelo.xlsx no mesmo padrão visual das planilhas anteriores da série."""
import os
import sys
from datetime import date

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
# funções de formatação compartilhadas com o gerador do PDCA (bloco inicial do arquivo)
_src = open(os.path.join(_here, "build_pdca.py"), encoding="utf-8").read()
exec(_src[: _src.index("STATUS = [")])

from ish_data import EX1, EX2, HINTS, M6  # noqa: E402

BLUE, BLUE_T = "2B5C8A", "DCE8F3"
TEAL, AMBER, PURPLE, REDC = "1E7B73", "A96A12", "7A4A9A", "B0413E"
NEUTRAL = "D9DEE2"
YESNO = ["Sim", "Parcial", "Não"]
YESNO_CF = [("Sim", GREEN), ("Parcial", YELLOW), ("Não", RED)]
STATUS_CF = [("Concluída", GREEN), ("Em andamento", YELLOW), ("Não iniciada", RED)]
RES = ["Confirmada", "Descartada", "Não verificada"]
RES_CF = [("Confirmada", GREEN), ("Descartada", NEUTRAL), ("Não verificada", YELLOW)]
PROB_CF = [("Alta", RED), ("Média", YELLOW), ("Baixa", GREEN)]
NC, NR = 6, 5                  # categorias e causas por categoria
T1 = 14                        # primeira linha da tabela (faixa da primeira categoria)
T2 = T1 + NC * (NR + 1) - 1    # última linha da tabela
band_row = lambda i: T1 + i * (NR + 1)
cause_rows = lambda i: range(band_row(i) + 1, band_row(i) + NR + 1)
ALL = f"{T1}:{{c}}{T2}"
rng = lambda c: f"{c}{T1}:{c}{T2}"
SH = "Ishikawa"


def note(ws, ref, text):
    c = Comment(text, "Modelo Ishikawa")
    c.width, c.height = 280, 110
    ws[ref].comment = c


ISH_W = {"A": 2, "B": 6, "C": 16, "D": 18, "E": 34, "F": 14, "G": 30, "H": 16, "I": 30, "J": 12, "K": 2, "L": 8}


def ish_sheet(ws, tab, data=None):
    widths(ws, ISH_W)
    is_ex = data is not None
    title(ws, "Ishikawa — Análise de causa e efeito",
          "Exemplo preenchido, para consulta. Use a aba Ishikawa para a sua análise." if is_ex
          else "Preencha as células em amarelo-claro. As células cinza são calculadas automaticamente.", "J")
    hb = WHITE if is_ex else INPUT
    H = data["head"] if is_ex else {}
    for r, l1, k1, l2, k2, f2 in [(4, "Tema da análise", "tema", "Responsável", "resp", None),
                                  (5, "Área / unidade", "area", "Data", "data", DATE),
                                  (6, "Elaborado por", "autor", "Versão", "versao", None),
                                  (8, "Onde e quando ocorre", "onde", "Participantes", "part", None)]:
        label(ws, f"B{r}", l1, merge=f"B{r}:C{r}")
        inp(ws, f"D{r}", H.get(k1), merge=f"D{r}:F{r}", bg=hb)
        label(ws, f"G{r}", l2)
        inp(ws, f"H{r}", H.get(k2), merge=f"H{r}:J{r}", bg=hb, fmt=f2)
        ws.row_dimensions[r].height = 21.75
    for r, l1, k1 in [(7, "Efeito (problema)", "efeito"), (9, "Origem da análise", "origem")]:
        label(ws, f"B{r}", l1, merge=f"B{r}:C{r}")
        inp(ws, f"D{r}", H.get(k1), merge=f"D{r}:J{r}", bg=hb)
        ws.row_dimensions[r].height = 30
    ws.row_dimensions[8].height = 30
    dv_date(ws, "H5")

    head(ws, "B11", "#")
    put(ws, "C11", "Causa provável", f=font(10, True, c=WHITE), bg=INK, h="center", merge="C11:D11")
    for col, text in zip("EFGHIJ", ["Por quê? (subcausa)", "Probabilidade", "Como verificar", "Resultado", "Evidência", "Segue para o plano?"]):
        head(ws, f"{col}11", text)
    ws.row_dimensions[11].height = 30
    hint = lambda ref, text, merge=None: put(ws, ref, text, f=font(9, i=True, c=MUTED), bg=GRAY, h="center", merge=merge)
    hint("B12", "")
    hint("C12", "Fato que pode produzir o efeito", "C12:D12")
    hint("E12", "Por que essa causa acontece?")
    hint("F12", "Na opinião do grupo")
    hint("G12", "Contagem, comparação, observação, medição ou teste")
    hint("H12", "O que os dados mostraram")
    hint("I12", "Número ou fato que sustenta o resultado")
    hint("J12", "Sim ou Não")
    ws.row_dimensions[12].height = 30
    if is_ex:
        put(ws, "B13", "Cada causa é uma hipótese até ser verificada. As descartadas ficam registradas, com a evidência. "
            "Só as confirmadas podem seguir para o plano de ação.", f=font(9, i=True, c=MUTED), bg=GRAY, merge="B13:J13")
    else:
        ex(ws, "B13", "Ex.", h="center")
        put(ws, "C13", "Pedidos saem um a um, sem agrupamento por bairro", f=font(9, i=True, c=MUTED), bg=GRAY, merge="C13:D13")
        ex(ws, "E13", "A expedição não separa os pedidos por zona")
        ex(ws, "F13", "Alta", h="center")
        ex(ws, "G13", "Acompanhar 50 saídas no pico e mapear as rotas")
        ex(ws, "H13", "Confirmada", h="center")
        ex(ws, "I13", "Rotas cruzadas em 31 das 50 saídas")
        ex(ws, "J13", "Sim", h="center")
        note(ws, "D4", 'Nome curto da análise.\nEx.: "Atrasos nas entregas de delivery".')
        note(ws, "D7", 'O problema, com número, local e período. Sem causa e sem solução.\nEx.: "18% das entregas chegam depois de 40 minutos".')
        note(ws, "D8", 'Onde o problema se concentra, conforme os dados da observação.\nEx.: "Sextas e sábados, das 19h às 22h".')
        note(ws, "C11", "Escreva um fato que possa ser verificado.\nEvite: falta de treinamento, falha humana, falta de sistema.")
        note(ws, "F11", "Probabilidade de a causa explicar o efeito, na opinião do grupo. Serve para escolher o que verificar primeiro.")
        note(ws, "H11", "Confirmada: os dados mostram que a causa contribui para o efeito.\nDescartada: os dados mostram que não contribui.\nNão verificada: ainda é hipótese.")
        note(ws, "J11", "Marque Sim só para causas confirmadas que serão tratadas neste ciclo. Elas aparecem na aba Plano de ação.")
    ws.row_dimensions[13].height = 33
    put(ws, "L13", "Apoio", f=font(9, True, c=MUTED), bg=GRAY, h="center")

    cats = data["cats"] if is_ex else M6
    for i in range(NC):
        rb = band_row(i)
        put(ws, f"B{rb}", "ABCDEF"[i], f=font(11, True, c=WHITE), bg=BLUE, h="center")
        put(ws, f"C{rb}", cats[i], f=font(11, True), bg=WHITE if is_ex else INPUT, merge=f"C{rb}:E{rb}")
        vazio = is_ex and not any(c["cat"] == cats[i] for c in data["causas"])
        put(ws, f"F{rb}", "Categoria discutida pelo grupo, sem causas levantadas." if vazio else HINTS[M6[i]],
            f=font(9, i=True, c=MUTED), bg=BLUE_T, merge=f"F{rb}:J{rb}")
        ws.row_dimensions[rb].height = 24
        items = [c for c in data["causas"] if c["cat"] == cats[i]] if is_ex else []
        for n, r in enumerate(cause_rows(i)):
            c = items[n] if n < len(items) else None
            bg = WHITE if is_ex else INPUT
            put(ws, f"B{r}", f"{'ABCDEF'[i]}{n+1}", f=font(10, True, c=MUTED), bg=GRAY, h="center")
            inp(ws, f"C{r}", c["causa"] if c else None, merge=f"C{r}:D{r}", bg=bg)
            inp(ws, f"E{r}", c["porque"] if c else None, bg=bg)
            inp(ws, f"F{r}", c["prob"] if c else None, h="center", bg=bg)
            inp(ws, f"G{r}", c["como"] if c else None, bg=bg)
            inp(ws, f"H{r}", c["res"] if c else None, h="center", bg=bg)
            inp(ws, f"I{r}", c["evid"] if c else None, bg=bg)
            inp(ws, f"J{r}", ("Sim" if c["segue"] else "Não") if c else None, h="center", bg=bg)
            put(ws, f"L{r}", f'=IF(J{r}="Sim",COUNTIF($J${T1}:J{r},"Sim"),"")', f=font(9, c=MUTED), bg=GRAY, h="center")
            ws.row_dimensions[r].height = 36 if is_ex else 27
            if is_ex and not c:
                ws.row_dimensions[r].hidden = True  # nos exemplos, só as linhas preenchidas ficam à vista
        a, b = cause_rows(i)[0], cause_rows(i)[-1]
        dv_list(ws, f"F{a}:F{b}", ["Alta", "Média", "Baixa"], "Alta, Média ou Baixa")
        dv_list(ws, f"H{a}:H{b}", RES, "Confirmada, Descartada ou Não verificada")
        dv_list(ws, f"J{a}:J{b}", ["Sim", "Não"], "Sim ou Não")
    cf_equal(ws, rng("H"), RES_CF)
    cf_equal(ws, rng("J"), [("Sim", GREEN)])
    # a coluna F abriga também o texto de apoio das faixas; a regra só atinge as três opções da lista
    cf_equal(ws, rng("F"), PROB_CF)

    s = T2 + 2
    band(ws, s, "Resumo automático", "J")

    def row(k, text, formula, fmt=None, sz=10, b=True):
        label(ws, f"B{s+k}", text, merge=f"B{s+k}:E{s+k}", h="right")
        calc(ws, f"F{s+k}", formula, fmt=fmt, merge=f"F{s+k}:I{s+k}", sz=sz, b=b)
        ws.row_dimensions[s + k].height = 21.75

    blocks = [f"C{cause_rows(i)[0]}:C{cause_rows(i)[-1]}" for i in range(NC)]
    row(1, "Causas levantadas", "=COUNTA(" + ",".join(blocks) + ")")
    row(2, "Categorias com causas", "=" + "+".join(f"(COUNTA({b})>0)" for b in blocks), fmt='0" de 6"')
    row(3, "Causas confirmadas", f'=COUNTIF({rng("H")},"Confirmada")')
    row(4, "Causas descartadas", f'=COUNTIF({rng("H")},"Descartada")')
    row(5, "Causas não verificadas", f"=F{s+1}-F{s+3}-F{s+4}")
    row(6, "Causas que seguem para o plano", f'=COUNTIF({rng("J")},"Sim")')
    row(7, "Aviso: evidências",
        f'=IF(SUMPRODUCT((({rng("H")}="Confirmada")+({rng("H")}="Descartada"))*({rng("I")}=""))>0,"Há causa verificada sem evidência","OK")', sz=9, b=False)
    row(8, "Aviso: coerência",
        f'=IF(SUMPRODUCT(({rng("J")}="Sim")*({rng("H")}<>"Confirmada"))>0,"Há causa que segue para o plano sem estar confirmada",'
        f'IF(SUMPRODUCT(({rng("F")}="Alta")*({rng("H")}<>"Confirmada")*({rng("H")}<>"Descartada"))>0,"Há causa de alta probabilidade sem verificação","OK"))', sz=9, b=False)
    row(9, "Aviso: categorias", f'=IF(F{s+1}=0,"Liste as causas",IF(F{s+2}<6,"Há categoria sem causa: confira se ela foi discutida","OK"))', sz=9, b=False)
    row(10, "Campos do cabeçalho preenchidos", "=COUNTA(D4,H4,D5,H5,D6,H6,D7,D8,H8,D9)", fmt='0" de 10"')
    cf_ok(ws, f"F{s+7}:I{s+9}")
    end = s + 10

    if is_ex:
        ws.row_breaks.append(Break(id=s - 1))
        band(ws, end + 2, "5 porquês das causas principais", "J", color=PURPLE)
        r = end + 3
        head(ws, f"B{r}", "#", bg=GRAY, fg=INK)
        put(ws, f"C{r}", "Causa", f=font(10, True), bg=GRAY, h="center", merge=f"C{r}:D{r}")
        put(ws, f"E{r}", "Cadeia de porquês", f=font(10, True), bg=GRAY, h="center", merge=f"E{r}:G{r}")
        put(ws, f"H{r}", "Causa raiz", f=font(10, True), bg=GRAY, h="center", merge=f"H{r}:J{r}")
        ws.row_dimensions[r].height = 21.75
        by = {c["k"]: c for c in data["causas"]}
        for code, chain in data["whys"].items():
            r += 1
            put(ws, f"B{r}", code, f=font(10, True, c=MUTED), bg=GRAY, h="center")
            put(ws, f"C{r}", by[code]["causa"], merge=f"C{r}:D{r}")
            put(ws, f"E{r}", "\n".join(f"{i}º por quê? {t}." for i, t in enumerate(chain, 1)), merge=f"E{r}:G{r}")
            put(ws, f"H{r}", data["raiz"][code], f=font(10, True), bg=BLUE_T, merge=f"H{r}:J{r}")
            ws.row_dimensions[r].height = 18 * len(chain) + 12
        end = r
    setup(ws, tab, f"B1:J{end}")
    if not is_ex:
        ws.print_title_rows = "11:11"


# ================================================================== pasta de trabalho
wb = Workbook()
wb.properties.title = "Ishikawa — Modelo de análise de causa e efeito"
wb.properties.creator = "Modelo Ishikawa"
wb.properties.language = "pt-BR"

# ------------------------------------------------------------------ Instruções
ws = wb.active
ws.title = "Instruções"
widths(ws, {"A": 2, "B": 24, "C": 92, "D": 2})
title(ws, "Ishikawa — Como usar esta planilha",
      "Modelo para levantar, verificar e aprofundar as causas de um problema.", "C")
r = 4


def section(text):
    global r
    band(ws, r, text, "C", sz=11)
    r += 1


def line(k, v, kbg=GRAY, vbg=None, kf=None, kh="left", height=19.5):
    global r
    put(ws, f"B{r}", k, f=kf or font(10, True), bg=kbg, h=kh)
    put(ws, f"C{r}", v, bg=vbg)
    ws.row_dimensions[r].height = height
    r += 1


section("Legenda: onde preencher")
line("Amarelo-claro", "Células de entrada. É aqui que você digita.", vbg=INPUT)
line("Cinza", "Células calculadas ou fixas (rótulos, contagens, avisos). Não altere.", vbg=GRAY)
line("Cinza em itálico", "Linha de exemplo (marcada com “Ex.”). Mostra o formato esperado e não entra nas contagens.", vbg=GRAY)
line("Listas suspensas", "Colunas de probabilidade, resultado, código e status aceitam apenas as opções da lista.")
line("Comentários", "Células com triângulo vermelho no canto trazem uma dica de preenchimento. Passe o mouse sobre elas.", height=31.5)
r += 1
section("As seis categorias (6M)")
for i, cat in enumerate(M6):
    line(f"{'ABCDEF'[i]} — {cat}", HINTS[cat], kbg=BLUE, vbg=BLUE_T, kf=font(10, True, c=WHITE))
line("Nomes", "Os nomes das categorias podem ser trocados na aba Ishikawa. Em serviços, é comum usar procedimentos, pessoas, sistemas, informações, indicadores e ambiente.", height=31.5)
r += 1
section("Ordem recomendada de preenchimento")
for k, text in enumerate([
    "Aba Ishikawa: preencha o cabeçalho, com o efeito escrito como problema, com número, local e período.",
    "Aba Ishikawa: confira os nomes das seis categorias e ajuste ao seu processo.",
    "Aba Ishikawa: escreva as causas de cada categoria e a subcausa de cada uma (por quê?).",
    "Aba Ishikawa: marque a probabilidade e defina como verificar as causas mais prováveis.",
    "Aba Ishikawa: depois da verificação, registre o resultado e a evidência de cada causa.",
    "Aba Diagrama: leia o diagrama montado e confira se ele conta a história do problema.",
    "Aba 5 Porquês: aprofunde as causas confirmadas até a causa raiz.",
    "Aba Ishikawa: marque as causas que seguem para o plano. Aba Plano de ação: defina as ações.",
    "Aba Checklist: valide a análise com o grupo.",
], 1):
    line(f"Passo {k}", text)
r += 1
section("Abas da planilha")
for k, text in [
    ("Ishikawa", "Modelo principal. Cabeçalho, seis categorias com cinco causas cada e resumo automático."),
    ("Diagrama", "Visão do diagrama para leitura e impressão. É toda calculada."),
    ("5 Porquês", "Cadeia de porquês de até seis causas, com a causa raiz e o teste de volta."),
    ("Plano de ação", "Lista sozinha as causas que seguem para o plano e pede ação, responsável e prazo."),
    ("Checklist", "Doze verificações de qualidade da análise, com percentual de conclusão."),
    ("Exemplo 1 - Pizzaria", "Análise preenchida com as seis categorias dos 6M e doze hipóteses."),
    ("Exemplo 2 - Compras", "Análise preenchida com categorias adaptadas e uma categoria sem causas."),
]:
    line(k, text)
r += 1
section("Regras e premissas do modelo")
for k, text in [
    ("Códigos", "Cada causa tem um código fixo, formado pela letra da categoria e pelo número da linha: de A1 a F5. As abas 5 Porquês e Plano de ação usam o código para buscar o texto da causa."),
    ("Hipótese e causa", "Toda causa começa como hipótese. O resultado só deve ser marcado como Confirmada ou Descartada depois da verificação, com a evidência registrada."),
    ("Marcações do diagrama", "Na aba Diagrama, ● indica causa confirmada que segue para o plano; ○, causa confirmada que fica para depois; ✕, causa descartada. Causa sem marca ainda não foi verificada."),
    ("Ação atrasada", "Uma ação é considerada atrasada quando o prazo é anterior à data de hoje e o status não é Concluída nem Cancelada."),
    ("Capacidade", "A planilha comporta 30 causas, 6 cadeias de porquês e 12 causas no plano de ação. Se faltar espaço, o efeito provavelmente está amplo demais: divida o problema."),
    ("Exemplos", "Os dados das abas de exemplo são ilustrativos, criados para este material."),
]:
    line(k, text, height=45.75 if len(text) > 100 else 31.5)
setup(ws, INK, f"B1:C{r}", landscape=False, fit_height=True)

# ------------------------------------------------------------------ Ishikawa
ish_sheet(wb.create_sheet(SH), BLUE)

# ------------------------------------------------------------------ Diagrama
ws = wb.create_sheet("Diagrama")
widths(ws, {"A": 2, "B": 40, "C": 40, "D": 40, "E": 5, "F": 34, "G": 2})
title(ws, "Diagrama de Ishikawa", "Esta aba é calculada a partir da aba Ishikawa. Não há nada para digitar aqui.", "F")


def cell_cause(src):
    return (f'=IF({SH}!C{src}="","",IF({SH}!H{src}="Confirmada",IF({SH}!J{src}="Sim","● ","○ "),'
            f'IF({SH}!H{src}="Descartada","✕ ",""))&{SH}!C{src})')


TOPH, SPINE, BOTH = 4, 10, 16
for j, col in enumerate("BCD"):
    # metade de cima: categorias A, B e C
    put(ws, f"{col}{TOPH}", f"={SH}!C{band_row(j)}", f=font(11, True, c=WHITE), bg=BLUE, h="center")
    for n, src in enumerate(cause_rows(j)):
        put(ws, f"{col}{TOPH + 1 + n}", cell_cause(src), f=font(10), bg=WHITE)
    # metade de baixo: categorias D, E e F, com o nome no pé
    put(ws, f"{col}{BOTH}", f"={SH}!C{band_row(j + 3)}", f=font(11, True, c=WHITE), bg=BLUE, h="center")
    for n, src in enumerate(cause_rows(j + 3)):
        put(ws, f"{col}{BOTH - 1 - n}", cell_cause(src), f=font(10), bg=WHITE)
for rr in range(TOPH, BOTH + 1):
    ws.row_dimensions[rr].height = 27
for col in "BCDE":
    put(ws, f"{col}{SPINE}", "►" if col == "E" else None, f=font(9, True, c=WHITE), bg=INK, h="center", box=False)
ws.row_dimensions[SPINE].height = 12
put(ws, f"F{SPINE - 2}", f'=IF({SH}!D7="","Efeito: preencha na aba Ishikawa",{SH}!D7)', f=font(11, True, c=WHITE), bg=INK, h="center",
    merge=f"F{SPINE - 2}:F{SPINE + 2}")
put(ws, f"F{SPINE - 3}", "EFEITO", f=font(9, True, c=MUTED), h="center", box=False)
for a, b in ((TOPH + 1, SPINE - 1), (SPINE + 1, BOTH - 1)):
    area = f"B{a}:D{b}"
    ws.conditional_formatting.add(area, FormulaRule(formula=[f'LEFT(B{a},1)="●"'], font=Font(bold=True, color=INK),
                                  fill=PatternFill("solid", bgColor=BLUE_T, fgColor=BLUE_T)))
    ws.conditional_formatting.add(area, FormulaRule(formula=[f'LEFT(B{a},1)="✕"'], font=Font(strike=True, color=MUTED)))
put(ws, f"B{BOTH + 2}", "Marcações:  ● confirmada, segue para o plano   ·   ○ confirmada, fica para depois   ·   ✕ descartada pelos dados   ·   "
    "sem marca: ainda não verificada", f=font(9, i=True, c=MUTED), box=False, merge=f"B{BOTH + 2}:F{BOTH + 2}")
ws.row_dimensions[BOTH + 2].height = 21.75
band(ws, BOTH + 4, "Resumo automático", "F")
for k, (text, formula) in enumerate([
    ("Causas levantadas", f"={SH}!F{T2 + 3}"),
    ("Causas confirmadas", f"={SH}!F{T2 + 5}"),
    ("Causas descartadas", f"={SH}!F{T2 + 6}"),
    ("Causas que seguem para o plano", f"={SH}!F{T2 + 8}"),
], 1):
    label(ws, f"B{BOTH + 4 + k}", text, merge=f"B{BOTH + 4 + k}:C{BOTH + 4 + k}", h="right")
    calc(ws, f"D{BOTH + 4 + k}", formula)
    ws.row_dimensions[BOTH + 4 + k].height = 19.5
setup(ws, TEAL, f"B1:F{BOTH + 8}", fit_height=True)

# ------------------------------------------------------------------ 5 Porquês
ws = wb.create_sheet("5 Porquês")
widths(ws, {"A": 2, "B": 5, "C": 10, "D": 32, "E": 26, "F": 26, "G": 26, "H": 26, "I": 26, "J": 32, "K": 13, "L": 22, "M": 2})
title(ws, "5 porquês — da causa à causa raiz",
      "Escolha o código de uma causa confirmada e pergunte por quê a cada resposta, até chegar a algo que se possa mudar.", "L")
for col, text in zip("BCDEFGHIJKL", ["#", "Código", "Causa", "1º por quê?", "2º por quê?", "3º por quê?", "4º por quê?", "5º por quê?",
                                      "Causa raiz", "Teste de volta", "Situação"]):
    head(ws, f"{col}4", text)
ws.row_dimensions[4].height = 21.75
ex(ws, "B5", "Ex.", h="center")
ex(ws, "C5", "B1", h="center")
ex(ws, "D5", "Escala de entregadores igual em todos os dias")
ex(ws, "E5", "A escala foi montada pelo movimento médio da semana")
ex(ws, "F5", "Os pedidos não são analisados por faixa de horário")
ex(ws, "G5", "O relatório do aplicativo mostra só o total do dia")
ex(ws, "H5", "")
ex(ws, "I5", "")
ex(ws, "J5", "A escala não acompanha o pico, porque os pedidos não são analisados por horário")
ex(ws, "K5", "Sim", h="center")
ex(ws, "L5", "Concluída", h="center")
ws.row_dimensions[5].height = 45
W1, W2 = 6, 11
for k in range(6):
    rr = W1 + k
    num(ws, f"B{rr}", k + 1)
    inp(ws, f"C{rr}", h="center")
    calc(ws, f"D{rr}", f'=IF(C{rr}="","",INDEX({SH}!$C${T1}:$C${T2},(CODE(LEFT(C{rr},1))-65)*{NR + 1}+VALUE(MID(C{rr},2,1))+1)&"")', h="left", b=False)
    for col in "EFGHIJ":
        inp(ws, f"{col}{rr}")
    inp(ws, f"K{rr}", h="center")
    calc(ws, f"L{rr}", f'=IF(C{rr}="","",IF(D{rr}="","Código sem causa",IF(COUNTA(E{rr}:I{rr})<3,"Poucos porquês",IF(J{rr}="","Falta a causa raiz",'
         f'IF(K{rr}="Sim","Concluída",IF(K{rr}="Não","Refazer a cadeia","Falta o teste de volta"))))))', b=False, sz=9)
    ws.row_dimensions[rr].height = 54
dv_list(ws, f"C{W1}:C{W2}", [f"{l}{n}" for l in "ABCDEF" for n in range(1, NR + 1)], "Código da causa na aba Ishikawa, de A1 a F5")
dv_list(ws, f"K{W1}:K{W2}", ["Sim", "Não"], "A cadeia faz sentido lida de trás para a frente, com “portanto”?")
cf_equal(ws, f"L{W1}:L{W2}", [("Concluída", GREEN), ("Refazer a cadeia", RED), ("Código sem causa", RED),
                               ("Poucos porquês", YELLOW), ("Falta a causa raiz", YELLOW), ("Falta o teste de volta", YELLOW)])
note(ws, "K4", "Leia a cadeia da causa raiz para a causa, trocando “por quê?” por “portanto”. Se algum elo não fizer sentido, marque Não e refaça.")
note(ws, "J4", "A causa raiz está ao alcance da organização, foi confirmada e não aponta uma pessoa.")
band(ws, 13, "Resumo automático", "L")
summary(ws, 14, "Cadeias registradas", f"=COUNTA(C{W1}:C{W2})", "I", "J")
summary(ws, 15, "Cadeias concluídas", f'=COUNTIF(L{W1}:L{W2},"Concluída")', "I", "J")
summary(ws, 16, "Causas confirmadas sem cadeia de porquês",
        f'=SUMPRODUCT(({SH}!{rng("H")}="Confirmada")*(COUNTIF($C${W1}:$C${W2},{SH}!{rng("B")})=0))', "I", "J")
summary(ws, 17, "Aviso", f'=IF(J14=0,"Escolha as causas a aprofundar",IF(J15<J14,"Há cadeia incompleta: veja a coluna Situação","OK"))', "I", "J")
ws["J17"].font = font(9)
cf_ok(ws, "J17")
ws.freeze_panes = "E5"
setup(ws, PURPLE, "B1:L17", fit_height=True)

# ------------------------------------------------------------------ Plano de ação
ws = wb.create_sheet("Plano de ação")
widths(ws, {"A": 2, "B": 5, "C": 9, "D": 18, "E": 40, "F": 40, "G": 18, "H": 13, "I": 15, "J": 14, "K": 2})
title(ws, "Plano de ação", "As causas marcadas com “Sim” na aba Ishikawa aparecem aqui. Defina a ação de cada uma.", "J")
for col, text in zip("BCDEFGHIJ", ["#", "Código", "Categoria", "Causa confirmada", "Ação", "Responsável", "Prazo", "Status", "Situação"]):
    head(ws, f"{col}4", text)
ws.row_dimensions[4].height = 21.75
ex(ws, "B5", "Ex.", h="center")
ex(ws, "C5", "A1", h="center")
ex(ws, "D5", "Método", h="center")
ex(ws, "E5", "Pedidos saem um a um, sem agrupamento por bairro")
ex(ws, "F5", "Agrupar os pedidos por bairro antes da saída")
ex(ws, "G5", "Líder da expedição")
ex(ws, "H5", date(2026, 10, 30), h="center", fmt=DATE)
ex(ws, "I5", "Em andamento", h="center")
ex(ws, "J5", "No prazo", h="center")
ws.row_dimensions[5].height = 31.5
P1, P2 = 6, 17
pos = lambda rr: f"MATCH($B{rr},{SH}!$L${T1}:$L${T2},0)"
for k in range(12):
    rr = P1 + k
    num(ws, f"B{rr}", k + 1)
    calc(ws, f"C{rr}", f'=IFERROR(INDEX({SH}!$B${T1}:$B${T2},{pos(rr)})&"","")')
    calc(ws, f"D{rr}", f'=IFERROR(INDEX({SH}!$C${T1}:$C${T2},INT(({pos(rr)}-1)/{NR + 1})*{NR + 1}+1)&"","")', b=False)
    calc(ws, f"E{rr}", f'=IFERROR(INDEX({SH}!$C${T1}:$C${T2},{pos(rr)})&"","")', h="left", b=False)
    inp(ws, f"F{rr}")
    inp(ws, f"G{rr}")
    inp(ws, f"H{rr}", h="center", fmt=DATE)
    inp(ws, f"I{rr}", h="center")
    calc(ws, f"J{rr}", f'=IF(F{rr}="","",IF(OR(I{rr}="Concluída",I{rr}="Cancelada"),I{rr},'
         f'IF(H{rr}="","Sem prazo",IF(H{rr}<TODAY(),"Atrasada","No prazo"))))', b=False)
    ws.row_dimensions[rr].height = 30
dv_list(ws, f"I{P1}:I{P2}", ["Não iniciada", "Em andamento", "Concluída", "Cancelada"], "Não iniciada, Em andamento, Concluída ou Cancelada")
dv_date(ws, f"H{P1}:H{P2}")
cf_equal(ws, f"I{P1}:I{P2}", STATUS_CF)
cf_equal(ws, f"J{P1}:J{P2}", [("Concluída", GREEN), ("No prazo", GREEN), ("Sem prazo", YELLOW), ("Atrasada", RED)])
band(ws, 19, "Resumo automático", "J")
summary(ws, 20, "Causas que seguem para o plano", f'=COUNTIF({SH}!{rng("J")},"Sim")', "F", "G", val_merge="G20:H20")
summary(ws, 21, "Causas com ação definida", f'=SUMPRODUCT((E{P1}:E{P2}<>"")*(F{P1}:F{P2}<>""))', "F", "G", val_merge="G21:H21")
summary(ws, 22, "Ações concluídas", f'=COUNTIF(I{P1}:I{P2},"Concluída")', "F", "G", val_merge="G22:H22")
summary(ws, 23, "Ações atrasadas", f'=COUNTIF(J{P1}:J{P2},"Atrasada")', "F", "G", val_merge="G23:H23")
summary(ws, 24, "Ações sem responsável ou sem prazo", f'=SUMPRODUCT((F{P1}:F{P2}<>"")*((G{P1}:G{P2}="")+(H{P1}:H{P2}="")>0))', "F", "G", val_merge="G24:H24")
summary(ws, 25, "Aviso",
        '=IF(G20=0,"Marque na aba Ishikawa as causas que seguem para o plano",IF(G20>12,"Mais de 12 causas marcadas: priorize",'
        'IF(G21<G20,"Há causa sem ação definida","OK")))', "F", "G", val_merge="G25:H25")
ws["G25"].font = font(9)
ws.row_dimensions[25].height = 30
cf_ok(ws, "G25:H25")
ws.freeze_panes = "C5"
setup(ws, AMBER, "B1:J25", fit_height=True)

# ------------------------------------------------------------------ Checklist
ws = wb.create_sheet("Checklist")
widths(ws, {"A": 2, "B": 5, "C": 70, "D": 14, "E": 44, "F": 2})
title(ws, "Checklist de validação do Diagrama de Ishikawa", "Escolha o status de cada item na lista suspensa (coluna em amarelo-claro).", "E")
for col, text in zip("BCDE", ["#", "Item de verificação", "Status", "Observações"]):
    head(ws, f"{col}4", text)
ws.row_dimensions[4].height = 21.75
for k, text in enumerate([
    "O efeito está escrito como problema, com número, local e período.",
    "O efeito não traz causa nem solução embutida.",
    "Participaram pessoas que conhecem o processo, de funções diferentes.",
    "As categorias foram escolhidas de acordo com o tipo de processo.",
    "Todas as categorias foram discutidas, mesmo as que ficaram sem causa.",
    "Cada causa é um fato que pode ser verificado, e não uma opinião ou a falta de uma solução.",
    "As causas foram aprofundadas com a pergunta “por quê?”.",
    "Nenhuma causa aponta uma pessoa como culpada.",
    "As causas mais prováveis foram escolhidas pelo grupo, com critério combinado.",
    "As causas escolhidas foram verificadas com dados ou no local.",
    "As causas descartadas ficaram registradas, com o motivo.",
    "As causas confirmadas seguiram para o plano de ação.",
]):
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
setup(ws, REDC, "B1:E24", landscape=False, fit_height=True)

# ------------------------------------------------------------------ Exemplos
ish_sheet(wb.create_sheet("Exemplo 1 - Pizzaria"), MUTED, EX1)
ish_sheet(wb.create_sheet("Exemplo 2 - Compras"), MUTED, EX2)

wb.active = 1
wb.save(OUT)
print("ok", OUT, "| tabela", T1, "a", T2, "| resumo em", T2 + 2)
