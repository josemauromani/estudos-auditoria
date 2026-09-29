# -*- coding: utf-8 -*-
"""Dados do estudo de Análise crítica pela direção, usados pelo HTML e pela planilha.

As três situações de uma entrada, a regra "entrada crítica pede decisão" e as situações das ações são uma convenção deste material.
Os exemplos continuam os dos outros estudos da série (pizzaria e indústria de embalagens).
"""
from datetime import date

D = date
FAV, ATE, CRI = "Favorável", "Atenção", "Crítica"
SITS = [FAV, ATE, CRI]
MELHOR, ESTAVEL, PIOR, SEMH = "Melhorando", "Estável", "Piorando", "Sem histórico"
TENDS = [MELHOR, ESTAVEL, PIOR, SEMH]
MEL, MUD, REC = "Melhoria", "Mudança no sistema", "Recursos"
TIPOS = [MEL, MUD, REC]
SIM, PARCIAL, NAO = "Sim", "Parcial", "Não"
CONC, ANDA, NINI, CANC = "Concluída", "Em andamento", "Não iniciada", "Cancelada"
STATUS = [CONC, ANDA, NINI, CANC]
A_PRAZO, A_ATRASO, A_ABERTA, A_VENCIDA, A_CANC = "Concluída no prazo", "Concluída com atraso", "No prazo", "Atrasada", "Cancelada"
SIT_ACAO = [A_PRAZO, A_ATRASO, A_ABERTA, A_VENCIDA, A_CANC]

# as doze entradas, na ordem do requisito 9.3.2 da ISO 9001:2015 (resumo com palavras próprias)
# item, nome curto, o que olhar, onde buscar, estudo da série (chave do painel) ou None
ENTRADAS = [
    ("a", "Ações das análises anteriores", "O que foi decidido nas análises anteriores, e o que foi feito.", "Ata da análise anterior e plano de ação", "w5h2"),
    ("b", "Mudanças no contexto", "O que mudou fora e dentro da organização, e afeta o sistema.", "Matriz SWOT atualizada", "swot"),
    ("c1", "Satisfação do cliente", "O que os clientes e as outras partes interessadas dizem.", "Pesquisa, reclamações e elogios", None),
    ("c2", "Objetivos da qualidade", "Quanto de cada objetivo foi alcançado.", "Quadro de objetivos, com meta e resultado", "ind"),
    ("c3", "Processos e produtos", "Como os processos se saíram, e se o produto saiu conforme.", "Indicadores dos processos e de produto", "proc"),
    ("c4", "Não conformidades", "Quantas houve, de que tipo, e se as ações funcionaram.", "Controle das não conformidades", "nc"),
    ("c5", "Monitoramento e medição", "O que as medições do período mostram.", "Painel de indicadores", "ind"),
    ("c6", "Auditorias", "O que as auditorias internas e externas constataram.", "Relatórios e programa de auditoria", "auditoria"),
    ("c7", "Provedores externos", "Como os fornecedores e os terceirizados se saíram.", "Avaliação de fornecedores", None),
    ("d", "Recursos", "Se as pessoas, os equipamentos e os sistemas são suficientes.", "Pedidos das áreas e orçamento", None),
    ("e", "Riscos e oportunidades", "Se as ações sobre os riscos e as oportunidades funcionaram.", "Matriz de riscos, com o risco residual", "riscos"),
    ("f", "Oportunidades de melhoria", "O que pode ser feito melhor, mesmo sem problema.", "Sugestões, projetos e ciclos PDCA", "pdca"),
]
ITENS = [e[0] for e in ENTRADAS]
NOME = {e[0]: e[1] for e in ENTRADAS}

# as três saídas do requisito 9.3.3, em resumo
SAIDAS = [
    (MEL, "a", "Oportunidades de melhoria", "O que será feito melhor.", "Abrir um ciclo PDCA para reduzir o refugo."),
    (MUD, "b", "Necessidades de mudança no sistema", "O que muda nos processos, nos documentos, nos objetivos ou nos indicadores.", "Auditar a Produção a cada quatro meses."),
    (REC, "c", "Necessidades de recursos", "Que pessoas, equipamentos ou dinheiro serão providos.", "Aprovar a compra do medidor de espessura."),
]

