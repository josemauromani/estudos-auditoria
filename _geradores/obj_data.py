# -*- coding: utf-8 -*-
"""Dados do estudo de Objetivos da qualidade, usados pelo HTML e pela planilha.

As situações de um objetivo, a regra do caminho percorrido e os tipos de origem são uma convenção deste material.
Os exemplos continuam os dos outros estudos da série: os objetivos de 2027 da pizzaria saem da análise crítica de
14/12/2026 e os da indústria, da análise crítica de 18/02/2027.
"""
from datetime import date

D = date
MAIOR, MENOR = "Maior é melhor", "Menor é melhor"
ALC, CAM, RISCO, ANDA_O, NAOALC, SEMR = "Alcançado", "No caminho", "Em risco", "Em andamento", "Não alcançado", "Sem resultado"
SITS = [ALC, CAM, RISCO, ANDA_O, NAOALC]
NINI, ANDA, CONC, CANC = "Não iniciada", "Em andamento", "Concluída", "Cancelada"
STATUS = [NINI, ANDA, CONC, CANC]
FREQS = ["Mensal", "Trimestral", "Semestral"]
ORIGENS = ["Política da qualidade", "Estratégia (SWOT)", "Análise crítica", "Parte interessada", "Requisito legal ou contratual", "Indicador fora da meta", "Auditoria ou não conformidade"]
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
PERGUNTAS = [
    ("O quê", "O verbo e o resultado: reduzir, alcançar, manter, obter.", "Reduzir as reclamações"),
    ("Quanto", "A meta, com número e unidade, e o valor de partida.", "De 1,9 para no máximo 1,5 por 100 pedidos"),
    ("Até quando", "O prazo, com data.", "Até 31/12/2027"),
    ("Quem", "O responsável pelo resultado, e o processo.", "Atendente líder, no processo de medir e melhorar"),
    ("Como se mede", "O indicador, a fonte e a frequência.", "Reclamações por 100 pedidos, no registro, todo mês"),
]
PLANO = [
    ("O que será feito", "As ações, uma a uma, com verbo.", "Combinar a entrega na porta com as administrações dos condomínios."),
    ("Recursos", "Pessoas, dinheiro, equipamento ou tempo.", "Duas horas do gerente por condomínio."),
    ("Quem", "O responsável por cada ação.", "Gerente da loja."),
    ("Até quando", "O prazo de cada ação, anterior ao do objetivo.", "30/04/2027."),
    ("Como se avalia", "A medida que dirá se funcionou.", "Reclamações de pizza fria por condomínio, todo mês."),
]
ETAPAS = [
    ("Partir da política", "Cada objetivo responde a um compromisso da política e a uma fonte: estratégia, análise crítica, parte interessada."),
    ("Escolher poucos", "De quatro a oito. O que não cabe fica para o ano seguinte, ou vira indicador de rotina."),
    ("Escrever com medida", "Indicador, valor de partida, meta e prazo. Um responsável por objetivo."),
    ("Planejar", "O que será feito, com que recursos, por quem, até quando e como se avalia."),
    ("Acompanhar e rever", "Resultado a cada mês, situação e decisão. Objetivos revistos na análise crítica."),
]


def atende(v, meta, sentido):
    return v >= meta if sentido == MAIOR else v <= meta


def melhor(v, ref, sentido):
    return v > ref if sentido == MAIOR else v < ref


def ultimo(o):
    v = [x for x in o["res"] if x is not None]
    return v[-1] if v else None


def caminho(o):
    """Parte do caminho entre a base e a meta já percorrida, de 0 a 1. Objetivo de manutenção: 1 se atende, 0 se não."""
    u = ultimo(o)
    if u is None or o["base"] is None:
        return None
    if o["base"] == o["meta"] or not melhor(o["meta"], o["base"], o["sentido"]):
        return 1.0 if atende(u, o["meta"], o["sentido"]) else 0.0
    return max(0.0, min(1.0, (u - o["base"]) / (o["meta"] - o["base"])))


