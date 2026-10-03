# -*- coding: utf-8 -*-
"""Dados do Caso integrado, usados pelo HTML e pela planilha.

O caso junta o que os outros estudos da série contam sobre as duas organizações. Os passos do rastro repetem datas e
registros que já aparecem nos estudos de origem; as análises críticas de 14/06/2027 (pizzaria) e de 19/08/2027
(indústria) e os calendários anuais são novos, coerentes com eles. As frequências recomendadas, as situações e as regras
de conferência são uma convenção deste material.
"""
from datetime import date

D = date
# ---- os 29 estudos da série: nome curto, título, grupo, pasta e arquivo, frequência recomendada, ritmo
G1, G2, G3, G4 = "Conhecer a norma e montar o sistema", "Conhecer a organização e planejar", "Resolver problemas e melhorar", "Verificar e corrigir o sistema"
GRUPOS = [G1, G2, G3, G4]
MENSAL, TRIM, SEM, ANUAL, CONT, NEC = "Mensal", "Trimestral", "Semestral", "Anual", "Contínuo", "Quando necessário"
ESTUDOS = [
    ("ISO 9001", "ISO 9001 requisito a requisito", G1, "ISO-9001/treinamento-iso-9001.html", "Diagnóstico requisito a requisito, uma vez por ano.", ANUAL),
    ("Escopo e liderança", "Escopo e liderança", G1, "Escopo/treinamento-escopo.html", "Revisão do escopo e dos compromissos da direção.", ANUAL),
    ("Informação documentada", "Informação documentada", G1, "Informacao-Documentada/treinamento-informacao-documentada.html", "Revisão da lista mestra e da retenção.", ANUAL),
    ("Matriz de competências", "Matriz de competências e treinamento", G1, "Competencias/treinamento-competencias.html", "Matriz atualizada e plano de treinamento.", SEM),
    ("Calibração", "Calibração e recursos de medição", G1, "Calibracao/treinamento-calibracao.html", "Leitura dos vencimentos e ronda metrológica.", MENSAL),
    ("Recursos e infraestrutura", "Recursos, infraestrutura e ambiente", G1, "Recursos/treinamento-recursos.html", "Ronda dos recursos: escala, preventivas, ambiente.", MENSAL),
    ("Conhecimento e pós-entrega", "Conhecimento organizacional e pós-entrega", G1, "Conhecimento/treinamento-conhecimento.html", "Ronda do aprendizado: lições e atendimentos.", MENSAL),
    ("Partes interessadas", "Partes interessadas", G2, "Partes-Interessadas/treinamento-partes-interessadas.html", "Revisão das partes e dos requisitos.", ANUAL),
    ("Matriz SWOT", "Matriz SWOT", G2, "SWOT/treinamento-swot.html", "Diagnóstico estratégico, antes do planejamento do ano.", ANUAL),
    ("Objetivos da qualidade", "Objetivos da qualidade", G2, "Objetivos/treinamento-objetivos.html", "Acompanhamento dos objetivos e dos planos.", TRIM),
    ("Requisitos do cliente", "Requisitos do cliente e análise de pedidos", G2, "Pedidos/treinamento-pedidos.html", "A cada pedido, com leitura mensal dos registros.", CONT),
    ("Projeto e desenvolvimento", "Projeto e desenvolvimento", G2, "Projeto/treinamento-projeto.html", "A cada produto ou serviço novo.", NEC),
    ("Mapa de processos", "Mapa de processos e diagrama de tartaruga", G2, "Processos/treinamento-processos.html", "Revisão anual, ou quando um processo muda.", ANUAL),
    ("SIPOC", "SIPOC", G2, "SIPOC/treinamento-sipoc.html", "Revisão anual, ou quando o processo muda.", ANUAL),
    ("Matriz RACI", "Matriz RACI", G2, "RACI/treinamento-raci.html", "Revisão anual, ou quando a equipe muda.", ANUAL),
    ("Matriz de riscos", "Matriz de riscos", G2, "Riscos/treinamento-riscos.html", "Revisão dos riscos e das ações.", SEM),
    ("Controle de produção", "Controle de produção e de serviço", G2, "Producao/treinamento-producao.html", "Plano de controle todo dia, com leitura mensal.", CONT),
    ("Liberação e produto não conforme", "Liberação e produto não conforme", G2, "Liberacao/treinamento-liberacao.html", "A cada lote, com leitura mensal dos registros.", CONT),
    ("Matriz GUT", "Matriz GUT", G3, "GUT/treinamento-gut.html", "Escolha dos problemas do trimestre.", TRIM),
    ("Pareto", "Pareto e folha de verificação", G3, "Pareto/treinamento-pareto.html", "A cada problema escolhido.", NEC),
    ("Ishikawa", "Diagrama de Ishikawa", G3, "Ishikawa/treinamento-ishikawa.html", "A cada problema escolhido.", NEC),
    ("5W2H", "5W2H", G3, "5W2H/treinamento-5w2h.html", "A cada plano de ação.", NEC),
    ("PDCA", "PDCA", G3, "PDCA/treinamento-pdca.html", "A cada problema escolhido, do começo ao fim.", NEC),
    ("Indicadores", "Indicadores de desempenho", G4, "Indicadores/treinamento-indicadores.html", "Reunião mensal de indicadores.", MENSAL),
    ("Auditoria interna", "Auditoria interna", G4, "Auditoria/treinamento-auditoria.html", "Programa com auditorias a cada semestre.", SEM),
    ("Não conformidade", "Não conformidade e ação corretiva", G4, "Nao-Conformidade/treinamento-nao-conformidade.html", "A cada desvio, com leitura mensal dos registros.", CONT),
    ("Análise crítica", "Análise crítica pela direção", G4, "Analise-Critica/treinamento-analise-critica.html", "Reunião da direção a cada semestre.", SEM),
    ("Avaliação de fornecedores", "Avaliação de fornecedores", G4, "Fornecedores/treinamento-fornecedores.html", "Avaliação dos fornecedores críticos.", SEM),
    ("Satisfação do cliente", "Satisfação do cliente", G4, "Satisfacao/treinamento-satisfacao.html", "Reclamações todo dia, pesquisa a cada trimestre.", TRIM),
]
NOMES = [e[0] for e in ESTUDOS]
GRUPO = {e[0]: e[2] for e in ESTUDOS}
LINK = {e[0]: "../" + e[3] for e in ESTUDOS}
assert len(ESTUDOS) == 29 and len(set(NOMES)) == 29

