# -*- coding: utf-8 -*-
"""Dados do estudo de Informação documentada, usados pelo HTML e pela planilha.

Os tipos de documento, a codificação, os intervalos de revisão e os prazos de retenção são uma convenção deste material.
Os exemplos continuam os dos outros estudos da série (pizzaria e compras da indústria de embalagens).
"""
from calendar import monthrange
from datetime import date

D = date
DOCUMENTO, REGISTRO = "Documento", "Registro"
PAPEL, ELET, AMBOS = "Papel", "Eletrônico", "Ambos"
MEIOS = [PAPEL, ELET, AMBOS]
VIG, EMREV, OBS = "Vigente", "Em revisão", "Obsoleto"
STATUS = [VIG, EMREV, OBS]
S_VIG, S_VENC, S_CODIGO, S_APROV, S_REV, S_EMREV, S_OBS = "Vigente", "Revisão vencida", "Falta o código", "Falta a aprovação", "Falta a revisão", "Em revisão", "Obsoleto"
SIM, NAO = "Sim", "Não"
REV_MESES = 24  # intervalo padrão de revisão, em meses

# tipos de documento: sigla, nome, o que é, exemplo
TIPOS = [
    ("PO", "Política", "Compromisso da direção, em uma página.", "Política da qualidade, política de compras."),
    ("MP", "Mapa e descrição de processo", "Como os processos se ligam, e o que cada um precisa.", "Mapa de processos, SIPOC, tartaruga."),
    ("PR", "Procedimento", "Como um processo é feito: quem faz o quê, em que ordem, com que critério.", "PR-SUP-01, aquisição de materiais e serviços."),
    ("IT", "Instrução de trabalho", "Como uma atividade é feita, passo a passo, no posto de trabalho.", "IT-EXP-01, expedição e agrupamento por zona."),
    ("ES", "Especificação", "O que o produto ou o serviço deve ser.", "Cardápio com composição, ficha técnica do produto."),
    ("FR", "Formulário", "Modelo em branco, que vira registro quando preenchido.", "Requisição de compra, ficha de alergênicos."),
    ("DE", "Documento externo", "Vem de fora e a organização precisa seguir.", "Norma ISO 9001, desenho do cliente, manual do forno."),
]

# ciclo de vida de um documento
CICLO = [
    ("Elaborar", "Quem conhece a atividade escreve, no modelo padrão."),
    ("Analisar criticamente", "Quem usa o documento lê e aponta o que não funciona."),
    ("Aprovar", "Quem tem autoridade assina, e a revisão passa a valer."),
    ("Distribuir", "A versão nova chega a quem usa, e a antiga sai de circulação."),
    ("Usar", "O documento fica disponível no posto de trabalho, legível e protegido."),
    ("Revisar", "Na data prevista, ou quando o processo muda, o ciclo recomeça."),
]

# atividades de controle do requisito 7.5.3.2, em resumo, com a pergunta de auditoria
CONTROLE = [
    ("Distribuição, acesso e uso", "Quem precisa do documento tem a versão em vigor?", "O posto de trabalho tem a revisão da lista mestra."),
    ("Armazenamento e preservação", "O documento e o registro continuam legíveis até o fim da retenção?", "Pasta ou sistema com cópia de segurança."),
    ("Controle de alterações", "Dá para saber o que mudou, quando e quem aprovou?", "Histórico de revisões no próprio documento."),
    ("Retenção e disposição", "Por quanto tempo o registro é guardado, e o que se faz depois?", "Tabela de retenção, com o descarte registrado."),
    ("Informação de origem externa", "Os documentos de fora são identificados e atualizados?", "Lista de documentos externos, com a data de verificação."),
    ("Proteção dos registros", "O registro pode ser alterado sem que se perceba?", "Registro assinado, ou sistema com trilha de alteração."),
]


def situacao(d, ref):
    """Situação de um documento da lista mestra, na data de referência."""
    if not d["codigo"]:
        return S_CODIGO
    if d["status"] == OBS:
        return S_OBS
    if not d["rev"] or not d["data"]:
        return S_REV
    if not d["aprovou"]:
        return S_APROV
    if d["status"] == EMREV:
        return S_EMREV
    return S_VENC if proxima(d) < ref else S_VIG


def proxima(d):
    """Próxima revisão: a data da revisão mais o intervalo, em meses."""
    m = d["data"].month - 1 + d["meses"]
    ano, mes = d["data"].year + m // 12, m % 12 + 1
    return D(ano, mes, min(d["data"].day, monthrange(ano, mes)[1]))


def _docs(rows):
    keys = ("codigo", "titulo", "tipo", "processo", "rev", "data", "elaborou", "aprovou", "meio", "onde", "meses", "status")
    return [dict(zip(keys, r), n=i + 1) for i, r in enumerate(rows)]


