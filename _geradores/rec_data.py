# -*- coding: utf-8 -*-
"""Dados do estudo de Recursos, infraestrutura e ambiente, usados pelo HTML e pela planilha.

O dimensionamento pela demanda do pico, as situações da preventiva, a disponibilidade calculada só com as paradas
corretivas e as regras de conferência são uma convenção deste material. Os exemplos continuam os dos outros estudos
da série: a pizzaria em abril de 2027, depois da troca do termômetro da câmara fria, e a indústria em julho de 2027,
depois da calibração do micrômetro.
"""
import calendar
import math
from datetime import date

D = date
# ---- pessoas
FALTA, JUSTO, FOLGA = "Falta gente", "Justo", "Com folga"
CAP_SITS = [FALTA, JUSTO, FOLGA]
# ---- infraestrutura
TIPOS = ["Edifício e instalações", "Equipamento", "Transporte", "TI e software"]
ALTA, MEDIA, BAIXA = "Alta", "Média", "Baixa"
CRITS = [ALTA, MEDIA, BAIXA]
CORR, PREV = "Corretiva", "Preventiva"
TIPOS_OC = [CORR, PREV]
SIM, NAO = "Sim", "Não"
EMDIA, VENCE, ATRAS, SEMPLANO = "Em dia", "Vence em 7 dias", "Atrasada", "Sem plano"
PREV_SITS = [EMDIA, VENCE, ATRAS, SEMPLANO]
JANELA = 7  # dias de antecedência para o aviso da preventiva
# ---- ambiente
FIS, SOC, PSI = "Físico", "Social", "Psicológico"
FATORES = [FIS, SOC, PSI]
DENTRO, FORA, SEMMED = "Dentro", "Fora", "Sem medição"
AMB_SITS = [DENTRO, FORA, SEMMED]

ETAPAS = [
    ("Listar o que o processo usa", "As funções, os equipamentos, os sistemas, os veículos e as condições do lugar."),
    ("Dimensionar as pessoas", "Pela demanda do pico, e não pelo costume. Com quem cubra as ausências."),
    ("Manter a infraestrutura", "Preventiva no prazo para o que é crítico, e um plano para quando parar."),
    ("Controlar o ambiente", "Os fatores físicos, sociais e psicológicos, com limite e medição."),
    ("Ler e reagir", "Falta de gente, parada e ambiente fora do limite viram ação, e o produto afetado é avaliado."),
]
BLOCOS = [
    ("7.1.1 e 7.1.2", "Pessoas e recursos", "Quantas pessoas, em que turnos, e o que mais o processo consome: orçamento, tempo, material."),
    ("7.1.3", "Infraestrutura", "Prédio, equipamentos, veículos, sistemas e comunicação: o que precisa funcionar."),
    ("7.1.4", "Ambiente", "Temperatura, limpeza, luz, ruído, carga de trabalho, pausas e convivência."),
]
FATOR_EX = {
    FIS: ["Temperatura e umidade", "Limpeza e higiene", "Iluminação", "Ruído e vibração"],
    SOC: ["Convivência sem conflito", "Tratamento justo", "Comunicação entre turnos", "Relação com a liderança"],
    PSI: ["Carga de trabalho no pico", "Horas extras e jornada", "Pausas e descanso", "Pressão do prazo"],
}


def add_meses(d, m):
    """Soma meses a uma data, como a função EDATE das planilhas."""
    y, mo = divmod(d.month - 1 + m, 12)
    y, mo = d.year + y, mo + 1
    return date(y, mo, min(d.day, calendar.monthrange(y, mo)[1]))


# ------------------------------------------------------------ pessoas
def necessarias(c):
    if not c["dem"] or not c["prod"]:
        return None
    return math.ceil(c["dem"] / c["prod"] - 1e-9)


def cap_sit(c):
    n = necessarias(c)
    if n is None or c["esc"] is None:
        return ""
    return FALTA if c["esc"] < n else JUSTO if c["esc"] == n else FOLGA


