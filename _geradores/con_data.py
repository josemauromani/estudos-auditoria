# -*- coding: utf-8 -*-
"""Dados do estudo de Conhecimento organizacional e pós-entrega, usados pelo HTML e pela planilha.

A pontuação de exposição do conhecimento, as situações, o prazo de 60 dias para uma lição pendente e as regras de
conferência são uma convenção deste material. Os exemplos continuam os dos outros estudos da série: a pizzaria em maio
de 2027, depois da quebra da câmara fria, e a indústria em setembro de 2027, depois das quebras da extrusora 3.
"""
from datetime import date

D = date
# ---- conhecimento
ALTA, MEDIA, BAIXA = "Alta", "Média", "Baixa"
CRITS = [ALTA, MEDIA, BAIXA]
CABECA, ESCRITO, TREINADO = "Só na cabeça", "Escrito", "Escrito e treinado"
FORMAS = [CABECA, ESCRITO, TREINADO]
PTS_FORMA = {CABECA: 2, ESCRITO: 1, TREINADO: 0}
SIM, NAO = "Sim", "Não"
CRITICO, RISCO, CONTROLE = "Crítico", "Em risco", "Sob controle"
CON_SITS = [CRITICO, RISCO, CONTROLE]
# ---- lições
ORIGENS = ["Reclamação", "Pós-entrega", "Quebra", "Não conformidade", "Auditoria", "Projeto"]
INCORP, PEND = "Incorporada", "Pendente"
PRAZO_LICAO = 60  # dias para uma lição pendente virar aviso
# ---- pós-entrega
TIPOS_AT = ["Reclamação", "Garantia", "Devolução", "Assistência técnica", "Orientação de uso"]
TIPOS_CAUSA = TIPOS_AT[:3]  # tipos que pedem a causa quando resolvidos
NOPRAZO, FORAPRAZO, ABERTO, ATRASADO = "No prazo", "Fora do prazo", "Aberto no prazo", "Aberto e atrasado"
AT_SITS = [NOPRAZO, FORAPRAZO, ABERTO, ATRASADO]

ETAPAS = [
    ("Mapear o conhecimento", "O que é preciso saber para cada processo dar certo, e quem sabe."),
    ("Proteger o que está exposto", "Escrever, treinar e acompanhar o que só uma pessoa sabe."),
    ("Definir o pós-entrega", "O que a organização faz depois da entrega, com prazo, pela lei e pelo cliente."),
    ("Atender e registrar", "Cada reclamação, garantia ou assistência, com prazo, causa e custo."),
    ("Transformar em lição", "O que se aprendeu vai para um documento ou um treinamento, e não fica na conversa."),
]
CICLO = [
    ("Processo", "Faz o produto com o que a organização sabe."),
    ("Entrega", "O produto chega ao cliente, e começa a vida útil."),
    ("Pós-entrega", "Garantia, assistência, orientação de uso. As reclamações chegam pelo mesmo caminho."),
    ("Lição aprendida", "O que o caso ensinou, escrito e com destino."),
    ("Conhecimento", "O documento, a instrução e o treinamento mudam."),
]
ESCADA = [
    (CABECA, "O conhecimento existe, mas só em quem faz. Some com a pessoa.", "A regulagem do forno, que só o pizzaiolo líder conhece."),
    (ESCRITO, "Está num documento que outra pessoa pode ler.", "A ficha de regulagem da extrusora 3."),
    (TREINADO, "Está escrito, e outras pessoas já fizeram sozinhas.", "As receitas, que os três pizzaiolos e o forneiro seguem."),
]
CONSIDERA = [
    ("Requisitos legais", "Prazos para reclamar, troca e recolhimento, pela lei."),
    ("Consequências indesejadas", "O que pode dar errado no uso, e como evitar ou reagir."),
    ("Natureza, uso e vida útil", "Quanto tempo o produto dura, e como o cliente o usa."),
    ("Requisitos do cliente", "O que o contrato ou o pedido exige depois da entrega."),
    ("Retorno do cliente", "O que as reclamações e as perguntas já mostraram."),
]
TRANSFERIR = [
    ("Escrever", "Instrução curta, com fotos, feita por quem sabe e testada por quem não sabe."),
    ("Acompanhar", "Quem não sabe faz junto com quem sabe, até fazer sozinho."),
    ("Gravar", "Vídeo curto do jeito certo, guardado onde o posto alcança."),
    ("Fazer rodízio", "Mais de uma pessoa passa pela tarefa, para o saber não morar num só."),
]