def _regs(rows):
    keys = ("nome", "form", "processo", "gerado", "guardado", "meio", "meses", "acesso", "disposicao")
    return [dict(zip(keys, r), n=i + 1) for i, r in enumerate(rows)]


def _ext(rows):
    keys = ("nome", "origem", "versao", "onde", "como", "verificado", "meses")
    return [dict(zip(keys, r), n=i + 1) for i, r in enumerate(rows)]


# ------------------------------------------------------------ exemplo 1: pizzaria
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", data=D(2027, 1, 22), por="Gerente da loja, com os líderes",
                 origem="Decisão da análise crítica de 14/12/2026 e lacuna do requisito 7.5 no diagnóstico de 02/10/2026.",
                 regra="Documentos revistos a cada 24 meses, ou quando o processo muda."),
    "docs": _docs([
        ("IT-EXP-01", "Expedição e agrupamento por zona", "IT", "Entregar o pedido", "2", D(2026, 7, 10), "Líder da expedição", "Gerente da loja", PAPEL, "Quadro da expedição", 24, VIG),
        ("IT-ATE-01", "Roteiro de atendimento por telefone e mensagens", "IT", "Registrar o pedido", "2", D(2026, 10, 8), "Atendente líder", "Gerente da loja", PAPEL, "Balcão", 24, VIG),
        ("", "Escala padrão de entregadores", "IT", "Entregar o pedido", "", None, "Líder da expedição", "", PAPEL, "Quadro da expedição", 24, VIG),
        ("IT-PRO-01", "Rotina de controle de temperatura", "IT", "Comprar e armazenar insumos", "1", D(2026, 9, 30), "Pizzaiolo líder", "Gerente da loja", PAPEL, "Porta da câmara fria", 24, VIG),
        ("PR-GES-01", "Rotina de documentos", "PR", "Medir e melhorar", "3", D(2026, 10, 14), "Gerente da loja", "Dono da loja", ELET, "Pasta da gerência", 24, VIG),
        ("FR-03", "Ficha de alergênicos", "FR", "Produzir e embalar", "1", D(2026, 10, 16), "Pizzaiolo líder", "Gerente da loja", AMBOS, "Sistema de pedidos", 24, VIG),
        ("", "Receitas padrão", "IT", "Produzir e embalar", "", None, "Pizzaiolo líder", "", PAPEL, "Caderno do pizzaiolo", 24, VIG),
        ("", "Cardápio", "ES", "Atender no salão", "2026-2", D(2026, 7, 1), "Gerente da loja", "Dono da loja", AMBOS, "Mesas e site", 12, VIG),
        ("FR-04", "Planilha de descarte de insumos", "FR", "Comprar e armazenar insumos", "1", D(2026, 8, 3), "Gerente da loja", "Gerente da loja", ELET, "Planilha da gerência", 24, VIG),
        ("FR-05", "Ficha de treinamento", "FR", "Treinar a equipe", "1", D(2026, 7, 10), "Gerente da loja", "", PAPEL, "Pasta de pessoal", 24, VIG),
        ("MP-01", "Mapa de processos", "MP", "Planejar e dirigir a loja", "1", D(2026, 10, 14), "Gerente da loja", "Dono da loja", ELET, "Pasta da gerência", 12, VIG),
        ("MP-02", "Matriz de riscos do delivery", "MP", "Planejar e dirigir a loja", "1", D(2026, 10, 5), "Gerente da loja", "Dono da loja", ELET, "Pasta da gerência", 6, VIG),
        ("IT-CAI-01", "Fechamento de caixa", "IT", "Atender no salão", "1", D(2025, 3, 12), "Gerente da loja", "Dono da loja", PAPEL, "Gaveta do caixa", 24, OBS),
    ]),
    "regs": _regs([
        ("Pedido registrado", "Sistema de pedidos", "Registrar o pedido", "Balcão e site", "Sistema, na nuvem", ELET, 24, "Gerente e atendentes", "Exclusão pelo sistema"),
        ("Planilha de temperatura", "FR-02", "Comprar e armazenar insumos", "Câmara fria", "Pasta da cozinha", PAPEL, 12, "Pizzaiolo líder", "Picotar"),
        ("Etiqueta de conferência do pedido", "Etiqueta do sistema", "Produzir e embalar", "Bancada de embalagem", "Caixa da expedição", PAPEL, 1, "Líder da expedição", "Descartar após 30 dias"),
        ("Ficha de treinamento preenchida", "FR-05", "Treinar a equipe", "Sala da gerência", "Pasta de pessoal", PAPEL, 60, "Gerente da loja", "Picotar"),
        ("Registro de reclamações", "Planilha de reclamações", "Medir e melhorar", "Balcão e site", "Planilha da gerência", ELET, 24, "Gerente e atendente líder", "Exclusão"),
        ("Registro de não conformidade", "FR-06", "Medir e melhorar", "Sala da gerência", "Pasta da qualidade", AMBOS, 60, "Gerente da loja", "Picotar e excluir"),
        ("Relatório de auditoria interna", "FR-07", "Medir e melhorar", "Sala da gerência", "Pasta da qualidade", ELET, 60, "Gerente e dono", "Exclusão"),
        ("Ata da análise crítica", "FR-08", "Planejar e dirigir a loja", "Sala da gerência", "Pasta da gerência", ELET, 60, "Dono e gerente", "Exclusão"),
    ]),
    "ligados": [("IT-ATE-01", "Roteiro de atendimento"), ("Tela do sistema", "Campo de complemento obrigatório"), ("FR-03", "Ficha de alergênicos"),
                ("Etiqueta", "Rubrica da conferência")],
}

