# -*- coding: utf-8 -*-
"""Dados do estudo ISO 9001:2026: o que muda, usados pelo HTML e pela planilha.

As mudanças vêm do anúncio da ISO de 16/09/2026 e do que os organismos de certificação publicaram sobre a edição nova
(DQS, NQA, SGS, BSI e outros); só entram as citadas por mais de uma fonte, resumidas com palavras próprias, sem
reproduzir o texto da norma. As datas de transição são as do documento Global ACI-TECH-3-TR. O tipo, o impacto, a
pontuação de prioridade e os prazos do plano de transição são uma convenção deste material. Os exemplos continuam os dos
outros estudos: a pizzaria, que se prepara para a certificação inicial pela edição de 2026, e a indústria, certificada
pela edição de 2015 em dezembro de 2027, que fará a transição na 1ª manutenção.
"""
from datetime import date, timedelta

D = date
PUBLICACAO, SO_2026, FIM_TRANSICAO = D(2026, 9, 16), D(2028, 3, 31), D(2029, 9, 30)
NOVO, REFORCADO, REESTR, INCORP, ESCLAR = "Novo", "Reforçado", "Reestruturado", "Incorporado", "Esclarecimento"
TIPOS = [NOVO, REFORCADO, REESTR, INCORP, ESCLAR]
ALTO, MEDIO, BAIXO = "Alto", "Médio", "Baixo"
IMPACTOS = {ALTO: 3, MEDIO: 2, BAIXO: 1}
ATENDE, PARCIAL, NAOATENDE, NA = "Atende", "Atende em parte", "Não atende", "Não se aplica"
SITUACOES = [ATENDE, PARCIAL, NAOATENDE, NA]
LACUNA = {ATENDE: 0, PARCIAL: 1, NAOATENDE: 2, NA: 0}
P_ALTA, P_MEDIA, P_BAIXA, P_SEM = "Alta", "Média", "Baixa", "Sem lacuna"
PRIORIDADES = [P_ALTA, P_MEDIA, P_BAIXA, P_SEM]
CONCL, NOPRAZO, ATRAS, SEMACAO = "Concluída", "No prazo", "Atrasada", "—"

