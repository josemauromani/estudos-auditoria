# -*- coding: utf-8 -*-
"""Dados do estudo de Liberação e produto não conforme, usados pelo HTML e pela planilha.

As decisões de liberação, as seis disposições, as situações de um registro e as regras de conferência são uma
convenção deste material. Os exemplos continuam os do estudo de Controle de produção e de serviço: as noites de
15 a 21/03/2027 da pizzaria e os lotes 136 a 143 da extrusora 3 da indústria, de 17 a 26/05/2027.
"""
from datetime import date

D = date
LIBERADO, AUTORIZADO, RETIDO = "Liberado", "Liberado com autorização", "Retido"
DECISOES = [LIBERADO, AUTORIZADO, RETIDO]
L_CONF, L_PEND, L_DESV = "Conforme", "Verificação pendente", "Com desvio"
RECEB, PROC, FINAL, APOS = "Recebimento", "Processo", "Inspeção final", "Após a entrega"
DET = [RECEB, PROC, FINAL, APOS]
RETRAB, RECLAS, CONCES, REFUGO, DEVOLV, RECOLH = "Retrabalhar", "Reclassificar", "Aceitar sob concessão", "Refugar", "Devolver ao fornecedor", "Recolher ou substituir"
DISP = [RETRAB, RECLAS, CONCES, REFUGO, DEVOLV, RECOLH]
R_CONF, R_NAO = "Conforme", "Não conforme"
REVERIF = [R_CONF, R_NAO]
ABERTO, TRAT, ENCER = "Aberto", "Em tratamento", "Encerrado"
SITS = [ABERTO, TRAT, ENCER]
REPETE = 3   # a partir de quantos registros do mesmo defeito a planilha pede a avaliação de uma ação corretiva
DISP_INFO = [
    (RETRAB, "Corrigir o produto para que volte a atender ao requisito.", "O defeito pode ser corrigido, e a correção custa menos do que refazer.", "Verificar de novo depois da correção.",
     "Reaquecer a pizza. Refilar a bobina larga."),
    (RECLAS, "Destinar o produto a outro uso, em que ele atende ao requisito.", "O produto não serve para este cliente, e serve para outro uso ou outra classe.", "Identificar de novo, com a nova classe.",
     "Filme espesso vendido como segunda linha."),
    (CONCES, "Entregar o produto como está, com a autorização de quem pode aceitar.", "O desvio não afeta o uso, e o cliente concorda em receber.", "A autorização do cliente, por escrito, antes da entrega.",
     "Bobinas com 43 µm aceitas pelo cliente B."),
    (REFUGO, "Descartar o produto, ou destruí-lo para reaproveitar o material.", "Não há correção possível, ou ela custa mais do que refazer.", "Garantir que o produto não volte ao fluxo.",
     "Pizza com o sabor trocado. Bobina com géis, moída."),
    (DEVOLV, "Devolver o item recebido a quem o forneceu.", "O defeito veio no insumo, e foi visto no recebimento ou antes do uso.", "Registrar a ocorrência na avaliação do fornecedor.",
     "Muçarela recebida a 9 °C."),
    (RECOLH, "Buscar o produto que já está com o cliente, trocar ou reparar.", "O defeito foi encontrado depois da entrega.", "Informar o cliente, sem esperar a reclamação.",
     "Pedido entregue com o sabor errado."),
]
ETAPAS = [
    ("Definir quem libera", "Os critérios de aceitação, as verificações e quem tem autoridade para liberar."),
    ("Verificar e liberar", "Conferir as verificações planejadas e registrar quem liberou."),
    ("Identificar e segregar", "O que não atende recebe uma marca e sai do fluxo, para não ser entregue."),
    ("Decidir a disposição", "Quem tem autoridade escolhe uma das seis disposições."),
    ("Verificar e registrar", "O que foi corrigido é verificado de novo. O registro guarda o defeito e quem decidiu."),
]


def lib_leitura(l):
    if l["feitas"] < l["prev"]:
        return L_PEND
    return L_DESV if l["fora"] else L_CONF


def lib_conf(l):
    """Conferência de uma liberação: a mesma regra da planilha."""
    if l["feitas"] < l["prev"] and l["dec"] == LIBERADO:
        return "Liberado com verificação pendente"
    if l["dec"] == AUTORIZADO and not l["aut"]:
        return "Falta quem autorizou"
    if l["fora"] and not l["pnc"]:
        return "Desvio sem registro de não conforme"
    if l["dec"] == RETIDO and not l["pnc"]:
        return "Retido sem registro de não conforme"
    if l["dec"] != RETIDO and not l["quem"]:
        return "Falta quem liberou"
    return "OK"