# ------------------------------------------------------------ exemplo 2: compras da indústria
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas · Suprimentos", data=D(2027, 3, 5), por="Gerente de Suprimentos, com o Coordenador da Qualidade",
                 origem="Preparação da auditoria de certificação, decidida na análise crítica de 18/02/2027.",
                 regra="Documentos revistos a cada 24 meses. Formulários e listas, a cada 12."),
    "docs": _docs([
        ("PR-SUP-01", "Aquisição de materiais e serviços", "PR", "Suprimentos", "6", D(2026, 10, 16), "Gerente de Suprimentos", "Diretor geral", ELET, "Rede, pasta Qualidade", 24, VIG),
        ("PO-02", "Política de compras e alçadas", "PO", "Suprimentos", "3", D(2025, 11, 20), "Diretor geral", "Diretor geral", ELET, "Rede, pasta Qualidade", 24, VIG),
        ("PR-SUP-02", "Homologação e avaliação de fornecedores", "PR", "Suprimentos", "2", D(2026, 11, 27), "Comprador sênior", "Gerente de Suprimentos", ELET, "Rede, pasta Qualidade", 24, VIG),
        ("PR-SUP-03", "Compras de urgência", "PR", "Suprimentos", "1", D(2025, 4, 8), "Gerente de Suprimentos", "Diretor geral", ELET, "Rede, pasta Qualidade", 24, EMREV),
        ("IT-REC-01", "Recebimento e conferência de materiais", "IT", "Recebimento", "1", D(2025, 2, 17), "Líder do Recebimento", "Gerente de Suprimentos", PAPEL, "Quadro do almoxarifado", 24, VIG),
        ("FR-11", "Requisição de compra", "FR", "Suprimentos", "4", D(2026, 10, 14), "Analista de sistemas", "Gerente de Suprimentos", ELET, "Sistema de compras", 12, VIG),
        ("FR-12", "Avaliação de desempenho de fornecedor", "FR", "Suprimentos", "2", D(2026, 11, 27), "Comprador sênior", "Gerente de Suprimentos", ELET, "Rede, pasta Suprimentos", 12, VIG),
        ("FR-13", "Registro de devolução ao fornecedor", "FR", "Recebimento", "1", D(2025, 2, 17), "Líder do Recebimento", "Gerente de Suprimentos", PAPEL, "Almoxarifado", 12, VIG),
        ("LS-01", "Lista de fornecedores homologados", "FR", "Suprimentos", "2027-02", D(2027, 2, 26), "Comprador sênior", "Gerente de Suprimentos", ELET, "Rede, pasta Suprimentos", 6, VIG),
        ("", "Cadastro de itens com especificação padrão", "FR", "Suprimentos", "", D(2026, 10, 23), "Supervisor de manutenção", "", ELET, "Sistema de compras", 12, VIG),
    ]),
    "regs": _regs([
        ("Requisição de compra aprovada", "FR-11", "Suprimentos", "Sistema de compras", "Sistema de compras", ELET, 60, "Compradores e requisitantes", "Arquivo morto do sistema"),
        ("Cotações e mapa comparativo", "Planilha de cotação", "Suprimentos", "Comprador", "Rede, pasta do pedido", ELET, 60, "Compradores", "Exclusão"),
        ("Pedido de compra emitido", "Sistema de compras", "Suprimentos", "Sistema de compras", "Sistema de compras", ELET, 60, "Compradores e Fiscal", "Arquivo morto do sistema"),
        ("Registro de recebimento e conferência", "FR-14", "Recebimento", "Almoxarifado", "Pasta do almoxarifado e sistema", AMBOS, 36, "Recebimento e Qualidade", "Picotar"),
        ("Avaliação de desempenho de fornecedor", "FR-12", "Suprimentos", "Comprador sênior", "Rede, pasta Suprimentos", ELET, 60, "Suprimentos e Qualidade", "Exclusão"),
        ("Dossiê de homologação", "PR-SUP-02, anexo A", "Suprimentos", "Comprador sênior", "Rede, pasta Fornecedores", ELET, 60, "Suprimentos e Qualidade", "Exclusão após o descredenciamento"),
        ("Registro de devolução", "FR-13", "Recebimento", "Almoxarifado", "Pasta do almoxarifado", PAPEL, 36, "Recebimento", "Picotar"),
        ("Contrato com fornecedor", "Modelo jurídico", "Suprimentos", "Gerente de Suprimentos", "Cofre da diretoria", PAPEL, 120, "Diretoria e Jurídico", "Picotar após o fim do contrato"),
    ]),
    "fluxo": [("Requisição", ["FR-11", "Cadastro de itens"]), ("Cotação", ["PO-02", "LS-01"]), ("Pedido", ["PR-SUP-01", "PR-SUP-03"]),
              ("Recebimento", ["IT-REC-01", "FR-13"]), ("Avaliação", ["PR-SUP-02", "FR-12"])],
}

