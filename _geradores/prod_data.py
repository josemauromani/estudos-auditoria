# -*- coding: utf-8 -*-
"""Dados do estudo de Controle de produção e de serviço, usados pelo HTML e pela planilha.

As leituras de um registro (dentro, fora, fora sem reação) e os campos do plano de controle são uma convenção deste
material. Os exemplos continuam os dos outros estudos da série: a cozinha e a expedição da pizzaria, na semana de
08 a 14/03/2027, e a extrusora 3 da indústria de embalagens, na semana de 10 a 14/05/2027.
"""
from datetime import date

D = date
PRODUTO, PROCESSO = "Produto", "Processo"
TIPOS = [PRODUTO, PROCESSO]
DENTRO, FORA = "Dentro", "Fora"
SIM, NAO = "Sim", "Não"
SEMREACAO = "Fora sem reação registrada"
PARTES = [
    ("O que controlar", "A característica do produto ou o parâmetro do processo, em uma etapa.", "A temperatura da pizza na saída, na expedição"),
    ("Critério", "O valor mínimo, o máximo, ou o padrão que diz o que é conforme.", "No mínimo 65 °C"),
    ("Como medir", "O método e o instrumento.", "Termômetro de espeto, no centro da pizza"),
    ("Frequência", "Quando e em quantas unidades.", "Três pedidos por hora"),
    ("Quem", "A função que mede e registra.", "Líder da expedição"),
    ("Registro", "Onde o resultado fica guardado.", "Planilha da expedição"),
    ("Reação", "O que fazer com o produto e com o processo quando o resultado sai do critério.", "Reaquecer ou refazer, e conferir a bolsa térmica"),
]
ETAPAS = [
    ("Listar as etapas", "Do recebimento à entrega, na ordem em que o produto anda. Vêm do SIPOC ou da tartaruga."),
    ("Escolher o que controlar", "Em cada etapa, o que pode dar errado e pesa para o cliente, para a lei ou para a etapa seguinte."),
    ("Escrever o critério", "Mínimo, máximo ou padrão. Como medir, com que frequência, quem mede e onde registra."),
    ("Definir a reação", "O que fazer com o produto e com o processo quando o resultado sai do critério."),
    ("Registrar e rever", "Medir, registrar, reagir. Rever o plano a cada mudança, reclamação ou desvio que se repete."),
]


def criterio(k):
    """Texto do critério: faixa, mínimo, máximo ou atributo."""
    def n(v):
        return str(int(v)) if float(v).is_integer() else f"{v:g}".replace(".", ",")
    if k["min"] is None and k["max"] is None:
        return "Conforme ou não"
    if k["max"] is None:
        return f'mín. {n(k["min"])} {k["unid"]}'
    if k["min"] is None:
        return f'máx. {n(k["max"])} {k["unid"]}'
    return f'{n(k["min"])} a {n(k["max"])} {k["unid"]}'


def atributo(k):
    return k["min"] is None and k["max"] is None


def leitura(k, r):
    if atributo(k):
        return DENTRO if r["conf"] == SIM else FORA
    v = r["valor"]
    return DENTRO if (k["min"] is None or v >= k["min"]) and (k["max"] is None or v <= k["max"]) else FORA


def _plano(rows):
    keys = ("id", "etapa", "caract", "tipo", "min", "max", "unid", "metodo", "freq", "resp", "registro", "reacao")
    out = [dict(zip(keys, r)) for r in rows]
    for k in out:
        assert k["tipo"] in TIPOS, k["id"]
        assert k["min"] is None or k["max"] is None or k["min"] <= k["max"], k["id"]
    return out


