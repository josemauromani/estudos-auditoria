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
    'turnos': 'Dois turnos (N22): o da tarde, antes da abertura, sem atendimento a clientes, em que a loja recebe os '
              'insumos (recebimento às 15h, Técnica de auditoria); e o da noite, das 18h à meia-noite, que atende o '
              'salão, o balcão e o delivery. Não existe "turno do almoço".',
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
     'revisao': '2', 'data': '2026-09-15', 'nota': 'P09: fim da ação A6 do 5W2H e etapa 7 do PDCA. Próxima revisão 09/2028. Lição L-01 incorporada em 15/03/2027.'},
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
    {'codigo': 'FR-02', 'titulo': 'Planilha de temperatura', 'revisao': None, 'data': None, 'nota': 'Entra na lista mestra (P08).'},
    {'codigo': 'FR-03', 'titulo': 'Ficha de alergênicos', 'revisao': '1', 'data': '2026-10-16', 'nota': ''},
    {'codigo': 'FR-04', 'titulo': 'Planilha de descarte de insumos', 'revisao': '1', 'data': '2026-08-03', 'nota': ''},
    {'codigo': 'FR-05', 'titulo': 'Ficha de treinamento', 'revisao': '1', 'data': '2026-07-10', 'nota': 'Sem aprovação em 22/01/2027.'},
    {'codigo': 'FR-06', 'titulo': 'Registro de não conformidade', 'revisao': None, 'data': None, 'nota': 'Entra na lista mestra (P08).'},
    {'codigo': 'FR-07', 'titulo': 'Planilha de verificação dos instrumentos', 'revisao': None, 'data': None,
     'nota': 'Só a planilha de verificação (P08). Fica fora da lista mestra de 22/01/2027, como hoje.'},
    {'codigo': 'FR-08', 'titulo': 'Ata da análise crítica', 'revisao': None, 'data': None, 'nota': 'Entra na lista mestra (P08).'},
    {'codigo': 'FR-09', 'titulo': 'Relatório de auditoria interna', 'revisao': None, 'data': None,
     'nota': 'Código novo (P08): o próximo FR- da pizzaria, depois do FR-08. Entra na lista mestra.'},
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
    ('2026-09-06', 'Fim da verificação do PDCA: 95,5% nas semanas 9 a 12; padronização até 15/09', ['PDCA', 'Caso-Integrado']),
    ('2026-09-15', 'IT-EXP-01 revisão 2, com o agrupamento por zona: ação A6 do 5W2H e etapa 7 do PDCA (P09, N01)', ['Informacao-Documentada', 'Nao-Conformidade', '5W2H', 'PDCA']),
    ('2026-09', 'Auditoria interna 2026-03, do delivery: 2 NC menores e 1 oportunidade', ['Auditoria', 'Analise-Critica', 'Competencias']),
    ('2026-09-25', 'RNC 2026-05 aberto; encerrado como eficaz em 10/11/2026', ['Nao-Conformidade']),
    ('2026-09-29', 'Matriz GUT dos problemas do trimestre', ['GUT', 'Caso-Integrado']),
    ('2026-10-02', 'Diagnóstico da ISO 9001 (68% hoje; a T13 recalcula)', ['ISO-9001', 'Analise-Critica']),
    ('2026-10-05', 'Matriz de riscos do delivery (MP-02)', ['Riscos']),
    ('2026-10-06', 'Leitura dos indicadores de out/2025 a set/2026 (terça-feira)', ['Indicadores', 'Caso-Integrado']),
    ('2026-10-09', 'Renovação da licença sanitária protocolada; PDCA da margem do delivery aberto', ['Partes-Interessadas']),
    ('2026-10-14', 'Mapa de processos (MP-01) e rotina de documentos revisão 3', ['Processos', 'Informacao-Documentada']),
    ('2026-10-23', 'Partes interessadas: 11 listadas, 9 pertinentes', ['Partes-Interessadas']),
    ('2026-11-20', 'Homologação do segundo fornecedor de queijo (P2), resposta ao risco R4 (P13)', ['Fornecedores', 'Analise-Critica']),
    ('2026-12-04', 'Homologação dos outros seis fornecedores, P1 e P3 a P7 (P13)', ['Fornecedores']),
    ('2026-12-14', 'Primeira análise crítica: oito decisões, R$ 11.100 aprovados; registra as homologações (P13)', ['Analise-Critica', 'Escopo', 'Caso-Integrado']),
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

# ---------------------------------------------------------------------------------------------
# Indústria. Valores do cânone. Os itens I01 a I19 e N08 em diante, em DECISOES, dizem o que muda e onde.
# ---------------------------------------------------------------------------------------------
_INDUSTRIA = _org()

_INDUSTRIA['identidade'] = {
    'nome': 'Indústria de embalagens plásticas',
    'descricao': 'Fábrica de filmes plásticos técnicos, lisos e impressos: extrusão, impressão, corte (rebobinamento), '
                 'inspeção e expedição; laboratório próprio de ensaios; armazém externo operado por empresa contratada.',
    'escopo': 'Projeto, fabricação e expedição de filmes plásticos técnicos, lisos e impressos, para embalagem de '
              'alimentos (Escopo, revisão 1, de 10/05/2027; 8.5.3 declarado não aplicável). Processos terceirizados: '
              'armazenagem e transporte, ensaios de migração em laboratório externo e calibração dos instrumentos. '
              'O escopo restrito a alimentos contra os clientes de cosméticos e industriais fica para o autor (N21).',
    'funcionamento': 'Três turnos, A, B e C, todos os dias: 744 horas no mês. O turno C é o da noite e responde por um '
                     'terço da produção. A impressora trabalha em dois turnos: 496 horas (Recursos).',
    'extrusoras': 'Quatro extrusoras desde setembro de 2026 (I02). A extrusora 3 é a dos exemplos de produção; as '
                  'extrusoras 3 e 4 não têm medidor de espessura em linha (I07).',
    'clientes': '58 clientes ativos em 2026: 24 de alimentos, 18 de cosméticos e 16 industriais (Satisfação). Cliente A, '
                'alimentos (filme de 40 µm, biscoito; cilindros de impressão guardados na fábrica; o contrato exige 60 dias '
                'para reclamação); cliente B (filme liso de 50 µm); cliente C, alimentos congelados (projeto D-07); '
                'cliente D (queijos; pedido PR-119 recusado); cliente E (filme impresso para biscoitos, PR-120).',
    'politica': 'Entregar embalagens conformes e no prazo, cumprir os requisitos legais e os dos clientes, e melhorar os '
                'processos reduzindo as perdas (Objetivos, 18/02/2027).',
    'norma': 'Segue a ISO 9001:2015 até a transição. Comprou a edição de 2026 em 10/02/2027 (ISO 9001:2026, plano de '
             'transição); ela entra na lista de documentos externos (I12).',
    'certificacao': 'Antes de 17/12/2027, sistema implantado, sem certificado (I01). Objetivo O4: certificação até '
                    'dezembro de 2027. Organismo acreditado contratado em 23/04/2027, por R$ 38.000. Prontidão de '
                    '30/09/2027: 93%. Fase 1 em 20/10/2027, fase 2 em 23/11/2027 (uma NC maior, 8.5.6), decisão em '
                    '17/12/2027: certificado ISO 9001:2015 válido até 16/12/2030. Transição para a edição de 2026 na '
                    '1ª manutenção, em 22/11/2028 (limite 30/09/2029).',
    'analise_critica': 'Semestral, em fevereiro e em agosto, conduzida pelo diretor geral: 12/02/2026, 13/08/2026, '
                       '18/02/2027 e 19/08/2027 (I06).',
    'auditorias': 'Programa anual de 12 auditorias em 9 processos, gerido pelo Coordenador da Qualidade. Auditoria '
                  '2026-07, de compras, em 22/09/2026; auditoria 2027-11, da produção, em 06/10/2027. Seis auditores '
                  'em 2026; mais quatro formados em 21/05/2027: dez auditores.',
}

_INDUSTRIA['pessoas'] = [
    {'nome': None, 'cargo': 'Diretor geral', 'desde': None,
     'papel': 'Conduz a análise crítica, aprova o escopo e os documentos de gestão; responsável pela SWOT (N11).'},
    {'nome': None, 'cargo': 'Gerente industrial', 'desde': None,
     'papel': 'Dono da Produção. Ciclo PDCA do refugo; autoriza mudanças de processo e a liberação com verificação '
              'pendente. Não existe "Gerente de Produção" nem "Diretor industrial" (I04, N11).'},
    {'nome': None, 'cargo': 'Gerente de engenharia', 'desde': None,
     'papel': 'Dono do Desenvolvimento de produto: projeto D-07, linha com material reciclado, medidores em linha.'},
    {'nome': None, 'cargo': 'Gerente comercial', 'desde': None,
     'papel': 'Dono de Comercial e análise de pedidos; pesquisa de satisfação; visitas ao cliente A (I18).'},
    {'nome': 'Helena', 'cargo': 'Gerente de Suprimentos', 'desde': '2019-04',
     'papel': 'Dona de Suprimentos; responsável pelo RNC 2026-31 e pela matriz de riscos de compras. Em formação como '
              'auditora interna (prazo 28/05/2027).'},
    {'nome': 'Antônio', 'cargo': 'Comprador sênior', 'desde': '2017-02',
     'papel': 'Avaliação e homologação de fornecedores; treina os compradores novos.'},
    {'nome': 'Luana', 'cargo': 'Compradora', 'desde': '2022-07', 'papel': 'Nível 2 em S1 (P18); reciclagem não eficaz.'},
    {'nome': 'Felipe', 'cargo': 'Comprador', 'desde': '2024-03', 'papel': 'Nível 2 em S7 (P18).'},
    {'nome': 'Camila', 'cargo': 'Compradora', 'desde': '2027-01',
     'papel': 'Admitida em janeiro de 2027 no lugar de um comprador que saiu no fim de 2026: os compradores continuam '
              'quatro (N15). Sete lacunas em 12/03/2027.'},
    {'nome': 'Jorge', 'cargo': 'Líder do Recebimento', 'desde': '2020-10',
     'papel': 'Confere os itens antes de liberar; única pessoa com nível 2 ou mais em receber e conferir (S6). Há seis '
              'anos na empresa (P18).'},
    {'nome': None, 'cargo': 'Coordenador da Qualidade', 'desde': None,
     'papel': 'Dono de Laboratório e controle da qualidade e de Gestão do sistema da qualidade; gestor do programa de '
              'auditoria; auditor líder apto a liderar (94%).'},
    {'nome': None, 'cargo': 'Gerente de RH', 'desde': None,
     'papel': 'Dono de Gestão de pessoas; mantém a avaliação dos auditores internos.'},
    {'nome': None, 'cargo': 'Supervisor de manutenção', 'desde': None, 'papel': 'Dono da Manutenção; preventivas das extrusoras.'},
    {'nome': None, 'cargo': 'Supervisor de logística', 'desde': None, 'papel': 'Dono de Expedição e logística.'},
    {'nome': None, 'cargo': 'Líder da expedição', 'desde': None, 'papel': 'Responsável pelo objetivo O3, entregas no prazo.'},
    {'nome': None, 'cargo': 'Analista da Qualidade', 'desde': None,
     'papel': 'Libera os lotes com o laudo; programa de calibração; auditor interno.'},
    {'nome': None, 'cargo': 'Engenheiro de processos', 'desde': None, 'papel': 'Auditor interno, apto a auditar em equipe (70%).'},
    {'nome': None, 'cargo': 'Analista de RH', 'desde': None, 'papel': 'Auditora em formação (50%) na auditoria 2027-11.'},
    {'nome': None, 'cargo': 'Operador sênior da extrusão', 'desde': None,
     'papel': 'Regula a extrusora 3 (C-01); aposenta-se em dezembro de 2027.'},
    {'nome': None, 'cargo': 'Operador novo do turno C', 'desde': None,
     'papel': 'Regula a extrusora 3 sem registro de treinamento ("aprendi com o colega"): NC menor I-4 da fase 2.'},
]

