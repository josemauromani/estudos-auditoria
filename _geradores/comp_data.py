# -*- coding: utf-8 -*-
"""Dados do estudo de Matriz de competências e treinamento, usados pelo HTML e pela planilha.

A escala de quatro níveis, a regra de cobertura e os prazos de avaliação da eficácia são uma convenção deste material.
Os exemplos continuam os dos outros estudos da série (pizzaria e compras da indústria de embalagens).
"""
from datetime import date, timedelta

D = date
# escala de níveis: nível, nome, o que a pessoa faz, evidência típica
NIVEIS = [
    (0, "Não conhece", "Nunca fez, ou não sabe o que é.", "Nenhuma."),
    (1, "Executa com acompanhamento", "Conhece o padrão e faz com alguém por perto.", "Treinamento realizado, com avaliação de aprendizado."),
    (2, "Executa sozinho", "Faz no padrão, sem ajuda, com o resultado esperado.", "Avaliação no posto de trabalho, pelo líder."),
    (3, "Executa e treina", "Faz, resolve os problemas e ensina os outros.", "Treinamentos que deu, e resultados do processo."),
]
COBERTURA = 2  # pessoas com nível 2 ou mais que uma competência precisa ter, para não depender de uma só
PRAZO_EFICACIA = 60  # dias depois do treinamento para avaliar a eficácia no posto
EFICAZ, PARCIAL, NAOEF = "Eficaz", "Parcial", "Não eficaz"
EFICACIAS = [EFICAZ, PARCIAL, NAOEF]
SIM, NAO = "Sim", "Não"
# situações de uma ação do plano
A_PLAN, A_ATRAS, A_APREND, A_ACOMP, A_AVAL, A_EFICAZ, A_PARCIAL, A_REFAZER = ("Planejada", "Atrasada", "Falta a avaliação de aprendizado", "Em acompanhamento",
                                                                              "Avaliar a eficácia", "Eficaz", "Parcial: reforçar", "Não eficaz: refazer")

# as três fontes de competência do requisito 7.2, em resumo
FONTES = [
    ("Educação", "O que a pessoa estudou: escolaridade e formação.", "Diploma, certificado, histórico."),
    ("Treinamento", "O que a pessoa aprendeu para a função: curso, instrução no posto, integração.", "Lista de presença, avaliação de aprendizado, certificado."),
    ("Experiência", "O que a pessoa já fez: tempo e resultados na função.", "Histórico profissional, avaliação no posto."),
]

# etapas da vida de uma ação de treinamento
ETAPAS = [
    ("Necessidade", "A matriz mostra a lacuna: nível abaixo do requerido."),
    ("Treinamento", "Curso, instrução no posto ou acompanhamento, com registro."),
    ("Aprendizado", "A pessoa entendeu? Prova, exercício ou demonstração, no mesmo dia."),
    ("Acompanhamento", "A pessoa aplica, com o líder por perto, por 30 a 90 dias."),
    ("Eficácia", "A pessoa faz sozinha, no padrão? O líder avalia no posto e registra."),
    ("Matriz atualizada", "O nível sobe na matriz. Se não subiu, a ação é refeita."),
]


def situacao_acao(a, ref):
    """Situação de uma ação do plano de treinamento, na data de referência."""
    if not a["feito"]:
        return A_ATRAS if a["prazo"] < ref else A_PLAN
    if not a["aprend"]:
        return A_APREND
    if a["aprend"] == NAO:
        return A_REFAZER
    if not a["eficacia"]:
        return A_AVAL if a["feito"] + timedelta(days=PRAZO_EFICACIA) <= ref else A_ACOMP
    return {EFICAZ: A_EFICAZ, PARCIAL: A_PARCIAL, NAOEF: A_REFAZER}[a["eficacia"]]


def _pessoas(rows):
    keys = ("nome", "funcao", "desde", "niveis")
    out = [dict(zip(keys, r), n=i + 1) for i, r in enumerate(rows)]
    for p in out:
        p["niveis"] = [int(x) for x in p["niveis"]]
    return out


