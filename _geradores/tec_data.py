# -*- coding: utf-8 -*-
"""Dados do estudo de Técnica de auditoria, usados pelo HTML e pela planilha.

A tabela de tamanho de amostra, os fatores de risco, a força da evidência, a escala de avaliação do auditor e as regras de
conferência são uma convenção deste material: a ISO 19011 descreve a amostragem por julgamento e a estatística, mas não fixa
números. Os exemplos continuam os dos outros estudos da série: a auditoria do salão e do recebimento da pizzaria em
18/03/2027, três dias depois da troca do termômetro da câmara fria, e a auditoria da produção da indústria em 06/10/2027.
"""
import math
from datetime import date

D = date
# ---- amostragem
ALTO, MEDIO, BAIXO = "Alto", "Médio", "Baixo"
RISCOS = [ALTO, MEDIO, BAIXO]
FATOR = {ALTO: 1.5, MEDIO: 1.0, BAIXO: 0.6}
MINIMO = 3
BASE = [(5, None), (20, 5), (50, 8), (100, 10), (500, 15), (None, 20)]  # população até: amostra-base (None: todos / acima)
INCOMP, CONF, ISOL, REPET = "Amostra incompleta", "Conforme na amostra", "Desvio isolado: ampliar a amostra", "Desvio repetido: não conformidade"
AM_SITS = [CONF, ISOL, REPET, INCOMP]
# ---- evidências
CONFORME, NC, OM = "Conforme", "Não conformidade", "Oportunidade de melhoria"
CONSTS = [CONFORME, NC, OM]
FORTE, MEDIA, FRACA = "Forte", "Média", "Fraca"
FORCAS = [FORTE, MEDIA, FRACA]
SEMCORR = "Não conformidade sem corroboração"
# ---- auditor
NIVEIS = ["Apto a liderar", "Apto a auditar em equipe", "Em formação", "Observação insuficiente"]
LIDERAR, EQUIPE, FORMACAO, POUCO = NIVEIS
MIN_OBS = 8
CRITERIOS = [  # etapa, critério, crítico
    ("Preparação", "Leu os documentos e o relatório da auditoria anterior antes de ir a campo.", False),
    ("Preparação", "Preparou a lista de verificação e o tamanho das amostras com antecedência.", False),
    ("Abertura", "Confirmou o objetivo, o escopo, os critérios e o plano na reunião de abertura.", False),
    ("Entrevista", "Fez perguntas abertas e pediu para ver: “mostre-me”.", False),
    ("Entrevista", "Ouviu sem interromper e sem sugerir a resposta.", False),
    ("Amostra", "Escolheu a amostra, em vez de aceitar a oferecida pelo auditado.", True),
    ("Amostra", "Anotou o tamanho de cada amostra e o que encontrou nela.", False),
    ("Evidência", "Corroborou o que ouviu com observação ou registro.", True),
    ("Evidência", "Seguiu ao menos uma trilha até o fim, de um registro ao seguinte.", False),
    ("Constatação", "Escreveu cada não conformidade com requisito, evidência e desvio.", True),
    ("Constatação", "Não apontou culpados nem ditou a solução.", False),
    ("Encerramento", "Comunicou as constatações durante a auditoria, sem surpresa no encerramento.", False),
]
ESCALA = [(0, "Não fez"), (1, "Fez em parte"), (2, "Fez bem"), (3, "Referência para os outros")]

