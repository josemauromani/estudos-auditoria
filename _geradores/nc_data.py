# -*- coding: utf-8 -*-
"""Dados dos exemplos de não conformidade e ação corretiva, usados pelo HTML e pela planilha.

Os dois exemplos continuam as auditorias do estudo de Auditoria interna (aud_data.py):
cada um trata a constatação nº 1 da auditoria correspondente.
"""
from datetime import date

D = date
COR, AC = "Correção", "Ação corretiva"
ANTES, DURANTE, DEPOIS = "Antes", "Durante", "Depois"


def _acoes(rows):
    keys = ("tipo", "oque", "causa", "resp", "prazo", "status", "feito", "evid")
    return [dict(zip(keys, r), n=i + 1) for i, r in enumerate(rows)]


def _porques(rows):
    return [dict(zip(("perg", "resp", "conf"), r), n=i + 1) for i, r in enumerate(rows)]


def dentro(valor, meta, sentido):
    return valor <= meta if sentido.startswith("Menor") else valor >= meta


def media(ex, momento):
    v = [x for _, m, x in ex["eficacia"]["medicoes"] if m == momento]
    return sum(v) / len(v) if v else None


EX1 = {
    "head": dict(num="2026-05", aberta=D(2026, 9, 25), origem="Auditoria interna", ref="Auditoria 2026-03, constatação nº 1",
                 processo="Registro do pedido", area="Pizzaria (loja)", por="Atendente do turno da tarde, auditor líder",
                 resp="Atendente líder"),
    "desc": dict(req="IT-EXP-01 rev. 2, item 2: todo pedido deve ser registrado com o complemento do endereço.",
                 evid="Em 10 pedidos recebidos por telefone em 19/09, 6 foram registrados sem complemento.",
                 decl="Pedidos recebidos por telefone são registrados sem o complemento do endereço exigido pela instrução."),
    "abrang": dict(resposta="Sim",
                   texto="Site e aplicativo: o campo é obrigatório, e os 20 pedidos da amostra estavam completos. "
                         "WhatsApp: 3 de 8 pedidos sem complemento, em 26/09. O canal entrou no tratamento.",
                   conseq="Em setembro, 9 entregas atrasaram por endereço incompleto, com 2 reclamações. "
                          "Os 2 clientes receberam contato e um cupom de desconto."),
    "decisao": dict(resposta="Sim", just="A falha se repete em mais da metade dos pedidos por telefone e atrasa a entrega ao cliente."),
    "porques": _porques([
        ("Por que os pedidos por telefone ficam sem complemento?",
         "O atendente não pergunta o complemento, e a tela aceita o pedido sem ele.",
         "Observação de 12 atendimentos em 26/09: a pergunta foi feita em 4. Teste na tela do sistema."),
        ("Por que o atendente não pergunta?",
         "O roteiro de atendimento por telefone não traz essa pergunta.",
         "Leitura do roteiro afixado no balcão, de março de 2026."),
        ("Por que o roteiro não traz a pergunta?",
         "O roteiro foi escrito antes da revisão 2 da instrução, de setembro de 2026, e não foi atualizado.",
         "Comparação das datas dos dois documentos."),
        ("Por que o roteiro não foi atualizado?",
         "Quando uma instrução muda, ninguém confere os roteiros, as telas e os formulários ligados a ela.",
         "Entrevista com o gerente: a revisão 2 alterou só a instrução."),
    ]),
    "raiz": "A mudança de uma instrução não leva à revisão dos roteiros, das telas e dos formulários ligados a ela.",
    "acoes": _acoes([
        (COR, "Ligar para os clientes dos pedidos da noite que estavam sem complemento e completar o endereço antes da saída.",
         "", "Atendente líder", D(2026, 9, 25), "Concluída", D(2026, 9, 25), "5 pedidos completados antes da saída."),
        (COR, "Conferir o endereço de todo pedido por telefone e por WhatsApp antes da saída, até a ação corretiva entrar em vigor.",
         "", "Líder da expedição", D(2026, 9, 26), "Concluída", D(2026, 9, 26), "Conferência anotada na etiqueta, de 26/09 a 11/10."),
        (AC, "Tornar obrigatório o campo de complemento na tela de pedidos por telefone e por WhatsApp, com a opção “casa, sem complemento”.",
         "A tela aceita o pedido sem complemento.", "Gerente da loja", D(2026, 10, 9), "Concluída", D(2026, 10, 7),
         "Tela alterada pelo fornecedor do sistema. Teste com 5 pedidos."),
        (AC, "Revisar o roteiro de atendimento, com a pergunta do complemento, e treinar os atendentes dos dois turnos.",
         "O roteiro não traz a pergunta.", "Atendente líder", D(2026, 10, 9), "Concluída", D(2026, 10, 8),
         "Roteiro rev. 2 afixado. Lista de presença com 7 atendentes."),
        (AC, "Incluir na rotina de revisão de instruções a conferência dos roteiros, das telas e dos formulários ligados.",
         "A mudança de instrução não leva à revisão dos documentos ligados.", "Gerente da loja", D(2026, 10, 16), "Concluída", D(2026, 10, 14),
         "Rotina de documentos rev. 3, item 4."),
    ]),
    "eficacia": dict(indicador="Pedidos por telefone e por WhatsApp registrados sem complemento", unidade="%",
                     sentido="Menor é melhor", meta=5, criterio=4, periodo="semanas",
                     metodo="Amostra de 30 pedidos por semana, escolhida pelo gerente.",
                     quem="Gerente da loja", data=D(2026, 11, 9),
                     medicoes=[("Auditoria, 19/09", ANTES, 60), ("Semana de 21/09", ANTES, 57), ("Semana de 28/09", ANTES, 53),
                               ("Semana de 05/10", DURANTE, 37), ("Semana de 12/10", DEPOIS, 3), ("Semana de 19/10", DEPOIS, 0),
                               ("Semana de 26/10", DEPOIS, 3), ("Semana de 02/11", DEPOIS, 0)],
                     reincid="Não", conclusao="Eficaz",
                     obs="Entregas atrasadas por endereço incompleto: 9 em setembro, nenhuma de 12/10 a 08/11."),
    "encerr": dict(riscos="Sem alteração. A loja não mantém registro formal de riscos.",
                   mudanca="Rotina de revisão de instruções, rev. 3, e roteiro de atendimento, rev. 2.",
                   data=D(2026, 11, 10), aprov="Gerente da loja"),
}