# os quatro critérios do requisito 9.3.1, em resumo
CRITERIOS = [
    ("Adequado", "O sistema serve para a organização como ela é hoje?", "Os processos, os documentos e os objetivos correspondem ao que a organização faz."),
    ("Suficiente", "O sistema cobre tudo o que precisa cobrir?", "Não há processo, requisito ou risco importante fora do sistema."),
    ("Eficaz", "O sistema entrega os resultados planejados?", "Os objetivos são alcançados, e os problemas não voltam."),
    ("Alinhado", "O sistema aponta para onde a direção quer ir?", "Os objetivos da qualidade apoiam a estratégia do negócio."),
]


def situacao_acao(a, ref):
    """Situação de uma ação de análise anterior, na data da reunião."""
    if a["status"] == CANC:
        return A_CANC
    if a["status"] == CONC:
        return A_PRAZO if a["feito"] <= a["prazo"] else A_ATRASO
    return A_VENCIDA if a["prazo"] < ref else A_ABERTA


def _entradas(rows):
    out = [dict(zip(("item", "quem", "fonte", "resultado", "tend", "sit", "conclusao"), r)) for r in rows]
    assert [e["item"] for e in out] == ITENS
    assert all(e["sit"] in SITS and e["tend"] in TENDS for e in out)
    return out


def _saidas(rows):
    rows = sorted(rows, key=lambda r: ITENS.index(r[0]))
    out = [dict(zip(("item", "tipo", "decisao", "quem", "prazo", "recurso", "valor"), r), n=i + 1) for i, r in enumerate(rows)]
    assert all(s["item"] in ITENS and s["tipo"] in TIPOS for s in out)
    return out


def _anteriores(rows):
    return [dict(zip(("origem", "acao", "quem", "prazo", "status", "feito", "eficaz", "obs"), r), n=i + 1) for i, r in enumerate(rows)]


def decisoes(ex, item):
    return [s for s in ex["saidas"] if s["item"] == item]