# ------------------------------------------------------------ conhecimento
def pts_pessoas(n):
    return 2 if n <= 1 else 1 if n == 2 else 0


def pontos(k):
    if not k["forma"] or k["pessoas"] is None:
        return None
    return PTS_FORMA[k["forma"]] + pts_pessoas(k["pessoas"]) + (1 if k["saida"] == SIM else 0)


def con_sit(k):
    p = pontos(k)
    if p is None or not k["crit"]:
        return ""
    if k["crit"] == ALTA and p >= 3:
        return CRITICO
    if k["crit"] in (ALTA, MEDIA) and p >= 2:
        return RISCO
    return CONTROLE


def con_conf(k, ref):
    """Conferência de um conhecimento: a mesma regra da planilha."""
    if not k["crit"]:
        return "Falta a criticidade"
    if not k["forma"]:
        return "Falta a forma"
    if k["pessoas"] is None:
        return "Falta quantas pessoas sabem"
    s = con_sit(k)
    if s in (CRITICO, RISCO):
        if not k["acao"]:
            return "Falta a ação de transferência"
        if not k["prazo"]:
            return "Falta o prazo da ação"
        if k["prazo"] < ref:
            return "Prazo da ação vencido"
    if k["forma"] != CABECA and not k["onde"]:
        return "Falta onde está escrito"
    return "OK"


# ------------------------------------------------------------ lições
def lic_sit(l):
    return INCORP if l["incorp"] else PEND


def lic_dias(l, ref):
    return (ref - l["data"]).days if not l["incorp"] and l["data"] else None


def lic_conf(l, cons, ref):
    if not l["data"]:
        return "Falta a data"
    if not l["oque"]:
        return "Falta o que aconteceu"
    if not l["aprend"]:
        return "Falta o que aprendemos"
    if not l["onde"]:
        return "Falta onde incorporar"
    if l["cod"] and l["cod"] not in {k["cod"] for k in cons}:
        return "Conhecimento não cadastrado"
    if lic_sit(l) == PEND and lic_dias(l, ref) > PRAZO_LICAO:
        return f"Pendente há mais de {PRAZO_LICAO} dias"
    return "OK"


# ------------------------------------------------------------ pós-entrega
def pol_conf(p):
    if p["minimo"] is None:
        return "Falta o prazo mínimo para reclamar"
    if p["aceito"] is None:
        return "Falta o prazo aceito"
    if p["aceito"] < p["minimo"]:
        return "Prazo aceito menor que o mínimo"
    if not p["ativ"]:
        return "Falta o que se faz"
    if p["resp"] is None:
        return "Falta o prazo de solução"
    return "OK"


def prazo_at(a, pols):
    p = {x["prod"]: x for x in pols}.get(a["prod"])
    return p["resp"] if p else None


def at_dias(a, ref):
    if not a["abert"]:
        return None
    return ((a["resol"] or ref) - a["abert"]).days


def at_sit(a, pols, ref):
    pz, d = prazo_at(a, pols), at_dias(a, ref)
    if pz is None or d is None:
        return ""
    if a["resol"]:
        return NOPRAZO if d <= pz else FORAPRAZO
    return ABERTO if d <= pz else ATRASADO


def at_conf(a, pols, lics):
    if a["prod"] not in {p["prod"] for p in pols}:
        return "Produto sem política"
    if not a["abert"]:
        return "Falta a data de abertura"
    if not a["tipo"]:
        return "Falta o tipo"
    if a["resol"] and a["tipo"] in TIPOS_CAUSA and not a["causa"]:
        return "Falta a causa"
    if a["licao"] and a["licao"] not in {l["num"] for l in lics}:
        return "Lição não encontrada"
    return "OK"


# ------------------------------------------------------------ montagem dos exemplos
def _cons(rows):
    out = [dict(zip(("cod", "nome", "proc", "crit", "forma", "onde", "pessoas", "saida", "acao", "prazo"), r)) for r in rows]
    for k in out:
        assert k["crit"] in CRITS and k["forma"] in FORMAS and k["saida"] in (SIM, NAO), k["cod"]
    return out


