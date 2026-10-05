# -*- coding: utf-8 -*-
"""Dados do estudo de Requisitos do cliente e análise de pedidos, usados pelo HTML e pela planilha.

As sete perguntas da análise, as decisões, as leituras e as regras de conferência são uma convenção deste material.
Os exemplos continuam os dos outros estudos da série: as encomendas e os pedidos por telefone da pizzaria de 22 a
28/03/2027, e os pedidos e as propostas da indústria de 01 a 15/06/2027.
"""
from datetime import date

D = date
SIM, NAO, NA = "Sim", "Não", "Não se aplica"
RESP = [SIM, NAO, NA]
ACEITO, ALTERADO, RECUSADO, EMANALISE = "Aceito", "Aceito com alteração", "Recusado", "Em análise"
DECISOES = [ACEITO, ALTERADO, RECUSADO, EMANALISE]
L_OK, L_PEND, L_INC = "Pode aceitar", "Resolver antes de aceitar", "Análise incompleta"
PERGUNTAS = [
    ("Especificação", "O produto e a especificação estão definidos, e a organização consegue cumpri-la?"),
    ("Capacidade e prazo", "A quantidade e o prazo cabem na capacidade, considerando o que já foi aceito?"),
    ("Entrega e pós-entrega", "O local, a forma de entrega e o que vem depois dela estão combinados?"),
    ("Uso pretendido", "Os requisitos que o cliente não declarou, mas que o uso exige, foram considerados?"),
    ("Requisitos legais", "Os requisitos legais e regulamentares do produto e do uso foram identificados?"),
    ("Diferenças", "As diferenças em relação à proposta, ao pedido anterior ou ao catálogo foram resolvidas?"),
    ("Preço e condições", "O preço, o pagamento e as demais condições estão confirmados?"),
]
NQ = len(PERGUNTAS)
FONTES = [
    ("Declarados", "O que o cliente pede: o produto, a quantidade, o prazo, o local.", "50 pizzas grandes para sábado, às 21h, no salão de festas do condomínio."),
    ("Não declarados, mas necessários", "O que o uso exige, mesmo sem o cliente dizer.", "A pizza para uma criança celíaca precisa estar livre de glúten, inclusive de contaminação na cozinha."),
    ("Legais e regulamentares", "O que a lei exige do produto e da forma de vender.", "Informar os alergênicos. Não vender bebida alcoólica a menores de idade."),
    ("Da organização", "O que a própria organização decide exigir de si.", "Encomendas a partir de 20 pizzas, com 48 horas de antecedência."),
]
ETAPAS = [
    ("Definir a oferta", "O que se oferece, a especificação, os requisitos legais e o que não se garante."),
    ("Receber o pedido", "Pelos canais definidos, com os requisitos declarados por escrito ou confirmados."),
    ("Analisar antes de aceitar", "As sete perguntas, com quem conhece a capacidade, o produto e a lei."),
    ("Decidir e confirmar", "Aceitar, negociar uma alteração ou recusar, e confirmar com o cliente."),
    ("Controlar as mudanças", "O pedido que muda é analisado de novo, os documentos são atualizados e as pessoas, informadas."),
]


def respostas_txt(r):
    return [{"S": SIM, "N": NAO, "-": NA, "": ""}[c] for c in r]


def leitura(p):
    if any(x == "" for x in p["q"]):
        return L_INC
    return L_PEND if NAO in p["q"] else L_OK


def pendencias(p):
    return sum(1 for x in p["q"] if x == NAO)


