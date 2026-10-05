# -*- coding: utf-8 -*-
"""Dados do estudo de Satisfação do cliente, usados pelo HTML e pela planilha.

A escala de satisfação, o limite de "satisfeito", a classificação da indicação e os prazos de resposta são uma convenção deste material.
Os exemplos continuam os dos outros estudos da série (pizzaria e indústria de embalagens).
"""
from datetime import date

D = date
# as três famílias de fontes
FONTES = [
    ("Diz, quando perguntamos", "Pesquisa depois da entrega, pesquisa anual, entrevista.", "Nota média, percentual de satisfeitos, indicação."),
    ("Diz, sem perguntar", "Reclamações, elogios, comentários, devoluções pedidas.", "Reclamações por 100 pedidos, prazo da primeira resposta, motivos."),
    ("Faz", "Volta a comprar, cancela, reduz o pedido, indica a outros.", "Recompra, clientes perdidos, participação de mercado."),
]
SATISFEITO = 0.8   # nota igual ou acima de 80% da escala conta como satisfeito
PROMOTOR, NEUTRO, DETRATOR = "Promotor", "Neutro", "Detrator"
PRAZO_RESPOSTA = 2  # dias úteis para a primeira resposta a uma reclamação, neste modelo
PRAZO_SOLUCAO = 10  # dias para resolver
ETAPAS = [
    ("Receber", "Qualquer canal: telefone, mensagem, site, visita. Quem recebe registra."),
    ("Registrar", "Data, cliente, pedido, motivo e o que o cliente pede."),
    ("Responder", f"Em até {PRAZO_RESPOSTA} dias úteis: o cliente sabe que foi ouvido e quem cuida."),
    ("Resolver", f"Em até {PRAZO_SOLUCAO} dias: reposição, desconto, devolução ou explicação."),
    ("Analisar", "Motivo agrupado. A procedente é não conformidade; a grave ou repetida pede ação corretiva."),
    ("Devolver", "O cliente sabe o que foi feito. A equipe sabe o que mudou."),
]


def classificar(nota):
    """Classificação da indicação, de 0 a 10."""
    return PROMOTOR if nota >= 9 else (NEUTRO if nota >= 7 else DETRATOR)


def nps(prom, neu, det):
    n = prom + neu + det
    return round(100 * (prom - det) / n) if n else 0


# ------------------------------------------------------------ exemplo 1: pizzaria
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", data=D(2027, 5, 5), periodo="Fevereiro a abril de 2027", por="Atendente líder, com o gerente da loja",
                 origem="Decisão da análise crítica de 14/12/2026: pesquisa de três perguntas, com acesso pelo código impresso na caixa.",
                 escala=5, canal="Código impresso na caixa, lido pelo celular. Três perguntas e um campo de comentário."),
    "perguntas": [("P1", "Como foi a entrega?", "Prazo e estado do pedido"), ("P2", "Como estava a pizza?", "Sabor, temperatura e padrão"),
                  ("P3", "Como foi o atendimento?", "Registro do pedido e contato")],
    # mês: pedidos, respostas, média por pergunta, promotores, neutros, detratores, reclamações
    "meses": [("Fev/2027", 840, 96, [4.1, 4.4, 4.5], 52, 31, 13, 16), ("Mar/2027", 910, 108, [4.3, 4.4, 4.6], 63, 32, 13, 15),
              ("Abr/2027", 870, 108, [4.5, 4.5, 4.6], 71, 28, 9, 12)],
    "motivos": [("Entrega atrasada", 34), ("Pizza fria", 19), ("Pedido errado ou incompleto", 11), ("Embalagem amassada", 7), ("Atendimento", 4)],
    "reclamacoes": [
        (D(2027, 2, 6), "Pedido 2.318", "Aplicativo", "Entrega atrasada", "Pedido chegou 25 minutos depois do prometido, na noite de chuva.", D(2027, 2, 6), D(2027, 2, 7), "", "Resolvida"),
        (D(2027, 2, 20), "Pedido 2.671", "Telefone", "Pizza fria", "Pizza fria no salão de festas: entrega em condomínio, 15 minutos na portaria.", D(2027, 2, 20), D(2027, 2, 22), "", "Resolvida"),
        (D(2027, 3, 13), "Pedido 3.104", "Aplicativo", "Pedido errado ou incompleto", "Faltou o refrigerante.", D(2027, 3, 13), D(2027, 3, 13), "", "Resolvida"),
        (D(2027, 4, 3), "Pedido 3.611", "Mensagem", "Pizza fria", "Terceira reclamação de pizza fria do mesmo condomínio.", D(2027, 4, 3), D(2027, 4, 10), "RNC 2027-04", "Resolvida"),
        (D(2027, 4, 24), "Pedido 3.902", "Aplicativo", "Embalagem amassada", "Caixa amassada, pizza colada na tampa.", D(2027, 4, 27), None, "", "Aberta"),
    ],
    "metas": dict(media=4.3, satisfeitos=0.80, nps=50, reclamacoes=1.5, resposta=1.0),
}