# cada mudança: código, onde, título, tipo, impacto, o que mudou (resumo próprio), pergunta do diagnóstico, evidência típica, estudo da série
MUDANCAS = [
    ("M1", "4.1 e 4.2", "Mudança climática no contexto", INCORP, BAIXO,
     "A emenda de 2024, que pedia para avaliar se a mudança climática é uma questão pertinente e se as partes interessadas têm requisitos ligados a ela, passa para o texto da norma.",
     "A análise de contexto e a lista de partes interessadas dizem se o clima afeta a organização?", "SWOT e lista de partes interessadas com o clima avaliado.", "swot"),
    ("M2", "5.1.1", "Cultura da qualidade e comportamento ético", NOVO, ALTO,
     "A alta direção passa a ter de promover e demonstrar uma cultura da qualidade e o comportamento ético.",
     "Como a direção mostra, na prática, a cultura da qualidade e o comportamento ético que espera?", "Compromissos da direção, código de conduta, decisões registradas.", "esc"),
    ("M3", "5.2", "Política ligada à direção estratégica", REFORCADO, MEDIO,
     "A ligação da política e dos objetivos com o contexto e a direção estratégica da organização fica mais explícita.",
     "A política conversa com a estratégia e com o contexto, e os objetivos saem dela?", "Política revisada junto com a SWOT e os objetivos.", "obj"),
    ("M4", "6.1", "Riscos e oportunidades separados", REESTR, ALTO,
     "Os riscos e as oportunidades passam a ter requisitos próprios, cada um com determinação, ações e avaliação.",
     "Os riscos e as oportunidades estão em listas separadas, cada uma com análise, ação e eficácia?", "Matriz de riscos e lista de oportunidades, com ações próprias.", "riscos"),
    ("M5", "6.3", "Planejamento de mudanças", REFORCADO, MEDIO,
     "O planejamento das mudanças no sistema é reforçado: planejar, comunicar, acompanhar e analisar o efeito.",
     "A última mudança importante no sistema teve plano, comunicação e análise do resultado?", "Registro de mudanças do sistema, com o acompanhamento.", "caso"),
    ("M6", "7.3", "Conscientização sobre cultura e ética", NOVO, MEDIO,
     "As pessoas precisam estar conscientes da cultura da qualidade e do comportamento ético esperados, além da política e dos objetivos.",
     "As pessoas sabem dizer que comportamento a organização espera delas, e por quê?", "Entrevistas de conscientização, integração dos novos.", "comp"),
    ("M7", "3", "Termos essenciais dentro da norma", ESCLAR, BAIXO,
     "Um conjunto pequeno de termos essenciais, vindos da ISO 9000, passa a aparecer na própria norma, e a redação sobre informação documentada é ajustada.",
     "Os documentos internos usam os termos como a norma nova os define?", "Glossário interno e lista mestra revisados.", "doc"),
    ("M8", "Estrutura", "Estrutura harmonizada atualizada", ESCLAR, BAIXO,
     "A norma acompanha a versão atual da estrutura comum às normas de sistema de gestão, sem mudar a numeração principal.",
     "Os documentos que citam números de requisitos continuam certos?", "Matriz de requisitos e procedimentos conferidos.", "iso"),
    ("M9", "Anexo A", "Anexo A ampliado", ESCLAR, BAIXO,
     "O anexo informativo explica a intenção dos requisitos e as relações entre eles, sem criar obrigações.",
     "Quem interpreta a norma na organização leu o anexo novo?", "Registro de leitura, dúvidas resolvidas.", "iso"),
]
NAO_MUDOU = [
    ("Numeração e estrutura", "As seções de 4 a 10 e a maior parte dos requisitos seguem com os mesmos números."),
    ("Abordagem de processo e PDCA", "Continuam a base do sistema."),
    ("Requisitos de operação", "Pedidos, projeto, fornecedores, produção, liberação e produto não conforme seguem como em 2015."),
    ("Avaliação e melhoria", "Indicadores, satisfação, auditoria interna, análise crítica e ação corretiva não ganham requisitos novos."),
    ("Temas que ficaram de fora", "Inteligência artificial, digitalização e cibersegurança não viraram requisitos, e a sustentabilidade só entra pelo clima."),
]
# plano de transição: etapa, dias antes da auditoria (convenção)
PASSOS = [
    ("Comprar e ler a norma nova", 180),
    ("Diagnóstico das mudanças", 150),
    ("Plano de ação aprovado pela direção", 120),
    ("Ações concluídas", 60),
    ("Conscientização da equipe", 45),
    ("Auditoria interna pela edição de 2026", 30),
    ("Análise crítica com a transição", 15),
    ("Auditoria do organismo", 0),
]
AVISO = 30
P_REAL, P_FORA, P_PREV, P_VENCE, P_ATRAS = "Feito no prazo", "Feito fora do prazo", "Previsto", f"Vence em {AVISO} dias", "Atrasado"
PL_SITS = [P_REAL, P_FORA, P_PREV, P_VENCE, P_ATRAS]

ETAPAS = [
    ("Ler a edição nova", "Com o anexo A, comparando com o sistema atual."),
    ("Diagnosticar", "Para cada mudança: atende, atende em parte ou não atende."),
    ("Ajustar o sistema", "Ações com dono e prazo, aprovadas pela direção."),
    ("Auditar por dentro", "Auditoria interna e análise crítica já pela edição nova."),
    ("Auditar com o organismo", "Numa manutenção, numa recertificação ou numa auditoria separada."),
]
CULTURA = [
    ("Direção", "Promove e demonstra a cultura da qualidade e a ética, nas decisões do dia a dia.", "5.1.1"),
    ("Política e objetivos", "Ligados ao contexto e à direção estratégica, e conhecidos por todos.", "5.2"),
    ("Pessoas", "Sabem que comportamento se espera delas, e por quê.", "7.3"),
]


def prioridade_pts(m, sit):
    if sit not in LACUNA:
        return None
    return IMPACTOS[m[4]] * LACUNA[sit]


def prioridade(m, sit):
    p = prioridade_pts(m, sit)
    if p is None:
        return ""
    return P_ALTA if p >= 4 else P_MEDIA if p >= 2 else P_BAIXA if p >= 1 else P_SEM


def acao_sit(d, ref):
    if not d["acao"]:
        return SEMACAO
    if d["concl"]:
        return CONCL
    if d["prazo"] and ref > d["prazo"]:
        return ATRAS
    return NOPRAZO