def _plano(rows):
    keys = ("pessoa", "comp", "acao", "quem", "prazo", "feito", "aprend", "eficacia", "obs")
    return [dict(zip(keys, r), n=i + 1) for i, r in enumerate(rows)]


def requerido(ex, p):
    return ex["funcoes"][p["funcao"]]


def lacunas(ex, p):
    """Competências em que o nível está abaixo do requerido: (índice, atual, requerido)."""
    return [(k, a, r) for k, (a, r) in enumerate(zip(p["niveis"], requerido(ex, p))) if r > a]


def cobertura(ex, k):
    """Pessoas com nível 2 ou mais na competência k."""
    return sum(1 for p in ex["pessoas"] if p["niveis"][k] >= COBERTURA)


def precisam(ex, k):
    return sum(1 for p in ex["pessoas"] if requerido(ex, p)[k] > 0)


# ------------------------------------------------------------ exemplo 1: pizzaria
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", data=D(2027, 2, 12), por="Gerente da loja, com os três líderes",
                 origem="Processo “Treinar a equipe” com 31% dos elementos definidos no mapa de 14/10/2026, e risco R6: só o pizzaiolo líder regula o forno.",
                 revisao="A cada seis meses, e a cada admissão ou mudança de função."),
    "comps": [("C1", "Registrar o pedido pelo roteiro", "IT-ATE-01"), ("C2", "Produzir no padrão das receitas", "Receitas padrão"),
              ("C3", "Regular o forno", "Regulagem registrada"), ("C4", "Controlar a temperatura e as boas práticas", "IT-PRO-01"),
              ("C5", "Embalar e conferir o pedido", "IT-EXP-01, item 5"), ("C6", "Agrupar por zona e entregar", "IT-EXP-01"),
              ("C7", "Dirigir com segurança", "Treinamento de direção segura"), ("C8", "Atender no salão", "Padrão de atendimento, em elaboração")],
    "funcoes": {"Gerente da loja": [2, 1, 1, 2, 1, 2, 0, 3], "Atendente": [2, 0, 0, 1, 2, 1, 0, 2], "Pizzaiolo": [0, 3, 2, 3, 2, 0, 0, 0],
                "Líder da expedição": [1, 0, 0, 1, 3, 3, 2, 0], "Entregador": [0, 0, 0, 1, 1, 2, 2, 0]},
    "pessoas": _pessoas([
        ("Marina", "Gerente da loja", D(2022, 3, 1), "31122203"),
        ("Carla", "Atendente", D(2023, 8, 14), "30012202"),
        ("Diego", "Atendente", D(2026, 5, 4), "20011101"),
        ("Rafael", "Pizzaiolo", D(2021, 6, 7), "03332000"),
        ("Bruno", "Pizzaiolo", D(2025, 11, 10), "02222000"),
        ("Sérgio", "Líder da expedição", D(2022, 9, 19), "10013320"),
        ("Paulo", "Entregador", D(2024, 2, 5), "00011220"),
        ("Igor", "Entregador", D(2026, 9, 8), "00001120"),
    ]),
    "plano": _plano([
        ("Bruno", "C3", "Instrução no posto: regular o forno com o pizzaiolo líder, uma semana por turno.", "Rafael", D(2027, 1, 22), D(2027, 1, 20), SIM, EFICAZ,
         "Regulou o forno sozinho em 8 turnos de fevereiro. Risco R6 tratado."),
        ("Bruno", "C2", "Acompanhamento das receitas com maior desperdício, com conferência do pizzaiolo líder.", "Rafael", D(2027, 3, 12), D(2027, 2, 5), SIM, None, ""),
        ("Bruno", "C4", "Treinamento em boas práticas e controle de temperatura, com prova.", "Marina", D(2027, 2, 26), D(2027, 2, 10), SIM, None, ""),
        ("Diego", "C5", "Conferência do pedido com o líder da expedição, nas noites de sexta.", "Sérgio", D(2027, 2, 26), None, None, None, ""),
        ("Diego", "C8", "Atendimento no salão, depois do padrão de atendimento.", "Marina", D(2027, 3, 26), None, None, None, "Depende do padrão, previsto para 26/02."),
        ("Igor", "C6", "Treinamento na IT-EXP-01, com o líder da expedição.", "Sérgio", D(2026, 10, 30), D(2026, 10, 28), SIM, PARCIAL,
         "Agrupa por zona, mas ainda confunde as zonas 3 e 4. Reforço marcado."),
        ("Igor", "C4", "Integração: boas práticas de manipulação.", "Marina", D(2027, 1, 29), None, None, None, ""),
    ]),
}

