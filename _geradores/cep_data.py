# -*- coding: utf-8 -*-
"""Dados do estudo Histograma e CEP, usados pelo HTML e pela planilha.

O gráfico de controle é o de média e amplitude (X̄-R), com subgrupos de cinco medições e as constantes de Shewhart para
n = 5. As três regras de sinal (ponto fora dos limites, sete pontos do mesmo lado, seis pontos subindo ou descendo), a
classificação da capacidade e as classes do histograma são uma convenção deste material, próxima das usuais. Os exemplos
continuam os dos outros estudos: o peso da bola de massa da pizzaria (critério de 380 a 420 g no plano de controle), de
22/03 a 15/04/2027, depois do registro de produto não conforme 2027-17; e a espessura do filme da extrusora 3 da
indústria (38 a 42 µm), de 04 a 16/07/2027, os dias antes da parada de 18/07 pela rosca desgastada (registro de produto não conforme 2027-30).
"""
from datetime import date, timedelta
from statistics import mean

D = date
N = 5
A2, D3, D4, D2 = 0.577, 0, 2.114, 2.326
SIM = "Sim"
BASE, EXCL, ACOMP = "Base", "Excluído", "Acompanhamento"
S_FORA, S_AMP, S_LADO, S_TEND = "Média fora dos limites", "Amplitude fora do limite", "7 do mesmo lado", "6 subindo ou descendo"
SINAIS = [S_FORA, S_AMP, S_LADO, S_TEND]
LADO, TEND = 7, 6
SEP = "; "  # separa os sinais de um mesmo subgrupo na coluna Sinal
CAPAZ, LIMITE, NAOCAPAZ = "Capaz", "No limite", "Não capaz"
CPK_BOM, CPK_MIN = 1.33, 1.0
NCLASSES = 12

# as partes do gráfico de controle, para a figura e o glossário
PARTES = [
    ("Linha central", "A média das médias dos subgrupos da base. É onde o processo costuma ficar."),
    ("Limites de controle", "A linha central mais e menos três desvios-padrão das médias, σ ÷ √n. Vêm dos dados, não do cliente."),
    ("Subgrupo", "Cinco medições feitas juntas, nas mesmas condições: as cinco bolas de um lote, os cinco pontos de uma bobina."),
    ("Amplitude", "A maior menos a menor medição do subgrupo. Mostra a variação de dentro do subgrupo."),
]
ETAPAS = [
    ("Escolher o que medir", "Uma característica que pesa para o cliente, com critério e instrumento adequado."),
    ("Montar os subgrupos", "Cinco medições nas mesmas condições, em intervalos que deixem a mudança aparecer."),
    ("Calcular a base", "20 a 25 subgrupos sem causa conhecida: linha central e limites."),
    ("Acompanhar", "Cada subgrupo novo no gráfico, lido na hora, com as quatro regras."),
    ("Reagir e melhorar", "Sinal pede causa e ação. Sem sinal e sem capacidade, quem muda é o processo."),
]
# formas do histograma: nome, o que sugere, perfil da figura (alturas relativas de 9 barras)
FORMAS = [
    ("Sino", "Variação comum, de muitas causas pequenas.", [1, 2, 4, 7, 9, 7, 4, 2, 1]),
    ("Deslocado", "O centro saiu do alvo: ajuste ou desgaste.", [0, 0, 1, 2, 4, 7, 9, 6, 3]),
    ("Largo", "Muita variação: o processo não cabe na tolerância.", [3, 4, 5, 6, 6, 6, 5, 4, 3]),
    ("Dois picos", "Duas origens misturadas: turnos, máquinas, lotes.", [1, 4, 7, 4, 2, 4, 7, 4, 1]),
    ("Cortado", "Valores fora foram retirados ou medidos de novo.", [0, 0, 2, 9, 8, 6, 4, 2, 1]),
    ("Ilha", "Um grupo à parte: um lote, um dia ou um erro de registro.", [1, 3, 6, 8, 6, 3, 0, 0, 2]),
]
REGRAS = [
    (S_FORA, "Uma média acima do limite superior ou abaixo do inferior."),
    (S_AMP, "Uma amplitude acima do limite: um subgrupo com variação demais por dentro."),
    (S_LADO, "Sete médias seguidas acima da linha central, ou sete abaixo."),
    (S_TEND, "Seis médias seguidas, cada uma maior que a anterior, ou cada uma menor."),
]
CHECK = [
    "A característica medida pesa para o cliente e tem critério escrito.",
    "O instrumento tem resolução de no máximo um décimo da tolerância e está calibrado ou verificado.",
    "Cada subgrupo tem cinco medições feitas nas mesmas condições.",
    "A base tem pelo menos 20 subgrupos.",
    "Os subgrupos com causa conhecida foram excluídos da base, com o motivo escrito.",
    "Os limites de controle vêm dos dados, e não da especificação.",
    "Os limites ficam fixos durante o acompanhamento, e só são recalculados depois de uma mudança no processo.",
    "Cada subgrupo novo é lançado e lido no mesmo turno.",
    "Todo sinal tem causa procurada e ação registrada.",
    "A capacidade só é calculada com a base em controle.",
    "O histograma é lido junto com a especificação: centro, largura e forma.",
    "A decisão sobre capacidade baixa foi levada à direção ou ao dono do processo.",
]