_INDUSTRIA['processos'] = [
    # os nove do programa de auditoria e da matriz de interações (Auditoria, Processos); I05
    {'codigo': '1', 'nome': 'Comercial e análise de pedidos', 'tipo': None, 'dono': 'Gerente comercial',
     'indicador': 'Reclamações por milhão de peças (O2)'},
    {'codigo': '2', 'nome': 'Desenvolvimento de produto', 'tipo': None, 'dono': 'Gerente de engenharia',
     'indicador': 'Etapas do lote piloto com resina reciclada (O5)'},
    {'codigo': '3', 'nome': 'Suprimentos', 'tipo': None, 'dono': 'Gerente de Suprimentos',
     'indicador': 'C1 a C4 (Indicadores) e fornecedores críticos avaliados (O7)'},
    {'codigo': '4', 'nome': 'Produção', 'tipo': None, 'dono': 'Gerente industrial', 'indicador': 'Refugo, % do peso (O1)'},
    {'codigo': '5', 'nome': 'Laboratório e controle da qualidade', 'tipo': None, 'dono': 'Coordenador da Qualidade',
     'indicador': 'Lotes reprovados na inspeção final (1,1% em 2026)'},
    {'codigo': '6', 'nome': 'Expedição e logística', 'tipo': None, 'dono': 'Supervisor de logística',
     'indicador': 'Entregas no prazo (O3)'},
    {'codigo': '7', 'nome': 'Manutenção', 'tipo': None, 'dono': 'Supervisor de manutenção',
     'indicador': 'Disponibilidade, meta de 95%'},
    {'codigo': '8', 'nome': 'Gestão de pessoas', 'tipo': None, 'dono': 'Gerente de RH', 'indicador': 'Treinamentos no prazo'},
    {'codigo': '9', 'nome': 'Gestão do sistema da qualidade', 'tipo': None, 'dono': 'Coordenador da Qualidade',
     'indicador': 'Prazo médio de encerramento das não conformidades (O4 e O6)'},
    {'codigo': None, 'nome': 'Terceirizados', 'tipo': 'Externo', 'dono': None,
     'indicador': 'Processos terceirizados do Escopo: armazenagem e transporte, ensaios de migração em laboratório '
                  'externo e calibração dos instrumentos. Serviços críticos em Fornecedores: manutenção das extrusoras '
                  '(Mantec, F-10) e usinagem (Ferramentaria Precisa, F-12).'},
]

_INDUSTRIA['equipamentos'] = [
    # instrumentos (Calibração, leitura de 30/06/2027): 7 dos 25 instrumentos em uso (N19)
    {'codigo': 'MIC-07', 'descricao': 'Micrômetro de ponta plana, 1 µm, extrusora 3: espessura de 38 a 42 µm',
     'criterio': 'Calibração externa a cada 6 meses, ±1 µm',
     'situacao': 'Aprovado em 10/01/2027; reprovado em 12/06/2027 (FV-12, +1,6 µm): fora de uso; medições de 10/01 a '
                 '12/06 corrigidas, 6 bobinas abaixo de 38 µm, 2 entregues', 'datas': ['2027-01-10', '2027-06-12']},
    {'codigo': 'MIC-08', 'descricao': 'Micrômetro digital, 0,1 µm, laboratório; mede as bobinas da extrusora 3 desde 12/06/2027',
     'criterio': 'Calibração externa a cada 6 meses, ±0,5 µm', 'situacao': 'Calibrado em 15/03/2027; próxima 15/09/2027',
     'datas': ['2027-03-15']},
    {'codigo': 'TR-03', 'descricao': 'Trena digital, extrusora 3: largura de 598 a 602 mm',
     'criterio': 'Calibração externa a cada 12 meses, ±0,3 mm', 'situacao': 'Calibrada em 08/11/2026; próxima 08/11/2027',
     'datas': ['2026-11-08']},
    {'codigo': 'TER-Z3', 'descricao': 'Termopar da zona 3 da extrusora 3: 185 a 195 °C',
     'criterio': 'Calibração externa a cada 12 meses, ±2 °C',
     'situacao': 'Calibrado em 02/08/2026; cabo trocado e verificado contra o PAD-01 em 27/07/2027', 'datas': ['2026-08-02', '2027-07-27']},
    {'codigo': 'DIN-01', 'descricao': 'Dinamômetro do laboratório: solda de no mínimo 12 N/15 mm',
     'criterio': 'Calibração externa a cada 12 meses, ±0,2 N',
     'situacao': 'Em calibração em 20/05/2027; calibrado em 21/05/2027; próxima 21/05/2028', 'datas': ['2027-05-21']},
    {'codigo': 'TER-L1', 'descricao': 'Termômetro da câmara de condicionamento do laboratório (-18 °C)',
     'criterio': 'Verificação interna a cada 3 meses, ±1 °C',
     'situacao': 'Verificado em 15/03/2027 (FV-09); vencido desde 15/06/2027 e ainda em uso', 'datas': ['2027-03-15']},
    {'codigo': 'PAD-01', 'descricao': 'Termômetro padrão do laboratório, referência das verificações internas',
     'criterio': 'Calibração externa a cada 12 meses, ±0,1 °C', 'situacao': 'Calibrado em 10/02/2027; próxima 10/02/2028',
     'datas': ['2027-02-10']},
    {'codigo': None, 'descricao': 'Dois medidores de espessura em linha, extrusoras 3 e 4, R$ 96.000 com instalação (I07)',
     'criterio': 'Compra aprovada em 18/02/2027, prazo 30/06/2027',
     'situacao': 'Não instalados em 09/07/2027 (atrasados); antecipação decidida em 19/08/2027', 'datas': ['2027-02-18', '2027-06-30', '2027-08-19']},
    # infraestrutura (Recursos, julho de 2027; meta de disponibilidade 95%)
    {'codigo': 'EXT-01', 'descricao': 'Extrusora 1', 'criterio': 'Preventiva a cada 3 meses',
     'situacao': 'Em dia (10/05/2027); 100% em julho', 'datas': ['2027-05-10']},
    {'codigo': None, 'descricao': 'Extrusoras 2 e 4 (a 4 em operação desde setembro de 2026, I02)', 'criterio': None,
     'situacao': 'Sem código nos estudos', 'datas': ['2026-09']},
    {'codigo': 'EXT-03', 'descricao': 'Extrusora 3, a dos exemplos de produção, CEP e caso integrado',
     'criterio': 'Preventiva a cada 3 meses',
     'situacao': 'Preventiva vencida em 15/06/2027 e adiada; 3 quebras em julho (06/07 resistência, 14 h; 18/07 rosca, '
                 '20 h; 27/07 cabo do termopar, 6 h): 40 h, 94,6%. Duas das três vieram de peças que a preventiva teria '
                 'trocado ou medido (I19). Preventiva remarcada para 07/08/2027',
     'datas': ['2027-03-15', '2027-06-15', '2027-07-06', '2027-07-18', '2027-07-27']},
    {'codigo': 'IMP-01', 'descricao': 'Impressora flexográfica', 'criterio': 'Preventiva todo mês',
     'situacao': '1 quebra em julho (anilox, 4 h): 99,2%', 'datas': ['2027-07-12', '2027-07-20']},
    {'codigo': 'REB-01', 'descricao': 'Rebobinadeira', 'criterio': 'Preventiva a cada 6 meses', 'situacao': 'Em dia', 'datas': ['2027-02-20']},
    {'codigo': 'CMP-01', 'descricao': 'Compressor de ar, de que as quatro extrusoras dependem', 'criterio': 'Preventiva a cada 3 meses',
     'situacao': 'Em dia; crítico sem contingência', 'datas': ['2027-06-02']},
    {'codigo': 'CHI-01', 'descricao': 'Chiller de água gelada', 'criterio': 'Preventiva a cada 6 meses',
     'situacao': 'Quebra em 22/07/2027 (8 h): as extrusoras seguem com água da torre, em velocidade reduzida; produto '
                 'afetado sem destino registrado (I19)', 'datas': ['2027-04-10', '2027-07-22']},
    {'codigo': 'EMP-01', 'descricao': 'Empilhadeira', 'criterio': 'Preventiva a cada 3 meses', 'situacao': 'Vence em 7 dias', 'datas': ['2027-05-05']},
    {'codigo': 'ERP-01', 'descricao': 'Sistema de gestão (ERP)', 'criterio': 'Preventiva a cada 3 meses',
     'situacao': 'Teste de restauração em 03/07/2027: 40 minutos', 'datas': ['2027-07-03']},
    {'codigo': 'EXS-01', 'descricao': 'Exaustão de solventes da impressão', 'criterio': 'Preventiva uma vez por ano',
     'situacao': 'Em dia', 'datas': ['2026-09-15']},
    {'codigo': 'SEL-01', 'descricao': 'Seladora manual da expedição (o mesmo código existe na pizzaria: COMPARTILHADOS)',
     'criterio': 'Sem preventiva', 'situacao': 'Sem plano', 'datas': []},
]

_INDUSTRIA['documentos'] = [
    # lista mestra do processo de compras (Informação documentada, 05/03/2027)
    {'codigo': 'PR-SUP-01', 'titulo': 'Aquisição de materiais e serviços (procedimento de compras)', 'revisao': '6', 'data': '2026-10-16',
     'nota': 'Revisão 5 até a ação 2 do RNC 2026-31. Próxima 10/2028. É o único procedimento de compras (N16).'},
    {'codigo': 'PO-02', 'titulo': 'Política de compras e alçadas', 'revisao': '3', 'data': '2025-11-20', 'nota': 'Três cotações acima de R$ 2.000.'},
    {'codigo': 'PR-SUP-02', 'titulo': 'Homologação e avaliação de fornecedores', 'revisao': '2', 'data': '2026-11-27', 'nota': ''},
    {'codigo': 'PR-SUP-03', 'titulo': 'Compras de urgência', 'revisao': '1', 'data': '2025-04-08', 'nota': 'Em revisão.'},
    {'codigo': 'IT-REC-01', 'titulo': 'Recebimento e conferência de materiais', 'revisao': '1', 'data': '2025-02-17', 'nota': 'Revisão vencida.'},
    {'codigo': 'FR-11', 'titulo': 'Requisição de compra (formulário no sistema, com campo de especificação obrigatório)',
     'revisao': '4', 'data': '2026-10-14', 'nota': ''},
    {'codigo': 'FR-12', 'titulo': 'Avaliação de desempenho de fornecedor', 'revisao': '2', 'data': '2026-11-27', 'nota': ''},
    {'codigo': 'FR-13', 'titulo': 'Registro de devolução ao fornecedor', 'revisao': '1', 'data': '2025-02-17', 'nota': 'Revisão vencida.'},
    {'codigo': 'FR-14', 'titulo': 'Registro de recebimento e conferência', 'revisao': None, 'data': None, 'nota': 'Só na tabela de retenção.'},
    {'codigo': 'LS-01', 'titulo': 'Lista de fornecedores homologados', 'revisao': '2027-02', 'data': '2027-02-26',
     'nota': 'Revista a cada 6 meses, com a avaliação semestral: a exceção dita da regra (I12).'},
    {'codigo': None, 'titulo': 'Cadastro de itens com especificação padrão', 'revisao': None, 'data': '2026-10-23',
     'nota': 'Ação 3 do RNC 2026-31; sem código nem aprovação.'},
    # outros processos
    {'codigo': 'FR-03', 'titulo': 'Ficha de regulagem da extrusora 3 (o mesmo código existe na pizzaria: COMPARTILHADOS)',
     'revisao': None, 'data': None, 'nota': 'Conhecimento C-01.'},
    {'codigo': 'PR-RH-02', 'titulo': 'Procedimento de treinamento (registro antes do início da operação)', 'revisao': None,
     'data': None, 'nota': 'Auditoria: 3 dos 8 operadores admitidos em 2026 sem registro.'},
    {'codigo': 'PG-05', 'titulo': 'Procedimento de mudanças', 'revisao': None, 'data': None, 'nota': 'Critério da auditoria 2027-11.'},
    {'codigo': 'PQ-08', 'titulo': 'Tratamento de reclamação técnica', 'revisao': None, 'data': None,
     'nota': 'Lição I-01 incorporada em 20/06/2027.'},
    {'codigo': 'PE-11', 'titulo': 'Ensaio de resistência da solda', 'revisao': None, 'data': None, 'nota': ''},
    {'codigo': 'PE-14', 'titulo': 'Procedimento do laboratório para ensaios (instrumentos conferidos antes)', 'revisao': None,
     'data': None, 'nota': 'Lição I-06 incorporada em 10/09/2027.'},
    {'codigo': 'PM-01', 'titulo': 'Plano de manutenção', 'revisao': None, 'data': None, 'nota': 'Lições I-03 e I-04 em 10/08/2027.'},
    {'codigo': 'FM-02', 'titulo': 'Formulário de manutenção', 'revisao': None, 'data': None, 'nota': 'Lição I-05 pendente.'},
    {'codigo': 'IE-12', 'titulo': 'Instrução de ensaio de queda de dardo', 'revisao': None, 'data': '2027-07-02', 'nota': 'Projeto D-07, E5.'},
    {'codigo': 'RX-40', 'titulo': 'Receita do filme de 40 µm da extrusora 3', 'revisao': None, 'data': None, 'nota': 'Projeto D-07, E6.'},
    {'codigo': 'RE-D07-1', 'titulo': 'Relatório de ensaios do lote de teste do D-07', 'revisao': None, 'data': '2027-07-16', 'nota': ''},
    {'codigo': None, 'titulo': 'ES-D07 (especificação), RX-D07 (receita) e DC-D07 (declaração) do projeto D-07',
     'revisao': '1', 'data': '2027-06-24', 'nota': 'ES-D07 rev. 2 com a camada interna de 20 µm (12/08/2027).'},
    {'codigo': None, 'titulo': 'Plano de controle da extrusão', 'revisao': '5', 'data': '2027-05-03',
     'nota': 'Sete controles, K1 a K7. Revisão 6 em vigor na auditoria de 06/10/2027.'},
    {'codigo': None, 'titulo': 'Mapa de processos', 'revisao': '4', 'data': None,
     'nota': 'Ação 6 da análise crítica de 13/08/2026, concluída no prazo (30/11/2026), com a nova linha de produção.'},
    # documentos de origem externa (Informação documentada, exemplo 3; I12)
    {'codigo': None, 'titulo': 'ISO 9001:2015, com a emenda de 2024', 'revisao': 'Emenda 1, de 2024', 'data': '2027-01-12',
     'nota': 'Em uso até a transição.'},
    {'codigo': None, 'titulo': 'ISO 9001:2026', 'revisao': 'Edição de 2026', 'data': '2027-02-10',
     'nota': 'Comprada em 10/02/2027; entra na lista de documentos externos (I12).'},
]

