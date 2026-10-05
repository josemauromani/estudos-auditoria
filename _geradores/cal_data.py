# -*- coding: utf-8 -*-
"""Dados do estudo de Calibração e recursos de medição, usados pelo HTML e pela planilha.

A regra de adequação (resolução de até um décimo da tolerância), o critério de aprovação (erro mais incerteza dentro
do erro máximo admissível), as situações e as regras de conferência são uma convenção deste material. Os exemplos
continuam os dos outros estudos da série: os instrumentos da pizzaria em março de 2027 e os da indústria em junho de 2027.
"""
import calendar
from datetime import date

D = date
CALEXT, VERINT = "Calibração externa", "Verificação interna"
TIPOS = [CALEXT, VERINT]
CAL, VER = "Calibração", "Verificação"
TIPOS_REG = [CAL, VER]
SIM, NAO = "Sim", "Não"
EMDIA, VENCE, VENCIDO, SEMCAL, FORA = "Em dia", "Vence em 30 dias", "Vencido", "Sem calibração", "Fora de uso"
SITS = [EMDIA, VENCE, VENCIDO, SEMCAL, FORA]
ADEQ, GROSSA = "Adequado", "Resolução grossa"
APROV, REPROV = "Aprovado", "Reprovado"
RAZAO = 10   # a resolução deve caber ao menos dez vezes na tolerância
JANELA = 30  # dias de antecedência para o aviso de vencimento
ETAPAS = [
    ("Listar o que se mede", "Cada medição que decide se o produto está conforme, e o instrumento que a faz."),
    ("Escolher o instrumento", "Faixa, resolução e método adequados à tolerância do que se mede."),
    ("Calibrar ou verificar", "Contra padrão rastreável, no intervalo definido, com o erro máximo admissível."),
    ("Identificar e proteger", "Etiqueta com a situação. Proteção contra queda, ajuste indevido e desgaste."),
    ("Ler e reagir", "Ler o certificado. Reprovado: bloquear, corrigir e rever o que foi medido antes."),
]
CADEIA = [
    ("Padrão internacional", "Define a unidade de medida."),
    ("Instituto nacional de metrologia", "Mantém o padrão nacional do país."),
    ("Laboratório acreditado", "Calibra os padrões e os instrumentos das empresas, com incerteza declarada."),
    ("Padrão da organização", "Termômetro padrão, peso-padrão, bloco-padrão."),
    ("Instrumento do posto", "Mede o produto, todos os dias."),
]


def add_meses(d, m):
    """Soma meses a uma data, como a função EDATE das planilhas."""
    y, mo = divmod(d.month - 1 + m, 12)
    y, mo = d.year + y, mo + 1
    return date(y, mo, min(d.day, calendar.monthrange(y, mo)[1]))


def proxima(i):
    return add_meses(i["ultima"], i["interv"]) if i["ultima"] and i["interv"] else None


def situacao(i, ref):
    if i["emuso"] == NAO:
        return FORA
    if not i["ultima"]:
        return SEMCAL
    p = proxima(i)
    if p < ref:
        return VENCIDO
    if (p - ref).days <= JANELA:
        return VENCE
    return EMDIA


def adequacao(i):
    if i["tol"] is None or i["res"] is None:
        return ""
    return ADEQ if i["res"] <= i["tol"] / RAZAO + 1e-9 else GROSSA


def inst_conf(i, ref):
    """Conferência de um instrumento: a mesma regra da planilha."""
    if not i["uso"]:
        return "Falta o que mede"
    if not i["tipo"]:
        return "Falta o tipo de controle"
    if not i["interv"]:
        return "Falta o intervalo"
    if i["ema"] is None:
        return "Falta o erro máximo admissível"
    s = situacao(i, ref)
    if s == FORA:
        return FORA
    if s == VENCIDO:
        return "Vencido: bloquear ou calibrar"
    if s == SEMCAL:
        return "Sem calibração ou verificação"
    if adequacao(i) == GROSSA:
        return "Resolução grossa para a tolerância"
    return "OK"


def resultado(c, insts):
    i = {x["cod"]: x for x in insts}.get(c["cod"])
    if not i or c["erro"] is None:
        return ""
    return APROV if abs(c["erro"]) + (c["inc"] or 0) <= i["ema"] + 1e-9 else REPROV


def cal_conf(c, insts):
    if c["cod"] not in {x["cod"] for x in insts}:
        return "Instrumento não cadastrado"
    if not c["reg"]:
        return "Falta o registro"
    if c["erro"] is None:
        return "Falta o erro encontrado"
    if resultado(c, insts) == REPROV:
        if not c["acao"]:
            return "Falta a ação"
        if not c["impacto"]:
            return "Falta avaliar os resultados anteriores"
    return "OK"


def _insts(rows):
    keys = ("cod", "nome", "local", "uso", "unid", "tol", "res", "tipo", "interv", "ultima", "ema", "emuso")
    out = [dict(zip(keys, r)) for r in rows]
    for i in out:
        assert i["tipo"] in TIPOS and i["emuso"] in (SIM, NAO), i["cod"]
    return out


