# Ficha de fatos da série: o que é verdade nos exemplos de todos os estudos.
# É lida por testes/coerencia.py. Nasce com a estrutura e as regras iniciais.

def _org():
    return {'identidade': {}, 'pessoas': [], 'processos': [], 'equipamentos': [],
            'documentos': [], 'linha_do_tempo': [], 'numeros': []}

# ---------------------------------------------------------------------------------------------
# Pizzaria. Valores do cânone: o que os estudos dizem depois das correções da leva 1.
# Os itens P01 a P23 e N01 em diante, em DECISOES, dizem o que muda e onde.
# ---------------------------------------------------------------------------------------------
_PIZZARIA = _org()

_PIZZARIA['identidade'] = {
    'nome': 'Pizzaria (loja com salão e delivery)',
    'descricao': 'Pizzaria de bairro, com uma loja: salão, cozinha, expedição e delivery próprio.',
    'escopo': 'Produção e venda de pizzas e bebidas no salão, para retirada e por entrega, e encomendas '
              'para eventos, na loja do bairro (Escopo, rascunho de 08/02/2027; revisado em novembro de 2027).',
    'funcionamento': 'Aberta todos os dias, das 18h à meia-noite: 180 horas no mês (Recursos). O alvará '
                     'permite funcionar até a meia-noite (N04).',
    'turnos': 'Dois turnos. O turno do almoço prepara a massa, recebe os insumos (recebimento às 15h) e '
              'limpa; o turno da noite atende o salão, o balcão e o delivery.',
    'encomendas': 'Encomenda para eventos: a partir de 20 pizzas, com 48 horas de antecedência, de terça a '
                  'domingo, das 18h às 23h (P01).',
    'entrega': 'Até 40 minutos na área de entrega; retirada no balcão em até 25 minutos.',
    'politica': 'Entregar a pizza certa, quente e no prazo, cuidar da segurança do alimento e de quem '
                'trabalha, e ouvir o cliente para melhorar todo mês (Objetivos, 19/02/2027).',
    'norma': 'Segue a numeração da ISO 9001:2015 até a certificação, feita já pela edição de 2026.',
    'certificacao': 'Sem certificado até 2028. Prontidão de 30/11/2027: 79%. Fase 1 em 15/02/2028, '
                    'fase 2 em 21/03/2028, decisão em 25/04/2028: certificado ISO 9001:2026 válido até '
                    '24/04/2031. Não tem transição a fazer.',
    'canais': 'Salão (um terço dos clientes), balcão, telefone, aplicativo de mensagens, site e aplicativo '
              'de delivery (mais da metade dos pedidos, em Partes interessadas; 70% dos pedidos do delivery, na SWOT).',
    'turnos_nota': 'O horário de atendimento vem de Recursos; o papel do turno do almoço é dedução da ficha '
                   '(Auditoria, Técnica de auditoria e Certificação citam pessoas "do turno do almoço"; a Técnica '
                   'registra o recebimento às 15h). Nenhum estudo precisa mudar.',
}

_PIZZARIA['pessoas'] = [
    {'nome': None, 'cargo': 'Dono da loja', 'desde': None,
     'papel': 'Dono do processo G1; conduz a análise crítica; aprova os documentos de gestão.'},
    {'nome': 'Marina', 'cargo': 'Gerente da loja', 'desde': '2022-03',
     'papel': 'Dona de G2, P4, A1 e A3; responsável pela maioria dos exemplos.'},
    {'nome': None, 'cargo': 'Atendente líder', 'desde': None,
     'papel': 'Dono do P1, Registrar o pedido; reclamações e pesquisa de satisfação.'},
    {'nome': 'Carla', 'cargo': 'Atendente', 'desde': '2023-08', 'papel': ''},
    {'nome': 'Diego', 'cargo': 'Atendente', 'desde': '2026-05', 'papel': 'Duas lacunas em 12/02/2027.'},
    {'nome': 'Rafael', 'cargo': 'Pizzaiolo líder', 'desde': '2021-06',
     'papel': 'Dono de P2 e A2. Há seis anos na loja (P04). Só ele regula o forno e a chama do lastro '
              '(K-01); muda de cidade em agosto de 2027.'},
    {'nome': 'Bruno', 'cargo': 'Pizzaiolo', 'desde': '2025-11',
     'papel': 'Treinado no forno em 20/01/2027: resultado parcial, regula a temperatura em turno normal, '
              'mas não reacende nem regula a chama do lastro; nível 1 em C3 (P03).'},
    {'nome': 'Sérgio', 'cargo': 'Líder da expedição', 'desde': '2022-09', 'papel': 'Dono do P3, Entregar o pedido.'},
    {'nome': 'Paulo', 'cargo': 'Entregador', 'desde': '2024-02', 'papel': ''},
    {'nome': 'Igor', 'cargo': 'Entregador', 'desde': '2026-09',
     'papel': 'O entregador que a auditoria 2026-03 encontrou sem treinamento; IT-EXP-01 parcial.'},
    {'nome': None, 'cargo': 'Equipe no pico de sexta (Recursos, abril de 2027)', 'desde': None,
     'papel': '2 atendentes, 3 pizzaiolos, 1 forneiro (faltando 1), 2 na expedição, 8 entregadores '
              '(faltando 2) e 3 no salão. A matriz de Competências mostra só as oito pessoas acima (P02).'},
]

_PIZZARIA['processos'] = [
    {'codigo': 'G1', 'nome': 'Planejar e dirigir a loja', 'tipo': 'Gestão', 'dono': 'Dono da loja',
     'indicador': 'Objetivos alcançados no ano'},
    {'codigo': 'G2', 'nome': 'Medir e melhorar', 'tipo': 'Gestão', 'dono': 'Gerente da loja',
     'indicador': 'Indicadores na meta'},
    {'codigo': 'P1', 'nome': 'Registrar o pedido', 'tipo': 'Principal', 'dono': 'Atendente líder',
     'indicador': 'Pedidos refeitos por erro (P11)'},
    {'codigo': 'P2', 'nome': 'Produzir e embalar', 'tipo': 'Principal', 'dono': 'Pizzaiolo líder',
     'indicador': 'Desperdício de insumos'},
    {'codigo': 'P3', 'nome': 'Entregar o pedido', 'tipo': 'Principal', 'dono': 'Líder da expedição',
     'indicador': 'Entregas em até 40 minutos'},
    {'codigo': 'P4', 'nome': 'Atender no salão', 'tipo': 'Principal', 'dono': 'Gerente da loja',
     'indicador': 'Sem indicador em 14/10/2026; definido até 24/02/2027 (O5)'},
    {'codigo': 'A1', 'nome': 'Comprar e armazenar insumos', 'tipo': 'Apoio', 'dono': 'Gerente da loja',
     'indicador': 'Definido até 24/02/2027 (O5)'},
    {'codigo': 'A2', 'nome': 'Manter equipamentos e motos', 'tipo': 'Apoio', 'dono': 'Pizzaiolo líder',
     'indicador': 'Definido até 24/02/2027 (O5)'},
    {'codigo': 'A3', 'nome': 'Treinar a equipe', 'tipo': 'Apoio', 'dono': 'Gerente da loja',
     'indicador': 'Definido até 24/02/2027 (O5)'},
    {'codigo': None, 'nome': 'Terceirizados', 'tipo': 'Externo', 'dono': None,
     'indicador': 'Pagamento pelo aplicativo, controle de pragas e manutenção do forno.'},
]