def conf(p):
    """Conferência de um pedido: a mesma regra da planilha."""
    if not p["dec"]:
        return "Falta a decisão"
    if not p["quem"]:
        return "Falta quem analisou"
    if p["dec"] == EMANALISE:
        return "OK"
    if any(x == "" for x in p["q"]):
        return "Falta responder à análise"
    if not p["analise"]:
        return "Falta a data da análise"
    if p["dec"] in (ACEITO, ALTERADO) and not p["confirm"]:
        return "Falta a data da confirmação"
    if p["dec"] in (ACEITO, ALTERADO) and p["analise"] > p["confirm"]:
        return "Analisado depois de aceitar"
    if p["dec"] == ACEITO and NAO in p["q"]:
        return "Aceito com pendência na análise"
    if p["dec"] == ALTERADO and not p["neg"]:
        return "Falta o que foi negociado"
    if p["dec"] == RECUSADO and not p["neg"]:
        return "Falta o motivo da recusa"
    return "OK"


def mud_conf(m):
    if not m["analise"]:
        return "Falta a análise"
    if m["docs"] != SIM:
        return "Documentos não atualizados"
    if not m["inform"]:
        return "Falta quem foi informado"
    return "OK"


def oferta_conf(o):
    if not o["espec"]:
        return "Falta a especificação"
    if not o["onde"]:
        return "Falta onde o cliente é informado"
    if o["cap"] != SIM:
        return "Capacidade não confirmada"
    return "OK"


def _ofertas(rows):
    return [dict(zip(("item", "espec", "legal", "naogar", "onde", "cap"), r)) for r in rows]


def _peds(rows):
    keys = ("num", "data", "cliente", "canal", "pede", "naodecl", "prazo", "q", "dec", "neg", "quem", "analise", "confirm")
    out = []
    for r in rows:
        p = dict(zip(keys, r))
        assert len(p["q"]) == NQ, p["num"]
        p["q"] = respostas_txt(p["q"])
        assert p["dec"] in DECISOES, p["num"]
        out.append(p)
    return out


def _muds(rows):
    out = [dict(zip(("data", "ped", "oque", "pediu", "analise", "docs", "inform"), r)) for r in rows]
    for m in out:
        assert m["docs"] in (SIM, NAO), m["oque"]
    return out