_INDUSTRIA['linha_do_tempo'] = [
    ('2025-10', 'Início da série dos indicadores de compras (C1 a C4, outubro de 2025 a setembro de 2026)', ['Indicadores']),
    ('2026-02-12', 'Análise crítica: preventiva das extrusoras, analista do laboratório, PDCA do refugo, pesquisa revista', ['Analise-Critica', 'Satisfacao']),
    ('2026-08', 'Auditoria interna do laboratório de recebimento: 3 de 25 instrumentos com calibração vencida', ['GUT', 'Ishikawa', '5W2H', 'PDCA', 'Calibracao']),
    ('2026-08-13', 'Análise crítica: ações 5 a 8, entre elas orçar os medidores de espessura (I07)', ['Analise-Critica']),
    ('2026-09', 'Extrusora 4 em operação (I02)', ['Analise-Critica', 'Recursos']),
    ('2026-09-01', 'Instrumentos vencidos retirados de uso; plano 5W2H até 18/12/2026 (I19)', ['5W2H', 'PDCA']),
    ('2026-09-14', 'Sétima reclamação do cliente A em 2026, a quinta por espessura (lote 26-0911)', ['Satisfacao', 'Caso-Integrado']),
    ('2026-09-22', 'Auditoria 2026-07, de compras: 2 NC menores e 1 OM; RNC 2026-31 aberto', ['Auditoria', 'Nao-Conformidade', 'ISO-9001']),
    ('2026-09-23', 'RNC 2026-32 (era 2026-29, I11): espessura na extrusora 3, sem medidor em linha', ['Caso-Integrado', 'Satisfacao']),
    ('2026-09-25', 'Processo de compras diante da norma: 81%', ['ISO-9001']),
    ('2026-10-02', 'Primeira visita ao cliente A: plano com inspeção de 100% das bobinas', ['Satisfacao']),
    ('2026-10-08', 'Leitura dos indicadores de compras', ['Indicadores']),
    ('2026-10-09', 'Pareto das bobinas reprovadas de julho a setembro de 2026', ['Pareto']),
    ('2026-10-12', 'Matriz de riscos do processo de compras (revisão marcada para 12/04/2027)', ['Riscos']),
    ('2026-10-16', 'PR-SUP-01 rev. 6 e campo de especificação obrigatório', ['Nao-Conformidade', 'Informacao-Documentada']),
    ('2026-10-20', 'Tartaruga do processo de compras', ['Processos']),
    ('2026-11', 'Pesquisa anual de satisfação: 41 respostas de 58 clientes; análise em 04/12/2026', ['Satisfacao', 'Analise-Critica']),
    ('2027-01', 'Camila admitida como compradora; SWOT de janeiro de 2027', ['Competencias', 'Analise-Critica']),
    ('2027-01-11', 'Avaliação dos 12 fornecedores críticos, segundo semestre de 2026 (P13)', ['Fornecedores', 'Analise-Critica']),
    ('2027-01-20', 'Partes interessadas: 12 listadas, 10 pertinentes', ['Partes-Interessadas']),
    ('2027-02-05', 'RNC 2026-31 encerrado como eficaz', ['Nao-Conformidade']),
    ('2027-02-10', 'Compra da ISO 9001:2026', ['ISO-9001-2026']),
    ('2027-02-18', 'Análise crítica: dez decisões, R$ 161.000; objetivos de 2027', ['Analise-Critica', 'Objetivos', 'Caso-Integrado']),
    ('2027-03-05', 'Documentos de compras e externos; ficha de homologação do F-13', ['Informacao-Documentada', 'Fornecedores']),
    ('2027-03-12', 'Matriz de competências de Suprimentos; segunda visita ao cliente A (I18)', ['Competencias', 'Objetivos']),
    ('2027-03-29', 'F-13, Resinas Atlântico, homologado: segundo fornecedor de resina, que oferece também a reciclada (N14)', ['Fornecedores', 'Caso-Integrado', 'Objetivos']),
    ('2027-04-23', 'Organismo de certificação contratado', ['Objetivos', 'Certificacao']),
    ('2027-05-03', 'Plano de controle rev. 5; velocidade de 42 para 45 m/min sem análise', ['Producao']),
    ('2027-05-05', 'Lote piloto 127, duas bobinas com a resina do F-13 (I09)', ['Producao', 'Caso-Integrado']),
    ('2027-05-10', 'Escopo, revisão 1', ['Escopo']),
    ('2027-05-14', 'Resina do F-13 na produção regular: lote 135; bobina 1 segregada (PNC 2027-19)', ['Producao', 'Liberacao', 'Caso-Integrado']),
    ('2027-05-21', 'Mais quatro auditores internos formados', ['Objetivos']),
    ('2027-05-24', 'Reclamação do cliente A, lote 135, bobina 2 (PNC 2027-22)', ['Liberacao', 'Conhecimento', 'Caso-Integrado', 'Calibracao']),
    ('2027-06-07', 'Projeto D-07 aberto (proposta PR-118)', ['Projeto', 'Pedidos']),
    ('2027-06-12', 'MIC-07 reprovado (FV-12); clientes informados em 14/06', ['Calibracao', 'Caso-Integrado']),
    ('2027-06-24', 'Lote piloto de uma tonelada com resina reciclada', ['Objetivos']),
    ('2027-06-30', 'Prazo dos medidores em linha, vencido sem instalação (I07)', ['Objetivos', 'Escopo']),
    ('2027-07', 'Três quebras da extrusora 3; CEP de 04 a 16/07; PNC 2027-29 e 2027-30', ['Recursos', 'Histograma-CEP', 'Caso-Integrado']),
    ('2027-07-08', 'Resina B no projeto D-07, antes do lote de teste de 15/07 (I10)', ['Projeto']),
    ('2027-08-19', 'Análise crítica: antecipar os medidores e passar o conhecimento do operador sênior', ['Caso-Integrado', 'Certificacao', 'Conhecimento']),
    ('2027-09-30', 'Mapa do conhecimento; prontidão para a certificação: 93%', ['Conhecimento', 'Certificacao', 'Caso-Integrado']),
    ('2027-10-06', 'Auditoria interna 2027-11, da produção', ['Tecnica-Auditoria']),
    ('2027-10-20', 'Fase 1 da certificação', ['Certificacao']),
    ('2027-11-23', 'Fase 2: NC maior nas mudanças de processo (11 em 2027, 4 sem autorização, I03)', ['Certificacao']),
    ('2027-12-17', 'Decisão de certificação, ISO 9001:2015, válida até 16/12/2030 (I01)', ['Certificacao', 'ISO-9001-2026']),
    ('2028-03-20', 'Diagnóstico das mudanças da edição de 2026', ['ISO-9001-2026']),
    ('2028-11-22', '1ª manutenção, com a transição', ['ISO-9001-2026']),
]

_INDUSTRIA['numeros'] = [
    ('Refugo', '3,4% antes do PDCA; 2,6% em 2026 (meta 2,0%). 2027: jan 2,5, fev 2,5, mar 2,4, abr 2,3, mai 2,2, jun 2,2 (O1).'),
    ('Reclamações por milhão de peças', '62 em 2026 (máximo 50). 2027: 58, 55, 47, 44, 40, 38 (O2). 18 reclamações em 2026, '
     '7 do cliente A, 5 delas por espessura até 14/09/2026; 8 por espessura no ano.'),
    ('Entregas no prazo', '97% em 2026; meta do O3: manter 97% (I15). 2027: 97, 96, 97, 97, 98, 97.'),
    ('Pesquisa de satisfação', 'Novembro de 2026: 41 respostas de 58 clientes (71%); média 8,38 ("8,4"), meta 8,0; indicação 39, meta 40.'),
    ('Não conformidades', '38 registros em 2026: 30 encerrados, 27 eficazes, 8 em tratamento; prazo médio de 74 dias. '
     'Meta de 60 dias em 2027: 70, 66, 61, 58, 55, 52 (O6).'),
    ('Fornecedores críticos', '12 (F-01 a F-12), mais o F-13 em 29/03/2027. Avaliados em 2026: 83, 75, 67, 67, 58, 58 '
     '(abr a set). Segundo semestre de 2026: A 8, B 1, C 2, D 1 (avaliação de 11/01/2027). 2027: 100% até maio, 92% em junho (O7).'),
    ('Requisições sem especificação', 'C2: 29, 31, 33, 30, 31, 29 (abr a set/2026; média do ano 30,2); abrangência: 97 de 312 '
     '(31%); depois das ações: 14%, e 4, 3 e 2%.'),
    ('Disponibilidade', 'Meta de 95%; 744 horas programadas (496 na impressora). EXT-03 em julho de 2027: 94,6%.'),
    ('Instrumentos', '25 em uso (auditoria de 2026, 5W2H, Técnica de auditoria); a Calibração mostra 7 deles (N19).'),
    ('Espessura do filme do cliente A', '40 µm, de 38 a 42 µm. CEP de julho de 2027: LC 39,97, LSC 40,34, LIC 39,60, Cp 2,43, Cpk 2,39.'),
    ('Mudanças de processo em 2027', '11: 9 até setembro e 2 em outubro e novembro; 4 sem autorização (I03).'),
    ('Prontidão para a certificação', '93% em 30/09/2027.'),
]

# ---------------------------------------------------------------------------------------------
# Distribuidora: a cadeia de compras das ferramentas (GUT, Pareto, Ishikawa, 5W2H e PDCA), item I08.
# Os fatos estão como os cinco estudos os contam, com a cronologia de N09 e a SWOT de N08.
# ---------------------------------------------------------------------------------------------
_DISTRIBUIDORA = _org()

_DISTRIBUIDORA['identidade'] = {
    'nome': 'Distribuidora de materiais elétricos · Compras',
    'descricao': 'Distribuidora de materiais elétricos. Os exemplos olham só a área de compras.',
    'escopo': 'Processo de compras: da requisição aprovada ao pedido emitido.',
    'areas_requisitantes': 'Manutenção, Produção, Laboratório, Logística e Administrativo, como na folha do Pareto e no '
                           'piloto do 5W2H. Ficam como estão (regra 3 da seção 4.3 do spec).',
    'nomes': 'Os exemplos chamam a área de Suprimentos e o dono do processo de Gerente de Suprimentos; ficam assim. O '
             'nome da organização, em cada exemplo, é o acima.',
    'sistema': 'Sistema de compras desde antes de dezembro de 2025 (dados do Pareto); cotações e aprovações por e-mail, '
               'fora do sistema (SWOT, W2, N08).',
    'politica_de_compras': 'Três cotações para qualquer valor até julho de 2026; desde 08/07/2026, uma cotação só para '
                           'compras de até R$ 2.000, aprovada pela Diretoria.',
}