ETAPAS = [
    ("Preparar a amostra", "O que verificar, de que população, com quantos registros e a partir de onde."),
    ("Abrir", "Objetivo, escopo, critérios e plano confirmados com quem será auditado."),
    ("Coletar", "Perguntar, ver acontecer e ler os registros, no local de trabalho."),
    ("Comparar", "Cada evidência contra o critério: o requisito, o procedimento, o contrato."),
    ("Concluir e comunicar", "A constatação escrita, corroborada e mostrada ao auditado na hora."),
]
CICLO = [
    ("Pergunta", "O que o critério pede, transformado em pergunta aberta."),
    ("Fonte", "Quem responde, o que se observa, que registro se lê."),
    ("Amostra", "Quantos casos, escolhidos pelo auditor."),
    ("Critério", "A régua: o requisito ou o documento que diz como deveria ser."),
    ("Constatação", "Conforme, não conforme ou oportunidade, com a evidência."),
]
FUNIL = [
    ("Aberta", "Como vocês sabem que o termômetro mede certo?", "Abre o assunto sem sugerir a resposta."),
    ("Mostre-me", "Pode me mostrar a última verificação?", "Troca a palavra pela evidência."),
    ("Seguimento", "E o que foi feito com as leituras de antes?", "Segue a trilha que a resposta abriu."),
    ("Confirmação", "Então as leituras de 08 a 14/03 não foram revistas?", "Fecha o ponto, com uma pergunta fechada."),
]
TIPOS_PERG = [
    ("Aberta", "Como, o que, quem, quando, onde.", "“Como é feita a conferência do pedido?”", "Começar um assunto."),
    ("Mostre-me", "Pede o objeto, o registro, a tela.", "“Pode me mostrar o último registro?”", "Passar da palavra à evidência."),
    ("Seguimento", "Puxa o fio da resposta anterior.", "“E depois que a bobina foi segregada?”", "Seguir uma trilha."),
    ("Hipotética", "Uma situação que pode acontecer.", "“O que você faz se o termômetro marcar 7 °C?”", "Testar o conhecimento do procedimento."),
    ("Confirmação", "Fechada, para resumir o que se entendeu.", "“Então a escala de sábado não foi revista?”", "Fechar um ponto antes da constatação."),
    ("Indutora", "Sugere a resposta esperada.", "“Vocês verificam o termômetro, certo?”", "Evitar: a resposta vem pronta."),
]
TRIANGULO = [("Entrevista", "O que as pessoas dizem que fazem."), ("Observação", "O que o auditor vê acontecer."), ("Registro", "O que ficou escrito.")]


# ------------------------------------------------------------ amostragem
def base(n_pop):
    for ate, b in BASE:
        if ate is None or n_pop <= ate:
            return b
    return None


def tamanho(a):
    """Tamanho da amostra: todos até 5; acima disso, a base da tabela vezes o fator de risco, com mínimo de 3."""
    N, r = a["pop"], a["risco"]
    if not N or r not in FATOR:
        return None
    b = base(N)
    if b is None:
        return N
    return min(N, max(MINIMO, math.ceil(b * FATOR[r] - 1e-9)))


def passo(a):
    n = tamanho(a)
    return a["pop"] // n if n else None


def am_sit(a):
    n = tamanho(a)
    if n is None or a["verif"] is None or a["desv"] is None:
        return ""
    if a["verif"] < n:
        return INCOMP
    if a["desv"] == 0:
        return CONF
    return ISOL if a["desv"] == 1 else REPET


def am_conf(a):
    if not a["oque"]:
        return "Falta o que se verifica"
    if not a["pop"]:
        return "Falta a população"
    if a["risco"] not in FATOR:
        return "Falta o risco"
    p = passo(a)
    if not a["inicio"] or not 1 <= a["inicio"] <= p:
        return f"Início deve ir de 1 a {p}"
    if a["verif"] is None:
        return "Falta quantos foram verificados"
    if a["verif"] > a["pop"]:
        return "Verificados acima da população"
    if a["desv"] is None:
        return "Falta quantos desvios"
    if a["desv"] > a["verif"]:
        return "Mais desvios que verificados"
    return "OK"


# ------------------------------------------------------------ evidências
def fontes(e):
    return sum(1 for k in ("ent", "obs", "reg") if e[k])


def forca(e):
    f = fontes(e)
    if f == 0:
        return ""
    if f >= 2:
        return FORTE
    return MEDIA if (e["obs"] or e["reg"]) else FRACA


def ev_conf(e):
    if not e["req"]:
        return "Falta o requisito"
    if not e["perg"]:
        return "Falta a pergunta"
    if fontes(e) == 0:
        return "Falta a evidência"
    if not e["const"]:
        return "Falta a constatação"
    if e["const"] == NC and forca(e) != FORTE:
        return SEMCORR
    return "OK"