# ------------------------------------------------------------ exemplo 1: pizzaria, encomendas e pedidos por telefone
_GL, _AT = "Gerente da loja", "Atendente do turno"
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", processo="Registrar o pedido (P1)", periodo="Encomendas e pedidos especiais de 22 a 28/03/2027", ref=D(2027, 3, 29),
                 analisa="Pedido comum: atendente, na tela de confirmação. Encomenda de 20 pizzas ou mais: gerente da loja, antes de confirmar.",
                 origem="Requisito 8.2.3 atendido em parte no diagnóstico de 2026: pedidos por telefone sem o complemento do endereço (RNC 2026-05)."),
    "ofertas": _ofertas([
        ("Pizza no delivery", "Sabores e tamanhos do cardápio, com os ingredientes. Entrega em até 40 minutos na área de entrega.",
         "Alergênicos informados no cardápio.", "Ausência de glúten e de traços de leite: a cozinha é compartilhada. Entrega fora da área.", "Cardápio, site e aplicativo.", SIM),
        ("Retirada no balcão", "Os mesmos sabores e tamanhos, prontos em até 25 minutos.", "Alergênicos informados no cardápio.", "Reserva de horário exato.", "Cardápio e telefone.", SIM),
        ("Encomenda para eventos", "A partir de 20 pizzas, com 48 horas de antecedência, de terça a domingo, das 18h às 23h.",
         "Alergênicos informados na confirmação. Bebida alcoólica só para maiores de 18 anos.", "Montagem no local do evento.", "Site e telefone.", NAO),
    ]),
    "peds": _peds([
        ("E-31", D(2027, 3, 22), "Escritório de contabilidade", "Telefone", "30 pizzas grandes, sexta 26/03 às 19h, no 8º andar de um prédio comercial.",
         "Entrega com elevador de serviço, combinada com a portaria.", D(2027, 3, 26), "SSSSSSS", ACEITO, "", _GL, D(2027, 3, 22), D(2027, 3, 22)),
        ("T-1184", D(2027, 3, 23), "Cliente por telefone", "Telefone", "Uma pizza grande meia calabresa, meia muçarela.",
         "", D(2027, 3, 23), "SSSS-SS", ACEITO, "Complemento do endereço pedido e lido de volta antes de confirmar.", _AT, D(2027, 3, 23), D(2027, 3, 23)),
        ("A-772", D(2027, 3, 24), "Cliente pelo aplicativo", "Aplicativo", "Pizza de muçarela “sem glúten”, para uma criança celíaca.",
         "Isenção total de glúten, inclusive de contaminação na cozinha.", D(2027, 3, 24), "SSSNSSS", RECUSADO,
         "A cozinha não garante a ausência de glúten. Cliente informado pelo telefone, com o motivo.", _GL, D(2027, 3, 24), None),
        ("E-32", D(2027, 3, 25), "Comissão de formatura", "Telefone", "50 pizzas grandes, sábado 27/03 às 21h, no salão de festas.",
         "Bebidas para a festa: o cliente pediu cerveja; a turma tem alunos menores de idade.", D(2027, 3, 27), "SNSSNSS", ALTERADO,
         "Entrega às 18h30, em duas levas, antes do pico do sábado. Sem bebida alcoólica no pedido.", _GL, D(2027, 3, 25), D(2027, 3, 25)),
        ("E-33", D(2027, 3, 25), "Escola do bairro", "Telefone", "20 pizzas para segunda 29/03, às 11h.", "", D(2027, 3, 29), "SNSSSSS", RECUSADO,
         "A loja não atende encomendas para eventos às segundas, e o horário de encomenda começa às 18h. O cliente não aceitou outro dia.", _GL, D(2027, 3, 25), None),
        ("T-1201", D(2027, 3, 26), "Cliente por telefone", "Telefone", "Duas pizzas grandes, para entrega em um bairro vizinho.", "", D(2027, 3, 26), "SSNS-SS", ALTERADO,
         "O endereço fica fora da área de entrega. O cliente aceitou retirar no balcão.", _AT, D(2027, 3, 26), D(2027, 3, 26)),
        ("E-34", D(2027, 3, 26), "Empresa de eventos", "Telefone", "40 pizzas grandes, sábado 27/03 às 20h.", "", D(2027, 3, 27), "SNSSSSS", ACEITO, "", _AT,
         D(2027, 3, 26), D(2027, 3, 26)),
        ("E-35", D(2027, 3, 26), "Família do bairro", "Telefone", "25 pizzas grandes, domingo 28/03 às 20h, para um aniversário.", "", D(2027, 3, 28), "SSSSSSS", ACEITO, "",
         _GL, D(2027, 3, 27), D(2027, 3, 26)),
    ]),
    "muds": _muds([
        (D(2027, 3, 24), "E-31", "De 30 para 35 pizzas, com 5 sabores trocados.", "Cliente, por telefone", "Capacidade conferida pelo gerente: a sexta às 19h comporta.",
         SIM, "Pizzaiolo líder e líder da expedição"),
        (D(2027, 3, 26), "E-32", "Mais 10 pizzas doces na segunda leva.", "Cliente, pelo aplicativo de mensagens", "", NAO, ""),
    ]),
}

