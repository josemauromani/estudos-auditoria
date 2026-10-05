# -*- coding: utf-8 -*-
"""Dados dos exemplos do Diagrama de Ishikawa, usados pelo HTML e pela planilha."""
from datetime import date

M6 = ["Método", "Mão de obra", "Máquina", "Material", "Medição", "Meio ambiente"]
HINTS = {
    "Método": "Como o trabalho é feito: procedimentos, sequência, regras.",
    "Mão de obra": "Quem faz o trabalho: treinamento, quantidade, escala.",
    "Máquina": "Com o que se faz: equipamentos, ferramentas, sistemas.",
    "Material": "O que entra no processo: insumos e informações.",
    "Medição": "Como se mede: instrumentos, indicadores, critérios.",
    "Meio ambiente": "Onde se faz: espaço, temperatura, ruído, clima de trabalho.",
}
# resultado: C = confirmada, D = descartada, N = não verificada; segue = vai para o plano de ação
RES = {"C": "Confirmada", "D": "Descartada", "N": "Não verificada"}


def _mk(cats, rows):
    out, count = [], {}
    for cat, causa, curto, porque, prob, como, res, evid, segue in rows:
        i = cats.index(cat)
        count[i] = count.get(i, 0) + 1
        assert len(curto) <= 34, (curto, len(curto))
        out.append(dict(k=f"{'ABCDEF'[i]}{count[i]}", cat=cat, causa=causa, curto=curto, porque=porque, prob=prob,
                        como=como, res=RES[res], evid=evid, segue=segue))
    return out


EX1 = {
    "head": dict(tema="Atrasos nas entregas de delivery", resp="Gerente da loja", area="Pizzaria (loja)",
                 data=date(2026, 7, 17), autor="Equipe da loja", versao="1.0",
                 efeito="18% das entregas chegam depois de 40 minutos.",
                 onde="Sextas e sábados, das 19h às 22h", part="Gerente, líder da expedição, pizzaiolo, atendente e um entregador",
                 origem="Ciclo PDCA: etapa de análise das causas"),
    "efeito_curto": ["18% das entregas", "chegam depois", "de 40 minutos"],
    "cats": M6,
    "causas": _mk(M6, [
        ("Método", "Pedidos saem um a um, sem agrupamento por bairro", "Pedidos não agrupados por bairro",
         "A expedição não separa os pedidos por zona", "Alta", "Acompanhar 50 saídas no pico e mapear as rotas", "C",
         "Em 31 das 50 saídas, outro entregador saiu para o mesmo bairro menos de 10 minutos depois", True),
        ("Método", "Rota escolhida por cada entregador", "Rota escolhida pelo entregador",
         "Não há roteiro sugerido", "Média", "Comparar o tempo de rota entre os entregadores", "D",
         "Tempos parecidos entre os entregadores", False),
        ("Mão de obra", "Escala de entregadores igual em todos os dias", "Escala igual em todos os dias",
         "A escala foi montada pelo movimento médio da semana", "Alta", "Comparar os entregadores disponíveis e as entregas por noite", "C",
         "Mesmo número de entregadores todos os dias; nas sextas e nos sábados, 74 entregas por noite, contra 35 nos outros dias", True),
        ("Mão de obra", "Expedição sem responsável definido no pico", "Expedição sem responsável no pico",
         "Quem está livre faz o despacho", "Média", "Observar a expedição em três noites de pico", "N", None, False),
        ("Máquina", "Forno único, com fila no horário de pico", "Forno único, com fila no pico",
         "O forno assa seis pizzas por vez", "Alta", "Medir o tempo de espera antes do forno", "C",
         "Espera média de 12 minutos antes do forno no pico, contra 3 fora dele. Fica para o próximo ciclo", False),
        ("Máquina", "Motos com manutenção atrasada", "Motos com manutenção atrasada",
         None, "Baixa", "Conferir o registro de quebras do trimestre", "D", "Nenhuma quebra em horário de pico", False),
        ("Material", "Pedido chega com endereço sem complemento", "Endereço sem complemento",
         "O formulário não exige o campo", "Alta", "Contar os atrasos com endereço incompleto", "C",
         "Endereço incompleto em 15% dos atrasos", True),
        ("Material", "Bolsas térmicas insuficientes", "Bolsas térmicas insuficientes",
         None, "Baixa", "Contar bolsas e entregadores no pico", "D", "Há bolsas para todos os entregadores", False),
        ("Medição", "Tempo de entrega medido só pela média do dia", "Tempo medido pela média do dia",
         "O relatório padrão do aplicativo não separa por horário", "Média", "Refazer o indicador por faixa de horário", "C",
         "No prazo: 91% fora do pico e 68% no pico. A média do dia, de 82%, escondia o pico", True),
        ("Medição", "Prazo prometido igual para todos os bairros", "Prazo igual para todos os bairros",
         None, "Média", "Comparar os atrasos por distância", "N", None, False),
        ("Meio ambiente", "Obras na avenida principal", "Obras na avenida principal",
         None, "Média", "Comparar rotas com e sem passagem pela avenida", "D", "Atraso igual nas rotas sem obra", False),
        ("Meio ambiente", "Chuva nas noites de pico", "Chuva nas noites de pico",
         None, "Baixa", "Cruzar os atrasos com os dias de chuva", "N", None, False),
    ]),
    "whys": {
        "B1": ["Não há entregador disponível no pico", "A escala tem o mesmo número de entregadores todos os dias",
               "A escala foi montada pelo movimento médio da semana", "Os pedidos não são analisados por faixa de horário"],
        "A1": ["Cada pedido sai assim que fica pronto", "A expedição não separa os pedidos por zona",
               "Não há regra de agrupamento nem lugar para os pedidos esperarem"],
    },
    "raiz": {"B1": "Os pedidos não são analisados por faixa de horário, e a escala não acompanha o pico.",
             "A1": "A expedição não tem regra nem espaço para agrupar os pedidos por zona."},
    # causas que não produzem o efeito, mas explicam por que ele não foi percebido antes (T61)
    "nao_deteccao": ["E1"],
    "pareto": [("Pizza pronta esperando entregador", 46), ("Fila no forno", 27), ("Endereço incompleto", 15),
               ("Trânsito ou obras", 5), ("Outros motivos", 7)],
}

