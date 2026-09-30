# -*- coding: utf-8 -*-
"""Dados do estudo de Pareto e folha de verificação, usados pelo HTML e pela planilha.

O corte de 80%, o limite de "Outros", o mínimo de ocorrências e a regra do Pareto plano são uma convenção deste material.
Os exemplos continuam os dos outros estudos da série: os atrasos da pizzaria e as requisições devolvidas de compras
são os mesmos dos estudos de PDCA e de Ishikawa.
"""
from datetime import date

D = date
OUTROS = "Outros"
CORTE = 0.80        # as categorias necessárias para chegar a este acumulado são a prioridade
OUTROS_MAX = 0.10   # acima disso, "Outros" esconde alguma categoria e deve ser aberto
MIN_OBS = 50        # abaixo disso, a ordem das barras pode ser acaso
PLANO = 0.50        # as duas primeiras categorias somam menos do que isso: Pareto plano
PRIOR, DEPOIS = "Prioridade", "Depois"

ETAPAS = [
    ("Definir", "O que se conta, onde, quando e por quem. Categorias com definição escrita."),
    ("Contar", "Folha de verificação preenchida na hora, por quem vê a ocorrência."),
    ("Ordenar", "Do maior para o menor, com percentual e acumulado. Outros por último."),
    ("Ler", "Onde está o peso? Se o gráfico for plano, estratificar por outro fator."),
    ("Agir", "Analisar a causa das primeiras barras, agir e contar de novo."),
]


def ordenar(rows):
    """Do maior para o menor, com "Outros" sempre por último. No empate, vale a ordem da lista."""
    nomeadas = [r for r in rows if r[0] != OUTROS and r[1] > 0]
    outros = [r for r in rows if r[0] == OUTROS and r[1] > 0]
    return sorted(nomeadas, key=lambda r: -r[1]) + outros


def pareto(rows):
    """Lista ordenada, com valor, parte do total, acumulado e classe de cada categoria."""
    rows = ordenar(rows)
    total = sum(v for _, v in rows)
    out, acc = [], 0
    for k, (nome, v) in enumerate(rows, 1):
        antes = acc / total
        acc += v
        classe = OUTROS if nome == OUTROS else (PRIOR if round(antes, 6) < CORTE else DEPOIS)
        out.append(dict(k=k, nome=nome, v=v, pct=v / total, acc=acc / total, classe=classe))
    return out


def aviso(rows, ocorrencias=None):
    """O mesmo aviso que a planilha mostra na aba Pareto."""
    p = pareto(rows)
    n = ocorrencias if ocorrencias is not None else sum(r["v"] for r in p)
    nomeadas = [r for r in p if r["nome"] != OUTROS]
    outros = sum(r["pct"] for r in p if r["nome"] == OUTROS)
    if n < MIN_OBS:
        return f"Poucos dados: menos de {MIN_OBS} ocorrências"
    if outros > OUTROS_MAX:
        return f"Outros acima de {round(100 * OUTROS_MAX)}%: abra em categorias"
    if len(nomeadas) >= 4 and sum(r["pct"] for r in nomeadas[:2]) < PLANO:
        return "Pareto plano: estratifique por outro fator"
    return "OK"


def linhas(ex):
    """Total de cada categoria da folha, na ordem em que foi escrita."""
    return [(nome, sum(v)) for nome, _, v in ex["folha"]]


def colunas(ex):
    """Total de cada coluna da folha (o segundo fator)."""
    return [(c, sum(v[j] for _, _, v in ex["folha"])) for j, c in enumerate(ex["cols"])]


# ------------------------------------------------------------ exemplo 1: pizzaria
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", data=D(2026, 7, 10), por="Líder da expedição",
                 conta="Entregas de delivery que chegaram depois de 40 minutos, pelo motivo principal do atraso.",
                 periodo="De 15/06 a 09/07/2026, todos os dias. Folha na bancada da expedição.",
                 como="Um traço por entrega atrasada, feito quando o entregador volta e informa o motivo.",
                 origem="Ciclo PDCA dos atrasos nas entregas: etapa de observação do problema.",
                 base=1110, base_nome="entregas", fator="Dia da semana"),
    "cols": ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
    "curto": ["Esperando entregador", "Fila no forno", "Endereço incompleto", "Trânsito ou obras", OUTROS],
    # categoria, definição (conta quando...), contagem por coluna
    "folha": [
        ("Pizza pronta esperando entregador", "A pizza ficou mais de 5 minutos na bancada, embalada, sem entregador para sair.", [3, 2, 4, 5, 36, 38, 4]),
        ("Fila no forno", "O pedido esperou mais de 10 minutos para entrar no forno.", [1, 1, 2, 3, 20, 24, 3]),
        ("Endereço incompleto", "O entregador precisou ligar ou procurar, por falta de complemento ou de referência.", [3, 4, 3, 4, 6, 6, 4]),
        ("Trânsito ou obras", "O entregador informou rua fechada, desvio ou trânsito parado no caminho.", [1, 1, 1, 2, 2, 2, 1]),
        (OUTROS, "O que não cabe nas categorias acima. Anotar o motivo ao lado do traço.", [2, 1, 2, 2, 3, 3, 1]),
    ],
    # a folha de uma noite: sábado, 20/06/2026, por faixa de horário (só no treinamento)
    "noite": dict(dia="Sábado, 20/06/2026", base=148, cols=["19h", "20h", "21h", "22h"],
                  linhas=[[2, 5, 4, 2], [1, 3, 3, 1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 0, 1, 0]]),
    # depois das ações do ciclo PDCA: escala reforçada, agrupamento por zona e complemento obrigatório
    "depois": dict(periodo="De 10/08 a 06/09/2026", base=1380, valores=[9, 38, 2, 6, 7]),
}