# ------------------------------------------------------------ exemplo 2: indústria de embalagens
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", data=D(2026, 12, 4), periodo="Pesquisa anual, novembro de 2026, e reclamações de 2026",
                 por="Gerente comercial, com a Qualidade", origem="Ação da análise crítica de 12/02/2026: rever a pesquisa de satisfação do cliente.",
                 escala=10, canal="Pesquisa por e-mail aos 58 clientes ativos, com cinco perguntas de 0 a 10 e uma de indicação. 41 respostas, 71%."),
    "perguntas": [("Q1", "Qualidade do produto", "Conformidade e constância"), ("Q2", "Prazo de entrega", "Cumprimento do combinado"),
                  ("Q3", "Atendimento comercial", "Resposta a pedidos e cotações"), ("Q4", "Assistência técnica", "Apoio no uso da embalagem"),
                  ("Q5", "Documentação", "Laudos, certificados e notas")],
    # segmento: clientes, respostas, média por pergunta, promotores, neutros, detratores
    "segmentos": [("Alimentos", 24, 19, [8.5, 7.8, 8.9, 7.9, 8.3], 9, 8, 2), ("Cosméticos", 18, 12, [8.9, 8.4, 9.0, 8.2, 8.1], 7, 4, 1),
                  ("Industrial", 16, 10, [8.8, 8.3, 8.8, 8.0, 8.2], 4, 5, 1)],
    "motivos": [("Espessura fora da especificação", 8), ("Impressão fora do padrão", 4), ("Atraso na entrega", 4), ("Embalagem de transporte danificada", 2)],
    "cliente_x": dict(nome="Cliente A, do segmento de alimentos", reclamacoes=7, total=18),
    "metas": dict(media=8.0, satisfeitos=0.75, nps=40, reclamacoes=None, resposta=2.0),
}

# exemplo 3: o tratamento de uma reclamação, do registro à devolutiva (só no treinamento)
RECLAMACAO = dict(cliente="Cliente A, alimentos", data=D(2026, 9, 14), motivo="Espessura fora da especificação",
                  descricao="Lote 26-0911 de filme para embalagem de biscoito com espessura abaixo do mínimo em 3 bobinas. A linha do cliente parou 40 minutos.",
                  linha=[
                      (D(2026, 9, 14), "Recebida", "Ligação do comprador do cliente ao gerente comercial, às 9h. Registrada às 9h30."),
                      (D(2026, 9, 14), "Respondida", "E-mail no mesmo dia: reposição de 3 bobinas em 48 horas e visita técnica marcada."),
                      (D(2026, 9, 16), "Resolvida", "Bobinas repostas. Lote reprovado devolvido para análise."),
                      (D(2026, 9, 23), "Analisada", "RNC 2026-32: variação de espessura na extrusora 3, sem medidor em linha. Sétima reclamação do cliente no ano, quinta pelo mesmo motivo."),
                      (D(2026, 10, 2), "Devolvida", "Visita ao cliente: plano apresentado, com inspeção de 100% das bobinas para ele até a compra dos medidores."),
                      (D(2027, 2, 18), "Fechada", "Análise crítica aprova os dois medidores de espessura em linha. Nenhuma reclamação do cliente A de outubro a fevereiro."),
                  ])

CHECK = [
    "Está definido quem é o cliente e o que ele valoriza no produto ou no serviço.",
    "Há pelo menos uma fonte de cada família: o que o cliente diz quando perguntamos, o que diz sem perguntar e o que faz.",
    "A pesquisa é curta, com perguntas ligadas ao que o cliente valoriza, e tem frequência definida.",
    "A amostra e a taxa de resposta são conhecidas, e o resultado não é generalizado além delas.",
    "Toda reclamação é registrada, de qualquer canal, com data, motivo e o que o cliente pede.",
    "A reclamação recebe resposta no prazo definido, e o cliente sabe quem cuida dela.",
    "Os motivos das reclamações e das notas baixas são agrupados e analisados.",
    "Reclamação procedente é tratada como não conformidade, com correção, e a grave ou repetida tem análise de causa.",
    "Os indicadores de satisfação têm meta e entram no painel da organização.",
    "O resultado é analisado em reunião, com decisões registradas.",
    "O cliente recebe a devolutiva: o que foi feito com o que ele disse.",
    "A satisfação do cliente é entrada da análise crítica pela direção.",
]


def resumo_mes(m):
    rot, ped, resp, medias, prom, neu, det, rec = m
    return dict(rot=rot, pedidos=ped, respostas=resp, medias=medias, media=round(sum(medias) / len(medias), 2), prom=prom, neu=neu, det=det,
                nps=nps(prom, neu, det), reclamacoes=rec, taxa=resp / ped, por100=100 * rec / ped)


if __name__ == "__main__":
    for m in EX1["meses"]:
        r = resumo_mes(m)
        assert r["prom"] + r["neu"] + r["det"] == r["respostas"], r["rot"]
        print(r["rot"], "média %.2f" % r["media"], "NPS", r["nps"], "taxa %.0f%%" % (100 * r["taxa"]), "recl. por 100: %.1f" % r["por100"])
    tot = sum(m[2] for m in EX1["meses"])
    print("respostas", tot, "| motivos", sum(v for _, v in EX1["motivos"]))
    for seg in EX2["segmentos"]:
        rot, cli, resp, medias, prom, neu, det = seg
        assert prom + neu + det == resp, rot
        print(rot, "média %.2f" % (sum(medias) / len(medias)), "NPS", nps(prom, neu, det))
    n = sum(s[2] for s in EX2["segmentos"])
    geral = [sum(s[3][k] * s[2] for s in EX2["segmentos"]) / n for k in range(5)]
    print("indústria: respostas", n, "de", sum(s[1] for s in EX2["segmentos"]), "| médias", [round(g, 1) for g in geral], "| geral %.2f" % (sum(geral) / 5),
          "| NPS", nps(sum(s[4] for s in EX2["segmentos"]), sum(s[5] for s in EX2["segmentos"]), sum(s[6] for s in EX2["segmentos"])))