# ------------------------------------------------------------ exemplo 1: pizzaria, primeira análise crítica
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", data=D(2026, 12, 14), periodo="Janeiro a novembro de 2026", local="Salão da loja, antes da abertura",
                 conduz="Dono da loja", secretario="Gerente da loja", anterior=None, proxima=D(2027, 6, 14),
                 origem="Lacuna do requisito 9.3 no diagnóstico de 02/10/2026: a loja nunca tinha feito análise crítica."),
    "part": [("Dono da loja", "Direção", SIM, "Presente"), ("Gerente da loja", "Gerência", SIM, "Presente"), ("Atendente líder", "Atendimento", NAO, "Presente"),
             ("Pizzaiolo líder", "Produção", NAO, "Presente"), ("Líder da expedição", "Expedição", NAO, "Presente")],
    "anteriores": [],
    "entradas": _entradas([
        ("a", "Gerente da loja", "Diagnóstico de 02/10/2026", "Primeira análise crítica: não há ações anteriores. O ponto de partida é o diagnóstico, com 68% de atendimento.",
         SEMH, ATE, "As lacunas do diagnóstico entram nesta pauta, cada uma na sua entrada."),
        ("b", "Dono da loja", "Matriz SWOT", "Sistema de pedidos trocado em julho. Duas pizzarias novas no bairro. Preço do queijo em alta.",
         ESTAVEL, ATE, "A concorrência pede atenção ao salão, que não tem padrão de atendimento."),
        ("c1", "Atendente líder", "Registro de reclamações", "Reclamações por 100 pedidos: 3,4 em outubro de 2025 e 1,7 em novembro de 2026. Não há pesquisa de satisfação.",
         MELHOR, ATE, "A reclamação caiu, mas a loja só ouve quem reclama."),
        ("c2", "Gerente da loja", "Painel de indicadores", "Entregas em até 40 minutos: 95% em novembro, para uma meta de 95%. Os quatro indicadores estão na meta.",
         MELHOR, FAV, "Os objetivos do delivery foram alcançados. Manter."),
        ("c3", "Gerente da loja", "Mapa de processos de 14/10/2026", "63% dos elementos dos processos estão definidos. Quatro processos não têm indicador. O salão não tem padrão.",
         SEMH, ATE, "O sistema cobre bem o delivery, e pouco o restante da loja."),
        ("c4", "Gerente da loja", "Controle das não conformidades", "Dois registros no ano, os dois da auditoria 2026-03. O RNC 2026-05 foi encerrado como eficaz. O segundo está em verificação.",
         SEMH, FAV, "O tratamento funciona. Manter."),
        ("c5", "Pizzaiolo líder", "Planilhas de temperatura e de pedidos refeitos", "Temperatura registrada em todos os turnos desde outubro. Pedidos refeitos: 2,0% em setembro e 1,4% em novembro.",
         MELHOR, FAV, "As medições são feitas e usadas. Manter."),
        ("c6", "Atendente líder", "Relatório da auditoria 2026-03", "Uma auditoria no ano, no delivery: duas não conformidades menores e uma oportunidade de melhoria. O salão e as compras nunca foram auditados.",
         SEMH, ATE, "O programa de auditoria precisa cobrir os outros processos."),
        ("c7", "Gerente da loja", "Notas de compra e matriz de riscos", "O fornecedor de queijo atrasou três entregas no ano. O segundo fornecedor foi homologado em novembro. Não há avaliação registrada.",
         MELHOR, ATE, "O desempenho dos fornecedores é conhecido de memória, sem registro."),
        ("d", "Dono da loja", "Escalas e pedidos dos líderes", "Nas noites de sexta e de sábado, o atendente do delivery também atende o salão. As motos e o forno atendem à demanda.",
         ESTAVEL, ATE, "Falta uma pessoa no salão nas noites de pico."),
        ("e", "Gerente da loja", "Matriz de riscos de 05/10/2026", "Sete riscos com ação: seis ações concluídas. O treinamento do segundo pizzaiolo, do risco R6, está atrasado.",
         SEMH, ATE, "As ações funcionaram nas duas noites de chuva de novembro. Falta concluir a do risco R6."),
        ("f", "Todos", "Sugestões da equipe", "Três sugestões: pesquisa de satisfação na caixa, cardápio com fotos no salão e pedido por aplicativo de mensagens com roteiro.",
         SEMH, FAV, "A pesquisa de satisfação entra como decisão. As outras duas ficam para junho."),
    ]),
    "saidas": _saidas([
        ("c1", MEL, "Criar uma pesquisa de satisfação de três perguntas, com acesso pelo código impresso na caixa.", "Atendente líder", D(2027, 1, 29), "Impressão das etiquetas", 300),
        ("c3", MUD, "Definir indicador e meta para os quatro processos que não têm.", "Gerente da loja", D(2027, 2, 26), "", None),
        ("b", MUD, "Descrever o atendimento no salão, com SIPOC e padrão de atendimento.", "Gerente da loja", D(2027, 2, 26), "", None),
        ("c6", MUD, "Aprovar o programa de auditoria de 2027, com o salão e as compras.", "Gerente da loja", D(2027, 1, 15), "", None),
        ("c7", MUD, "Avaliar os fornecedores de insumos críticos a cada semestre, com registro.", "Gerente da loja", D(2027, 1, 29), "", None),
        ("d", REC, "Contratar um atendente de salão para as noites de sexta e de sábado.", "Dono da loja", D(2027, 1, 29), "Um atendente, duas noites por semana, por seis meses", 10800),
        ("e", MEL, "Treinar o segundo pizzaiolo na regulagem do forno, como previsto no risco R6.", "Pizzaiolo líder", D(2027, 1, 22), "Oito horas de treinamento", None),
        ("a", MUD, "Fazer a análise crítica a cada seis meses, com a pauta das doze entradas.", "Dono da loja", D(2027, 6, 14), "", None),
    ]),
    "sistema": [(SIM, "Os padrões descrevem o que a loja faz no delivery."),
                (PARCIAL, "O salão, as compras e o treinamento ainda estão fora do sistema."),
                (PARCIAL, "Eficaz no delivery. Nos outros processos, não há indicador para dizer."),
                (SIM, "Os objetivos apoiam a estratégia de crescer no delivery sem perder o salão.")],
}

