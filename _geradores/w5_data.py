# -*- coding: utf-8 -*-
"""Dados dos exemplos do 5W2H, usados pelo HTML e pela planilha."""
from datetime import date


def _mk(rows):
    keys = ("oque", "curto", "porque", "onde", "inicio", "prazo", "quem", "como", "custo", "custo_txt",
            "status", "fim", "real", "evidencia")
    return [dict(zip(keys, r), k=f"A{i+1}") for i, r in enumerate(rows)]


D = date

EX1 = {
    "head": dict(plano="Reduzir os atrasos nas entregas de delivery", resp="Gerente da loja", area="Pizzaria (loja)",
                 data=D(2026, 7, 24), autor="Equipe da loja", versao="1.0",
                 objetivo="Aumentar de 82% para 95% as entregas em até 40 minutos.",
                 origem="Ciclo PDCA: causas confirmadas na análise", orcamento=1500,
                 fora="Compra de forno e mudanças no cardápio."),
    "ref": D(2026, 8, 5),  # data de referência do gráfico do treinamento
    "ref_status": ["Concluída", "Concluída", "Concluída", "Atrasada", "No prazo", "No prazo"],  # situação calculada, como no módulo 5
    "itens": _mk([
        ("Reforçar a escala de entregadores nas sextas e nos sábados, das 19h às 22h", "Reforçar a escala de entregadores no pico",
         "A escala é igual em todos os dias e não acompanha o pico de pedidos", "Expedição da loja",
         D(2026, 7, 27), D(2026, 7, 31), "Gerente da loja",
         "Contratar dois entregadores parceiros para o pico; daí em diante, a escala do pico segue os pedidos por faixa de horário medidos na A5", 600, "R$ 600 no primeiro mês",
         "Concluída", D(2026, 7, 31), 600, "Escala de agosto publicada"),
        ("Tornar obrigatório o complemento do endereço no pedido", "Tornar obrigatório o complemento do endereço",
         "15% dos atrasos têm endereço incompleto", "Site e aplicativo de delivery",
         D(2026, 7, 27), D(2026, 7, 29), "Atendente do cadastro",
         "Alterar o campo no painel do aplicativo e no formulário do site", 0, "Sem custo",
         "Concluída", D(2026, 7, 29), 0, "Tela do formulário com o campo obrigatório"),
        ("Treinar a equipe da expedição no agrupamento de pedidos", "Treinar a equipe da expedição",
         "O agrupamento muda a rotina de quem embala e despacha", "Loja, antes da abertura",
         D(2026, 7, 27), D(2026, 7, 30), "Líder da expedição",
         "Duas sessões de 30 minutos, com simulação de pedidos", 200, "R$ 200 em horas extras",
         "Concluída", D(2026, 7, 30), 200, "Lista de presença"),
        ("Agrupar os pedidos por bairro antes da saída", "Agrupar os pedidos por bairro",
         "Os pedidos saem um a um, e as rotas se cruzam", "Expedição da loja",
         D(2026, 7, 31), D(2026, 8, 2), "Líder da expedição",
         "Separar os pedidos em três zonas, com uma prateleira para cada uma", 350, "R$ 350 em prateleiras e etiquetas",
         "Concluída", D(2026, 8, 7), 420, "Fotos da expedição e registro das saídas"),
        ("Medir o tempo de entrega por faixa de horário", "Medir o tempo de entrega por faixa de horário",
         "A média do dia esconde o que acontece no pico", "Relatório do aplicativo",
         D(2026, 7, 27), D(2026, 9, 6), "Gerente da loja",
         "Exportar o relatório toda segunda-feira e atualizar o gráfico", 0, "Sem custo",
         "Concluída", D(2026, 9, 6), 0, "Gráfico de tendência de 12 semanas"),
        ("Atualizar a instrução de trabalho da expedição", "Atualizar a instrução de trabalho",
         "O novo método precisa virar padrão", "Pasta de procedimentos da loja",
         D(2026, 9, 7), D(2026, 9, 15), "Gerente da loja",
         "Revisar o documento e colher a assinatura da equipe", 0, "Sem custo",
         "Concluída", D(2026, 9, 15), 0, "Instrução revisada e assinada"),
    ]),
    "verif": [("Entregas no prazo", "% de entregas em até 40 minutos", 82, 95, "Maior é melhor", 95.5, D(2026, 9, 8),
               "Média das semanas 9 a 12")],
}

