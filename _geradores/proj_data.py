# -*- coding: utf-8 -*-
"""Dados do estudo de Projeto e desenvolvimento, usados pelo HTML e pela planilha.

Os tipos de entrada, os tipos de etapa, os resultados e as regras de conferência são uma convenção deste material.
Os exemplos continuam os dos outros estudos da série: a pizza vegana do cardápio de inverno da pizzaria, de abril a
maio de 2027, e o filme para vegetais congelados do cliente C (pedido PR-118), na indústria, de junho a agosto de 2027.
"""
from datetime import date

D = date
CLI, FUN, LEG, NOR, ANT, FAL, ORG = ("Cliente", "Funcional ou de desempenho", "Legal ou regulamentar", "Norma ou código", "Projeto anterior", "Falha potencial",
                                     "Da organização")
TIPOS_E = [CLI, FUN, LEG, NOR, ANT, FAL, ORG]
PLAN, DES, ANAL, VERIF, VALID, LIB = "Planejamento", "Desenvolvimento", "Análise crítica", "Verificação", "Validação", "Liberação para produção"
TIPOS_ET = [PLAN, DES, ANAL, VERIF, VALID, LIB]
APROV, RESS, REPROV = "Aprovado", "Aprovado com ressalvas", "Reprovado"
RESULT = [APROV, RESS, REPROV]
ATENDE, NAOAT = "Atende", "Não atende"
RES_E = [ATENDE, NAOAT]
PENDENTE = "Verificação pendente"
TIPOS_INFO = [
    (CLI, "O que o cliente pede e o que o uso dele exige.", "Bobinas de 600 mm, para a embaladora do cliente."),
    (FUN, "O que o produto precisa fazer, e com que desempenho.", "Resistir ao impacto a -18 °C."),
    (LEG, "O que a lei exige do produto.", "Declaração de conformidade para contato com alimentos."),
    (NOR, "Normas técnicas e códigos que a organização decidiu seguir.", "O método de ensaio de queda de dardo."),
    (ANT, "O que se aprendeu em projetos parecidos.", "O perfil de extrusão do filme de 40 µm."),
    (FAL, "O que pode dar errado no uso, e precisa ser evitado.", "Furo no pacote pelas pontas dos vegetais congelados."),
    (ORG, "O que a própria organização exige: custo, capacidade, insumos.", "Velocidade mínima de 40 m/min na extrusora."),
]
CONTROLES = [
    ("Análise crítica", "O projeto está no caminho certo?", "Ao fim de cada fase, antes de gastar mais.", "Quem decide, com as áreas afetadas.",
     "Seguir para o lote de teste, com a especificação revista."),
    ("Verificação", "As saídas atendem às entradas?", "Quando há uma saída para conferir: o desenho, a receita, o lote de teste.", "Quem conhece o critério: laboratório, engenharia.",
     "O filme tem 50 µm e resiste a 420 g no ensaio de queda de dardo."),
    ("Validação", "O produto serve para o uso pretendido?", "Antes da liberação, no uso real ou o mais perto dele.", "O cliente, ou o usuário, com a organização.",
     "Os pacotes de brócolis sobrevivem ao transporte e a três semanas no freezer."),
]
ETAPAS = [
    ("Planejar", "Etapas, responsáveis, prazos, análises críticas, verificações e validações."),
    ("Definir as entradas", "Cliente, desempenho, lei, normas, projetos anteriores, falhas e a organização."),
    ("Desenvolver as saídas", "Especificação, receita, critérios de aceitação: o que a produção vai usar."),
    ("Verificar e validar", "Saídas contra entradas, e produto contra o uso. Analisar criticamente cada resultado."),
    ("Liberar e controlar mudanças", "Liberar só com a validação aprovada. Toda mudança é analisada e verificada de novo."),
]