# ------------------------------------------------------------ auditor
def aud_conta(notas):
    obs = [n for n in notas if n is not None]
    return len(obs), sum(obs)


def aud_pct(notas):
    k, s = aud_conta(notas)
    return s / (3 * k) if k else None


def aud_nivel(notas):
    k, _ = aud_conta(notas)
    if k == 0:
        return ""
    if k < MIN_OBS:
        return POUCO
    if any(n is not None and n <= 1 for n, c in zip(notas, CRITERIOS) if c[2]):
        return FORMACAO
    p = aud_pct(notas)
    return LIDERAR if p >= 0.8 - 1e-9 else EQUIPE if p >= 0.6 - 1e-9 else FORMACAO


def aud_conf(nome, notas):
    k, _ = aud_conta(notas)
    if not nome:
        return "Falta o nome" if k else ""
    if k == 0:
        return "Faltam as notas"
    if k < MIN_OBS:
        return "Observar mais critérios"
    return "OK"


def _ams(rows):
    return [dict(zip(("oque", "req", "periodo", "pop", "risco", "inicio", "verif", "desv", "nota"), r)) for r in rows]


def _evs(rows):
    out = [dict(zip(("req", "perg", "ent", "obs", "reg", "const"), r)) for r in rows]
    for e in out:
        assert e["const"] in CONSTS + [""], e
    return out


def _auds(rows):
    out = [dict(nome=n, papel=p, notas=list(ns)) for n, p, ns in rows]
    for a in out:
        assert len(a["notas"]) == len(CRITERIOS), a["nome"]
    return out


_ = None
# ------------------------------------------------------------ exemplo 1: pizzaria, 18/03/2027
EX1 = {
    "head": dict(num="2027-02", processo="Atender no salão e receber insumos", org="Pizzaria (loja com salão e delivery)", data=D(2027, 3, 18),
                 lider="Atendente do turno do almoço", equipe="Pizzaiolo do turno do almoço", observador="Consultor que acompanhou a primeira auditoria do salão",
                 criterios="ISO 9001:2015, requisitos 7 e 8. Instrução do salão IT-SAL-01 rev. 2. Rotina de recebimento de insumos."),
    "ams": _ams([
        ("Comandas do salão: mesa e horário anotados", "8.5.1", "Fevereiro de 2027", 620, MEDIO, 7, 20, 3, "Três comandas sem mesa ou sem horário, todas de sábado."),
        ("Leituras de temperatura da câmara fria", "7.1.4", "Fevereiro de 2027", 56, MEDIO, 2, 10, 1, "Leitura do domingo, 14/02, sem anotação."),
        ("Notas de recebimento com a temperatura anotada", "8.4", "Fevereiro de 2027", 48, ALTO, 3, 12, 0, ""),
        ("Fichas de treinamento da equipe nova do salão", "7.2", "Admissões de 2027", 6, BAIXO, 1, 3, 0, ""),
        ("Checklists de limpeza do salão", "7.1.4", "Fevereiro de 2027", 28, MEDIO, 2, 6, 0, "Dois checklists não estavam na pasta no dia."),
    ]),
    "evs": _evs([
        ("8.5.1", "Como a comanda do salão registra a mesa e o horário?", "Garçom do turno da noite", "Duas comandas abertas na hora; uma sem horário",
         "20 comandas de fevereiro: 3 sem mesa ou sem horário", NC),
        ("7.1.5", "Como vocês sabem que o termômetro da câmara mede certo?", "Pizzaiolo líder: “verificamos todo mês”", "",
         "Planilha FR-07: termômetro da câmara verificado em 15/03, reprovado e trocado; leituras anteriores não revistas", NC),
        ("8.4", "Como o recebimento confere a temperatura dos refrigerados?", "Atendente que recebe", "Recebimento do laticínio às 15h: temperatura medida e anotada",
         "12 notas de fevereiro com a temperatura anotada", CONFORME),
        ("7.2", "Quem treinou a equipe nova do salão, e como?", "Gerente da loja", "", "3 fichas de treinamento assinadas, com a instrução IT-SAL-01", CONFORME),
        ("8.2.1", "O cliente do salão é avisado do tempo de espera?", "Garçom: “nem sempre avisamos”", "", "", NC),
        ("9.1.2", "Como as reclamações do salão são registradas?", "Gerente da loja", "", "Registro de reclamações só com o delivery; o salão não aparece", OM),
        ("7.5", "A instrução do salão em uso é a vigente?", "", "Instrução no balcão na revisão 1", "Lista mestra: IT-SAL-01 na revisão 2, de 10/02/2027", NC),
        ("8.5.4", "Como os insumos são guardados depois do recebimento?", "Pizzaiolo do turno", "Câmara organizada, com etiquetas de validade", "", CONFORME),
        ("8.5.1", "Como a pizza do salão é conferida antes de servir?", "Pizzaiolo do turno", "Conferência do sabor pela comanda, no passa-pratos", "", ""),
    ]),
    "auds": _auds([
        ("Atendente do turno do almoço", "Auditor líder", [2, 2, 3, 2, 1, 3, 2, 1, 2, 2, 3, _]),
        ("Pizzaiolo do turno do almoço", "Auditor", [1, 1, _, 2, 2, 2, 1, 2, 3, _, 2, 2]),
    ]),
}