def cap_conf(c):
    """Conferência de uma linha de dimensionamento: a mesma regra da planilha."""
    if not c["dem"]:
        return "Falta a demanda"
    if not c["prod"]:
        return "Falta a produtividade"
    if c["esc"] is None:
        return "Falta o número escalado"
    if c["qual"] is None:
        return "Falta o número de qualificados"
    if c["qual"] > c["esc"]:
        return "Mais qualificados que escalados"
    f = c["esc"] - necessarias(c)
    if f < 0:
        return "Falta 1 pessoa" if f == -1 else f"Faltam {-f} pessoas"
    if c["qual"] == 0:
        return "Sem pessoa qualificada na escala"
    return "OK"


# ------------------------------------------------------------ infraestrutura
def proxima(i):
    return add_meses(i["ultima"], i["interv"]) if i["ultima"] and i["interv"] else None


def prev_sit(i, ref):
    if not i["interv"]:
        return SEMPLANO
    if not i["ultima"]:
        return ATRAS
    p = proxima(i)
    if p < ref:
        return ATRAS
    if (p - ref).days <= JANELA:
        return VENCE
    return EMDIA


def paradas(i, ocs, ini, fim):
    """Quebras e horas paradas no período: só as corretivas contam."""
    sel = [o for o in ocs if o["cod"] == i["cod"] and o["tipo"] == CORR and o["data"] and ini <= o["data"] <= fim]
    return len(sel), sum(o["horas"] or 0 for o in sel)


def disp(i, ocs, ini, fim):
    if not i["prog"]:
        return None
    return (i["prog"] - paradas(i, ocs, ini, fim)[1]) / i["prog"]


def mtbf(i, ocs, ini, fim):
    q, h = paradas(i, ocs, ini, fim)
    return (i["prog"] - h) / q if i["prog"] and q else None


def mttr(i, ocs, ini, fim):
    q, h = paradas(i, ocs, ini, fim)
    return h / q if q else None


def infra_conf(i, ex):
    h = ex["head"]
    if not i["tipo"]:
        return "Falta o tipo"
    if not i["crit"]:
        return "Falta a criticidade"
    if i["crit"] in (ALTA, MEDIA) and not i["interv"]:
        return "Sem plano de preventiva"
    if prev_sit(i, h["ref"]) == ATRAS:
        return "Preventiva atrasada"
    if i["crit"] == ALTA and not i["cont"]:
        return "Crítico sem contingência"
    d = disp(i, ex["ocs"], h["ini"], h["fim"])
    if d is not None and d < h["meta"] - 1e-9:
        return "Disponibilidade abaixo da meta"
    return "OK"


def oc_conf(o, infra):
    if o["cod"] not in {i["cod"] for i in infra}:
        return "Item não cadastrado"
    if not o["data"]:
        return "Falta a data"
    if not o["tipo"]:
        return "Falta o tipo"
    if o["horas"] is None:
        return "Falta o tempo parado"
    if o["tipo"] == CORR:
        if not o["causa"]:
            return "Falta a causa"
        if not o["acao"]:
            return "Falta a ação"
        if o["afetou"] not in (SIM, NAO):
            return "Falta dizer se afetou o produto"
        if o["afetou"] == SIM and not o["trat"]:
            return "Produto afetado sem tratamento"
    return "OK"


# ------------------------------------------------------------ ambiente
def amb_sit(a):
    if a["valor"] is None:
        return SEMMED
    if (a["min"] is not None and a["valor"] < a["min"]) or (a["max"] is not None and a["valor"] > a["max"]):
        return FORA
    return DENTRO


def amb_conf(a):
    if not a["porque"]:
        return "Falta por que afeta o produto"
    if not a["controle"]:
        return "Falta como é controlado"
    if a["min"] is None and a["max"] is None:
        return "Falta o limite"
    s = amb_sit(a)
    if s == SEMMED:
        return "Falta a medição"
    if s == FORA and not a["acao"]:
        return "Fora do limite: falta a ação"
    return "OK"


def limite(a):
    u = a["unid"]
    if a["min"] is not None and a["max"] is not None:
        return f'{num(a["min"])} a {num(a["max"])} {u}'
    if a["min"] is not None:
        return f'no mínimo {num(a["min"])} {u}'
    if a["max"] is not None:
        return f'no máximo {num(a["max"])} {u}'
    return "—"