_DISTRIBUIDORA['pessoas'] = [
    {'nome': None, 'cargo': 'Gerente de Suprimentos', 'desde': None,
     'papel': 'Dono do problema no PDCA e responsável pela SWOT, pela GUT, pelo Ishikawa e pelo 5W2H do prazo de compra.'},
    {'nome': None, 'cargo': 'Analista de compras', 'desde': None,
     'papel': 'Fez a folha e o Pareto de 19/06/2026; formulário (A1), treinamento (A4) e medição do piloto (A6).'},
    {'nome': None, 'cargo': 'Comprador sênior', 'desde': None, 'papel': 'Catálogo dos itens mais comprados (A2): 214 itens.'},
    {'nome': None, 'cargo': 'Comprador de serviços', 'desde': None, 'papel': 'Renegociação do contrato de frete (GUT, P4).'},
    {'nome': None, 'cargo': 'Requisitantes', 'desde': None, 'papel': '38 requisitantes, nenhum treinado antes do piloto (Ishikawa, B1).'},
    {'nome': None, 'cargo': 'Diretoria', 'desde': None, 'papel': 'Aprovou a alçada de uma cotação em 08/07/2026 (A3).'},
    {'nome': None, 'cargo': 'Equipe de TI', 'desde': None, 'papel': 'Configurou os campos obrigatórios do formulário (A1).'},
]

_DISTRIBUIDORA['processos'] = [
    {'codigo': None, 'nome': 'Compras', 'tipo': None, 'dono': 'Gerente de Suprimentos',
     'indicador': 'Dias úteis entre a requisição aprovada e o pedido emitido; requisições devolvidas, em %'},
]

_DISTRIBUIDORA['equipamentos'] = [
    {'codigo': None, 'descricao': 'Sistema de compras', 'criterio': None,
     'situacao': 'Aceitava a descrição em texto livre e o envio com campos vazios até o formulário novo (10/07/2026)',
     'datas': ['2026-07-10']},
]

_DISTRIBUIDORA['documentos'] = [
    {'codigo': None, 'titulo': 'Formulário de requisição com campos obrigatórios', 'revisao': None, 'data': '2026-07-10',
     'nota': 'Ação A1; estendido a todas as áreas em 11/09/2026.'},
    {'codigo': None, 'titulo': 'Catálogo dos itens mais comprados', 'revisao': None, 'data': '2026-07-21', 'nota': '214 itens (A2).'},
    {'codigo': None, 'titulo': 'Política de compras', 'revisao': None, 'data': '2026-07-08', 'nota': 'Alçada de uma cotação até R$ 2.000 (A3).'},
    {'codigo': None, 'titulo': 'Procedimento de compras', 'revisao': None, 'data': '2026-09-11', 'nota': 'Revisado na etapa 7 do PDCA.'},
]

_DISTRIBUIDORA['linha_do_tempo'] = [
    ('2025-12', 'Início da folha das requisições devolvidas (dezembro de 2025 a maio de 2026)', ['Pareto']),
    ('2026-05-22', 'SWOT da área de compras (N08)', ['SWOT']),
    ('2026-05-29', 'Matriz GUT dos problemas de compras (N09)', ['GUT']),
    ('2026-06-01', 'Início do ciclo PDCA do prazo de compra: 12 dias úteis, meta de 7 em 3 meses', ['PDCA']),
    ('2026-06-19', 'Pareto das requisições devolvidas: 100 de 250 (40%), 48% da Manutenção', ['Pareto', 'PDCA']),
    ('2026-06-26', 'Ishikawa das requisições devolvidas: 5 causas confirmadas, 4 seguem para o plano', ['Ishikawa', 'PDCA']),
    ('2026-07-03', 'Plano 5W2H: seis ações, R$ 2.200 de R$ 3.000', ['5W2H', 'PDCA']),
    ('2026-07-13', 'Piloto de 4 semanas na Manutenção e na Produção, até 07/08/2026', ['5W2H', 'PDCA']),
    ('2026-08-28', 'Verificação: prazo de 8 dias úteis (meta 7, não atingida); devoluções de 40% para 12%', ['5W2H', 'PDCA']),
    ('2026-09-11', 'Formulário e alçada estendidos a todas as áreas; procedimento de compras revisado', ['PDCA']),
    ('2026-09-18', 'Conclusão do ciclo; novo ciclo sobre a revisão de contratos', ['PDCA']),
]

_DISTRIBUIDORA['numeros'] = [
    ('Prazo de compra', '12 dias úteis entre a requisição aprovada e o pedido emitido; meta de 7; 8 depois do piloto.'),
    ('Requisições devolvidas', '40% (100 de 250, de dezembro de 2025 a maio de 2026); 72 das 100 com campo essencial em '
     'branco; 38 por especificação técnica, 24 delas da Manutenção; 12% depois do piloto (meta de 15%).'),
    ('Plano 5W2H', 'R$ 2.200 previstos para um orçamento de R$ 3.000 (R$ 1.800 de TI e R$ 400 de material; gasto R$ 350).'),
    ('GUT', 'Compras urgentes fora do processo: +30% no semestre (80 pontos); fornecedor único para três itens críticos (60).'),
]

ORGS = {'pizzaria': _PIZZARIA, 'industria': _INDUSTRIA, 'distribuidora': _DISTRIBUIDORA}

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
        'FR-02': 'Planilha de temperatura da câmara fria',
        'FR-03': 'Ficha de alergênicos',
        'FR-04': 'Planilha de descarte de insumos',
        'FR-05': 'Ficha de treinamento',
        'FR-06': 'Registro de não conformidade',
        'FR-07': 'Planilha de verificação dos instrumentos',
        'FR-08': 'Ata da análise crítica',
        'FR-09': 'Relatório de auditoria interna',
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
    'industria': {
        # documentos do processo de compras (Informação documentada, 05/03/2027)
        'PR-SUP-01': 'Procedimento de aquisição de materiais e serviços, o procedimento de compras (rev. 6, 16/10/2026)',
        'PR-SUP-02': 'Procedimento de homologação e avaliação de fornecedores',
        'PR-SUP-03': 'Procedimento de compras de urgência',
        'PO-02': 'Política de compras e alçadas',
        'IT-REC-01': 'Instrução de recebimento e conferência de materiais',
        'FR-11': 'Formulário de requisição de compra',
        'FR-12': 'Formulário de avaliação de desempenho de fornecedor',
        'FR-13': 'Registro de devolução ao fornecedor',
        'FR-14': 'Registro de recebimento e conferência',
        'LS-01': 'Lista de fornecedores homologados',
        # documentos de outros processos (N17: códigos fora do padrão PR-XXX-00, mantidos nesta leva)
        'FR-03': 'Ficha de regulagem da extrusora 3',
        'PR-RH-02': 'Procedimento de treinamento: registro antes do início da operação',
        'PG-05': 'Procedimento de mudanças',
        'PQ-08': 'Procedimento de tratamento de reclamação técnica',
        'PE-11': 'Procedimento do ensaio de resistência da solda',
        'PE-14': 'Procedimento do laboratório para ensaios',
        'PM-01': 'Plano de manutenção',
        'FM-02': 'Formulário de manutenção',
        # projeto D-07 (ES-D07, RX-D07 e DC-D07 não têm a forma que o teste lê)
        'IE-12': 'Instrução de ensaio de queda de dardo',
        'RX-40': 'Receita do filme de 40 µm da extrusora 3',
        'RE-D07-1': 'Relatório de ensaios do lote de teste do D-07',
        # registros de verificação dos instrumentos
        'FV-09': 'Registro de verificação do TER-L1 (15/03/2027)',
        'FV-12': 'Registro de verificação do MIC-07, reprovado (12/06/2027)',
        # propostas e requisições citadas (os pedidos PV- são série livre)
        'PR-118': 'Proposta do cliente C, filme para congelados (03/06/2027)',
        'PR-119': 'Proposta do cliente D, filme com 50% de resina reciclada, recusada (08/06/2027)',
        'PR-120': 'Proposta do cliente E, filme impresso para biscoitos (10/06/2027)',
        'RC-0412': 'Requisição de compra sem especificação técnica (auditoria 2026-07)',
        'RC-0433': 'Requisição de compra sem especificação técnica (auditoria 2026-07)',
        'RC-0457': 'Requisição de compra sem especificação técnica; rolamento devolvido ao fornecedor',
        'RC-0461': 'Requisição de compra sem especificação técnica (auditoria 2026-07)',
        # instrumentos (Calibração; TER-Z3 e TER-L1 não têm a forma que o teste lê)
        'MIC-07': 'Micrômetro de ponta plana da extrusora 3 (fora de uso desde 12/06/2027)',
        'MIC-08': 'Micrômetro digital do laboratório',
        'TR-03': 'Trena digital da extrusora 3',
        'TER-Z3': 'Termopar da zona 3 da extrusora 3',
        'DIN-01': 'Dinamômetro do laboratório',
        'TER-L1': 'Termômetro da câmara de condicionamento do laboratório',
        'PAD-01': 'Termômetro padrão do laboratório',
        # infraestrutura (Recursos)
        'EXT-01': 'Extrusora 1',
        'EXT-03': 'Extrusora 3',
        'IMP-01': 'Impressora flexográfica',
        'REB-01': 'Rebobinadeira',
        'CMP-01': 'Compressor de ar',
        'CHI-01': 'Chiller de água gelada',
        'EMP-01': 'Empilhadeira',
        'ERP-01': 'Sistema de gestão (ERP)',
        'EXS-01': 'Exaustão de solventes da impressão',
        'SEL-01': 'Seladora manual da expedição',
    },
    # a cadeia de compras das ferramentas não cita códigos
    'distribuidora': {},
    # códigos que aparecem nos textos e não são de nenhuma organização
    'sem_organizacao': {
        'ISO-9001': 'Nome da planilha do estudo ISO 9001 requisito a requisito',
        'ISO-9001-2026': 'Nome da planilha do estudo ISO 9001:2026',
        'PR-2026-10': 'Exemplo de código ruim (Informação documentada, módulo 4)',
        'SUP-BR-001': 'Exemplo de código ruim (Informação documentada, módulo 4)',
    },
}
# receitas padrão das pizzas, RC-01 a RC-24
CODIGOS['pizzaria'].update({'RC-%02d' % i: 'Receita padrão nº %d' % i for i in range(1, 25)})

# códigos que existem de propósito em mais de uma organização (seção 4.3 do spec, regra 3: trocar o código
# mudaria mais arquivos do que registrar os dois sentidos)
COMPARTILHADOS = {
    'SEL-01',  # pizzaria: seladora de embalagens; indústria: seladora manual da expedição (os dois em Recursos)
    'FR-03',   # pizzaria: ficha de alergênicos; indústria: ficha de regulagem da extrusora 3 (Conhecimento)
}