# ------------------------------------------------------------ contas
def completo(s):
    return len([v for v in s if v is not None]) == N


def media(s):
    return mean(s) if completo(s) else None


def amp(s):
    return max(s) - min(s) if completo(s) else None


def fase(ex, k):
    g = ex["subs"][k]
    if not completo(g["v"]):
        return ""
    if g["excl"] == SIM:
        return EXCL
    return BASE if not ex["head"]["base"] or k < ex["head"]["base"] else ACOMP


def limites(ex):
    b = [g["v"] for k, g in enumerate(ex["subs"]) if fase(ex, k) == BASE]
    if not b:
        return None
    xbb = mean(media(s) for s in b)
    rb = mean(amp(s) for s in b)
    return dict(lc=xbb, lsc=xbb + A2 * rb, lic=xbb - A2 * rb, rb=rb, lscr=D4 * rb, licr=D3 * rb, sigma=rb / D2, n=len(b))


def sinais(ex, k, L=None):
    """Os sinais do subgrupo: o da média (o primeiro, na ordem das regras da média) e o da amplitude, que tem gráfico próprio."""
    L = L or limites(ex)
    xs = [media(g["v"]) for g in ex["subs"]]
    x, r = xs[k], amp(ex["subs"][k]["v"])
    if x is None or L is None:
        return []
    out = []
    if x > L["lsc"] or x < L["lic"]:
        out.append(S_FORA)
    elif k >= LADO - 1 and (all(v is not None and v > L["lc"] for v in xs[k - LADO + 1:k + 1])
                            or all(v is not None and v < L["lc"] for v in xs[k - LADO + 1:k + 1])):
        out.append(S_LADO)
    elif k >= TEND - 1:
        jan = xs[k - TEND + 1:k + 1]
        if all(v is not None for v in jan) and (all(b > a for a, b in zip(jan, jan[1:])) or all(b < a for a, b in zip(jan, jan[1:]))):
            out.append(S_TEND)
    if r > L["lscr"]:
        out.append(S_AMP)
    return out


def sinal(ex, k, L=None):
    """O texto da coluna Sinal: os sinais do subgrupo, separados por ponto e vírgula."""
    return SEP.join(sinais(ex, k, L))


def conta_sinais(sg):
    """Quantos subgrupos têm cada sinal, a partir da coluna Sinal."""
    return {s: sum(1 for x in sg if s in x.split(SEP)) for s in SINAIS}


def fora_espec(ex, s):
    h = ex["head"]
    return sum(1 for v in s if v is not None and (v < h["lie"] or v > h["lse"]))


def conf(g):
    n = len([v for v in g["v"] if v is not None])
    if n == 0 and not (g["data"] or g["id"] or g["excl"]):
        return ""
    if 0 < n < N:
        return "Faltam medições"
    if n and not g["data"]:
        return "Falta a data"
    if g["excl"] == SIM and not g["motivo"]:
        return "Falta o motivo"
    return "OK" if n else "Faltam medições"


