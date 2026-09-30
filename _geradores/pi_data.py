# -*- coding: utf-8 -*-
"""Dados do estudo de Partes interessadas, usados pelo HTML e pela planilha.

A escala de 1 a 5, o corte de "alta" em 4, as quatro estratégias e a regra de pertinência são uma convenção deste material.
Os exemplos continuam os dos outros estudos da série (pizzaria e indústria de embalagens).
"""
from datetime import date

D = date
ALTA = 4   # nota igual ou acima disso conta como alta
GERIR, SATISF, INFORM, MONIT = "Gerir de perto", "Manter satisfeito", "Manter informado", "Monitorar"
# estratégia, quando, o que fazer
ESTRS = [
    (GERIR, "Influência alta e interesse alto", "Reunir, combinar os requisitos e acompanhar de perto."),
    (SATISF, "Influência alta e interesse baixo", "Cumprir o que exige, sem surpresas. Contato pontual."),
    (INFORM, "Influência baixa e interesse alto", "Contar o que muda e ouvir. Pode virar aliada ou reclamante."),
    (MONIT, "Influência baixa e interesse baixo", "Listar e rever uma vez por ano. Sem requisito no sistema."),
]
GRUPOS = ["Cliente", "Colaborador", "Fornecedor ou parceiro", "Regulador", "Proprietário ou investidor", "Sociedade", "Outro"]
LEGAL, CONTR, EXPEC = "Legal", "Contratual", "Expectativa"
TIPOS = [LEGAL, CONTR, EXPEC]
SIM, NAO = "Sim", "Não"
ATENDE, PARTE, NAOAT = "Atende", "Atende em parte", "Não atende"
SITS = [ATENDE, PARTE, NAOAT]
PONTOS = {ATENDE: 1.0, PARTE: 0.5, NAOAT: 0.0}
ETAPAS = [
    ("Identificar", "Listar quem afeta a organização e quem é afetado por ela, grupo por grupo."),
    ("Avaliar", "Dar nota à influência e ao interesse. A posição na matriz define a estratégia."),
    ("Levantar", "Escrever o que cada parte pertinente precisa e espera, com o tipo do requisito."),
    ("Decidir e atender", "Adotar ou não cada expectativa. Ligar o requisito a um processo e a uma medida."),
    ("Monitorar e revisar", "Acompanhar a situação e rever a lista todo ano, ou quando algo muda."),
]


def estrategia(inf, int_):
    if inf >= ALTA:
        return GERIR if int_ >= ALTA else SATISF
    return INFORM if int_ >= ALTA else MONIT


def pertinente(p):
    """Pertinente ao sistema: toda parte fora do quadrante de monitorar, ou com requisito legal."""
    return estrategia(p["inf"], p["int"]) != MONIT or p["legal"]


def _partes(rows):
    keys = ("nome", "curto", "grupo", "porque", "inf", "int", "legal", "canal", "quem")
    out = [dict(zip(keys, r), n=i + 1) for i, r in enumerate(rows)]
    for p in out:
        assert p["grupo"] in GRUPOS and 1 <= p["inf"] <= 5 and 1 <= p["int"] <= 5, p["nome"]
        assert len(p["curto"]) <= 26, p["curto"]
    return out


def _reqs(rows, partes):
    keys = ("parte", "req", "tipo", "adotado", "como", "monit", "sit", "acao", "resp", "prazo")
    nomes = {p["nome"] for p in partes}
    out = []
    for i, r in enumerate(rows):
        r = tuple(r) + (None,) * (len(keys) - len(r))
        d = dict(zip(keys, r), n=i + 1)
        assert d["parte"] in nomes, d["parte"]
        assert d["tipo"] in TIPOS and d["adotado"] in (SIM, NAO), d["req"]
        assert d["adotado"] == SIM or d["tipo"] == EXPEC, d["req"]
        if d["adotado"] == SIM:
            assert d["sit"] in SITS and d["monit"], d["req"]
            assert (d["sit"] == ATENDE) == (not d["acao"]), d["req"]
            assert bool(d["acao"]) == bool(d["resp"]) == bool(d["prazo"]), d["req"]
        out.append(d)
    return out