def etapa_conf(e, ref, etapas):
    """Conferência de uma etapa: a mesma regra da planilha."""
    if not e["resp"]:
        return "Falta o responsável"
    if not e["prazo"]:
        return "Falta o prazo"
    if e["concl"] and not e["result"]:
        return "Falta o resultado"
    if e["result"] in (RESS, REPROV) and not e["acoes"]:
        return "Falta a ação"
    if e["tipo"] == LIB and e["concl"] and not any(x["tipo"] == VALID and x["result"] in (APROV, RESS) for x in etapas):
        return "Liberado sem validação aprovada"
    if not e["concl"] and e["prazo"] < ref:
        return "Atrasada"
    return "OK"


def entrada_conf(x):
    if not x["tipo"]:
        return "Falta o tipo"
    if not x["fonte"]:
        return "Falta a fonte"
    if not x["saida"]:
        return "Falta a saída que atende"
    if not x["metodo"]:
        return "Falta como verificar"
    if x["result"] == NAOAT:
        return "Não atende, sem ação" if not x["evid"] else "Não atende: ação em curso"
    if not x["result"]:
        return PENDENTE
    return "OK"


def mud_conf(m):
    if not m["analise"]:
        return "Falta a análise"
    if not m["aut"]:
        return "Falta quem autorizou"
    if not m["verif"]:
        return "Falta o que foi verificado de novo"
    return "OK"


def _ents(rows):
    out = [dict(zip(("id", "req", "tipo", "fonte", "saida", "metodo", "result", "evid"), r)) for r in rows]
    for x in out:
        assert x["tipo"] in TIPOS_E and x["result"] in RES_E + [""], x["id"]
    return out


def _etps(rows):
    out = [dict(zip(("etapa", "tipo", "resp", "part", "prazo", "concl", "result", "acoes", "registro"), r), n=k + 1) for k, r in enumerate(rows)]
    for e in out:
        assert e["tipo"] in TIPOS_ET and e["result"] in RESULT + [""] and bool(e["concl"]) == bool(e["result"]), e["etapa"]
    return out


def _muds(rows):
    return [dict(zip(("data", "oque", "motivo", "analise", "verif", "aut"), r)) for r in rows]


