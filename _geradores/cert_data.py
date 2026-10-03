# -*- coding: utf-8 -*-
"""Dados do estudo do Processo de certificação, usados pelo HTML e pela planilha.

A validade de três anos, a primeira manutenção em até 12 meses da decisão e a manutenção ao menos uma vez por ano vêm da
prática dos organismos acreditados (ISO/IEC 17021-1). Os prazos de 30 dias para o plano e de 90 dias para fechar a não
conformidade maior, os 6 meses entre as fases, os 3 meses de antecedência da recertificação, os 60 dias de aviso e os
critérios de prontidão são uma convenção deste material: cada organismo define os seus no regulamento. A ISO 9001:2026
foi publicada em 16/09/2026; o fim da transição (16/09/2029, três anos) é o anunciado pelos organismos e deve ser
confirmado no comunicado da acreditação. Os exemplos continuam os dos outros estudos: a indústria, com o objetivo O4 de se
certificar até dezembro de 2027, e a pizzaria, que avalia a prontidão no fim de 2027 e se certifica em 2028.
"""
import calendar
from datetime import date, timedelta

D = date
PUBLICACAO = D(2026, 9, 16)
FIM_TRANSICAO = D(2029, 9, 16)
E2015, E2026 = "ISO 9001:2015", "ISO 9001:2026"
EDICOES = [E2015, E2026]
SIM, PARCIAL, NAO = "Sim", "Parcial", "Não"
STATUS = [SIM, PARCIAL, NAO]
PTS = {SIM: 1.0, PARCIAL: 0.5, NAO: 0.0}
F1, F2 = "Fase 1", "Fase 2"
PRONTA2, PRONTA1, NAOPRONTA = "Pronta para a fase 2", "Pronta para a fase 1", "Ainda não está pronta"
CRITERIOS = [  # antes de, impeditivo, critério
    (F1, True, "O escopo está definido, com a justificativa do que não se aplica."),
    (F1, True, "A política e os objetivos da qualidade estão aprovados e comunicados."),
    (F1, True, "Os processos estão determinados, com a sequência e a interação entre eles."),
    (F1, True, "A informação documentada exigida existe e está sob controle."),
    (F1, False, "O organismo de certificação está escolhido, acreditado para o escopo."),
    (F2, True, "O sistema funciona há pelo menos três meses, com registros."),
    (F2, True, "Há um ciclo completo de auditoria interna, cobrindo todos os processos."),
    (F2, True, "Houve ao menos uma análise crítica pela direção, com todas as entradas."),
    (F2, True, "As não conformidades da auditoria interna têm ação definida."),
    (F2, False, "Os indicadores têm série de pelo menos três meses."),
    (F2, False, "As pessoas sabem explicar a política e o próprio papel no sistema."),
    (F2, False, "Os requisitos legais do produto estão identificados e atendidos."),
    (F2, False, "A calibração e a manutenção dos itens críticos estão em dia."),
    (F2, False, "As reclamações e a satisfação do cliente são registradas e analisadas."),
]
# ---- ciclo do certificado
VALIDADE_MESES, MANUT_MESES, FASES_MESES, RECERT_ANTES, AVISO = 36, 12, 6, 3, 60
EVENTOS = ["Fase 1", "Fase 2", "Decisão de certificação", "1ª manutenção", "2ª manutenção", "Auditoria de recertificação", "Transição para a edição de 2026"]
REALIZADA, NOPRAZO, FORAPRAZO, PREVISTA, VENCE, ATRASADA, NA = ("Realizada", "No prazo", "Fora do prazo", "Prevista", f"Vence em {AVISO} dias", "Atrasada",
                                                                "Não se aplica")
CIC_SITS = [REALIZADA, NOPRAZO, FORAPRAZO, PREVISTA, VENCE, ATRASADA, NA]
# ---- constatações
MAIOR, MENOR, OM, PONTO = "NC maior", "NC menor", "Oportunidade de melhoria", "Ponto de atenção da fase 1"
TIPOS = [MAIOR, MENOR, OM, PONTO]
AUDITORIAS = ["Fase 1", "Fase 2", "Manutenção", "Recertificação", "Transição"]
PLANO_DIAS, MAIOR_DIAS = 30, 90
FECHADA, PLANOATR, VENCIDA, AGUARDA, ABERTA, CONSIDERAR, TRATAR = ("Fechada", "Plano atrasado", "Vencida: risco ao certificado", "Aguarda verificação",
                                                                    "Aberta no prazo", "Para considerar", "Tratar antes da fase 2")