def diag_conf(d):
    if d["sit"] not in LACUNA:
        return "Falta a situação"
    if d["sit"] in (PARCIAL, NAOATENDE) and not d["acao"]:
        return "Lacuna sem ação"
    if d["acao"] and not d["prazo"]:
        return "Falta o prazo"
    if d["acao"] and not d["resp"]:
        return "Falta o responsável"
    if d["sit"] == ATENDE and not d["evid"]:
        return "Falta a evidência"
    return "OK"


def limite_passo(audit, k):
    return audit - timedelta(days=PASSOS[k][1]) if audit else None


def passo_sit(pl, k):
    lim, feito, ref = limite_passo(pl["audit"], k), pl["feito"][k], pl["ref"]
    if lim is None:
        return ""
    if feito:
        return P_REAL if feito <= lim else P_FORA
    if ref > lim:
        return P_ATRAS
    return P_VENCE if (lim - ref).days <= AVISO else P_PREV


def _diag(rows):
    out = [dict(zip(("sit", "evid", "acao", "resp", "prazo", "concl"), r)) for r in rows]
    assert len(out) == len(MUDANCAS)
    for d in out:
        assert d["sit"] in SITUACOES
    return out


# ------------------------------------------------------------ exemplo 1: pizzaria, preparando a certificação inicial
_GL, _DL = "Gerente da loja", "Dono da loja"
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", situacao="Sem certificado. Certificação inicial marcada, já pela edição de 2026.",
                 auditoria="Fase 1 da certificação inicial", resp="Gerente da loja", ref=D(2028, 1, 5)),
    "diag": _diag([
        (PARCIAL, "Calor da cozinha medido todo dia; o clima não está na SWOT", "Incluir o calor na cozinha e as chuvas fortes na SWOT e nas partes interessadas.", _GL, D(2027, 12, 15), D(2027, 12, 12)),
        (NAOATENDE, "", "O dono escreve três comportamentos esperados e os cobra na reunião mensal.", _DL, D(2027, 12, 31), None),
        (ATENDE, "Política de 2027 ligada ao crescimento do delivery", "", "", None, None),
        (PARCIAL, "Matriz de riscos do delivery", "Separar as oportunidades da SWOT numa lista própria, com ação e prazo.", _GL, D(2027, 12, 20), D(2027, 12, 18)),
        (PARCIAL, "Troca do sistema de pedidos sem plano, em abril de 2027", "Criar uma rotina simples de planejar mudanças no sistema.", _GL, D(2028, 1, 15), None),
        (NAOATENDE, "", "Conversa com toda a equipe sobre a política e os comportamentos esperados.", _GL, D(2028, 1, 15), None),
        (ATENDE, "Termos lidos; a loja não tem glossário próprio", "", "", None, None),
        (ATENDE, "Matriz de requisitos conferida", "", "", None, None),
        (ATENDE, "Anexo A lido na preparação", "", "", None, None),
    ]),
    "plano": dict(audit=D(2028, 2, 15), ref=D(2028, 1, 5), fim=FIM_TRANSICAO,
                  feito=[D(2027, 10, 10), D(2027, 11, 30), D(2027, 12, 5), None, None, None, None, None]),
}

# ------------------------------------------------------------ exemplo 2: indústria, transição na 1ª manutenção
_CQ, _DG = "Coordenador da Qualidade", "Diretor geral"
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", situacao="Certificada pela edição de 2015 em 17/12/2027. Transição combinada para a 1ª manutenção.",
                 auditoria="1ª manutenção, com a transição", resp="Coordenador da Qualidade", ref=D(2028, 6, 30)),
    "diag": _diag([
        (ATENDE, "Calor no salão de impressão medido e avaliado como questão pertinente", "", "", None, None),
        (PARCIAL, "Compromissos da direção de 2027, sem cultura e ética", "Código de conduta e comportamentos esperados, apresentados pela direção.", _DG, D(2028, 8, 31), None),
        (ATENDE, "Política revisada com a SWOT e o objetivo O4", "", "", None, None),
        (ATENDE, "Riscos C1 a C8 e oportunidades O1 a O4 em listas separadas, desde 2026", "", "", None, None),
        (NAOATENDE, "", "Procedimento de mudanças do sistema, com plano, comunicação e análise do efeito.", _CQ, D(2028, 8, 31), None),
        (NAOATENDE, "", "Incluir cultura e ética nas entrevistas de conscientização e na integração.", "Gerente de RH", D(2028, 9, 30), None),
        (PARCIAL, "Glossário da lista mestra com os termos de 2015", "Atualizar o glossário com os termos da norma nova.", _CQ, D(2028, 5, 31), None),
        (ATENDE, "Matriz de requisitos e procedimentos conferidos", "", "", None, None),
        (ATENDE, "Anexo A lido pelos auditores internos", "", "", None, None),
    ]),
    "plano": dict(audit=D(2028, 11, 22), ref=D(2028, 6, 30), fim=FIM_TRANSICAO,
                  feito=[D(2027, 2, 10), D(2028, 3, 20), D(2028, 4, 10), None, None, None, None, None]),
}