_PIZZARIA['equipamentos'] = [
    # instrumentos de medição (Calibração, leitura de 31/03/2027)
    {'codigo': 'TER-01', 'descricao': 'Termômetro de espeto, expedição: pizza na saída, no mínimo 65 °C; padrão interno das verificações',
     'criterio': 'Verificação interna todo mês, ±1 °C', 'situacao': 'Verificado em 05/03/2027; próxima 05/04/2027', 'datas': ['2027-03-05']},
    {'codigo': 'TER-02', 'descricao': 'Termômetro de visor da câmara fria, 0 a 5 °C',
     'criterio': 'Verificação interna a cada 3 meses, ±1 °C',
     'situacao': 'Reprovado em 15/03/2027 (-2 °C contra o TER-01), retirado: fora de uso', 'datas': ['2027-03-15']},
    {'codigo': 'TER-03', 'descricao': 'Termômetro do forno, 280 a 320 °C',
     'criterio': 'Calibração externa a cada 12 meses, ±5 °C',
     'situacao': 'Certificado 1442/26 de 15/06/2026; próxima 15/06/2027', 'datas': ['2026-06-15']},
    {'codigo': 'TER-04', 'descricao': 'Termômetro de espeto do recebimento: insumos refrigerados até 7 °C',
     'criterio': 'Verificação interna todo mês, ±1 °C',
     'situacao': 'Nunca verificado; mediu a muçarela recusada a 9 °C (PNC 2027-16)', 'datas': []},
    {'codigo': 'TER-05', 'descricao': 'Termômetro de visor da câmara fria, novo, no lugar do TER-02 (P20)',
     'criterio': 'Verificação interna a cada 3 meses, ±1 °C',
     'situacao': 'Verificado contra o TER-01 e instalado em 15/03/2027; próxima 15/06/2027; em dia em 31/03/2027',
     'datas': ['2027-03-15']},
    {'codigo': 'BAL-01', 'descricao': 'Balança da bancada, 1 g: bola de massa de 380 a 420 g',
     'criterio': 'Verificação interna todo mês com peso-padrão de 500 g, ±2 g',
     'situacao': 'Verificada em 01/03/2027 (FR-07); próxima 01/04/2027', 'datas': ['2027-03-01']},
    {'codigo': 'BAL-02', 'descricao': 'Balança do recebimento',
     'criterio': 'Calibração externa a cada 12 meses, ±10 g',
     'situacao': 'Certificado 0187/27 de 20/01/2027; próxima 20/01/2028', 'datas': ['2027-01-20']},
    # infraestrutura (Recursos, abril de 2027; meta de disponibilidade 97%)
    {'codigo': 'FOR-01', 'descricao': 'Forno de lastro a gás, único; reserva: forno elétrico com metade da capacidade',
     'criterio': 'Preventiva todo mês', 'situacao': '1 quebra, 3 h em abril (26/04: chama apagando, sem causa)', 'datas': ['2027-04-02', '2027-04-26']},
    {'codigo': 'CAM-01', 'descricao': 'Câmara fria',
     'criterio': 'Preventiva a cada 3 meses (P05)',
     'situacao': 'Revisão de 10/04/2027 não feita; quebra em 12/04/2027 (capacitor, 9 h, câmara a 11 °C); '
                 'alarme instalado em 13/04/2027; revisão remarcada para 05/05/2027',
     'datas': ['2027-01-10', '2027-04-12', '2027-04-13']},
    {'codigo': 'MAS-01', 'descricao': 'Masseira', 'criterio': 'Preventiva a cada 6 meses', 'situacao': 'Em dia', 'datas': ['2026-11-15']},
    {'codigo': 'MOT-01', 'descricao': 'Moto de entrega 1', 'criterio': 'Revisão todo mês', 'situacao': 'Em dia', 'datas': ['2027-04-05']},
    {'codigo': 'MOT-02', 'descricao': 'Moto de entrega 2', 'criterio': 'Revisão todo mês',
     'situacao': 'Corrente partiu em 19/04/2027, 12 h parada: 93,3%, abaixo da meta', 'datas': ['2027-04-05', '2027-04-19']},
    {'codigo': 'MOT-03', 'descricao': 'Moto de entrega 3', 'criterio': 'Revisão todo mês',
     'situacao': 'Sem revisão desde 15/02/2027', 'datas': ['2027-02-15']},
    {'codigo': 'SIS-01', 'descricao': 'Sistema de pedidos, trocado em julho de 2026; atualização de versão em 01/04/2027 (P06)',
     'criterio': 'Preventiva todo mês', 'situacao': 'Fora do ar em 16/04/2027, das 20h às 21h30',
     'datas': ['2027-04-01', '2027-04-16']},
    {'codigo': 'EXA-01', 'descricao': 'Coifa e exaustão', 'criterio': 'Preventiva a cada 3 meses', 'situacao': 'Em dia', 'datas': ['2027-03-20']},
    {'codigo': 'SEL-01', 'descricao': 'Seladora de embalagens', 'criterio': 'Sem preventiva', 'situacao': 'Sem plano', 'datas': []},
]

_PIZZARIA['documentos'] = [
    # lista mestra (Informação documentada, levantamento de 22/01/2027), com o cânone de P08 e P09
    {'codigo': 'IT-EXP-01', 'titulo': 'Expedição e agrupamento por zona; inclui a montagem e a conferência do pedido (item 5)',
     'revisao': '2', 'data': '2026-07-31', 'nota': 'P09. Próxima revisão 07/2028. Lição L-01 incorporada em 15/03/2027.'},
    {'codigo': 'IT-ATE-01', 'titulo': 'Roteiro de atendimento por telefone e mensagens', 'revisao': '2', 'data': '2026-10-08',
     'nota': 'Revisão 1 de março de 2026; revisão 2 pela ação 2 do RNC 2026-05.'},
    {'codigo': 'IT-PRO-01', 'titulo': 'Rotina de controle de temperatura (duas vezes por turno)', 'revisao': '1', 'data': '2026-09-30', 'nota': ''},
    {'codigo': 'IT-PRO-02', 'titulo': 'Regulagem do forno e da chama do lastro', 'revisao': None, 'data': None,
     'nota': 'Código novo (P08), no lugar de "IT-08"; pendente desde a lição L-05, de 26/04/2027.'},
    {'codigo': 'IT-SAL-01', 'titulo': 'Instrução do salão', 'revisao': '2', 'data': '2027-02-10',
     'nota': 'A revisão 1 continuava no balcão em 18/03/2027 e em 30/11/2027.'},
    {'codigo': 'IT-CAI-01', 'titulo': 'Fechamento de caixa', 'revisao': '1', 'data': '2025-03-12', 'nota': 'Obsoleto, na gaveta do caixa.'},
    {'codigo': 'PR-GES-01', 'titulo': 'Rotina de documentos', 'revisao': '3', 'data': '2026-10-14',
     'nota': 'Revisão 3, item 4: conferir os documentos ligados (ação 3 do RNC 2026-05).'},
    {'codigo': 'MP-01', 'titulo': 'Mapa de processos', 'revisao': '1', 'data': '2026-10-14', 'nota': ''},
    {'codigo': 'MP-02', 'titulo': 'Matriz de riscos do delivery', 'revisao': '1', 'data': '2026-10-05',
     'nota': 'Revista a cada seis meses: revisão marcada para 05/04/2027 (P12).'},
    {'codigo': 'FR-01', 'titulo': 'Relatório de auditoria interna', 'revisao': None, 'data': None,
     'nota': 'Código novo (P08): o primeiro FR- livre da pizzaria. Entra na lista mestra.'},
    {'codigo': 'FR-02', 'titulo': 'Planilha de temperatura', 'revisao': None, 'data': None, 'nota': 'Entra na lista mestra (P08).'},
    {'codigo': 'FR-03', 'titulo': 'Ficha de alergênicos', 'revisao': '1', 'data': '2026-10-16', 'nota': ''},
    {'codigo': 'FR-04', 'titulo': 'Planilha de descarte de insumos', 'revisao': '1', 'data': '2026-08-03', 'nota': ''},
    {'codigo': 'FR-05', 'titulo': 'Ficha de treinamento', 'revisao': '1', 'data': '2026-07-10', 'nota': 'Sem aprovação em 22/01/2027.'},
    {'codigo': 'FR-06', 'titulo': 'Registro de não conformidade', 'revisao': None, 'data': None, 'nota': 'Entra na lista mestra (P08).'},
    {'codigo': 'FR-07', 'titulo': 'Planilha de verificação dos instrumentos', 'revisao': None, 'data': None,
     'nota': 'Só a planilha de verificação (P08). Fica fora da lista mestra de 22/01/2027, como hoje.'},
    {'codigo': 'FR-08', 'titulo': 'Ata da análise crítica', 'revisao': None, 'data': None, 'nota': 'Entra na lista mestra (P08).'},
    {'codigo': 'RC-01 a RC-24', 'titulo': 'Receitas padrão das pizzas', 'revisao': None, 'data': None,
     'nota': 'Sem código no levantamento de 22/01/2027; codificadas depois (Conhecimento, 31/05/2027).'},
    {'codigo': 'CT-02', 'titulo': 'Contingência da câmara fria, na porta da câmara', 'revisao': None, 'data': '2027-04-13',
     'nota': 'Escrita em 13/04/2027 e incorporada em 20/04/2027 (P19).'},
    {'codigo': None, 'titulo': 'Escala padrão de entregadores; Cardápio (2026-2, 01/07/2026)', 'revisao': None, 'data': None,
     'nota': 'Sem código no levantamento de 22/01/2027.'},
    {'codigo': None, 'titulo': 'Plano de controle da cozinha e da expedição', 'revisao': '2', 'data': '2027-03-01', 'nota': 'Sete controles, K1 a K7.'},
]