def pnc_sit(r):
    if not r["disp"]:
        return ABERTO
    return ENCER if r["enc"] else TRAT


def repeticoes(r, regs):
    return sum(1 for x in regs if x["defeito"] == r["defeito"])


def pnc_conf(r, regs):
    """Conferência de um registro de produto não conforme: a mesma regra da planilha."""
    if not r["disp"]:
        return "Falta a disposição"
    if not r["quem"]:
        return "Falta quem decidiu"
    if not r["seg"] and r["det"] != APOS:
        return "Falta a identificação e a segregação"
    if r["disp"] == CONCES and not r["cliente"]:
        return "Falta a concessão do cliente"
    if r["det"] == APOS and not r["cliente"]:
        return "Falta informar o cliente"
    if r["disp"] == RETRAB and not r["rev"]:
        return "Falta a reverificação"
    if r["rev"] == R_NAO and r["enc"]:
        return "Encerrado com reverificação não conforme"
    if repeticoes(r, regs) >= REPETE and not any(x["acao"] for x in regs if x["defeito"] == r["defeito"]):
        return "Defeito repetido: avaliar ação corretiva"
    return "OK"


def _libs(rows):
    keys = ("data", "lote", "prod", "prev", "feitas", "fora", "dec", "quem", "aut", "pnc", "obs")
    out = [dict(zip(keys, r)) for r in rows]
    for l in out:
        assert l["dec"] in DECISOES and l["feitas"] <= l["prev"], l["lote"]
    return out


def _pncs(rows):
    keys = ("num", "data", "lote", "defeito", "desc", "qtd", "det", "seg", "disp", "quem", "cliente", "rev", "enc", "custo", "acao")
    out = [dict(zip(keys, r)) for r in rows]
    for r in out:
        assert r["det"] in DET and (r["disp"] in DISP or not r["disp"]) and (r["rev"] in REVERIF or not r["rev"]), r["num"]
        assert r["enc"] is None or r["enc"] >= r["data"], r["num"]
    return out