def _regs(plano, dias, series, reacoes, lotes, quem):
    """Uma leitura por dia, para cada controle; `series` traz os valores na ordem dos dias."""
    ks = {k["id"]: k for k in plano}
    out = []
    for kid, vals in series:
        per = len(vals) // len(dias)
        assert per * len(dias) == len(vals), kid
        for j, v in enumerate(vals):
            d = dias[j // per]
            att = atributo(ks[kid])
            assert att == isinstance(v, str), (kid, v)
            out.append(dict(data=d, lote=lotes(d, kid, j % per), k=kid, valor=None if att else v, conf=v if att else None,
                            reacao=reacoes.get((kid, j), ""), quem=quem[kid]))
    for (kid, j) in reacoes:
        assert any(r["k"] == kid for r in out), kid
    out.sort(key=lambda r: (r["data"], int(r["k"][1:])))
    return out


# ------------------------------------------------------------ exemplo 1: pizzaria, cozinha e expedição
_DIAS1 = [D(2027, 3, d) for d in range(8, 15)]
_P1 = _plano([
    ("K1", "Receber e guardar insumos", "Temperatura da câmara fria", PROCESSO, 0, 5, "°C", "Termômetro da câmara, leitura no visor", "Duas vezes por turno",
     "Pizzaiolo do turno", "Planilha de temperatura (FR-02)", "Avisar o gerente, passar os insumos para o refrigerador reserva e avaliar o que ficou acima de 5 °C por mais de duas horas."),
    ("K2", "Preparar a massa", "Peso da bola de massa da pizza grande", PRODUTO, 380, 420, "g", "Balança da bancada, média de cinco bolas", "Cada lote de massa",
     "Pizzaiolo do turno", "Ficha do lote de massa", "Regular a divisora e pesar de novo o lote inteiro."),
    ("K3", "Montar", "Bancada e utensílios higienizados antes do turno", PROCESSO, None, None, "", "Lista de abertura do turno, conferida no posto", "Cada turno",
     "Pizzaiolo líder", "Lista de abertura do turno", "Higienizar antes de começar. Não montar pizza em bancada reprovada."),
    ("K4", "Assar", "Temperatura do forno", PROCESSO, 280, 320, "°C", "Termômetro do forno, no pico do turno", "Uma vez por hora",
     "Pizzaiolo do turno", "Registro de regulagem do forno", "Regular o forno e segurar a entrada de pizzas até a temperatura voltar à faixa."),
    ("K5", "Conferir e embalar", "Pedidos com a etiqueta rubricada, em 20 conferidos", PRODUTO, 20, None, "pedidos", "Conferência da pizza com a etiqueta; amostra de 20 no fechamento",
     "Todo pedido", "Quem embala", "Etiqueta rubricada", "Conferir de novo o pedido sem rubrica antes da saída e orientar quem embalou."),
    ("K6", "Expedir", "Maior espera da pizza pronta, na noite", PROCESSO, None, 10, "min", "Horários de pronto e de saída, no sistema de pedidos", "Todo pedido de entrega",
     "Líder da expedição", "Sistema de pedidos", "Priorizar a saída. Acima de 15 minutos, refazer a pizza."),
    ("K7", "Expedir", "Temperatura da pizza na saída", PRODUTO, 65, None, "°C", "Termômetro de espeto, no centro da pizza", "Três pedidos por hora",
     "Líder da expedição", "Planilha da expedição", "Reaquecer ou refazer, e conferir a bolsa térmica."),
])
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", processo="Produzir e embalar (P2) e Entregar o pedido (P3)", produto="Pizza entregue em casa",
                 rev="Revisão 2, de 01/03/2027", por="Pizzaiolo líder e líder da expedição, com o gerente da loja", periodo="Noites de 08 a 14/03/2027", ref=D(2027, 3, 15),
                 origem="Requisito 8.5.6 não atendido no diagnóstico de 2026, e objetivo O4: reduzir os pedidos refeitos."),
    "plano": _P1,
    "regs": _regs(_P1, _DIAS1, [
        ("K1", [3.2, 3.5, 3.0, 3.4, 3.6, 3.8, 4.1, 7.0, 3.3, 3.1, 2.9, 3.4, 3.2, 3.6]),
        ("K2", [402, 398, 405, 396, 410, 401, 399]),
        ("K3", [SIM] * 7),
        ("K4", [301, 296, 305, 299, 310, 268, 302]),
        ("K5", [20, 20, 20, 20, 19, 20, 20]),
        ("K6", [7, 6, 8, 9, 12, 14, 8]),
        ("K7", [71, 69, 72, 68, 66, 62, 70]),
    ], {
        ("K1", 7): "Insumos passados para o refrigerador reserva às 21h40. Borracha da porta solta, trocada em 12/03.",
        ("K4", 5): "Forno regulado. Entrada de pizzas segurada por seis minutos.",
        ("K5", 4): "Pedido conferido de novo antes de sair. Atendente do turno orientado.",
        ("K6", 4): "Saída priorizada. Nenhum pedido passou de 15 minutos.",
        ("K6", 5): "Dois pedidos refeitos. Escala do pico levada à reunião mensal.",
    }, lambda d, kid, j: {"K1": f"Câmara, {'1ª' if j == 0 else '2ª'} leitura", "K2": f"Massa {d:%d/%m}", "K3": f"Turno {d:%d/%m}"}.get(kid, f"Noite {d:%d/%m}"),
        {"K1": "Pizzaiolo do turno", "K2": "Pizzaiolo do turno", "K3": "Pizzaiolo líder", "K4": "Pizzaiolo do turno", "K5": "Quem embala", "K6": "Líder da expedição", "K7": "Líder da expedição"}),
    "rast": [
        ("Receber e guardar insumos", "Etiqueta com a data de recebimento e a validade.", "Só entra na câmara o que foi conferido no recebimento.", "Nota do fornecedor e planilha de recebimento.",
         "Câmara fria de 0 a 5 °C. Sai primeiro o que vence primeiro."),
        ("Preparar a massa", "Caixa com o lote do dia: data e turno.", "Massa liberada depois de pesada.", "Ficha do lote de massa.", "Descanso coberto, por até 24 horas."),
        ("Montar e assar", "A comanda, com o número do pedido, acompanha a pizza.", "Pizza assada só segue com a comanda.", "Sistema de pedidos.", "Bancada refrigerada para os recheios."),
        ("Conferir e embalar", "Etiqueta com o número do pedido, na caixa.", "Rubrica de quem conferiu.", "Etiqueta rubricada.", "Caixa lacrada."),
        ("Expedir e entregar", "Pedido ligado ao entregador, no sistema.", "Saída registrada com horário.", "Sistema: horário de saída e entregador.", "Bolsa térmica. Espera de até 10 minutos."),
    ],
    "prop": [
        ("Endereço e telefone do cliente", "Cliente", "Cadastro no sistema de pedidos.", "Acesso por senha. Listas de entrega picotadas no fechamento.", ""),
        ("Bolsas térmicas da plataforma de entrega", "Fornecedor", "Numeradas, com o nome da plataforma.", "Higienizadas a cada noite e guardadas na expedição.",
         "Bolsa nº 4 rasgada em 12/03. Plataforma avisada em 13/03; troca combinada."),
    ],
    "mud": [
        (D(2027, 3, 2), "Farinha da marca B no lugar da marca A.", "Falta no fornecedor.", "Um lote de massa de teste: peso e ponto conferidos.", "Pizzaiolo líder",
         "Receita ajustada, com 2% a mais de água. Ficha da massa atualizada."),
        (D(2027, 3, 12), "Tempo de forno de sete para seis minutos, no pico.", "Fila no forno na sexta à noite.", "", "", ""),
        (D(2027, 3, 26), "Dois entregadores extras nas sextas e nos sábados.", "Espera da pizza pronta acima de 10 minutos no pico.", "Esperas das duas últimas semanas, lidas na reunião mensal.",
         "Gerente da loja", "Escala padrão revista. Líder da expedição informado."),
    ],
}

