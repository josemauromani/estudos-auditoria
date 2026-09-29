# -*- coding: utf-8 -*-
"""Dados dos exemplos da Matriz RACI, usados pelo HTML e pela planilha."""
from datetime import date

NOMES = {"R": "Responsável", "A": "Aprovador", "C": "Consultado", "I": "Informado"}


def _mk(papeis, linhas):
    """linhas: (atividade, 'letras na ordem dos papéis'), com '-' para célula vazia e 'X' para A/R."""
    out = []
    for atividade, letras in linhas:
        cel = letras.split()
        assert len(cel) == len(papeis), (atividade, cel)
        cel = ["A/R" if c == "X" else ("" if c == "-" else c) for c in cel]
        n_a = sum(1 for c in cel if c in ("A", "A/R"))
        n_r = sum(1 for c in cel if c in ("R", "A/R"))
        assert n_a == 1 and n_r >= 1, (atividade, n_a, n_r)
        out.append((atividade, cel))
    return out


def carga(ex):
    """Contagem de R, A, C e I por papel. A/R conta como A e como R."""
    res = []
    for j, p in enumerate(ex["papeis"]):
        col = [cel[j] for _, cel in ex["linhas"]]
        res.append(dict(papel=p, R=sum(c in ("R", "A/R") for c in col), A=sum(c in ("A", "A/R") for c in col),
                        C=col.count("C"), I=col.count("I")))
    return res


P1 = ["Gerente da loja", "Atendente", "Pizzaiolo", "Líder da expedição", "Entregador"]
EX1 = {
    "head": dict(processo="Atender pedido de delivery", dono="Gerente da loja", area="Pizzaria (loja)",
                 data=date(2026, 9, 29), autor="Equipe da loja", versao="1.0",
                 escopo="Do pedido confirmado pelo cliente até o pagamento recebido, mais a rotina de escala e de acompanhamento.",
                 origem="Macroetapas do SIPOC do processo", part="Gerente, atendente, pizzaiolo, líder da expedição e um entregador",
                 fora="Compra de ingredientes e atendimento no salão."),
    "papeis": P1,
    "linhas": _mk(P1, [
        ("Registrar o pedido", "- X I I -"),
        ("Montar e assar a pizza", "- C X I -"),
        ("Embalar e conferir o pedido", "- - C X -"),
        ("Agrupar os pedidos por bairro e despachar", "I - - X I"),
        ("Entregar ao cliente", "- I - A R"),
        ("Confirmar o pagamento", "I A - - R"),
        ("Tratar a reclamação do cliente", "A R C C -"),
        ("Definir a escala de entregadores", "X - - C I"),
        ("Acompanhar o indicador de entregas no prazo", "A - I R I"),
    ]),
}

P2 = ["Requisitante", "Comprador", "Gerente de Suprimentos", "Controladoria", "Jurídico", "Recebimento"]
EX2 = {
    "head": dict(processo="Adquirir materiais e serviços", dono="Gerente de Suprimentos", area="Suprimentos",
                 data=date(2026, 9, 29), autor="Equipe de compras", versao="1.0",
                 escopo="Da requisição de compra até a liberação da nota fiscal para pagamento, mais a avaliação do fornecedor.",
                 origem="Macroetapas do SIPOC do processo", part="Gerente, compradores, dois requisitantes, Controladoria e Recebimento",
                 fora="Homologação de fornecedores, pagamento e gestão de estoque."),
    "papeis": P2,
    "linhas": _mk(P2, [
        ("Emitir a requisição de compra", "X I - C - -"),
        ("Analisar a requisição", "C R A - - -"),
        ("Cotar com fornecedores", "C X - - - -"),
        ("Selecionar a proposta", "C R A I - -"),
        ("Aprovar a compra, conforme a alçada", "I I X C - -"),
        ("Emitir o pedido de compra ou o contrato", "I R A - C I"),
        ("Receber e conferir o item", "C I - - - X"),
        ("Liberar a nota fiscal para pagamento", "- R A I - C"),
        ("Avaliar o desempenho do fornecedor", "C R A - - C"),
    ]),
}

P3 = ["Alta direção", "Gestor do programa", "Auditor líder", "Auditor", "Gestor da área auditada"]
EX3 = {
    "papeis": P3,
    "linhas": _mk(P3, [
        ("Aprovar o programa anual de auditoria", "A R - - C"),
        ("Selecionar a equipe auditora", "- X C I I"),
        ("Preparar o plano de auditoria", "- I X C C"),
        ("Conduzir a auditoria", "- I A R C"),
        ("Relatar as constatações", "I I X C I"),
        ("Analisar as causas e definir a ação corretiva", "- C I - X"),
        ("Implementar a ação corretiva", "I I - - X"),
        ("Verificar a eficácia da ação", "I A - R C"),
        ("Levar os resultados à análise crítica", "A R - - I"),
    ]),
}