def adotados(ex, parte=None):
    return [r for r in ex["reqs"] if r["adotado"] == SIM and (parte is None or r["parte"] == parte)]


def atendimento(ex, parte=None):
    """Pontos dos requisitos adotados: 1 para atende, 0,5 para atende em parte, 0 para não atende."""
    a = adotados(ex, parte)
    return sum(PONTOS[r["sit"]] for r in a) / len(a) if a else None


def conta(ex, sit, parte=None):
    return sum(1 for r in adotados(ex, parte) if r["sit"] == sit)


# ------------------------------------------------------------ exemplo 1: pizzaria
_P1 = _partes([
    ("Clientes", "Clientes", "Cliente", "Compram, avaliam no aplicativo e decidem se voltam.", 5, 5, False,
     "Pedidos, reclamações e avaliações do aplicativo, todos os dias.", "Atendente líder"),
    ("Sócios", "Sócios", "Proprietário ou investidor", "Definem o investimento e esperam resultado.", 5, 5, False,
     "Reunião mensal de resultados.", "Gerente da loja"),
    ("Equipe da loja", "Equipe da loja", "Colaborador", "Produz, atende e embala. Sem ela não há pedido certo.", 4, 5, True,
     "Reunião semanal e quadro de avisos.", "Gerente da loja"),
    ("Entregadores", "Entregadores", "Fornecedor ou parceiro", "Levam o pedido ao cliente. São a loja na porta de quem comprou.", 4, 5, False,
     "Conversa no início do turno e grupo de mensagens.", "Líder da expedição"),
    ("Vigilância sanitária", "Vigilância sanitária", "Regulador", "Licencia e fiscaliza. Pode interditar a loja.", 5, 2, True,
     "Renovação anual da licença e visitas de fiscalização.", "Gerente da loja"),
    ("Prefeitura e Corpo de Bombeiros", "Prefeitura e Bombeiros", "Regulador", "Emitem o alvará e o auto de vistoria.", 5, 1, True,
     "Renovações, nas datas de vencimento.", "Gerente da loja"),
    ("Aplicativo de delivery", "Aplicativo de delivery", "Fornecedor ou parceiro", "Traz mais da metade dos pedidos e define a taxa e as regras.", 5, 2, False,
     "Painel do parceiro, toda semana.", "Gerente da loja"),
    ("Fornecedores de insumos", "Fornecedores de insumos", "Fornecedor ou parceiro", "Entregam queijo, farinha e embalagens. A falta para a produção.", 4, 3, False,
     "Pedido semanal e avaliação a cada semestre.", "Pizzaiolo líder"),
    ("Vizinhos da loja", "Vizinhos da loja", "Sociedade", "Convivem com o movimento, o ruído e as motos.", 2, 4, False,
     "Conversa direta e telefone da gerência na porta.", "Gerente da loja"),
    ("Portarias dos condomínios atendidos", "Portarias dos condomínios", "Sociedade", "Recebem o entregador e definem como o pedido sobe.", 3, 2, False, "", ""),
    ("Concorrentes do bairro", "Concorrentes", "Outro", "Disputam o mesmo cliente. Não têm requisito sobre a loja.", 2, 2, False, "", ""),
])
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", data=D(2026, 10, 23), por="Gerente da loja, com os três líderes",
                 escopo="A loja inteira: salão, produção e delivery.",
                 origem="Diagnóstico da ISO 9001 de 02/10/2026, requisito 4.2: incluir entregadores e fornecedores, com o que cada um espera.",
                 revisao="Uma vez por ano, em outubro, e sempre que uma parte mudar de posição."),
    "partes": _P1,
    "reqs": _reqs([
        ("Clientes", "Receber o pedido em até 40 minutos.", CONTR, SIM, "Processo de delivery, com escala reforçada no pico e agrupamento por zona.",
         "Entregas em até 40 minutos, todo mês.", ATENDE),
        ("Clientes", "Receber a pizza quente e o pedido certo, na primeira vez.", EXPEC, SIM, "Conferência do pedido antes de embalar, com etiqueta rubricada.",
         "Pedidos refeitos por erro, todo mês.", PARTE, "Analisar a alta dos pedidos refeitos desde a troca do sistema de pedidos.", "Pizzaiolo líder", D(2026, 11, 20)),
        ("Clientes", "Ter um canal para reclamar e receber resposta.", EXPEC, SIM, "Registro de reclamações do site, do aplicativo e do telefone.",
         "Reclamações por 100 pedidos, todo mês.", PARTE, "Medir a satisfação, e não só a reclamação: propor a pesquisa na análise crítica.", "Atendente líder", D(2026, 12, 14)),
        ("Sócios", "Recuperar a margem do delivery, que caiu com a taxa do aplicativo.", EXPEC, SIM, "Ciclo PDCA da margem do delivery, aberto em 09/10/2026.",
         "Margem do delivery, todo mês, na reunião de resultados.", NAOAT, "Concluir o ciclo PDCA e levar o resultado aos sócios.", "Gerente da loja", D(2027, 1, 29)),
        ("Equipe da loja", "Salário em dia, registro e condições seguras de trabalho.", LEGAL, SIM, "Folha de pagamento e rotina de segurança da cozinha.",
         "Conferência da folha, todo mês, e inspeção de segurança, a cada trimestre.", ATENDE),
        ("Equipe da loja", "Saber o que se espera da função e ser treinada para ela.", EXPEC, SIM, "Instruções de trabalho nos postos e treinamento na admissão.",
         "Registros de treinamento, a cada admissão.", PARTE, "Montar a matriz de competências da loja.", "Gerente da loja", D(2027, 2, 12)),
        ("Entregadores", "Receber por entrega, no dia combinado.", CONTR, SIM, "Fechamento semanal das entregas.", "Conferência do fechamento, toda segunda-feira.", ATENDE),
        ("Entregadores", "Sair com o pedido pronto, a rota agrupada e o endereço completo.", EXPEC, SIM, "Instrução da expedição e campo de complemento obrigatório.",
         "Atrasos por motivo, na folha de verificação.", ATENDE),
        ("Entregadores", "Conhecer a escala com antecedência.", EXPEC, SIM, "Escala avisada na véspera, pelo grupo de mensagens.",
         "Saídas de entregadores, a cada trimestre.", PARTE, "Publicar a escala da semana toda sexta-feira.", "Líder da expedição", D(2026, 11, 6)),
        ("Vigilância sanitária", "Manter a licença sanitária válida.", LEGAL, SIM, "Renovação protocolada em 09/10/2026.",
         "Controle de vencimentos das licenças, todo mês.", PARTE, "Acompanhar o protocolo até a emissão da licença.", "Gerente da loja", D(2026, 11, 13)),
        ("Vigilância sanitária", "Cumprir as boas práticas de manipulação: temperatura, higiene e controle de pragas.", LEGAL, SIM,
         "Manual de boas práticas e registro de temperatura, duas vezes por turno.", "Registros de temperatura, conferidos toda semana.", ATENDE),
        ("Prefeitura e Corpo de Bombeiros", "Manter o alvará de funcionamento e o auto de vistoria válidos.", LEGAL, SIM, "Documentos afixados na loja, com vencimento em 2027.",
         "Controle de vencimentos das licenças, todo mês.", ATENDE),
        ("Aplicativo de delivery", "Aceitar o pedido em até 3 minutos e manter a nota mínima da loja.", CONTR, SIM, "Tela de pedidos no balcão, com alerta sonoro.",
         "Painel do parceiro, toda semana.", ATENDE),
        ("Fornecedores de insumos", "Receber o pedido da semana até quarta-feira e o pagamento no prazo.", CONTR, SIM, "Rotina de compras do pizzaiolo líder.",
         "Pedidos fora do dia e pagamentos em atraso, todo mês.", ATENDE),
        ("Vizinhos da loja", "Motos desligadas na espera e fora da calçada.", EXPEC, SIM, "Área de espera marcada no recuo da loja.",
         "Reclamações de vizinhos, registradas pela gerência.", ATENDE),
        ("Vizinhos da loja", "Encerrar as entregas às 22h.", EXPEC, NAO,
         "O alvará permite funcionar até 23h30, e um terço dos pedidos de sexta e de sábado entra depois das 22h. A loja adotou o requisito do ruído."),
    ], _P1),
}