# prefixos de numeração corrida, que não são registrados um a um.
# Pizzaria: as séries corridas têm prefixo de uma letra, que o teste não lê como código:
# encomendas E-31 a E-35, pedidos T-1184 e A-772, projetos P-01 e P-03, conhecimentos K-01 a K-07,
# lições L-01 a L-06, atendimentos A-01 a A-08 e constatações do organismo P-1 a P-4.
# Indústria: pedidos de venda PV-2231 em diante (Pedidos). As propostas (PR-) e as requisições (RC-) são
# registradas uma a uma, porque PR- é também o prefixo dos procedimentos e RC- o das receitas da pizzaria.
# As séries de uma letra da indústria (lições I-01 a I-07, conhecimentos C-01 a C-07, atendimentos N-01 a N-08,
# constatações do organismo I-1 a I-6, fornecedores F-01 a F-13) também não são lidas pelo teste.
SERIES_LIVRES = ('PV',)

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
    # indústria · RNC (I11: a série segue a data de abertura)
    {'org': 'industria', 'serie': 'RNC', 'numero': '2026-31', 'data': '2026-09-22',
     'assunto': 'Requisições de compra sem especificação técnica; auditoria 2026-07, constatação 1; PR-SUP-01 rev. 6; '
                'encerrado como eficaz em 05/02/2027',
     'estudos': ['Nao-Conformidade', 'Indicadores', 'ISO-9001', 'Riscos', 'Processos', 'Informacao-Documentada',
                 'Analise-Critica']},
    {'org': 'industria', 'serie': 'RNC', 'numero': '2026-32', 'data': '2026-09-23',
     'assunto': 'Espessura fora na extrusora 3, sem medidor em linha; reclamação do cliente A de 14/09/2026; era '
                '"RNC 2026-29" (I11)',
     'estudos': ['Caso-Integrado', 'Satisfacao']},
    # indústria · PNC (Liberação: lotes de maio de 2027; Recursos e Histograma e CEP: julho de 2027)
    {'org': 'industria', 'serie': 'PNC', 'numero': '2027-17', 'data': '2027-05-11',
     'assunto': 'Lote 132, bobina 2: géis; refugada', 'estudos': ['Liberacao']},
    {'org': 'industria', 'serie': 'PNC', 'numero': '2027-18', 'data': '2027-05-12',
     'assunto': 'Lote 133, bobina 1: 42,6 µm; reclassificada', 'estudos': ['Producao', 'Liberacao']},
    {'org': 'industria', 'serie': 'PNC', 'numero': '2027-19', 'data': '2027-05-14',
     'assunto': 'Lote 135, bobina 1: 37,4 µm, primeira bobina da produção regular com a resina do F-13; refugada; '
                'o Caso integrado dizia "RNC 2027-19" (N10)',
     'estudos': ['Liberacao', 'Caso-Integrado']},
    {'org': 'industria', 'serie': 'PNC', 'numero': '2027-20', 'data': '2027-05-18',
     'assunto': 'Lote 137, bobina 3: géis; refugada', 'estudos': ['Liberacao']},
    {'org': 'industria', 'serie': 'PNC', 'numero': '2027-21', 'data': '2027-05-20',
     'assunto': 'Lote 140, duas bobinas com 43,1 e 43,4 µm; retido; cliente B aceitou sob concessão em 21/05 (P16)',
     'estudos': ['Liberacao']},
    {'org': 'industria', 'serie': 'PNC', 'numero': '2027-22', 'data': '2027-05-24',
     'assunto': 'Lote 135, bobina 2: reclamação do cliente A de filme fino; recolhida e reposta em 26/05; o Caso '
                'integrado dizia "RNC 2027-22" (N10)',
     'estudos': ['Liberacao', 'Caso-Integrado']},
    {'org': 'industria', 'serie': 'PNC', 'numero': '2027-23', 'data': '2027-05-25',
     'assunto': 'Resina úmida, lote R-0440, 2.000 kg; devolvida ao fornecedor', 'estudos': ['Liberacao']},
    {'org': 'industria', 'serie': 'PNC', 'numero': '2027-24', 'data': '2027-05-26',
     'assunto': 'Lote 143, bobina 1: largura de 603 mm; retrabalhada', 'estudos': ['Liberacao']},
    {'org': 'industria', 'serie': 'PNC', 'numero': '2027-25', 'data': '2027-05-26',
     'assunto': 'Lote 142: solda fraca, ensaio dois dias depois do embarque', 'estudos': ['Liberacao']},
    {'org': 'industria', 'serie': 'PNC', 'numero': '2027-29', 'data': '2027-07-06',
     'assunto': 'Bobina segregada e moída na quebra da resistência da zona 3 da extrusora 3; era "RNC 2027-29" (P10)',
     'estudos': ['Recursos', 'Histograma-CEP']},
    {'org': 'industria', 'serie': 'PNC', 'numero': '2027-30', 'data': '2027-07-18',
     'assunto': '6 bobinas com espessura fora, rosca desgastada da extrusora 3; era "RNC 2027-30" (P10)',
     'estudos': ['Recursos', 'Histograma-CEP']},
    # distribuidora: a cadeia de compras das ferramentas não tem registros numerados.
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
    {'id': 'T01', 'regex': r'[Dd]esvio isolado|oportunidade ou ponto a verificar', 'motivo': 'um desvio com evidência objetiva já é não conformidade', 'pastas': ['Tecnica-Auditoria']},
    {'id': 'T02', 'regex': r'corroborada por duas fontes', 'motivo': 'afirmação a corrigir', 'pastas': None},
    {'id': 'T02b', 'regex': r'precisa de duas fontes|regra das duas fontes|quais foram as duas fontes', 'motivo': 'a não conformidade pede uma fonte objetiva; a segunda é recomendada', 'pastas': ['Tecnica-Auditoria']},
    {'id': 'T03', 'regex': r'ainda não sustenta nada', 'motivo': 'a leitura que faltou é não conformidade pontual', 'pastas': ['Tecnica-Auditoria']},
    {'id': 'T04', 'regex': r'virou oportunidade de melhoria até a amostra', 'motivo': 'a quebra sem destino é não conformidade contra o 8.7', 'pastas': ['Tecnica-Auditoria']},
    {'id': 'T05', 'regex': r'A instrução pode definir quando e como treinar', 'motivo': 'a constatação 3 é não conformidade menor', 'pastas': ['Auditoria']},
    {'id': 'T06', 'regex': r'A verificação deve ser feita por quem não executou', 'motivo': 'verificação independente é convenção do material', 'pastas': ['Nao-Conformidade']},
    {'id': 'N02', 'regex': r'IT-05', 'motivo': 'a rotina de temperatura é a IT-PRO-01', 'pastas': ['Auditoria']},
    {'id': 'N20', 'regex': r'Desenvolvimento e produção de filmes', 'motivo': 'o escopo do certificado é o da declaração de Escopo', 'pastas': ['Certificacao']},
    {'id': 'N22a', 'regex': r'turno do almoço', 'motivo': 'a pizzaria não tem turno do almoço', 'pastas': ['Auditoria', 'Tecnica-Auditoria', 'Certificacao', 'Nao-Conformidade']},
    {'id': 'P09a', 'regex': r'revisão 2 da instrução, de julho', 'motivo': 'a revisão 2 da IT-EXP-01 é de 15/09/2026', 'pastas': ['Nao-Conformidade']},
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
               'auditoria interna passa a FR-09, o próximo número depois do FR-08: um salto na numeração sugeriria um '
               'documento retirado, e o próprio estudo ensina que um código não é reaproveitado. Os formulários da '
               'tabela de retenção entram na lista mestra de 22/01/2027: FR-02 Planilha de temperatura, FR-06 Registro '
               'de não conformidade, FR-08 Ata da análise crítica e FR-09 Relatório de auditoria interna (FR-05 já está). A lista '
               'passa de 13 para 17 documentos; os registros continuam 8; os cinco documentos fora de ordem continuam '
               'cinco. As instruções seguem o padrão IT-XXX-00: em Conhecimento, "IT-05" (montagem e conferência do '
               'pedido, K-04 e L-01) passa a IT-EXP-01, que já cobre a conferência no item 5, e "IT-08" (instrução do '
               'forno, L-05) passa a IT-PRO-02. O "IT-05" de Auditoria é outro documento: ver N02.',
     'estudos': ['Informacao-Documentada', 'Conhecimento']},
    {'id': 'P09',
     'conflito': 'IT-EXP-01 revisão 2 em 10/07/2026, antes do plano de 24/07.',
     'canone': 'IT-EXP-01 revisão 2 em 15/09/2026: é a ação A6 do 5W2H ("Atualizar a instrução de trabalho da '
               'expedição", 07/09 a 15/09) e a etapa 7 do PDCA (15/09/2026, "a instrução de trabalho da expedição foi '
               'atualizada"). A revisão vem depois do agrupamento por zona, que só começou na semana 8 do PDCA (de '
               '03/08/2026), e antes da auditoria 2026-03 (25/09/2026), que a usa como critério. (O spec dizia 31/07/2026; '
               'essa data viria antes do início do agrupamento e exigiria mudar o acompanhamento do 5W2H: ver N01.) '
               'Todos os lugares que derivam da data antiga, com valor antigo → novo e arquivo: (1) Informação '
               'documentada, lista mestra da pizzaria (exemplo 1, treinamento e planilha): data da IT-EXP-01 10/07/2026 → '
               '15/09/2026, em doc_data.py, EX1, linha da IT-EXP-01, D(2026, 7, 10) → D(2026, 9, 15); a coluna Próxima, '
               'calculada pelo gerador com o intervalo de 24 meses, passa de 07/2028 a 09/2028 sem outra edição. (2) '
               'Informação documentada, módulo 4, tabela dos campos da lista mestra, linha "Revisão e data": "Rev. 2 · '
               '10/07/2026" → "Rev. 2 · 15/09/2026" (doc_body.html). (3) A mesma tabela, linha "Intervalo de revisão", '
               'logo abaixo: "24 meses · próxima em 07/2028" → "24 meses · próxima em 09/2028" (doc_body.html, escrita à '
               'mão). (4) Informação documentada, figura 6: "IT-EXP-01 · REV. 2 · 10/07/2026" → "IT-EXP-01 · REV. 2 · '
               '15/09/2026" (build_doc_html.py). (5) Não conformidade, RNC 2026-05, etapa 4, porquê 3: "O roteiro foi '
               'escrito antes da revisão 2 da instrução, de julho de 2026, e não foi atualizado." → "O roteiro foi '
               'escrito antes da revisão 2 da instrução, de setembro de 2026, e não foi atualizado." (nc_data.py). '
               'Nenhum outro lugar das origens cita a data ou o mês da revisão 2 da IT-EXP-01: as outras menções a "rev. '
               '2" (aud_data.py, nc_data.py, proc_data.py) não têm data, e os outros "10/07/2026" e "D(2026, 7, 10)" '
               '(Pareto, PDCA etapa 2, Caso integrado, FR-05 da lista mestra, 5W2H da distribuidora) são de outros '
               'fatos e não mudam. Auditoria ("A equipe foi treinada em julho") não muda: o treinamento '
               'é a ação A3, de 27/07 a 30/07. 5W2H e PDCA não mudam.',
     'estudos': ['Informacao-Documentada', 'Nao-Conformidade']},
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
     'canone': 'Pizzaria (exemplo 2 de Fornecedores): as homologações mantêm as datas de hoje: P2 Queijaria do Campo em '
               '20/11/2026 (válida até 11/2028); P1, P3, P4, P5, P6 e P7 em 04/12/2026 (válidas até 12/2028). O que '
               'muda é a frase do "O que observar" que diz que a análise crítica "decidiu começar": as homologações '
               'começaram em novembro de 2026, como resposta ao risco R4 (segundo fornecedor de queijo), e a análise '
               'crítica de 14/12/2026 registrou o resultado e decidiu avaliar os fornecedores críticos a cada semestre. '
               'Texto: "A pizzaria nunca tinha avaliado fornecedores. As homologações começaram em novembro de 2026, '
               'como resposta ao risco R4: o segundo fornecedor de queijo foi homologado em 20/11/2026, e os outros '
               'seis, de uma vez, em 04/12/2026, com os fornecedores já em uso: cadastro, nota fiscal e uma visita. A '
               'análise crítica de 14/12/2026 registrou o resultado e decidiu avaliar os fornecedores críticos a cada '
               'semestre." As caixas de pizza (P5), item não crítico, saem da tabela de desempenho, e o total da classe A '
               'passa de 5 para 4 ("A: 4 · B: 2 · C: 0 · D: 0"). O gás (P6), crítico com documentos pendentes, continua '
               'comentado no "O que observar". A análise crítica da pizzaria de 14/12/2026 ("O segundo fornecedor foi '
               'homologado em novembro"; ação do R4 concluída) não muda. Indústria (exemplo 1 de Fornecedores): a '
               'avaliação do segundo semestre de 2026 passa a ser datada de 11/01/2027 (era 11/12/2026); no "O que '
               'observar" do exemplo 1, "A avaliação de dezembro" passa a "A avaliação de janeiro"; na análise crítica da '
               'indústria de 18/02/2027 (entrada c7), "avaliação de fornecedores de dezembro" passa a "de janeiro" '
               '(Análise crítica acrescentada à lista do spec).',
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
     'conflito': 'A revisão 2 da IT-EXP-01 em 31/07/2026, como o spec propunha para P09, bate com a ação A6 do 5W2H '
                 '("Atualizar a instrução de trabalho da expedição", 07/09 a 15/09/2026), com o acompanhamento de 05/08 '
                 '(A6 "Não iniciada"; a legenda da figura 4 diz que só a A4 está atrasada) e com o PDCA (agrupamento '
                 'só na semana 8, a partir de 03/08/2026; instrução atualizada na etapa 7, em 15/09/2026).',
     'canone': 'Vale o 5W2H, com o PDCA: a revisão 2 é de 15/09/2026 (P09). O 5W2H não muda em nenhum lugar: na tabela '
               'do exemplo 1, a A6 continua "07/09 a 15/09"; no acompanhamento de 05/08 (tabela e figura 4), a A6 '
               'continua "Não iniciada", com início 07/09 e prazo 15/09; a legenda da figura 4 continua "A ação A4 '
               'deveria ter terminado no dia 2 e aparece como atrasada"; w5_data.py não muda. O PDCA também não muda. '
               'Os estudos que mudam são os de P09: Informação documentada e Não conformidade.',
     'estudos': []},
    {'id': 'N02',
     'conflito': 'Em Auditoria (tabela de como escrever a constatação), "A instrução IT-05 pede o registro da temperatura '
                 'a cada turno", com as datas da constatação 2 da auditoria 2026-03 da pizzaria. A rotina de temperatura '
                 'é a IT-PRO-01, duas vezes por turno, e "IT-05" é outro documento em Conhecimento.',
     'canone': 'A frase passa a "A rotina IT-PRO-01 pede o registro da temperatura duas vezes por turno."',
     'estudos': ['Auditoria']},
    # N03 foi retirado na revisão do controlador: com as homologações nas datas de hoje (P13), a análise crítica da
    # pizzaria não muda. Os demais números N não foram renumerados.
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

    # ---------------------------------------------------------------- indústria (spec, seção 6.2)
    {'id': 'I01',
     'conflito': '"Certificada há 8 anos", contra a primeira certificação em 17/12/2027.',
     'canone': 'Primeira certificação em 17/12/2027 (ISO 9001:2015, válida até 16/12/2030). Antes disso, sistema '
               'implantado, sem certificado. SWOT, exemplo 3: o objeto passa a "Indústria de embalagens plásticas, com '
               'sistema de gestão da qualidade implantado, sem certificado", e o S1 a "Sistema de gestão implantado, com '
               'auditores internos formados" (16 pontos, sem mudança). Auditoria, exemplo 3: a organização passa a '
               '"Indústria de embalagens plásticas, com sistema de gestão implantado, sem certificado". Partes '
               'interessadas (20/01/2027), parte 8, Organismo de certificação: "Por que importa" passa a "Fará a '
               'auditoria de certificação, que dois grandes clientes passaram a exigir."; relacionamento "Contratação '
               'prevista para 2027 e contato do Coordenador da Qualidade."; o requisito passa a "Sistema pronto para a '
               'auditoria de certificação, com as não conformidades tratadas no prazo.", tipo Expectativa, situação '
               'Atende (as contagens não mudam). A expectativa da direção segue I14.',
     'estudos': ['SWOT', 'Partes-Interessadas', 'Auditoria']},
    {'id': 'I02',
     'conflito': '"Extrusora 4 em operação", contra "as três extrusoras".',
     'canone': 'Quatro extrusoras desde setembro de 2026. Recursos (julho de 2027): nas três linhas de operador de '
               'extrusão, a demanda passa a "4 extrusoras em operação" e as necessárias a 4; turnos A e B com 4 escaladas '
               'e 4 qualificadas (Justo); turno C com 3 escaladas e 3 qualificadas (Falta 1 pessoa). O resumo continua '
               '"8 funções e períodos, 2 com falta de gente: 2 pessoas a menos". "Alarme luminoso instalado nas três '
               'extrusoras" passa a "nas quatro extrusoras"; "O compressor de ar, de que as três extrusoras dependem" '
               'passa a "as quatro extrusoras"; a frase do chiller segue I19. "Pedidos redistribuídos entre as '
               'extrusoras 1 e 2" não muda.',
     'estudos': ['Recursos']},
    {'id': 'I03',
     'conflito': 'Nove mudanças de processo até setembro de 2027; "das 9 de 2027", com duas depois de outubro.',
     'canone': 'Onze mudanças de processo em 2027: nove até setembro (a população da auditoria 2027-11, de 06/10/2027, '
               'com 2 sem autorização) e duas em outubro e novembro, as duas sem autorização, depois da constatação da '
               'auditoria interna de outubro. Quatro sem autorização no ano. Em Certificação, a constatação I-3 passa a '
               '"Das 11 mudanças de processo de 2027, 4 sem autorização, 2 delas depois da constatação da auditoria '
               'interna de outubro: a ação corretiva não funcionou." Técnica de auditoria (população de 9, "9 no ano", '
               'lida até setembro) não muda.',
     'estudos': ['Certificacao']},
    {'id': 'I04',
     'conflito': '"Gerente de Produção", contra "Gerente industrial" e "Gerente de engenharia".',
     'canone': 'Valem os cargos de Auditoria (programa), Objetivos e Riscos: Gerente industrial, dono da Produção, e '
               'Gerente de engenharia, dono do Desenvolvimento de produto. Não existe "Gerente de Produção". Em Partes '
               'interessadas: nas partes 6 (Órgão ambiental) e 10 (Comunidade vizinha), "Gerente de Produção" passa a '
               '"Gerente industrial"; nas ações dos requisitos, "Levar a compra do medidor de espessura em linha à '
               'análise crítica" (18/02/2027) passa a "Gerente industrial", e "Abrir o projeto de resina reciclada, com '
               'fornecedor homologado" (30/06/2027) passa a "Gerente de engenharia"; a ação da expectativa da direção '
               'segue I14. Acrescentados à lista do spec: "gerente de produção" passa a "gerente industrial" em Recursos '
               '(responsável do exemplo 2), em Conhecimento (responsável do exemplo 2) e no Caso integrado (calendário, '
               'linha "Mapa do conhecimento").',
     'estudos': ['Partes-Interessadas', 'Recursos', 'Conhecimento', 'Caso-Integrado']},
    {'id': 'I05',
     'conflito': 'Processos "Extrusão", "Engenharia" e "Comercial e Qualidade", que não estão entre os nove.',
     'canone': 'Os nove de Processos (e do programa de Auditoria): 1 Comercial e análise de pedidos, 2 Desenvolvimento de '
               'produto, 3 Suprimentos, 4 Produção, 5 Laboratório e controle da qualidade, 6 Expedição e logística, 7 '
               'Manutenção, 8 Gestão de pessoas, 9 Gestão do sistema da qualidade. Na coluna Processo do quadro da '
               'indústria em Objetivos: O1 "Extrusão" passa a "Produção"; O2 "Comercial e Qualidade" passa a "Comercial e '
               'análise de pedidos"; O3 "Expedição" passa a "Expedição e logística"; O4 e O6 "Gestão do sistema" passam a '
               '"Gestão do sistema da qualidade"; O5 "Engenharia" passa a "Desenvolvimento de produto"; O7 '
               '"Suprimentos" não muda. Os responsáveis não mudam.',
     'estudos': ['Objetivos']},
    {'id': 'I06',
     'conflito': 'Análise crítica "de julho".',
     'canone': 'As análises críticas da indústria são semestrais: 12/02/2026, 13/08/2026, 18/02/2027 e 19/08/2027. Em '
               'Conhecimento (exemplo 2), a origem passa a "Análise crítica de 19/08/2027: as quebras da extrusora 3 '
               'mostraram que o desgaste da rosca só era medido pelo técnico do fabricante." Em Recursos (exemplo 2, '
               'julho de 2027), "Análise crítica do semestre" passa a "Preparação da análise crítica de 19/08/2027", com '
               'o resto da frase igual: a leitura de julho alimenta a análise de agosto, como no Caso integrado (passos '
               '10 e 11).',
     'estudos': ['Conhecimento', 'Recursos']},
    {'id': 'I07',
     'conflito': 'Medidor em linha: um ou dois, atraso antes do prazo, decisão antes da reclamação que a justifica.',
     'canone': 'Dois medidores de espessura em linha, para as extrusoras 3 e 4, R$ 96.000 com instalação, compra aprovada '
               'na análise crítica de 18/02/2027 (decisão 5, diretor geral), com prazo em 30/06/2027; não instalados em '
               '30/06 (Objetivos, 09/07/2027: atrasada); antecipação decidida em 19/08/2027. Escopo (10/05/2027), '
               'compromisso 5: "Aprovou os dois medidores de espessura em linha, de R$ 96.000, com instalação até '
               '30/06/2027; em maio, a compra ainda não tinha sido feita." (situação Parcial e ação sem mudança). '
               'Análise crítica de 18/02/2027, ação 7 da análise de 13/08/2026: "Instalar o medidor de espessura em '
               'linha na extrusora 3." passa a "Orçar os medidores de espessura em linha para as extrusoras 3 e 4.", '
               'decidida pelas reclamações de espessura do cliente A do primeiro semestre de 2026 (prazo, situação e '
               'resultado sem mudança: "Orçamento recebido. Compra não aprovada."). A reclamação de 14/09/2026 e o RNC '
               '2026-32 confirmaram a causa e levaram a proposta à análise de 18/02/2027. Caso integrado: passo 11 '
               'sem mudança; onde citar o medidor, "os dois medidores em linha".',
     'estudos': ['Escopo', 'Analise-Critica', 'Caso-Integrado']},
    {'id': 'I08',
     'conflito': 'Compras com duas histórias: formulário novo e devoluções de 40% para 12% em 2026, contra indicador em 30% '
                 'até setembro e RNC 2026-31.',
     'canone': 'A cadeia datada é da indústria (Suprimentos): auditoria 2026-07 (22/09/2026), RNC 2026-31 (22/09/2026, '
               'encerrado em 05/02/2027), indicadores C1 a C4 (C2 em 30% até setembro de 2026), riscos (12/10/2026), '
               'tartaruga (20/10/2026), RACI e SIPOC de "Adquirir materiais e serviços", ISO 9001 requisito a requisito, '
               'Informação documentada, Competências e Fornecedores. A cadeia das ferramentas (prazo de compra de 12 '
               'para 8 dias úteis, devoluções de 40% para 12%, formulário com campos obrigatórios, piloto na Manutenção '
               'e na Produção) é da "Distribuidora de materiais elétricos · Compras", com esse nome exato, no exemplo 2 '
               'de GUT, Pareto, Ishikawa, 5W2H e PDCA: no Pareto, o campo Organização passa de "Indústria de embalagens '
               'plásticas · Suprimentos" a esse nome; nos outros quatro, o cabeçalho do exemplo 2 ganha a linha '
               'Organização com esse nome. Cargos, áreas requisitantes, datas e números ficam como estão (ver '
               'ORGS["distribuidora"]); a cronologia segue N09, e a SWOT de origem, N08. Nas listas dos exemplos da '
               'planilha, "de Suprimentos" passa a "da distribuidora" (GUT, Ishikawa e 5W2H: "As matrizes/análises/'
               'planos da pizzaria e da distribuidora"; PDCA: "Os ciclos da pizzaria e da distribuidora"). O exemplo 3 '
               'desses estudos, dos instrumentos vencidos ("3 de 25"), continua da indústria (I19).',
     'estudos': ['GUT', 'Pareto', 'Ishikawa', '5W2H', 'PDCA']},
    {'id': 'I09',
     'conflito': 'Lote piloto da resina nova, contra "o lote 135 foi o primeiro"; resposta "dentro do critério", contra '
                 '37,9 µm medidos.',
     'canone': 'O lote piloto da resina do F-13 é o lote 127, de 05/05/2027, com duas bobinas: espessura e solda '
               'ensaiadas, dentro do critério. O lote 135, de 14/05/2027, é o primeiro da produção regular com a resina '
               'nova. Produção: na tabela de mudanças, a análise passa a "Lote piloto 127, de 05/05/2027, com duas '
               'bobinas: espessura e solda ensaiadas."; no "O que observar", "a primeira bobina com a resina do segundo '
               'fornecedor" passa a "a primeira bobina da produção regular com a resina do segundo fornecedor". '
               'Calibração (exemplo 3) conta em ordem: em 24/05, o cliente A reclama do lote 135 e a primeira resposta '
               'cita a medição da liberação, 39,1 µm, dentro do critério; em 26/05, a bobina devolvida é medida no '
               'laboratório, com o MIC-08: trechos com 37,9 µm; em 12/06, a verificação do MIC-07 mostra +1,6 µm, e a '
               'bobina corrigida tem 37,5 µm. Acrescentados à lista do spec: Liberação (2027-19: "na primeira bobina da '
               'produção regular com a resina do segundo fornecedor"; 2027-22: "Primeira resposta, em 24/05: 39,1 µm na '
               'liberação. Medida no laboratório em 26/05, com o MIC-08: trechos com 37,9 µm.") e Caso integrado (passo '
               '5: "Mudança registrada: resina do segundo fornecedor na extrusora 3, depois do lote piloto 127, de duas '
               'bobinas; o lote 135 é o primeiro da produção regular."; coluna "O que seguiu": "O lote 135, para liberar").',
     'estudos': ['Producao', 'Calibracao', 'Liberacao', 'Caso-Integrado']},
    {'id': 'I10',
     'conflito': 'Laudo de migração antes do lote de teste; ensaio com a resina B sem lote da resina B.',
     'canone': 'Projeto D-07: a mudança de resina (fornecedor B no lugar do A, pelo prazo de entrega) passa de 20/07 para '
               '08/07/2027, antes do lote de teste de 15/07, que já sai com a resina B. O laudo de migração (E4) passa de '
               '"Laudo de 12/07." para "Laudo de 18/07.", feito sobre o filme do lote de teste, antes da validação no '
               'cliente, que começa em 19/07. Na mudança de 08/07, "O que foi verificado de novo" passa de "Queda de '
               'dardo repetida com a resina B: 410 g, conforme." para "Queda de dardo no lote de teste, com a resina B: '
               '420 g, em 16/07, conforme." No "O que observar", "com o ensaio repetido" passa a "com o laudo e o ensaio '
               'no lote de teste". As outras datas não mudam.',
     'estudos': ['Projeto']},
    {'id': 'I11',
     'conflito': 'RNC 2026-29 em 23/09, depois do 2026-31 em 22/09.',
     'canone': 'Na série RNC da indústria, o número segue a data de abertura. O RNC 2026-31, de 22/09/2026, citado em '
               'sete estudos, não muda. O RNC de 23/09/2026 (espessura na extrusora 3, reclamação do cliente A) passa de '
               '2026-29 a 2026-32. Acrescentada à lista do spec: Satisfação (exemplo 3, linha de 23/09/2026).',
     'estudos': ['Caso-Integrado', 'Satisfacao']},
    {'id': 'I12',
     'conflito': 'ISO 9001:2015 "verificada" como vigente em 2027; figura 8 com números de Suprimentos diferentes do '
                 'exemplo; retenção e intervalo fora da regra.',
     'canone': 'Exemplo 3 (documentos externos, 05/03/2027): a linha da ISO 9001:2015 fica, com "Versão em uso" "Emenda '
               '1, de 2024; em uso até a transição", e entra a linha "ISO 9001:2026 · ISO e ABNT · Edição de 2026, '
               'comprada em 10/02/2027 · Todo o sistema, para a transição · Consulta ao site da ABNT a cada seis meses · '
               '10/02/2027 · 08/2027 · Verificado" (a compra é a etapa 1 do plano de transição da indústria). Figura 8: '
               'Suprimentos passa a 10 documentos, 7 em dia, 2 com revisão vencida (IT-REC-01 e FR-13) e 1 sem controle '
               '(o cadastro de itens), 70%, como o exemplo 2; os totais da figura são refeitos. Exemplo 2, regra: '
               '"Documentos revistos a cada 24 meses. Formulários e listas, a cada 12; a lista de fornecedores '
               'homologados, a cada 6, com a avaliação semestral. Registros retidos por 3 anos; os de compra, por 5, '
               'pelo prazo fiscal; os contratos, por 10."',
     'estudos': ['Informacao-Documentada']},
    {'id': 'I13',
     'conflito': '"Cinco etapas", contra oito; "O4" é oportunidade e objetivo; prazos de M5 e M6 depois do limite.',
     'canone': 'A transição tem oito etapas, as do plano do exemplo 2: comprar e ler a norma; diagnóstico das mudanças; '
               'plano aprovado pela direção; ações concluídas; conscientização da equipe; auditoria interna pela edição '
               'de 2026; análise crítica com a transição; auditoria do organismo. O módulo 3 e a figura 3 passam de '
               '"cinco etapas" a "oito etapas". A oportunidade deixa de ser chamada pelo código: na M4, "Riscos C1 a C8 '
               'e quatro oportunidades em listas separadas, desde 2026"; no exemplo 3, "A oportunidade dos clientes que '
               'exigem a ISO 9001 virou o objetivo O4"; "O4" fica só para o objetivo. A figura 7, cópia da matriz de '
               'Riscos, mantém os códigos. Os prazos do M5 (31/08/2028) e do M6 (30/09/2028) não mudam; o "O que '
               'observar" do exemplo 2 diz que o M6 vence depois do limite da etapa 4, ações concluídas (23/09/2028), e '
               'que o M5 fica a três semanas dele.',
     'estudos': ['ISO-9001-2026']},
    {'id': 'I14',
     'conflito': 'Refugo de 2,6% "atende em parte" com meta abaixo de 3%; contagens de quadrantes e de pendências.',
     'canone': 'Texto refeito pela tabela de Partes interessadas (20/01/2027). Expectativa da direção: "Refugo abaixo de '
               '3% e certificação ISO 9001 obtida."; como atende: "Refugo de 2,6% em 2026, com o ciclo PDCA. A '
               'certificação ainda é um projeto."; situação Atende em parte (pela certificação); ação "Contratar a '
               'auditoria de certificação", Diretor geral, 30/04/2027. As contagens não mudam: 16 requisitos, 15 '
               'adotados, 10 atendem, 4 em parte e 1 não atende, 80%. Quadrantes: gerir de perto 4, manter satisfeito 4, '
               'manter informado 2, monitorar 2. O "O que observar" passa a "O quadrante de manter satisfeito tem tantas '
               'partes quanto o de gerir de perto, quatro: dois órgãos reguladores, o fornecedor único de resina e o '
               'organismo de certificação." e, sobre as pendências, "Das cinco pendências, três estão nos clientes: a '
               'espessura do filme, que levou o medidor em linha à análise crítica, a entrega na data e a resina '
               'reciclada, uma expectativa de sustentabilidade que a fábrica adotou e ainda não atende. As outras duas '
               'são a certificação, esperada pela direção, e a matriz de competências fora de Suprimentos."',
     'estudos': ['Partes-Interessadas']},
    {'id': 'I15',
     'conflito': '"Dois antes do prazo" com três; definição em 19/02 com ações anteriores; meta de 96 com base de 97, que '
                 'o próprio estudo chama de erro.',
     'canone': 'Pizzaria (exemplo 1): "Em maio, quatro estão alcançados, e dois deles antes do prazo: a nota da pesquisa '
               'e os pedidos refeitos." passa a "Em maio, quatro estão alcançados, e três deles antes do prazo: as '
               'reclamações, a nota da pesquisa e os pedidos refeitos." Os objetivos são definidos em 19/02/2027, e as '
               'ações do O3 (27/01) e do O7 (20/01), concluídas antes, vêm da análise crítica de 14/12/2026: o "O que '
               'observar" acrescenta "As ações do O3 e do O7 foram decididas na análise crítica de dezembro e entraram '
               'no quadro já concluídas." Indústria (exemplo 2): o O3 passa a "Manter 97% das entregas na data '
               'confirmada.", meta 97 (base 97); o acompanhamento fica 97, 96, 97, 97, 98, 97, e fevereiro (96) passa a '
               'não atender à meta; último 97, Alcançado, caminho 100%. No módulo, o exemplo de objetivo de manter passa '
               'a "Manter 97% das entregas na data confirmada."',
     'estudos': ['Objetivos']},
    {'id': 'I16',
     'conflito': 'G1 com indicador e "não" no elemento; tartaruga e interações de Suprimentos diferentes.',
     'canone': 'Pizzaria: o G1 tem o indicador "Objetivos alcançados no ano", e o elemento g (avaliação) passa de "Não" '
               'para "Parcial": G1 com 5,0 pontos e 62% (arredondamento do gerador); a média é refeita pelo gerador. '
               'Indústria: a tartaruga (20/10/2026) e a matriz de interações ficam iguais. Na tartaruga, "O que entra" '
               'ganha "Resultado da inspeção de recebimento · Laboratório e controle da qualidade" e "Resultados de '
               'auditoria e ações · Gestão do sistema da qualidade", e a origem da requisição passa a "Produção e '
               'Manutenção". Nas interações do processo 3, "Recebe de 4 · Produção" passa a "Requisição de compra, com '
               'especificação, e plano de produção do mês". As saídas já batem.',
     'estudos': ['Processos']},
    {'id': 'I17',
     'conflito': '"Sete seguem para o cruzamento", com estratégias de fatores médios e ameaça alta sem estratégia.',
     'canone': 'Pizzaria (SWOT, exemplo 1). Só os sete fatores de prioridade alta entram no cruzamento: S1, S2, W1, W2, '
               'O1, O4 e T1. As seis estratégias passam a: S×O "S1 receita elogiada × O1 novos condomínios": "Fazer uma '
               'ação de boas-vindas nos novos condomínios, com degustação." (sem mudança); S×O "S2 entrega própria no '
               'prazo × O4 pedido por aplicativo de mensagens": "Lançar o pedido por mensagem, com a entrega própria no '
               'prazo como argumento."; W×O "W2 × O4" e "W1 × O1" sem mudança; S×T "S2 entrega própria no prazo × T1 '
               'aumento da taxa do aplicativo": "Divulgar a entrega própria no prazo para levar os clientes do aplicativo '
               'ao canal próprio."; W×T "W2 dependência do aplicativo × T1 aumento da taxa": "Negociar a taxa com o '
               'aplicativo e definir preços por canal, para que o aumento não consuma a margem." A ficha técnica e o '
               'custo por pizza (W3 × T3) saem do cruzamento. Acrescentado à lista do spec: em Objetivos, a origem do O6 '
               'passa de "Estratégia (SWOT)" a "Análise crítica".',
     'estudos': ['SWOT', 'Objetivos']},
    {'id': 'I18',
     'conflito': 'Visita ao cliente A decidida depois de feita.',
     'canone': 'A primeira visita ao cliente A foi em 02/10/2026 (Satisfação). Na análise crítica de 18/02/2027, a '
               'decisão 3 passa a "Fazer a segunda visita ao cliente A e rever o plano conjunto de outubro de 2026.", '
               'Gerente comercial, 19/03/2027. Acrescentado à lista do spec: em Objetivos, a ação do O2 passa a "Fazer a '
               'segunda visita ao cliente A e rever o plano conjunto.", concluída em 12/03/2027.',
     'estudos': ['Analise-Critica', 'Objetivos']},
    {'id': 'I19',
     'conflito': 'Instrumentos vencidos: meta em 60 dias e eficácia em 90; "três quebras" na figura e "duas" no texto; '
                 'chiller "parou todas" com uma extrusora a 100%.',
     'canone': 'Instrumentos vencidos (exemplo 3 de GUT, Ishikawa, 5W2H e PDCA, da indústria): auditoria interna de '
               'agosto de 2026, 3 de 25 instrumentos no laboratório de recebimento. Prazo de tratamento da GUT: 30 dias '
               '(sem mudança). Os 90 dias contam do fim da ação A3 do 5W2H, o cadastro único com aviso de vencimento, e '
               'a verificação da eficácia (A6) começa no 90º dia. Para isso, só o prazo da A3 muda: no 5W2H, exemplo 3, '
               'coluna Quando da A3 ("Centralizar o controle dos 25 instrumentos em um cadastro único"), "07/09 a 25/09" '
               'passa a "07/09 a 15/09" (w5_data.py, EX3, terceiro item: D(2026, 9, 25) passa a D(2026, 9, 15)). De '
               '15/09/2026, 90 dias dão 14/12/2026: a A6 continua "14/12 a 18/12", e o texto "nenhum instrumento vencido '
               'depois de 90 dias" e o "O que observar" ("data marcada para 90 dias depois") continuam certos. A A5 '
               '(28/09 a 09/10) e as outras ações não mudam. No PDCA, a meta passa de "Nenhum instrumento vencido, em 60 '
               'dias" a "Nenhum instrumento vencido, por 90 dias seguidos" (PDCA acrescentado à lista do spec; a etapa 6, '
               '"Depois de 3 meses", já está certa). Nos quatro estudos, o cabeçalho do exemplo 3 ganha a linha Organização: "Indústria de '
               'embalagens plásticas". Recursos: na figura 4, "As três quebras de julho vieram de peças que a preventiva '
               'atrasada teria trocado ou medido." passa a "Duas das três quebras de julho vieram de peças que a '
               'preventiva atrasada teria trocado ou medido." (o texto já diz duas: a de 27/07, cabo do termopar, não '
               'dependia da preventiva). "o chiller, com uma quebra só, parou as três extrusoras ao mesmo tempo" passa a '
               '"o chiller, com uma quebra só, fez as quatro extrusoras trabalharem em velocidade reduzida por 8 horas", '
               'como diz a contingência do CHI-01.',
     'estudos': ['GUT', 'Ishikawa', '5W2H', 'PDCA', 'Recursos']},

    # ---------------------------------------------------------------- indústria e distribuidora: contradições novas
    {'id': 'N08',
     'conflito': 'A GUT da distribuidora tira a lista da "Matriz SWOT da área", e os itens P1, P2 e P7 são os fatores W3, '
                 'W1 e W4 da SWOT, exemplo 2, mas a SWOT diz "Área de Suprimentos de uma indústria", é datada de '
                 '29/09/2026 (depois da GUT, ver N09) e tem W2 "Processo manual, em planilhas e e-mails", contra o '
                 'sistema de compras dos outros quatro estudos.',
     'canone': 'A SWOT, exemplo 2, é da distribuidora: o objeto passa a "Distribuidora de materiais elétricos · '
               'Compras"; a data, a 22/05/2026; o W2, a "Cotações e aprovações por e-mail, fora do sistema de compras" '
               '(16 pontos, sem mudança). Título, responsável, notas e estratégias não mudam. Na lista dos exemplos da '
               'planilha, "As matrizes da pizzaria e de Suprimentos" passa a "da pizzaria e da distribuidora".',
     'estudos': ['SWOT']},
    {'id': 'N09',
     'conflito': 'Cronologia da distribuidora: o Ishikawa (26/06/2026) e o 5W2H (03/07/2026) citam a "Matriz GUT da '
                 'área", mas a GUT é de 29/09/2026, com 40% de devoluções e 12 dias de prazo, depois do ciclo que os '
                 'reduziu (verificação em 28/08/2026), e decide "abrir um ciclo PDCA" já aberto em 01/06/2026. A etapa 5 '
                 'do PDCA tem data de 31/07/2026, e o piloto do 5W2H vai até 07/08/2026.',
     'canone': 'Vale a sequência do PDCA: GUT, exemplo 2, datada de 29/05/2026, antes do ciclo; prazos das decisões: P6 '
               '09/06/2026, P1 18/08/2026, P3 30/06/2026 e P4 16/06/2026 (era 09/10, 18/12, 30/10 e 16/10/2026). No PDCA, '
               'exemplo 2, a data da etapa 5 passa de 31/07/2026 a 07/08/2026, o fim do piloto. Os valores da matriz não '
               'mudam.',
     'estudos': ['GUT', 'PDCA']},
    {'id': 'N10',
     'conflito': 'Caso integrado chama de "RNC 2027-19" e "RNC 2027-22" dois registros de produto não conforme da '
                 'Liberação (série PNC, como em P10).',
     'canone': 'Nos passos 6 e 7 do fio da indústria, "RNC 2027-19" passa a "Registro de produto não conforme 2027-19" e '
               '"RNC 2027-22" a "Registro de produto não conforme 2027-22". Os números não mudam.',
     'estudos': ['Caso-Integrado']},
    {'id': 'N11',
     'conflito': 'SWOT, exemplo 3: responsável "Diretor industrial"; nos outros estudos, a indústria tem diretor geral e '
                 'gerente industrial.',
     'canone': 'O responsável da SWOT da indústria passa a "Diretor geral".',
     'estudos': ['SWOT']},
    {'id': 'N12',
     'conflito': 'Partes interessadas, parte 3 (Direção e acionistas): "Análise crítica anual"; a análise crítica da '
                 'indústria é semestral (I06).',
     'canone': 'O relacionamento passa a "Análise crítica a cada semestre e reunião mensal de resultados."',
     'estudos': ['Partes-Interessadas']},
    {'id': 'N13',
     'conflito': 'Partes interessadas, parte 7: "Três itens críticos têm fornecedor único"; ISO 9001 requisito a requisito: '
                 '"os itens de fornecedor único". Riscos (C1), Fornecedores, Análise crítica e Caso integrado: um só '
                 'fornecedor, o da resina de polietileno (F-01).',
     'canone': 'O item crítico de fornecedor único é a resina de polietileno, até a homologação do F-13 em 29/03/2027. '
               'Partes interessadas, parte 7: "A resina de polietileno tem fornecedor único." ISO 9001 requisito a '
               'requisito (6.1, O que falta): "Definir ação para a resina, de fornecedor único."',
     'estudos': ['Partes-Interessadas', 'ISO-9001']},
    {'id': 'N14',
     'conflito': 'Objetivos: a ação do O5 "Homologar o fornecedor de resina reciclada", com os ensaios externos de R$ '
                 '12.000, prazo 31/03/2027 e conclusão em 29/03/2027, é a decisão 9 da análise crítica (homologar o '
                 'segundo fornecedor de resina, F-13, pelo risco C1), que o Caso integrado diz homologado "por outro '
                 'motivo".',
     'canone': 'O F-13, Resinas Atlântico, é o segundo fornecedor de resina de polietileno (risco C1) e oferece também a '
               'resina reciclada de menor custo (oportunidade O3 de Riscos). Em Objetivos, a ação passa a "Homologar o '
               'segundo fornecedor de resina, que oferece a resina reciclada."; recursos, responsável, prazo e conclusão '
               'não mudam.',
     'estudos': ['Objetivos']},
    {'id': 'N15',
     'conflito': 'Não conformidade e Processos (setembro e outubro de 2026): quatro compradores; Competências (12/03/2027): '
                 'quatro compradores, um deles admitido em janeiro de 2027.',
     'canone': 'Um comprador saiu no fim de 2026, e Camila foi admitida em janeiro de 2027 no lugar dele: são quatro '
               'compradores nos dois momentos. Nenhum estudo muda.',
     'estudos': []},
    {'id': 'N16',
     'conflito': 'Conhecimento, lição I-02: "Procedimento de compras PC-02"; o procedimento de compras da indústria é o '
                 'PR-SUP-01, em seis estudos.',
     'canone': 'Onde incorporar a lição I-02 passa a "Procedimento PR-SUP-01".',
     'estudos': ['Conhecimento']},
    {'id': 'N17',
     'conflito': 'Códigos de documentos da indústria fora do padrão que Informação documentada ensina (tipo-processo-número, '
                 'como PR-SUP-01): PQ-08, PE-11, PE-14, PG-05, PM-01, FM-02 e IE-12.',
     'canone': 'Não aplicar nesta leva: padronizar exige trocar códigos em Conhecimento, Caso integrado, Técnica de '
               'auditoria e Projeto, e o spec não prevê. Os códigos ficam registrados como estão. Fica para a revisão do '
               'autor.',
     'estudos': []},
    {'id': 'N18',
     'conflito': 'Não conformidade, exemplo 3 (injeção de tampas, desenho D-118, lotes 2607 e 2655): a organização é '
                 '"Indústria de embalagens plásticas", que só faz filmes (Escopo, Certificação).',
     'canone': 'O exemplo é de outra organização, que não volta na série: o campo Organização passa a "Fábrica de tampas '
               'plásticas por injeção".',
     'estudos': ['Nao-Conformidade']},
    {'id': 'N19',
     'conflito': 'Calibração (30/06/2027): "Instrumentos · 7 cadastrados"; auditoria de 2026, 5W2H e Técnica de auditoria: '
                 '25 instrumentos em uso.',
     'canone': 'O exemplo mostra 7 dos 25 instrumentos, os da extrusora 3 e do laboratório. O título da tabela passa a '
               '"Instrumentos da extrusora 3 e do laboratório · 7 dos 25 cadastrados", com o resto das contagens igual.',
     'estudos': ['Calibracao']},
    {'id': 'N20',
     'conflito': 'Certificação, escopo do certificado: "Desenvolvimento e produção de filmes técnicos lisos e impressos para '
                 'embalagem de alimentos"; Escopo (10/05/2027): "Projeto, fabricação e expedição de filmes plásticos '
                 'técnicos, lisos e impressos, para embalagem de alimentos."',
     'canone': 'Vale a declaração do Escopo, que o certificado repete: o campo Escopo de Certificação passa a "Projeto, '
               'fabricação e expedição de filmes plásticos técnicos, lisos e impressos, para embalagem de alimentos."',
     'estudos': ['Certificacao']},
    {'id': 'N21',
     'conflito': 'A declaração de escopo restringe a indústria a "embalagem de alimentos", e o Escopo diz que ela "não '
                 'exclui nada que a fábrica faça", mas Satisfação e Partes interessadas têm clientes de cosméticos (18) e '
                 'industriais (16).',
     'canone': 'Não aplicar nesta leva: acertar exige reescrever as declarações e a figura do Escopo, o escopo de '
               'Certificação e conferir Partes interessadas e Satisfação, e o spec não prevê. Fica para a revisão do autor.',
     'estudos': []},
    {'id': 'N22',
     'conflito': 'A pizzaria abre das 18h à meia-noite (Recursos, base das contas de disponibilidade, 180 horas no mês), '
                 'mas quatro estudos citam um "turno do almoço": a equipe auditora de Auditoria ("Atendente e pizzaiolo '
                 'do turno do almoço"), os auditores de Técnica de auditoria, o responsável do critério 7 de Certificação '
                 'e o auditor líder do RNC 2026-05 na planilha de Não conformidade. Indicadores diz que "O turno do '
                 'almoço entrega 96% no prazo", como se a loja entregasse no almoço.',
     'canone': 'Vale o horário de Recursos (contas conferidas). A loja tem dois turnos: o da tarde, antes da abertura, sem '
               'atendimento a clientes (é nele que a loja recebe os insumos, às 15h, como em Técnica de auditoria), e o da '
               'noite, das 18h à meia-noite. "Turno do almoço" passa a "turno da tarde" em todos os lugares: Auditoria, '
               'exemplo 1, equipe auditora: "Atendente e pizzaiolo do turno da tarde" (aud_body.html e aud_data.py, '
               'lider e equipe); Técnica de auditoria, exemplo 1: auditor líder "Atendente do turno da tarde", equipe '
               '"Pizzaiolo do turno da tarde", e as duas colunas da tabela de avaliação dos auditores com os mesmos nomes '
               '(tec_data.py, cabeçalho e avaliação); Certificação, critério 7 da prontidão da pizzaria: responsável '
               '"Atendente do turno da tarde" (cert_data.py); Não conformidade, RNC 2026-05: "Atendente do turno da '
               'tarde, auditor líder" (nc_data.py). Indicadores, módulo da meta, linha "Uma referência": "O turno do '
               'almoço entrega 96% no prazo." passa a "As pizzarias da região entregam 96% no prazo, pelo relatório do '
               'aplicativo de delivery." (ind_body.html); o número 96 não entra em nenhuma conta e fica. Os "atendentes '
               'da noite", o "garçom do turno da noite" e o "cansaço do turno da noite" não mudam.',
     'estudos': ['Auditoria', 'Tecnica-Auditoria', 'Certificacao', 'Nao-Conformidade', 'Indicadores']},
    {'id': 'N23',
     'conflito': 'Achado na tarefa 3 (núcleo de auditoria). Pelo item T05 do spec, a constatação 3 da auditoria 2026-03 '
                 '(entregador admitido em setembro sem o treinamento na IT-EXP-01) passa de oportunidade de melhoria a '
                 'não conformidade menor nº 3. Dois estudos ainda contam o resultado antigo: a análise crítica de '
                 '14/12/2026 (c4: dois registros; c6: "duas não conformidades menores e uma oportunidade de melhoria", '
                 'texto que N05 mantinha) e Competências ("A integração, que a auditoria sugeriu").',
     'canone': 'Vale T05 (spec, aprovado). A auditoria 2026-03 teve três não conformidades menores e nenhuma oportunidade '
               'de melhoria. Na análise crítica (ac_data.py), as frases de N05 passam a: c4 "Três registros abertos pela '
               'auditoria 2026-03. O RNC 2026-05 foi encerrado como eficaz. Os outros dois estão em verificação." (o '
               'segundo é o da temperatura, que c5 dá como registrada em todos os turnos desde outubro; o terceiro é o do '
               'treinamento, cuja eficácia saiu parcial em Competências); c6 "A auditoria 2026-03, no delivery: três não '
               'conformidades menores. O salão e as compras nunca foram auditados." Esta entrada substitui o texto de c4 e '
               'c6 dado em N05, e foi aplicada na tarefa 3. Em Competências (comp_body.html, exemplo 1, "O que observar"), '
               '"A integração, que a auditoria sugeriu, passa a ser" passa a "A integração, ação corretiva da não '
               'conformidade da auditoria, passa a ser". Nenhuma conta muda: a avaliação de c4 (Favorável) e a de c6 '
               '(Atenção) ficam.',
     'estudos': ['Analise-Critica', 'Competencias']},
]
