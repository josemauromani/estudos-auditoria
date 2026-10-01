# -*- coding: utf-8 -*-
"""Dados do estudo de Escopo e liderança, usados pelo HTML e pela planilha.

Os requisitos que admitem não aplicabilidade, as situações dos compromissos e as regras de conferência são uma
convenção deste material. Os exemplos continuam os dos outros estudos da série: o primeiro escopo escrito da pizzaria,
em fevereiro de 2027, e a revisão do escopo da indústria antes da certificação, em maio de 2027.
"""
from datetime import date

from iso_data import REQ

D = date
SIM, NAO = "Sim", "Não"
DEM, PARC, NDEM = "Demonstrado", "Parcial", "Não demonstrado"
SITS = [DEM, PARC, NDEM]
# requisitos que, na prática, podem não se aplicar a uma organização; os outros se aplicam sempre
EXCLUIVEL = {"7.1.5": "Quando nenhum resultado depende de medição, ou a medição não exige rastreabilidade a padrões.",
             "8.3": "Quando a organização não define as características do que fornece: produz pelo projeto do cliente ou revende.",
             "8.5.3": "Quando nada do cliente ou do fornecedor fica sob os cuidados da organização: material, ferramenta, dado.",
             "8.5.5": "Quando não há nenhuma atividade depois da entrega: garantia, troca, assistência, reclamação."}
REQS = [(r["num"], r["titulo"]) for r in REQ]
CAMPOS = [("unidades", "Unidades e locais"), ("produtos", "Produtos e serviços"), ("processos", "Processos"), ("terceiros", "Processos terceirizados"),
          ("fora", "Fora do escopo"), ("declaracao", "Declaração de escopo"), ("rev", "Revisão e data"), ("aprov", "Aprovado por")]
OBRIG = ["unidades", "produtos", "processos", "declaracao", "aprov"]
COMPROMISSOS = [
    ("Responder pela eficácia", "Responder pela eficácia do sistema de gestão da qualidade."),
    ("Política e objetivos", "Garantir que a política e os objetivos sejam compatíveis com o contexto e com a estratégia."),
    ("Integração ao negócio", "Integrar os requisitos do sistema aos processos do negócio."),
    ("Processos e riscos", "Promover a abordagem de processo e a mentalidade de risco."),
    ("Recursos", "Garantir os recursos necessários ao sistema."),
    ("Comunicação", "Comunicar a importância de uma gestão da qualidade eficaz e de atender aos requisitos."),
    ("Resultados", "Garantir que o sistema alcance os resultados pretendidos."),
    ("Pessoas", "Engajar, dirigir e apoiar as pessoas para que contribuam com o sistema."),
    ("Melhoria", "Promover a melhoria."),
    ("Outros gestores", "Apoiar os outros gestores a demonstrar liderança nas suas áreas."),
]
NC = len(COMPROMISSOS)
ETAPAS = [
    ("Reunir o contexto", "As questões internas e externas, as partes interessadas e os produtos e serviços."),
    ("Desenhar a fronteira", "Unidades, produtos, processos e o que é terceirizado. O que fica de fora, e por quê."),
    ("Decidir a aplicabilidade", "Requisito por requisito. Não aplicável só com justificativa e sem afetar o cliente."),
    ("Escrever e aprovar", "A declaração de escopo, aprovada pela direção e disponível."),
    ("Demonstrar a liderança", "Os dez compromissos da direção, com evidência e registro."),
]
DECLARACOES = [
    ("Vaga", "Fabricação de embalagens.", "Não diz quais embalagens, em que unidade, nem se há projeto. Qualquer coisa cabe, e nada se confere."),
    ("Incompleta", "Fabricação de filmes plásticos na fábrica. Não se aplica o 8.3.", "Diz o local e exclui o projeto sem justificativa, embora a fábrica desenvolva filmes sob encomenda."),
    ("Clara", "Projeto, fabricação e expedição de filmes plásticos técnicos, lisos e impressos, para embalagem de alimentos, na fábrica da empresa e no armazém externo contratado.",
     "Diz o que, onde e como. Inclui o projeto e o processo terceirizado. Sem requisitos não aplicáveis."),
]


def aplic_conf(num, aplica, just, afeta):
    """Conferência de uma linha da aplicabilidade: a mesma regra da planilha."""
    if not aplica:
        return "Falta decidir"
    if aplica == SIM:
        return "OK"
    if num not in EXCLUIVEL:
        return "Requisito que se aplica sempre"
    if not just:
        return "Falta a justificativa"
    if not afeta:
        return "Falta avaliar o efeito"
    if afeta == SIM:
        return "Exclusão indevida"
    return "OK"