# ------------------------------------------------------------ exemplo 2: compras da indústria
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas · Suprimentos", data=D(2027, 3, 12), por="Gerente de Suprimentos, com o Coordenador da Qualidade e o RH",
                 origem="Revisão 6 do PR-SUP-01, admissão de um comprador em janeiro e decisão da análise crítica de 18/02/2027: formar mais quatro auditores internos.",
                 revisao="A cada seis meses, com a avaliação de desempenho."),
    "comps": [("S1", "Aplicar o PR-SUP-01 rev. 6", "PR-SUP-01"), ("S2", "Especificar itens e usar o cadastro", "Cadastro de itens"),
              ("S3", "Cotar e negociar", "PO-02"), ("S4", "Homologar e avaliar fornecedores", "PR-SUP-02"),
              ("S5", "Operar o sistema de compras", "Manual do sistema"), ("S6", "Receber e conferir materiais", "IT-REC-01"),
              ("S7", "Requisitos da ISO 9001 para aquisição", "ISO 9001, 8.4"), ("S8", "Auditar processos internamente", "ISO 19011")],
    "funcoes": {"Gerente de Suprimentos": [3, 2, 3, 3, 2, 1, 2, 1], "Comprador": [3, 2, 2, 2, 3, 1, 1, 0], "Líder do Recebimento": [1, 2, 0, 0, 2, 3, 1, 0]},
    "pessoas": _pessoas([
        ("Helena", "Gerente de Suprimentos", D(2019, 4, 1), "32332120"),
        ("Antônio", "Comprador", D(2017, 2, 13), "33333121"),
        ("Luana", "Comprador", D(2022, 7, 4), "22213110"),
        ("Felipe", "Comprador", D(2024, 3, 18), "32223100"),
        ("Camila", "Comprador", D(2027, 1, 11), "11102000"),
        ("Jorge", "Líder do Recebimento", D(2020, 10, 26), "12002310"),
    ]),
    "plano": _plano([
        ("Camila", "S1", "Integração: leitura do PR-SUP-01 rev. 6 e prova de 10 questões.", "Antônio", D(2027, 1, 22), D(2027, 1, 15), SIM, EFICAZ,
         "Prova: 9 de 10. Requisições devolvidas por erro de procedimento: nenhuma em fevereiro."),
        ("Camila", "S5", "Treinamento no sistema de compras, com 20 requisições acompanhadas.", "Antônio", D(2027, 2, 12), D(2027, 2, 5), SIM, None, ""),
        ("Camila", "S2", "Especificação técnica: acompanhamento com o supervisor de manutenção.", "Supervisor de manutenção", D(2027, 3, 31), None, None, None, ""),
        ("Camila", "S3", "Cotação e negociação: acompanhar 10 cotações do comprador sênior.", "Antônio", D(2027, 4, 30), None, None, None, ""),
        ("Camila", "S4", "Homologação de fornecedores: participar de duas homologações.", "Antônio", D(2027, 5, 28), None, None, None, ""),
        ("Luana", "S1", "Reciclagem no PR-SUP-01 rev. 6, com foco no cadastro do item antes da compra.", "Helena", D(2026, 11, 13), D(2026, 11, 10), SIM, NAOEF,
         "Duas requisições aceitas sem cadastro em janeiro. Refazer com acompanhamento."),
        ("Luana", "S4", "Avaliação de fornecedores: fazer as 12 avaliações de junho com o comprador sênior.", "Antônio", D(2027, 6, 30), None, None, None, ""),
        ("Felipe", "S7", "Curso interno: requisitos da ISO 9001 para aquisição, 4 horas.", "Coordenador da Qualidade", D(2027, 2, 26), D(2027, 2, 24), SIM, None, ""),
        ("Helena", "S8", "Formação de auditor interno: curso de 16 horas e duas auditorias acompanhadas.", "Coordenador da Qualidade", D(2027, 5, 28), None, None, None,
         "Decisão da análise crítica de 18/02/2027."),
    ]),
}

