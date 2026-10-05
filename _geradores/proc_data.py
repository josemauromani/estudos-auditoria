# -*- coding: utf-8 -*-
"""Dados do estudo de Mapa de processos e diagrama de tartaruga, usados pelo HTML e pela planilha.

A divisão em processos de gestão, principais e de apoio e a pontuação dos oito elementos são uma convenção deste material.
Os exemplos continuam os dos outros estudos da série (pizzaria, compras e indústria de embalagens).
"""
from datetime import date

D = date
GESTAO, PRINCIPAL, APOIO = "Gestão", "Principal", "Apoio"
TIPOS = [GESTAO, PRINCIPAL, APOIO]
SIM, PARCIAL, NAO = "Sim", "Parcial", "Não"
PONTOS = {SIM: 1.0, PARCIAL: 0.5, NAO: 0.0}

# os oito elementos de um processo, na ordem do requisito 4.4.1 da ISO 9001:2015 (resumo com palavras próprias)
ELEMENTOS = [
    ("a", "Entradas e saídas", "O que o processo recebe e o que ele entrega estão definidos?"),
    ("b", "Sequência e interação", "Está claro de quem o processo recebe e a quem entrega?"),
    ("c", "Critérios e indicadores", "Há critérios de controle e indicadores, com meta?"),
    ("d", "Recursos", "Os recursos necessários estão definidos e disponíveis?"),
    ("e", "Responsabilidades", "O processo tem dono, e os papéis estão atribuídos?"),
    ("f", "Riscos e oportunidades", "Os riscos e as oportunidades do processo foram avaliados?"),
    ("g", "Avaliação e mudanças", "O processo é avaliado, e as mudanças são planejadas?"),
    ("h", "Melhoria", "Há melhoria registrada no processo?"),
]

# partes da tartaruga: chave -> (pergunta, título, o que escrever)
PARTES = {
    "entradas": ("O QUE ENTRA?", "Entradas", "O que o processo recebe, e de quem."),
    "saidas": ("O QUE SAI?", "Saídas", "O que o processo entrega, e a quem."),
    "oque": ("COM O QUÊ?", "Recursos", "Equipamentos, sistemas, materiais e instalações."),
    "quem": ("COM QUEM?", "Pessoas", "Funções, competências e treinamentos."),
    "como": ("COMO?", "Métodos", "Procedimentos, instruções e critérios."),
    "quanto": ("QUANTO?", "Indicadores", "Medidas de desempenho, com meta."),
    "riscos": ("E SE?", "Riscos", "O que pode impedir o resultado."),
}
ORDEM_PARTES = ["entradas", "saidas", "oque", "quem", "como", "quanto", "riscos"]


def _procs(rows):
    keys = ("id", "nome", "tipo", "dono", "objetivo", "indicador", "elem")
    out = []
    for r in rows:
        d = dict(zip(keys, r))
        d["elem"] = [{"S": SIM, "P": PARCIAL, "N": NAO}[x] for x in d["elem"]]
        assert len(d["elem"]) == 8, d["id"]
        d["pts"] = sum(PONTOS[x] for x in d["elem"])
        d["pct"] = d["pts"] / 8
        out.append(d)
    return out