def lider_conf(c):
    if not c["faz"]:
        return "Falta a evidência"
    if not c["sit"]:
        return "Falta a situação"
    if c["sit"] in (PARC, NDEM) and not c["acao"]:
        return "Falta a ação"
    if c["acao"] and (not c["resp"] or not c["prazo"]):
        return "Falta o responsável ou o prazo"
    if c["sit"] == DEM and not c["reg"]:
        return "Falta o registro"
    return "OK"


def escopo_conf(e):
    return [f'Falta: {dict(CAMPOS)[k].lower()}' for k in OBRIG if not e[k]]


def _lid(rows):
    assert len(rows) == NC
    out = [dict(zip(("faz", "freq", "reg", "sit", "acao", "resp", "prazo"), r)) for r in rows]
    for c in out:
        assert c["sit"] in SITS, c["faz"]
    return out


def aplicabilidade(ex):
    """As 45 linhas, com a decisão: sim para tudo o que não está nas exclusões do exemplo."""
    out = []
    for num, tit in REQS:
        just, afeta = ex["excl"].get(num, ("", ""))
        aplica = NAO if num in ex["excl"] else SIM
        out.append(dict(num=num, tit=tit, aplica=aplica, just=just, afeta=afeta, conf=aplic_conf(num, aplica, just, afeta)))
    return out


# ------------------------------------------------------------ exemplo 1: pizzaria, o primeiro escopo escrito
_DO, _GL = "Dono", "Gerente da loja"
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", data=D(2027, 2, 8), por="Gerente da loja, com o dono", ref=D(2027, 2, 15),
                 origem="Requisito 4.3 não atendido no diagnóstico de 2026: não havia escopo escrito."),
    "escopo": dict(unidades="Uma loja, com salão, cozinha e expedição.", produtos="Pizzas e bebidas, servidas no salão, para retirada no balcão e entregues em casa. Encomendas para eventos.",
                   processos="Registrar o pedido, produzir e embalar, entregar; planejar e dirigir a loja, medir e melhorar; comprar e armazenar, manter equipamentos e motos, treinar a equipe.",
                   terceiros="Pagamento pelo aplicativo, controle de pragas e manutenção do forno, por empresas contratadas.", fora="Nenhuma parte da loja.",
                   declaracao="Produção e venda de pizzas e bebidas no salão, para retirada e por entrega, e encomendas para eventos, na loja do bairro.",
                   rev="Rascunho de 08/02/2027", aprov=""),
    "excl": {"8.3": ("A loja não projeta produtos: segue receitas.", SIM), "8.5.3": ("A loja não recebe bens do cliente.", SIM)},
    "lid": _lid([
        ("O dono conduz a análise crítica de dezembro e assina as decisões.", "Anual", "Ata da análise crítica de 14/12/2026", DEM, "", "", None),
        ("Os objetivos de 2027 saíram da análise crítica e da SWOT, com o dono.", "Anual", "Quadro de objetivos de 2027", DEM, "", "", None),
        ("Os indicadores são lidos na reunião semanal, junto com as vendas.", "Semanal", "Painel de indicadores", DEM, "", "", None),
        ("O mapa de processos está na parede da cozinha. Os riscos são revistos uma vez por ano.", "Anual", "Matriz de riscos", PARC,
         "Ler os riscos de cada processo na reunião mensal com os líderes.", _GL, D(2027, 4, 30)),
        ("Aprovou o segundo pizzaiolo e o treinamento. O segundo forno está em estudo.", "Quando necessário", "Ata da análise crítica de 14/12/2026", DEM, "", "", None),
        ("Fala da qualidade na abertura do turno de sexta-feira.", "Semanal", "", PARC, "Incluir os entregadores e mandar uma mensagem por semana no grupo da equipe.", _DO,
         D(2027, 3, 31)),
        ("Acompanha o quadro de objetivos todo mês.", "Mensal", "Quadro de objetivos", DEM, "", "", None),
        ("Escolhe o funcionário do mês, com os líderes.", "Mensal", "", DEM, "", "", None),
        ("Pede um ciclo PDCA por semestre e acompanha o resultado.", "Semestral", "PDCA dos atrasos na entrega", DEM, "", "", None),
        ("As decisões dos processos passam todas pelo gerente.", "", "", NDEM, "", "", None),
    ]),
}

