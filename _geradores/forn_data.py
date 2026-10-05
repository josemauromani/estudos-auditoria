# -*- coding: utf-8 -*-
"""Dados do estudo de Avaliação de fornecedores, usados pelo HTML e pela planilha.

O índice de desempenho, os pesos, as classes e as condutas são uma convenção deste material.
Os exemplos continuam os dos outros estudos da série (indústria de embalagens e pizzaria).
"""
from calendar import monthrange
from datetime import date

D = date
PRODUTO, SERVICO, TERCEIRIZADO = "Produto", "Serviço", "Processo terceirizado"
TIPOS = [PRODUTO, SERVICO, TERCEIRIZADO]
CRITICO, NAOCRIT = "Crítico", "Não crítico"
CRITICIDADES = [CRITICO, NAOCRIT]
SIM, NAO, NA = "Sim", "Não", "Não se aplica"
ATENDE, NAOATENDE = "Atende", "Não atende"
# pesos do índice de desempenho, em percentual
PESOS = [("Qualidade", 50, "Lotes ou serviços aceitos, sobre os recebidos."), ("Prazo", 30, "Entregas no prazo, sobre as entregas."),
         ("Atendimento", 20, "Nota do comprador, de 0 a 10: resposta, documentação, flexibilidade.")]
# classes: letra, faixa mínima, nome, conduta
CLASSES = [("A", 90, "Preferencial", "Manter. Pode ter menos inspeção no recebimento."),
           ("B", 75, "Aprovado", "Manter e acompanhar. Comunicar o resultado ao fornecedor."),
           ("C", 60, "Com plano de ação", "Pedir plano de ação, com prazo. Reavaliar no período seguinte."),
           ("D", 0, "Reprovado", "Suspender as compras até um plano aprovado, ou desqualificar.")]
VALIDADE = 24  # meses de validade da homologação, neste modelo
S_HOM, S_VENC, S_NAO, S_DOC, S_EMH = "Homologado", "Homologação vencida", "Não homologado", "Falta a homologação", "Em homologação"

# critérios de homologação, com o que é conferido e a evidência
CRITERIOS = [
    ("Documentos legais", "Empresa regular, com as licenças da atividade.", "Cadastro, certidões, licença ambiental quando exigida."),
    ("Capacidade técnica", "Consegue fazer o que se pede, na quantidade e no prazo.", "Visita, portfólio, referências de clientes."),
    ("Qualidade do produto", "A amostra ou o lote piloto atende à especificação.", "Laudo de ensaio, inspeção de recebimento."),
    ("Sistema de gestão", "Tem controle do próprio processo.", "Certificado ISO 9001, ou auditoria de segunda parte."),
    ("Condições comerciais", "Preço, prazo de pagamento e de entrega compatíveis.", "Proposta e contrato."),
    ("Segurança e meio ambiente", "Cumpre o que a lei e o cliente exigem.", "Fichas de segurança, programa de gestão de resíduos."),
]

# etapas do ciclo do fornecedor
CICLO = [
    ("Selecionar", "Definir o que é crítico e homologar quem pode fornecer."),
    ("Controlar", "Pedido com os requisitos, e conferência no recebimento."),
    ("Avaliar", "Medir o desempenho do período: qualidade, prazo e atendimento."),
    ("Reavaliar", "Decidir pela classe: manter, plano de ação ou desqualificar."),
]


def pct(a, b):
    return a / b if b else 0.0


def indice(av):
    """Índice de desempenho, de 0 a 100."""
    q, p, a = pct(av["aceitos"], av["recebidos"]), pct(av["no_prazo"], av["entregas"]), av["nota"] / 10
    return round(100 * (0.5 * q + 0.3 * p + 0.2 * a), 1)


def classe(i):
    for letra, minimo, _, _ in CLASSES:
        if i >= minimo:
            return letra
    return "D"


def proxima(d, meses):
    m = d.month - 1 + meses
    ano, mes = d.year + m // 12, m % 12 + 1
    return D(ano, mes, min(d.day, monthrange(ano, mes)[1]))


def _forn(rows):
    keys = ("cod", "nome", "fornece", "tipo", "crit", "homologado", "docs")
    return [dict(zip(keys, r), n=i + 1) for i, r in enumerate(rows)]


