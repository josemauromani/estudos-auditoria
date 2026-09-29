# -*- coding: utf-8 -*-
"""Dados dos exemplos da Matriz GUT, usados pelo HTML e pela planilha."""
from datetime import date

ALTA, MEDIA = 64, 27  # cortes das faixas: nota 4 e nota 3 nos três critérios


def pontos(p):
    return p["g"] * p["u"] * p["t"]


def faixa(v):
    return "Alta" if v >= ALTA else ("Média" if v >= MEDIA else "Baixa")


def ordenar(lista):
    """Maior pontuação primeiro; desempate por gravidade, urgência, tendência e ordem da lista."""
    return sorted(lista, key=lambda p: (-pontos(p), -p["g"], -p["u"], -p["t"], int(p["k"][1:])))


def _mk(rows):
    return [dict(k=f"P{i+1}", txt=t, curto=c, origem=o, g=g, u=u, t=tt) for i, (t, c, o, g, u, tt) in enumerate(rows)]


EX1 = {
    "head": dict(tema="Problemas da operação da pizzaria", resp="Gerente da loja", area="Pizzaria (loja)",
                 data=date(2026, 9, 29), autor="Equipe da loja", versao="1.0",
                 objetivo="Escolher os problemas que serão tratados no trimestre.",
                 origem="Reclamações, indicadores e reunião mensal da equipe",
                 part="Gerente, líder da expedição, pizzaiolo e atendente",
                 fora="Problemas do salão e decisões de cardápio."),
    "itens": _mk([
        ("Forno único opera no limite no horário de pico", "Forno único no limite no horário de pico", "Indicador", 4, 3, 4),
        ("Margem do delivery caiu com o aumento da taxa do aplicativo", "Margem do delivery em queda", "Indicador", 4, 4, 4),
        ("Câmara fria com falha intermitente de temperatura", "Câmara fria com falha de temperatura", "Reunião", 5, 5, 4),
        ("Erros de sabor ou de tamanho em 3% dos pedidos", "Erros de sabor ou de tamanho em 3% dos pedidos", "Reclamação", 3, 3, 2),
        ("Desperdício de ingredientes acima de 8% do consumo", "Desperdício de ingredientes acima de 8%", "Indicador", 3, 2, 3),
        ("Licença sanitária vence em 45 dias", "Licença sanitária vence em 45 dias", "Reunião", 5, 4, 2),
        ("Saídas de entregadores subiram de 2 para 5 por trimestre", "Saídas de entregadores em alta", "Indicador", 3, 3, 4),
        ("Fila no balcão de retirada nas noites de sábado", "Fila no balcão de retirada aos sábados", "Reclamação", 2, 1, 2),
    ]),
    "decisoes": [
        ("P3", "Chamar a assistência técnica e registrar a temperatura duas vezes por turno até o reparo.", "Gerente da loja", date(2026, 10, 2)),
        ("P2", "Abrir um ciclo PDCA para recuperar a margem do delivery.", "Gerente da loja", date(2026, 10, 9)),
        ("P6", "Protocolar o pedido de renovação da licença. Tratado fora da ordem, pela gravidade máxima.", "Gerente da loja", date(2026, 10, 9)),
        ("P1", "Estudar a compra do segundo forno, com início em novembro.", "Pizzaiolo", date(2026, 11, 30)),
    ],
}

EX2 = {
    "head": dict(tema="Problemas do processo de compras", resp="Gerente de Suprimentos", area="Suprimentos",
                 data=date(2026, 9, 29), autor="Equipe de compras", versao="1.0",
                 objetivo="Definir a ordem dos projetos de melhoria do semestre.",
                 origem="Matriz SWOT da área, indicadores e auditoria interna",
                 part="Gerente, compradores, Controladoria e Qualidade",
                 fora="Gestão de estoques e pagamento a fornecedores."),
    "itens": _mk([
        ("Fornecedor único contratado para três itens críticos", "Fornecedor único para três itens críticos", "SWOT", 5, 3, 4),
        ("40% das requisições são devolvidas por especificação incompleta", "40% das requisições devolvidas", "Indicador", 3, 3, 3),
        ("Pedido de compra leva 12 dias úteis para ser emitido", "Pedido leva 12 dias úteis para ser emitido", "Indicador", 4, 4, 3),
        ("Contrato de frete vence em 60 dias, sem renegociação iniciada", "Contrato de frete vence em 60 dias", "Reunião", 4, 5, 2),
        ("Cadastro de fornecedores com dados desatualizados", "Cadastro de fornecedores desatualizado", "Auditoria", 2, 2, 3),
        ("Compras urgentes fora do processo cresceram 30% no semestre", "Compras urgentes cresceram 30%", "Indicador", 4, 4, 5),
        ("Avaliação de fornecedores não distingue bom e mau desempenho", "Avaliação de fornecedores sem distinção", "Auditoria", 3, 2, 2),
    ]),
    "decisoes": [
        ("P6", "Abrir um ciclo PDCA sobre as compras urgentes fora do processo.", "Gerente de Suprimentos", date(2026, 10, 9)),
        ("P1", "Homologar um segundo fornecedor para os três itens críticos. Avaliado à parte, pela gravidade máxima.", "Comprador sênior", date(2026, 12, 18)),
        ("P3", "Abrir um ciclo PDCA para reduzir o prazo de emissão do pedido.", "Analista de compras", date(2026, 10, 30)),
        ("P4", "Iniciar a renegociação do contrato de frete.", "Comprador de serviços", date(2026, 10, 16)),
    ],
}

EX3 = {
    "itens": _mk([
        ("Instrumentos de medição em uso com calibração vencida (3 de 25)", "", "Auditoria", 4, 5, 3),
        ("Registros de treinamento incompletos para operadores novos", "", "Auditoria", 3, 3, 4),
        ("Procedimento de compras diferente da prática atual", "", "Auditoria", 2, 2, 2),
        ("Produto não conforme sem identificação na área de expedição", "", "Auditoria", 5, 5, 3),
        ("Indicadores sem análise registrada nos últimos 6 meses", "", "Auditoria", 3, 2, 3),
        ("Reclamações de clientes respondidas fora do prazo definido", "", "Auditoria", 4, 4, 4),
    ]),
}