def _lics(rows):
    out = [dict(zip(("num", "data", "origem", "oque", "aprend", "onde", "resp", "cod", "incorp"), r)) for r in rows]
    for l in out:
        assert l["origem"] in ORIGENS, l["num"]
    return out


def _pols(rows):
    return [dict(zip(("prod", "vida", "minimo", "aceito", "ativ", "resp", "conseq"), r)) for r in rows]


def _ats(rows):
    out = [dict(zip(("num", "abert", "cliente", "prod", "tipo", "relato", "resol", "custo", "causa", "licao"), r)) for r in rows]
    for a in out:
        assert a["tipo"] in TIPOS_AT, a["num"]
    return out


# ------------------------------------------------------------ exemplo 1: pizzaria, maio de 2027
_PE, _SA, _MC = "Pizza entregue", "Pizza no salão", "Massa congelada para levar"
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", resp="Gerente da loja", ref=D(2027, 5, 31),
                 mudanca="O pizzaiolo líder, há seis anos na loja, muda de cidade em agosto de 2027.",
                 origem="Diagnóstico ISO de 2026: requisito 7.1.6 atendido em parte. As receitas estavam escritas, e a regulagem do forno só o pizzaiolo líder conhecia."),
    "cons": _cons([
        ("K-01", "Regulagem do forno e da chama do lastro", "Produção", ALTA, CABECA, "", 1, SIM,
         "O pizzaiolo líder escreve a regulagem, grava um vídeo e acompanha os dois pizzaiolos no forno.", D(2027, 6, 30)),
        ("K-02", "Ponto da massa pela temperatura da cozinha", "Produção", ALTA, ESCRITO, "Receita RC-01", 2, NAO, "", None),
        ("K-03", "Receitas das pizzas", "Produção", ALTA, TREINADO, "Receitas RC-01 a RC-24", 4, NAO, "", None),
        ("K-04", "Montagem e conferência do pedido", "Expedição", ALTA, TREINADO, "Instrução IT-EXP-01", 3, NAO, "", None),
        ("K-05", "Uso do sistema de pedidos, depois da atualização de versão", "Atendimento", MEDIA, CABECA, "", 2, NAO, "O gerente escreve o passo a passo do sábado, com as telas.", None),
        ("K-06", "Contingência da câmara fria", "Estoque", ALTA, ESCRITO, "Contingência CT-02, na porta da câmara", 2, NAO,
         "Treinar a equipe do domingo na contingência, com simulação.", D(2027, 6, 15)),
        ("K-07", "Rotas e atalhos do bairro", "Entrega", BAIXA, CABECA, "", 3, NAO, "", None),
    ]),
    "lics": _lics([
        ("L-01", D(2027, 3, 5), "Reclamação", "Pizza chegou fria.", "A bolsa térmica fica fechada até a entrega, e a pizza sai com 65 °C ou mais.",
         "Instrução IT-EXP-01", "Gerente da loja", "K-04", D(2027, 3, 15)),
        ("L-02", D(2027, 3, 22), "Reclamação", "Cliente pediu sem cebola e recebeu com cebola.", "A observação do pedido precisa sair em destaque na etiqueta.",
         "Etiqueta do sistema de pedidos", "", "K-05", None),
        ("L-03", D(2027, 4, 13), "Quebra", "Câmara fria parou, e a contingência foi improvisada.", "A contingência precisa estar escrita e na porta da câmara.",
         "Contingência CT-02", "Gerente da loja", "K-06", D(2027, 4, 20)),
        ("L-04", D(2027, 4, 19), "Quebra", "Corrente da moto partiu na entrega.", "A revisão mensal precisa conferir a corrente.",
         "Roteiro de revisão das motos", "Gerente da loja", "", D(2027, 4, 25)),
        ("L-05", D(2027, 4, 26), "Quebra", "Chama do forno apagando, e só o pizzaiolo líder sabia regular.", "A regulagem do forno precisa estar escrita.",
         "Instrução do forno IT-PRO-02", "Pizzaiolo líder", "K-01", None),
        ("L-06", D(2027, 5, 10), "Pós-entrega", "Clientes perguntam como reaquecer a pizza.", "", "Embalagem", "", "", None),
    ]),
    "pols": _pols([
        (_PE, "Consumo no dia; até 3 dias na geladeira", 30, 1, "Reposição ou desconto, e orientação de reaquecimento.", 1, "Cliente comer a pizza depois de 3 dias."),
        (_SA, "Consumo no local", 30, 30, "Troca na hora.", 0, ""),
        (_MC, "60 dias no freezer", 30, 30, "Troca ou devolução do valor, e orientação de armazenagem na embalagem.", 2, "Descongelar e congelar de novo."),
    ]),
    "ats": _ats([
        ("A-01", D(2027, 5, 3), "Cliente do bairro A", _PE, "Reclamação", "Pizza fria.", D(2027, 5, 3), 45, "Entregador com 4 pedidos na mesma rota.", "L-01"),
        ("A-02", D(2027, 5, 7), "Cliente do bairro B", _PE, "Reclamação", "Sabor trocado: pediu sem cebola.", D(2027, 5, 7), 60, "Observação do pedido sem destaque na etiqueta.", "L-02"),
        ("A-03", D(2027, 5, 14), "Cliente do bairro A", _PE, "Reclamação", "Borda queimada.", D(2027, 5, 16), 50, "Chama irregular no forno.", "L-05"),
        ("A-04", D(2027, 5, 15), "Cliente do balcão", _MC, "Orientação de uso", "Como descongelar a massa.", D(2027, 5, 15), 0, "", ""),
        ("A-05", D(2027, 5, 21), "Cliente do bairro C", _PE, "Reclamação", "Atraso de uma hora.", D(2027, 5, 22), 40, "", ""),
        ("A-06", D(2027, 5, 28), "Cliente do balcão", _MC, "Devolução", "Pacote rasgado, massa com gelo.", None, None, "", ""),
        ("A-07", D(2027, 5, 30), "Mesa 12", _SA, "Reclamação", "Refrigerante quente.", D(2027, 5, 30), 0, "Geladeira do salão desligada à tarde.", ""),
        ("A-08", D(2027, 5, 31), "Cliente do bairro B", _PE, "Reclamação", "Faltou o refrigerante do combo.", None, None, "", ""),
    ]),
}