_PIZZARIA['linha_do_tempo'] = [
    ('2026-06-15', 'Ciclo PDCA dos atrasos aberto: 82% das entregas em até 40 minutos', ['PDCA', 'Caso-Integrado']),
    ('2026-07-10', 'Pareto da folha de 15/06 a 09/07/2026: 200 atrasos em 1.110 entregas', ['Pareto', 'Caso-Integrado']),
    ('2026-07', 'Troca do sistema de pedidos, sem teste e sem treinamento (P06)', ['Indicadores', 'Analise-Critica', 'ISO-9001', 'Partes-Interessadas']),
    ('2026-07-17', 'Ishikawa: 12 hipóteses, 5 confirmadas, 4 seguem para o plano (P22)', ['Ishikawa', 'Caso-Integrado']),
    ('2026-07-24', 'Plano 5W2H: seis ações, A1 a A6 (P22)', ['5W2H', 'Caso-Integrado']),
    ('2026-07-31', 'IT-EXP-01 revisão 2, no início do agrupamento por zona (P09, N01)', ['Informacao-Documentada', 'Nao-Conformidade']),
    ('2026-09-06', 'Fim da verificação do PDCA: 95,5% nas semanas 9 a 12; padronização até 15/09', ['PDCA', 'Caso-Integrado']),
    ('2026-09', 'Auditoria interna 2026-03, do delivery: 2 NC menores e 1 oportunidade', ['Auditoria', 'Analise-Critica', 'Competencias']),
    ('2026-09-25', 'RNC 2026-05 aberto; encerrado como eficaz em 10/11/2026', ['Nao-Conformidade']),
    ('2026-09-29', 'Matriz GUT dos problemas do trimestre', ['GUT', 'Caso-Integrado']),
    ('2026-10-02', 'Diagnóstico da ISO 9001 (68% hoje; a T13 recalcula)', ['ISO-9001', 'Analise-Critica']),
    ('2026-10-05', 'Matriz de riscos do delivery (MP-02)', ['Riscos']),
    ('2026-10-06', 'Leitura dos indicadores de out/2025 a set/2026 (terça-feira)', ['Indicadores', 'Caso-Integrado']),
    ('2026-10-09', 'Renovação da licença sanitária protocolada; PDCA da margem do delivery aberto', ['Partes-Interessadas']),
    ('2026-10-14', 'Mapa de processos (MP-01) e rotina de documentos revisão 3', ['Processos', 'Informacao-Documentada']),
    ('2026-10-23', 'Partes interessadas: 11 listadas, 9 pertinentes', ['Partes-Interessadas']),
    ('2026-12-14', 'Primeira análise crítica: oito decisões, R$ 11.100 aprovados', ['Analise-Critica', 'Escopo', 'Caso-Integrado']),
    ('2026-12-15', 'Homologação do segundo fornecedor de queijo (P2); os demais em 18/12/2026 (P13)', ['Fornecedores']),
    ('2027-01-20', 'Treinamento de Bruno no forno: parcial (P03)', ['Competencias', 'Objetivos']),
    ('2027-01-22', 'Levantamento da lista mestra: 17 documentos e 8 registros (P08)', ['Informacao-Documentada']),
    ('2027-02-08', 'Primeiro escopo escrito (rascunho)', ['Escopo']),
    ('2027-02-12', 'Matriz de competências', ['Competencias']),
    ('2027-02-15', 'Primeira avaliação de fornecedores (agosto de 2026 a janeiro de 2027)', ['Fornecedores']),
    ('2027-02-19', 'Objetivos de 2027', ['Objetivos', 'Caso-Integrado']),
    ('2027-03-12', 'Tempo de forno de 7 para 6 minutos, sem análise', ['Producao']),
    ('2027-03-15', 'TER-02 reprovado; TER-05 instalado (P20)', ['Calibracao', 'Tecnica-Auditoria']),
    ('2027-03-18', 'Auditoria interna 2027-02, do salão e do recebimento', ['Tecnica-Auditoria']),
    ('2027-03-22', 'RNC 2027-03, sabor trocado repetido (P10)', ['Liberacao']),
    ('2027-03-26', 'Escala do pico revista: mais dois entregadores extras nas sextas e nos sábados (N07)', ['Producao', 'Objetivos']),
    ('2027-04-01', 'Atualização de versão do sistema de pedidos (P06)', ['Recursos', 'Conhecimento', 'ISO-9001-2026']),
    ('2027-04-03', 'RNC 2027-04, pizza fria no condomínio', ['Partes-Interessadas', 'Satisfacao']),
    ('2027-04-12', 'Quebra da câmara fria; registro de produto não conforme 2027-27', ['Recursos', 'Conhecimento']),
    ('2027-05-07', 'Objetivos lidos; portarias dos condomínios reavaliadas', ['Objetivos', 'Partes-Interessadas']),
    ('2027-05-31', 'Mapa do conhecimento; projeto P-03 da pizza vegana lido', ['Conhecimento', 'Projeto']),
    ('2027-06-14', 'Segunda análise crítica: segundo forno, escala nova da sexta e decisão de certificar', ['Caso-Integrado', 'Certificacao']),
    ('2027-08', 'O pizzaiolo líder, Rafael, sai da loja', ['Conhecimento', 'Caso-Integrado']),
    ('2027-11-30', 'Prontidão para a certificação: 79%', ['Certificacao']),
    ('2028-01-05', 'Diagnóstico das mudanças da ISO 9001:2026', ['ISO-9001-2026']),
    ('2028-02-15', 'Fase 1 da certificação', ['Certificacao', 'ISO-9001-2026']),
    ('2028-04-25', 'Decisão de certificação, ISO 9001:2026', ['Certificacao']),
]