# ---- calendário
FREQS = {"Mensal": 1, "Bimestral": 2, "Trimestral": 3, "Semestral": 6, "Anual": 12}
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
EMDIA, ATRASO, NAOCOMECOU = "Em dia", "Com atraso", "Ainda não começou"
CAL_SITS = [EMDIA, ATRASO, NAOCOMECOU]

ETAPAS = [
    ("Escolher um fio", "Um problema real e importante: uma reclamação grave, um indicador fora, uma quebra."),
    ("Seguir os registros", "De registro em registro, com a data e o estudo de cada passo."),
    ("Ligar saída e entrada", "O que cada passo entregou, e quem recebeu. Onde o fio se partiu?"),
    ("Montar o calendário", "As atividades que mantêm o sistema rodando, com frequência, mês e dono."),
    ("Ler e ajustar", "Todo mês: o que está atrasado no calendário, e onde os fios estão demorando."),
]
CADEIA = [
    ("Satisfação do cliente", "Reclamação registrada"),
    ("Não conformidade", "Causa e ação corretiva"),
    ("Indicadores", "Efeito medido no mês"),
    ("Auditoria interna", "Ação conferida no processo"),
    ("Análise crítica", "Decisão da direção"),
    ("Conhecimento e pós-entrega", "Lição incorporada"),
]


# ------------------------------------------------------------ rastro
def rastro_dias(passos):
    """Dias desde o passo imediatamente anterior, quando os dois têm data."""
    return [None if k == 0 or not p["data"] or not passos[k - 1]["data"] else (p["data"] - passos[k - 1]["data"]).days for k, p in enumerate(passos)]