# ------------------------------------------------------------ exemplo 2: indústria, setembro de 2027
_D7, _LI, _IM = "Filme para congelados D-07", "Filme liso padrão", "Filme impresso"
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", resp="Analista da Qualidade, com o gerente industrial", ref=D(2027, 9, 30),
                 mudanca="O operador sênior da extrusão se aposenta em dezembro de 2027. O filme D-07 entrou em produção em setembro.",
                 origem="Análise crítica de 19/08/2027: as quebras da extrusora 3 mostraram que o desgaste da rosca só era medido pelo técnico do fabricante."),
    "cons": _cons([
        ("C-01", "Regulagem da extrusora 3 para filme de 38 a 42 µm", "Extrusão", ALTA, ESCRITO, "Ficha de regulagem FR-03", 2, SIM,
         "O operador sênior acompanha os operadores do turno C por dois meses.", D(2027, 11, 30)),
        ("C-02", "Troca de clichês e acerto de cor", "Impressão", ALTA, CABECA, "", 1, NAO, "", None),
        ("C-03", "Medição da rosca e diagnóstico de desgaste", "Manutenção", ALTA, CABECA, "", 1, NAO,
         "O contrato com o fabricante inclui o treinamento do mecânico na medição.", D(2027, 10, 31)),
        ("C-04", "Ensaio de resistência da solda", "Laboratório", ALTA, TREINADO, "Procedimento PE-11", 2, NAO, "", None),
        ("C-05", "Formulação do filme D-07", "Projeto", ALTA, ESCRITO, "Dossiê do projeto D-07", 3, NAO, "", None),
        ("C-06", "Restauração do sistema de gestão", "TI", MEDIA, ESCRITO, "", 1, NAO, "O analista de TI treina o supervisor administrativo.", D(2027, 10, 15)),
        ("C-07", "Tratamento de reclamação técnica", "Qualidade", MEDIA, TREINADO, "Procedimento PQ-08", 3, NAO, "", None),
    ]),
    "lics": _lics([
        ("I-01", D(2027, 5, 24), "Reclamação", "Cliente A reclamou de filme fino no lote 135.", "Reclamação de espessura dispara a verificação do micrômetro do posto.",
         "Procedimento PQ-08", "Analista da Qualidade", "C-07", D(2027, 6, 20)),
        ("I-02", D(2027, 6, 12), "Não conformidade", "Micrômetro de 1 µm era grosso demais para a tolerância.", "Na compra de instrumentos, a resolução cabe 10 vezes na tolerância.",
         "Procedimento PR-SUP-01", "Comprador", "", None),
        ("I-03", D(2027, 7, 6), "Quebra", "Resistência da zona 3 queimou, com a preventiva adiada.", "Preventiva de item crítico só é adiada com análise da direção.",
         "Plano de manutenção PM-01", "Supervisor de manutenção", "", D(2027, 8, 10)),
        ("I-04", D(2027, 7, 18), "Quebra", "Rosca desgastada, medida só na preventiva.", "O desgaste da rosca é medido todo mês.",
         "Plano de manutenção PM-01", "Supervisor de manutenção", "C-03", D(2027, 8, 10)),
        ("I-05", D(2027, 7, 22), "Quebra", "Chiller parou, e o produto afetado não foi registrado.", "Toda quebra registra o produto afetado e o destino dele.",
         "Formulário de manutenção FM-02", "Supervisor de manutenção", "", None),
        ("I-06", D(2027, 8, 30), "Projeto", "Ensaio a -18 °C quase feito com a câmara vencida.", "Ensaio só começa com os instrumentos conferidos.",
         "Procedimento PE-14", "Laboratório", "C-04", D(2027, 9, 10)),
        ("I-07", D(2027, 9, 15), "Pós-entrega", "Bobina telescopada no transporte para o cliente B.", "Bobina acima de 600 mm viaja com cantoneira.", "", "", "", None),
    ]),
    "pols": _pols([
        (_D7, "12 meses em estoque, de 15 a 30 °C", 90, 90, "Laudo da reclamação técnica, visita técnica quando pedida, reposição do lote.", 5,
         "Embalagem rompendo no freezer do consumidor."),
        (_LI, "12 meses em estoque", 30, 30, "Laudo da reclamação técnica e reposição do lote.", 5, ""),
        (_IM, "12 meses em estoque", 60, 30, "Laudo da reclamação técnica, prova de cor e reposição do lote.", 5, "Cor diferente da marca do cliente na gôndola."),
    ]),
    "ats": _ats([
        ("N-01", D(2027, 8, 2), "Cliente A", _IM, "Reclamação", "Cor fora do padrão no lote 151.", D(2027, 8, 6), 3200, "Acerto de cor feito sem a prova aprovada pelo cliente.", ""),
        ("N-02", D(2027, 8, 10), "Cliente B", _LI, "Garantia", "Bobinas com furos.", D(2027, 8, 18), 5400, "Contaminação no material reciclado.", ""),
        ("N-03", D(2027, 8, 20), "Cliente C", _D7, "Assistência técnica", "Ajuste da seladora do cliente ao filme novo.", D(2027, 8, 22), 800, "", ""),
        ("N-04", D(2027, 9, 5), "Cliente A", _IM, "Devolução", "Rolo com emenda não sinalizada.", D(2027, 9, 12), 2100, "Emenda sem fita colorida no turno C.", ""),
        ("N-05", D(2027, 9, 15), "Cliente B", _LI, "Reclamação", "Bobina telescopada no transporte.", D(2027, 9, 19), 1500, "Bobina larga sem cantoneira.", "I-07"),
        ("N-06", D(2027, 9, 22), "Cliente D", _LI, "Orientação de uso", "Temperatura de selagem.", D(2027, 9, 22), 0, "", ""),
        ("N-07", D(2027, 9, 23), "Cliente A", _IM, "Reclamação", "Odor de solvente nas bobinas.", None, None, "", ""),
        ("N-08", D(2027, 9, 26), "Cliente C", _D7, "Reclamação", "Embalagem rasgando a -18 °C no teste do cliente.", None, None, "", ""),
    ]),
}