# ------------------------------------------------------------ exemplo 1: pizzaria, noites de 15 a 21/03/2027
_LE = "Líder da expedição"
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", processo="Produzir e embalar (P2) e Entregar o pedido (P3)", produto="Pizza entregue em casa e servida no salão",
                 libera="Cada pedido: quem embala, com a rubrica na etiqueta. O fechamento da noite: líder da expedição.",
                 decide="Pizzaiolo líder e líder da expedição, no turno. Gerente da loja, para descarte de insumos, concessão e troca no cliente.",
                 periodo="Noites de 15 a 21/03/2027", ref=D(2027, 3, 22), origem="Requisito 8.7 atendido em parte no diagnóstico de 2026: a pizza errada era refeita, sem registro."),
    "libs": _libs([
        (D(2027, 3, 15), "Noite 15/03", "142 pedidos", 8, 8, 0, LIBERADO, _LE, "", "", ""),
        (D(2027, 3, 16), "Noite 16/03", "118 pedidos", 8, 8, 1, LIBERADO, _LE, "", "2027-15", ""),
        (D(2027, 3, 17), "Noite 17/03", "125 pedidos", 8, 8, 0, LIBERADO, _LE, "", "", ""),
        (D(2027, 3, 18), "Noite 18/03", "131 pedidos", 8, 8, 1, LIBERADO, _LE, "", "2027-17", ""),
        (D(2027, 3, 19), "Noite 19/03", "214 pedidos", 8, 8, 2, LIBERADO, _LE, "", "2027-18 e 2027-19", ""),
        (D(2027, 3, 20), "Noite 20/03", "236 pedidos", 8, 7, 1, LIBERADO, _LE, "", "2027-21", "A temperatura na saída não foi medida na última hora do pico."),
        (D(2027, 3, 21), "Noite 21/03", "160 pedidos", 8, 8, 0, LIBERADO, _LE, "", "", ""),
    ]),
    "pncs": _pncs([
        ("2027-14", D(2027, 3, 15), "Noite 13/03, pedido das 21h", "Pizza fria na saída", "Pizza a 62 °C na saída, registrada sem reação no plano de controle. Vista na leitura de 15/03: já tinha sido entregue.",
         "1 pizza", FINAL, "", "", "", "", "", None, None, ""),
        ("2027-15", D(2027, 3, 16), "Pedido 5127", "Sabor trocado", "Pizza de calabresa montada no lugar da portuguesa. Vista na conferência com a etiqueta.",
         "1 pizza", FINAL, "Retirada da bancada de saída.", REFUGO, "Pizzaiolo líder", "", "", D(2027, 3, 16), 28, ""),
        ("2027-16", D(2027, 3, 17), "Muçarela, nota de 17/03", "Insumo fora de temperatura", "Muçarela recebida a 9 °C, com o critério de até 7 °C.",
         "12 kg", RECEB, "Não entrou na câmara. Ficou na área de recebimento, com etiqueta vermelha.", DEVOLV, "Gerente da loja", "", "", D(2027, 3, 17), 0, ""),
        ("2027-17", D(2027, 3, 18), "Massa 18/03", "Peso da massa fora", "Bolas de massa com 365 g em média, com o critério de 380 a 420 g.",
         "40 bolas", PROC, "Caixa do lote com etiqueta vermelha.", RETRAB, "Pizzaiolo líder", "", R_CONF, D(2027, 3, 18), 0, ""),
        ("2027-18", D(2027, 3, 19), "Pedido 5342, mesa 7", "Borda queimada", "Pizza com a borda escura de um lado, vista ao servir no salão.",
         "1 pizza", FINAL, "Mostrada ao cliente antes de servir.", CONCES, "Gerente da loja", "Cliente da mesa 7 aceitou, com desconto de 20%, em 19/03.", "", D(2027, 3, 19), 11, ""),
        ("2027-19", D(2027, 3, 19), "Pedido 5360", "Pizza fria na saída", "Pizza a 61 °C na saída, depois de 13 minutos de espera.",
         "1 pizza", FINAL, "Voltou da bancada de saída para o forno.", RETRAB, _LE, "", R_CONF, D(2027, 3, 19), 0, ""),
        ("2027-20", D(2027, 3, 20), "Pedido 5431", "Sabor trocado", "Cliente recebeu meia muçarela no lugar de meia marguerita. Avisou pelo aplicativo.",
         "1 pizza", APOS, "", RECOLH, "Gerente da loja", "Cliente atendido em 20/03: pizza nova entregue em 35 minutos.", "", D(2027, 3, 20), 46, ""),
        ("2027-21", D(2027, 3, 20), "Pedido 5440", "Sabor trocado", "Pizza de frango montada no lugar da de atum. Vista na conferência com a etiqueta.",
         "1 pizza", FINAL, "Retirada da bancada de saída.", REFUGO, "Pizzaiolo líder", "", "", D(2027, 3, 20), 28, "RNC 2027-03"),
    ]),
}