def _aval(rows):
    keys = ("cod", "recebidos", "aceitos", "entregas", "no_prazo", "nota", "obs")
    out = [dict(zip(keys, r), n=i + 1) for i, r in enumerate(rows)]
    for a in out:
        a["indice"] = indice(a)
        a["classe"] = classe(a["indice"])
    return out


# ------------------------------------------------------------ exemplo 1: indústria de embalagens
EX1 = {
    "head": dict(org="Indústria de embalagens plásticas · Suprimentos", data=D(2027, 1, 11), periodo="Julho a dezembro de 2026",
                 por="Comprador sênior, com o Gerente de Suprimentos e a Qualidade",
                 origem="Constatação nº 2 da auditoria 2026-07: cinco fornecedores críticos sem avaliação em 2026. Avaliação semestral, PR-SUP-02 rev. 2."),
    "forns": _forn([
        ("F-01", "Polímeros do Vale", "Resina de polietileno", PRODUTO, CRITICO, D(2025, 3, 10), SIM),
        ("F-02", "Petroquímica Sul", "Resina de polipropileno", PRODUTO, CRITICO, D(2025, 6, 2), SIM),
        ("F-03", "Colorfix", "Masterbatch e pigmentos", PRODUTO, CRITICO, D(2024, 11, 18), SIM),
        ("F-04", "Tintas Gráficas Ltda.", "Tintas de impressão", PRODUTO, CRITICO, D(2025, 2, 24), SIM),
        ("F-05", "Cliché Print", "Clichês e matrizes", PRODUTO, CRITICO, D(2025, 8, 11), SIM),
        ("F-06", "Filmes Técnicos", "Filme para laminação", PRODUTO, CRITICO, D(2026, 1, 20), SIM),
        ("F-07", "Papelão Oeste", "Caixas de papelão", PRODUTO, CRITICO, D(2024, 9, 30), SIM),
        ("F-08", "Paletes Rápido", "Paletes de madeira", PRODUTO, CRITICO, D(2024, 10, 14), NAO),
        ("F-09", "Transportes Horizonte", "Transporte de produto acabado", TERCEIRIZADO, CRITICO, D(2025, 5, 5), SIM),
        ("F-10", "Mantec", "Manutenção de extrusoras", SERVICO, CRITICO, D(2025, 4, 22), SIM),
        ("F-11", "Laboratório Analítica", "Ensaios de migração e espessura", TERCEIRIZADO, CRITICO, D(2025, 7, 8), SIM),
        ("F-12", "Ferramentaria Precisa", "Usinagem de moldes", SERVICO, CRITICO, D(2025, 1, 13), SIM),
    ]),
    "avals": _aval([
        ("F-01", 26, 26, 26, 24, 8, "Fornecedor único da resina. Segundo fornecedor em homologação."),
        ("F-02", 14, 14, 14, 14, 9, ""),
        ("F-03", 18, 13, 18, 15, 6, "Cinco lotes com tonalidade fora do padrão, devolvidos. Três entregas atrasadas."),
        ("F-04", 9, 9, 9, 9, 9, ""),
        ("F-05", 22, 21, 22, 20, 8, ""),
        ("F-06", 11, 11, 11, 11, 8, "Primeira avaliação depois da homologação."),
        ("F-07", 30, 25, 30, 19, 5, "Onze entregas atrasadas. Caixas úmidas em cinco lotes."),
        ("F-08", 12, 8, 12, 7, 4, "Paletes fora da medida e madeira sem tratamento. Licença ambiental vencida."),
        ("F-09", 60, 58, 60, 55, 8, "Duas cargas com avaria."),
        ("F-10", 6, 6, 6, 5, 9, "Uma manutenção reprogramada pela produção."),
        ("F-11", 15, 15, 15, 12, 7, "Laudos entregues com atraso em três pedidos."),
        ("F-12", 5, 5, 5, 5, 8, ""),
    ]),
}