# ------------------------------------------------------------ exemplo 1: pizzaria, a pizza vegana do cardápio de inverno
_PL, _GL = "Pizzaiolo líder", "Gerente da loja"
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", projeto="P-03 · Pizza vegana do cardápio de inverno", cliente="Clientes do salão e do aplicativo",
                 objetivo="Uma pizza sem ingrediente de origem animal, com o sabor e o tempo de forno das outras, no cardápio de 01/06/2027.",
                 resp="Pizzaiolo líder. Aprovação: gerente da loja e dono.", inicio=D(2027, 4, 5), fim=D(2027, 6, 1), ref=D(2027, 5, 31),
                 origem="Requisito 8.3 atendido em parte no diagnóstico de 2026: sabores novos eram testados com a equipe, sem registro da receita aprovada nem do teste."),
    "ents": _ents([
        ("E1", "Nenhum ingrediente de origem animal, inclusive na massa e no molho.", CLI, "Pedidos e comentários no aplicativo", "Ficha técnica P-03, com todos os ingredientes",
         "Conferência da ficha técnica e dos rótulos dos insumos", ATENDE, "Rótulos conferidos em 20/04."),
        ("E2", "Alergênicos informados no cardápio e no aplicativo.", LEG, "Requisito legal de rotulagem de alergênicos", "Texto do cardápio e do aplicativo",
         "Conferência do texto contra a ficha técnica", ATENDE, "Texto conferido em 03/05."),
        ("E3", "Aviso de que a cozinha é compartilhada com produtos de origem animal.", FAL, "Oferta: o que a loja não garante", "Texto do cardápio",
         "Conferência do texto", ATENDE, "Texto conferido em 03/05."),
        ("E4", "Tempo de forno de até 7 minutos, como o das outras pizzas.", FUN, "Capacidade do forno no pico", "Instrução de montagem e de forno",
         "Teste no forno, com 10 pizzas", ATENDE, "7 minutos a 300 °C, em 22/04."),
        ("E5", "Nota de pelo menos 4,0, de 1 a 5, na degustação da equipe.", FUN, "Padrão do cardápio", "Receita final", "Degustação com 8 pessoas da equipe", ATENDE,
         "Nota média de 4,4, em 22/04."),
        ("E6", "Custo de insumos de até 30% do preço de venda.", ORG, "Ficha técnica e custo por pizza (objetivo O6)", "Ficha técnica, com o custo", "Cálculo do custo",
         NAOAT, "Custo de 34%. Recheio trocado em 18/05; custo a recalcular."),
        ("E7", "Queijo vegetal que derreta sem queimar a 300 °C.", ANT, "Teste com outra marca, no projeto P-01 de 2026", "Marca do queijo vegetal na ficha técnica",
         "Teste no forno", ATENDE, "Marca A aprovada em 22/04."),
        ("E8", "Fornecedor do queijo vegetal homologado.", ORG, "Avaliação de fornecedores", "Fornecedor na lista de homologados", "Homologação", "", ""),
    ]),
    "etps": _etps([
        ("Plano e entradas aprovados", PLAN, _GL, "Pizzaiolo líder e dono", D(2027, 4, 5), D(2027, 4, 5), APROV, "", "Ata de 05/04"),
        ("Receita e ficha técnica, primeira versão", DES, _PL, "Segundo pizzaiolo", D(2027, 4, 23), D(2027, 4, 22), APROV, "", "Ficha técnica P-03 rev. 1"),
        ("Ficha técnica, custo e teste de forno contra as entradas", VERIF, _PL, "Gerente da loja", D(2027, 4, 30), D(2027, 5, 3), RESS, "Custo de 34% (E6): rever o recheio.",
         "Planilha de verificação P-03"),
        ("Análise crítica antes da degustação", ANAL, _GL, "Dono e pizzaiolo líder", D(2027, 5, 7), D(2027, 5, 7), RESS, "Seguir para a degustação. Resolver o custo até 25/05.",
         "Ata de 07/05"),
        ("Degustação com 20 clientes no salão", VALID, _GL, "20 clientes, por convite", D(2027, 5, 21), D(2027, 5, 20), APROV, "",
         "Fichas da degustação: nota média 4,3; 17 de 20 pediriam de novo"),
        ("Custo recalculado, com o recheio novo", VERIF, _PL, "Gerente da loja", D(2027, 5, 25), None, "", "", ""),
        ("Inclusão no cardápio de inverno, com treinamento da equipe", LIB, _GL, "Toda a equipe", D(2027, 6, 1), None, "", "", ""),
    ]),
    "muds": _muds([
        (D(2027, 5, 12), "Queijo vegetal da marca B no lugar da marca A.", "Falta no fornecedor.", "", "", _PL),
        (D(2027, 5, 18), "Recheio de tofu defumado no lugar da castanha de caju.", "Custo de 34% na verificação.", "Custo estimado em 29%, a confirmar.", "", _GL),
    ]),
}