CT_SITS = [FECHADA, PLANOATR, VENCIDA, AGUARDA, ABERTA, CONSIDERAR, TRATAR]

ETAPAS = [
    ("Implantar e rodar", "O sistema funcionando por alguns meses, com auditoria interna e análise crítica."),
    ("Escolher o organismo", "Acreditado para o escopo, com proposta de dias de auditoria e regulamento."),
    ("Fase 1", "O organismo confere se o sistema está pronto: escopo, documentos, auditoria interna, análise crítica."),
    ("Fase 2", "Auditoria no local: o sistema está implementado e é eficaz?"),
    ("Decisão e manutenção", "Constatações tratadas, decisão do organismo, certificado e auditorias anuais."),
]
CADEIA = [
    ("Fórum internacional de acreditação", "Reúne os acreditadores e garante que um certificado valha em outros países."),
    ("Organismo de acreditação", "No Brasil, a Cgcre do Inmetro. Avalia os organismos de certificação."),
    ("Organismo de certificação", "Audita e certifica, seguindo a ISO/IEC 17021-1."),
    ("Organização certificada", "Mantém o sistema e recebe as auditorias de manutenção."),
    ("Cliente", "Confia no certificado sem precisar auditar o fornecedor."),
]
FASES = [
    ("Fase 1", ["Escopo, locais e processos", "Informação documentada", "Auditoria interna e análise crítica planejadas e feitas", "Requisitos legais conhecidos",
                "Prontidão para a fase 2"], "Saída: pontos de atenção e o plano da fase 2."),
    ("Fase 2", ["O sistema implementado, nos postos", "Desempenho contra os objetivos", "Controle operacional", "Auditoria interna e análise crítica funcionando",
                "Responsabilidade da direção"], "Saída: constatações e a recomendação de certificar ou não."),
]

CHECK = [
    "O escopo da certificação está definido e é o mesmo do sistema.",
    "O organismo escolhido é acreditado para o escopo, e o regulamento foi lido.",
    "O sistema funciona há meses, com indicadores, auditoria interna completa e análise crítica.",
    "As constatações da fase 1 foram tratadas antes da fase 2.",
    "Quem será entrevistado sabe explicar o próprio trabalho e a política.",
    "Os registros pedidos pela norma estão acessíveis no dia da auditoria.",
    "Os planos de ação são enviados dentro do prazo do organismo.",
    "As não conformidades maiores são fechadas, com evidência, antes da decisão.",
    "As datas das manutenções e da recertificação estão no calendário do sistema.",
    "O uso da marca de certificação segue as regras do organismo.",
    "Mudanças importantes, como escopo, endereço ou porte, são comunicadas ao organismo.",
    "A transição para a nova edição da norma está planejada antes do fim do prazo.",
]


def add_meses(d, m):
    """Soma meses a uma data, como a função EDATE das planilhas."""
    y, mo = divmod(d.month - 1 + m, 12)
    y, mo = d.year + y, mo + 1
    return date(y, mo, min(d.day, calendar.monthrange(y, mo)[1]))


# ------------------------------------------------------------ prontidão
def pront_res(itens):
    """Percentual, impeditivos pendentes antes da fase 1 e da fase 2, e o resultado."""
    resp = [i for i in itens if i["status"] in PTS]
    pct = sum(PTS[i["status"]] for i in resp) / len(itens) if itens else None
    imp1 = sum(1 for c, i in zip(CRITERIOS, itens) if c[1] and c[0] == F1 and i["status"] != SIM)
    imp2 = sum(1 for c, i in zip(CRITERIOS, itens) if c[1] and c[0] == F2 and i["status"] != SIM)
    res = NAOPRONTA if imp1 else PRONTA1 if imp2 else PRONTA2
    return dict(pct=pct, imp1=imp1, imp2=imp2, res=res, resp=len(resp))


def pront_conf(c, i):
    if i["status"] not in PTS:
        return "Falta o status"
    if i["status"] != SIM and not i["acao"]:
        return "Falta a ação"
    if i["status"] != SIM and not i["prazo"]:
        return "Falta o prazo"
    if i["status"] == SIM and not i["evid"]:
        return "Falta a evidência"
    return "OK"