C2 = ["Procedimentos", "Pessoas", "Sistemas", "Informações", "Indicadores", "Ambiente"]
EX2 = {
    "head": dict(tema="Requisições de compra devolvidas", resp="Gerente de Suprimentos", area="Distribuidora de materiais elétricos · Compras",
                 data=date(2026, 6, 26), autor="Equipe de compras", versao="1.0",
                 efeito="40% das requisições de compra são devolvidas ao requisitante.",
                 onde="Todas as áreas requisitantes, no último trimestre", part="Gerente, compradores, dois requisitantes e TI",
                 origem="Ciclo PDCA e Matriz GUT da área"),
    "efeito_curto": ["40% das requisições", "de compra são", "devolvidas"],
    "cats": C2,
    "causas": _mk(C2, [
        ("Procedimentos", "Formulário de requisição sem campos obrigatórios", "Formulário sem campos obrigatórios",
         "O formulário foi criado antes do sistema atual", "Alta", "Analisar 100 requisições devolvidas", "C",
         "72 das 100 tinham campo essencial em branco", True),
        ("Procedimentos", "Procedimento não define quem confere a especificação", "Conferência sem dono definido",
         None, "Média", "Entrevistar compradores e requisitantes", "N", None, False),
        ("Pessoas", "Requisitantes nunca foram treinados no processo de compras", "Requisitantes sem treinamento",
         "A integração não inclui o processo de compras", "Alta", "Conferir os registros de treinamento", "C",
         "Nenhum dos 38 requisitantes foi treinado", True),
        ("Pessoas", "Troca frequente de requisitantes nas áreas", "Troca frequente de requisitantes",
         None, "Baixa", "Levantar as trocas dos últimos 12 meses", "D", "Só 3 trocas em 12 meses", False),
        ("Sistemas", "Sistema aceita a descrição do item em texto livre", "Descrição do item em texto livre",
         "Não há catálogo de itens cadastrado", "Alta", "Comparar as descrições de um mesmo item", "C",
         "Um mesmo rolamento com 9 descrições diferentes", True),
        ("Sistemas", "Sistema lento no fechamento do mês", "Sistema lento no fim do mês",
         None, "Baixa", "Comparar as devoluções por semana do mês", "D", "Devoluções iguais ao longo do mês", False),
        ("Informações", "Desenhos técnicos desatualizados na rede", "Desenhos técnicos desatualizados",
         None, "Média", "Conferir uma amostra de 20 desenhos", "N", None, False),
        ("Informações", "Requisitante não conhece o prazo de cada tipo de compra", "Prazos de compra desconhecidos",
         "Os prazos não estão publicados", "Média", "Perguntar a 10 requisitantes", "C",
         "8 em 10 não souberam informar. Tratado em outro plano", False),
        ("Indicadores", "Devoluções não são medidas por área requisitante", "Devoluções sem medição por área",
         "O relatório mostra só o total do mês", "Média", "Verificar os relatórios disponíveis", "C",
         "Só existe o total mensal", True),
    ]),
    "whys": {
        "A1": ["O requisitante deixa a especificação técnica em branco", "O formulário aceita o envio sem esse campo",
               "O formulário foi criado antes do sistema atual e nunca foi revisado"],
        "C1": ["Cada requisitante descreve o item de um jeito", "O sistema aceita texto livre na descrição",
               "Não há catálogo de itens cadastrado"],
    },
    "raiz": {"A1": "O formulário não foi revisado quando o sistema mudou e não tem campos obrigatórios.",
             "C1": "Falta um catálogo de itens, com descrições padronizadas."},
}