# exemplo 3: documentos de origem externa da indústria (só no treinamento)
EXT = _ext([
    ("ISO 9001:2015, com a emenda de 2024", "ISO e ABNT", "Emenda 1, de 2024", "Todo o sistema", "Consulta ao site da ABNT a cada seis meses", D(2027, 1, 12), 6),
    ("Norma regulamentadora de segurança em máquinas", "Ministério do Trabalho", "Texto vigente em 2026", "Produção e Manutenção", "Consultoria de segurança avisa as mudanças", D(2026, 11, 3), 6),
    ("Desenhos e especificações do cliente", "Cada cliente", "Revisão informada no desenho", "Desenvolvimento e Produção", "O cliente envia a revisão nova; a antiga é retirada do posto", D(2027, 2, 20), 3),
    ("Fichas técnicas das resinas", "Fornecedores", "Data da ficha", "Suprimentos e Produção", "Pedida ao fornecedor a cada lote novo", D(2027, 2, 26), 6),
    ("Regulamento de embalagens em contato com alimentos", "Agência reguladora", "Resolução vigente", "Desenvolvimento e Laboratório", "Consulta ao site da agência a cada seis meses", D(2026, 7, 8), 6),
    ("Manuais das extrusoras", "Fabricante", "Edição de cada máquina", "Produção e Manutenção", "Fabricante envia as revisões", D(2026, 5, 15), 12),
])

# situação dos documentos por processo da indústria (módulo 7): em dia, revisão vencida, sem controle
IND_DOCS = [("Comercial e análise de pedidos", 4, 1, 1), ("Desenvolvimento de produto", 5, 2, 0), ("Suprimentos", 8, 1, 1), ("Produção", 9, 3, 2),
            ("Laboratório e controle da qualidade", 7, 1, 0), ("Expedição e logística", 3, 1, 1), ("Manutenção", 2, 2, 3), ("Gestão de pessoas", 3, 0, 1),
            ("Gestão do sistema da qualidade", 6, 1, 0)]

CHECK = [
    "A lista mestra existe e traz todos os documentos em uso, com código, revisão e data.",
    "Cada documento tem um responsável por elaborar e um por aprovar.",
    "A revisão em uso no posto de trabalho é a mesma da lista mestra.",
    "As versões antigas foram retiradas de circulação, ou estão marcadas como obsoletas.",
    "Cada documento tem data de revisão prevista, ou é revisto quando o processo muda.",
    "Quando um documento muda, os documentos ligados a ele são conferidos.",
    "Os formulários em uso são a versão em vigor.",
    "Cada registro tem prazo de retenção, local de guarda e forma de descarte definidos.",
    "Os registros em papel estão legíveis e protegidos de perda e de alteração.",
    "Os registros eletrônicos têm cópia de segurança e controle de acesso.",
    "Os documentos de origem externa estão listados, com a data da última verificação.",
    "A lista dos documentos e registros exigidos pela norma foi conferida.",
]

if __name__ == "__main__":
    for nome, ex in (("EX1", EX1), ("EX2", EX2)):
        ref = ex["head"]["data"]
        sits = [situacao(d, ref) for d in ex["docs"]]
        print(nome, len(ex["docs"]), "documentos:", {s: sits.count(s) for s in sorted(set(sits))}, "| registros:", len(ex["regs"]))
        print("   ", [(d["codigo"] or d["titulo"], s) for d, s in zip(ex["docs"], sits) if s != S_VIG])
    print("externos:", [(e["nome"][:20], e["verificado"], e["meses"]) for e in EXT])
    print("indústria:", sum(a for _, a, _, _ in IND_DOCS), sum(b for _, _, b, _ in IND_DOCS), sum(c for _, _, _, c in IND_DOCS))