def situacao(o, ref):
    u = ultimo(o)
    if u is None:
        return SEMR
    if atende(u, o["meta"], o["sentido"]):
        return ALC
    if o["prazo"] < ref:
        return NAOALC
    if o["base"] is None:
        return ANDA_O
    return CAM if melhor(u, o["base"], o["sentido"]) else RISCO


def atrasada(a, ref):
    return a["status"] in (NINI, ANDA) and a["prazo"] < ref


def _objs(rows):
    keys = ("id", "texto", "comp", "origem", "ind", "unid", "sentido", "base", "meta", "prazo", "processo", "resp", "freq", "acoes", "res")
    out = []
    for r in rows:
        o = dict(zip(keys, r))
        assert o["origem"] in ORIGENS and o["freq"] in FREQS and o["sentido"] in (MAIOR, MENOR), o["id"]
        assert len(o["res"]) <= 12
        o["acoes"] = [dict(zip(("oque", "rec", "resp", "prazo", "status", "feito", "avalia"), a), n=i + 1) for i, a in enumerate(o["acoes"])]
        for a in o["acoes"]:
            assert a["status"] in STATUS and (a["status"] == CONC) == (a["feito"] is not None), (o["id"], a["oque"])
            assert a["prazo"] <= o["prazo"], (o["id"], a["oque"])
        out.append(o)
    return out