# ------------------------------------------------------------ exemplo 2: indústria, extrusora 3
_DIAS2 = [D(2027, 5, d) for d in range(10, 15)]
_P2 = _plano([
    ("K1", "Receber a resina", "Índice de fluidez do lote de resina", PRODUTO, 1.8, 2.2, "g/10 min", "Laudo do fornecedor, conferido com a ficha técnica", "Cada lote recebido",
     "Laboratório", "Registro de recebimento", "Segregar o lote com etiqueta vermelha e acionar Suprimentos."),
    ("K2", "Extrusar", "Temperatura da zona 3 da extrusora", PROCESSO, 185, 195, "°C", "Leitura no painel da extrusora", "A cada duas horas",
     "Operador", "Folha de processo", "Ajustar a zona e medir de novo a bobina em curso."),
    ("K3", "Extrusar", "Espessura do filme", PRODUTO, 38, 42, "µm", "Micrômetro MIC-07, cinco pontos na largura", "Cada bobina",
     "Operador", "Folha de processo", "Ajustar a matriz, segregar a bobina com etiqueta vermelha e abrir o registro de produto não conforme."),
    ("K4", "Extrusar", "Largura do filme", PRODUTO, 598, 602, "mm", "Trena calibrada TR-03", "Cada bobina",
     "Operador", "Folha de processo", "Ajustar as guias e segregar a bobina."),
    ("K5", "Bobinar", "Aparência: sem géis, rugas ou furos", PRODUTO, None, None, "", "Exame visual, com o padrão de defeitos do posto", "Cada bobina",
     "Operador", "Folha de processo", "Segregar a bobina e procurar a origem: filtro, matriz ou resina."),
    ("K6", "Inspecionar e liberar", "Resistência da solda", PRODUTO, 12, None, "N/15 mm", "Dinamômetro do laboratório, três corpos de prova", "Uma amostra por lote",
     "Laboratório", "Laudo do lote", "Reter o lote, ensaiar de novo e decidir com a Qualidade."),
    ("K7", "Embalar e armazenar", "Etiqueta da bobina com lote, extrusora, turno e situação", PRODUTO, None, None, "", "Conferência da etiqueta com a folha de processo", "Cada bobina",
     "Expedição", "Romaneio", "Identificar de novo pela folha de processo. Sem origem comprovada, segregar."),
])
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", processo="Extrusão, na extrusora 3", produto="Filme de 40 µm para o cliente A, do segmento de alimentos",
                 rev="Revisão 5, de 03/05/2027", por="Gerente industrial, com o Laboratório e o Coordenador da Qualidade", periodo="Lotes 131 a 135, de 10 a 14/05/2027", ref=D(2027, 5, 17),
                 origem="Reclamações do cliente A por espessura e o objetivo O1: reduzir o refugo para 2,0%."),
    "plano": _P2,
    "regs": _regs(_P2, _DIAS2, [
        ("K1", [2.0, 2.0, 1.9, 2.0, 2.2]),
        ("K2", [190, 189, 196, 192, 191]),
        ("K3", [40.1, 39.6, 40.8, 41.5, 42.6, 41.9, 39.8, 40.2, 37.4, 39.1]),
        ("K4", [600, 601, 599, 600, 600]),
        ("K5", [SIM, NAO, SIM, SIM, SIM]),
        ("K6", [14.2, 13.8, 13.1, 14.0, 12.4]),
        ("K7", [SIM, SIM, SIM, NAO, SIM]),
    ], {
        ("K2", 2): "Zona 3 ajustada para 190 °C. Resistência com mau contato, trocada na parada do turno.",
        ("K3", 4): "Bobina segregada com etiqueta vermelha. Registro de produto não conforme 2027-18.",
        ("K3", 8): "Bobina segregada. Perfil de temperatura revisto para a resina do segundo fornecedor.",
        ("K5", 1): "Bobina segregada por géis. Tela do filtro trocada.",
    }, lambda d, kid, j: f"Lote {131 + (d.day - 10)}" + (f", bobina {j + 1}" if kid == "K3" else ""),
        {"K1": "Laboratório", "K2": "Operador", "K3": "Operador", "K4": "Operador", "K5": "Operador", "K6": "Laboratório", "K7": "Expedição"}),
    "rast": [
        ("Receber a resina", "Etiqueta com o lote do fornecedor e a data.", "Verde: aprovado. Amarela: aguarda laudo. Vermelha: reprovado.", "Registro de recebimento, com lote e laudo.",
         "Sacaria em palete, coberta e longe da umidade."),
        ("Extrusar", "Folha de processo com lote, extrusora, turno e lote da resina.", "Medições da bobina dentro do critério.", "Folha de processo.", ""),
        ("Bobinar", "Etiqueta da bobina: lote, número, extrusora e turno.", "Etiqueta verde depois das medições; vermelha se reprovada.", "Folha de processo, por bobina.",
         "Bobina em berço, sem contato com o piso."),
        ("Inspecionar e liberar", "Laudo com o número do lote.", "Carimbo de liberado, da Qualidade.", "Laudo do lote e amostra retida.", "Amostra guardada por 12 meses."),
        ("Embalar, armazenar e expedir", "Palete com etiqueta de lote e cliente.", "Só sai palete com laudo.", "Romaneio com os lotes embarcados.", "Filme esticável, cantoneiras e no máximo dois paletes de altura."),
    ],
    "prop": [
        ("Cilindros de impressão do cliente A", "Cliente", "Gravados com o código do cliente.", "Estante própria. Inspeção a cada uso.",
         "Risco em um cilindro em 06/05. Cliente avisado no mesmo dia; cilindro regravado."),
        ("Especificação e arte do cliente A", "Cliente", "Documento externo, com a revisão do cliente.", "Controlado na lista de documentos externos.", ""),
        ("Paletes e embalagens retornáveis", "Fornecedor", "Marca do fornecedor.", "Controle de saldo por fornecedor.", ""),
    ],
    "mud": [
        (D(2027, 5, 3), "Velocidade da linha de 42 para 45 m/min.", "Atraso na programação.", "", "Líder do turno", ""),
        (D(2027, 5, 14), "Resina do segundo fornecedor na extrusora 3.", "Segundo fornecedor homologado em 29/03.", "Lote piloto de duas bobinas: espessura e solda ensaiadas.",
         "Gerente industrial", "Zona 3 de 190 para 187 °C. Folha de processo na revisão 5."),
    ],
}