EX3 = {
    "efeito_curto": ["3 de 25 instrumentos", "em uso com a", "calibração vencida"],
    "cats": M6,
    "causas": _mk(M6, [
        ("Método", "Vencimentos controlados em planilhas de cada setor", "Controle em planilhas locais",
         None, "Alta", "Levantar os controles existentes", "C", "Quatro planilhas, com formatos diferentes", True),
        ("Método", "Procedimento não prevê suplente para o controle", "Controle sem suplente",
         None, "Alta", "Ler o procedimento vigente", "C", "O texto cita só um responsável", True),
        ("Mão de obra", "Responsável pelo controle mudou de área", "Responsável mudou de área",
         None, "Alta", "Conferir a data da mudança e a da última atualização", "C",
         "Planilha sem atualização desde a mudança", False),
        ("Mão de obra", "Usuários não conferem a etiqueta antes do uso", "Etiqueta não conferida no uso",
         None, "Média", "Observar o uso em dois turnos", "N", None, False),
        ("Máquina", "Planilha não emite alerta de vencimento", "Planilha sem alerta de vencimento",
         None, "Alta", "Testar a planilha com datas vencidas", "C", "Nenhum aviso é exibido", True),
        ("Material", "Etiquetas de calibração ilegíveis", "Etiquetas de calibração ilegíveis",
         None, "Baixa", "Conferir as etiquetas dos 25 instrumentos", "D", "Todas as etiquetas legíveis", False),
        ("Medição", "Não há indicador de instrumentos vencidos", "Sem indicador de vencimentos",
         None, "Média", "Verificar os indicadores do sistema de gestão", "C", "O tema não aparece nos indicadores", True),
        ("Meio ambiente", "Laboratório externo com prazo de atendimento longo", "Laboratório externo demorado",
         None, "Baixa", "Conferir os prazos das últimas calibrações", "D", "Prazo médio de 6 dias, dentro do contrato", False),
    ]),
}