def rastro_conf(passos):
    """Conferência de cada passo: a mesma regra da planilha."""
    dias = rastro_dias(passos)
    out = []
    for k, p in enumerate(passos):
        ultimo = k == len(passos) - 1
        if not p["data"]:
            out.append("Falta a data")
        elif not p["estudo"]:
            out.append("Falta o estudo")
        elif not p["oque"]:
            out.append("Falta o que aconteceu")
        elif not p["reg"]:
            out.append("Falta o registro")
        elif dias[k] is not None and dias[k] < 0:
            out.append("Data antes do passo anterior")
        elif not ultimo and not p["saida"]:
            out.append("Falta a saída")
        elif not ultimo and not p["prox"]:
            out.append("Falta o próximo estudo")
        elif not ultimo and p["prox"] != passos[k + 1]["estudo"]:
            out.append("O passo seguinte é de outro estudo")
        else:
            out.append("OK")
    return out


# ------------------------------------------------------------ calendário
def previstos(a):
    if a["freq"] not in FREQS or not a["inicio"]:
        return set()
    return set(range(a["inicio"], 13, FREQS[a["freq"]]))


def cal_conta(a, ref):
    prev = {m for m in previstos(a) if m <= ref}
    feitos = prev & a["feito"]
    return dict(prev=len(prev), feitos=len(feitos), atras=len(prev) - len(feitos), fora=len(a["feito"] - previstos(a)))


def cal_sit(a, ref):
    c = cal_conta(a, ref)
    if not previstos(a):
        return ""
    if c["prev"] == 0:
        return NAOCOMECOU
    return ATRASO if c["atras"] else EMDIA


def cal_conf(a):
    if not a["estudo"]:
        return "Falta o estudo"
    if not a["resp"]:
        return "Falta o responsável"
    if not a["freq"]:
        return "Falta a frequência"
    if not a["inicio"]:
        return "Falta o mês de início"
    if not 1 <= a["inicio"] <= 12:
        return "Mês de início fora de 1 a 12"
    return "OK"


def mes_estado(a, m, ref):
    """Para a figura e para a formatação da planilha: feito, atrasado, previsto, extra ou vazio."""
    p = m in previstos(a)
    if p and m in a["feito"]:
        return "feito"
    if p and m <= ref:
        return "atrasado"
    if p:
        return "previsto"
    return "extra" if m in a["feito"] else ""


def _passos(rows):
    out = [dict(zip(("data", "estudo", "oque", "reg", "saida", "prox"), r)) for r in rows]
    for p in out:
        assert p["estudo"] in NOMES and (not p["prox"] or p["prox"] in NOMES), p
    return out


def _cal(rows):
    out = [dict(zip(("ativ", "estudo", "req", "resp", "freq", "inicio", "feito"), r)) for r in rows]
    for a in out:
        assert a["estudo"] in NOMES and a["freq"] in FREQS, a["ativ"]
        a["feito"] = set(a["feito"])
    return out