# ------------------------------------------------------------ exemplo 2: indústria, lotes 136 a 143
_AQ = "Analista da Qualidade"
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", processo="Extrusão, na extrusora 3, e inspeção final", produto="Filme de 40 µm para clientes do segmento de alimentos",
                 libera="Analista da Qualidade, com o laudo do lote. Liberação com verificação pendente: só com a autorização do gerente industrial e o aceite do cliente.",
                 decide="Coordenador da Qualidade. Retrabalho na linha: líder do turno. Devolução de insumo ao fornecedor: gerente de Suprimentos. "
                        "Refugo acima de 500 kg e recolhimento no cliente: gerente industrial e gerente comercial.",
                 periodo="Lotes 136 a 143, de 17 a 26/05/2027", ref=D(2027, 5, 28), origem="Reclamações do cliente A e o objetivo O1: reduzir o refugo para 2,0%."),
    "libs": _libs([
        (D(2027, 5, 17), "Lote 136", "4 bobinas, 1.210 kg", 12, 12, 0, LIBERADO, _AQ, "", "", ""),
        (D(2027, 5, 18), "Lote 137", "4 bobinas, 1.180 kg", 12, 12, 1, LIBERADO, _AQ, "", "2027-20", "Bobina 3 segregada. As outras três foram liberadas."),
        (D(2027, 5, 19), "Lote 138", "4 bobinas, 1.225 kg", 12, 12, 0, LIBERADO, _AQ, "", "", ""),
        (D(2027, 5, 20), "Lote 139", "4 bobinas, 1.190 kg", 12, 11, 0, AUTORIZADO, _AQ, "Gerente industrial, com o aceite do cliente A por e-mail.", "",
         "Ensaio de solda pendente: dinamômetro em calibração. Feito em 21/05, conforme."),
        (D(2027, 5, 20), "Lote 140", "2 bobinas, 600 kg", 12, 12, 2, RETIDO, _AQ, "", "2027-21",
         "Espessura acima do critério nas duas bobinas. Retido em 20/05; liberado em 21/05, com a concessão do cliente B."),
        (D(2027, 5, 21), "Lote 141", "4 bobinas, 1.205 kg", 12, 12, 0, LIBERADO, _AQ, "", "", ""),
        (D(2027, 5, 24), "Lote 142", "4 bobinas, 1.215 kg", 12, 11, 0, LIBERADO, _AQ, "", "", "Ensaio de solda na fila do laboratório. Lote embarcado no mesmo dia."),
        (D(2027, 5, 26), "Lote 143", "4 bobinas, 1.200 kg", 12, 12, 1, LIBERADO, _AQ, "", "2027-24", "Bobina 1 segregada para refilar."),
    ]),
    "pncs": _pncs([
        ("2027-17", D(2027, 5, 11), "Lote 132, bobina 2", "Géis", "Géis visíveis, comparados com o padrão de defeitos do posto.",
         "290 kg", PROC, "Etiqueta vermelha. Área de segregação da extrusão.", REFUGO, "Coordenador da Qualidade", "", "", D(2027, 5, 12), 580, ""),
        ("2027-18", D(2027, 5, 12), "Lote 133, bobina 1", "Espessura fora", "Espessura de 42,6 µm, com o critério de 38 a 42 µm.",
         "310 kg", PROC, "Etiqueta vermelha. Área de segregação da extrusão.", RECLAS, "Coordenador da Qualidade", "", "", D(2027, 5, 14), 620, "Ciclo PDCA do refugo"),
        ("2027-19", D(2027, 5, 14), "Lote 135, bobina 1", "Espessura fora", "Espessura de 37,4 µm, na primeira bobina da produção regular com a resina do segundo fornecedor.",
         "305 kg", PROC, "Etiqueta vermelha. Área de segregação da extrusão.", REFUGO, "Coordenador da Qualidade", "", "", D(2027, 5, 17), 610, ""),
        ("2027-20", D(2027, 5, 18), "Lote 137, bobina 3", "Géis", "Géis visíveis depois da troca da tela do filtro.",
         "280 kg", PROC, "Etiqueta vermelha. Área de segregação da extrusão.", REFUGO, "Coordenador da Qualidade", "", "", D(2027, 5, 19), 560, ""),
        ("2027-21", D(2027, 5, 20), "Lote 140, duas bobinas", "Espessura fora", "Espessura de 43,1 e 43,4 µm, vista na inspeção final.",
         "600 kg", FINAL, "Lote retido no armazém, com etiqueta vermelha no palete.", CONCES, "Coordenador da Qualidade", "Cliente B aceitou até 44 µm, por e-mail de 21/05, com desconto de 15%.", "",
         D(2027, 5, 21), 1350, ""),
        ("2027-22", D(2027, 5, 24), "Lote 135, bobina 2", "Espessura fora", "Cliente A reclamou de filme fino. Primeira resposta, em 24/05: 39,1 µm na liberação. Medida no laboratório em 26/05, com o MIC-08: trechos com 37,9 µm.",
         "300 kg", APOS, "", RECOLH, "Gerente industrial e gerente comercial", "Cliente A informado em 24/05. Bobina recolhida e reposta em 26/05.", "", None, 2900, ""),
        ("2027-23", D(2027, 5, 25), "Resina, lote R-0440", "Resina úmida", "Sacaria molhada no recebimento. Umidade acima do limite da ficha técnica.",
         "2.000 kg", RECEB, "Etiqueta vermelha no almoxarifado. Não entrou no estoque.", DEVOLV, "Gerente de Suprimentos", "", "", D(2027, 5, 27), 0, ""),
        ("2027-24", D(2027, 5, 26), "Lote 143, bobina 1", "Largura fora", "Largura de 603 mm, com o critério de 598 a 602 mm.",
         "300 kg", PROC, "Etiqueta vermelha. Ao lado da refiladeira.", RETRAB, "Líder do turno", "", "", None, 150, ""),
        ("2027-25", D(2027, 5, 26), "Lote 142", "Solda fraca", "Resistência da solda de 11,2 N/15 mm, com o critério de no mínimo 12. Ensaio feito dois dias depois do embarque.",
         "1.215 kg", APOS, "", RECOLH, "Gerente industrial e gerente comercial", "", "", None, 3400, ""),
    ]),
}