# ------------------------------------------------------------ exemplo 2: indústria, pedidos e propostas
_CO, _EN, _PC = "Gerente comercial", "Gerente de engenharia", "Programação da produção"
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", processo="Vender e programar", periodo="Pedidos e propostas de 01 a 15/06/2027", ref=D(2027, 6, 16),
                 analisa="Gerente comercial, com a Programação para capacidade e prazo, a Engenharia para itens novos e a Qualidade para requisitos legais.",
                 origem="Reclamações do cliente A por espessura e a certificação ISO 9001 prevista para dezembro (objetivo O4)."),
    "ofertas": _ofertas([
        ("Filme liso", "Espessura de 30 a 80 µm, com tolerância de ±2 µm; largura de 300 a 1.200 mm; bobinas de até 800 mm de diâmetro.",
         "Declaração de conformidade para contato com alimentos, a cada lote.", "Tolerância de espessura menor que ±2 µm.", "Catálogo técnico e proposta.", SIM),
        ("Filme impresso", "Até seis cores, com a arte aprovada pelo cliente e os cilindros do cliente.", "Tintas próprias para embalagem de alimentos.",
         "Cores fora da tabela de tintas homologadas.", "Catálogo técnico e proposta.", SIM),
        ("Filme com resina reciclada", "Até 30% de resina reciclada, só na camada externa, por acordo de desenvolvimento.",
         "Resina reciclada não é usada na camada em contato com o alimento.", "Fornecimento regular antes da aprovação do lote piloto.", "Proposta de desenvolvimento.", SIM),
    ]),
    "peds": _peds([
        ("PV-2231", D(2027, 6, 1), "Cliente A", "E-mail", "12 t de filme liso de 40 µm, 600 mm, em 20 dias. Igual ao pedido de maio.", "", D(2027, 6, 21), "SSSSSSS", ACEITO, "", _CO,
         D(2027, 6, 1), D(2027, 6, 1)),
        ("PV-2232", D(2027, 6, 2), "Cliente B", "E-mail", "30 t de filme liso de 50 µm em 10 dias.", "", D(2027, 6, 12), "SNSSSSS", ALTERADO,
         "15 t em 10 dias e 15 t em 25 dias, com o aceite do cliente por e-mail.", _CO, D(2027, 6, 2), D(2027, 6, 3)),
        ("PR-118", D(2027, 6, 3), "Cliente C, alimentos congelados", "Visita", "Filme liso de 50 µm para embalar vegetais congelados.",
         "Resistência ao impacto a -18 °C, que o filme padrão não tem. Declaração de conformidade para contato com alimentos.", D(2027, 7, 15), "SSSNSSS", ALTERADO,
         "Lote de teste de 500 kg com a resina para baixa temperatura, ensaiado pelo cliente antes do pedido firme.", _EN, D(2027, 6, 4), D(2027, 6, 7)),
        ("PV-2236", D(2027, 6, 7), "Cliente A", "E-mail", "Item novo: filme de 35 µm com tolerância de ±1 µm.", "", D(2027, 6, 30), "NSSSSSS", ALTERADO,
         "Tolerância de ±2 µm, a capacidade do processo, aceita pelo cliente por e-mail.", _EN, D(2027, 6, 8), D(2027, 6, 9)),
        ("PR-119", D(2027, 6, 8), "Cliente D", "E-mail", "Filme com 50% de resina reciclada, para contato direto com queijos.", "", D(2027, 7, 1), "SSSSNSS", RECUSADO,
         "A resina reciclada não pode estar em contato com o alimento. Oferecido o filme com 30% na camada externa, em desenvolvimento.", "Coordenador da Qualidade",
         D(2027, 6, 9), None),
        ("PV-2238", D(2027, 6, 9), "Cliente B", "E-mail", "10 t de filme liso de 50 µm, com 620 mm de largura.", "", D(2027, 6, 25), "SSSSSNS", ACEITO, "", _CO,
         D(2027, 6, 9), D(2027, 6, 9)),
        ("PR-120", D(2027, 6, 10), "Cliente E", "Visita", "Filme impresso em quatro cores para embalagem de biscoitos.", "", D(2027, 7, 10), "NSSSSSS", EMANALISE,
         "Aguardando a arte aprovada pelo cliente.", _CO, D(2027, 6, 11), None),
        ("PV-2241", D(2027, 6, 11), "Cliente A", "Telefone", "8 t de filme liso de 40 µm, urgente, em 5 dias.", "", D(2027, 6, 16), "SSSSSSS", ACEITO, "", _PC,
         D(2027, 6, 14), D(2027, 6, 11)),
    ]),
    "muds": _muds([
        (D(2027, 6, 4), "PV-2232", "Entrega no novo centro de distribuição do cliente.", "Comprador do cliente B", "Frete recalculado e aceito pelo cliente.", SIM, "Expedição"),
        (D(2027, 6, 11), "PV-2231", "De 12 para 16 t.", "Comprador do cliente A", "Programação conferiu a extrusora 3. Compras confirmou a resina.", SIM, "Produção e Compras"),
        (D(2027, 6, 12), "PV-2238", "Largura corrigida de 600 para 620 mm na ordem de produção.", "Programação da produção", "Conferida com o pedido do cliente.", SIM, ""),
    ]),
}