# ------------------------------------------------------------ exemplo 2: indústria, a revisão antes da certificação
_DG = "Diretor geral"
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", data=D(2027, 5, 10), por="Coordenador da Qualidade, com o diretor geral e os gerentes", ref=D(2027, 5, 17),
                 origem="Objetivo O4: certificação ISO 9001 até dezembro. A revisão do escopo é a primeira etapa."),
    "escopo": dict(unidades="Fábrica: extrusão, impressão, corte e expedição. Armazém externo, operado por empresa de logística contratada.",
                   produtos="Filmes técnicos lisos e impressos para embalagem de alimentos, e o desenvolvimento de filmes sob encomenda.",
                   processos="Vender e programar, desenvolver, extrusar, imprimir, cortar, inspecionar e expedir; gestão do sistema; suprimentos, manutenção, laboratório e pessoas.",
                   terceiros="Armazenagem e transporte, ensaios de migração em laboratório externo e calibração dos instrumentos.",
                   fora="Nenhuma unidade. O armazém externo entra como processo terceirizado.",
                   declaracao="Projeto, fabricação e expedição de filmes plásticos técnicos, lisos e impressos, para embalagem de alimentos.",
                   rev="Revisão 1, de 10/05/2027", aprov=_DG),
    "excl": {"8.5.3": ("A fábrica não recebe material do cliente.", NAO)},
    "lid": _lid([
        ("O diretor geral conduz a análise crítica a cada semestre.", "Semestral", "Ata da análise crítica de 18/02/2027", DEM, "", "", None),
        ("Os objetivos de 2027 estão ligados à SWOT e à certificação.", "Anual", "Quadro de objetivos de 2027", DEM, "", "", None),
        ("Os indicadores da qualidade são lidos na reunião mensal de resultados, junto com os financeiros.", "Mensal", "Ata da reunião de resultados", DEM, "", "", None),
        ("Cada gerente é dono de processo, com tartaruga e matriz de riscos.", "Semestral", "Mapa de processos e matrizes de riscos", DEM, "", "", None),
        ("Aprovou o medidor de espessura de R$ 96.000, e a instalação atrasou.", "Quando necessário", "Ata da análise crítica de 18/02/2027", PARC,
         "Acompanhar a instalação na reunião mensal de resultados.", _DG, D(2027, 9, 30)),
        ("Comunicado trimestral do diretor sobre qualidade e clientes, no mural e na intranet.", "Trimestral", "Comunicados publicados", DEM, "", "", None),
        ("Os objetivos são revistos a cada trimestre, com os gerentes.", "Trimestral", "Quadro de objetivos", DEM, "", "", None),
        ("Programa de sugestões e operadores nas equipes de melhoria.", "Mensal", "Registro de sugestões", PARC,
         "Uma reunião por mês do gerente industrial com o turno da noite, que não participa.", "Gerente industrial", D(2027, 7, 31)),
        ("Mantém a equipe de melhoria do refugo, com horas e verba.", "Mensal", "Ciclo PDCA do refugo", DEM, "", "", None),
        ("Os gerentes conduzem a análise crítica do seu processo antes da geral.", "Semestral", "", DEM, "", "", None),
    ]),
}

CHECK = [
    "O contexto e as partes interessadas foram considerados para definir o escopo.",
    "A declaração de escopo diz que produtos e serviços estão cobertos.",
    "As unidades, os locais e as atividades dentro do escopo estão claros.",
    "Os processos terceirizados aparecem no escopo e são controlados.",
    "Cada requisito considerado não aplicável tem justificativa.",
    "Nenhuma não aplicabilidade afeta a conformidade do produto ou a satisfação do cliente.",
    "O escopo está escrito, aprovado e disponível como informação documentada.",
    "A direção responde pela eficácia do sistema e conduz a análise crítica.",
    "A política e os objetivos são compatíveis com a estratégia e com o contexto.",
    "Os requisitos do sistema estão integrados aos processos do negócio, e não em paralelo.",
    "A direção garante os recursos e comunica a importância da qualidade.",
    "A direção engaja as pessoas, promove a melhoria e apoia os outros gestores.",
]


def resumo(ex):
    ap = aplicabilidade(ex)
    lid = ex["lid"]
    return dict(reqs=len(ap), aplic=sum(1 for a in ap if a["aplica"] == SIM), naoap=sum(1 for a in ap if a["aplica"] == NAO), ap_rever=sum(1 for a in ap if a["conf"] != "OK"),
                esc_falta=len(escopo_conf(ex["escopo"])), dem=sum(1 for c in lid if c["sit"] == DEM), parc=sum(1 for c in lid if c["sit"] == PARC),
                ndem=sum(1 for c in lid if c["sit"] == NDEM), acoes=sum(1 for c in lid if c["acao"]), lid_rever=sum(1 for c in lid if lider_conf(c) != "OK"))


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        print("==", nome, resumo(ex), escopo_conf(ex["escopo"]))
        for a in aplicabilidade(ex):
            if a["aplica"] == NAO:
                print("  ", a["num"], a["just"], a["afeta"], a["conf"])
        for (t, _), c in zip(COMPROMISSOS, ex["lid"]):
            print("   %-26s %-16s %s" % (t, c["sit"], lider_conf(c)))