# ------------------------------------------------------------ exemplo 2: compras
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas · Suprimentos", data=D(2026, 6, 19), por="Analista de compras",
                 conta="Requisições de compra devolvidas ao requisitante, pelo motivo da devolução.",
                 periodo="De dezembro de 2025 a maio de 2026. Dados do sistema de compras, conferidos uma a uma.",
                 como="Uma linha por requisição devolvida, com o motivo lido no campo de observação do comprador.",
                 origem="Ciclo PDCA do prazo de compra: etapa de observação do problema.",
                 base=250, base_nome="requisições", fator="Área requisitante"),
    "cols": ["Manutenção", "Produção", "Laboratório", "Logística", "Administrativo"],
    "folha": [
        ("Especificação técnica em branco", "O campo de especificação veio vazio ou com “conforme amostra”.", [24, 7, 4, 2, 1]),
        ("Quantidade ou unidade em branco", "Faltou a quantidade, ou a unidade não permite comprar (peça, caixa, quilo).", [8, 6, 2, 2, 1]),
        ("Centro de custo em branco", "A requisição não informa quem paga.", [4, 3, 2, 2, 4]),
        ("Descrição não identifica o item", "O texto livre não permite saber qual item comprar.", [8, 3, 1, 1, 0]),
        ("Falta a aprovação do gestor", "A requisição chegou a Compras sem a aprovação exigida.", [2, 2, 1, 1, 2]),
        (OUTROS, "O que não cabe nas categorias acima.", [2, 2, 1, 1, 1]),
    ],
}

# ------------------------------------------------------------ exemplo 3: frequência e peso (só no treinamento)
EX3 = {
    "head": dict(org="Indústria de embalagens plásticas · Produção", data=D(2026, 10, 9), por="Analista da Qualidade",
                 conta="Bobinas reprovadas na inspeção final, pelo defeito principal, com o peso refugado.",
                 periodo="De julho a setembro de 2026. Registros de produto não conforme.",
                 origem="Reclamações do cliente A por espessura e a análise crítica de 2026."),
    # defeito, bobinas reprovadas, quilos refugados por bobina, em média
    "defeitos": [("Impressão fora de registro", 46, 10), ("Espessura fora da especificação", 31, 95), ("Solda fraca", 24, 15),
                 ("Furos e géis", 18, 30), ("Contaminação", 6, 60), (OUTROS, 9, 12)],
}

CHECK = [
    "O problema a contar está definido, com unidade: entrega atrasada, requisição devolvida, peça reprovada.",
    "Cada categoria tem definição escrita, e duas pessoas classificam o mesmo caso do mesmo jeito.",
    "A folha de verificação informa o que se conta, onde, em que período e quem registra.",
    "O registro é feito na hora, por quem vê a ocorrência, e não de memória no fim do dia.",
    "A folha guarda um segundo fator: dia, turno, área, máquina ou produto.",
    f"Há pelo menos {MIN_OBS} ocorrências no período, ou o período foi ampliado.",
    "As barras estão em ordem decrescente, com “Outros” por último.",
    f"“Outros” não passa de {round(100 * OUTROS_MAX)}% do total. Se passa, foi aberto em categorias.",
    "O gráfico mostra o total, o período e a base, e o eixo da esquerda vai até o total.",
    "O Pareto foi feito também por custo, tempo ou gravidade, quando as ocorrências não pesam igual.",
    "As primeiras barras seguiram para a análise de causa, e a decisão está registrada.",
    "Depois da ação, a contagem foi repetida com as mesmas categorias, e a comparação usa a taxa.",
]


def taxa(n, base):
    return 100 * n / base


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("compras", EX2)):
        print("==", nome, "| total", sum(v for _, v in linhas(ex)), "| colunas", colunas(ex))
        for r in pareto(linhas(ex)):
            print("  %d %-36s %4d %5.1f%% %5.1f%% %s" % (r["k"], r["nome"], r["v"], 100 * r["pct"], 100 * r["acc"], r["classe"]))
        print("  aviso:", aviso(linhas(ex)))
    assert sum(v for _, v in linhas(EX1)) == 200 and sum(v for _, v in linhas(EX2)) == 100
    assert [sum(l) for l in EX1["noite"]["linhas"]] == [13, 8, 2, 1, 1]
    d = EX1["depois"]
    print("depois:", sum(d["valores"]), "atrasos em", d["base"], "| %.1f por 100, contra %.1f" % (taxa(sum(d["valores"]), d["base"]), taxa(200, EX1["head"]["base"])))
    for titulo, rows in (("bobinas", [(n, q) for n, q, _ in EX3["defeitos"]]), ("quilos", [(n, q * kg) for n, q, kg in EX3["defeitos"]])):
        print("== indústria, por", titulo, "| total", sum(v for _, v in rows))
        for r in pareto(rows):
            print("  %d %-36s %5d %5.1f%% %5.1f%% %s" % (r["k"], r["nome"], r["v"], 100 * r["pct"], 100 * r["acc"], r["classe"]))