# ------------------------------------------------------------ exemplo 1: pizzaria, objetivos de 2027
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", data=D(2027, 2, 19), por="Gerente da loja, com o dono e os três líderes", periodo="Ano de 2027",
                 ref=D(2027, 5, 7), meses=4, origem="Análise crítica de 14/12/2026: objetivos e metas para o ano, com indicador e meta para os processos que não tinham.",
                 politica="Entregar a pizza certa, quente e no prazo, cuidar da segurança do alimento e de quem trabalha, e ouvir o cliente para melhorar todo mês."),
    "comps": [("C1", "Entregar a pizza certa, quente e no prazo."), ("C2", "Cuidar da segurança do alimento e de quem trabalha."), ("C3", "Ouvir o cliente e melhorar todo mês.")],
    "objs": _objs([
        ("O1", "Entregar 96% dos pedidos em até 40 minutos.", "C1", "Estratégia (SWOT)", "Entregas em até 40 minutos", "%", MAIOR, 95, 96, D(2027, 12, 31),
         "Entregar o pedido (P3)", "Líder da expedição", "Mensal",
         [("Rever a escala do pico com a entrega dos novos condomínios, em março.", "Dois entregadores extras nas sextas e nos sábados", "Líder da expedição", D(2027, 3, 31), CONC, D(2027, 3, 26),
           "Entregas no prazo nas noites de pico, por semana."),
          ("Estudar a compra do segundo forno, segundo item do Pareto dos atrasos.", "Orçamento de R$ 38.000", "Pizzaiolo líder", D(2027, 6, 30), ANDA, None, "Decisão dos sócios em junho.")],
         [95, 94, 96, 95]),
        ("O2", "Reduzir as reclamações para no máximo 1,5 por 100 pedidos.", "C3", "Análise crítica", "Reclamações por 100 pedidos", "por 100 pedidos", MENOR, 1.9, 1.5, D(2027, 12, 31),
         "Medir e melhorar (G2)", "Atendente líder", "Mensal",
         [("Tratar o motivo mais frequente de cada mês, com o Pareto das reclamações.", "Uma hora da reunião mensal", "Atendente líder", D(2027, 12, 31), ANDA, None,
           "Reclamações do motivo tratado, no mês seguinte."),
          ("Combinar a entrega na porta com as administrações dos condomínios.", "Duas horas do gerente por condomínio", "Gerente da loja", D(2027, 4, 30), CONC, D(2027, 4, 10),
           "Reclamações de pizza fria por condomínio, todo mês.")],
         [1.9, 1.9, 1.6, 1.4]),
        ("O3", "Alcançar a nota média 4,3 na pesquisa depois da entrega.", "C3", "Análise crítica", "Nota média das três perguntas", "de 1 a 5", MAIOR, None, 4.3, D(2027, 6, 30),
         "Medir e melhorar (G2)", "Atendente líder", "Mensal",
         [("Imprimir o código da pesquisa nas caixas e divulgar aos clientes.", "Etiquetas: R$ 300", "Atendente líder", D(2027, 1, 29), CONC, D(2027, 1, 27), "Taxa de resposta, todo mês."),
          ("Ler os comentários na reunião mensal e responder aos clientes.", "", "Gerente da loja", D(2027, 6, 30), ANDA, None, "Nota por pergunta, todo mês.")],
         [None, 4.33, 4.43, 4.53]),
        ("O4", "Reduzir os pedidos refeitos por erro para 1,5%.", "C1", "Indicador fora da meta", "Pedidos refeitos por erro", "%", MENOR, 2.0, 1.5, D(2027, 6, 30),
         "Produzir e embalar (P2)", "Pizzaiolo líder", "Mensal",
         [("Conferir o pedido na tela antes de montar, com a etiqueta rubricada.", "", "Pizzaiolo líder", D(2027, 2, 28), CONC, D(2027, 2, 20), "Pedidos refeitos, todo mês.")],
         [1.6, 1.5, 1.4, 1.3]),
        ("O5", "Dar indicador e meta aos quatro processos que não têm.", "C3", "Análise crítica", "Processos com indicador e meta", "de 9", MAIOR, 5, 9, D(2027, 2, 26),
         "Planejar e dirigir a loja (G1)", "Gerente da loja", "Mensal",
         [("Definir o indicador do salão, das compras, da manutenção e do treinamento, com os líderes.", "Quatro reuniões de uma hora", "Gerente da loja", D(2027, 2, 26), CONC, D(2027, 2, 24),
           "Processos com indicador no painel.")],
         [5, 7, 9, 9]),
        ("O6", "Reduzir o desperdício de insumos para 3,5%.", "C1", "Estratégia (SWOT)", "Desperdício de insumos", "%", MENOR, 3.9, 3.5, D(2027, 12, 31),
         "Produzir e embalar (P2)", "Gerente da loja", "Mensal",
         [("Implantar a ficha técnica e o custo por pizza.", "Oito horas do gerente e do pizzaiolo", "Gerente da loja", D(2027, 4, 30), NINI, None, "Desperdício por insumo, todo mês.")],
         [3.9, 4.0, 3.8, 3.9]),
        ("O7", "Treinar toda a equipe nas funções da matriz de competências.", "C2", "Parte interessada", "Cobertura da matriz de competências", "%", MAIOR, 60, 100, D(2027, 10, 29),
         "Treinar a equipe (A3)", "Gerente da loja", "Mensal",
         [("Treinar o segundo pizzaiolo na regulagem do forno.", "Oito horas", "Pizzaiolo líder", D(2027, 1, 22), CONC, D(2027, 1, 20), "Avaliação no posto, pelo pizzaiolo líder."),
          ("Cumprir o plano de treinamento do primeiro semestre.", "Quatro horas por semana", "Gerente da loja", D(2027, 6, 30), ANDA, None, "Cobertura da matriz, todo mês.")],
         [None, 60, 68, 75]),
    ]),
}

