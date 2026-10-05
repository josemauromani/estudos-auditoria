# -*- coding: utf-8 -*-
"""Dados dos exemplos de auditoria interna, usados pelo HTML e pela planilha."""
from datetime import date, time

C, NC, OM = "Conforme", "Não conforme", "Oportunidade de melhoria"

# ---------------------------------------------------------------- programa: pontuação de prioridade
IMP = {"Alta": 3, "Média": 2, "Baixa": 1}
MUD = {"Sim": 2, "Não": 0}
ANT = {"NC maior": 3, "NC menor": 2, "Não auditado": 2, "Sem NC": 0}


def pontos(p):
    return IMP[p["imp"]] + MUD[p["mud"]] + ANT[p["ant"]]


def prioridade(v):
    return "Alta" if v >= 6 else ("Média" if v >= 3 else "Baixa")


FREQ = {"Alta": "A cada 6 meses", "Média": "A cada 12 meses", "Baixa": "A cada 18 meses"}


def _lv(rows):
    keys = ("req", "verificar", "amostra", "evid", "res", "ref")
    return [dict(zip(keys, r), n=i + 1) for i, r in enumerate(rows)]


def _ct(rows):
    keys = ("tipo", "processo", "req", "evid", "decl", "resp", "prazo", "status")
    return [dict(zip(keys, r), n=i + 1) for i, r in enumerate(rows)]


D, T = date, time

EX1 = {
    "head": dict(num="2026-03", processo="Atender pedido de delivery", area="Pizzaria (loja)", data=D(2026, 9, 25),
                 lider="Atendente do turno da tarde", equipe="Pizzaiolo do turno da tarde",
                 auditado="Líder da expedição e atendentes da noite", versao="1.0",
                 objetivo="Verificar se os padrões definidos no ciclo de melhoria das entregas estão sendo seguidos.",
                 escopo="Registro do pedido, expedição e controle de temperatura, nos turnos da noite de sexta e de sábado.",
                 criterios="Instrução IT-EXP-01 rev. 2, escala padrão de entregadores e rotina de controle de temperatura."),
    "agenda": [
        (T(18, 0), T(18, 20), "Reunião de abertura", "Todos", "Gerente e líder da expedição", "Escritório"),
        (T(18, 20), T(19, 0), "Análise de registros: escala, temperatura e indicador", "Atendente", "Gerente", "Escritório"),
        (T(19, 0), T(21, 0), "Observação da expedição no horário de pico", "Atendente e pizzaiolo", "Líder da expedição", "Expedição"),
        (T(21, 0), T(21, 40), "Entrevistas: atendimento por telefone e entregadores", "Pizzaiolo", "Atendentes e entregadores", "Balcão"),
        (T(21, 40), T(22, 10), "Reunião da equipe auditora", "Atendente e pizzaiolo", "", "Escritório"),
        (T(22, 10), T(22, 40), "Reunião de encerramento", "Todos", "Gerente e líder da expedição", "Escritório"),
    ],
    "lista": _lv([
        ("IT-EXP-01, item 3", "Os pedidos são agrupados por zona antes da saída?", "20 saídas, sexta-feira, das 19h às 21h",
         "18 saídas agrupadas. 2 saídas avulsas, de pedidos urgentes, como prevê a instrução.", C, None),
        ("IT-EXP-01, item 5", "O pedido é conferido antes de ser embalado?", "20 pedidos embalados",
         "20 etiquetas rubricadas pelo responsável pela conferência.", C, None),
        ("Escala padrão", "Há dois entregadores extras nas sextas e nos sábados, das 19h às 22h?", "Escalas das últimas 4 semanas",
         "Escala cumprida nas 4 semanas.", C, None),
        ("IT-EXP-01, item 2", "O pedido é registrado com o complemento do endereço?", "30 pedidos: 20 do site e do aplicativo, 10 por telefone",
         "Site e aplicativo: 20 com complemento. Telefone: 6 de 10 sem complemento.", NC, 1),
        ("Rotina de temperatura", "A temperatura da câmara fria é registrada em cada turno?", "Registros de 14 dias, 28 turnos",
         "3 turnos sem registro: 12/09 noite, 13/09 noite e 20/09 noite.", NC, 2),
        ("Indicador de entregas", "O indicador de entregas no prazo é atualizado toda semana?", "Últimas 8 semanas",
         "Gráfico atualizado nas 8 semanas, por faixa de horário.", C, None),
        ("IT-EXP-01, item 7", "A equipe da expedição foi treinada no método de agrupamento?", "Lista de presença e 2 entregadores admitidos em setembro",
         "Equipe treinada em julho. A instrução não diz como treinar quem entra depois. 1 dos 2 novos ainda não foi treinado.", NC, 3),
    ]),
    "const": _ct([
        ("NC menor", "Registro do pedido", "IT-EXP-01 rev. 2, item 2: todo pedido deve ser registrado com o complemento do endereço.",
         "Em 10 pedidos recebidos por telefone em 19/09, 6 foram registrados sem complemento.",
         "Pedidos recebidos por telefone são registrados sem o complemento do endereço exigido pela instrução.",
         "Atendente líder", D(2026, 10, 16), "Em tratamento"),
        ("NC menor", "Controle de temperatura", "Rotina de controle: a temperatura da câmara fria deve ser registrada uma vez em cada turno.",
         "Planilha de temperatura sem registro nos turnos da noite de 12/09, 13/09 e 20/09, em 28 turnos analisados.",
         "O registro de temperatura da câmara fria não é feito em todos os turnos.",
         "Pizzaiolo líder", D(2026, 10, 9), "Aberta"),
        ("NC menor", "Expedição", "IT-EXP-01 rev. 2, item 7: a equipe deve ser treinada no método.",
         "A equipe foi treinada em julho. 1 de 2 entregadores admitidos em setembro ainda não recebeu o treinamento.",
         "Entregadores admitidos depois do treinamento inicial trabalham sem o treinamento no método exigido pela instrução.",
         "Líder da expedição", D(2026, 10, 30), "Aberta"),
    ]),
    "conclusao": "Os padrões da expedição estão implantados e são seguidos. O registro do pedido por telefone, o controle de temperatura e o treinamento de quem entra na expedição precisam de ação corretiva.",
}