# exemplo 3: trilha de formação de auditores internos (só no treinamento)
TRILHA = [
    ("1", "Curso de 16 horas", "ISO 9001 e diretrizes da ISO 19011, com exercícios de redação de constatação.", "Prova com nota mínima de 70%", "Nível 1"),
    ("2", "Auditoria como observador", "Acompanha uma auditoria completa, da abertura ao relatório, sem auditar.", "Relatório de observação entregue", "Nível 1"),
    ("3", "Auditoria em dupla", "Audita um processo com um auditor experiente como líder.", "Avaliação do líder: lista de verificação e constatações", "Nível 2, se aprovado"),
    ("4", "Auditoria como líder", "Conduz uma auditoria de processo de baixa complexidade, com acompanhamento.", "Relatório aprovado pela Qualidade", "Nível 2 confirmado"),
    ("5", "Reciclagem anual", "Quatro horas por ano, com os erros mais comuns do ciclo anterior.", "Lista de presença", "Mantém o nível"),
]

# perguntas de conscientização (7.3), com o que se espera ouvir
CONSCIENTIZACAO = [
    ("O que a política da qualidade pede de você?", "Uma frase com palavras próprias, ligada ao trabalho da pessoa. Não é preciso recitar."),
    ("Qual é o objetivo da qualidade do seu processo, e como está?", "O indicador do processo e o resultado recente."),
    ("Como o seu trabalho contribui para o resultado?", "O que a pessoa faz e o que acontece quando faz bem."),
    ("O que acontece se o padrão não for seguido?", "A consequência para o cliente, para o colega ou para a empresa."),
    ("O que você faz quando encontra um problema?", "Para quem avisa, e onde registra."),
]

CHECK = [
    "As funções que afetam a qualidade estão listadas, com as competências que cada uma exige.",
    "A escala de níveis está escrita e foi entendida pelos líderes.",
    "Cada pessoa foi avaliada em cada competência da sua função, com evidência.",
    "As lacunas estão identificadas: nível abaixo do requerido.",
    "Cada lacuna tem uma ação no plano, com responsável e prazo.",
    "Cada competência crítica tem pelo menos duas pessoas no nível 2 ou mais.",
    "Os treinamentos realizados têm registro: data, tema, instrutor e presença.",
    "O aprendizado é avaliado no fim de cada treinamento.",
    "A eficácia é avaliada no posto de trabalho, depois de um prazo definido.",
    "A matriz é atualizada depois da avaliação da eficácia.",
    "Quem entra na equipe passa pela integração antes de trabalhar sozinho.",
    "As pessoas sabem responder às perguntas de conscientização: política, objetivos, contribuição e consequências.",
]

if __name__ == "__main__":
    for nome, ex in (("EX1", EX1), ("EX2", EX2)):
        ref = ex["head"]["data"]
        print(nome, len(ex["pessoas"]), "pessoas |", len(ex["comps"]), "competências | lacunas:", sum(len(lacunas(ex, p)) for p in ex["pessoas"]),
              "| por pessoa", [(p["nome"], len(lacunas(ex, p))) for p in ex["pessoas"] if lacunas(ex, p)])
        print("    cobertura", [(c[0], cobertura(ex, k), precisam(ex, k)) for k, c in enumerate(ex["comps"])])
        print("    plano", [situacao_acao(a, ref) for a in ex["plano"]])
        for p in ex["pessoas"]:
            assert p["funcao"] in ex["funcoes"] and len(p["niveis"]) == len(ex["comps"]), p
        for a in ex["plano"]:
            assert a["pessoa"] in [p["nome"] for p in ex["pessoas"]] and a["comp"] in [c[0] for c in ex["comps"]], a