def capacidade(ex, L=None):
    L = L or limites(ex)
    h = ex["head"]
    if L is None or L["sigma"] == 0:
        return None
    cp = (h["lse"] - h["lie"]) / (6 * L["sigma"])
    cpk = min(h["lse"] - L["lc"], L["lc"] - h["lie"]) / (3 * L["sigma"])
    base_sinal = sum(1 for k in range(len(ex["subs"])) if fase(ex, k) == BASE and sinal(ex, k, L))
    st = CAPAZ if cpk >= CPK_BOM else LIMITE if cpk >= CPK_MIN else NAOCAPAZ
    return dict(cp=cp, cpk=cpk, status=st, base_sinal=base_sinal)


def classes(ex):
    """Doze classes de mesma largura: um oitavo da tolerância, começando dois oitavos abaixo do limite inferior."""
    h = ex["head"]
    w = (h["lse"] - h["lie"]) / 8
    return [(h["lie"] - 2 * w + i * w, h["lie"] - 2 * w + (i + 1) * w) for i in range(NCLASSES)]


def histograma(ex):
    vals = [v for g in ex["subs"] for v in g["v"] if v is not None]
    cl = classes(ex)
    cont = [sum(1 for v in vals if a <= v < b) for a, b in cl]
    return dict(cont=cont, abaixo=sum(1 for v in vals if v < cl[0][0]), acima=sum(1 for v in vals if v >= cl[-1][1]), n=len(vals),
                media=mean(vals), mn=min(vals), mx=max(vals), fora=sum(1 for v in vals if v < ex["head"]["lie"] or v > ex["head"]["lse"]))


def _subs(datas, ids, vals, excl=None):
    excl = excl or {}
    return [dict(data=d, id=i, v=list(v), excl=SIM if k in excl else "", motivo=excl.get(k, "")) for k, (d, i, v) in enumerate(zip(datas, ids, vals))]


# ------------------------------------------------------------ exemplo 1: pizzaria, peso da bola de massa
_DP = [D(2027, 3, 22) + timedelta(days=k) for k in range(25)]
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", processo="Preparar a massa", carac="Peso da bola de massa da pizza grande", unid="g", lie=380, lse=420,
                 instr="Balança da bancada BAL-01, de 1 g, verificada em 01/03/2027", subgrupo="As cinco bolas de cada lote de massa, pesadas uma a uma",
                 periodo="Um lote por dia, de 22/03 a 15/04/2027", base=25, resp="Pizzaiolo líder, com o gerente da loja",
                 origem="Registro de produto não conforme 2027-17: bolas com 365 g em média em 18/03. O plano registrava só a média de cinco bolas."),
    "subs": _subs(_DP, [f"Massa {d.strftime('%d/%m')}" for d in _DP], [
        [390, 399, 411, 386, 407], [395, 409, 398, 400, 404], [396, 400, 399, 412, 403], [387, 403, 402, 400, 411], [409, 388, 411, 396, 396],
        [396, 399, 406, 390, 398], [393, 397, 395, 404, 405], [391, 401, 386, 400, 405], [397, 419, 403, 393, 402], [393, 403, 398, 399, 378],
        [393, 405, 405, 406, 402], [408, 407, 404, 409, 407], [396, 404, 407, 398, 384], [397, 402, 379, 388, 390], [413, 406, 397, 407, 402],
        [387, 396, 407, 397, 419], [396, 397, 398, 400, 400], [411, 417, 398, 387, 397], [401, 414, 406, 401, 423], [391, 391, 412, 405, 400],
        [390, 403, 403, 395, 401], [388, 409, 390, 408, 392], [392, 398, 393, 406, 393], [401, 406, 407, 407, 398], [416, 399, 395, 402, 416]]),
}