_PIZZARIA['numeros'] = [
    ('Entregas em até 40 minutos', 'Meta de 95% em 2026 e de 96% em 2027 (O1). Série semanal do PDCA, de 15/06/2026: '
     '81, 83, 80, 84, 82, 82, 86, 90, 94, 96, 95, 97. Mensal (Indicadores, P07): jun/26 81, jul/26 84, ago/26 96, '
     'set/26 95; média de out/25 a set/26: 84,4. 2027: jan 95, fev 94, mar 96, abr 95.'),
    ('Atrasos no Pareto', '200 atrasos em 1.110 entregas, de 15/06 a 09/07/2026 (82,0% no prazo); 140 nas sextas e nos '
     'sábados. Depois das ações: 62 em 1.380, de 10/08 a 06/09/2026 (95,5%). No prazo: 91% fora do pico e 68% no pico (P22).'),
    ('Reclamações por 100 pedidos', 'Meta até 2,0 em 2026 (Indicadores) e 1,5 em 2027 (O2, P19). Out/25 3,4; set/26 1,9; '
     'nov/26 1,7; 2027: jan 1,9, fev 1,9, mar 1,6, abr 1,4.'),
    ('Pedidos refeitos por erro', 'Meta 1,5%, limite 2,5%. Set/26 2,0; nov/26 1,4; 2027: jan 1,6, fev 1,5, mar 1,4, abr 1,3.'),
    ('Desperdício de insumos', 'Meta 4,0% em 2026 e 3,5% em 2027 (O6). Set/26 3,9; 2027: jan 3,9, fev 4,0, mar 3,8, abr 3,9.'),
    ('Pesquisa de satisfação', 'Meta 4,3. Fev/27 4,33; mar 4,43; abr 4,53. Pedidos de delivery: fev 840, mar 910, abr 870.'),
    ('Processos com indicador e meta', '5 de 9 em 14/10/2026; 9 de 9 em 24/02/2027.'),
    ('Disponibilidade dos equipamentos', 'Meta de 97%; 180 horas programadas no mês (720 h para a câmara fria).'),
    ('Diagnóstico da ISO 9001', '02/10/2026: 45 requisitos, 21 atendidos, 19 em parte, 5 não atendidos, 68%. '
     'O item T13 (5.1.1 em parte) recalcula esses números na tarefa 4.'),
    ('Lista mestra', '17 documentos e 8 registros em 22/01/2027 (P08).'),
    ('Instrumentos', '7 cadastrados em 31/03/2027 (P20).'),
]

ORGS = {'pizzaria': _PIZZARIA, 'industria': _org(), 'distribuidora': _org()}

# organização -> código -> significado
CODIGOS = {
    'pizzaria': {
        # documentos (P08: instruções no padrão IT-XXX-00; FR-07 só a planilha de verificação)
        'IT-EXP-01': 'Instrução de expedição e agrupamento por zona, com a montagem e a conferência do pedido',
        'IT-ATE-01': 'Roteiro de atendimento por telefone e mensagens',
        'IT-PRO-01': 'Rotina de controle de temperatura',
        'IT-PRO-02': 'Instrução de regulagem do forno e da chama do lastro',
        'IT-SAL-01': 'Instrução do salão',
        'IT-CAI-01': 'Instrução de fechamento de caixa (obsoleta)',
        'PR-GES-01': 'Procedimento: rotina de documentos',
        'MP-01': 'Mapa de processos',
        'MP-02': 'Matriz de riscos do delivery',
        'FR-01': 'Relatório de auditoria interna',
        'FR-02': 'Planilha de temperatura da câmara fria',
        'FR-03': 'Ficha de alergênicos',
        'FR-04': 'Planilha de descarte de insumos',
        'FR-05': 'Ficha de treinamento',
        'FR-06': 'Registro de não conformidade',
        'FR-07': 'Planilha de verificação dos instrumentos',
        'FR-08': 'Ata da análise crítica',
        'CT-02': 'Contingência da câmara fria',
        # instrumentos de medição
        'TER-01': 'Termômetro de espeto da expedição',
        'TER-02': 'Termômetro de visor da câmara fria (reprovado em 15/03/2027)',
        'TER-03': 'Termômetro do forno',
        'TER-04': 'Termômetro de espeto do recebimento',
        'TER-05': 'Termômetro de visor da câmara fria, novo (15/03/2027)',
        'BAL-01': 'Balança da bancada',
        'BAL-02': 'Balança do recebimento',
        # equipamentos e infraestrutura
        'FOR-01': 'Forno de lastro a gás',
        'CAM-01': 'Câmara fria',
        'MAS-01': 'Masseira',
        'MOT-01': 'Moto de entrega 1',
        'MOT-02': 'Moto de entrega 2',
        'MOT-03': 'Moto de entrega 3',
        'SIS-01': 'Sistema de pedidos',
        'EXA-01': 'Coifa e exaustão',
        'SEL-01': 'Seladora de embalagens',
    },
    'industria': {},
    'distribuidora': {},
}
# receitas padrão das pizzas, RC-01 a RC-24
CODIGOS['pizzaria'].update({'RC-%02d' % i: 'Receita padrão nº %d' % i for i in range(1, 25)})

# códigos que existem de propósito em mais de uma organização
COMPARTILHADOS = set()

# prefixos de numeração corrida, que não são registrados um a um.
# Pizzaria: as séries corridas têm prefixo de uma letra, que o teste não lê como código:
# encomendas E-31 a E-35, pedidos T-1184 e A-772, projetos P-01 e P-03, conhecimentos K-01 a K-07,
# lições L-01 a L-06, atendimentos A-01 a A-08 e constatações do organismo P-1 a P-4.
SERIES_LIVRES = ()