# exemplo 3: a mesma reclamação, duas vezes (só no treinamento)
REPETE = [
    ("22/03", "Reclamação", "Cliente pediu sem cebola e recebeu com cebola. Reposição na hora."),
    ("22/03", "Lição registrada", "A observação precisa sair em destaque na etiqueta. Ninguém ficou com a tarefa."),
    ("Abril", "Lição parada", "O sistema de pedidos recebe uma atualização de versão, e a etiqueta continua igual."),
    ("07/05", "A mesma reclamação", "Sabor trocado de novo. R$\u00a060 de reposição, e um cliente que talvez não volte."),
    ("31/05", "Na leitura", "A lição aparece com 70 dias pendente. Agora precisa de responsável e prazo."),
]

CHECK = [
    "O conhecimento necessário para cada processo está mapeado, com a criticidade.",
    "Para cada conhecimento, sabe-se quantas pessoas o dominam e onde está escrito.",
    "O conhecimento crítico que só uma pessoa sabe tem ação de transferência com prazo.",
    "Saídas previstas, como aposentadoria e mudança, entram no mapa com antecedência.",
    "As lições aprendidas são registradas, com o que aconteceu e o que se aprendeu.",
    "Cada lição tem destino: um documento, uma instrução ou um treinamento.",
    "Lições pendentes são lidas todo mês, e nenhuma fica parada sem responsável.",
    "O que a organização faz depois da entrega está definido para cada produto ou serviço.",
    "Os prazos aceitos para reclamar respeitam a lei e os contratos.",
    "As reclamações, garantias e assistências são registradas, com prazo de solução.",
    "Cada reclamação resolvida tem a causa registrada.",
    "O que o pós-entrega ensina volta como lição aprendida.",
]