# ------------------------------------------------------------ exemplo 2: pizzaria
EX2 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", data=D(2027, 2, 15), periodo="Agosto de 2026 a janeiro de 2027",
                 por="Gerente da loja, com o pizzaiolo líder",
                 origem="Decisão da análise crítica de 14/12/2026: avaliar os fornecedores de insumos críticos a cada semestre, com registro."),
    "forns": _forn([
        ("P1", "Laticínios Serra", "Queijo muçarela", PRODUTO, CRITICO, D(2026, 12, 4), SIM),
        ("P2", "Queijaria do Campo", "Queijo muçarela, segundo fornecedor", PRODUTO, CRITICO, D(2026, 11, 20), SIM),
        ("P3", "Moinho Bom Trigo", "Farinha de trigo", PRODUTO, CRITICO, D(2026, 12, 4), SIM),
        ("P4", "Conservas Vale Verde", "Molho e tomate pelado", PRODUTO, CRITICO, D(2026, 12, 4), SIM),
        ("P5", "Embalagens Rápidas", "Caixas de pizza", PRODUTO, NAOCRIT, D(2026, 12, 4), SIM),
        ("P6", "Gás Central", "Gás de cozinha", PRODUTO, CRITICO, D(2026, 12, 4), NAO),
        ("P7", "Oficina Duas Rodas", "Revisão mensal das motos", SERVICO, CRITICO, D(2026, 12, 4), SIM),
    ]),
    "avals": _aval([
        ("P1", 24, 23, 24, 21, 7, "Três atrasos, um deles no sábado. Um lote devolvido por temperatura."),
        ("P2", 8, 8, 8, 8, 8, "Fornece desde novembro. Primeira avaliação."),
        ("P3", 12, 12, 12, 12, 9, ""),
        ("P4", 12, 12, 12, 11, 8, ""),
        ("P6", 26, 26, 26, 26, 7, "Nota fiscal sem o número do contrato em cinco entregas."),
        ("P7", 6, 5, 6, 6, 8, "Uma revisão refeita: freio com folga."),
    ]),
}

# exemplo 3: homologação do segundo fornecedor de resina (só no treinamento)
HOMOLOG = dict(cod="F-13", nome="Resinas Atlântico", fornece="Resina de polietileno", data=D(2027, 3, 5), por="Comprador sênior e Coordenador da Qualidade",
               origem="Risco C1 da matriz de riscos: fornecedor único de resina. Decisão da análise crítica de 18/02/2027: contratar os ensaios externos.",
               itens=[
                   ("Documentos legais", ATENDE, "Cadastro, certidões e licença de operação válidas até 2028."),
                   ("Capacidade técnica", ATENDE, "Visita em 24/02/2027: duas linhas de extrusão, estoque para 20 dias de consumo."),
                   ("Qualidade do produto", "Pendente", "Amostra de 500 kg em ensaio no laboratório externo. Laudo previsto para 26/03/2027."),
                   ("Sistema de gestão", ATENDE, "Certificado ISO 9001 válido até 11/2028."),
                   ("Condições comerciais", ATENDE, "Preço 3% acima do atual, com prazo de entrega de 7 dias."),
                   ("Segurança e meio ambiente", ATENDE, "Fichas de segurança do produto recebidas."),
               ],
               resultado="Em homologação: aprovado em cinco critérios. A homologação é concluída com o laudo do ensaio, e o primeiro pedido é um lote piloto de 2 toneladas.")

CHECK = [
    "Os itens e serviços críticos estão identificados, com o motivo.",
    "Os critérios de homologação estão escritos e são os mesmos para todos os fornecedores do mesmo tipo.",
    "Todo fornecedor crítico tem homologação registrada e dentro da validade.",
    "O pedido de compra informa os requisitos do produto ou do serviço.",
    "O recebimento confere o que chega, com registro, antes da liberação.",
    "Os indicadores de desempenho e os pesos estão definidos e foram comunicados aos fornecedores.",
    "A avaliação é feita no período definido, com os dados do recebimento.",
    "Cada fornecedor avaliado tem classe e conduta registradas.",
    "Os fornecedores com plano de ação têm prazo e responsável.",
    "Os fornecedores reprovados estão bloqueados no sistema de compras.",
    "As ocorrências com fornecedores são registradas e tratadas.",
    "Os processos terceirizados têm o controle definido: o que a organização confere e quando.",
]

if __name__ == "__main__":
    for nome, ex in (("EX1", EX1), ("EX2", EX2)):
        print(nome, len(ex["forns"]), "fornecedores")
        for a in ex["avals"]:
            print("   ", a["cod"], a["indice"], a["classe"], "|", pct(a["aceitos"], a["recebidos"]), pct(a["no_prazo"], a["entregas"]), a["nota"])
        print("   classes", {c: sum(1 for a in ex["avals"] if a["classe"] == c) for c, _, _, _ in CLASSES})
        for f in ex["forns"]:
            assert (f["crit"] == CRITICO) == any(a["cod"] == f["cod"] for a in ex["avals"]), f["cod"]