# {'org', 'serie' ('RNC' ou 'PNC'), 'numero' ('aaaa-nn'), 'data' ('aaaa-mm-dd'), 'assunto', 'estudos'}
# RNC: não conformidade e ação corretiva (10.2). PNC: registro de produto não conforme (8.7).
REGISTROS = [
    # pizzaria · RNC
    {'org': 'pizzaria', 'serie': 'RNC', 'numero': '2026-05', 'data': '2026-09-25',
     'assunto': 'Pedidos por telefone sem complemento do endereço; auditoria 2026-03, constatação 1; '
                'encerrado como eficaz em 10/11/2026',
     'estudos': ['Nao-Conformidade', 'Analise-Critica', 'Informacao-Documentada', 'Pedidos']},
    {'org': 'pizzaria', 'serie': 'RNC', 'numero': '2027-03', 'data': '2027-03-22',
     'assunto': 'Sabor trocado repetido (PNC 2027-15, 2027-20 e 2027-21): ação corretiva; era "RNC 2027-07" (P10)',
     'estudos': ['Liberacao']},
    {'org': 'pizzaria', 'serie': 'RNC', 'numero': '2027-04', 'data': '2027-04-03',
     'assunto': 'Terceira reclamação de pizza fria do mesmo condomínio; entrega na porta combinada em 10/04/2027',
     'estudos': ['Partes-Interessadas', 'Satisfacao']},
    # pizzaria · PNC (Liberação: noites de 15 a 21/03/2027; Recursos: abril de 2027)
    {'org': 'pizzaria', 'serie': 'PNC', 'numero': '2027-14', 'data': '2027-03-15',
     'assunto': 'Pizza a 62 °C na saída em 13/03, vista na leitura de 15/03; aberto sem disposição',
     'estudos': ['Liberacao']},
    {'org': 'pizzaria', 'serie': 'PNC', 'numero': '2027-15', 'data': '2027-03-16',
     'assunto': 'Sabor trocado (pedido 5127), visto na conferência; refugado', 'estudos': ['Liberacao']},
    {'org': 'pizzaria', 'serie': 'PNC', 'numero': '2027-16', 'data': '2027-03-17',
     'assunto': '12 kg de muçarela recebidos a 9 °C; devolvidos ao fornecedor', 'estudos': ['Liberacao']},
    {'org': 'pizzaria', 'serie': 'PNC', 'numero': '2027-17', 'data': '2027-03-18',
     'assunto': '40 bolas de massa com 365 g em média; retrabalhadas', 'estudos': ['Liberacao', 'Histograma-CEP']},
    {'org': 'pizzaria', 'serie': 'PNC', 'numero': '2027-18', 'data': '2027-03-19',
     'assunto': 'Borda queimada, mesa 7 (pedido 5342); aceita sob concessão', 'estudos': ['Liberacao']},
    {'org': 'pizzaria', 'serie': 'PNC', 'numero': '2027-19', 'data': '2027-03-19',
     'assunto': 'Pizza a 61 °C na saída (pedido 5360); retrabalhada', 'estudos': ['Liberacao']},
    {'org': 'pizzaria', 'serie': 'PNC', 'numero': '2027-20', 'data': '2027-03-20',
     'assunto': 'Sabor trocado visto pelo cliente (pedido 5431); substituída; decidido pelo gerente da loja (P16)',
     'estudos': ['Liberacao']},
    {'org': 'pizzaria', 'serie': 'PNC', 'numero': '2027-21', 'data': '2027-03-20',
     'assunto': 'Sabor trocado (pedido 5440), visto na conferência; refugado; leva ao RNC 2027-03', 'estudos': ['Liberacao']},
    {'org': 'pizzaria', 'serie': 'PNC', 'numero': '2027-27', 'data': '2027-04-12',
     'assunto': '18 kg de muçarela e molho descartados na quebra da câmara fria; era "RNC 2027-27" (P10)',
     'estudos': ['Recursos']},
]

# {'id', 'regex', 'motivo', 'pastas' (None = todos os estudos, ou lista de pastas)}
PROIBIDO = [
    {'id': 'I01a', 'regex': r'certificad[oa] há 8 anos', 'motivo': 'tempo de certificação incoerente', 'pastas': None},
    {'id': 'I01b', 'regex': r'com sistema de gestão certificado', 'motivo': 'a organização do exemplo de auditoria ainda não é certificada', 'pastas': ['Auditoria']},
    {'id': 'I02', 'regex': r'(três|3) extrusoras', 'motivo': 'número de extrusoras da indústria', 'pastas': None},
    {'id': 'I03', 'regex': r'Das 9 mudanças de processo de 2027', 'motivo': 'contagem de mudanças de processo', 'pastas': None},
    {'id': 'P01', 'regex': r'não abre às segundas', 'motivo': 'dia de funcionamento da pizzaria', 'pastas': None},
    {'id': 'P04', 'regex': r'há 12 anos na loja', 'motivo': 'tempo de casa da pessoa', 'pastas': None},
    {'id': 'P10a', 'regex': r'RNC 2027-07', 'motivo': 'número de RNC em conflito', 'pastas': None},
    {'id': 'P10b', 'regex': r'RNC 2027-(27|29|30)', 'motivo': 'número de RNC em conflito', 'pastas': ['Recursos']},
    {'id': 'P10c', 'regex': r'RNC 2027-(27|29|30)', 'motivo': 'número de RNC em conflito', 'pastas': ['Histograma-CEP']},
    {'id': 'P23', 'regex': r'mussarela', 'motivo': 'grafia única: muçarela', 'pastas': None},
    {'id': 'T02', 'regex': r'corroborada por duas fontes', 'motivo': 'afirmação a corrigir', 'pastas': None},
    {'id': 'T07', 'regex': r'Não há justificativa possível', 'motivo': 'afirmação absoluta a corrigir', 'pastas': None},
    {'id': 'T19', 'regex': r'A Produção tem o maior número de pendências', 'motivo': 'conclusão que os dados não sustentam', 'pastas': None},
    {'id': 'T41', 'regex': r'Erro, ou correção', 'motivo': 'título a corrigir', 'pastas': None},
    {'id': 'T53', 'regex': r'decidir menos em cada reunião', 'motivo': 'recomendação a corrigir', 'pastas': None},
    {'id': 'T54', 'regex': r'nem toda vira não conformidade', 'motivo': 'afirmação a corrigir', 'pastas': None},
    {'id': 'T56', 'regex': r'três desvios da média das médias|a três desvios da linha central', 'motivo': 'descrição incorreta do limite de controle', 'pastas': None},
    {'id': 'T65', 'regex': r'mais de 100 pontos', 'motivo': 'afirmação numérica a corrigir', 'pastas': None},
    {'id': 'T66', 'regex': r'Resultado ruim sem decisão é uma não conformidade', 'motivo': 'afirmação a corrigir', 'pastas': None},
    {'id': 'D01', 'regex': r'\b29 estudos', 'motivo': 'a série tem 34 estudos', 'pastas': None},
    {'id': 'D02', 'regex': r'estava em preparação', 'motivo': 'o estudo já está publicado', 'pastas': None},
    {'id': 'D03', 'regex': r'ainda não têm estudo próprio', 'motivo': 'os estudos já existem', 'pastas': None},
    {'id': 'D05', 'regex': r'as três ferramentas trabalham', 'motivo': 'contagem de ferramentas a corrigir', 'pastas': None},
]