# ------------------------------------------------------------ exemplo 2: indústria, filme para vegetais congelados
_GE, _LAB = "Gerente de engenharia", "Laboratório"
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", projeto="D-07 · Filme para vegetais congelados", cliente="Cliente C, alimentos congelados (proposta PR-118)",
                 objetivo="Filme liso de 50 µm que resista ao freezer e ao transporte congelado, para produção regular a partir de outubro de 2027.",
                 resp="Gerente de engenharia. Aprovação: diretor geral.", inicio=D(2027, 6, 7), fim=D(2027, 9, 24), ref=D(2027, 8, 30),
                 origem="Pedido PR-118, aceito com alteração em 07/06: lote de teste antes do pedido firme."),
    "ents": _ents([
        ("E1", "Espessura de 50 µm, com tolerância de ±2 µm.", CLI, "Proposta PR-118", "Especificação ES-D07", "Micrômetro, cinco pontos, lote de teste", ATENDE,
         "Média de 50,3 µm, em 16/07."),
        ("E2", "Largura de 600 mm e bobina de até 600 mm de diâmetro.", CLI, "Visita à embaladora do cliente", "Especificação ES-D07", "Medição no lote de teste", ATENDE,
         "600 mm e 580 mm de diâmetro."),
        ("E3", "Queda de dardo de pelo menos 300 g a -18 °C.", FUN, "Uso pretendido: freezer do cliente", "Resina para baixa temperatura e receita RX-D07",
         "Ensaio de queda de dardo a -18 °C", ATENDE, "420 g, em 16/07."),
        ("E4", "Declaração de conformidade para contato com alimentos.", LEG, "Legislação de embalagens para alimentos", "Declaração DC-D07, com as resinas e o aditivo",
         "Laudo de migração de laboratório externo", ATENDE, "Laudo de 12/07."),
        ("E5", "Método de ensaio de queda de dardo da norma técnica.", NOR, "Ficha técnica do cliente", "Instrução de ensaio IE-12", "Conferência da instrução com a norma",
         ATENDE, "Instrução revista em 02/07."),
        ("E6", "Perfil de extrusão do filme de 40 µm como ponto de partida.", ANT, "Receita RX-40 da extrusora 3", "Receita RX-D07", "Lote de teste de 500 kg", ATENDE,
         "Lote de teste de 15/07."),
        ("E7", "Selagem sem falhas na embaladora do cliente, a 120 °C.", CLI, "Visita à embaladora do cliente", "Faixa de selagem na especificação ES-D07",
         "Ensaio de selagem no laboratório", ATENDE, "Selagem conforme de 110 a 135 °C."),
        ("E8", "Velocidade de pelo menos 40 m/min na extrusora 3.", ORG, "Custo-alvo da proposta", "Receita RX-D07", "Lote de teste", NAOAT,
         "38 m/min. Ajustar o resfriamento no lote 2."),
        ("E9", "Resistência à perfuração pelas pontas dos vegetais congelados.", FAL, "Validação de 09/08: furos no transporte", "Camada interna de 20 µm (ES-D07 rev. 2)",
         "Ensaio de perfuração no lote 2", "", ""),
    ]),
    "etps": _etps([
        ("Plano do projeto e entradas, com o cliente", PLAN, _GE, "Comercial, Qualidade e cliente C", D(2027, 6, 11), D(2027, 6, 11), APROV, "", "Ata de 11/06"),
        ("Especificação ES-D07 e receita RX-D07", DES, _GE, "Produção", D(2027, 6, 25), D(2027, 6, 24), APROV, "", "ES-D07 rev. 1 e RX-D07 rev. 1"),
        ("Análise crítica antes do lote de teste", ANAL, _GE, "Qualidade, Produção e Comercial", D(2027, 6, 28), D(2027, 6, 28), APROV, "", "Ata de 28/06"),
        ("Lote de teste de 500 kg: ensaios contra as entradas", VERIF, _LAB, "Engenharia", D(2027, 7, 16), D(2027, 7, 16), RESS, "Velocidade de 38 m/min (E8): ajustar no lote 2.",
         "Relatório de ensaios RE-D07-1"),
        ("Embalagem, congelamento e transporte no cliente C, por três semanas", VALID, _GE, "Cliente C", D(2027, 8, 6), D(2027, 8, 9), REPROV,
         "Furos em 4% dos pacotes no transporte. Nova entrada E9: camada interna de 20 µm.", "Relatório do cliente C, de 09/08"),
        ("Análise crítica depois da validação", ANAL, _GE, "Diretor geral, Qualidade e Comercial", D(2027, 8, 13), D(2027, 8, 12), APROV, "", "Ata de 12/08"),
        ("Lote 2: ensaios, com perfuração e velocidade", VERIF, _LAB, "Engenharia", D(2027, 8, 27), None, "", "", ""),
        ("Segunda validação no cliente C", VALID, _GE, "Cliente C", D(2027, 9, 17), None, "", "", ""),
        ("Liberação para produção regular, com o plano de controle", LIB, _GE, "Produção e Qualidade", D(2027, 9, 24), None, "", "", ""),
    ]),
    "muds": _muds([
        (D(2027, 7, 20), "Resina para baixa temperatura do fornecedor B no lugar do fornecedor A.", "Prazo de entrega do fornecedor A.",
         "Fichas técnicas comparadas. Laudo de migração estendido à resina B.", "Queda de dardo repetida com a resina B: 410 g, conforme.", _GE),
        (D(2027, 8, 12), "Camada interna de 15 para 20 µm.", "Validação de 09/08: furos no transporte.", "Efeito na selagem, no custo e na espessura total avaliado.",
         "Planejado no lote 2: perfuração, selagem e espessura.", _GE),
        (D(2027, 8, 22), "Espessura total de 50 para 52 µm, para compensar a camada interna.", "Pedido da Produção.", "", "", "Líder do turno"),
    ]),
}