# ------------------------------------------------------------ exemplo 2: indústria, 06/10/2027
EX2 = {
    "head": dict(num="2027-11", processo="Produção (extrusão e rebobinamento)", org="Indústria de embalagens plásticas", data=D(2027, 10, 6),
                 lider="Coordenador da Qualidade", equipe="Engenheiro de processos e Analista de RH (auditor em formação)",
                 observador="Gerente de RH, que mantém a avaliação dos auditores internos",
                 criterios="ISO 9001:2015, requisitos 7.1, 7.2, 8.5 e 8.7. Plano de controle da extrusão rev. 6. Procedimento de mudanças PG-05."),
    "ams": _ams([
        ("Registros de espessura por bobina, com cinco pontos", "8.5.1", "Julho e agosto de 2027", 1150, ALTO, 12, 30, 0, ""),
        ("Registros de mudança de processo, com autorização", "8.5.6", "2027 até setembro", 9, ALTO, 1, 8, 2, "Duas mudanças de velocidade do turno C sem autorização."),
        ("Ordens de manutenção corretiva, com o produto afetado", "7.1.3", "Julho e agosto de 2027", 14, MEDIO, 2, 5, 1, "Quebra do chiller, 22/07: produto afetado sem destino."),
        ("Instrumentos do posto com etiqueta em dia", "7.1.5", "Na data da auditoria", 25, ALTO, 1, 12, 0, ""),
        ("Registros de treinamento do turno C", "7.2", "Admissões e remanejamentos de 2027", 12, MEDIO, 2, 5, 0, ""),
    ]),
    "evs": _evs([
        ("8.5.6", "Como uma mudança de processo é autorizada?", "Líder do turno C", "", "8 registros de mudança de 2027: 2 sem autorização", NC),
        ("8.5.1", "Como a espessura é medida na extrusora 3?", "Operador do turno A", "Medição em cinco pontos com o micrômetro de 0,1 µm",
         "30 bobinas de julho e agosto, todas com os cinco pontos", CONFORME),
        ("7.1.3", "O que acontece com o produto quando uma máquina quebra?", "Supervisor de manutenção", "",
         "5 ordens corretivas: 1 sem o destino do produto afetado", OM),
        ("7.1.6", "Quem mais sabe regular a extrusora 3?", "Operador sênior e operador do turno C", "Operador do turno C regulando com acompanhamento",
         "Mapa do conhecimento, C-01, ação até 30/11", CONFORME),
        ("7.1.5", "Os instrumentos do posto estão identificados e em dia?", "", "12 instrumentos com etiqueta em dia", "Lista de instrumentos de 30/09", CONFORME),
        ("7.2", "O operador novo do turno C foi treinado na regulagem?", "Operador novo: “aprendi com o colega”", "", "", NC),
        ("9.1.3", "Como o refugo da extrusão é analisado?", "Gerente industrial", "", "Painel de indicadores de setembro, com o Pareto do refugo", CONFORME),
        ("8.7", "O que se faz com a bobina fora de espessura?", "Líder do turno", "Bobina com etiqueta vermelha na área de segregação",
         "Registro de produto não conforme de 03/10", CONFORME),
    ]),
    "auds": _auds([
        ("Coordenador da Qualidade", "Auditor líder", [3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3]),
        ("Engenheiro de processos", "Auditor", [2, 2, _, 2, 2, 3, 2, 2, 3, 2, 1, 2]),
        ("Analista de RH", "Auditor em formação", [2, 1, _, 2, 2, 1, 1, 1, _, _, 2, _]),
    ]),
}