def _cals(rows):
    out = [dict(zip(("data", "cod", "tipo", "reg", "ponto", "erro", "inc", "acao", "impacto"), r)) for r in rows]
    for c in out:
        assert c["tipo"] in TIPOS_REG, c["cod"]
    return out


# ------------------------------------------------------------ exemplo 1: pizzaria, março de 2027
_PL, _GL = "Pizzaiolo líder", "Gerente da loja"
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", resp="Pizzaiolo líder, com o gerente da loja", ref=D(2027, 3, 31),
                 padrao="Termômetro de espeto TER-01, verificado em água com gelo, e peso-padrão de 500 g, calibrado por laboratório externo.",
                 origem="Requisito 7.1.5 atendido em parte no diagnóstico de 2026: a balança era verificada todo mês, e o termômetro da câmara fria, nunca."),
    "insts": _insts([
        ("TER-01", "Termômetro de espeto", "Expedição", "Temperatura da pizza na saída: no mínimo 65 °C", "°C", 5, 0.1, VERINT, 1, D(2027, 3, 5), 1, SIM),
        ("TER-02", "Termômetro de visor da câmara fria", "Câmara fria", "Temperatura da câmara: 0 a 5 °C", "°C", 5, 0.1, VERINT, 3, D(2027, 3, 15), 1, NAO),
        ("TER-03", "Termômetro do forno", "Forno", "Temperatura do forno: 280 a 320 °C", "°C", 40, 1, CALEXT, 12, D(2026, 6, 15), 5, SIM),
        ("TER-04", "Termômetro de espeto do recebimento", "Recebimento", "Temperatura dos insumos refrigerados: até 7 °C", "°C", 2, 0.1, VERINT, 1, None, 1, SIM),
        ("BAL-01", "Balança da bancada", "Produção", "Peso da bola de massa: 380 a 420 g", "g", 40, 1, VERINT, 1, D(2027, 3, 1), 2, SIM),
        ("BAL-02", "Balança do recebimento", "Recebimento", "Peso dos insumos recebidos", "g", 200, 5, CALEXT, 12, D(2027, 1, 20), 10, SIM),
    ]),
    "cals": _cals([
        (D(2027, 1, 20), "BAL-02", CAL, "Certificado 0187/27, laboratório acreditado", "10 kg", 5, 3, "", ""),
        (D(2027, 3, 1), "BAL-01", VER, "Planilha de verificação FR-07", "Peso-padrão de 500 g", 1, 0.5, "", ""),
        (D(2027, 3, 5), "TER-01", VER, "Planilha de verificação FR-07", "Água com gelo, 0 °C", 0.3, 0.2, "", ""),
        (D(2027, 3, 15), "TER-02", VER, "Planilha de verificação FR-07", "Contra o TER-01, a 5 °C", -2.0, 0.3,
         "Retirado da câmara. Um termômetro novo, verificado contra o TER-01, foi instalado no lugar.", ""),
        (D(2026, 6, 15), "TER-03", CAL, "Certificado 1442/26, laboratório acreditado", "300 °C", -3, 1.5, "", ""),
    ]),
}

# ------------------------------------------------------------ exemplo 2: indústria, junho de 2027
_LAB, _AQ = "Laboratório", "Analista da Qualidade"
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", resp="Analista da Qualidade, com o Laboratório", ref=D(2027, 6, 30),
                 padrao="Termômetro padrão PAD-01 e blocos-padrão de espessura, calibrados por laboratório acreditado.",
                 origem="Auditoria interna de 2026: 3 de 25 instrumentos em uso com a calibração vencida (GUT e Ishikawa da série)."),
    "insts": _insts([
        ("MIC-07", "Micrômetro de ponta plana", "Extrusora 3", "Espessura do filme: 38 a 42 µm", "µm", 4, 1, CALEXT, 6, D(2027, 6, 12), 1, NAO),
        ("MIC-08", "Micrômetro digital", "Laboratório", "Espessura do filme: 38 a 42 µm", "µm", 4, 0.1, CALEXT, 6, D(2027, 3, 15), 0.5, SIM),
        ("TR-03", "Trena digital", "Extrusora 3", "Largura do filme: 598 a 602 mm", "mm", 4, 0.1, CALEXT, 12, D(2026, 11, 8), 0.3, SIM),
        ("TER-Z3", "Termopar da zona 3", "Extrusora 3", "Temperatura da zona 3: 185 a 195 °C", "°C", 10, 1, CALEXT, 12, D(2026, 8, 2), 2, SIM),
        ("DIN-01", "Dinamômetro", "Laboratório", "Resistência da solda: no mínimo 12 N/15 mm", "N", 2, 0.01, CALEXT, 12, D(2027, 5, 21), 0.2, SIM),
        ("TER-L1", "Termômetro da câmara de condicionamento", "Laboratório", "Temperatura do ensaio a -18 °C, com ±2 °C", "°C", 4, 0.1, VERINT, 3, D(2027, 3, 15), 1, SIM),
        ("PAD-01", "Termômetro padrão", "Laboratório", "Referência das verificações internas", "°C", None, 0.01, CALEXT, 12, D(2027, 2, 10), 0.1, SIM),
    ]),
    "cals": _cals([
        (D(2026, 8, 2), "TER-Z3", CAL, "Certificado T-2026-0802, laboratório acreditado", "190 °C", 1.2, 0.5, "", ""),
        (D(2026, 11, 8), "TR-03", CAL, "Certificado D-2026-1108, laboratório acreditado", "600 mm", 0.1, 0.05, "", ""),
        (D(2027, 1, 10), "MIC-07", CAL, "Certificado C-2027-0112, laboratório acreditado", "40 µm", 0.6, 0.3, "", ""),
        (D(2027, 2, 10), "PAD-01", CAL, "Certificado P-2027-0210, laboratório acreditado", "-18 °C e 20 °C", 0.02, 0.03, "", ""),
        (D(2027, 3, 15), "MIC-08", CAL, "Certificado C-2027-0315, laboratório acreditado", "40 µm", 0.1, 0.08, "", ""),
        (D(2027, 3, 15), "TER-L1", VER, "Registro de verificação FV-09", "Contra o PAD-01, a -18 °C", 0.4, 0.1, "", ""),
        (D(2027, 5, 21), "DIN-01", CAL, "Certificado F-2027-0521, laboratório acreditado", "15 N", 0.15, 0.05, "", ""),
        (D(2027, 6, 12), "MIC-07", VER, "Registro de verificação FV-12", "Bloco-padrão de 40 µm", 1.6, 0.2,
         "Retirado do posto. O MIC-08 mede as bobinas até a reposição, e um micrômetro de 0,1 µm foi comprado.",
         "Medições de 10/01 a 12/06 corrigidas em 1,6 µm: 6 bobinas abaixo de 38 µm, 2 delas já entregues, inclusive a do lote 135. Clientes informados em 14/06."),
    ]),
}

