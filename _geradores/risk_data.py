# -*- coding: utf-8 -*-
"""Dados do estudo de Matriz de riscos, usados pelo HTML e pela planilha.

As escalas, as faixas de nível e as condutas são uma convenção deste material.
Os exemplos continuam os dos outros estudos da série (pizzaria e compras).
"""
from datetime import date

D = date
NIVEIS = ["Baixo", "Médio", "Alto", "Crítico"]
EVITAR, REDUZIR, COMPARTILHAR, ACEITAR = "Evitar", "Reduzir", "Compartilhar", "Aceitar"
RESPOSTAS = [EVITAR, REDUZIR, COMPARTILHAR, ACEITAR]


def nivel(p):
    return "Crítico" if p >= 20 else ("Alto" if p >= 10 else ("Médio" if p >= 5 else "Baixo"))


PROB = [
    (1, "Muito baixa", "Menos de uma vez a cada cinco anos."),
    (2, "Baixa", "Uma vez em um período de um a cinco anos."),
    (3, "Média", "Cerca de uma vez por ano."),
    (4, "Alta", "Algumas vezes por ano."),
    (5, "Muito alta", "Uma vez por mês, ou mais."),
]
IMPACTO = [
    (1, "Muito baixo", "Resolvido na rotina, sem efeito no resultado."),
    (2, "Baixo", "Retrabalho interno ou custo pequeno. O cliente não percebe."),
    (3, "Médio", "Atraso ou falha percebida pelo cliente. Reclamação."),
    (4, "Alto", "Vários clientes afetados, perda de cliente ou custo alto."),
    (5, "Muito alto", "Dano a pessoas, descumprimento da lei ou parada da operação."),
]
CONDUTA = [
    ("Baixo", "1 a 4", "Aceitar e acompanhar na revisão anual."),
    ("Médio", "5 a 9", "Tratar quando o custo compensar. Revisar a cada seis meses."),
    ("Alto", "10 a 16", "Tratar, com ação, responsável e prazo."),
    ("Crítico", "20 a 25", "Tratar de imediato, com decisão da direção."),
]
RESP_TXT = [
    (EVITAR, "Deixar de fazer a atividade que gera o risco, ou impedir que ela aconteça.", "A probabilidade cai para o mínimo.",
     "Bloquear no sistema a compra de fornecedor não homologado."),
    (REDUZIR, "Agir sobre a causa, para o evento ficar menos provável, ou sobre a consequência, para o efeito ficar menor.",
     "A probabilidade ou o impacto diminuem.", "Homologar um segundo fornecedor. Manter estoque mínimo."),
    (COMPARTILHAR, "Dividir o efeito com outra parte, por contrato ou seguro.", "O impacto para a organização diminui.",
     "Contratar seguro. Fixar o preço em contrato."),
    (ACEITAR, "Decidir, com consciência, não agir agora, e acompanhar o risco.", "O nível não muda.",
     "Acompanhar o prazo da transportadora pelo indicador."),
]


def _riscos(rows):
    keys = ("id", "processo", "causa", "evento", "conseq", "p", "i", "resp", "acao", "quem", "prazo", "status", "pr", "ir")
    out = []
    for r in rows:
        d = dict(zip(keys, r))
        d["pts"], d["ptsr"] = d["p"] * d["i"], d["pr"] * d["ir"]
        d["nivel"], d["nivelr"] = nivel(d["pts"]), nivel(d["ptsr"])
        out.append(d)
    return out


EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", processo="Atender pedido de delivery", data=D(2026, 10, 5),
                 por="Gerente da loja, com a equipe dos dois turnos", revisao=D(2027, 4, 5),
                 objetivo="Entregar 95% dos pedidos em até 40 minutos, sem falhas de segurança do alimento.",
                 origem="Ameaças da Matriz SWOT e lacuna do requisito 6.1 no diagnóstico de 02/10/2026."),
    "riscos": _riscos([
        ("R1", "Expedição", "Chuva forte nas noites de pico", "Faltam entregadores", "Entregas fora do prazo e reclamações", 4, 3,
         REDUZIR, "Manter dois entregadores de sobreaviso nos dias com previsão de chuva.", "Líder da expedição", D(2026, 10, 30), "Concluída", 2, 3),
        ("R2", "Registro do pedido", "Queda da internet ou do sistema", "A loja fica sem registrar pedidos", "Pedidos perdidos e clientes sem resposta", 3, 4,
         REDUZIR, "Ter um celular com internet móvel e um bloco de pedidos em papel para a contingência.", "Atendente líder", D(2026, 10, 23), "Concluída", 3, 2),
        ("R3", "Armazenamento", "Falha do compressor da câmara fria", "A temperatura sobe sem ninguém perceber", "Perda de insumos e risco para a saúde do cliente", 2, 5,
         REDUZIR, "Fazer a manutenção preventiva a cada três meses.", "Pizzaiolo líder", D(2026, 11, 13), "Em andamento", 1, 5),
        ("R4", "Compras", "Um só fornecedor de queijo", "O fornecedor atrasa a entrega", "Sabores fora do cardápio no fim de semana", 3, 3,
         REDUZIR, "Homologar um segundo fornecedor de queijo.", "Gerente da loja", D(2026, 11, 27), "Em andamento", 2, 2),
        ("R5", "Expedição", "Pressa e moto sem revisão", "Acidente com o entregador", "Dano à pessoa e entregas interrompidas", 2, 5,
         REDUZIR, "Revisar as motos todo mês e treinar direção segura. O seguro, contratado junto, compartilha o custo do acidente.", "Líder da expedição", D(2026, 11, 13), "Em andamento", 1, 5),
        ("R6", "Produção", "Só o pizzaiolo líder sabe regular o forno", "O pizzaiolo líder sai ou se afasta", "Pizzas fora do padrão e atraso na produção", 2, 4,
         REDUZIR, "Registrar a regulagem do forno e treinar um segundo pizzaiolo.", "Pizzaiolo líder", D(2026, 11, 27), "Não iniciada", 2, 2),
        ("R7", "Compras", "Alta no preço dos insumos", "O custo da pizza sobe", "Margem menor ou aumento de preço ao cliente", 4, 2,
         ACEITAR, "", "Gerente da loja", None, "", 4, 2),
        ("R8", "Produção", "Sabor novo com ingrediente alergênico", "O cardápio não avisa o cliente", "Reação alérgica e responsabilidade legal", 2, 5,
         EVITAR, "Só cadastrar sabor novo no sistema com a ficha de alergênicos preenchida.", "Gerente da loja", D(2026, 10, 16), "Concluída", 1, 5),
    ]),
}

EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", processo="Adquirir materiais e serviços", data=D(2026, 10, 12),
                 por="Gerente de Suprimentos, com compradores, Recebimento e Qualidade", revisao=D(2027, 4, 12),
                 objetivo="Fornecer os materiais certos, no prazo, sem parar a produção.",
                 origem="Diagnóstico de 25/09/2026, auditoria 2026-07 e RNC 2026-31."),
    "riscos": _riscos([
        ("C1", "Planejamento de compras", "Um só fornecedor de resina", "O fornecedor deixa de entregar", "Parada da produção por falta de material", 4, 5,
         REDUZIR, "Homologar um segundo fornecedor de resina e manter estoque mínimo de 15 dias.", "Gerente de Suprimentos", D(2026, 12, 18), "Em andamento", 2, 3),
        ("C2", "Requisição", "Requisição sem especificação técnica", "O item comprado é diferente do necessário", "Devolução ao fornecedor e atraso de 9 dias", 4, 3,
         REDUZIR, "Ações do RNC 2026-31: campo obrigatório, cadastro dos itens e revisão do procedimento.", "Gerente de Suprimentos", D(2026, 10, 23), "Em andamento", 2, 3),
        ("C3", "Avaliação de fornecedores", "Fornecedor crítico sem avaliação de desempenho", "A qualidade do fornecedor cai sem ser percebida", "Material não conforme na produção", 3, 4,
         REDUZIR, "Avaliar os 12 fornecedores críticos a cada semestre, com registro.", "Comprador sênior", D(2026, 10, 30), "Em andamento", 2, 4),
        ("C4", "Negociação", "Resina com preço ligado ao dólar", "O câmbio sobe depois do pedido", "Custo acima do orçamento", 4, 3,
         COMPARTILHAR, "Negociar contrato com preço fixo por seis meses.", "Gerente de Suprimentos", D(2026, 11, 27), "Não iniciada", 4, 2),
        ("C5", "Compra de urgência", "Pressão de prazo da produção", "Compra de fornecedor não homologado", "Material sem garantia de qualidade", 3, 4,
         EVITAR, "Bloquear no sistema o pedido para fornecedor não homologado.", "Analista de sistemas", D(2026, 11, 13), "Não iniciada", 1, 4),
        ("C6", "Aprovação", "Compra acima da alçada sem conferência", "Favorecimento de um fornecedor", "Perda financeira e dano à imagem", 1, 5,
         ACEITAR, "", "Gerente de Suprimentos", None, "", 1, 5),
        ("C7", "Recebimento", "Transportadora com frota reduzida", "O material chega depois do prazo", "Reprogramação da produção", 4, 2,
         ACEITAR, "", "Líder do Recebimento", None, "", 4, 2),
        ("C8", "Homologação", "Fornecedor sem licença ambiental", "O fornecedor é autuado ou interditado", "Falta de material e dano à imagem", 2, 4,
         REDUZIR, "Exigir os documentos legais na homologação e a cada renovação.", "Comprador sênior", D(2026, 11, 27), "Não iniciada", 1, 4),
    ]),
}
# justificativa dos riscos aceitos (aparece no HTML e na planilha)
ACEITE = {
    "R7": "O preço dos insumos não depende da loja. O gerente acompanha os preços todo mês.",
    "C6": "As três cotações e as alçadas já reduzem a probabilidade ao mínimo. A auditoria confere o controle. Contingência: se aparecer um favorecimento, suspender as compras do fornecedor e levar o caso à direção.",
    "C7": "O efeito é pequeno, e o indicador de prazo do Recebimento acompanha o risco.",
}