def num(v):
    if v is None:
        return "—"
    if float(v).is_integer():
        return f"{int(v):,}".replace(",", ".")
    return f"{v:g}".replace(".", ",")


# ------------------------------------------------------------ montagem dos exemplos
def _caps(rows):
    return [dict(zip(("funcao", "periodo", "unid", "dem", "prod", "esc", "qual"), r)) for r in rows]


def _infra(rows):
    keys = ("cod", "nome", "tipo", "local", "crit", "interv", "ultima", "cont", "prog")
    out = [dict(zip(keys, r)) for r in rows]
    for i in out:
        assert i["tipo"] in TIPOS and i["crit"] in CRITS, i["cod"]
    return out


def _ocs(rows):
    out = [dict(zip(("data", "cod", "tipo", "horas", "oque", "causa", "acao", "afetou", "trat"), r)) for r in rows]
    for o in out:
        assert o["tipo"] in TIPOS_OC, o["cod"]
    return out


def _amb(rows):
    out = [dict(zip(("fator", "tipo", "local", "porque", "unid", "min", "max", "controle", "valor", "acao"), r)) for r in rows]
    for a in out:
        assert a["tipo"] in FATORES, a["fator"]
    return out


# ------------------------------------------------------------ exemplo 1: pizzaria, abril de 2027
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", resp="Gerente da loja, com o pizzaiolo líder", ini=D(2027, 4, 1), fim=D(2027, 4, 30), ref=D(2027, 4, 30),
                 meta=0.97, horario="Loja aberta das 18h à meia-noite: 180 horas no mês. A câmara fria fica ligada o tempo todo: 720 horas. O sistema de pedidos é contado nas horas de loja aberta.",
                 origem="Requisitos 7.1.1, 7.1.3 e 7.1.4 atendidos no diagnóstico de 2026, mas a escala de pico era feita de cabeça, e a quebra da câmara fria em abril mostrou que não havia plano para ela parar."),
    "caps": _caps([
        ("Atendimento", "Sexta, 19h às 23h", "pedidos por hora", 40, 20, 2, 2),
        ("Atendimento", "Sábado, 19h às 23h", "pedidos por hora", 36, 20, 2, 0),
        ("Pizzaiolo", "Sexta, 20h às 22h", "pizzas por hora", 60, 20, 3, 2),
        ("Forneiro", "Sexta, 20h às 22h", "pizzas por hora", 60, 40, 1, 1),
        ("Expedição", "Sexta, 20h às 22h", "pedidos por hora", 40, 30, 2, 1),
        ("Entregador", "Sexta, 20h às 22h", "entregas por hora", 29, 3, 8, 8),
        ("Entregador", "Terça, 19h às 22h", "entregas por hora", 10, 3, 4, 4),
        ("Salão", "Sexta, 20h às 22h", "clientes por hora", 30, 15, 3, 3),
    ]),
    "infra": _infra([
        ("FOR-01", "Forno de lastro a gás", "Equipamento", "Cozinha", ALTA, 1, D(2027, 4, 2), "Forno elétrico reserva, com metade da capacidade, e cardápio reduzido.", 180),
        ("CAM-01", "Câmara fria", "Equipamento", "Estoque", ALTA, 3, D(2027, 1, 10), "Freezer reserva e caixas térmicas com gelo. Acima de 5 °C, medir cada item com o TER-01.", 720),
        ("MAS-01", "Masseira", "Equipamento", "Produção", MEDIA, 6, D(2026, 11, 15), "", 180),
        ("MOT-01", "Moto de entrega 1", "Transporte", "Expedição", ALTA, 1, D(2027, 4, 5), "Entregador extra com moto própria, chamado pelo grupo.", 180),
        ("MOT-02", "Moto de entrega 2", "Transporte", "Expedição", ALTA, 1, D(2027, 4, 5), "Entregador extra com moto própria, chamado pelo grupo.", 180),
        ("MOT-03", "Moto de entrega 3", "Transporte", "Expedição", ALTA, 1, D(2027, 2, 15), "Entregador extra com moto própria, chamado pelo grupo.", 180),
        ("SIS-01", "Sistema de pedidos", "TI e software", "Atendimento", ALTA, 1, D(2027, 4, 1), "Bloco de pedidos em papel e telefone fixo.", 180),
        ("EXA-01", "Coifa e exaustão", "Edifício e instalações", "Cozinha", MEDIA, 3, D(2027, 3, 20), "", 180),
        ("SEL-01", "Seladora de embalagens", "Equipamento", "Expedição", BAIXA, None, None, "", None),
    ]),
    "ocs": _ocs([
        (D(2027, 4, 1), "SIS-01", PREV, 0, "Atualização de versão do sistema e cópia de segurança testada.", "", "", "", ""),
        (D(2027, 4, 2), "FOR-01", PREV, 0, "Limpeza dos queimadores e teste da válvula de segurança.", "", "", "", ""),
        (D(2027, 4, 5), "MOT-01", PREV, 0, "Revisão mensal: óleo, freios, pneus e luzes.", "", "", "", ""),
        (D(2027, 4, 5), "MOT-02", PREV, 0, "Revisão mensal: óleo, freios, pneus e luzes.", "", "", "", ""),
        (D(2027, 4, 12), "CAM-01", CORR, 9, "Compressor parado. Câmara a 11 °C na abertura da cozinha.", "Capacitor do compressor queimado. A revisão de 10/04 não tinha sido feita.",
         "Capacitor trocado. Alarme de temperatura instalado, contingência escrita e revisão marcada para 05/05.", SIM, "18 kg de muçarela e molho descartados (registro de produto não conforme 2027-27)."),
        (D(2027, 4, 16), "SIS-01", CORR, 1.5, "Sistema fora do ar na sexta, das 20h às 21h30.", "Atualização automática disparada no horário de pico.",
         "Atualização automática desligada. Atualizar só às segundas, de manhã.", NAO, ""),
        (D(2027, 4, 19), "MOT-02", CORR, 12, "Corrente da transmissão partiu durante uma entrega.", "Corrente gasta, que a revisão não confere.",
         "Corrente trocada e incluída no roteiro da revisão mensal.", SIM, "1 pedido entregue com 50 minutos de atraso. Desconto dado ao cliente."),
        (D(2027, 4, 26), "FOR-01", CORR, 3, "Chama apagando no lastro do fundo.", "", "", NAO, ""),
    ]),
    "amb": _amb([
        ("Temperatura da cozinha", FIS, "Cozinha", "Acima de 32 °C, a massa passa do ponto e o pizzaiolo perde o ritmo.", "°C", None, 32,
         "Termômetro de parede, lido às 21h, todo dia", 34, "Coifa limpa em 22/04. Segundo ventilador pedido para maio."),
        ("Temperatura da câmara fria", FIS, "Estoque", "Acima de 5 °C, os insumos estragam.", "°C", 0, 5,
         "Visor lido na abertura e no fechamento. Alarme desde 13/04", 3.5, ""),
        ("Limpeza da bancada e dos utensílios", FIS, "Cozinha", "Bancada suja contamina a massa e o recheio.", "% do checklist", 95, None,
         "Checklist de limpeza no fechamento, conferido pelo gerente", 88, ""),
        ("Iluminação da expedição", FIS, "Expedição", "Com pouca luz, o pedido sai com o sabor trocado.", "lux", 500, None,
         "Medição com luxímetro a cada 6 meses", None, ""),
        ("Pizzas por pizzaiolo no pico", PSI, "Cozinha", "Acima de 20 por hora, a montagem perde o padrão.", "pizzas/h", None, 20,
         "Pedidos do sistema divididos pelos pizzaiolos, toda sexta", 20, ""),
        ("Horas extras por pessoa na semana", PSI, "Loja", "Equipe cansada erra mais e falta mais.", "h", None, 6,
         "Folha de ponto, toda semana", 5, ""),
    ]),
}