# ------------------------------------------------------------ exemplo 2: indústria de embalagens
_P2 = _partes([
    ("Clientes de alimentos", "Clientes de alimentos", "Cliente", "Compram a maior parte do volume e respondem pela embalagem perante o consumidor.", 5, 5, False,
     "Visitas do comercial, pesquisa anual e reclamações.", "Gerente comercial"),
    ("Clientes de cosméticos e industriais", "Outros clientes", "Cliente", "Exigem impressão no padrão e pedem embalagem com material reciclado.", 4, 4, False,
     "Visitas do comercial, pesquisa anual e reclamações.", "Gerente comercial"),
    ("Direção e acionistas", "Direção e acionistas", "Proprietário ou investidor", "Aprovam os recursos e definem a estratégia.", 5, 5, False,
     "Análise crítica anual e reunião mensal de resultados.", "Coordenador da Qualidade"),
    ("Colaboradores", "Colaboradores", "Colaborador", "Operam as extrusoras e a impressão. A segurança deles é obrigação legal.", 4, 5, True,
     "Reunião de turno, mural e pesquisa de clima anual.", "RH"),
    ("Autoridade sanitária", "Autoridade sanitária", "Regulador", "Regula os materiais que entram em contato com alimentos.", 5, 2, True,
     "Acompanhamento das normas, a cada trimestre.", "Coordenador da Qualidade"),
    ("Órgão ambiental", "Órgão ambiental", "Regulador", "Emite a licença de operação e fiscaliza os resíduos.", 5, 2, True,
     "Renovação da licença e relatórios anuais.", "Gerente de Produção"),
    ("Fornecedores de resina", "Fornecedores de resina", "Fornecedor ou parceiro", "Três itens críticos têm fornecedor único.", 5, 3, False,
     "Previsão trimestral e avaliação a cada semestre.", "Gerente de Suprimentos"),
    ("Organismo de certificação", "Organismo de certificação", "Fornecedor ou parceiro", "Audita o sistema todo ano e mantém o certificado.", 4, 3, False,
     "Auditoria anual e contato do Coordenador da Qualidade.", "Coordenador da Qualidade"),
    ("Transportadoras", "Transportadoras", "Fornecedor ou parceiro", "Levam o produto ao cliente. O atraso delas é atraso da fábrica.", 3, 4, False,
     "Agendamento diário e reunião a cada semestre.", "Líder da expedição"),
    ("Comunidade vizinha", "Comunidade vizinha", "Sociedade", "Convive com o tráfego de caminhões e com o ruído do turno da noite.", 2, 4, False,
     "Telefone da portaria e reunião anual com a associação do bairro.", "Gerente de Produção"),
    ("Sindicato da categoria", "Sindicato", "Sociedade", "Negocia o acordo coletivo uma vez por ano.", 3, 3, False, "", ""),
    ("Bancos e seguradora", "Bancos e seguradora", "Outro", "Financiam e seguram o patrimônio. Não têm requisito sobre o produto.", 2, 2, False, "", ""),
])
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", data=D(2027, 1, 20), por="Coordenador da Qualidade, com os gerentes e a direção",
                 escopo="A fábrica inteira: extrusão, impressão, corte e expedição.",
                 origem="Revisão anual, em preparação para a análise crítica de 18/02/2027.",
                 revisao="Uma vez por ano, em janeiro, antes da análise crítica."),
    "partes": _P2,
    "reqs": _reqs([
        ("Clientes de alimentos", "Filme com espessura e dimensões dentro da especificação, em todas as bobinas.", CONTR, SIM,
         "Plano de inspeção da extrusão. Inspeção de 100% das bobinas do cliente A desde outubro.", "Reclamações por motivo e refugo por defeito, todo mês.", PARTE,
         "Levar a compra do medidor de espessura em linha à análise crítica.", "Gerente de Produção", D(2027, 2, 18)),
        ("Clientes de alimentos", "Declaração de conformidade para contato com alimentos, a cada lote.", CONTR, SIM, "Laudo emitido pela Qualidade na liberação do lote.",
         "Auditoria interna da liberação, a cada semestre.", ATENDE),
        ("Clientes de alimentos", "Entrega na data confirmada.", CONTR, SIM, "Programação da produção e agendamento com as transportadoras.",
         "Entregas no prazo, todo mês, e nota de prazo na pesquisa anual.", PARTE, "Rever a programação do segmento de alimentos, que deu nota 7,8 ao prazo.", "Gerente comercial", D(2027, 3, 31)),
        ("Clientes de alimentos", "Resposta a reclamação em até 2 dias úteis, com análise de causa.", EXPEC, SIM, "Tratamento de reclamações, com registro de não conformidade.",
         "Prazo de resposta, todo mês.", ATENDE),
        ("Clientes de cosméticos e industriais", "Impressão dentro do padrão de cor aprovado.", CONTR, SIM, "Padrão de cor assinado pelo cliente, no posto da impressora.",
         "Reclamações por motivo, todo mês.", ATENDE),
        ("Clientes de cosméticos e industriais", "Embalagem com 30% de resina reciclada até 2028.", EXPEC, SIM, "Ainda não há produto com resina reciclada.",
         "Projetos de desenvolvimento, a cada trimestre.", NAOAT, "Abrir o projeto de resina reciclada, com fornecedor homologado.", "Gerente de Produção", D(2027, 6, 30)),
        ("Direção e acionistas", "Refugo abaixo de 3% e certificado mantido.", EXPEC, SIM, "Objetivos da qualidade e ciclo PDCA do refugo.",
         "Painel de indicadores, todo mês.", PARTE, "Concluir o ciclo PDCA do refugo.", "Gerente de Produção", D(2027, 4, 30)),
        ("Colaboradores", "Máquinas com proteção e treinamento de segurança em dia.", LEGAL, SIM, "Programa de segurança e inspeção das proteções.",
         "Inspeção mensal e registros de treinamento.", ATENDE),
        ("Colaboradores", "Saber o que falta aprender para a função e ter um plano de treinamento.", EXPEC, SIM, "Matriz de competências de Suprimentos em montagem. As outras áreas não têm.",
         "Cobertura da matriz, a cada semestre.", PARTE, "Estender a matriz de competências à Produção.", "RH", D(2027, 5, 28)),
        ("Autoridade sanitária", "Usar só materiais permitidos para contato com alimentos.", LEGAL, SIM, "Especificação das resinas e laudos do fornecedor, conferidos no recebimento.",
         "Laudos de migração, uma vez por ano.", ATENDE),
        ("Órgão ambiental", "Licença de operação válida e resíduos com destinação comprovada.", LEGAL, SIM, "Licença válida até 2028 e manifestos de resíduos arquivados.",
         "Controle de vencimentos e manifestos, todo mês.", ATENDE),
        ("Fornecedores de resina", "Previsão de compra do trimestre e pagamento no prazo.", CONTR, SIM, "Previsão enviada por Suprimentos no início de cada trimestre.",
         "Avaliação de fornecedores, a cada semestre.", ATENDE),
        ("Organismo de certificação", "Auditoria anual recebida e não conformidades tratadas no prazo.", CONTR, SIM, "Programa de auditorias e controle das não conformidades.",
         "Situação das não conformidades, todo mês.", ATENDE),
        ("Transportadoras", "Carga pronta e conferida no horário agendado.", CONTR, SIM, "Agendamento da expedição.", "Tempo de espera do caminhão, todo mês.", ATENDE),
        ("Comunidade vizinha", "Caminhões fora do horário de entrada e de saída da escola.", EXPEC, SIM, "Janela de carga e descarga definida na portaria.",
         "Reclamações da comunidade, registradas pela portaria.", ATENDE),
        ("Comunidade vizinha", "Encerrar o turno da noite.", EXPEC, NAO,
         "A fábrica opera dentro do limite de ruído da licença, medido todo ano, e o turno da noite responde por um terço da produção."),
    ], _P2),
}