# exemplo 3: oportunidades (probabilidade de se concretizar × benefício)
OPORT = [
    ("O1", "Cliente atual pede embalagem com material reciclado", 4, 4, "Aproveitar", "Abrir projeto de desenvolvimento da nova linha.", "Gerente de engenharia"),
    ("O2", "Grandes clientes passam a exigir a certificação ISO 9001", 3, 4, "Aproveitar", "Concluir a implantação e marcar a auditoria de certificação.", "Coordenador da Qualidade"),
    ("O3", "Fornecedor oferece resina reciclada de menor custo", 3, 3, "Testar", "Produzir um lote piloto e medir o resultado.", "Engenheiro de processos"),
    ("O4", "Feira do setor em outro estado", 2, 2, "Não agir agora", "Reavaliar no planejamento do próximo ano.", "Gerente comercial"),
]


def prioridade(p):
    return "Alta" if p >= 10 else ("Média" if p >= 5 else "Baixa")


CHECK = [
    "O escopo da análise está definido: processo, objetivo e período.",
    "As escalas de probabilidade e de impacto estão escritas e foram entendidas pelo grupo.",
    "Os riscos foram levantados com quem executa o processo.",
    "Cada risco está descrito com causa, evento e consequência.",
    "Os problemas que já aconteceram foram separados e tratados como não conformidades.",
    "As oportunidades também foram levantadas.",
    "A probabilidade e o impacto de cada risco têm justificativa.",
    "Os riscos de impacto máximo têm plano de contingência.",
    "Cada risco alto ou crítico tem resposta, responsável e prazo.",
    "O risco residual foi avaliado depois das ações.",
    "A eficácia das ações foi verificada.",
    "A matriz tem data de revisão definida.",
]


def contagem(ex, campo="nivel"):
    return {n: sum(1 for r in ex["riscos"] if r[campo] == n) for n in NIVEIS}


if __name__ == "__main__":
    for nome, ex in (("EX1", EX1), ("EX2", EX2)):
        rs = ex["riscos"]
        print(nome, len(rs), "riscos | inicial", contagem(ex), "| residual", contagem(ex, "nivelr"),
              "| média %.1f -> %.1f" % (sum(r["pts"] for r in rs) / len(rs), sum(r["ptsr"] for r in rs) / len(rs)))
        print("   ", [(r["id"], r["pts"], r["ptsr"], r["resp"]) for r in rs])
        assert all(r["ptsr"] <= r["pts"] for r in rs)
        assert all((r["resp"] == ACEITAR) == (r["id"] in ACEITE) for r in rs)
    print("oportunidades", [(o[0], o[2] * o[3], prioridade(o[2] * o[3])) for o in OPORT])