# ------------------------------------------------------------ exemplo 2: indústria, análise crítica semestral
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", data=D(2027, 2, 18), periodo="Julho a dezembro de 2026, com o fechamento do ano", local="Sala de reuniões da diretoria",
                 conduz="Diretor geral", secretario="Coordenador da Qualidade", anterior=D(2026, 8, 13), proxima=D(2027, 8, 19),
                 origem="Calendário do sistema de gestão: análise crítica em fevereiro e em agosto."),
    "part": [("Diretor geral", "Direção", SIM, "Presente"), ("Gerente industrial", "Produção", SIM, "Presente"), ("Gerente comercial", "Comercial", SIM, "Presente"),
             ("Gerente de Suprimentos", "Suprimentos", SIM, "Presente"), ("Gerente de engenharia", "Engenharia", SIM, "Justificado"),
             ("Gerente de RH", "Gestão de pessoas", SIM, "Presente"), ("Coordenador da Qualidade", "Qualidade", NAO, "Presente")],
    "anteriores": _anteriores([
        (D(2026, 2, 12), "Implantar a manutenção preventiva das extrusoras.", "Supervisor de manutenção", D(2026, 6, 30), CONC, D(2026, 6, 26), SIM,
         "Paradas por quebra: de 14 para 5 por mês."),
        (D(2026, 2, 12), "Contratar um analista para o Laboratório.", "Gerente de RH", D(2026, 4, 30), CONC, D(2026, 5, 15), SIM, "Admissão em 15/05."),
        (D(2026, 2, 12), "Abrir um projeto de redução do refugo, com ciclo PDCA.", "Gerente industrial", D(2026, 3, 31), CONC, D(2026, 3, 20), PARCIAL,
         "Refugo de 3,4% para 2,6%. A meta é 2,0%."),
        (D(2026, 2, 12), "Rever a pesquisa de satisfação do cliente.", "Gerente comercial", D(2026, 5, 29), CONC, D(2026, 5, 28), SIM, "Pesquisa aplicada em novembro, com 41 respostas."),
        (D(2026, 8, 13), "Treinar os auditores internos nas diretrizes da ISO 19011.", "Coordenador da Qualidade", D(2026, 9, 30), CONC, D(2026, 9, 11), SIM, "Seis auditores treinados."),
        (D(2026, 8, 13), "Atualizar o mapa de processos com a nova linha de produção.", "Coordenador da Qualidade", D(2026, 11, 30), CONC, D(2026, 10, 20), SIM, "Mapa rev. 4."),
        (D(2026, 8, 13), "Instalar o medidor de espessura em linha na extrusora 3.", "Gerente de engenharia", D(2026, 11, 30), ANDA, None, "",
         "Orçamento recebido. Compra não aprovada."),
        (D(2026, 8, 13), "Definir o indicador de prazo de entrega por cliente.", "Gerente comercial", D(2026, 10, 30), NINI, None, "", ""),
    ]),
    "entradas": _entradas([
        ("a", "Coordenador da Qualidade", "Atas de fevereiro e de agosto de 2026", "Oito ações decididas em 2026: seis concluídas, uma delas com atraso, e duas atrasadas.",
         MELHOR, ATE, "As duas ações atrasadas dependem de decisão da direção."),
        ("b", "Diretor geral", "Matriz SWOT de janeiro de 2027", "Extrusora 4 em operação desde setembro. Dois grandes clientes passam a exigir a certificação ISO 9001. Preço da resina ligado ao dólar.",
         ESTAVEL, ATE, "A certificação deixou de ser um projeto e virou condição de venda."),
        ("c1", "Gerente comercial", "Pesquisa de novembro e reclamações", "Nota da pesquisa: 8,4, para uma meta de 8,0. Reclamações por milhão de peças: 62, para um máximo de 50. Um só cliente fez 40% das reclamações.",
         ESTAVEL, ATE, "A satisfação geral é boa. O problema está concentrado em um cliente."),
        ("c2", "Coordenador da Qualidade", "Quadro de objetivos da qualidade", "Cinco objetivos: três na meta, um em atenção e um fora da meta. O refugo fechou o ano em 2,6%, para um máximo de 2,0%.",
         MELHOR, ATE, "O objetivo de refugo não foi alcançado pelo segundo ano."),
        ("c3", "Gerente industrial", "Indicadores da Produção e do Laboratório", "Refugo acima da meta nos doze meses. Lotes reprovados na inspeção final: 1,1%. A variação de espessura é a primeira causa, nas extrusoras 3 e 4.",
         MELHOR, CRI, "O ciclo PDCA reduziu o refugo, mas a causa principal depende de equipamento."),
        ("c4", "Coordenador da Qualidade", "Controle das não conformidades", "38 registros em 2026: 30 encerrados, 27 deles como eficazes, e 8 em tratamento. O prazo médio de encerramento foi de 74 dias.",
         ESTAVEL, ATE, "O tratamento é eficaz, mas lento. Dois registros têm prazo vencido."),
        ("c5", "Coordenador da Qualidade", "Painel de indicadores", "Painel com 18 indicadores: 12 na meta, 4 em atenção e 2 fora da meta. Instrumentos calibrados no prazo: 100%.",
         ESTAVEL, FAV, "As medições são feitas e analisadas todo mês. Manter."),
        ("c6", "Coordenador da Qualidade", "Relatórios das auditorias de 2026", "Programa cumprido: 12 auditorias, nos 9 processos. Foram 10 não conformidades e 14 oportunidades de melhoria. A Produção teve 3 não conformidades.",
         ESTAVEL, ATE, "A Produção concentra as não conformidades pelo segundo ciclo."),
        ("c7", "Gerente de Suprimentos", "Avaliação de fornecedores de dezembro", "Doze fornecedores críticos avaliados: nove aprovados, dois com plano de ação e um reprovado. Nenhuma devolução por item errado desde novembro.",
         MELHOR, FAV, "As ações do RNC 2026-31 funcionaram. Manter a avaliação semestral."),
        ("d", "Gerente de RH", "Pedidos das áreas e orçamento de 2027", "O Laboratório tem um analista a mais desde maio. A Qualidade tem seis auditores para doze auditorias, e as extrusoras 3 e 4 não têm medidor de espessura.",
         ESTAVEL, ATE, "Faltam auditores e o equipamento de medição."),
        ("e", "Gerente de Suprimentos", "Matriz de riscos de Suprimentos", "Oito riscos: cinco ações concluídas e uma atrasada. O segundo fornecedor de resina, do risco C1, não foi homologado. O risco continua crítico.",
         ESTAVEL, CRI, "Um atraso do fornecedor único para a produção. A homologação depende de ensaios externos."),
        ("f", "Gerente de engenharia", "Lista de oportunidades", "Três oportunidades em andamento: linha com material reciclado, certificação e resina reciclada de menor custo.",
         SEMH, FAV, "O lote piloto com resina reciclada pode começar no primeiro semestre."),
    ]),
    "saidas": _saidas([
        ("a", MUD, "Acompanhar as ações da análise crítica na reunião mensal de indicadores, a começar pelas duas atrasadas.", "Coordenador da Qualidade", D(2027, 3, 5), "", None),
        ("b", REC, "Contratar a auditoria de certificação ISO 9001 para o segundo semestre.", "Diretor geral", D(2027, 4, 30), "Organismo de certificação", 38000),
        ("c1", MEL, "Visitar o cliente que concentra as reclamações e combinar um plano conjunto.", "Gerente comercial", D(2027, 3, 19), "", None),
        ("c3", REC, "Aprovar a compra do medidor de espessura em linha para as extrusoras 3 e 4.", "Diretor geral", D(2027, 6, 30), "Dois medidores, com instalação", 96000),
        ("c2", MEL, "Abrir novo ciclo PDCA do refugo, com meta de 2,0% até dezembro.", "Gerente industrial", D(2027, 3, 31), "", None),
        ("c4", MUD, "Definir prazo máximo de 60 dias para o tratamento das não conformidades.", "Coordenador da Qualidade", D(2027, 3, 31), "", None),
        ("c6", MUD, "Auditar a Produção a cada quatro meses, no programa de 2027.", "Coordenador da Qualidade", D(2027, 3, 12), "", None),
        ("d", REC, "Formar mais quatro auditores internos.", "Gerente de RH", D(2027, 5, 28), "Curso de 16 horas", 6000),
        ("e", REC, "Contratar os ensaios externos para concluir a homologação do segundo fornecedor de resina.", "Gerente de Suprimentos", D(2027, 3, 31), "Laboratório externo", 12000),
        ("f", MEL, "Produzir o lote piloto com resina reciclada e medir o resultado.", "Gerente de engenharia", D(2027, 6, 30), "Uma tonelada de resina", 9000),
    ]),
    "sistema": [(SIM, "O mapa de processos foi atualizado com a nova linha de produção."),
                (SIM, "Os nove processos têm dono, indicador e auditoria no programa."),
                (PARCIAL, "Três dos cinco objetivos foram alcançados. O refugo e o risco da resina seguem sem solução."),
                (SIM, "A certificação e a linha com material reciclado estão nos objetivos de 2027.")],
}