# ------------------------------------------------------------ exemplo 2: indústria, objetivos de 2027
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", data=D(2027, 2, 18), por="Diretor geral, com os gerentes e o Coordenador da Qualidade", periodo="Ano de 2027",
                 ref=D(2027, 7, 9), meses=6, origem="Análise crítica de 18/02/2027: a certificação e a linha com material reciclado entram nos objetivos do ano.",
                 politica="Entregar embalagens conformes e no prazo, cumprir os requisitos legais e os dos clientes, e melhorar os processos reduzindo as perdas."),
    "comps": [("C1", "Entregar embalagens conformes e no prazo."), ("C2", "Cumprir os requisitos legais e os dos clientes."), ("C3", "Melhorar os processos e reduzir as perdas.")],
    "objs": _objs([
        ("O1", "Reduzir o refugo para 2,0% do peso produzido.", "C3", "Análise crítica", "Refugo", "% do peso", MENOR, 2.6, 2.0, D(2027, 12, 31),
         "Extrusão", "Gerente industrial", "Mensal",
         [("Instalar o medidor de espessura em linha nas extrusoras 3 e 4.", "Dois medidores, com instalação: R$ 96.000", "Gerente de engenharia", D(2027, 6, 30), ANDA, None,
           "Refugo por espessura, por extrusora, todo mês."),
          ("Conduzir o ciclo PDCA do refugo, com o Pareto por defeito a cada mês.", "Equipe de melhoria, quatro horas por semana", "Gerente industrial", D(2027, 12, 31), ANDA, None,
           "Refugo total, todo mês.")],
         [2.5, 2.5, 2.4, 2.3, 2.2, 2.2]),
        ("O2", "Reduzir as reclamações para no máximo 50 por milhão de peças.", "C2", "Parte interessada", "Reclamações por milhão de peças", "por milhão", MENOR, 62, 50, D(2027, 6, 30),
         "Comercial e Qualidade", "Gerente comercial", "Mensal",
         [("Visitar o cliente A e combinar um plano conjunto.", "Uma visita", "Gerente comercial", D(2027, 3, 19), CONC, D(2027, 3, 12), "Reclamações do cliente A, todo mês."),
          ("Inspecionar 100% das bobinas do cliente A até a instalação do medidor.", "Um inspetor por turno", "Gerente industrial", D(2027, 6, 30), ANDA, None, "Bobinas reprovadas na inspeção, por semana.")],
         [58, 55, 47, 44, 40, 38]),
        ("O3", "Manter 96% das entregas na data confirmada.", "C1", "Requisito legal ou contratual", "Entregas no prazo", "%", MAIOR, 97, 96, D(2027, 12, 31),
         "Expedição", "Líder da expedição", "Mensal",
         [("Rever a programação do segmento de alimentos, que deu nota 7,8 ao prazo.", "", "Gerente comercial", D(2027, 3, 31), CONC, D(2027, 3, 26), "Entregas no prazo por segmento, todo mês.")],
         [97, 96, 97, 97, 98, 97]),
        ("O4", "Obter a certificação ISO 9001 até dezembro.", "C2", "Estratégia (SWOT)", "Etapas concluídas, de seis", "etapas", MAIOR, 0, 6, D(2027, 12, 17),
         "Gestão do sistema", "Coordenador da Qualidade", "Mensal",
         [("Contratar o organismo de certificação.", "R$ 38.000", "Diretor geral", D(2027, 4, 30), CONC, D(2027, 4, 23), "Contrato assinado."),
          ("Formar mais quatro auditores internos.", "Curso de 16 horas: R$ 6.000", "Gerente de RH", D(2027, 5, 28), CONC, D(2027, 5, 21), "Auditores aprovados no curso."),
          ("Concluir o ciclo de auditorias internas nos nove processos.", "Dez auditores, dois dias por processo", "Coordenador da Qualidade", D(2027, 8, 31), ANDA, None,
           "Processos auditados, todo mês.")],
         [0, 0, 0, 1, 2, 2]),
        ("O5", "Produzir e aprovar o lote piloto com 30% de resina reciclada.", "C3", "Parte interessada", "Etapas concluídas, de quatro", "etapas", MAIOR, 0, 4, D(2027, 9, 30),
         "Engenharia", "Gerente de engenharia", "Mensal",
         [("Homologar o fornecedor de resina reciclada.", "Ensaios externos: R$ 12.000", "Gerente de Suprimentos", D(2027, 3, 31), CONC, D(2027, 3, 29), "Laudo dos ensaios."),
          ("Produzir o lote piloto de uma tonelada.", "Uma tonelada de resina: R$ 9.000", "Gerente de engenharia", D(2027, 6, 30), CONC, D(2027, 6, 24), "Lote produzido e identificado."),
          ("Ensaiar o lote e apresentar ao cliente.", "Laboratório interno", "Gerente de engenharia", D(2027, 9, 30), NINI, None, "Aprovação do cliente por escrito.")],
         [0, 0, 1, 1, 1, 2]),
        ("O6", "Encerrar as não conformidades em até 60 dias.", "C3", "Análise crítica", "Prazo médio de encerramento", "dias", MENOR, 74, 60, D(2027, 6, 30),
         "Gestão do sistema", "Coordenador da Qualidade", "Mensal",
         [("Acompanhar as não conformidades abertas na reunião mensal de indicadores.", "", "Coordenador da Qualidade", D(2027, 3, 5), CONC, D(2027, 3, 5), "Prazo médio, todo mês.")],
         [70, 66, 61, 58, 55, 52]),
        ("O7", "Manter 100% dos fornecedores críticos avaliados a cada semestre.", "C2", "Auditoria ou não conformidade", "Fornecedores críticos avaliados", "%", MAIOR, 100, 100, D(2027, 12, 31),
         "Suprimentos", "Gerente de Suprimentos", "Mensal",
         [("Avaliar o segundo fornecedor de resina no primeiro recebimento.", "", "Comprador sênior", D(2027, 7, 30), NINI, None, "Avaliação registrada.")],
         [100, 100, 100, 100, 100, 92]),
    ]),
}