EX2 = {
    "head": dict(num="2026-07", processo="Adquirir materiais e serviços", area="Suprimentos", data=D(2026, 9, 22),
                 lider="Analista da Qualidade", equipe="Engenheiro de processos",
                 auditado="Gerente de Suprimentos e compradores", versao="1.0",
                 objetivo="Verificar a conformidade do processo de aquisição com o procedimento interno e com o requisito 8.4 da ISO 9001:2015.",
                 escopo="Requisições, cotações, pedidos, recebimentos e avaliação de fornecedores, de janeiro a agosto de 2026.",
                 criterios="ISO 9001:2015, requisito 8.4. Procedimento PR-SUP-01 rev. 5. Política de compras e alçadas."),
    "agenda": [
        (T(8, 30), T(9, 0), "Reunião de abertura", "Todos", "Gerente de Suprimentos", "Sala de reuniões"),
        (T(9, 0), T(10, 30), "Requisição e análise", "Analista da Qualidade", "Compradores", "Suprimentos"),
        (T(10, 30), T(12, 0), "Cotação e seleção da proposta", "Engenheiro de processos", "Compradores", "Suprimentos"),
        (T(13, 0), T(14, 30), "Pedido, contrato e recebimento", "Analista da Qualidade", "Comprador e Recebimento", "Almoxarifado"),
        (T(14, 30), T(15, 30), "Avaliação de fornecedores", "Engenheiro de processos", "Gerente de Suprimentos", "Suprimentos"),
        (T(15, 30), T(16, 15), "Reunião da equipe auditora", "Todos", "", "Sala de reuniões"),
        (T(16, 15), T(17, 0), "Reunião de encerramento", "Todos", "Gerente de Suprimentos", "Sala de reuniões"),
    ],
    "lista": _lv([
        ("PR-SUP-01, item 4.1", "A requisição é aprovada pelo gestor da área antes da compra?", "10 requisições, de janeiro a agosto",
         "10 requisições com aprovação registrada no sistema.", C, None),
        ("PR-SUP-01, item 4.2", "A requisição traz a especificação técnica do item?", "As mesmas 10 requisições",
         "4 requisições sem especificação técnica: RC-0412, RC-0433, RC-0457 e RC-0461.", NC, 1),
        ("Política de compras", "Compras acima de R$ 2.000 têm três cotações?", "8 compras acima do valor",
         "8 processos com três cotações arquivadas.", C, None),
        ("ISO 9001, 8.4.1", "Os critérios de seleção de fornecedores estão definidos e são aplicados?", "Procedimento e 5 homologações de 2026",
         "Critérios descritos no procedimento e aplicados nas 5 homologações.", C, None),
        ("ISO 9001, 8.4.1", "O desempenho dos fornecedores críticos é avaliado, com registro?", "12 fornecedores críticos",
         "5 fornecedores sem avaliação registrada em 2026: F-03, F-07, F-08, F-11 e F-12.", NC, 2),
        ("ISO 9001, 8.4.3", "O pedido de compra informa os requisitos do produto ao fornecedor?", "10 pedidos emitidos",
         "10 pedidos com especificação, quantidade, prazo e condição de aceitação.", C, None),
        ("ISO 9001, 8.4.2", "O item recebido é conferido antes da liberação?", "10 recebimentos",
         "Conferência feita nos 10. O registro é feito em papel e redigitado no sistema no dia seguinte.", OM, 3),
        ("Política de compras", "As alçadas de aprovação são respeitadas?", "10 pedidos emitidos",
         "10 pedidos aprovados dentro da alçada.", C, None),
    ]),
    "const": _ct([
        ("NC menor", "Requisição de compra", "PR-SUP-01 rev. 5, item 4.2: toda requisição deve conter a especificação técnica do item.",
         "Requisições RC-0412, RC-0433, RC-0457 e RC-0461 sem especificação técnica, em amostra de 10.",
         "Requisições de compra são aceitas sem a especificação técnica exigida pelo procedimento.",
         "Gerente de Suprimentos", D(2026, 10, 23), "Em tratamento"),
        ("NC menor", "Avaliação de fornecedores", "ISO 9001:2015, 8.4.1, e PR-SUP-01 rev. 5, item 6.1: avaliar o desempenho dos fornecedores críticos a cada semestre e reter o registro.",
         "Fornecedores críticos F-03, F-07, F-08, F-11 e F-12 sem avaliação registrada em 2026, em 12 verificados.",
         "A avaliação semestral de desempenho não foi realizada para parte dos fornecedores críticos.",
         "Comprador sênior", D(2026, 10, 30), "Aberta"),
        ("Oportunidade de melhoria", "Recebimento", "ISO 9001:2015, 8.4.2: assegurar que os itens recebidos atendem aos requisitos.",
         "A conferência é registrada em formulário de papel e redigitada no sistema no dia seguinte.",
         "O registro direto no sistema eliminaria a redigitação e o atraso de um dia na informação.",
         "Líder do Recebimento", D(2026, 11, 27), "Aberta"),
    ]),
    "conclusao": "O processo está implantado e atende a seis dos oito itens verificados. A especificação das requisições e a avaliação de fornecedores precisam de ação corretiva.",
}