def resumo(ex):
    ref, cons, lics, pols, ats = ex["head"]["ref"], ex["cons"], ex["lics"], ex["pols"], ex["ats"]
    sits = [con_sit(k) for k in cons]
    at_s = [at_sit(a, pols, ref) for a in ats]
    resolvidos = [s for s in at_s if s in (NOPRAZO, FORAPRAZO)]
    return dict(cons=len(cons), sits={s: sits.count(s) for s in CON_SITS}, semacao=sum(1 for k in cons if con_conf(k, ref) == "Falta a ação de transferência"),
                vencidas=sum(1 for k in cons if con_conf(k, ref) == "Prazo da ação vencido"), con_rever=sum(1 for k in cons if con_conf(k, ref) != "OK"),
                lics=len(lics), pend=sum(1 for l in lics if lic_sit(l) == PEND), velhas=sum(1 for l in lics if lic_conf(l, cons, ref).startswith("Pendente há")),
                lic_rever=sum(1 for l in lics if lic_conf(l, cons, ref) != "OK"),
                pols=len(pols), menor=sum(1 for p in pols if pol_conf(p) == "Prazo aceito menor que o mínimo"), pol_rever=sum(1 for p in pols if pol_conf(p) != "OK"),
                ats=len(ats), at_sits={s: at_s.count(s) for s in AT_SITS}, abertos=at_s.count(ABERTO) + at_s.count(ATRASADO),
                foraprazo=at_s.count(FORAPRAZO) + at_s.count(ATRASADO), noprazo=(resolvidos.count(NOPRAZO) / len(resolvidos)) if resolvidos else None,
                custo=sum(a["custo"] or 0 for a in ats), at_rever=sum(1 for a in ats if at_conf(a, pols, lics) != "OK"))


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        ref = ex["head"]["ref"]
        print("==", nome, resumo(ex))
        for k in ex["cons"]:
            print("  %-5s %-48s pts %-2s %-13s %s" % (k["cod"], k["nome"], pontos(k), con_sit(k), con_conf(k, ref)))
        for l in ex["lics"]:
            print("  %-5s %-11s dias %-4s %s" % (l["num"], lic_sit(l), lic_dias(l, ref), lic_conf(l, ex["cons"], ref)))
        for p in ex["pols"]:
            print("  %-30s %s" % (p["prod"], pol_conf(p)))
        for a in ex["ats"]:
            print("  %-5s prazo %-2s dias %-3s %-18s %s" % (a["num"], prazo_at(a, ex["pols"]), at_dias(a, ref), at_sit(a, ex["pols"], ref), at_conf(a, ex["pols"], ex["lics"])))