# ------------------------------------------------------------ exemplo 1: pizzaria
_PDCA, _PAR, _ISH, _W5, _GUT, _IND, _AC, _OBJ, _REC, _CON = ("PDCA", "Pareto", "Ishikawa", "5W2H", "Matriz GUT", "Indicadores", "Análise crítica",
                                                             "Objetivos da qualidade", "Recursos e infraestrutura", "Conhecimento e pós-entrega")
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", fio="Os atrasos das noites de sexta e de sábado", ano=2027, ref=6,
                 resp="Gerente da loja", origem="18% das entregas chegavam depois de 40 minutos em junho de 2026."),
    "passos": _passos([
        (D(2026, 6, 15), _PDCA, "Ciclo aberto: 18% das entregas depois de 40 minutos. Meta de 95% em 12 semanas.", "Ciclo PDCA dos atrasos",
         "O problema medido, para estratificar", _PAR),
        (D(2026, 7, 10), _PAR, "Folha de verificação: em 46% dos atrasos, a pizza pronta esperou entregador, nas sextas e nos sábados.", "Folha de verificação de 15/06 a 09/07",
         "Os dois motivos principais", _ISH),
        (D(2026, 7, 17), _ISH, "Causas confirmadas: escala igual todos os dias, pedidos sem agrupamento por bairro, endereço sem complemento.", "Diagrama de 17/07/2026",
         "Três causas confirmadas", _W5),
        (D(2026, 7, 24), _W5, "Três ações: reforçar a escala no pico, agrupar os pedidos por bairro, tornar o complemento obrigatório.", "Plano de ação de 24/07/2026",
         "Ações com dono e prazo", _PDCA),
        (D(2026, 9, 6), _PDCA, "Média de 95,5% nas semanas 9 a 12. Meta atingida, e a escala do pico vira padrão.", "Ciclo PDCA, etapa de padronização",
         "O segundo motivo, a fila do forno, fica para depois", _GUT),
        (D(2026, 9, 29), _GUT, "O forno único no limite do pico entra na lista dos problemas do trimestre.", "Matriz GUT de 29/09/2026",
         "Os problemas do trimestre, para acompanhar", _IND),
        (D(2026, 10, 6), _IND, "Entregas em até 40 minutos: 95% em setembro, com o padrão mantido.", "Painel de indicadores, P1",
         "O indicador estável e o forno no limite", _AC),
        (D(2026, 12, 14), _AC, "Decisões: atendente de salão nas noites de pico, e um segundo pizzaiolo treinado no forno.", "Ata da análise crítica de 14/12/2026",
         "Objetivos e metas para 2027", _OBJ),
        (D(2027, 2, 19), _OBJ, "Objetivo O1: 96% das entregas em até 40 minutos. Ações: rever a escala com os condomínios novos e estudar o segundo forno.", "Objetivos de 2027, O1",
         "A escala revista em março", _REC),
        (D(2027, 4, 16), _REC, "Na sexta, pico de 29 entregas por hora para 8 entregadores: faltam 2, mesmo com os extras de março. Falta também um forneiro.", "Dimensionamento das pessoas no pico",
         "O forno e a escala como gargalos da sexta", _CON),
        (D(2027, 5, 31), _CON, "A regulagem do forno está só na cabeça do pizzaiolo líder, que sai em agosto. Transferência planejada até 30/06.", "Mapa do conhecimento, K-01",
         "O risco do forno, com prazo", _AC),
        (D(2027, 6, 14), _AC, "Entradas: o objetivo O1, a falta de gente no pico e a saída do pizzaiolo líder. Decisões: segundo forno e escala nova da sexta.", "Ata da análise crítica de 14/06/2027",
         "", ""),
    ]),
    "cal": _cal([
        ("Reunião de indicadores", _IND, "9.1.3", "Gerente da loja", "Mensal", 1, [1, 2, 3, 5, 6]),
        ("Verificação dos termômetros e da balança", "Calibração", "7.1.5", "Pizzaiolo líder", "Mensal", 1, [1, 2, 3, 4, 5, 6]),
        ("Revisão do forno e das motos", _REC, "7.1.3", "Gerente da loja", "Mensal", 1, [1, 2, 3, 4, 5, 6]),
        ("Revisão da câmara fria", _REC, "7.1.3", "Pizzaiolo líder", "Trimestral", 1, [1]),
        ("Ronda do aprendizado", _CON, "7.1.6 · 8.5.5", "Gerente da loja", "Mensal", 5, [5, 6]),
        ("Pesquisa de satisfação", "Satisfação do cliente", "9.1.2", "Atendente líder", "Trimestral", 2, [2, 5]),
        ("Acompanhamento dos objetivos", _OBJ, "6.2", "Gerente da loja", "Trimestral", 2, [2, 5]),
        ("Escolha dos problemas do trimestre", _GUT, "10.1", "Gerente da loja", "Trimestral", 1, [1, 4]),
        ("Avaliação dos fornecedores", "Avaliação de fornecedores", "8.4", "Gerente da loja", "Semestral", 2, [2]),
        ("Revisão da matriz de riscos", "Matriz de riscos", "6.1", "Gerente da loja", "Semestral", 4, [4]),
        ("Auditoria interna", "Auditoria interna", "9.2", "Atendente líder", "Semestral", 3, [3]),
        ("Matriz de competências e treinamento", "Matriz de competências", "7.2", "Gerente da loja", "Semestral", 1, [1]),
        ("Análise crítica pela direção", _AC, "9.3", "Dono da loja", "Semestral", 6, [6]),
        ("Revisão da lista mestra de documentos", "Informação documentada", "7.5", "Gerente da loja", "Anual", 3, []),
        ("SWOT e partes interessadas", "Matriz SWOT", "4.1 · 4.2", "Dono da loja", "Anual", 9, []),
    ]),
}