# exemplo 3: duas liberações com verificação pendente (só no treinamento)
DUAS = dict(
    a=dict(tit="Lote 139 · liberado com autorização", passos=[
        ("20/05", "Ensaio de solda pendente", "O dinamômetro está em calibração. As outras 11 verificações estão conformes."),
        ("20/05", "Autorização antes de liberar", "O gerente industrial autoriza, e o cliente A aceita por e-mail. O lote sai identificado."),
        ("21/05", "Ensaio feito: conforme", "O resultado entra no laudo. O registro de liberação é fechado."),
        ("Resultado", "Nenhum custo", "Se o ensaio reprovasse, o cliente já sabia que lote separar.")]),
    b=dict(tit="Lote 142 · liberado com verificação pendente", passos=[
        ("24/05", "Ensaio de solda pendente", "A amostra está na fila do laboratório. As outras 11 verificações estão conformes."),
        ("24/05", "Liberado e embarcado", "Ninguém autorizou, e o cliente não foi avisado."),
        ("26/05", "Ensaio feito: não conforme", "Solda de 11,2 N/15 mm. O lote já está no cliente."),
        ("Resultado", "R$ 3.400 e o cliente a informar", "Recolher 1.215 kg, repor e explicar. O registro 2027-25 segue em tratamento.")]),
    conclusao="A verificação pendente era a mesma. A diferença foi a autorização: ela não evita o defeito, e sim a surpresa.")

CHECK = [
    "Cada produto tem critérios de aceitação escritos e as verificações que precisam estar feitas antes da liberação.",
    "Está definido quem tem autoridade para liberar, e o registro de liberação traz esse nome.",
    "Nenhum produto sai com verificação pendente sem a autorização de quem pode autorizar e, quando aplicável, do cliente.",
    "O produto não conforme é identificado assim que é encontrado.",
    "O produto não conforme é separado do fluxo, para não ser usado nem entregue por engano.",
    "Está definido quem pode decidir cada disposição: retrabalhar, reclassificar, conceder, refugar, devolver ou recolher.",
    "O produto retrabalhado é verificado de novo antes de seguir.",
    "A concessão tem a autorização do cliente registrada, antes da entrega.",
    "O defeito encontrado depois da entrega é comunicado ao cliente, sem esperar a reclamação.",
    "Cada registro descreve o defeito, a ação tomada, a concessão obtida e quem decidiu.",
    "Os registros abertos são lidos toda semana, e nenhum fica sem disposição.",
    "O defeito que se repete leva à análise de causa, no tratamento de não conformidades.",
]


def por_det(ex):
    """Por ponto de detecção: registros, custo e custo por registro."""
    out = []
    for d in DET:
        rs = [r for r in ex["pncs"] if r["det"] == d]
        c = sum(r["custo"] or 0 for r in rs)
        out.append(dict(det=d, n=len(rs), custo=c, medio=c / len(rs) if rs else None))
    return out


def resumo(ex):
    libs, pncs = ex["libs"], ex["pncs"]
    sits = [pnc_sit(r) for r in pncs]
    return dict(libs=len(libs), conf=sum(1 for l in libs if l["dec"] == LIBERADO and lib_leitura(l) == L_CONF), aut=sum(1 for l in libs if l["dec"] == AUTORIZADO),
                ret=sum(1 for l in libs if l["dec"] == RETIDO), lib_rever=sum(1 for l in libs if lib_conf(l) != "OK"),
                pncs=len(pncs), sits={s: sits.count(s) for s in SITS}, custo=sum(r["custo"] or 0 for r in pncs), pnc_rever=sum(1 for r in pncs if pnc_conf(r, pncs) != "OK"),
                apos=sum(1 for r in pncs if r["det"] == APOS))


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        print("==", nome, resumo(ex))
        for l in ex["libs"]:
            print("  %-12s %2d/%2d fora %d %-26s %-22s %s" % (l["lote"], l["feitas"], l["prev"], l["fora"], l["dec"], lib_leitura(l), lib_conf(l)))
        for r in ex["pncs"]:
            print("  %s %-28s %-15s %-24s %-14s x%d %s" % (r["num"], r["defeito"], r["det"], r["disp"] or "—", pnc_sit(r), repeticoes(r, ex["pncs"]), pnc_conf(r, ex["pncs"])))
        print("  ", [(x["det"], x["n"], x["custo"], x["medio"]) for x in por_det(ex)])