EX2 = {
    "head": dict(plano="Reduzir o prazo de compra", resp="Gerente de Suprimentos", area="Distribuidora de materiais elétricos · Compras",
                 data=D(2026, 7, 3), autor="Equipe de compras", versao="1.0",
                 objetivo="Reduzir de 12 para 7 dias úteis o prazo entre a requisição aprovada e o pedido emitido.",
                 origem="Ciclo PDCA e Matriz GUT da área", orcamento=3000,
                 fora="Revisão de contratos pelo Jurídico e homologação de fornecedores."),
    "itens": _mk([
        ("Criar o formulário de requisição com campos obrigatórios", "Criar o formulário de requisição",
         "40% das requisições são devolvidas por especificação incompleta", "Sistema de compras",
         D(2026, 7, 6), D(2026, 7, 10), "Analista de compras",
         "Configurar os campos obrigatórios e as validações com a equipe de TI", 1800, "R$ 1.800 em horas de TI",
         "Concluída", D(2026, 7, 10), 1800, "Formulário publicado no sistema"),
        ("Montar o catálogo dos 200 itens mais comprados", "Montar o catálogo de itens",
         "O mesmo item é descrito de formas diferentes a cada requisição", "Sistema de compras",
         D(2026, 7, 6), D(2026, 7, 17), "Comprador sênior",
         "Extrair o histórico de 12 meses e padronizar as descrições", 0, "Sem custo adicional",
         "Concluída", D(2026, 7, 21), 0, "Catálogo com 214 itens"),
        ("Aprovar a alçada de uma cotação para compras de até R$ 2.000", "Aprovar a nova alçada de cotação",
         "A política exige três cotações para qualquer valor", "Reunião da Diretoria",
         D(2026, 7, 6), D(2026, 7, 8), "Gerente de Suprimentos",
         "Apresentar a proposta, com a estimativa de ganho de prazo e de risco", 0, "Sem custo",
         "Concluída", D(2026, 7, 8), 0, "Ata da reunião e política revisada"),
        ("Treinar requisitantes e compradores das duas áreas do piloto", "Treinar requisitantes e compradores",
         "O formulário e a alçada mudam a rotina de quem pede e de quem compra", "Sala de treinamento",
         D(2026, 7, 9), D(2026, 7, 10), "Analista de compras",
         "Duas turmas de uma hora, com exercícios no sistema", 400, "R$ 400 em material e lanche",
         "Concluída", D(2026, 7, 10), 350, "Listas de presença"),
        ("Conduzir o piloto em duas áreas requisitantes", "Conduzir o piloto em duas áreas",
         "A mudança precisa ser testada antes de virar regra", "Manutenção e Produção",
         D(2026, 7, 13), D(2026, 8, 7), "Gerente de Suprimentos",
         "Aplicar o novo fluxo a todas as requisições das duas áreas e registrar os desvios", 0, "Sem custo",
         "Concluída", D(2026, 8, 7), 0, "Registro do piloto"),
        ("Medir o prazo de cada pedido emitido no piloto", "Medir o prazo dos pedidos do piloto",
         "O resultado precisa ser comparado com a meta de 7 dias úteis", "Relatório do sistema de compras",
         D(2026, 7, 13), D(2026, 8, 14), "Analista de compras",
         "Emitir o relatório semanal e calcular a média por área", 0, "Sem custo",
         "Concluída", D(2026, 8, 14), 0, "Relatório de prazos do piloto"),
    ]),
    "verif": [("Prazo de compra", "Dias úteis entre a requisição e o pedido", 12, 7, "Menor é melhor", 8, D(2026, 8, 28),
               "Meta não atingida: novo ciclo para a revisão de contratos"),
              ("Requisições devolvidas", "% de requisições devolvidas", 40, 15, "Menor é melhor", 12, D(2026, 8, 28), None)],
}

EX3 = {
    "itens": _mk([
        ("Retirar de uso os 3 instrumentos vencidos e enviá-los para calibração", "", "Instrumento vencido não pode ser usado para liberar produto",
         "Laboratório de recebimento", D(2026, 9, 1), D(2026, 9, 2), "Técnico do laboratório",
         "Identificar com etiqueta de bloqueio e enviar ao laboratório credenciado", 900, "R$ 900", "", None, None, ""),
        ("Avaliar as medições feitas no período em que os instrumentos estavam vencidos", "", "É preciso saber se algum produto foi liberado com medição duvidosa",
         "Registros de inspeção", D(2026, 9, 2), D(2026, 9, 9), "Coordenador da Qualidade",
         "Comparar os resultados com os da nova calibração e reavaliar os lotes afetados", 0, "Sem custo", "", None, None, ""),
        ("Centralizar o controle dos 25 instrumentos em um cadastro único", "", "A planilha local não avisa sobre o vencimento",
         "Sistema da Qualidade", D(2026, 9, 7), D(2026, 9, 15), "Analista da Qualidade",
         "Cadastrar os instrumentos, com aviso automático 30 dias antes do vencimento", 0, "Sem custo", "", None, None, ""),
        ("Nomear responsável e suplente pelo controle dos instrumentos", "", "O controle dependia de uma única pessoa, que mudou de área",
         "Todas as áreas com instrumentos", D(2026, 9, 7), D(2026, 9, 11), "Gerente industrial",
         "Registrar a nomeação na descrição de função e comunicar às áreas", 0, "Sem custo", "", None, None, ""),
        ("Revisar o procedimento de controle de instrumentos", "", "O procedimento permite controles locais, fora do cadastro",
         "Sistema de documentos", D(2026, 9, 28), D(2026, 10, 9), "Coordenador da Qualidade",
         "Atualizar o texto, desativar as planilhas locais e treinar os usuários", 0, "Sem custo", "", None, None, ""),
        ("Verificar a eficácia: nenhum instrumento vencido depois de 90 dias", "", "A não conformidade só é encerrada com a eficácia confirmada",
         "Cadastro de instrumentos", D(2026, 12, 14), D(2026, 12, 18), "Auditor interno",
         "Conferir o cadastro e uma amostra de instrumentos em uso", 0, "Sem custo", "", None, None, ""),
    ]),
}


def dm(d):
    return d.strftime("%d/%m")


def quando(p):
    return f"{dm(p['inicio'])} a {dm(p['prazo'])}"