# ------------------------------------------------------------ ciclo
def limites(c):
    """Limite de cada evento, na ordem de EVENTOS. None quando não há limite ou faltam datas."""
    dec, f1 = c["decisao"], c["feito"][0]
    lim = [None, add_meses(f1, FASES_MESES) if f1 else None, None]
    lim += [add_meses(dec, MANUT_MESES) if dec else None, add_meses(dec, 2 * MANUT_MESES) if dec else None,
            add_meses(dec, VALIDADE_MESES - RECERT_ANTES) if dec else None]
    lim.append(min(c["fimtrans"], validade(c)) if dec and c["edicao"] == E2015 else None)
    return lim


def validade(c):
    return add_meses(c["decisao"], VALIDADE_MESES) - timedelta(days=1) if c["decisao"] else None


def evento_sit(c, k):
    if k == 6 and c["edicao"] != E2015:
        return NA
    lim, feito, ref = limites(c)[k], c["feito"][k], c["ref"]
    if k in (0, 2):  # fase 1 e decisão: não têm limite neste material
        return REALIZADA if feito else PREVISTA
    if lim is None:
        return ""
    if feito:
        return NOPRAZO if feito <= lim else FORAPRAZO
    if ref > lim:
        return ATRASADA
    return VENCE if (lim - ref).days <= AVISO else PREVISTA


# ------------------------------------------------------------ constatações
def prazo_plano(x):
    return x["data"] + timedelta(days=PLANO_DIAS) if x["data"] and x["tipo"] in (MAIOR, MENOR) else None


def prazo_fech(x):
    return x["data"] + timedelta(days=MAIOR_DIAS) if x["data"] and x["tipo"] == MAIOR else None


def ct_sit(x, ref):
    if not x["tipo"] or not x["data"]:
        return ""
    if x["tipo"] in (OM, PONTO):
        if x["evid"]:
            return FECHADA
        return TRATAR if x["tipo"] == PONTO else CONSIDERAR
    if x["evid"]:
        return FECHADA
    if not x["plano"] and ref > prazo_plano(x):
        return PLANOATR
    if x["tipo"] == MAIOR and ref > prazo_fech(x):
        return VENCIDA
    if x["tipo"] == MENOR and x["plano"]:
        return AGUARDA
    return ABERTA


def ct_conf(x):
    if not x["data"]:
        return "Falta a data da auditoria"
    if not x["tipo"]:
        return "Falta o tipo"
    if not x["req"]:
        return "Falta o requisito"
    if not x["desc"]:
        return "Falta a descrição"
    if x["plano"] and x["plano"] < x["data"]:
        return "Plano antes da auditoria"
    if x["tipo"] == MAIOR and x["evid"] and not x["concl"]:
        return "Falta a conclusão da ação"
    return "OK"


def _itens(rows):
    out = [dict(zip(("status", "evid", "acao", "resp", "prazo"), r)) for r in rows]
    assert len(out) == len(CRITERIOS)
    return out


def _cts(rows):
    out = [dict(zip(("num", "aud", "data", "tipo", "req", "desc", "plano", "concl", "evid"), r)) for r in rows]
    for x in out:
        assert x["tipo"] in TIPOS and x["aud"] in AUDITORIAS, x["num"]
    return out


