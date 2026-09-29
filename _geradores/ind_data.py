# -*- coding: utf-8 -*-
"""Dados do estudo de Indicadores, usados pelo HTML e pela planilha.

As faixas de situação, a regra dos três períodos e o critério de tendência são uma convenção deste material.
Os exemplos continuam os dos outros estudos da série (pizzaria e compras).
"""
from datetime import date

D = date
MAIOR, MENOR = "Maior é melhor", "Menor é melhor"
NA_META, ATENCAO, FORA = "Na meta", "Atenção", "Fora da meta"
SITS = [NA_META, ATENCAO, FORA]
MESES = ["Out/25", "Nov/25", "Dez/25", "Jan/26", "Fev/26", "Mar/26", "Abr/26", "Mai/26", "Jun/26", "Jul/26", "Ago/26", "Set/26"]
SEGUIDOS = 3  # períodos seguidos fora da meta que pedem análise de causa
ESTAVEL = 0.05  # variação entre as médias de três períodos abaixo da qual a tendência é considerada estável


def atende(v, ind):
    return v >= ind["meta"] if ind["sentido"] == MAIOR else v <= ind["meta"]


def situacao(v, ind):
    if atende(v, ind):
        return NA_META
    dentro = v >= ind["limite"] if ind["sentido"] == MAIOR else v <= ind["limite"]
    return ATENCAO if dentro else FORA


def seguidos(ind):
    """Períodos seguidos fora da meta, contados a partir do último."""
    n = 0
    for v in reversed(ind["valores"]):
        if atende(v, ind):
            break
        n += 1
    return n


def tendencia(ind):
    v = ind["valores"]
    if len(v) < 6:
        return "Sem dados"
    a, b = sum(v[-6:-3]) / 3, sum(v[-3:]) / 3
    if abs(b - a) <= ESTAVEL * abs(a):
        return "Estável"
    melhor = b > a if ind["sentido"] == MAIOR else b < a
    return "Melhorando" if melhor else "Piorando"


def acao(ind):
    s = situacao(ind["valores"][-1], ind)
    if seguidos(ind) >= SEGUIDOS:
        return "Abrir análise de causa"
    return {NA_META: "Manter", ATENCAO: "Acompanhar", FORA: "Analisar na reunião"}[s]


def _inds(rows):
    keys = ("id", "nome", "objetivo", "processo", "formula", "unidade", "sentido", "meta", "limite", "fonte", "freq", "resp", "valores", "decisao")
    out = [dict(zip(keys, r)) for r in rows]
    for i in out:
        assert len(i["valores"]) == 12, i["id"]
        assert (i["limite"] < i["meta"]) == (i["sentido"] == MAIOR), i["id"]
    return out


EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", periodo="Outubro de 2025 a setembro de 2026", data=D(2026, 10, 6),
                 por="Gerente da loja", reuniao="Toda segunda-feira, com fechamento mensal"),
    "inds": _inds([
        ("P1", "Entregas em até 40 minutos", "Entregar o pedido no prazo prometido", "Atender pedido de delivery",
         "Pedidos entregues em até 40 minutos ÷ pedidos entregues × 100", "%", MAIOR, 95, 90,
         "Horários de saída e de chegada, no sistema de pedidos", "Mensal", "Líder da expedição",
         [81, 83, 80, 82, 82, 83, 82, 84, 88, 94, 96, 95],
         "A escala padrão e o agrupamento por zona, definidos no ciclo PDCA, continuam."),
        ("P2", "Reclamações por 100 pedidos", "Reduzir as reclamações dos clientes", "Atender pedido de delivery",
         "Reclamações registradas ÷ pedidos entregues × 100", "por 100 pedidos", MENOR, 2.0, 3.0,
         "Registro de reclamações do site, do aplicativo e do telefone", "Mensal", "Atendente líder",
         [3.4, 3.1, 3.8, 3.2, 3.0, 3.1, 2.9, 2.6, 2.2, 1.8, 1.6, 1.9],
         "A queda acompanha a melhora das entregas no prazo."),
        ("P3", "Pedidos refeitos por erro", "Entregar o pedido certo na primeira vez", "Produzir e embalar",
         "Pedidos refeitos ÷ pedidos produzidos × 100", "%", MENOR, 1.5, 2.5,
         "Etiquetas de pedido refeito, contadas no fechamento", "Mensal", "Pizzaiolo líder",
         [2.1, 1.9, 2.4, 1.8, 1.7, 1.6, 1.4, 1.5, 1.3, 1.6, 1.8, 2.0],
         "A alta começou em julho, junto com a troca do sistema de pedidos."),
        ("P4", "Desperdício de insumos", "Reduzir o custo sem mexer na receita", "Armazenar e produzir",
         "Custo dos insumos descartados ÷ custo dos insumos comprados × 100", "%", MENOR, 4.0, 5.0,
         "Planilha de descarte e notas de compra", "Mensal", "Gerente da loja",
         [4.8, 4.6, 5.2, 4.5, 4.3, 4.4, 4.1, 4.2, 3.9, 4.0, 3.8, 3.9],
         "A meta será revista na análise anual."),
    ]),
}