# ------------------------------------------------------------ exemplo 2: indústria, julho de 2027
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", resp="Supervisor de manutenção, com o gerente industrial", ini=D(2027, 7, 1), fim=D(2027, 7, 31), ref=D(2027, 7, 31),
                 meta=0.95, horario="Três turnos, todos os dias: 744 horas no mês. A impressora trabalha em dois turnos: 496 horas.",
                 origem="Preparação da análise crítica de 19/08/2027: as paradas da extrusora 3 foram a segunda causa dos atrasos, e o turno da noite trabalha com gente a menos desde as férias de junho."),
    "caps": _caps([
        ("Operador de extrusão", "Turno A", "extrusoras em operação", 4, 1, 4, 4),
        ("Operador de extrusão", "Turno B", "extrusoras em operação", 4, 1, 4, 4),
        ("Operador de extrusão", "Turno C", "extrusoras em operação", 4, 1, 3, 3),
        ("Impressor", "Turno A", "impressoras em operação", 1, 1, 1, 1),
        ("Rebobinador", "Turno A", "bobinas por hora", 24, 8, 3, 3),
        ("Rebobinador", "Turno C", "bobinas por hora", 24, 8, 2, 2),
        ("Técnico de laboratório", "Turno A", "ensaios por hora", 5, 6, 1, 1),
        ("Expedição", "Turno A", "cargas por hora", 4, 2, 3, 3),
    ]),
    "infra": _infra([
        ("EXT-01", "Extrusora 1", "Equipamento", "Extrusão", ALTA, 3, D(2027, 5, 10), "Pedidos urgentes passam para a extrusora 2.", 744),
        ("EXT-03", "Extrusora 3", "Equipamento", "Extrusão", ALTA, 3, D(2027, 3, 15), "Pedidos redistribuídos entre as extrusoras 1 e 2, com hora extra.", 744),
        ("EXT-04", "Extrusora 4", "Equipamento", "Extrusão", ALTA, 3, D(2027, 6, 21), "Pedidos urgentes passam para a extrusora 2.", 744),
        ("IMP-01", "Impressora flexográfica", "Equipamento", "Impressão", ALTA, 1, D(2027, 7, 20), "Impressão de pedidos urgentes em terceiro homologado.", 496),
        ("REB-01", "Rebobinadeira", "Equipamento", "Rebobinamento", MEDIA, 6, D(2027, 2, 20), "", 744),
        ("CMP-01", "Compressor de ar", "Equipamento", "Utilidades", ALTA, 3, D(2027, 6, 2), "", 744),
        ("CHI-01", "Chiller de água gelada", "Equipamento", "Utilidades", ALTA, 6, D(2027, 4, 10), "Água da torre de resfriamento, com as extrusoras em velocidade reduzida.", 744),
        ("EMP-01", "Empilhadeira", "Transporte", "Expedição", MEDIA, 3, D(2027, 5, 5), "", 744),
        ("ERP-01", "Sistema de gestão (ERP)", "TI e software", "Escritório", ALTA, 3, D(2027, 7, 3), "Cópia diária fora da fábrica. Pedidos em planilha por até um dia.", None),
        ("EXS-01", "Exaustão de solventes da impressão", "Edifício e instalações", "Impressão", MEDIA, 12, D(2026, 9, 15), "", 496),
        ("SEL-01", "Seladora manual", "Equipamento", "Expedição", BAIXA, None, None, "", None),
    ]),
    "ocs": _ocs([
        (D(2027, 6, 28), "EXT-03", CORR, 10, "Resistência da zona 2 queimou.", "Resistência no fim da vida útil.", "Resistência trocada.", NAO, ""),
        (D(2027, 7, 3), "ERP-01", PREV, 0, "Teste de restauração da cópia de segurança: dados recuperados em 40 minutos.", "", "", "", ""),
        (D(2027, 7, 6), "EXT-03", CORR, 14, "Resistência da zona 3 queimou.", "Resistência no fim da vida útil. A troca estava prevista na preventiva de junho, adiada.",
         "Resistência trocada. Preventiva remarcada para 07/08, com os pedidos redistribuídos.", SIM, "Bobina em produção segregada e moída (registro de produto não conforme 2027-29)."),
        (D(2027, 7, 12), "IMP-01", CORR, 4, "Anilox entupido: falha na cor.", "Limpeza do anilox esquecida na troca do turno C.",
         "Limpeza do anilox incluída no roteiro da troca de turno.", NAO, ""),
        (D(2027, 7, 18), "EXT-03", CORR, 20, "Espessura variando ao longo da bobina.", "Rosca desgastada. O desgaste só é medido na preventiva, que está atrasada.",
         "Rosca recuperada. Medição da rosca antecipada para a preventiva de 07/08.", SIM, "6 bobinas com espessura fora segregadas (registro de produto não conforme 2027-30)."),
        (D(2027, 7, 20), "IMP-01", PREV, 6, "Troca das facas e limpeza geral.", "", "", "", ""),
        (D(2027, 7, 22), "CHI-01", CORR, 8, "Vazamento de gás refrigerante: água acima de 18 °C.", "Conexão trincada por vibração.",
         "Conexão trocada e suporte antivibração instalado.", SIM, ""),
        (D(2027, 7, 27), "EXT-03", CORR, 6, "Leitura instável da temperatura da zona 3.", "Cabo do termopar danificado pela vibração.",
         "Cabo trocado. Termopar TER-Z3 calibrado no local por laboratório externo, a 190 °C, antes de a extrusora voltar.", NAO, ""),
    ]),
    "amb": _amb([
        ("Temperatura do salão de impressão", FIS, "Impressão", "Acima de 28 °C, a tinta seca no anilox e a cor varia.", "°C", 18, 28,
         "Termo-higrômetro lido a cada turno", 31, "Ventilação forçada no turno A. Climatização no orçamento de 2028."),
        ("Umidade do salão de impressão", FIS, "Impressão", "Abaixo de 40 %, a eletricidade estática atrai pó para o filme.", "%", 40, 65,
         "Termo-higrômetro lido a cada turno", 52, ""),
        ("Ruído na extrusão", FIS, "Extrusão", "Acima de 85 dB(A), o operador não ouve o alarme da extrusora.", "dB(A)", None, 85,
         "Medição a cada 6 meses", 88, "Alarme luminoso instalado nas quatro extrusoras. Protetor auricular obrigatório."),
        ("Limpeza da área de rebobinamento", FIS, "Rebobinamento", "Pó sobre o filme vira reclamação de sujeira.", "% do checklist", 95, None,
         "Checklist de limpeza a cada turno", 97, ""),
        ("Horas extras por operador no mês", PSI, "Turno C", "Turno com gente a menos, e cansada, erra a regulagem.", "h", None, 16,
         "Folha de ponto, todo mês", 22, ""),
        ("Pausas cumpridas no turno da noite", PSI, "Turno C", "Sem pausa, a atenção cai de madrugada, quando os ajustes errados se concentram.", "% das pausas", 90, None,
         "Registro de pausas no posto", None, ""),
    ]),
}