# exemplo 3: a validação que revelou uma entrada que faltava (só no treinamento)
HISTORIA = [
    ("15 e 16/07", "Lote de teste", "500 kg com a receita RX-D07. Todas as entradas verificadas atendem, menos a velocidade."),
    ("19/07 a 09/08", "Validação no cliente", "Os pacotes de brócolis são embalados, congelados e transportados por três semanas."),
    ("09/08", "Furos em 4% dos pacotes", "As pontas dos vegetais congelados perfuram o filme no transporte. Nenhuma entrada pedia isso."),
    ("12/08", "Nova entrada e mudança", "E9: resistência à perfuração. Camada interna de 15 para 20 µm, com análise e verificação planejada."),
    ("Até 17/09", "Lote 2 e nova validação", "A verificação inclui a entrada nova. A validação se repete no cliente."),
]

CHECK = [
    "Está decidido se a organização faz projeto e desenvolvimento, e a exclusão, se houver, está justificada.",
    "Cada projeto tem um plano: etapas, responsáveis, prazos, análises críticas, verificações e validações.",
    "O cliente e os usuários participam quando o projeto depende deles.",
    "As entradas estão escritas: cliente, desempenho, requisitos legais, normas, projetos anteriores, falhas potenciais e a organização.",
    "Cada entrada é clara, completa e não conflita com as outras.",
    "Cada entrada tem a saída que a atende e o modo de verificar.",
    "As saídas incluem os critérios de aceitação e o que é essencial para o uso seguro.",
    "A verificação confere as saídas contra as entradas, com registro.",
    "A validação confere o produto no uso pretendido, antes da liberação.",
    "As análises críticas registram os problemas encontrados e as ações.",
    "Toda mudança no projeto é analisada, autorizada e verificada de novo, com registro.",
    "O projeto só é liberado para a produção com a validação aprovada e as entradas verificadas.",
]


def por_tipo(ex):
    out = []
    for t in TIPOS_E:
        xs = [x for x in ex["ents"] if x["tipo"] == t]
        out.append(dict(tipo=t, n=len(xs), at=sum(1 for x in xs if x["result"] == ATENDE), nao=sum(1 for x in xs if x["result"] == NAOAT),
                        pend=sum(1 for x in xs if not x["result"])))
    return out


def resumo(ex):
    ref = ex["head"]["ref"]
    es, xs, ms = ex["etps"], ex["ents"], ex["muds"]
    return dict(etapas=len(es), concl=sum(1 for e in es if e["concl"]), atras=sum(1 for e in es if etapa_conf(e, ref, es) == "Atrasada"),
                et_rever=sum(1 for e in es if etapa_conf(e, ref, es) != "OK"), ents=len(xs), at=sum(1 for x in xs if x["result"] == ATENDE),
                nao=sum(1 for x in xs if x["result"] == NAOAT), pend=sum(1 for x in xs if not x["result"]), muds=len(ms), mud_rever=sum(1 for m in ms if mud_conf(m) != "OK"),
                valid_ok=sum(1 for e in es if e["tipo"] == VALID and e["result"] in (APROV, RESS)))


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        print("==", nome, resumo(ex))
        for e in ex["etps"]:
            print("  %d %-60s %-22s %-24s %s" % (e["n"], e["etapa"][:60], e["tipo"], e["result"] or "—", etapa_conf(e, ex["head"]["ref"], ex["etps"])))
        for x in ex["ents"]:
            print("  %s %-60s %s" % (x["id"], x["req"][:60], entrada_conf(x)))
        for m in ex["muds"]:
            print("  mudança %-50s %s" % (m["oque"][:50], mud_conf(m)))