# exemplo 3: uma parte que muda de posição (só no treinamento)
MUDANCA = dict(parte="Portarias dos condomínios atendidos", antes=(3, 2), depois=(4, 3), data=D(2027, 5, 7),
               requisito="Avisar a portaria na saída do pedido e entregar na porta do apartamento.",
               canal="Contato com a administração de cada condomínio, a cada trimestre.",
               linha=[
                   (D(2026, 10, 23), "Primeira análise", "Portarias listadas, com influência 3 e interesse 2. Estratégia: monitorar. Sem requisito e sem canal."),
                   (D(2027, 2, 20), "Primeiro sinal", "Reclamação de pizza fria: o pedido ficou 15 minutos na portaria de um condomínio."),
                   (D(2027, 4, 3), "Repetição", "Terceira reclamação do mesmo condomínio. Aberta a RNC 2027-04."),
                   (D(2027, 4, 10), "Tratamento", "Entrega na porta do apartamento, combinada com a administração do condomínio."),
                   (D(2027, 5, 7), "Revisão da lista", "Influência 4 e interesse 3. Estratégia: manter satisfeito. Um requisito adotado e um canal definido."),
               ])

CHECK = [
    "A lista cobre os grupos: clientes, colaboradores, fornecedores e parceiros, reguladores, proprietários e sociedade.",
    "Cada parte tem nota de influência e de interesse, dada pela equipe, com o motivo escrito.",
    "As partes pertinentes ao sistema estão separadas das que são só monitoradas.",
    "Cada parte pertinente tem pelo menos um requisito escrito, com verbo e critério.",
    "Os requisitos legais e contratuais estão identificados e foram todos adotados.",
    "Cada expectativa tem decisão registrada: adotada, ou não adotada, com a justificativa.",
    "Cada requisito adotado está ligado a um processo ou a um documento que o atende.",
    "Cada requisito adotado tem uma forma de monitoramento, com fonte e frequência.",
    "A situação de cada requisito está avaliada, e o que não atende tem ação, responsável e prazo.",
    "Cada parte pertinente tem um canal de relacionamento e alguém que cuida dele.",
    "A lista alimentou a Matriz SWOT, a Matriz de riscos e o escopo do sistema.",
    "A lista tem data de revisão, e o resultado vai à análise crítica pela direção.",
]


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        print("==", nome, "| partes", len(ex["partes"]), "| pertinentes", sum(1 for p in ex["partes"] if pertinente(p)), "| requisitos", len(ex["reqs"]), "| adotados", len(adotados(ex)))
        for p in ex["partes"]:
            a = atendimento(ex, p["nome"])
            print("  %2d %-38s %d %d %-18s %s %s" % (p["n"], p["nome"], p["inf"], p["int"], estrategia(p["inf"], p["int"]), "pert." if pertinente(p) else "     ",
                                                   "" if a is None else "%d req., %.0f%%" % (len(adotados(ex, p["nome"])), 100 * a)))
            assert not pertinente(p) or adotados(ex, p["nome"]), p["nome"]
            assert pertinente(p) == bool(p["canal"]), p["nome"]
            assert p["legal"] == any(r["tipo"] == LEGAL for r in ex["reqs"] if r["parte"] == p["nome"]), p["nome"]
        print("  atende %d, em parte %d, não atende %d | atendimento %.1f%%" % (conta(ex, ATENDE), conta(ex, PARTE), conta(ex, NAOAT), 100 * atendimento(ex)))
    assert estrategia(*MUDANCA["antes"]) == MONIT and estrategia(*MUDANCA["depois"]) == SATISF