# exemplo 3: a quebra da câmara fria (só no treinamento)
CAMARA = [
    ("10/04", "Revisão vencida", "A revisão trimestral da câmara fria vencia em 10/04. Ninguém olhou a data."),
    ("12/04, 15h", "Compressor parado", "Na abertura da cozinha, o visor marca 11 °C. Não havia alarme."),
    ("12/04, 15h20", "Contingência improvisada", "Insumos para o freezer reserva e para caixas com gelo. Cada item medido com o TER-01."),
    ("12/04, 24h", "Reparo", "Capacitor do compressor trocado às 22h. A câmara volta a 4 °C à meia-noite: 9 horas parada."),
    ("13/04", "Produto e prevenção", "18 kg descartados (registro de produto não conforme 2027-27). Contingência escrita, alarme instalado, revisão marcada."),
]

# figura do módulo 4: a sexta-feira 16/04/2027 da pizzaria, entregas por hora
SEXTA = [("18h", 6, 6), ("19h", 14, 6), ("20h", 27, 8), ("21h", 29, 8), ("22h", 18, 6), ("23h", 9, 6)]  # (hora, entregas pedidas, entregadores na escala)
POR_ENTREGADOR = 3

CHECK = [
    "As pessoas de cada processo estão dimensionadas pela demanda do pico, e não pelo costume.",
    "Cada função e turno tem ao menos uma pessoa qualificada na escala.",
    "Há um plano para as ausências: férias, faltas e afastamentos.",
    "A infraestrutura que afeta o produto está listada, com a criticidade de cada item.",
    "Cada item crítico tem manutenção preventiva com intervalo, feita no prazo.",
    "Cada item crítico tem uma contingência escrita para quando parar.",
    "As paradas são registradas com o tempo parado, a causa e a ação.",
    "A disponibilidade dos itens críticos é acompanhada contra uma meta.",
    "Quando uma parada afeta o produto, ele é avaliado e tratado como não conforme.",
    "Os sistemas de informação têm cópia de segurança, e a restauração é testada.",
    "Os fatores do ambiente que afetam o produto estão definidos, físicos, sociais e psicológicos, com limite e controle.",
    "O ambiente é medido, e o que está fora do limite tem ação.",
]