# ------------------------------------------------------------ exemplo 1: pizzaria
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", data=D(2026, 10, 14), por="Gerente da loja, com os líderes dos dois turnos",
                 cliente_in="Cliente com fome", cliente_out="Cliente atendido",
                 origem="Lacuna do requisito 4.4 no diagnóstico de 02/10/2026: só o delivery estava mapeado."),
    "procs": _procs([
        ("G1", "Planejar e dirigir a loja", GESTAO, "Dono da loja", "Definir objetivos, recursos e prioridades.", "Objetivos alcançados no ano", "SPNSSPPP"),
        ("G2", "Medir e melhorar", GESTAO, "Gerente da loja", "Acompanhar os resultados e tratar os desvios.", "Indicadores na meta", "SSSSSPPS"),
        ("P1", "Registrar o pedido", PRINCIPAL, "Atendente líder", "Registrar o pedido certo, com endereço completo.", "Pedidos refeitos por erro", "SSPSSSPP"),
        ("P2", "Produzir e embalar", PRINCIPAL, "Pizzaiolo líder", "Produzir a pizza pedida, no padrão da receita.", "Desperdício de insumos", "SSSSSPSP"),
        ("P3", "Entregar o pedido", PRINCIPAL, "Líder da expedição", "Entregar o pedido certo, quente e no prazo.", "Entregas em até 40 minutos", "SSSSSSSS"),
        ("P4", "Atender no salão", PRINCIPAL, "Gerente da loja", "Servir o cliente da mesa no tempo prometido.", "", "PNNSSNNN"),
        ("A1", "Comprar e armazenar insumos", APOIO, "Gerente da loja", "Ter os insumos certos, dentro da validade.", "", "SPNSSPNN"),
        ("A2", "Manter equipamentos e motos", APOIO, "Pizzaiolo líder", "Manter forno, câmara fria e motos disponíveis.", "", "PPNSSPNN"),
        ("A3", "Treinar a equipe", APOIO, "Gerente da loja", "Ter pessoas treinadas em todas as funções.", "", "PPNPSNNN"),
    ]),
    "tartaruga": dict(
        proc="P3", data=D(2026, 10, 14),
        entradas=[("Pedido embalado e conferido", "Produzir e embalar"), ("Endereço completo do cliente", "Registrar o pedido"),
                  ("Escala de entregadores do turno", "Planejar e dirigir a loja")],
        saidas=[("Pedido entregue ao cliente", "Cliente"), ("Horário de saída e de chegada", "Medir e melhorar"),
                ("Reclamações e devoluções", "Medir e melhorar")],
        oque=[("Motos revisadas", "Revisão mensal"), ("Bolsas térmicas", "Uma por entregador"), ("Sistema de pedidos e celular", "Com internet móvel")],
        quem=[("Líder da expedição", "Conhece a instrução e a escala"), ("Entregadores", "Habilitação e direção segura"),
              ("Atendente", "Avisa o cliente sobre atrasos")],
        como=[("Instrução IT-EXP-01 rev. 2", "Agrupamento por zona"), ("Escala padrão de entregadores", "Extras nas noites de pico"),
              ("Conferência do pedido", "Rubrica na etiqueta")],
        quanto=[("Entregas em até 40 minutos", "No mínimo 95%"), ("Reclamações por 100 pedidos", "Até 2,0")],
        riscos=[("Faltam entregadores em noite de chuva", "Reduzir: sobreaviso"), ("Acidente com o entregador", "Compartilhar: seguro")],
    ),
}

# ------------------------------------------------------------ exemplo 2: processo de compras
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", data=D(2026, 10, 20), por="Gerente de Suprimentos, com compradores e Recebimento",
                 origem="Preparação da auditoria de acompanhamento do processo de aquisição."),
    "proc": dict(id="3", nome="Adquirir materiais e serviços", tipo=APOIO, dono="Gerente de Suprimentos",
                 objetivo="Fornecer os materiais certos, no prazo, sem parar a produção."),
    "tartaruga": dict(
        proc="3", data=D(2026, 10, 20),
        entradas=[("Requisição aprovada, com especificação", "Produção e Manutenção"), ("Plano de produção do mês", "Produção"),
                  ("Especificação de materiais", "Desenvolvimento de produto"),
                  ("Resultado da inspeção de recebimento", "Laboratório e controle da qualidade"),
                  ("Resultados de auditoria e ações", "Gestão do sistema da qualidade")],
        saidas=[("Pedido de compra emitido", "Fornecedor"), ("Material recebido e conferido", "Produção e Manutenção"),
                ("Avaliação dos fornecedores", "Gestão do sistema da qualidade")],
        oque=[("Sistema de compras", "Campo de especificação obrigatório"), ("Cadastro de itens e de fornecedores", "Com especificação padrão"),
              ("Área de recebimento e balança", "Balança verificada")],
        quem=[("Gerente de Suprimentos", "Aprova acima da alçada"), ("Quatro compradores", "Treinados no PR-SUP-01"),
              ("Líder do Recebimento", "Confere antes de liberar")],
        como=[("Procedimento PR-SUP-01 rev. 6", "Da requisição ao recebimento"), ("Política de compras e alçadas", "Três cotações"),
              ("Critérios de homologação", "Documentos legais incluídos")],
        quanto=[("Prazo de atendimento", "Até 5,0 dias úteis"), ("Requisições com falha de especificação", "Até 5%"),
                ("Fornecedores críticos avaliados", "100%"), ("Itens devolvidos ao fornecedor", "Nenhum")],
        riscos=[("O fornecedor único deixa de entregar", "Reduzir: segundo fornecedor"),
                ("O item comprado é diferente do necessário", "Reduzir: RNC 2026-31"),
                ("Compra de fornecedor não homologado", "Evitar: bloqueio no sistema")],
    ),
}