# histórico das decisões das análises anteriores da indústria (módulo 7); as duas de 2026 saem do exemplo 2
HIST_2025 = [("Fev/2025", 4, 3, 2), ("Ago/2025", 4, 2, 1)]


def historico():
    """Por análise: concluídas no prazo, concluídas com atraso e não concluídas, na data da reunião do exemplo 2."""
    out = list(HIST_2025)
    ref = EX2["head"]["data"]
    for rot, origem in (("Fev/2026", D(2026, 2, 12)), ("Ago/2026", D(2026, 8, 13))):
        s = [situacao_acao(a, ref) for a in EX2["anteriores"] if a["origem"] == origem]
        out.append((rot, s.count(A_PRAZO), s.count(A_ATRASO), s.count(A_VENCIDA) + s.count(A_ABERTA)))
    return out


# exemplo 3: pauta dividida em quatro reuniões trimestrais (só no treinamento)
TRIMESTRES = ["Março", "Junho", "Setembro", "Dezembro"]
PAUTA = {"a": (1, 1, 1, 1), "b": (0, 1, 0, 1), "c1": (1, 0, 1, 1), "c2": (1, 1, 1, 1), "c3": (1, 1, 1, 1), "c4": (1, 1, 1, 1), "c5": (0, 1, 0, 1),
         "c6": (0, 1, 0, 1), "c7": (1, 0, 0, 1), "d": (0, 1, 0, 1), "e": (0, 1, 0, 1), "f": (1, 1, 1, 1)}