# exemplo 3: uma busca de rastreabilidade, para trás e para a frente (só no treinamento)
BUSCA = dict(
    gatilho="Cliente A reclama de filme fino no lote 135.",
    tras=[("Etiqueta do palete e romaneio", "Lote 135, extrusora 3, turno da manhã de 14/05."),
          ("Folha de processo", "Bobina 1 com 37,4 µm, fora do critério. Bobina 2 com 39,1 µm. Resina do lote R-0412, do segundo fornecedor."),
          ("Registro de recebimento", "Lote R-0412: índice de fluidez 2,2, no limite do critério. Laudo aprovado.")],
    frente=[("Bobinas do lote 135", "Bobina 1: segregada na fábrica, com etiqueta vermelha. Bobina 2: liberada."),
            ("Outros lotes com a resina R-0412", "Nenhum até 14/05. O lote 135 foi o primeiro com a resina nova."),
            ("Romaneio de expedição", "Só a bobina 2 foi embarcada para o cliente A, em 17/05.")],
    conclusao="A busca delimita o problema: só a bobina 2 chegou ao cliente, e mediu 39,1 µm, perto do mínimo. A resposta sai com dados, e a verificação se concentra nessa bobina.")

CHECK = [
    "As etapas do processo estão listadas, do recebimento à entrega.",
    "Cada controle diz o que medir, com o critério: mínimo, máximo ou padrão.",
    "Cada controle diz como medir, com que instrumento e com que frequência.",
    "Cada controle tem quem mede, onde registra e o que fazer quando o resultado sai do critério.",
    "Os instrumentos usados nos controles estão calibrados ou verificados.",
    "Quem executa conhece o plano, e a versão em uso no posto é a vigente.",
    "Os registros estão em dia, e cada resultado fora do critério tem a reação registrada.",
    "O produto é identificado em todas as etapas, e dá para saber se já foi verificado.",
    "É possível ir do produto entregue aos insumos e aos registros, e voltar.",
    "O que pertence ao cliente ou ao fornecedor está identificado e cuidado, e as ocorrências são comunicadas ao dono.",
    "O produto é protegido no manuseio, na armazenagem e no transporte.",
    "Toda mudança no processo tem análise, autorização e registro, antes de entrar em uso.",
]


def resumo_k(ex):
    """Por controle: verificações, resultados fora, fora sem reação."""
    out = []
    for k in ex["plano"]:
        rs = [r for r in ex["regs"] if r["k"] == k["id"]]
        fora = [r for r in rs if leitura(k, r) == FORA]
        out.append(dict(k=k, n=len(rs), fora=len(fora), semr=sum(1 for r in fora if not r["reacao"]), dentro=(len(rs) - len(fora)) / len(rs) if rs else None))
    return out


def resumo(ex):
    rk = resumo_k(ex)
    n, fora = sum(x["n"] for x in rk), sum(x["fora"] for x in rk)
    return dict(controles=len(rk), n=n, fora=fora, semr=sum(x["semr"] for x in rk), dentro=(n - fora) / n, semreg=sum(1 for x in rk if x["n"] == 0),
                mud=len(ex["mud"]), mud_ok=sum(1 for m in ex["mud"] if m[3] and m[4]))


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        print("==", nome, resumo(ex))
        for x in resumo_k(ex):
            print("  %s %-52s %-18s verif %2d fora %d sem reação %d" % (x["k"]["id"], x["k"]["caract"], criterio(x["k"]), x["n"], x["fora"], x["semr"]))