def resumo(ex):
    h, caps, infra, ocs, amb = ex["head"], ex["caps"], ex["infra"], ex["ocs"], ex["amb"]
    falta = sum(max(0, necessarias(c) - c["esc"]) for c in caps if necessarias(c) is not None and c["esc"] is not None)
    sits = [prev_sit(i, h["ref"]) for i in infra]
    corr = [o for o in ocs if o["tipo"] == CORR and h["ini"] <= o["data"] <= h["fim"]]
    return dict(caps=len(caps), cap_falta=sum(1 for c in caps if cap_sit(c) == FALTA), pessoas=falta,
                semqual=sum(1 for c in caps if cap_conf(c) == "Sem pessoa qualificada na escala"), cap_rever=sum(1 for c in caps if cap_conf(c) != "OK"),
                infra=len(infra), criticos=sum(1 for i in infra if i["crit"] == ALTA), sits={s: sits.count(s) for s in PREV_SITS},
                semcont=sum(1 for i in infra if i["crit"] == ALTA and not i["cont"]),
                abaixo=sum(1 for i in infra if disp(i, ocs, h["ini"], h["fim"]) is not None and disp(i, ocs, h["ini"], h["fim"]) < h["meta"] - 1e-9),
                infra_rever=sum(1 for i in infra if infra_conf(i, ex) != "OK"),
                ocs=len(ocs), corr=len(corr), horas=sum(o["horas"] for o in corr), afetou=sum(1 for o in corr if o["afetou"] == SIM),
                semtrat=sum(1 for o in ocs if oc_conf(o, infra) == "Produto afetado sem tratamento"), oc_rever=sum(1 for o in ocs if oc_conf(o, infra) != "OK"),
                amb=len(amb), fora=sum(1 for a in amb if amb_sit(a) == FORA), semmed=sum(1 for a in amb if amb_sit(a) == SEMMED),
                amb_rever=sum(1 for a in amb if amb_conf(a) != "OK"))


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        h = ex["head"]
        print("==", nome, resumo(ex))
        for c in ex["caps"]:
            print("  %-24s %-20s nec %-3s %-11s %s" % (c["funcao"], c["periodo"], necessarias(c), cap_sit(c), cap_conf(c)))
        for i in ex["infra"]:
            d = disp(i, ex["ocs"], h["ini"], h["fim"])
            print("  %-7s %-34s próx %-11s %-17s %-10s %s" % (i["cod"], i["nome"], proxima(i), prev_sit(i, h["ref"]), f"{d:.1%}" if d is not None else "—", infra_conf(i, ex)))
        for o in ex["ocs"]:
            print("  %s %-7s %-10s %s" % (o["data"], o["cod"], o["tipo"], oc_conf(o, ex["infra"])))
        for a in ex["amb"]:
            print("  %-36s %-14s %-12s %s" % (a["fator"], limite(a), amb_sit(a), amb_conf(a)))