# ------------------------------------------------------------ exemplo 1: pizzaria
_GL = "Gerente da loja"
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", escopo="Produção e venda de pizzas no salão, para retirada e por entrega, na loja do bairro.",
                 organismo="Organismo acreditado pela Cgcre, escolhido em dezembro de 2027", motivo="Decisão da análise crítica de 14/06/2027: certificar para atender contratos de refeições de empresas."),
    "pront": dict(data=D(2027, 11, 30), itens=_itens([
        (SIM, "Escopo de fevereiro de 2027, revisado em novembro", "", "", None),
        (SIM, "Política no salão; objetivos de 2027 no quadro da cozinha", "", "", None),
        (SIM, "Mapa de processos e SIPOC dos quatro processos", "", "", None),
        (PARCIAL, "Lista mestra em dia", "Recolher a instrução do salão na revisão 1, ainda em uso no balcão.", _GL, D(2027, 12, 10)),
        (NAO, "", "Escolher entre as três propostas pedidas em outubro.", "Dono da loja", D(2027, 12, 15)),
        (SIM, "Registros desde janeiro de 2027", "", "", None),
        (PARCIAL, "Delivery, salão e recebimento auditados", "Auditar a produção e as compras em janeiro.", "Atendente do turno do almoço", D(2028, 1, 31)),
        (SIM, "Atas de 14/12/2026 e de 14/06/2027", "", "", None),
        (SIM, "Ações das auditorias de 2026 e de março de 2027", "", "", None),
        (SIM, "Painel com 12 meses de entregas no prazo e de reclamações", "", "", None),
        (PARCIAL, "Perguntas de conscientização feitas a 6 pessoas", "Repetir a conversa da política com a equipe nova do salão.", _GL, D(2028, 1, 15)),
        (SIM, "Licença sanitária renovada; rotulagem de alergênicos", "", "", None),
        (PARCIAL, "Balança e termômetros em dia", "Fazer a revisão da câmara fria, atrasada desde outubro.", "Pizzaiolo líder", D(2027, 12, 10)),
        (SIM, "Registro de reclamações e pesquisa trimestral", "", "", None),
    ])),
    "ciclo": dict(edicao=E2026, decisao=D(2028, 4, 25), ref=D(2028, 5, 31), fimtrans=FIM_TRANSICAO,
                  feito=[D(2028, 2, 15), D(2028, 3, 21), D(2028, 4, 25), None, None, None, None]),
    "cts": _cts([
        ("P-1", "Fase 1", D(2028, 2, 15), PONTO, "9.2", "A auditoria interna da produção ficou para depois da fase 1. Fazer antes da fase 2.",
         D(2028, 2, 20), D(2028, 3, 1), D(2028, 3, 2)),
        ("P-2", "Fase 2", D(2028, 3, 21), MENOR, "7.1.4", "O checklist de limpeza da bancada ficou abaixo do mínimo de 95% em fevereiro, e nenhuma ação foi registrada.",
         D(2028, 4, 10), None, None),
        ("P-3", "Fase 2", D(2028, 3, 21), MENOR, "8.2.1", "O cliente do salão não é avisado do tempo de espera nas noites de pico, como prevê a instrução.",
         D(2028, 4, 12), None, None),
        ("P-4", "Fase 2", D(2028, 3, 21), OM, "9.1.2", "As reclamações do salão poderiam entrar no mesmo registro do delivery.", None, None, None),
    ]),
}

# ------------------------------------------------------------ exemplo 2: indústria
_CQ = "Coordenador da Qualidade"
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", escopo="Desenvolvimento e produção de filmes técnicos lisos e impressos para embalagem de alimentos.",
                 organismo="Organismo acreditado pela Cgcre, contratado em 23/04/2027 por R$ 38.000", motivo="Objetivo O4: certificação até dezembro de 2027. Dois grandes clientes passam a exigir o certificado."),
    "pront": dict(data=D(2027, 9, 30), itens=_itens([
        (SIM, "Escopo revisado em maio de 2027", "", "", None),
        (SIM, "Política e objetivos de 2027, com o O4", "", "", None),
        (SIM, "Mapa dos nove processos, com tartarugas", "", "", None),
        (SIM, "Lista mestra e tabela de retenção de março de 2027", "", "", None),
        (SIM, "Contrato de 23/04/2027", "", "", None),
        (SIM, "Indicadores desde 2025", "", "", None),
        (PARCIAL, "Sete dos nove processos auditados", "Auditar a manutenção e a gestão de pessoas em outubro.", _CQ, D(2027, 10, 31)),
        (SIM, "Ata de 19/08/2027", "", "", None),
        (SIM, "Ações das auditorias de 2027 definidas", "", "", None),
        (SIM, "Painel de indicadores por processo", "", "", None),
        (SIM, "Entrevistas de conscientização em julho", "", "", None),
        (SIM, "Laudos de migração do filme para alimentos", "", "", None),
        (PARCIAL, "Instrumentos em dia", "Concluir a preventiva atrasada da extrusora 3.", "Supervisor de manutenção", D(2027, 10, 15)),
        (SIM, "Pesquisa anual e registro de reclamações", "", "", None),
    ])),
    "ciclo": dict(edicao=E2015, decisao=D(2027, 12, 17), ref=D(2028, 1, 15), fimtrans=FIM_TRANSICAO,
                  feito=[D(2027, 10, 20), D(2027, 11, 23), D(2027, 12, 17), None, None, None, None]),
    "cts": _cts([
        ("I-1", "Fase 1", D(2027, 10, 20), PONTO, "9.2", "O ciclo de auditoria interna não incluiu a manutenção e a gestão de pessoas.",
         D(2027, 10, 25), D(2027, 10, 31), D(2027, 11, 5)),
        ("I-2", "Fase 1", D(2027, 10, 20), PONTO, "9.3", "A análise crítica de 19/08 não tratou a satisfação do cliente como entrada.",
         D(2027, 10, 25), D(2027, 11, 12), D(2027, 11, 15)),
        ("I-3", "Fase 2", D(2027, 11, 23), MAIOR, "8.5.6", "Das 9 mudanças de processo de 2027, 4 sem autorização, 2 delas depois da constatação da auditoria interna de outubro: a ação corretiva não funcionou.",
         D(2027, 11, 30), D(2027, 12, 8), D(2027, 12, 10)),
        ("I-4", "Fase 2", D(2027, 11, 23), MENOR, "7.2", "O operador novo do turno C regula a extrusora 3 sem registro de treinamento.", D(2027, 12, 5), None, None),
        ("I-5", "Fase 2", D(2027, 11, 23), MENOR, "8.5.5", "A política do filme impresso aceita reclamação em 30 dias, e o contrato do cliente A exige 60.", None, None, None),
        ("I-6", "Fase 2", D(2027, 11, 23), OM, "7.1.3", "O destino do produto afetado por quebra poderia constar em todas as ordens de manutenção.", None, None, None),
    ]),
}