EX2 = {
    "head": dict(num="2026-31", aberta=D(2026, 9, 22), origem="Auditoria interna", ref="Auditoria 2026-07, constatação nº 1",
                 processo="Requisição de compra", area="Suprimentos", por="Analista da Qualidade, auditor líder",
                 resp="Gerente de Suprimentos"),
    "desc": dict(req="PR-SUP-01 rev. 5, item 4.2: toda requisição deve conter a especificação técnica do item.",
                 evid="Requisições RC-0412, RC-0433, RC-0457 e RC-0461 sem especificação técnica, em amostra de 10.",
                 decl="Requisições de compra são aceitas sem a especificação técnica exigida pelo procedimento."),
    "abrang": dict(resposta="Sim",
                   texto="Levantamento das 312 requisições de janeiro a agosto: 97 sem especificação técnica, ou 31%. "
                         "Delas, 58 são da Manutenção, e 71 pedem itens sem cadastro.",
                   conseq="No período, 7 itens foram devolvidos a fornecedores por serem diferentes do necessário, "
                          "com atraso médio de 9 dias por devolução."),
    "decisao": dict(resposta="Sim", just="A falha atinge quase um terço das requisições e já causou compra de item errado."),
    "porques": _porques([
        ("Por que as requisições chegam sem especificação técnica?",
         "O campo de especificação do sistema é opcional e de texto livre.",
         "Teste no sistema: a requisição é enviada com o campo vazio."),
        ("Por que o requisitante deixa o campo vazio?",
         "Para itens sem cadastro, ele não sabe o que informar.",
         "71 das 97 requisições sem especificação pedem itens sem cadastro."),
        ("Por que os itens não têm cadastro com especificação?",
         "Não existe rotina para cadastrar o item antes da primeira compra.",
         "Leitura do PR-SUP-01 e entrevista com 3 requisitantes."),
        ("Por que o comprador aceita a requisição incompleta?",
         "Devolver a requisição atrasa a compra, e o comprador é medido só pelo prazo de atendimento.",
         "Entrevista com os 4 compradores e leitura do indicador da área."),
    ]),
    "raiz": "O processo permite requisitar sem especificação: o campo é opcional, os itens novos não têm cadastro "
            "e o indicador do comprador considera só o prazo.",
    "acoes": _acoes([
        (COR, "Completar a especificação das requisições RC-0412, RC-0433, RC-0457 e RC-0461 com as áreas requisitantes.",
         "", "Comprador sênior", D(2026, 9, 26), "Concluída", D(2026, 9, 25), "4 requisições completadas no sistema."),
        (COR, "Conferir os itens já recebidos dessas requisições contra a necessidade da área.",
         "", "Líder do Recebimento", D(2026, 9, 26), "Concluída", D(2026, 9, 26),
         "3 itens conformes. Rolamento da RC-0457 diferente do necessário: devolvido ao fornecedor."),
        (COR, "Devolver ao requisitante toda requisição sem especificação, a partir de 23/09.",
         "", "Compradores", D(2026, 9, 23), "Concluída", D(2026, 9, 23), "Comunicado da gerência, de 23/09."),
        (AC, "Tornar obrigatório o campo de especificação, com bloqueio do envio da requisição incompleta.",
         "O campo de especificação é opcional.", "Analista de sistemas", D(2026, 10, 16), "Concluída", D(2026, 10, 14),
         "Chamado 4471 encerrado. Teste com 5 requisições."),
        (AC, "Revisar o PR-SUP-01: cadastro do item antes da primeira compra, devolução da requisição incompleta em 1 dia útil "
             "e prazo do comprador contado a partir da requisição completa.",
         "Não há rotina de cadastro, e o indicador considera só o prazo.", "Gerente de Suprimentos", D(2026, 10, 16), "Concluída", D(2026, 10, 16),
         "PR-SUP-01 rev. 6 publicado."),
        (AC, "Cadastrar a especificação padrão dos 120 itens de manutenção mais comprados.",
         "Itens sem cadastro não têm especificação.", "Supervisor de manutenção", D(2026, 10, 23), "Concluída", D(2026, 10, 23),
         "120 itens cadastrados, com conferência do comprador sênior."),
        (AC, "Treinar os requisitantes das 6 áreas na revisão 6 do procedimento.",
         "O requisitante não sabe o que informar.", "Comprador sênior", D(2026, 10, 23), "Concluída", D(2026, 10, 22),
         "Listas de presença: 31 requisitantes."),
    ]),
    "eficacia": dict(indicador="Requisições com especificação ausente ou insuficiente", unidade="%",
                     sentido="Menor é melhor", meta=5, criterio=3, periodo="meses",
                     metodo="Todas as requisições do mês, na conferência do comprador.",
                     quem="Analista da Qualidade", data=D(2027, 2, 5),
                     medicoes=[("Abr/2026", ANTES, 29), ("Mai/2026", ANTES, 31), ("Jun/2026", ANTES, 33), ("Jul/2026", ANTES, 30),
                               ("Ago/2026", ANTES, 31), ("Set/2026", ANTES, 29), ("Out/2026", DURANTE, 14),
                               ("Nov/2026", DEPOIS, 4), ("Dez/2026", DEPOIS, 3), ("Jan/2027", DEPOIS, 2)],
                     reincid="Não", conclusao="Eficaz",
                     obs="Devoluções a fornecedor por item diferente do necessário: 7 de janeiro a agosto, nenhuma de novembro a janeiro."),
    "encerr": dict(riscos="Risco “compra de item diferente do necessário” reavaliado: probabilidade de alta para baixa.",
                   mudanca="PR-SUP-01 rev. 6 e campo obrigatório no sistema de requisições.",
                   data=D(2027, 2, 5), aprov="Coordenador da Qualidade"),
}