# ---------------------------------------------------------------- exemplo 3: programa anual
PROG = [dict(zip(("proc", "dono", "imp", "mud", "ant", "mes", "lider"), r)) for r in [
    ("Comercial e análise de pedidos", "Gerente comercial", "Média", "Não", "Sem NC", "Mai", "Analista da Qualidade"),
    ("Desenvolvimento de produto", "Gerente de engenharia", "Alta", "Sim", "NC menor", "Mar e Set", "Engenheiro de processos"),
    ("Suprimentos", "Gerente de Suprimentos", "Alta", "Não", "NC menor", "Set", "Analista da Qualidade"),
    ("Produção", "Gerente industrial", "Alta", "Sim", "NC maior", "Abr e Out", "Coordenador da Qualidade"),
    ("Laboratório e controle da qualidade", "Coordenador da Qualidade", "Alta", "Não", "NC maior", "Fev e Ago", "Engenheiro de processos"),
    ("Expedição e logística", "Supervisor de logística", "Média", "Sim", "Sem NC", "Jun", "Analista de RH"),
    ("Manutenção", "Supervisor de manutenção", "Média", "Não", "Não auditado", "Jul", "Analista da Qualidade"),
    ("Gestão de pessoas", "Gerente de RH", "Baixa", "Não", "Sem NC", "Nov", "Engenheiro de processos"),
    ("Gestão do sistema da qualidade", "Coordenador da Qualidade", "Média", "Não", "NC menor", "Out", "Gerente de RH"),
]]
# resultado do ciclo: não conformidades e oportunidades de melhoria por processo
RESULT = [("Produção", 3, 2), ("Laboratório e controle da qualidade", 2, 1), ("Suprimentos", 2, 1), ("Desenvolvimento de produto", 1, 3),
          ("Gestão do sistema da qualidade", 1, 1), ("Manutenção", 1, 2), ("Expedição e logística", 0, 2), ("Comercial e análise de pedidos", 0, 1),
          ("Gestão de pessoas", 0, 1)]