# exemplo 3: a avaliação dos resultados anteriores (só no treinamento)
IMPACTO = [
    ("10/01", "Última calibração aprovada", "Erro de +0,6 µm, dentro do critério de ±1 µm."),
    ("Até 12/06", "Cinco meses de medições", "Cerca de 1.200 bobinas medidas no posto da extrusora 3."),
    ("24 e 26/05", "Reclamação do cliente A", "Lote 135. Primeira resposta: 39,1 µm na liberação. Em 26/05, o MIC-08 mede trechos com 37,9 µm."),
    ("12/06", "Verificação reprovada", "O micrômetro marca 1,6 µm a mais. A bobina de 39,1 µm tinha, na verdade, 37,5 µm."),
    ("14/06", "Avaliação e ação", "Medições corrigidas desde 10/01. 6 bobinas abaixo de 38 µm, 2 entregues. Clientes informados."),
]

CHECK = [
    "Os instrumentos que verificam a conformidade do produto estão listados, com código e local.",
    "Cada instrumento é adequado ao que mede: faixa, resolução e método.",
    "Para cada instrumento está definido se é calibrado, verificado ou os dois, e com que intervalo.",
    "A calibração é rastreável a padrões nacionais ou internacionais, feita por laboratório competente.",
    "Quando não há padrão, o método de verificação está registrado.",
    "Cada instrumento tem o critério de aceitação: o erro máximo admissível.",
    "O certificado é lido: o erro e a incerteza são comparados com o critério, e o resultado é registrado.",
    "Cada instrumento está identificado com a situação: em dia, vencido, fora de uso.",
    "Os instrumentos são protegidos de ajustes, quedas e danos que invalidem a calibração.",
    "Instrumento vencido ou reprovado é bloqueado até a nova calibração.",
    "Quando um instrumento é reprovado, os resultados anteriores são avaliados, e o que foi afetado é tratado.",
    "Os registros de calibração e de verificação estão guardados.",
]


def resumo(ex):
    ref, insts, cals = ex["head"]["ref"], ex["insts"], ex["cals"]
    sits = [situacao(i, ref) for i in insts]
    return dict(insts=len(insts), sits={s: sits.count(s) for s in SITS}, grossa=sum(1 for i in insts if adequacao(i) == GROSSA),
                inst_rever=sum(1 for i in insts if inst_conf(i, ref) not in ("OK", FORA)), cals=len(cals), reprov=sum(1 for c in cals if resultado(c, insts) == REPROV),
                cal_rever=sum(1 for c in cals if cal_conf(c, insts) != "OK"))


if __name__ == "__main__":
    for nome, ex in (("pizzaria", EX1), ("indústria", EX2)):
        ref = ex["head"]["ref"]
        print("==", nome, resumo(ex))
        for i in ex["insts"]:
            print("  %-7s %-40s próxima %-11s %-17s %-17s %s" % (i["cod"], i["nome"], proxima(i), situacao(i, ref), adequacao(i), inst_conf(i, ref)))
        for c in ex["cals"]:
            print("  %s %-7s %-12s %-10s %s" % (c["data"], c["cod"], c["tipo"], resultado(c, ex["insts"]), cal_conf(c, ex["insts"])))