# exemplo 3: da não conformidade maior à decisão, na indústria (só no treinamento)
MAIOR_FIO = [
    ("23/11", "Fase 2", "NC maior no 8.5.6: 4 de 9 mudanças sem autorização. A ação da auditoria interna não funcionou."),
    ("30/11", "Plano enviado", "Causa: o formulário de mudança não chega ao turno C. Correção e ação com prazo."),
    ("08/12", "Ação concluída", "Mudança só no sistema, com aprovação do gerente; treinamento dos três turnos."),
    ("10/12", "Evidência aceita", "O organismo confere os registros de mudança de dezembro, todos autorizados."),
    ("17/12", "Decisão", "Certificado concedido, com as duas NC menores a verificar na 1ª manutenção."),
]
TRANSICAO = [
    (PUBLICACAO, "Publicação da ISO 9001:2026"),
    (D(2027, 12, 17), "Indústria certificada pela edição de 2015"),
    (D(2028, 4, 25), "Pizzaria certificada pela edição de 2026"),
    (D(2028, 12, 17), "1ª manutenção da indústria: boa data para a transição"),
    (FIM_TRANSICAO, "Fim da transição: certificados de 2015 deixam de valer"),
]


def resumo(ex):
    p = pront_res(ex["pront"]["itens"])
    c = ex["ciclo"]
    sits = [evento_sit(c, k) for k in range(len(EVENTOS))]
    cts = ex["cts"]
    csits = [ct_sit(x, c["ref"]) for x in cts]
    tipos = [x["tipo"] for x in cts]
    return dict(pct=p["pct"], imp1=p["imp1"], imp2=p["imp2"], res=p["res"], pront_rever=sum(1 for k, i in zip(CRITERIOS, ex["pront"]["itens"]) if pront_conf(k, i) != "OK"),
                validade=validade(c), sits={s: sits.count(s) for s in CIC_SITS},
                cts=len(cts), tipos={t: tipos.count(t) for t in TIPOS}, csits={s: csits.count(s) for s in CT_SITS},
                maiores_abertas=sum(1 for x, s in zip(cts, csits) if x["tipo"] == MAIOR and s != FECHADA), ct_rever=sum(1 for x in cts if ct_conf(x) != "OK"))


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        print("==", nome, resumo(ex))
        for k, i in zip(CRITERIOS, ex["pront"]["itens"]):
            print("  %-6s %-5s %-8s %s" % (k[0], k[1], i["status"], pront_conf(k, i)))
        c = ex["ciclo"]
        for k, (ev, lim) in enumerate(zip(EVENTOS, limites(c))):
            print("  %-32s limite %-11s feito %-11s %s" % (ev, lim, c["feito"][k], evento_sit(c, k)))
        for x in ex["cts"]:
            print("  %-4s %-28s plano até %-11s fechar até %-11s %-30s %s" % (x["num"], x["tipo"], prazo_plano(x), prazo_fech(x), ct_sit(x, c["ref"]), ct_conf(x)))