# ------------------------------------------------------------ exemplo 2: indústria
_SAT, _NC, _FORN, _PROD, _LIB, _CAL = ("Satisfação do cliente", "Não conformidade", "Avaliação de fornecedores", "Controle de produção", "Liberação e produto não conforme",
                                       "Calibração")
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", fio="O filme fino da extrusora 3", ano=2027, ref=9,
                 resp="Coordenador da Qualidade", origem="Sétima reclamação do cliente A em 2026, a quinta por espessura."),
    "passos": _passos([
        (D(2026, 9, 14), _SAT, "Cliente A reclama de espessura fora: a sétima reclamação do ano, a quinta pelo mesmo motivo.", "Registro de reclamação de 14/09/2026",
         "A reclamação, para análise de causa", _NC),
        (D(2026, 9, 23), _NC, "Causa: variação de espessura na extrusora 3, sem medidor em linha. Inspeção de 100% das bobinas do cliente A.", "RNC 2026-29",
         "A proposta do medidor de espessura em linha", _AC),
        (D(2027, 2, 18), _AC, "Aprova o medidor em linha e cobra a homologação do segundo fornecedor de resina, ação da matriz de riscos.", "Ata da análise crítica de 18/02/2027",
         "A homologação, com prazo", _FORN),
        (D(2027, 3, 29), _FORN, "Segundo fornecedor de resina homologado.", "Registro de homologação de 29/03/2027", "A resina nova liberada para uso", _PROD),
        (D(2027, 5, 14), _PROD, "Mudança registrada: resina do segundo fornecedor na extrusora 3, com lote piloto de duas bobinas, o lote 135.", "Registro de mudança de 14/05/2027",
         "O lote piloto, para liberar", _LIB),
        (D(2027, 5, 14), _LIB, "Bobina 1 com 37,4 µm, segregada. Bobina 2 com 39,1 µm, liberada e embarcada em 17/05.", "RNC 2027-19",
         "A bobina 2, no cliente A", _SAT),
        (D(2027, 5, 24), _SAT, "Cliente A reclama de filme fino no lote 135. Bobina recolhida e reposta em 26/05.", "RNC 2027-22",
         "A dúvida sobre a medição", _CAL),
        (D(2027, 6, 12), _CAL, "O micrômetro marca 1,6 µm a mais. Medições corrigidas desde 10/01: 6 bobinas abaixo de 38 µm, 2 entregues. Clientes informados em 14/06.",
         "Registro de verificação FV-12", "A lição sobre reclamação de espessura", _CON),
        (D(2027, 6, 20), _CON, "Lição incorporada: reclamação de espessura dispara a verificação do micrômetro do posto.", "Lição I-01, procedimento PQ-08",
         "A extrusora 3 sob atenção", _REC),
        (D(2027, 7, 31), _REC, "Três quebras da extrusora 3 em julho, 40 horas paradas, com a preventiva adiada desde junho.", "Registro de manutenções de julho",
         "A disponibilidade abaixo da meta", _AC),
        (D(2027, 8, 19), _AC, "Entradas: o lote 135, o micrômetro reprovado e as quebras de julho. Decisões: antecipar o medidor em linha e planejar a passagem do conhecimento do operador sênior.",
         "Ata da análise crítica de 19/08/2027", "A passagem do conhecimento, com prazo", _CON),
        (D(2027, 9, 30), _CON, "Mapa do conhecimento: a regulagem da extrusora 3 e a medição da rosca estão críticas, com transferência planejada.", "Mapa do conhecimento, C-01 e C-03",
         "", ""),
    ]),
    "cal": _cal([
        ("Reunião de indicadores", _IND, "9.1.3", "Coordenador da Qualidade", "Mensal", 1, [1, 2, 3, 4, 5, 6, 8, 9]),
        ("Programa de calibração", _CAL, "7.1.5", "Analista da Qualidade", "Mensal", 1, [1, 2, 3, 5, 6, 7, 8, 9]),
        ("Preventiva das extrusoras", _REC, "7.1.3", "Supervisor de manutenção", "Trimestral", 3, [3, 8, 9]),
        ("Ronda do aprendizado", _CON, "7.1.6 · 8.5.5", "Analista da Qualidade", "Mensal", 6, [6, 7, 9]),
        ("Mapa do conhecimento", _CON, "7.1.6", "Gerente de produção", "Anual", 9, [9]),
        ("Matriz de competências e treinamento", "Matriz de competências", "7.2", "Gerente de RH", "Trimestral", 1, [1, 4, 7]),
        ("Acompanhamento dos objetivos", _OBJ, "6.2", "Diretor geral", "Trimestral", 1, [1, 4, 7]),
        ("Avaliação dos fornecedores críticos", _FORN, "8.4", "Comprador sênior", "Semestral", 6, [6]),
        ("Revisão da matriz de riscos", "Matriz de riscos", "6.1", "Gerente de Suprimentos", "Semestral", 4, [4]),
        ("Auditoria interna", "Auditoria interna", "9.2", "Coordenador da Qualidade", "Semestral", 3, [3, 9]),
        ("Análise crítica pela direção", _AC, "9.3", "Diretor geral", "Semestral", 2, [2, 8]),
        ("Revisão dos documentos", "Informação documentada", "7.5", "Coordenador da Qualidade", "Semestral", 1, [1]),
        ("Pesquisa de satisfação", _SAT, "9.1.2", "Gerente comercial", "Anual", 11, []),
    ]),
}