# ------------------------------------------------------------ exemplo 3: interações da indústria
IND = ["Comercial e análise de pedidos", "Desenvolvimento de produto", "Suprimentos", "Produção", "Laboratório e controle da qualidade",
       "Expedição e logística", "Manutenção", "Gestão de pessoas", "Gestão do sistema da qualidade"]
IND_TIPO = [PRINCIPAL, PRINCIPAL, APOIO, PRINCIPAL, APOIO, PRINCIPAL, APOIO, APOIO, GESTAO]
# (de, para, o que é entregue), com os números da lista acima
INTER = [
    (1, 2, "Requisitos do cliente para o produto novo"),
    (1, 4, "Pedido confirmado, com quantidade e prazo"),
    (1, 6, "Endereço e condições de entrega"),
    (2, 3, "Especificação de materiais"),
    (2, 4, "Desenho e parâmetros do processo"),
    (2, 5, "Plano de controle do produto"),
    (3, 4, "Material recebido e conferido"),
    (3, 7, "Peças e serviços de manutenção"),
    (3, 9, "Avaliação dos fornecedores"),
    (4, 3, "Requisição de compra, com especificação, e plano de produção do mês"),
    (4, 5, "Amostras e lotes para inspeção"),
    (4, 6, "Produto embalado e liberado"),
    (4, 7, "Pedido de manutenção"),
    (5, 3, "Resultado da inspeção de recebimento"),
    (5, 4, "Laudo de liberação do lote"),
    (5, 9, "Registros de produto não conforme"),
    (6, 1, "Confirmação da entrega"),
    (7, 3, "Requisição de compra, com especificação"),
    (7, 4, "Equipamento disponível"),
    (8, 4, "Operadores treinados"),
    (8, 9, "Registros de competência"),
    (9, 3, "Resultados de auditoria e ações"),
    (9, 4, "Resultados de auditoria e ações"),
    (9, 8, "Necessidades de treinamento"),
]
assert all(1 <= a <= 9 and 1 <= b <= 9 and a != b for a, b, _ in INTER) and len({(a, b) for a, b, _ in INTER}) == len(INTER)


def fornece(n):
    return [(b, t) for a, b, t in INTER if a == n]


def recebe(n):
    return [(a, t) for a, b, t in INTER if b == n]


CHECK = [
    "O mapa mostra todos os processos necessários para atender ao cliente.",
    "Os processos principais estão em sequência, do pedido à entrega.",
    "Os processos de gestão e de apoio estão identificados.",
    "Cada processo tem um dono, que responde pelo resultado.",
    "As entradas e as saídas de cada processo estão definidas.",
    "As interações estão descritas: o que um processo entrega ao outro.",
    "Os recursos e as competências de cada processo estão definidos.",
    "Os métodos e os documentos de cada processo estão identificados.",
    "Cada processo tem pelo menos um indicador, com meta.",
    "Os riscos e as oportunidades de cada processo foram avaliados.",
    "O mapa foi validado por quem executa os processos.",
    "O mapa é revisto a cada mudança e pelo menos uma vez por ano.",
]

if __name__ == "__main__":
    for p in EX1["procs"]:
        print(p["id"], p["nome"], p["tipo"], "%.1f de 8" % p["pts"], "%d%%" % round(p["pct"] * 100))
    print("média", "%.0f%%" % (100 * sum(p["pct"] for p in EX1["procs"]) / len(EX1["procs"])))
    for k, (_, nome, _) in enumerate(ELEMENTOS):
        v = [p["elem"][k] for p in EX1["procs"]]
        print("  ", nome, v.count(SIM), v.count(PARCIAL), v.count(NAO))
    for n, nome in enumerate(IND, 1):
        print(n, nome, "| fornece a", len(fornece(n)), "| recebe de", len(recebe(n)))
    for ex in (EX1, EX2):
        t = ex["tartaruga"]
        print(max(len(a) for k in ORDEM_PARTES for a, _ in t[k]), max(len(b) for k in ORDEM_PARTES for _, b in t[k]))