EX2 = {
    "head": dict(org="Indústria de embalagens plásticas · Suprimentos", periodo="Outubro de 2025 a setembro de 2026", data=D(2026, 10, 8),
                 por="Gerente de Suprimentos", reuniao="Primeira quinta-feira de cada mês"),
    "inds": _inds([
        ("C1", "Prazo de atendimento das requisições", "Fornecer os materiais no prazo", "Adquirir materiais e serviços",
         "Soma dos dias úteis entre a requisição e o pedido ÷ número de requisições", "dias úteis", MENOR, 5.0, 6.0,
         "Datas da requisição e do pedido, no sistema", "Mensal", "Comprador sênior",
         [4.6, 4.8, 5.3, 4.7, 4.5, 4.8, 4.9, 5.2, 5.6, 5.9, 6.2, 5.8],
         "A alta acompanha as requisições devolvidas por falta de especificação."),
        ("C2", "Requisições com falha de especificação", "Comprar o item certo na primeira vez", "Requisição",
         "Requisições com especificação ausente ou insuficiente ÷ requisições recebidas × 100", "%", MENOR, 5, 10,
         "Conferência do comprador, no recebimento da requisição", "Mensal", "Gerente de Suprimentos",
         [28, 30, 32, 29, 31, 30, 29, 31, 33, 30, 31, 29],
         "O tratamento está no RNC 2026-31, aberto depois da auditoria 2026-07."),
        ("C3", "Fornecedores críticos com avaliação em dia", "Conhecer o desempenho de quem fornece", "Avaliação de fornecedores",
         "Fornecedores críticos avaliados no semestre ÷ fornecedores críticos × 100", "%", MAIOR, 100, 90,
         "Registros de avaliação de desempenho", "Mensal", "Comprador sênior",
         [100, 100, 100, 92, 92, 83, 83, 75, 67, 67, 58, 58],
         "O tratamento está na constatação nº 2 da auditoria 2026-07: avaliar os 5 fornecedores pendentes."),
        ("C4", "Itens devolvidos ao fornecedor", "Comprar o item certo na primeira vez", "Recebimento",
         "Número de itens devolvidos por divergência, no mês", "itens", MENOR, 0, 1,
         "Registros de devolução do Recebimento", "Mensal", "Líder do Recebimento",
         [1, 0, 1, 1, 0, 1, 1, 1, 0, 2, 1, 1],
         "A análise será feita em conjunto com a do indicador C2."),
    ]),
    "analise": [
        (D(2026, 10, 8), "C1", "Cinco meses seguidos acima da meta, com pico de 6,2 dias em agosto.",
         "Requisições incompletas voltam ao requisitante e entram de novo na fila.", "Tratar junto com o RNC 2026-31.", "Gerente de Suprimentos", D(2026, 10, 23)),
        (D(2026, 10, 8), "C3", "Queda contínua desde janeiro. 5 dos 12 fornecedores críticos sem avaliação.",
         "A avaliação do segundo semestre de 2025 não foi repetida em 2026.", "Avaliar os 5 fornecedores e marcar as datas no calendário da área.", "Comprador sênior", D(2026, 10, 30)),
        (D(2026, 10, 8), "C4", "Pelo menos uma devolução em 9 dos 12 meses.",
         "Item comprado diferente do necessário, por falta de especificação.", "Acompanhar depois das ações do RNC 2026-31.", "Líder do Recebimento", D(2026, 12, 3)),
    ],
}

# exemplo 3: quadro de objetivos da qualidade (só no treinamento)
QUADRO = [
    ("Entregar no prazo combinado", "Pedidos entregues no prazo", "No mínimo 96%", "97%", NA_META, "Manter o planejamento semanal de produção."),
    ("Reduzir as reclamações", "Reclamações por milhão de peças", "No máximo 50", "62", ATENCAO, "Acompanhar. A alta veio de um só cliente."),
    ("Reduzir o refugo", "Refugo, em percentual do peso", "No máximo 2,0%", "2,9%", FORA, "Projeto de melhoria aberto, com ciclo PDCA."),
    ("Manter a equipe competente", "Treinamentos realizados no prazo", "No mínimo 90%", "93%", NA_META, "Manter o plano anual de treinamento."),
    ("Conhecer os fornecedores", "Fornecedores críticos avaliados", "100%", "58%", FORA, "Ação corretiva da auditoria 2026-07."),
]

# figura: três leituras de um gráfico (valores esquemáticos, com meta de no máximo 5)
LEITURAS = [
    ("Ponto isolado", "Um período fora da meta, e os outros dentro.", "Anote o motivo e acompanhe.", [4.4, 4.6, 4.3, 5.6, 4.5, 4.4, 4.6, 4.3]),
    ("Tendência", "Vários períodos seguidos na mesma direção.", "Analise a causa antes de sair da meta.", [4.0, 4.1, 4.3, 4.4, 4.6, 4.8, 5.0, 5.3]),
    ("Mudança de patamar", "O resultado muda de nível e fica.", "Procure o que mudou naquela data.", [4.2, 4.4, 4.1, 4.3, 5.6, 5.8, 5.5, 5.7]),
]

CHECK = [
    "Cada indicador está ligado a um objetivo ou a um processo.",
    "A fórmula está escrita, com o que se divide, por quanto e em que unidade.",
    "A fonte dos dados e o responsável pela coleta estão definidos.",
    "A frequência de medição acompanha a velocidade do processo.",
    "A meta tem valor, sentido e prazo.",
    "A meta foi definida a partir do histórico ou de um requisito.",
    "O limite de atenção está definido.",
    "O conjunto de indicadores cabe em uma página.",
    "Os resultados são apresentados em gráfico, com a meta.",
    "Os resultados são analisados em reunião, com data marcada.",
    "Cada indicador fora da meta tem decisão registrada, com responsável e prazo.",
    "Os indicadores e as metas são revistos pelo menos uma vez por ano.",
]

if __name__ == "__main__":
    for nome, ex in (("EX1", EX1), ("EX2", EX2)):
        for i in ex["inds"]:
            v = i["valores"]
            print(nome, i["id"], "último", v[-1], situacao(v[-1], i), "| média %.2f" % (sum(v) / 12), "| seguidos", seguidos(i), "|", tendencia(i), "|", acao(i))