# exemplo 3: o fio de uma pergunta, na auditoria da pizzaria (só no treinamento)
PERGUNTA = [
    ("Aberta", "“Como vocês sabem que o termômetro da câmara mede certo?”", "“Verificamos todo mês.”"),
    ("Mostre-me", "“Pode me mostrar a última verificação?”", "Planilha FR-07: em 15/03, o termômetro marcou 2\u00a0°C a menos. Foi trocado."),
    ("Seguimento", "“E o que foi feito com as leituras de antes?”", "“Nada. O termômetro novo está certo.”"),
    ("Mostre-me", "“Posso ver as leituras de 08 a 14/03?”", "De 2,9 a 4,1\u00a0°C. Com o erro, até 6,1\u00a0°C, acima do limite de 5\u00a0°C."),
    ("Constatação", "Não conformidade com o 7.1.5", "Termômetro reprovado em 15/03 sem avaliação das leituras anteriores, que podem ter passado de 5\u00a0°C."),
]

CHECK = [
    "Cada item da lista de verificação vira uma pergunta aberta, com o requisito ao lado.",
    "O tamanho de cada amostra é decidido antes, pela população e pelo risco.",
    "O auditor escolhe a amostra, e o ponto de partida não vem do auditado.",
    "O tamanho da amostra e o resultado ficam anotados: quantos se viu e quantos desvios.",
    "Um desvio isolado leva a ampliar a amostra antes de concluir.",
    "Cada constatação tem ao menos uma evidência objetiva: observação ou registro.",
    "Toda não conformidade é corroborada por duas fontes.",
    "O auditor segue ao menos uma trilha até o fim em cada processo.",
    "As perguntas indutoras são evitadas, e o auditado fala mais que o auditor.",
    "As constatações são mostradas ao auditado durante a auditoria.",
    "Os auditores são avaliados em campo, por auditoria testemunhada, com critérios escritos.",
    "Quem está em formação audita em equipe até alcançar o nível de liderar.",
]


def resumo(ex):
    ams, evs, auds = ex["ams"], ex["evs"], ex["auds"]
    sits = [am_sit(a) for a in ams]
    forcas = [forca(e) for e in evs]
    consts = [e["const"] for e in evs]
    nivs = [aud_nivel(a["notas"]) for a in auds]
    return dict(ams=len(ams), verif=sum(a["verif"] or 0 for a in ams), desv=sum(a["desv"] or 0 for a in ams), sits={s: sits.count(s) for s in AM_SITS},
                am_rever=sum(1 for a in ams if am_conf(a) != "OK"),
                evs=len(evs), consts={c: consts.count(c) for c in CONSTS}, forcas={f: forcas.count(f) for f in FORCAS},
                semcorr=sum(1 for e in evs if ev_conf(e) == SEMCORR), ev_rever=sum(1 for e in evs if ev_conf(e) != "OK"),
                auds=len(auds), niveis={n: nivs.count(n) for n in NIVEIS})


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        print("==", nome, resumo(ex))
        for a in ex["ams"]:
            print("  %-52s N %-5s n %-3s passo %-3s %-36s %s" % (a["oque"][:52], a["pop"], tamanho(a), passo(a), am_sit(a), am_conf(a)))
        for e in ex["evs"]:
            print("  %-6s %-24s %-8s %s" % (e["req"], e["const"][:24], forca(e), ev_conf(e)))
        for a in ex["auds"]:
            print("  %-30s %s %s %s" % (a["nome"], aud_conta(a["notas"]), round(aud_pct(a["notas"]) or 0, 3), aud_nivel(a["notas"])))