# exemplo 3: o desdobramento de um objetivo nos processos (só no treinamento)
CASCATA = dict(comp="C1 · Entregar a pizza certa, quente e no prazo.", obj="O1 · Entregar 96% dos pedidos em até 40 minutos.",
               procs=[("Registrar o pedido (P1)", "Pedidos com endereço completo: 100%", "Campo de complemento obrigatório na tela."),
                      ("Produzir e embalar (P2)", "Pedidos que esperam mais de 10 minutos pelo forno: até 5%", "Estudo do segundo forno até junho."),
                      ("Entregar o pedido (P3)", "Entregas em até 40 minutos no pico: 94%", "Escala do pico revista em março.")])

CHECK = [
    "A política da qualidade está escrita, com compromissos que podem virar objetivos.",
    "Cada objetivo responde a um compromisso da política e a uma fonte: estratégia, análise crítica, parte interessada ou requisito.",
    "São poucos objetivos, de quatro a oito, e cabem em uma página.",
    "Cada objetivo tem verbo, indicador, valor de partida, meta e prazo.",
    "Cada objetivo tem um responsável, e um só.",
    "Cada objetivo tem plano: o que será feito, com que recursos, por quem, até quando e como se avalia.",
    "O prazo de cada ação é anterior ao prazo do objetivo.",
    "Os objetivos foram desdobrados nos processos que mais pesam para cada um.",
    "Os resultados são registrados na frequência definida, e a situação é lida a cada mês.",
    "Objetivo em risco ou ação atrasada tem decisão registrada, com responsável e prazo.",
    "A equipe conhece os objetivos do seu processo e sabe como contribui para eles.",
    "Os objetivos são revistos na análise crítica, e os do ano seguinte saem dela.",
]


def resumo(ex):
    ref = ex["head"]["ref"]
    sits = [situacao(o, ref) for o in ex["objs"]]
    acoes = [a for o in ex["objs"] for a in o["acoes"]]
    return dict(n=len(ex["objs"]), sits={s: sits.count(s) for s in SITS + [SEMR]}, acoes=len(acoes), conc=sum(1 for a in acoes if a["status"] == CONC),
                atras=sum(1 for a in acoes if atrasada(a, ref)))


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        r = resumo(ex)
        print("==", nome, "| objetivos", r["n"], "| ações", r["acoes"], "concluídas", r["conc"], "atrasadas", r["atras"], "| situações", {k: v for k, v in r["sits"].items() if v})
        for o in ex["objs"]:
            c = caminho(o)
            print("  %s %-62s base %-5s último %-5s meta %-5s %-14s %s" % (o["id"], o["texto"], o["base"], ultimo(o), o["meta"], situacao(o, ex["head"]["ref"]),
                                                                           "" if c is None else "%.0f%%" % (100 * c)))
            assert len([x for x in o["res"]]) == ex["head"]["meses"], o["id"]
            assert o["comp"] in [c for c, _ in ex["comps"]]