assert list(PAUTA) == ITENS and all(sum(v) >= 1 for v in PAUTA.values())

CHECK = [
    "A análise crítica está no calendário, com intervalo definido.",
    "A alta direção conduz a reunião e participa dela.",
    "A pauta traz todas as entradas que a norma pede.",
    "As entradas foram enviadas aos participantes antes da reunião.",
    "As ações das análises anteriores foram conferidas, uma a uma.",
    "Cada entrada traz fatos e dados, com a tendência do período.",
    "Cada entrada tem uma conclusão escrita.",
    "As decisões tratam de melhoria, de mudanças no sistema e de recursos.",
    "Cada decisão tem responsável e prazo.",
    "Os recursos necessários foram aprovados na própria reunião.",
    "A ata registra a avaliação do sistema: adequado, suficiente, eficaz e alinhado.",
    "A ata foi guardada, e as decisões são acompanhadas até o fim.",
]

if __name__ == "__main__":
    for nome, ex in (("EX1", EX1), ("EX2", EX2)):
        e = ex["entradas"]
        print(nome, {s: sum(1 for x in e if x["sit"] == s) for s in SITS}, "| decisões", len(ex["saidas"]),
              {t: sum(1 for s in ex["saidas"] if s["tipo"] == t) for t in TIPOS}, "| valor", sum(s["valor"] or 0 for s in ex["saidas"]))
        print("   sem decisão:", [(x["item"], x["sit"]) for x in e if not decisoes(ex, x["item"])])
        assert all(decisoes(ex, x["item"]) for x in e if x["sit"] == CRI)
        print("   ações anteriores:", [situacao_acao(a, ex["head"]["data"]) for a in ex["anteriores"]])
        print("   maior texto:", max(len(x["resultado"]) for x in e), max(len(x["conclusao"]) for x in e), max(len(s["decisao"]) for s in ex["saidas"]))
    print("histórico", historico())
    print("pauta por trimestre", [sum(v[k] for v in PAUTA.values()) for k in range(4)])