# exemplo 3: as quatro fontes de requisitos de um pedido novo (só no treinamento)
FONTES_C = dict(ped="PR-118 · Cliente C · filme para vegetais congelados", fontes=[
    ("Declarados", "Filme liso de 50 µm, bobinas de 600 mm, primeira entrega em julho."),
    ("Não declarados, mas necessários", "O filme vai ao freezer a -18 °C: precisa resistir ao impacto no frio, e o padrão fica quebradiço."),
    ("Legais e regulamentares", "Embalagem para alimentos: declaração de conformidade para contato com alimentos, a cada lote."),
    ("Da organização", "Item novo passa pela Engenharia. Material novo só com lote de teste aprovado."),
], decisao="Aceito com alteração: lote de teste de 500 kg com a resina para baixa temperatura, ensaiado pelo cliente antes do pedido firme.")

CHECK = [
    "Os canais de comunicação com o cliente estão definidos: informações, pedidos, mudanças e reclamações.",
    "O que a organização oferece está definido, com a especificação de cada produto ou serviço.",
    "Os requisitos legais aplicáveis ao que é oferecido estão identificados.",
    "A organização confirmou que consegue cumprir o que oferece, inclusive a capacidade.",
    "O que a organização não garante está informado ao cliente.",
    "Todo pedido é analisado antes de a organização se comprometer a fornecer.",
    "A análise considera os requisitos que o cliente não declarou, mas que o uso exige.",
    "As diferenças entre o pedido e a proposta são resolvidas antes da confirmação.",
    "O pedido verbal é confirmado com o cliente antes de ser aceito.",
    "O resultado da análise fica registrado, com quem analisou e quando.",
    "Quando o pedido muda, é analisado de novo, os documentos são atualizados e as pessoas são informadas.",
    "O pedido aceito com alteração ou recusado tem o motivo registrado e comunicado ao cliente.",
]


def nao_por_pergunta(ex):
    return [sum(1 for p in ex["peds"] if p["q"][k] == NAO) for k in range(NQ)]


def resumo(ex):
    ps = ex["peds"]
    return dict(peds=len(ps), dec={d: sum(1 for p in ps if p["dec"] == d) for d in DECISOES}, rever=sum(1 for p in ps if conf(p) != "OK"),
                com_pend=sum(1 for p in ps if pendencias(p) > 0), muds=len(ex["muds"]), mud_rever=sum(1 for m in ex["muds"] if mud_conf(m) != "OK"),
                of_rever=sum(1 for o in ex["ofertas"] if oferta_conf(o) != "OK"))


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        print("==", nome, resumo(ex), "| não por pergunta", nao_por_pergunta(ex))
        for o in ex["ofertas"]:
            print("  oferta %-28s %s" % (o["item"], oferta_conf(o)))
        for p in ex["peds"]:
            print("  %-8s %-24s %-26s %-22s %s" % (p["num"], p["dec"], leitura(p), "".join({SIM: "S", NAO: "N", NA: "-", "": "_"}[x] for x in p["q"]), conf(p)))
        for m in ex["muds"]:
            print("  mudança %-8s %s" % (m["ped"], mud_conf(m)))