# ------------------------------------------------------------ exemplo 2: indústria, espessura do filme na extrusora 3
_DI = [D(2027, 7, 4) + timedelta(days=k // 2) for k in range(25)]
_II = ["Turno A" if k % 2 == 0 else "Turno C" for k in range(25)]
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas", processo="Extrusão, na extrusora 3", carac="Espessura do filme de 40 µm do cliente A", unid="µm", lie=38, lse=42,
                 instr="Micrômetro digital MIC-08, de 0,1 µm, no lugar do MIC-07 retirado em 12/06", subgrupo="Os cinco pontos na largura da primeira bobina de cada turno",
                 periodo="Turnos A e C, de 04 a 16/07/2027", base=14, resp="Coordenador da Qualidade, com o operador do posto",
                 origem="Reclamações de espessura do cliente A e o micrômetro reprovado em junho. A fábrica quer saber se a extrusora 3 segura a espessura."),
    "subs": _subs(_DI, _II, [
        [39.7, 39.9, 39.8, 39.9, 40.2], [39.5, 39.9, 39.9, 39.7, 40.0], [40.0, 40.7, 40.1, 40.0, 40.3], [39.7, 39.8, 40.2, 39.8, 39.7], [39.8, 39.6, 40.3, 40.4, 40.8],
        [40.7, 41.3, 40.7, 41.5, 40.1], [40.2, 39.9, 39.6, 40.5, 39.9], [40.3, 39.9, 40.0, 39.5, 39.7], [40.1, 40.2, 39.9, 40.0, 39.4], [40.0, 39.8, 39.7, 40.1, 39.9],
        [39.7, 39.9, 39.9, 39.9, 40.0], [39.9, 40.3, 40.5, 40.3, 39.9], [39.8, 40.1, 39.9, 40.4, 40.1], [40.1, 39.8, 40.0, 39.7, 39.6], [40.0, 39.5, 39.7, 40.2, 40.5],
        [39.9, 39.7, 40.2, 40.2, 40.1], [39.4, 39.5, 40.2, 39.3, 39.8], [40.3, 40.2, 39.3, 39.5, 39.5], [38.9, 39.6, 39.1, 39.9, 39.0], [39.1, 39.1, 39.5, 38.0, 40.0],
        [39.2, 39.4, 40.1, 39.4, 39.6], [39.3, 39.8, 39.7, 40.0, 39.2], [38.5, 39.3, 38.4, 39.1, 38.9], [37.6, 38.8, 38.4, 38.1, 37.8], [39.2, 39.4, 38.2, 38.2, 38.4]],
        excl={5: "Resistência da zona 3 queimada; bobina segregada e moída (registro de produto não conforme 2027-29)."}),
}
PARADA = D(2027, 7, 18)


def resumo(ex):
    L = limites(ex)
    sg = [sinal(ex, k, L) for k in range(len(ex["subs"]))]
    fases = [fase(ex, k) for k in range(len(ex["subs"]))]
    primeiro = next((k for k in range(len(sg)) if sg[k] and fases[k] == ACOMP), None)
    return dict(L=L, cap=capacidade(ex, L), sinais=conta_sinais(sg), sg=sg, fases=fases, primeiro=primeiro, hist=histograma(ex),
                lotes_media_ok_bola_fora=sum(1 for g in ex["subs"] if ex["head"]["lie"] <= media(g["v"]) <= ex["head"]["lse"] and fora_espec(ex, g["v"])))


if __name__ == "__main__":
    for ex in (EX1, EX2):
        r = resumo(ex)
        print({k: round(v, 4) if isinstance(v, float) else v for k, v in r["L"].items()})
        print({k: round(v, 3) if isinstance(v, float) else v for k, v in r["cap"].items()}, r["sinais"], "primeiro", r["primeiro"],
              ex["subs"][r["primeiro"]]["data"] if r["primeiro"] is not None else None, "lotes ok com bola fora", r["lotes_media_ok_bola_fora"])
        h = r["hist"]
        print(h["cont"], h["abaixo"], h["acima"], h["n"], round(h["media"], 3), h["mn"], h["mx"], "fora", h["fora"])
        print([(k + 1, s) for k, s in enumerate(r["sg"]) if s], [conf(g) for g in ex["subs"]].count("OK"))