# exemplo 3: a separação de riscos e oportunidades na indústria (só no treinamento)
RISCOS_IND = [("C1", "Um só fornecedor de resina"), ("C2", "Requisição sem especificação"), ("C3", "Fornecedor crítico sem avaliação"), ("C4", "Resina com preço em dólar"),
              ("C5", "Compra de fornecedor não homologado"), ("C6", "Compra acima da alçada"), ("C7", "Transportadora com frota reduzida"), ("C8", "Fornecedor sem licença ambiental")]
OPORT_IND = [("O1", "Embalagem com material reciclado"), ("O2", "Clientes exigindo a ISO 9001"), ("O3", "Resina reciclada de menor custo"), ("O4", "Feira do setor em outro estado")]

CHECK = [
    "A norma nova foi comprada e lida, com o anexo A, por quem cuida do sistema.",
    "Cada mudança foi avaliada: atende, atende em parte ou não atende, com evidência.",
    "As lacunas têm ação, responsável e prazo, aprovados pela direção.",
    "A direção sabe dizer como promove a cultura da qualidade e o comportamento ético.",
    "A política está ligada ao contexto e à direção estratégica.",
    "Riscos e oportunidades estão em listas separadas, cada uma com ação e avaliação.",
    "As mudanças no sistema têm plano, comunicação e análise do efeito.",
    "As pessoas sabem que comportamento se espera delas, e por quê.",
    "A análise de contexto diz se o clima afeta a organização.",
    "Os documentos usam os termos da edição nova.",
    "Houve auditoria interna e análise crítica pela edição nova antes da auditoria externa.",
    "A data da auditoria de transição foi combinada com o organismo, antes de 30/09/2029.",
]


def resumo(ex):
    ref = ex["head"]["ref"]
    sits = [d["sit"] for d in ex["diag"]]
    pri = [prioridade(m, d["sit"]) for m, d in zip(MUDANCAS, ex["diag"])]
    ac = [acao_sit(d, ref) for d in ex["diag"]]
    pl = ex["plano"]
    ps = [passo_sit(pl, k) for k in range(len(PASSOS))]
    return dict(sits={s: sits.count(s) for s in SITUACOES}, pri={p: pri.count(p) for p in PRIORIDADES}, acoes=sum(1 for a in ac if a != SEMACAO),
                concl=ac.count(CONCL), atras=ac.count(ATRAS), diag_rever=sum(1 for d in ex["diag"] if diag_conf(d) != "OK"),
                pts=sum(prioridade_pts(m, d["sit"]) for m, d in zip(MUDANCAS, ex["diag"])), passos={s: ps.count(s) for s in PL_SITS},
                depois=bool(pl["audit"] and pl["audit"] > pl["fim"]))


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        ref = ex["head"]["ref"]
        print("==", nome, resumo(ex))
        for m, d in zip(MUDANCAS, ex["diag"]):
            print("  %-3s %-16s %-6s pts %s %-10s %-9s %s" % (m[0], d["sit"], m[4], prioridade_pts(m, d["sit"]), prioridade(m, d["sit"]), acao_sit(d, ref), diag_conf(d)))
        for k, (p, _) in enumerate(PASSOS):
            print("  %-40s limite %s feito %s %s" % (p, limite_passo(ex["plano"]["audit"], k), ex["plano"]["feito"][k], passo_sit(ex["plano"], k)))