# {'id', 'conflito', 'canone', 'estudos'}
# 'estudos' são as pastas a ajustar. Quando a ficha acrescenta uma pasta à lista do spec, o 'canone' diz.
DECISOES = [
    # ---------------------------------------------------------------- pizzaria (spec, seção 6.1)
    {'id': 'P01',
     'conflito': 'A loja "não abre às segundas", com registros em 08, 15 e 22/03/2027, que são segundas.',
     'canone': 'A loja abre todos os dias, das 18h à meia-noite. Só a encomenda para eventos (a partir de 20 pizzas, '
               'com 48 horas de antecedência) é atendida de terça a domingo, das 18h às 23h. Na oferta de Pedidos, '
               '"de terça a domingo" fica só na linha da encomenda para eventos. A recusa da E-33 passa a "A loja não '
               'atende encomendas para eventos às segundas, e o horário de encomenda começa às 18h."',
     'estudos': ['Pedidos']},
    {'id': 'P02',
     'conflito': 'Oito pessoas em Competências; equipe bem maior em Recursos; "quatro pizzaiolos" em Conhecimento.',
     'canone': 'Vale Recursos: no pico de sexta, 2 atendentes, 3 pizzaiolos, 1 forneiro, 2 na expedição, 8 entregadores '
               'e 3 no salão, além do gerente. A matriz de Competências continua com as oito pessoas dos postos-chave '
               '(Marina, Carla, Diego, Rafael, Bruno, Sérgio, Paulo e Igor), e o texto diz que ela não é a loja inteira. '
               'Em Conhecimento (questionário e figura), "quatro pizzaiolos" passa a "os três pizzaiolos e o forneiro"; '
               'o K-03 continua com 4 pessoas que sabem.',
     'estudos': ['Competencias', 'Conhecimento']},
    {'id': 'P03',
     'conflito': 'Bruno regula o forno sozinho em fevereiro de 2027; em maio, só o pizzaiolo líder sabe.',
     'canone': 'Valem Conhecimento e Caso integrado: em maio de 2027, só Rafael regula o forno e a chama do lastro. Em '
               'Competências, a ação 1 do plano (Bruno, C3) passa a "Parcial: reforçar", com a evidência "Regula a '
               'temperatura em turno normal. Não reacende nem regula a chama do lastro, e a regulagem segue sem registro. '
               'Risco R6 continua aberto." O nível de Bruno em C3 fica em 1 (não sobe para 2), e as contagens de lacunas '
               'e o texto do "O que observar" são refeitos. Objetivos (ação do O7 concluída em 20/01/2027) não muda: a '
               'ação foi feita; a eficácia é que foi parcial.',
     'estudos': ['Competencias']},
    {'id': 'P04',
     'conflito': 'Pizzaiolo líder "há 12 anos" e "desde 06/2021".',
     'canone': 'Rafael, pizzaiolo líder, desde 06/2021. Em Conhecimento, "há 12 anos na loja" passa a "há seis anos na loja".',
     'estudos': ['Conhecimento']},
    {'id': 'P05',
     'conflito': 'Alarme da câmara fria com prazo em 11/2026 e ações dadas como concluídas; em 04/2027, "não havia '
                 'alarme". Preventiva semestral e trimestral.',
     'canone': 'Vale Recursos: preventiva da câmara fria (CAM-01) a cada três meses (última em 10/01/2027; a de '
               '10/04/2027 não foi feita); o alarme de temperatura só foi instalado em 13/04/2027, depois da quebra de '
               '12/04. No R3 de Riscos, a resposta passa a "Reduzir. Fazer a manutenção preventiva a cada três meses." '
               'O residual não muda.',
     'estudos': ['Riscos']},
    {'id': 'P06',
     'conflito': 'Sistema de pedidos trocado em julho de 2026 e em abril de 2027.',
     'canone': 'A troca do sistema de pedidos foi em julho de 2026, sem teste e sem treinamento. Em abril de 2027 houve '
               'uma atualização de versão (SIS-01, preventiva de 01/04/2027). Em ISO 9001:2026 (M5: "Atualização de '
               'versão do sistema de pedidos sem plano, em abril de 2027" e o "O que observar"), em Conhecimento (K-05 e '
               'exemplo 3) e em Recursos, o evento de abril de 2027 passa a "atualização de versão do sistema de pedidos".',
     'estudos': ['ISO-9001-2026', 'Conhecimento', 'Recursos']},
    {'id': 'P07',
     'conflito': 'Entregas no prazo: 88 e 94 em junho e julho de 2026, contra 80 a 84 por semana até 26/07.',
     'canone': 'Vale a série semanal do PDCA (semana 1 = 15/06/2026): 81, 83, 80, 84, 82, 82, 86, 90, 94, 96, 95, 97. '
               'Cada mês é a média das semanas que começam nele: jun/26 = semanas 1 a 3 = 81 (81,3); jul/26 = semanas 4 '
               'a 7 = 84 (83,5). Em Indicadores, P1 passa de 88 e 94 para 81 e 84 em jun/26 e jul/26; a série de '
               'out/25 a set/26 fica 81, 83, 80, 82, 82, 83, 82, 84, 81, 84, 96, 95, e a média do ano passa de 85,8 '
               'para 84,4. Ago/26 (96) e set/26 (95) não mudam. Propagar a quem citar 88 ou 94 como valor mensal.',
     'estudos': ['Indicadores']},
    {'id': 'P08',
     'conflito': 'FR-07 é relatório de auditoria e planilha de verificação; formulários da tabela de retenção fora da '
                 'lista mestra; IT-05 e IT-08 fora do padrão.',
     'canone': 'FR-07 é só a planilha de verificação dos instrumentos (Calibração, Técnica de auditoria). O relatório de '
               'auditoria interna passa a FR-01, o primeiro FR- livre da pizzaria. Os formulários da tabela de retenção '
               'entram na lista mestra de 22/01/2027: FR-01 Relatório de auditoria interna, FR-02 Planilha de '
               'temperatura, FR-06 Registro de não conformidade e FR-08 Ata da análise crítica (FR-05 já está). A lista '
               'passa de 13 para 17 documentos; os registros continuam 8; os cinco documentos fora de ordem continuam '
               'cinco. As instruções seguem o padrão IT-XXX-00: em Conhecimento, "IT-05" (montagem e conferência do '
               'pedido, K-04 e L-01) passa a IT-EXP-01, que já cobre a conferência no item 5, e "IT-08" (instrução do '
               'forno, L-05) passa a IT-PRO-02. O "IT-05" de Auditoria é outro documento: ver N02.',
     'estudos': ['Informacao-Documentada', 'Conhecimento']},
    {'id': 'P09',
     'conflito': 'IT-EXP-01 revisão 2 em 10/07/2026, antes do plano de 24/07.',
     'canone': 'IT-EXP-01 revisão 2 em 31/07/2026, no início do agrupamento por zona (ação A4). A próxima revisão '
               'continua 07/2028. A Não conformidade ("revisão 2 da instrução, de julho de 2026") não muda. O 5W2H '
               'ajusta a ação A6: ver N01.',
     'estudos': ['Informacao-Documentada']},
    {'id': 'P10',
     'conflito': '"RNC" usado para duas séries; RNC 2027-04 em 03/04 e RNC 2027-07 em 22/03.',
     'canone': 'Duas séries com nomes diferentes: "RNC" (não conformidade e ação corretiva, 10.2) e "registro de produto '
               'não conforme" (8.7, série PNC na ficha). Os números 2027-27, 2027-29 e 2027-30 são registros de produto '
               'não conforme: em Recursos, "RNC 2027-27" (pizzaria, 12/04/2027) passa a "registro de produto não '
               'conforme 2027-27"; "RNC 2027-29" e "RNC 2027-30" (indústria, bobinas de julho de 2027) passam a '
               '"registro de produto não conforme 2027-29" e "2027-30" em Recursos e em Histograma e CEP. Na série RNC '
               'da pizzaria, o RNC de 22/03/2027 da Liberação passa de 2027-07 a 2027-03, antes do 2027-04 de 03/04/2027.',
     'estudos': ['Recursos', 'Histograma-CEP', 'Liberacao']},
    {'id': 'P11',
     'conflito': '"Pedidos refeitos" é do P1 num estudo e do P2 em outro.',
     'canone': 'Vale Processos: o indicador "Pedidos refeitos por erro" é do P1, Registrar o pedido. Em Objetivos, o '
               'processo do O4 passa de "Produzir e embalar (P2)" a "Registrar o pedido (P1)". O responsável do O4 e a '
               'ação (conferir o pedido na tela antes de montar) continuam com o pizzaiolo líder.',
     'estudos': ['Objetivos']},
    {'id': 'P12',
     'conflito': 'Escopo sem o processo "Atender no salão"; riscos revistos uma vez por ano, contra a revisão semestral; '
                 'dono e gerente misturados.',
     'canone': 'Valem Processos e Caso integrado: nove processos (G1, G2, P1 a P4, A1 a A3), e a linha "Processos" do '
               'Escopo ganha "atender no salão". O compromisso 4 da liderança passa a "Os riscos são revistos a cada seis '
               'meses", frequência "Semestral · Matriz de riscos" (revisões em abril e outubro; a de MP-02 marcada para '
               '05/04/2027). Papéis: o dono da loja dirige a loja (G1), conduz a análise crítica e aprova; o gerente da '
               'loja é dono de G2, P4, A1 e A3 e conduz o dia a dia.',
     'estudos': ['Escopo']},
    {'id': 'P13',
     'conflito': 'Caixas "sem avaliação formal", mas avaliadas; homologações antes da decisão de 14/12/2026; avaliação de '
                 '11/12 para o semestre inteiro; gás crítico com documentos pendentes.',
     'canone': 'Pizzaria: as caixas de pizza (P5) saem da tabela de desempenho, e o total da classe A passa de 5 para 4 '
               '("A: 4 · B: 2"). Homologações depois de 14/12/2026, na mesma ordem de hoje: P2 Queijaria do Campo em '
               '15/12/2026; P1, P3, P4, P5, P6 e P7 em 18/12/2026; todas válidas até 12/2028. O gás (P6), crítico com '
               'documentos pendentes, é comentado no "O que observar". Indústria (exemplo 1 de Fornecedores): a avaliação '
               'do segundo semestre de 2026 passa a ser datada de 11/01/2027 (era 11/12/2026); na análise crítica da '
               'indústria de 18/02/2027, "avaliação de fornecedores de dezembro" passa a "de janeiro" (Análise crítica '
               'acrescentada à lista do spec). Efeito na análise crítica da pizzaria: ver N03.',
     'estudos': ['Fornecedores', 'Analise-Critica']},
    {'id': 'P14',
     'conflito': '"Quatro resolvidos" com duas recusas; "3 das 8 encomendas"; E-34 fora das 48 horas sem comentário.',
     'canone': 'Texto refeito pela tabela de Pedidos: 8 pedidos, 4 aceitos (E-31, T-1184, E-34, E-35), 2 aceitos com '
               'alteração (E-32, T-1201) e 2 recusados (A-772, E-33); 5 são encomendas para eventos (E-31 a E-35). A E-34, '
               'analisada em 26/03 para 27/03 às 20h, foi aceita com menos de 48 horas de antecedência, e o texto diz isso. '
               'A E-33 não teve "outro dia": o cliente recusou.',
     'estudos': ['Pedidos']},
    {'id': 'P15',
     'conflito': 'Frequências do plano de controle que não batem com o número de registros; mudança de 26/03 em registros '
                 'lidos em 15/03; reação do K5 depois da saída.',
     'canone': 'Os totais não mudam: K1 com 14 verificações e K2 a K7 com 7 cada, nas noites de 08 a 14/03/2027 (56 no '
               'total, 6 fora). A frequência escrita passa a corresponder a esses totais: duas leituras por noite no K1 e '
               'um registro por noite nos demais (para K5, a amostra de 20 pedidos no fechamento). A tabela de mudanças no '
               'processo ganha a própria data de leitura, 31/03/2027, e mantém a mudança de 26/03/2027. A reação do K5 é '
               'reescrita para acontecer antes da saída do pedido.',
     'estudos': ['Producao']},
    {'id': 'P16',
     'conflito': 'Decisões tomadas por quem não tem a autoridade escrita; lote 140 liberado sem quem liberou; "segue '
                 'aberto" contra "0 abertos"; "2 fora" com três fora.',
     'canone': 'Em cada registro de produto não conforme, quem decidiu é a função que o cabeçalho de autoridades indica. '
               'Pizzaria: no 2027-20 (troca no cliente), "Atendente líder" passa a "Gerente da loja"; os demais já '
               'seguem o cabeçalho. Indústria: o lote 140 ganha quem liberou e a data, coerentes com o encerramento em '
               '21/05/2027; as frases "segue aberto" e "2 fora" são corrigidas pela tabela.',
     'estudos': ['Liberacao']},
    {'id': 'P17',
     'conflito': 'Entradas E1 e E2 da pizza vegana "atendem" depois de mudanças de ingrediente e alergênico.',
     'canone': 'E1 e E2 recebem nota de reverificação: o "Atende" vale para a receita de 22/04 a 03/05/2027; depois da '
               'troca do queijo vegetal (12/05, marca B) e do recheio (18/05, tofu defumado), a ficha técnica, os rótulos e '
               'o texto de alergênicos precisam ser conferidos de novo.',
     'estudos': ['Projeto']},
    {'id': 'P18',
     'conflito': 'Níveis da Luana e do Felipe diferentes na matriz e no questionário; Camila com lacunas sem ação; Jorge '
                 '"há sete anos" e "desde 10/2020".',
     'canone': 'Vale a matriz de Suprimentos da indústria (12/03/2027): Luana nível 2 em S1, Felipe nível 2 em S7; as '
               'perguntas do questionário sobre os dois passam a ter resposta 2, com o enunciado coerente. Camila tem sete '
               'lacunas, e o plano ganha ações para S6 e S7, as duas que hoje não têm. Jorge, desde 10/2020: "há sete '
               'anos" passa a "há seis anos". (Pessoas da indústria, embora o item seja da série P.)',
     'estudos': ['Competencias']},
    {'id': 'P19',
     'conflito': 'Meta de reclamações 2,0 e 1,5; "prazo de resposta" com dois sentidos; contingência escrita em 13/04 e '
                 'incorporada em 20/04.',
     'canone': 'Vale Objetivos: a meta de reclamações é até 2,0 por 100 pedidos em 2026 (Indicadores) e 1,5 em 2027 (O2). '
               'Em Satisfação, a meta da tabela e do texto passa de 2,0 a 1,5. "Primeira resposta" (o primeiro contato '
               'com o cliente) e "solução" (o caso resolvido) são termos distintos, usados assim em Satisfação e na '
               'política de pós-entrega de Conhecimento. A contingência CT-02 foi escrita em 13/04/2027 e incorporada em '
               '20/04/2027, e o texto diz as duas datas.',
     'estudos': ['Satisfacao', 'Conhecimento']},
    {'id': 'P20',
     'conflito': 'Termômetro novo da câmara fora da lista de instrumentos.',
     'canone': 'O termômetro novo é o TER-05, termômetro de visor da câmara fria, 0 a 5 °C, verificação interna a cada '
               '3 meses (±1 °C), verificado contra o TER-01 e instalado em 15/03/2027, próxima em 15/06/2027, em dia em '
               '31/03/2027. A lista passa de 6 para 7 instrumentos (em dia: de 2 para 3), e a tabela de verificações '
               'ganha a de 15/03/2027 do TER-05, aprovada.',
     'estudos': ['Calibracao']},
    {'id': 'P21',
     'conflito': 'Desperdício e erros com valores diferentes; reunião "toda segunda" numa terça; "três melhoraram" com um '
                 'estável.',
     'canone': 'Vale Indicadores (setembro de 2026). Na GUT de 29/09/2026: P4 passa a "Erros de sabor ou de tamanho em 2% '
               'dos pedidos" (pedidos refeitos: 2,0%) e P5 a "Desperdício de insumos em 3,9% do custo comprado"; as notas '
               'G, U e T não mudam. Em Indicadores, a leitura continua em 06/10/2026, uma terça, e a reunião passa a "Toda '
               'terça-feira, com fechamento mensal". O "O que observar" passa a dizer que dois indicadores melhoraram '
               '(entregas e reclamações), o desperdício ficou estável na meta e os pedidos refeitos sobem.',
     'estudos': ['GUT', 'Indicadores']},
    {'id': 'P22',
     'conflito': '96% e 68% de entregas no prazo não fecham com a folha do Pareto; 8 hipóteses e 3 causas no PDCA, 12 e 5 '
                 'no Ishikawa; três ações contra seis; ordem entre Pareto e Ishikawa; problema ausente da lista da GUT; '
                 'causa raiz sem ação.',
     'canone': 'Valem Pareto, Ishikawa e 5W2H. Hipóteses: 12, com 5 confirmadas (A1, B1, C1, D1, E1), 4 descartadas e 3 '
               'não verificadas; 4 causas seguem para o plano (a fila do forno, C1, fica para o ciclo seguinte). Plano: 6 '
               'ações, A1 a A6. No Ishikawa, a evidência do E1 passa a "No prazo: 91% fora do pico e 68% no pico", tirada '
               'da folha do Pareto (sextas e sábados: 140 atrasos em 444 entregas; demais dias: 60 em 666). Ordem: Pareto '
               '(10/07/2026) antes do Ishikawa (17/07/2026), e o Ishikawa analisa o efeito "18% das entregas depois de 40 '
               'minutos", com a primeira barra do Pareto como dado. A GUT da pizzaria, de 29/09/2026, é posterior ao '
               'ciclo dos atrasos, que se fechou em 06/09/2026: onde um estudo diz que a GUT escolheu o problema dos '
               'atrasos, o texto passa a dizer que o problema veio do indicador, antes da GUT. A causa raiz do B1 ("os '
               'pedidos não são analisados por faixa de horário, e a escala não acompanha o pico") tem ação no 5W2H: a A1 '
               'diz que a escala do pico passa a seguir os pedidos por faixa de horário medidos na A5. No PDCA: "Das '
               'doze hipóteses levantadas, cinco foram confirmadas" e seis ações. Também no Caso integrado (acrescentado '
               'à lista do spec): passo 3, cinco causas confirmadas e quatro para o plano; passo 4, seis ações.',
     'estudos': ['PDCA', 'Ishikawa', 'GUT', '5W2H', 'Caso-Integrado']},
    {'id': 'P23',
     'conflito': '"Muçarela" e "mussarela"; "fora da meta" com dois sentidos; status e situação trocados.',
     'canone': 'Grafia única "muçarela", em todos os estudos. Em Indicadores, "Fora da meta" é só a situação além do '
               'limite de atenção; o resultado que não atinge a meta sem passar do limite é "Atenção", e o sentido geral '
               'se escreve "sem atingir a meta". No 5W2H, "status" é o que o responsável informa (não iniciada, em '
               'andamento, concluída, cancelada) e "situação" é a calculada (no prazo, atrasada, concluída, concluída com '
               'atraso), como no módulo.',
     'estudos': ['Pedidos', 'Recursos', 'Liberacao', 'Calibracao', 'Indicadores', '5W2H']},

    # ---------------------------------------------------------------- pizzaria: contradições novas
    {'id': 'N01',
     'conflito': 'IT-EXP-01 revisão 2 em 31/07/2026 (P09) contra a ação A6 do 5W2H, "Atualizar a instrução de trabalho '
                 'da expedição", de 07/09 a 15/09/2026.',
     'canone': 'Vale a revisão 2 em 31/07/2026 (P09, e a Não conformidade: "de julho de 2026"). No 5W2H, a A6 passa a '
               '"27/07 a 31/07"; o resto da linha não muda. O PDCA não muda: o passo 7, de 15/09/2026, diz que a '
               'instrução foi atualizada, o que continua certo.',
     'estudos': ['5W2H']},
    {'id': 'N02',
     'conflito': 'Em Auditoria (tabela de como escrever a constatação), "A instrução IT-05 pede o registro da temperatura '
                 'a cada turno", com as datas da constatação 2 da auditoria 2026-03 da pizzaria. A rotina de temperatura '
                 'é a IT-PRO-01, duas vezes por turno, e "IT-05" é outro documento em Conhecimento.',
     'canone': 'A frase passa a "A rotina IT-PRO-01 pede o registro da temperatura duas vezes por turno."',
     'estudos': ['Auditoria']},
    {'id': 'N03',
     'conflito': 'Com P13, o segundo fornecedor de queijo (P2) é homologado em 15/12/2026, mas a análise crítica da '
                 'pizzaria de 14/12/2026 diz "O segundo fornecedor foi homologado em novembro" e conta como concluída a '
                 'ação do risco R4 (homologar um segundo fornecedor, até 27/11/2026).',
     'canone': 'Vale P13 (a decisão do spec e da tarefa). Na análise crítica de 14/12/2026: entrada c7 passa a "O segundo '
               'fornecedor de queijo entrega desde novembro, em teste; a homologação foi marcada para dezembro."; entrada '
               'e passa a "Sete riscos com ação: cinco ações concluídas. O treinamento do segundo pizzaiolo, do risco R6, '
               'está atrasado, e a homologação do segundo fornecedor de queijo, do R4, foi marcada para dezembro." A '
               'conclusão da entrada e passa a "Faltam concluir as dos riscos R4 e R6." Alternativa para o autor: manter '
               'o P2 homologado em 20/11/2026, pela ação do R4, e mover só os outros seis para 18/12/2026; nada muda na '
               'análise crítica.',
     'estudos': ['Analise-Critica']},
    {'id': 'N04',
     'conflito': 'Recursos: loja aberta das 18h à meia-noite (180 horas no mês, base das contas de disponibilidade). '
                 'Partes interessadas: "O alvará permite funcionar até 23h30".',
     'canone': 'Vale Recursos, que tem contas conferidas. Em Partes interessadas, a frase passa a "O alvará permite '
               'funcionar até a meia-noite".',
     'estudos': ['Partes-Interessadas']},
    {'id': 'N05',
     'conflito': 'Análise crítica de 14/12/2026: "Dois registros no ano, os dois da auditoria 2026-03", mas o primeiro deles '
                 'é o RNC 2026-05; e "Uma auditoria no ano", mas ela é a 2026-03. Certificação fala em "auditorias de 2026".',
     'canone': 'Valem os números de registro e de auditoria (quatro estudos citam o RNC 2026-05). Na análise crítica, a '
               'entrada c4 passa a "Dois registros abertos pela auditoria 2026-03. O RNC 2026-05 foi encerrado como '
               'eficaz. O segundo está em verificação." e a c6 passa a "A auditoria 2026-03, no delivery: duas não '
               'conformidades menores e uma oportunidade de melhoria. O salão e as compras nunca foram auditados."',
     'estudos': ['Analise-Critica']},
    {'id': 'N06',
     'conflito': 'Volume de pedidos: Liberação conta de 118 a 236 pedidos por noite (15 a 21/03/2027, cerca de 4.800 por '
                 'mês) e numera os pedidos acima de 5.100; Satisfação conta 840 a 910 pedidos por mês (fevereiro a abril '
                 'de 2027) e numera o pedido de 13/03/2027 como 3.104; o Pareto tem uma noite de sábado com 148 entregas '
                 'num período de 1.110 entregas em 25 dias.',
     'canone': 'Não aplicar nesta leva, como os itens da seção 6.3 do spec: acertar o volume exige refazer contas '
               'conferidas em Satisfação, Objetivos, Pareto ou Recursos, e o spec não prevê. Fica registrado para a revisão '
               'do autor.',
     'estudos': []},
    {'id': 'N07',
     'conflito': 'Os dois entregadores extras nas sextas e nos sábados existem desde julho de 2026 (A1 do 5W2H; auditoria '
                 'de setembro de 2026), mas Produção e Objetivos dão "Dois entregadores extras nas sextas e nos sábados" '
                 'como a mudança de 26/03/2027.',
     'canone': 'Em 26/03/2027, a escala do pico ganhou mais dois entregadores extras, além dos dois de 2026. Em Produção '
               '(tabela de mudanças) e em Objetivos (recursos da ação do O1), a frase passa a "Mais dois entregadores '
               'extras nas sextas e nos sábados". Recursos ("mesmo com os extras de março") não muda.',
     'estudos': ['Producao', 'Objetivos']},
]