PERGUNTAS = [
    ("De onde veio?", "Qual registro deu origem a este passo?", "A reclamação de 14/09, o RNC 2026-29."),
    ("O que foi feito?", "Qual foi a decisão ou a ação, e por quem?", "A inspeção de 100% das bobinas do cliente A."),
    ("O que saiu?", "Que registro este passo deixou?", "A ata da análise crítica, com a aprovação."),
    ("Para onde foi?", "Quem recebeu a saída, e o que fez com ela?", "Suprimentos, com a homologação do segundo fornecedor."),
    ("Quanto demorou?", "Quantos dias entre um passo e o seguinte?", "148 dias do RNC à decisão da direção."),
    ("O fio fechou?", "O problema parou de voltar, e o que se aprendeu ficou?", "A lição I-01 entrou no procedimento PQ-08."),
]

CHECK = [
    "Cada estudo usado na organização tem dono e frequência definidos.",
    "Existe um calendário anual com as atividades do sistema, os meses e os responsáveis.",
    "O calendário é lido todo mês, e as atividades atrasadas ganham data nova.",
    "As saídas de cada processo do sistema têm destino conhecido.",
    "É possível seguir um problema importante do primeiro registro à decisão final.",
    "Os registros citam uns aos outros: o RNC cita a reclamação, a ata cita o RNC.",
    "Os intervalos longos entre um passo e o seguinte são percebidos e discutidos.",
    "A análise crítica recebe o que os estudos produziram, e não só os indicadores.",
    "As decisões da análise crítica voltam aos objetivos, aos recursos e aos riscos.",
    "O que se aprende no fio vira lição incorporada.",
    "A implantação seguiu uma ordem: base, planejamento, operação, verificação.",
    "A equipe sabe explicar como o seu trabalho entra no sistema.",
]


def resumo(ex):
    h, ps, cal = ex["head"], ex["passos"], ex["cal"]
    contas = [cal_conta(a, h["ref"]) for a in cal]
    prev, feitos = sum(c["prev"] for c in contas), sum(c["feitos"] for c in contas)
    sits = [cal_sit(a, h["ref"]) for a in cal]
    datas = [p["data"] for p in ps if p["data"]]
    dias = [d for d in rastro_dias(ps) if d is not None]
    return dict(passos=len(ps), estudos=len({p["estudo"] for p in ps}), total=(max(datas) - min(datas)).days, maior=max(dias),
                ras_rever=sum(1 for c in rastro_conf(ps) if c != "OK"),
                ativ=len(cal), prev=prev, feitos=feitos, atras=prev - feitos, cumpr=feitos / prev if prev else None,
                fora=sum(c["fora"] for c in contas), sits={s: sits.count(s) for s in CAL_SITS}, cal_rever=sum(1 for a in cal if cal_conf(a) != "OK"))


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        print("==", nome, resumo(ex))
        for p, d, c in zip(ex["passos"], rastro_dias(ex["passos"]), rastro_conf(ex["passos"])):
            print("  %s %-34s %-5s %s" % (p["data"], p["estudo"], d, c))
        for a in ex["cal"]:
            print("  %-42s %-11s %s %s" % (a["ativ"], cal_sit(a, ex["head"]["ref"]), cal_conta(a, ex["head"]["ref"]), cal_conf(a)))