# linha do tempo do exemplo 2, em dias corridos a partir da abertura
LINHA = [("Correção", D(2026, 9, 22), D(2026, 9, 26)), ("Análise da causa", D(2026, 9, 26), D(2026, 10, 2)),
         ("Ações corretivas", D(2026, 10, 2), D(2026, 10, 23)), ("Observação do indicador", D(2026, 10, 23), D(2027, 1, 31)),
         ("Verificação da eficácia", D(2027, 1, 31), D(2027, 2, 5))]

CHECK = [
    "A não conformidade está descrita com requisito, evidência e declaração.",
    "A correção foi feita e registrada, com data e responsável.",
    "As consequências para o cliente foram tratadas.",
    "A abrangência foi verificada em outros produtos, locais e períodos.",
    "A decisão sobre a ação corretiva está registrada e justificada.",
    "A causa foi analisada com quem executa o processo.",
    "Cada causa foi confirmada com um fato ou um dado.",
    "Cada ação corretiva trata uma causa confirmada.",
    "Cada ação tem responsável, prazo e evidência de implantação.",
    "O indicador, a meta e o período de observação foram definidos antes da implantação.",
    "A eficácia foi verificada, de preferência por quem não executou as ações.",
    "Os riscos, os procedimentos e os treinamentos foram atualizados.",
]

if __name__ == "__main__":
    for nome, ex in (("EX1", EX1), ("EX2", EX2)):
        e = ex["eficacia"]
        print(nome, "ações:", {t: sum(1 for a in ex["acoes"] if a["tipo"] == t) for t in (COR, AC)},
              "| antes %.1f depois %.1f" % (media(ex, ANTES), media(ex, DEPOIS)),
              "| dentro da meta:", [dentro(v, e["meta"], e["sentido"]) for _, m, v in e["medicoes"] if m == DEPOIS])
    print("linha do tempo:", [(n, (b - a).days) for n, a, b in LINHA], "total", (LINHA[-1][2] - LINHA[0][1]).days)
