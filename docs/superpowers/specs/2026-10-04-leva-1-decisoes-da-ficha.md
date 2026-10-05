# Leva 1: decisões da ficha de fatos

Gerado de `DECISOES`, em `_geradores/fatos.py`, para a revisão do autor prevista na seção 4.4 do desenho. Cada entrada diz qual versão passa a valer e que estudos mudam. A fonte é a ficha: se uma decisão mudar, muda lá, e este arquivo é gerado de novo.

## Decididas depois da aprovação do autor

O autor aprovou as decisões como estavam em 04/10/2026 (commit d89fe50). As entradas abaixo foram decididas ou emendadas depois, durante as correções da leva e na revisão final de todo o ramo, e esperam a revisão dele. Cada uma está no seu grupo, mais abaixo, com o texto completo; nas emendadas, o trecho novo diz o que mudou e por quê.

**Entradas novas (15):** N23, N24, N25, N26, N27, N28, N29, N30, N31, N32, N33, N34, N35, N36, N37

**Entradas emendadas (19):** P06, P07, P08, P13, P15, P17, P18, P22, N01, N02, N05, N07, I02, I07, I08, I13, I16, I18, I19

**Na revisão final de todo o ramo:** novas N36, N37; emendadas P06, P07, P08, P13, P15, P17, P22, N01, N02, N07, I02, I07, I08, I13, I16, I19, N31. Nas emendadas, o texto diz o que mudou citando a revisão final ou a entrada nova que a emenda (N36, N37); a N01 foi reescrita como um só estado final.

## Pizzaria: itens do desenho (P)

23 decisões.

### P01

**Estudos que mudam:** Pedidos

**Conflito.** A loja "não abre às segundas", com registros em 08, 15 e 22/03/2027, que são segundas.

**Decisão.** A loja abre todos os dias, das 18h à meia-noite. Só a encomenda para eventos (a partir de 20 pizzas, com 48 horas de antecedência) é atendida de terça a domingo, das 18h às 23h. Na oferta de Pedidos, "de terça a domingo" fica só na linha da encomenda para eventos. A recusa da E-33 passa a "A loja não atende encomendas para eventos às segundas, e o horário de encomenda começa às 18h."

### P02

**Estudos que mudam:** Competencias, Conhecimento

**Conflito.** Oito pessoas em Competências; equipe bem maior em Recursos; "quatro pizzaiolos" em Conhecimento.

**Decisão.** Vale Recursos: no pico de sexta, 2 atendentes, 3 pizzaiolos, 1 forneiro, 2 na expedição, 8 entregadores e 3 no salão, além do gerente. A matriz de Competências continua com as oito pessoas dos postos-chave (Marina, Carla, Diego, Rafael, Bruno, Sérgio, Paulo e Igor), e o texto diz que ela não é a loja inteira. Em Conhecimento (questionário e figura), "quatro pizzaiolos" passa a "os três pizzaiolos e o forneiro"; o K-03 continua com 4 pessoas que sabem.

### P03

**Estudos que mudam:** Competencias

**Conflito.** Bruno regula o forno sozinho em fevereiro de 2027; em maio, só o pizzaiolo líder sabe.

**Decisão.** Valem Conhecimento e Caso integrado: em maio de 2027, só Rafael regula o forno e a chama do lastro. Em Competências, a ação 1 do plano (Bruno, C3) passa a "Parcial: reforçar", com a evidência "Regula a temperatura em turno normal. Não reacende nem regula a chama do lastro, e a regulagem segue sem registro. Risco R6 continua aberto." O nível de Bruno em C3 fica em 1 (não sobe para 2), e as contagens de lacunas e o texto do "O que observar" são refeitos. Objetivos (ação do O7 concluída em 20/01/2027) não muda: a ação foi feita; a eficácia é que foi parcial.

### P04

**Estudos que mudam:** Conhecimento

**Conflito.** Pizzaiolo líder "há 12 anos" e "desde 06/2021".

**Decisão.** Rafael, pizzaiolo líder, desde 06/2021. Em Conhecimento, "há 12 anos na loja" passa a "há seis anos na loja".

### P05

**Estudos que mudam:** Riscos

**Conflito.** Alarme da câmara fria com prazo em 11/2026 e ações dadas como concluídas; em 04/2027, "não havia alarme". Preventiva semestral e trimestral.

**Decisão.** Vale Recursos: preventiva da câmara fria (CAM-01) a cada três meses (última em 10/01/2027; a de 10/04/2027 não foi feita); o alarme de temperatura só foi instalado em 13/04/2027, depois da quebra de 12/04. No R3 de Riscos, a resposta passa a "Reduzir. Fazer a manutenção preventiva a cada três meses." O residual não muda.

### P06

**Estudos que mudam:** ISO-9001-2026, Conhecimento, Recursos

**Conflito.** Sistema de pedidos trocado em julho de 2026 e em abril de 2027.

**Decisão.** A troca do sistema de pedidos foi em julho de 2026, sem teste e sem treinamento. Em abril de 2027 houve uma atualização de versão (SIS-01, preventiva de 01/04/2027). Em ISO 9001:2026 (M5: "Atualização de versão do sistema de pedidos sem plano, em abril de 2027" e o "O que observar"), em Conhecimento (K-05 e exemplo 3) e em Recursos, o evento de abril de 2027 passa a "atualização de versão do sistema de pedidos". Revisão final: a evidência do M5 citava um lançamento de produto feito como projeto (8.3), e não uma mudança no sistema (6.3): ed26_data.py, "Lançamento da pizza vegana planejado pelo projeto P-03; a atualização de versão…" → "Inclusão do salão no sistema planejada na análise crítica de 14/12/2026, com responsável e prazo; a atualização de versão do sistema de pedidos, em abril de 2027, foi feita sem plano" (a decisão b daquela análise, descrever o atendimento no salão, com a gerente da loja e prazo em 26/02/2027). Em Recursos, "nenhum conhece o sistema de pedidos trocado sem treinamento" → "nenhum foi treinado no sistema de pedidos, trocado em julho de 2026 sem treinamento da equipe." (rec_body.html).

### P07

**Estudos que mudam:** Indicadores

**Conflito.** Entregas no prazo: 88 e 94 em junho e julho de 2026, contra 80 a 84 por semana até 26/07.

**Decisão.** Vale a série semanal do PDCA (semana 1 = 15/06/2026): 81, 83, 80, 84, 82, 82, 86, 90, 94, 96, 95, 97. Cada mês é a média das semanas que começam nele: jun/26 = semanas 1 a 3 = 81 (81,3); jul/26 = semanas 4 a 7 = 84 (83,5); ago/26 = semanas 8 a 12 = 94 (94,4). Em Indicadores, P1 passa de 88, 94 e 96 para 81, 84 e 94 em jun/26, jul/26 e ago/26; a série de out/25 a set/26 fica 81, 83, 80, 82, 82, 83, 82, 84, 81, 84, 94, 95, e a média do ano passa de 85,8 para 84,3 (84,25, arredondada para cima como na planilha; o gerador do treinamento passou a arredondar do mesmo modo: N37). Agosto fica abaixo da meta de 95, na faixa de atenção: a célula do mês fica cinza. Set/26 (95) não muda, nem a situação "Na meta", os "seguidos sem a meta" (0) e a tendência ("Melhorando"). Propagar a quem citar 88, 94 ou 96 como valor mensal de junho a agosto de 2026, ou a média do ano: nenhum outro estudo cita. Revisão final (decisão do controlador, à espera da revisão do autor): a versão aprovada aplicava a regra só a junho e julho e mantinha ago/26 em 96, com média do ano 84,4; pela mesma regra agosto dá 94,4, e um valor mensal não pode ficar no máximo das semanas do mês (ponderado pelas entregas do Pareto, cerca de 93). Valor antigo → novo: ind_data.py, EX1, P1, valores, 96 → 94 (11º mês); média do ano 84,4 → 84,3; regra P07 de PROIBIDO com "84,4" e "81 84 96 95". Nenhum texto de Indicadores ou do PDCA diz que o valor mensal é a média das semanas.

### P08

**Estudos que mudam:** Informacao-Documentada, Conhecimento

**Conflito.** FR-07 é relatório de auditoria e planilha de verificação; formulários da tabela de retenção fora da lista mestra; IT-05 e IT-08 fora do padrão.

**Decisão.** FR-07 é só a planilha de verificação dos instrumentos (Calibração, Técnica de auditoria). O relatório de auditoria interna passa a FR-09, o próximo número depois do FR-08: um salto na numeração sugeriria um documento retirado, e o próprio estudo ensina que um código não é reaproveitado. Os formulários da tabela de retenção entram na lista mestra de 22/01/2027: FR-02 Planilha de temperatura, FR-06 Registro de não conformidade, FR-08 Ata da análise crítica e FR-09 Relatório de auditoria interna (FR-05 já está). A lista passa de 13 para 17 documentos; os registros continuam 8; os cinco documentos fora de ordem continuam cinco. As instruções seguem o padrão IT-XXX-00: em Conhecimento, "IT-05" (montagem e conferência do pedido, K-04 e L-01) passa a IT-EXP-01, que já cobre a conferência no item 5, e "IT-08" (instrução do forno, L-05) passa a IT-PRO-02. O "IT-05" de Auditoria é outro documento: ver N02. Revisão final: o FR-06 e o FR-09 entraram na lista mestra com data de 20/10/2026, depois da auditoria 2026-03 e do RNC 2026-05, de setembro, que os usaram; a data dos dois passa a 01/09/2026 (doc_data.py, D(2026, 10, 20) → D(2026, 9, 1)); a próxima revisão, calculada, passa de 10/2028 a 09/2028.

### P09

**Estudos que mudam:** Informacao-Documentada, Nao-Conformidade

**Conflito.** IT-EXP-01 revisão 2 em 10/07/2026, antes do plano de 24/07.

**Decisão.** IT-EXP-01 revisão 2 em 15/09/2026: é a ação A6 do 5W2H ("Atualizar a instrução de trabalho da expedição", 07/09 a 15/09) e a etapa 7 do PDCA (15/09/2026, "a instrução de trabalho da expedição foi atualizada"). A revisão vem depois do agrupamento por zona, que só começou na semana 8 do PDCA (de 03/08/2026), e antes da auditoria 2026-03 (25/09/2026), que a usa como critério. (O spec dizia 31/07/2026; essa data viria antes do início do agrupamento e exigiria mudar o acompanhamento do 5W2H: ver N01.) Todos os lugares que derivam da data antiga, com valor antigo → novo e arquivo: (1) Informação documentada, lista mestra da pizzaria (exemplo 1, treinamento e planilha): data da IT-EXP-01 10/07/2026 → 15/09/2026, em doc_data.py, EX1, linha da IT-EXP-01, D(2026, 7, 10) → D(2026, 9, 15); a coluna Próxima, calculada pelo gerador com o intervalo de 24 meses, passa de 07/2028 a 09/2028 sem outra edição. (2) Informação documentada, módulo 4, tabela dos campos da lista mestra, linha "Revisão e data": "Rev. 2 · 10/07/2026" → "Rev. 2 · 15/09/2026" (doc_body.html). (3) A mesma tabela, linha "Intervalo de revisão", logo abaixo: "24 meses · próxima em 07/2028" → "24 meses · próxima em 09/2028" (doc_body.html, escrita à mão). (4) Informação documentada, figura 6: "IT-EXP-01 · REV. 2 · 10/07/2026" → "IT-EXP-01 · REV. 2 · 15/09/2026" (build_doc_html.py). (5) Não conformidade, RNC 2026-05, etapa 4, porquê 3: "O roteiro foi escrito antes da revisão 2 da instrução, de julho de 2026, e não foi atualizado." → "O roteiro foi escrito antes da revisão 2 da instrução, de setembro de 2026, e não foi atualizado." (nc_data.py). Nenhum outro lugar das origens cita a data ou o mês da revisão 2 da IT-EXP-01: as outras menções a "rev. 2" (aud_data.py, nc_data.py, proc_data.py) não têm data, e os outros "10/07/2026" e "D(2026, 7, 10)" (Pareto, PDCA etapa 2, Caso integrado, FR-05 da lista mestra, 5W2H da distribuidora) são de outros fatos e não mudam. Auditoria ("A equipe foi treinada em julho") não muda: o treinamento é a ação A3, de 27/07 a 30/07. 5W2H e PDCA não mudam.

### P10

**Estudos que mudam:** Recursos, Histograma-CEP, Liberacao

**Conflito.** "RNC" usado para duas séries; RNC 2027-04 em 03/04 e RNC 2027-07 em 22/03.

**Decisão.** Duas séries com nomes diferentes: "RNC" (não conformidade e ação corretiva, 10.2) e "registro de produto não conforme" (8.7, série PNC na ficha). Os números 2027-27, 2027-29 e 2027-30 são registros de produto não conforme: em Recursos, "RNC 2027-27" (pizzaria, 12/04/2027) passa a "registro de produto não conforme 2027-27"; "RNC 2027-29" e "RNC 2027-30" (indústria, bobinas de julho de 2027) passam a "registro de produto não conforme 2027-29" e "2027-30" em Recursos e em Histograma e CEP. Na série RNC da pizzaria, o RNC de 22/03/2027 da Liberação passa de 2027-07 a 2027-03, antes do 2027-04 de 03/04/2027.

### P11

**Estudos que mudam:** Objetivos

**Conflito.** "Pedidos refeitos" é do P1 num estudo e do P2 em outro.

**Decisão.** Vale Processos: o indicador "Pedidos refeitos por erro" é do P1, Registrar o pedido. Em Objetivos, o processo do O4 passa de "Produzir e embalar (P2)" a "Registrar o pedido (P1)". O responsável do O4 e a ação (conferir o pedido na tela antes de montar) continuam com o pizzaiolo líder.

### P12

**Estudos que mudam:** Escopo

**Conflito.** Escopo sem o processo "Atender no salão"; riscos revistos uma vez por ano, contra a revisão semestral; dono e gerente misturados.

**Decisão.** Valem Processos e Caso integrado: nove processos (G1, G2, P1 a P4, A1 a A3), e a linha "Processos" do Escopo ganha "atender no salão". O compromisso 4 da liderança passa a "Os riscos são revistos a cada seis meses", frequência "Semestral · Matriz de riscos" (revisões em abril e outubro; a de MP-02 marcada para 05/04/2027). Papéis: o dono da loja dirige a loja (G1), conduz a análise crítica e aprova; o gerente da loja é dono de G2, P4, A1 e A3 e conduz o dia a dia.

### P13

**Estudos que mudam:** Fornecedores, Analise-Critica

**Conflito.** Caixas "sem avaliação formal", mas avaliadas; homologações antes da decisão de 14/12/2026; avaliação de 11/12 para o semestre inteiro; gás crítico com documentos pendentes.

**Decisão.** Pizzaria (exemplo 2 de Fornecedores): as homologações mantêm as datas de hoje: P2 Queijaria do Campo em 20/11/2026 (válida até 11/2028); P1, P3, P4, P5, P6 e P7 em 04/12/2026 (válidas até 12/2028). O que muda é a frase do "O que observar" que diz que a análise crítica "decidiu começar": as homologações começaram em novembro de 2026, como resposta ao risco R4 (segundo fornecedor de queijo), e a análise crítica de 14/12/2026 registrou o resultado e decidiu avaliar os fornecedores críticos a cada semestre. Texto: "A pizzaria nunca tinha avaliado fornecedores. As homologações começaram em novembro de 2026, como resposta ao risco R4: o segundo fornecedor de queijo foi homologado em 20/11/2026, e os outros seis, de uma vez, em 04/12/2026, com os fornecedores já em uso: cadastro, nota fiscal e uma visita. A análise crítica de 14/12/2026 registrou o resultado e decidiu avaliar os fornecedores críticos a cada semestre." As caixas de pizza (P5), item não crítico, saem da tabela de desempenho, e o total da classe A passa de 5 para 4 ("A: 4 · B: 2 · C: 0 · D: 0"). O gás (P6), crítico com documentos pendentes, continua comentado no "O que observar". A análise crítica da pizzaria de 14/12/2026 ("O segundo fornecedor foi homologado em novembro"; ação do R4 concluída) não muda. Indústria (exemplo 1 de Fornecedores): a avaliação do segundo semestre de 2026 passa a ser datada de 11/01/2027 (era 11/12/2026); no "O que observar" do exemplo 1, "A avaliação de dezembro" passa a "A avaliação de janeiro"; na análise crítica da indústria de 18/02/2027 (entrada c7), "avaliação de fornecedores de dezembro" passa a "de janeiro" (Análise crítica acrescentada à lista do spec). Revisão final: a frase "e os outros seis, de uma vez, em 04/12/2026, com os fornecedores já em uso: cadastro, nota fiscal e uma visita." dava os seis como homologados, e o gás ficou pendente; passa a "e os outros seis passaram pela homologação de uma vez, em 04/12/2026, com os fornecedores já em uso: cadastro, nota fiscal e uma visita. Cinco foram homologados, e o de gás ficou com documentos pendentes." (forn_body.html). No erro comum "Esquecer o serviço", "A transportadora e a manutenção nunca foram avaliadas." → "A manutenção e a revisão das motos nunca foram avaliadas.", porque a transportadora (F-09) é processo terceirizado (N30).

### P14

**Estudos que mudam:** Pedidos

**Conflito.** "Quatro resolvidos" com duas recusas; "3 das 8 encomendas"; E-34 fora das 48 horas sem comentário.

**Decisão.** Texto refeito pela tabela de Pedidos: 8 pedidos, 4 aceitos (E-31, T-1184, E-34, E-35), 2 aceitos com alteração (E-32, T-1201) e 2 recusados (A-772, E-33); 5 são encomendas para eventos (E-31 a E-35). A E-34, analisada em 26/03 para 27/03 às 20h, foi aceita com menos de 48 horas de antecedência, e o texto diz isso. A E-33 não teve "outro dia": o cliente recusou.

### P15

**Estudos que mudam:** Producao

**Conflito.** Frequências do plano de controle que não batem com o número de registros; mudança de 26/03 em registros lidos em 15/03; reação do K5 depois da saída.

**Decisão.** Os totais não mudam: K1 com 14 verificações e K2 a K7 com 7 cada, nas noites de 08 a 14/03/2027 (56 no total, 6 fora). A frequência escrita passa a corresponder a esses totais, e acompanha o risco: as conferências são feitas durante a noite e no pico, e o registro de cada noite é um resumo delas (corrigido por N31, que traz o texto de cada controle). K1 com duas leituras por dia, uma em cada turno, cada uma registrada (N36). A tabela de mudanças no processo ganha a própria data de leitura, 31/03/2027, e mantém a mudança de 26/03/2027. A reação do K5 é reescrita para acontecer antes da saída do pedido.

### P16

**Estudos que mudam:** Liberacao

**Conflito.** Decisões tomadas por quem não tem a autoridade escrita; lote 140 liberado sem quem liberou; "segue aberto" contra "0 abertos"; "2 fora" com três fora.

**Decisão.** Em cada registro de produto não conforme, quem decidiu é a função que o cabeçalho de autoridades indica. Pizzaria: no 2027-20 (troca no cliente), "Atendente líder" passa a "Gerente da loja"; os demais já seguem o cabeçalho. Indústria: o lote 140 ganha quem liberou e a data, coerentes com o encerramento em 21/05/2027; as frases "segue aberto" e "2 fora" são corrigidas pela tabela.

### P17

**Estudos que mudam:** Projeto

**Conflito.** Entradas E1 e E2 da pizza vegana "atendem" depois de mudanças de ingrediente e alergênico.

**Decisão.** E1 e E2 recebem nota de reverificação: o "Atende" vale para a receita de 20/04 a 03/05/2027; depois da troca do queijo vegetal (12/05, marca B) e do recheio (18/05, tofu defumado), a ficha técnica, os rótulos e o texto de alergênicos precisam ser conferidos de novo. Revisão final: a nota dizia "de 22/04 a 03/05", mas os rótulos da E1 foram conferidos em 20/04: proj_body.html, "a receita verificada de 22/04 a 03/05" → "de 20/04 a 03/05".

### P18

**Estudos que mudam:** Competencias

**Conflito.** Níveis da Luana e do Felipe diferentes na matriz e no questionário; Camila com lacunas sem ação; Jorge "há sete anos" e "desde 10/2020".

**Decisão.** Vale a matriz de Suprimentos da indústria (12/03/2027): Luana nível 2 em S1, Felipe nível 2 em S7; as perguntas do questionário sobre os dois passam a ter resposta 2, com o enunciado coerente. Camila tem sete lacunas, e o plano ganha ações para S6 e S7, as duas que hoje não têm. Jorge, desde 10/2020: "há sete anos" passa a "há seis anos". (Pessoas da indústria, embora o item seja da série P.) Corrigido pela N32: na matriz, Felipe tem nível 0 em S7, e não 2; a pergunta sobre ele passa a ter resposta 0.

### P19

**Estudos que mudam:** Satisfacao, Conhecimento

**Conflito.** Meta de reclamações 2,0 e 1,5; "prazo de resposta" com dois sentidos; contingência escrita em 13/04 e incorporada em 20/04.

**Decisão.** Vale Objetivos: a meta de reclamações é até 2,0 por 100 pedidos em 2026 (Indicadores) e 1,5 em 2027 (O2). Em Satisfação, a meta da tabela e do texto passa de 2,0 a 1,5. "Primeira resposta" (o primeiro contato com o cliente) e "solução" (o caso resolvido) são termos distintos, usados assim em Satisfação e na política de pós-entrega de Conhecimento. A contingência CT-02 foi escrita em 13/04/2027 e incorporada em 20/04/2027, e o texto diz as duas datas.

### P20

**Estudos que mudam:** Calibracao

**Conflito.** Termômetro novo da câmara fora da lista de instrumentos.

**Decisão.** O termômetro novo é o TER-05, termômetro de visor da câmara fria, 0 a 5 °C, verificação interna a cada 3 meses (±1 °C), verificado contra o TER-01 e instalado em 15/03/2027, próxima em 15/06/2027, em dia em 31/03/2027. A lista passa de 6 para 7 instrumentos (em dia: de 2 para 3), e a tabela de verificações ganha a de 15/03/2027 do TER-05, aprovada.

### P21

**Estudos que mudam:** GUT, Indicadores

**Conflito.** Desperdício e erros com valores diferentes; reunião "toda segunda" numa terça; "três melhoraram" com um estável.

**Decisão.** Vale Indicadores (setembro de 2026). Na GUT de 29/09/2026: P4 passa a "Erros de sabor ou de tamanho em 2% dos pedidos" (pedidos refeitos: 2,0%) e P5 a "Desperdício de insumos em 3,9% do custo comprado"; as notas G, U e T não mudam. Em Indicadores, a leitura continua em 06/10/2026, uma terça, e a reunião passa a "Toda terça-feira, com fechamento mensal". O "O que observar" passa a dizer que dois indicadores melhoraram (entregas e reclamações), o desperdício ficou estável na meta e os pedidos refeitos sobem.

### P22

**Estudos que mudam:** PDCA, Ishikawa, GUT, 5W2H, Caso-Integrado

**Conflito.** 96% e 68% de entregas no prazo não fecham com a folha do Pareto; 8 hipóteses e 3 causas no PDCA, 12 e 5 no Ishikawa; três ações contra seis; ordem entre Pareto e Ishikawa; problema ausente da lista da GUT; causa raiz sem ação.

**Decisão.** Valem Pareto, Ishikawa e 5W2H. Hipóteses: 12, com 5 confirmadas (A1, B1, C1, D1, E1), 4 descartadas e 3 não verificadas; 4 causas seguem para o plano (a fila do forno, C1, fica para o ciclo seguinte). Plano: 6 ações, A1 a A6. No Ishikawa, a evidência do E1 passa a "No prazo: 91% fora do pico e 68% no pico", tirada da folha do Pareto (sextas e sábados: 140 atrasos em 444 entregas; demais dias: 60 em 666). Ordem: Pareto (10/07/2026) antes do Ishikawa (17/07/2026), e o Ishikawa analisa o efeito "18% das entregas depois de 40 minutos", com a primeira barra do Pareto como dado. A GUT da pizzaria, de 29/09/2026, é posterior ao ciclo dos atrasos, que se fechou em 06/09/2026: onde um estudo diz que a GUT escolheu o problema dos atrasos, o texto passa a dizer que o problema veio do indicador, antes da GUT. A causa raiz do B1 ("os pedidos não são analisados por faixa de horário, e a escala não acompanha o pico") tem ação no 5W2H: a A1 diz que a escala do pico passa a seguir os pedidos por faixa de horário medidos na A5. No PDCA: "Das doze hipóteses levantadas, cinco foram confirmadas" e seis ações. Também no Caso integrado (acrescentado à lista do spec): passo 3, cinco causas confirmadas e quatro para o plano; passo 4, seis ações. Revisão final: no PDCA (treinamento-pdca.html, "O que observar" do exemplo 1), "fora do pico, quase tudo chegava no prazo." → "fora do pico, 91% das entregas chegavam no prazo; no pico, só 68%."; no Ishikawa (ish_data.py, B1), o teste "Comparar entregadores disponíveis e pedidos por hora" → "Comparar os entregadores disponíveis e as entregas por noite", a medida da evidência (74 e 35 entregas por noite: T60).

### P23

**Estudos que mudam:** Pedidos, Recursos, Liberacao, Calibracao, Indicadores, 5W2H

**Conflito.** "Muçarela" e "mussarela"; "fora da meta" com dois sentidos; status e situação trocados.

**Decisão.** Grafia única "muçarela", em todos os estudos. Em Indicadores, "Fora da meta" é só a situação além do limite de atenção; o resultado que não atinge a meta sem passar do limite é "Atenção", e o sentido geral se escreve "sem atingir a meta". No 5W2H, "status" é o que o responsável informa (não iniciada, em andamento, concluída, cancelada) e "situação" é a calculada (no prazo, atrasada, concluída, concluída com atraso), como no módulo.

## Indústria e distribuidora: itens do desenho (I)

19 decisões.

### I01

**Estudos que mudam:** SWOT, Partes-Interessadas, Auditoria

**Conflito.** "Certificada há 8 anos", contra a primeira certificação em 17/12/2027.

**Decisão.** Primeira certificação em 17/12/2027 (ISO 9001:2015, válida até 16/12/2030). Antes disso, sistema implantado, sem certificado. SWOT, exemplo 3: o objeto passa a "Indústria de embalagens plásticas, com sistema de gestão da qualidade implantado, sem certificado", e o S1 a "Sistema de gestão implantado, com auditores internos formados" (16 pontos, sem mudança). Auditoria, exemplo 3: a organização passa a "Indústria de embalagens plásticas, com sistema de gestão implantado, sem certificado". Partes interessadas (20/01/2027), parte 8, Organismo de certificação: "Por que importa" passa a "Fará a auditoria de certificação, que dois grandes clientes passaram a exigir."; relacionamento "Contratação prevista para 2027 e contato do Coordenador da Qualidade."; o requisito passa a "Sistema pronto para a auditoria de certificação, com as não conformidades tratadas no prazo.", tipo Expectativa, situação Atende (as contagens não mudam). A expectativa da direção segue I14.

### I02

**Estudos que mudam:** Recursos

**Conflito.** "Extrusora 4 em operação", contra "as três extrusoras".

**Decisão.** Quatro extrusoras desde setembro de 2026. Recursos (julho de 2027): nas três linhas de operador de extrusão, a demanda passa a "4 extrusoras em operação" e as necessárias a 4; turnos A e B com 4 escaladas e 4 qualificadas (Justo); turno C com 3 escaladas e 3 qualificadas (Falta 1 pessoa). O resumo continua "8 funções e períodos, 2 com falta de gente: 2 pessoas a menos". "Alarme luminoso instalado nas três extrusoras" passa a "nas quatro extrusoras"; "O compressor de ar, de que as três extrusoras dependem" passa a "as quatro extrusoras"; a frase do chiller segue I19. "Pedidos redistribuídos entre as extrusoras 1 e 2" não muda. Além do texto (tarefa 7, registrado na revisão final): a infraestrutura do exemplo 2 de Recursos ganhou a linha EXT-04 (rec_data.py: Extrusora 4, Equipamento, Extrusão, criticidade alta, preventiva a cada 3 meses, última em 21/06/2027, contingência "Pedidos urgentes passam para a extrusora 2.", 744 horas), e com ela o resumo passou de "10 itens, 6 críticos. Preventivas: 7 em dia" a "11 itens, 7 críticos. Preventivas: 8 em dia" (1 vence em 7 dias, 1 atrasada e 1 sem plano não mudam), e a figura 7 ganhou a disponibilidade da EXT-04.

### I03

**Estudos que mudam:** Certificacao

**Conflito.** Nove mudanças de processo até setembro de 2027; "das 9 de 2027", com duas depois de outubro.

**Decisão.** Onze mudanças de processo em 2027: nove até setembro (a população da auditoria 2027-11, de 06/10/2027, com 2 sem autorização) e duas em outubro e novembro, as duas sem autorização, depois da constatação da auditoria interna de outubro. Quatro sem autorização no ano. Em Certificação, a constatação I-3 passa a "Das 11 mudanças de processo de 2027, 4 sem autorização, 2 delas depois da constatação da auditoria interna de outubro: a ação corretiva não funcionou." Técnica de auditoria (população de 9, "9 no ano", lida até setembro) não muda.

### I04

**Estudos que mudam:** Partes-Interessadas, Recursos, Conhecimento, Caso-Integrado

**Conflito.** "Gerente de Produção", contra "Gerente industrial" e "Gerente de engenharia".

**Decisão.** Valem os cargos de Auditoria (programa), Objetivos e Riscos: Gerente industrial, dono da Produção, e Gerente de engenharia, dono do Desenvolvimento de produto. Não existe "Gerente de Produção". Em Partes interessadas: nas partes 6 (Órgão ambiental) e 10 (Comunidade vizinha), "Gerente de Produção" passa a "Gerente industrial"; nas ações dos requisitos, "Levar a compra do medidor de espessura em linha à análise crítica" (18/02/2027) passa a "Gerente industrial", e "Abrir o projeto de resina reciclada, com fornecedor homologado" (30/06/2027) passa a "Gerente de engenharia"; a ação da expectativa da direção segue I14. Acrescentados à lista do spec: "gerente de produção" passa a "gerente industrial" em Recursos (responsável do exemplo 2), em Conhecimento (responsável do exemplo 2) e no Caso integrado (calendário, linha "Mapa do conhecimento").

### I05

**Estudos que mudam:** Objetivos

**Conflito.** Processos "Extrusão", "Engenharia" e "Comercial e Qualidade", que não estão entre os nove.

**Decisão.** Os nove de Processos (e do programa de Auditoria): 1 Comercial e análise de pedidos, 2 Desenvolvimento de produto, 3 Suprimentos, 4 Produção, 5 Laboratório e controle da qualidade, 6 Expedição e logística, 7 Manutenção, 8 Gestão de pessoas, 9 Gestão do sistema da qualidade. Na coluna Processo do quadro da indústria em Objetivos: O1 "Extrusão" passa a "Produção"; O2 "Comercial e Qualidade" passa a "Comercial e análise de pedidos"; O3 "Expedição" passa a "Expedição e logística"; O4 e O6 "Gestão do sistema" passam a "Gestão do sistema da qualidade"; O5 "Engenharia" passa a "Desenvolvimento de produto"; O7 "Suprimentos" não muda. Os responsáveis não mudam.

### I06

**Estudos que mudam:** Conhecimento, Recursos

**Conflito.** Análise crítica "de julho".

**Decisão.** As análises críticas da indústria são semestrais: 12/02/2026, 13/08/2026, 18/02/2027 e 19/08/2027. Em Conhecimento (exemplo 2), a origem passa a "Análise crítica de 19/08/2027: as quebras da extrusora 3 mostraram que o desgaste da rosca só era medido pelo técnico do fabricante." Em Recursos (exemplo 2, julho de 2027), "Análise crítica do semestre" passa a "Preparação da análise crítica de 19/08/2027", com o resto da frase igual: a leitura de julho alimenta a análise de agosto, como no Caso integrado (passos 10 e 11).

### I07

**Estudos que mudam:** Escopo, Analise-Critica, Caso-Integrado, Satisfacao

**Conflito.** Medidor em linha: um ou dois, atraso antes do prazo, decisão antes da reclamação que a justifica.

**Decisão.** Dois medidores de espessura em linha, para as extrusoras 3 e 4, R$ 96.000 com instalação, compra aprovada na análise crítica de 18/02/2027 (decisão 5, diretor geral), com prazo em 30/06/2027; não instalados em 30/06 (Objetivos, 09/07/2027: atrasada); em 19/08/2027, a análise crítica decide concluir a instalação, atrasada desde junho. Escopo (10/05/2027), compromisso 5: "Aprovou os dois medidores de espessura em linha, de R$ 96.000, com instalação até 30/06/2027; em maio, a compra ainda não tinha sido feita." (situação Parcial e ação sem mudança). Análise crítica de 18/02/2027, ação 7 da análise de 13/08/2026: "Instalar o medidor de espessura em linha na extrusora 3." passa a "Orçar os medidores de espessura em linha para as extrusoras 3 e 4 e levar a compra à aprovação.", decidida pelas reclamações de espessura do cliente A do primeiro semestre de 2026 (prazo, status e resultado sem mudança: "Orçamento recebido. Compra não aprovada."; a ação segue atrasada até a decisão 5 de 18/02/2027, que aprova a compra e a fecha). A reclamação de 14/09/2026 e o RNC 2026-32 confirmaram a causa e levaram a proposta à análise de 18/02/2027. Caso integrado: onde citar o medidor, "os dois medidores em linha"; no passo 11 (19/08/2027, caso_data.py), "Decisões: antecipar o medidor em linha e planejar a passagem do conhecimento do operador sênior." passa a "Decisões: concluir a instalação dos dois medidores em linha, atrasada desde junho, e planejar a passagem do conhecimento do operador sênior." Acrescentada na tarefa 7, Satisfação: exemplo 3 (sat_data.py), etapa de 02/10/2026, "até a compra do medidor." → "até a compra dos medidores."; etapa de 18/02/2027, "Análise crítica aprova o medidor de espessura." → "Análise crítica aprova os dois medidores de espessura em linha."; "O que observar" do exemplo 2 (sat_body.html), "justificou o medidor de espessura" → "justificou os medidores de espessura em linha". Revisão final (decisões do controlador, à espera da revisão do autor): a versão aprovada dava a ação 7 como "Orçar os medidores de espessura em linha para as extrusoras 3 e 4.", que, com o resultado "Orçamento recebido", ficava atrasada já feita: ela ganha "e levar a compra à aprovação". A versão aprovada dizia "passo 11 sem mudança" e "antecipação decidida em 19/08/2027"; com o prazo de 30/06/2027 vencido, "antecipar" (a palavra do desenho) não se lê, e o passo 11 passa a "concluir a instalação…, atrasada desde junho".

### I08

**Estudos que mudam:** GUT, Pareto, Ishikawa, 5W2H, PDCA

**Conflito.** Compras com duas histórias: formulário novo e devoluções de 40% para 12% em 2026, contra indicador em 30% até setembro e RNC 2026-31.

**Decisão.** A cadeia datada é da indústria (Suprimentos): auditoria 2026-07 (22/09/2026), RNC 2026-31 (22/09/2026, encerrado em 05/02/2027), indicadores C1 a C4 (C2 em 30% até setembro de 2026), riscos (12/10/2026), tartaruga (20/10/2026), RACI e SIPOC de "Adquirir materiais e serviços", ISO 9001 requisito a requisito, Informação documentada, Competências e Fornecedores. A cadeia das ferramentas (prazo de compra de 12 para 8 dias úteis, devoluções de 40% para 12%, formulário com campos obrigatórios, piloto na Manutenção e na Produção) é da "Distribuidora de materiais elétricos · Compras", com esse nome exato, no exemplo 2 de GUT, Pareto, Ishikawa, 5W2H e PDCA: no Pareto, o campo Organização passa de "Indústria de embalagens plásticas · Suprimentos" a esse nome; nos outros quatro, o cabeçalho do exemplo 2 ganha a linha Organização com esse nome. Cargos, áreas requisitantes, datas e números ficam como estão (ver ORGS["distribuidora"]); a cronologia segue N09, e a SWOT de origem, N08. Nas listas dos exemplos da planilha, "de Suprimentos" passa a "da distribuidora" (GUT, Ishikawa e 5W2H: "As matrizes/análises/planos da pizzaria e da distribuidora"; PDCA: "Os ciclos da pizzaria e da distribuidora"). O exemplo 3 desses estudos, dos instrumentos vencidos ("3 de 25"), continua da indústria (I19). Nas planilhas de GUT, Ishikawa, 5W2H e PDCA (tarefa 8, registrado na revisão final), o nome da distribuidora entrou no campo "Área / unidade" do cabeçalho do exemplo 2 (campo area de gut_data.py, ish_data.py, w5_data.py e do exemplo 2 de build_pdca.py), no lugar de "Suprimentos"; as planilhas não têm campo Organização.

### I09

**Estudos que mudam:** Producao, Calibracao, Liberacao, Caso-Integrado

**Conflito.** Lote piloto da resina nova, contra "o lote 135 foi o primeiro"; resposta "dentro do critério", contra 37,9 µm medidos.

**Decisão.** O lote piloto da resina do F-13 é o lote 127, de 05/05/2027, com duas bobinas: espessura e solda ensaiadas, dentro do critério. O lote 135, de 14/05/2027, é o primeiro da produção regular com a resina nova. Produção: na tabela de mudanças, a análise passa a "Lote piloto 127, de 05/05/2027, com duas bobinas: espessura e solda ensaiadas."; no "O que observar", "a primeira bobina com a resina do segundo fornecedor" passa a "a primeira bobina da produção regular com a resina do segundo fornecedor". Calibração (exemplo 3) conta em ordem: em 24/05, o cliente A reclama do lote 135 e a primeira resposta cita a medição da liberação, 39,1 µm, dentro do critério; em 26/05, a bobina devolvida é medida no laboratório, com o MIC-08: trechos com 37,9 µm; em 12/06, a verificação do MIC-07 mostra +1,6 µm, e a bobina corrigida tem 37,5 µm. Acrescentados à lista do spec: Liberação (2027-19: "na primeira bobina da produção regular com a resina do segundo fornecedor"; 2027-22: "Primeira resposta, em 24/05: 39,1 µm na liberação. Medida no laboratório em 26/05, com o MIC-08: trechos com 37,9 µm.") e Caso integrado (passo 5: "Mudança registrada: resina do segundo fornecedor na extrusora 3, depois do lote piloto 127, de duas bobinas; o lote 135 é o primeiro da produção regular."; coluna "O que seguiu": "O lote 135, para liberar").

### I10

**Estudos que mudam:** Projeto

**Conflito.** Laudo de migração antes do lote de teste; ensaio com a resina B sem lote da resina B.

**Decisão.** Projeto D-07: a mudança de resina (fornecedor B no lugar do A, pelo prazo de entrega) passa de 20/07 para 08/07/2027, antes do lote de teste de 15/07, que já sai com a resina B. O laudo de migração (E4) passa de "Laudo de 12/07." para "Laudo de 18/07.", feito sobre o filme do lote de teste, antes da validação no cliente, que começa em 19/07. Na mudança de 08/07, "O que foi verificado de novo" passa de "Queda de dardo repetida com a resina B: 410 g, conforme." para "Queda de dardo no lote de teste, com a resina B: 420 g, em 16/07, conforme." No "O que observar", "com o ensaio repetido" passa a "com o laudo e o ensaio no lote de teste". As outras datas não mudam.

### I11

**Estudos que mudam:** Caso-Integrado, Satisfacao

**Conflito.** RNC 2026-29 em 23/09, depois do 2026-31 em 22/09.

**Decisão.** Na série RNC da indústria, o número segue a data de abertura. O RNC 2026-31, de 22/09/2026, citado em sete estudos, não muda. O RNC de 23/09/2026 (espessura na extrusora 3, reclamação do cliente A) passa de 2026-29 a 2026-32. Acrescentada à lista do spec: Satisfação (exemplo 3, linha de 23/09/2026).

### I12

**Estudos que mudam:** Informacao-Documentada

**Conflito.** ISO 9001:2015 "verificada" como vigente em 2027; figura 8 com números de Suprimentos diferentes do exemplo; retenção e intervalo fora da regra.

**Decisão.** Exemplo 3 (documentos externos, 05/03/2027): a linha da ISO 9001:2015 fica, com "Versão em uso" "Emenda 1, de 2024; em uso até a transição", e entra a linha "ISO 9001:2026 · ISO e ABNT · Edição de 2026, comprada em 10/02/2027 · Todo o sistema, para a transição · Consulta ao site da ABNT a cada seis meses · 10/02/2027 · 08/2027 · Verificado" (a compra é a etapa 1 do plano de transição da indústria). Figura 8: Suprimentos passa a 10 documentos, 7 em dia, 2 com revisão vencida (IT-REC-01 e FR-13) e 1 sem controle (o cadastro de itens), 70%, como o exemplo 2; os totais da figura são refeitos. Exemplo 2, regra: "Documentos revistos a cada 24 meses. Formulários e listas, a cada 12; a lista de fornecedores homologados, a cada 6, com a avaliação semestral. Registros retidos por 3 anos; os de compra, por 5, pelo prazo fiscal; os contratos, por 10."

### I13

**Estudos que mudam:** ISO-9001-2026

**Conflito.** "Cinco etapas", contra oito; "O4" é oportunidade e objetivo; prazos de M5 e M6 depois do limite.

**Decisão.** A transição tem oito etapas, as do plano do exemplo 2: comprar e ler a norma; diagnóstico das mudanças; plano aprovado pela direção; ações concluídas; conscientização da equipe; auditoria interna pela edição de 2026; análise crítica com a transição; auditoria do organismo. O módulo 3 e a figura 3 passam de "cinco etapas" a "oito etapas". A oportunidade deixa de ser chamada pelo código: na M4, "Riscos C1 a C8 e quatro oportunidades em listas separadas, desde 2026"; no exemplo 3, "A oportunidade dos clientes que exigem a ISO 9001 virou o objetivo O4"; "O4" fica só para o objetivo. A figura 7, cópia da matriz de Riscos, mantém os códigos. Os prazos do M5 (31/08/2028) e do M6 (30/09/2028) não mudam; o "O que observar" do exemplo 2 diz que o M6 vence depois do limite da etapa 4, ações concluídas (23/09/2028), e que o M5 fica a três semanas dele. Revisão final: o módulo 3 dizia "oito etapas, as mesmas do plano dos exemplos" antes de um passo a passo com outras oito; passa a "A transição tem oito etapas, as do plano dos exemplos, mostradas na figura 3. O passo a passo abaixo diz como percorrê-las; as duas primeiras cabem em poucas semanas." (ed26_body.html).

### I14

**Estudos que mudam:** Partes-Interessadas

**Conflito.** Refugo de 2,6% "atende em parte" com meta abaixo de 3%; contagens de quadrantes e de pendências.

**Decisão.** Texto refeito pela tabela de Partes interessadas (20/01/2027). Expectativa da direção: "Refugo abaixo de 3% e certificação ISO 9001 obtida."; como atende: "Refugo de 2,6% em 2026, com o ciclo PDCA. A certificação ainda é um projeto."; situação Atende em parte (pela certificação); ação "Contratar a auditoria de certificação", Diretor geral, 30/04/2027. As contagens não mudam: 16 requisitos, 15 adotados, 10 atendem, 4 em parte e 1 não atende, 80%. Quadrantes: gerir de perto 4, manter satisfeito 4, manter informado 2, monitorar 2. O "O que observar" passa a "O quadrante de manter satisfeito tem tantas partes quanto o de gerir de perto, quatro: dois órgãos reguladores, o fornecedor único de resina e o organismo de certificação." e, sobre as pendências, "Das cinco pendências, três estão nos clientes: a espessura do filme, que levou o medidor em linha à análise crítica, a entrega na data e a resina reciclada, uma expectativa de sustentabilidade que a fábrica adotou e ainda não atende. As outras duas são a certificação, esperada pela direção, e a matriz de competências fora de Suprimentos."

### I15

**Estudos que mudam:** Objetivos

**Conflito.** "Dois antes do prazo" com três; definição em 19/02 com ações anteriores; meta de 96 com base de 97, que o próprio estudo chama de erro.

**Decisão.** Pizzaria (exemplo 1): "Em maio, quatro estão alcançados, e dois deles antes do prazo: a nota da pesquisa e os pedidos refeitos." passa a "Em maio, quatro estão alcançados, e três deles antes do prazo: as reclamações, a nota da pesquisa e os pedidos refeitos." Os objetivos são definidos em 19/02/2027, e as ações do O3 (27/01) e do O7 (20/01), concluídas antes, vêm da análise crítica de 14/12/2026: o "O que observar" acrescenta "As ações do O3 e do O7 foram decididas na análise crítica de dezembro e entraram no quadro já concluídas." Indústria (exemplo 2): o O3 passa a "Manter 97% das entregas na data confirmada.", meta 97 (base 97); o acompanhamento fica 97, 96, 97, 97, 98, 97, e fevereiro (96) passa a não atender à meta; último 97, Alcançado, caminho 100%. No módulo, o exemplo de objetivo de manter passa a "Manter 97% das entregas na data confirmada."

### I16

**Estudos que mudam:** Processos, Analise-Critica

**Conflito.** G1 com indicador e "não" no elemento; tartaruga e interações de Suprimentos diferentes.

**Decisão.** Pizzaria: o G1 tem o indicador "Objetivos alcançados no ano", e o elemento c (critérios e indicadores) passa de "Não" para "Parcial"; o elemento g (avaliação) não muda, "Não" (corrigido por N27; a primeira versão mudava o g): G1 com 5,0 pontos e 63% (62,5%: o gerador do treinamento arredonda para cima, como a planilha; a ficha dizia 62%, conferido na tarefa 5); a média dos nove processos passa de 63% a 64%. Indústria: a tartaruga (20/10/2026) e a matriz de interações ficam iguais. Na tartaruga, "O que entra" ganha "Resultado da inspeção de recebimento · Laboratório e controle da qualidade" e "Resultados de auditoria e ações · Gestão do sistema da qualidade", e a origem da requisição passa a "Produção e Manutenção". Nas interações do processo 3, "Recebe de 4 · Produção" passa a "Requisição de compra, com especificação, e plano de produção do mês". As saídas já batem. Revisão final: a Análise crítica de 14/12/2026 cita a média do mapa de 14/10/2026 (entrada c3, ac_data.py): "63% dos elementos dos processos estão definidos." → "64% dos elementos dos processos estão definidos." (46,0 de 72 pontos, 63,9%).

### I17

**Estudos que mudam:** SWOT, Objetivos

**Conflito.** "Sete seguem para o cruzamento", com estratégias de fatores médios e ameaça alta sem estratégia.

**Decisão.** Pizzaria (SWOT, exemplo 1). Só os sete fatores de prioridade alta entram no cruzamento: S1, S2, W1, W2, O1, O4 e T1. As seis estratégias passam a: S×O "S1 receita elogiada × O1 novos condomínios": "Fazer uma ação de boas-vindas nos novos condomínios, com degustação." (sem mudança); S×O "S2 entrega própria no prazo × O4 pedido por aplicativo de mensagens": "Lançar o pedido por mensagem, com a entrega própria no prazo como argumento."; W×O "W2 × O4" e "W1 × O1" sem mudança; S×T "S2 entrega própria no prazo × T1 aumento da taxa do aplicativo": "Divulgar a entrega própria no prazo para levar os clientes do aplicativo ao canal próprio."; W×T "W2 dependência do aplicativo × T1 aumento da taxa": "Negociar a taxa com o aplicativo e definir preços por canal, para que o aumento não consuma a margem." A ficha técnica e o custo por pizza (W3 × T3) saem do cruzamento. Acrescentado à lista do spec: em Objetivos, a origem do O6 passa de "Estratégia (SWOT)" a "Análise crítica".

### I18

**Estudos que mudam:** Analise-Critica, Objetivos, Satisfacao

**Conflito.** Visita ao cliente A decidida depois de feita.

**Decisão.** A primeira visita ao cliente A foi em 02/10/2026 (Satisfação). Na análise crítica de 18/02/2027, a decisão 3 passa a "Fazer a segunda visita ao cliente A e rever o plano conjunto de outubro de 2026.", Gerente comercial, 19/03/2027. Acrescentado à lista do spec: em Objetivos, a ação do O2 passa a "Fazer a segunda visita ao cliente A e rever o plano conjunto.", concluída em 12/03/2027. Acrescentada na tarefa 7: Satisfação, "O que observar" do exemplo 2, "Foi esse cliente que a análise crítica decidiu visitar" passa a "Foi esse cliente que a análise crítica de fevereiro de 2027 decidiu visitar de novo".

### I19

**Estudos que mudam:** GUT, Ishikawa, 5W2H, PDCA, Recursos

**Conflito.** Instrumentos vencidos: meta em 60 dias e eficácia em 90; "três quebras" na figura e "duas" no texto; chiller "parou todas" com uma extrusora a 100%.

**Decisão.** Instrumentos vencidos (exemplo 3 de GUT, Ishikawa, 5W2H e PDCA, da indústria): auditoria interna de agosto de 2026, 3 de 25 instrumentos no laboratório de recebimento. Prazo de tratamento da GUT: 30 dias (sem mudança). Os 90 dias contam do fim da ação A3 do 5W2H, o cadastro único com aviso de vencimento, e a verificação da eficácia (A6) começa no 90º dia. Para isso, só o prazo da A3 muda: no 5W2H, exemplo 3, coluna Quando da A3 ("Centralizar o controle dos 25 instrumentos em um cadastro único"), "07/09 a 25/09" passa a "07/09 a 15/09" (w5_data.py, EX3, terceiro item: D(2026, 9, 25) passa a D(2026, 9, 15)). De 15/09/2026, 90 dias dão 14/12/2026: a A6 continua "14/12 a 18/12", e o texto "nenhum instrumento vencido depois de 90 dias" e o "O que observar" ("data marcada para 90 dias depois") continuam certos. A A5 (28/09 a 09/10) e as outras ações não mudam. No PDCA, a meta passa de "Nenhum instrumento vencido, em 60 dias" a "Nenhum instrumento vencido, por 90 dias seguidos" (PDCA acrescentado à lista do spec; a etapa 6, "Depois de 3 meses", já está certa). No módulo 5 do PDCA (tabela de metas, escrita à mão; revisão da tarefa 8, registrado na revisão final), a meta completa de "Implantar o controle de instrumentos até março" passa de "Zerar os instrumentos com calibração vencida, em 60 dias" a "Zerar os instrumentos com calibração vencida e manter o zero por 90 dias seguidos, até 18/12/2026", o fim da A6. Nos quatro estudos, o cabeçalho do exemplo 3 ganha a linha Organização: "Indústria de embalagens plásticas". Recursos: na figura 4, "As três quebras de julho vieram de peças que a preventiva atrasada teria trocado ou medido." passa a "Duas das três quebras de julho vieram de peças que a preventiva atrasada teria trocado ou medido." (o texto já diz duas: a de 27/07, cabo do termopar, não dependia da preventiva). "o chiller, com uma quebra só, parou as três extrusoras ao mesmo tempo" passa a "o chiller, com uma quebra só, fez as quatro extrusoras trabalharem em velocidade reduzida por 8 horas", como diz a contingência do CHI-01.

## Contradições novas, achadas na montagem da ficha (N)

36 decisões.

### N01

**Estudos que mudam:** nenhum estudo muda

**Conflito.** A revisão 2 da IT-EXP-01 em 31/07/2026, como o spec propunha para P09, não fecha com a ação A6 do 5W2H ("Atualizar a instrução de trabalho da expedição", 07/09 a 15/09/2026), com o acompanhamento de 05/08 (a A6 ainda por começar; a legenda da figura 4 diz que só a A4 está atrasada) e com o PDCA (agrupamento só na semana 8, a partir de 03/08/2026; instrução atualizada na etapa 7, em 15/09/2026).

**Decisão.** Vale o 5W2H, com o PDCA: a revisão 2 é de 15/09/2026 (P09), e os estudos que mudam por isso são os de P09, Informação documentada e Não conformidade. A datação da A6 no 5W2H fica: "07/09 a 15/09" na tabela do exemplo 1 e, no acompanhamento de 05/08 (tabela e figura 4), início 07/09 e prazo 15/09; a legenda da figura 4 continua "A ação A4 deveria ter terminado no dia 2 e aparece como atrasada"; o PDCA não muda por esta entrada. O acompanhamento de 05/08 mostra a situação calculada, e não o status (P23): a A5 e a A6 aparecem "No prazo" (w5_data.py, ref_status). O w5_data.py mudou por outros itens: o exemplo 3, pela I19 (A3 até 15/09); a A1 do exemplo 1, pela P22 (escala do pico ligada à A5).

### N02

**Estudos que mudam:** Auditoria

**Conflito.** Em Auditoria (tabela de como escrever a constatação), "A instrução IT-05 pede o registro da temperatura a cada turno", com as datas da constatação 2 da auditoria 2026-03 da pizzaria. A rotina de temperatura é a IT-PRO-01, e "IT-05" é outro documento em Conhecimento.

**Decisão.** A frase passa a "A rotina IT-PRO-01 pede o registro da temperatura em cada turno." (uma leitura em cada turno, duas por dia: corrigido por N36; a versão aprovada dizia "duas vezes por turno").

### N04

**Estudos que mudam:** Partes-Interessadas

**Conflito.** Recursos: loja aberta das 18h à meia-noite (180 horas no mês, base das contas de disponibilidade). Partes interessadas: "O alvará permite funcionar até 23h30".

**Decisão.** Vale Recursos, que tem contas conferidas. Em Partes interessadas, a frase passa a "O alvará permite funcionar até a meia-noite".

### N05

**Estudos que mudam:** Analise-Critica

**Conflito.** Análise crítica de 14/12/2026: "Dois registros no ano, os dois da auditoria 2026-03", mas o primeiro deles é o RNC 2026-05; e "Uma auditoria no ano", mas ela é a 2026-03. Certificação fala em "auditorias de 2026".

**Decisão.** Valem os números de registro e de auditoria (quatro estudos citam o RNC 2026-05). Na análise crítica, a entrada c4 passa a "Dois registros abertos pela auditoria 2026-03. O RNC 2026-05 foi encerrado como eficaz. O segundo está em verificação." e a c6 passa a "A auditoria 2026-03, no delivery: duas não conformidades menores e uma oportunidade de melhoria. O salão e as compras nunca foram auditados." SUPERADO para c4 e c6 por N23 (tarefa 3, depois de T05): a auditoria 2026-03 teve três não conformidades menores. Vale o texto de N23, já aplicado em ac_data.py; não aplicar as frases acima.

### N06

**Estudos que mudam:** nenhum estudo muda

**Conflito.** Volume de pedidos: Liberação conta de 118 a 236 pedidos por noite (15 a 21/03/2027, cerca de 4.800 por mês) e numera os pedidos acima de 5.100; Satisfação conta 840 a 910 pedidos por mês (fevereiro a abril de 2027) e numera o pedido de 13/03/2027 como 3.104; o Pareto tem uma noite de sábado com 148 entregas num período de 1.110 entregas em 25 dias.

**Decisão.** Não aplicar nesta leva, como os itens da seção 6.3 do spec: acertar o volume exige refazer contas conferidas em Satisfação, Objetivos, Pareto ou Recursos, e o spec não prevê. Fica registrado para a revisão do autor.

### N07

**Estudos que mudam:** Producao, Objetivos

**Conflito.** Os dois entregadores extras nas sextas e nos sábados existem desde julho de 2026 (A1 do 5W2H; auditoria de setembro de 2026), mas Produção e Objetivos dão "Dois entregadores extras nas sextas e nos sábados" como a mudança de 26/03/2027.

**Decisão.** Em 26/03/2027, a escala do pico ganhou mais dois entregadores extras, além dos dois de 2026. Em Produção (tabela de mudanças) e em Objetivos (recursos da ação do O1), a frase passa a "Mais dois entregadores extras nas sextas e nos sábados". Recursos ("mesmo com os extras de março") não muda. Revisão final: a planilha de Objetivos (build_obj.py, exemplo 1, recursos da ação do O1) dizia "Dois entregadores extras nas sextas e nos sábados" → "Mais dois entregadores extras nas sextas e nos sábados"; o módulo (obj_body.html, linha Ação), "com dois entregadores extras" → "com mais dois entregadores extras".

### N08

**Estudos que mudam:** SWOT

**Conflito.** A GUT da distribuidora tira a lista da "Matriz SWOT da área", e os itens P1, P2 e P7 são os fatores W3, W1 e W4 da SWOT, exemplo 2, mas a SWOT diz "Área de Suprimentos de uma indústria", é datada de 29/09/2026 (depois da GUT, ver N09) e tem W2 "Processo manual, em planilhas e e-mails", contra o sistema de compras dos outros quatro estudos.

**Decisão.** A SWOT, exemplo 2, é da distribuidora: o objeto passa a "Distribuidora de materiais elétricos · Compras"; a data, a 22/05/2026; o W2, a "Cotações e aprovações por e-mail, fora do sistema de compras" (16 pontos, sem mudança). Título, responsável, notas e estratégias não mudam. Na lista dos exemplos da planilha, "As matrizes da pizzaria e de Suprimentos" passa a "da pizzaria e da distribuidora".

### N09

**Estudos que mudam:** GUT, PDCA

**Conflito.** Cronologia da distribuidora: o Ishikawa (26/06/2026) e o 5W2H (03/07/2026) citam a "Matriz GUT da área", mas a GUT é de 29/09/2026, com 40% de devoluções e 12 dias de prazo, depois do ciclo que os reduziu (verificação em 28/08/2026), e decide "abrir um ciclo PDCA" já aberto em 01/06/2026. A etapa 5 do PDCA tem data de 31/07/2026, e o piloto do 5W2H vai até 07/08/2026.

**Decisão.** Vale a sequência do PDCA: GUT, exemplo 2, datada de 29/05/2026, antes do ciclo; prazos das decisões: P6 09/06/2026, P1 18/08/2026, P3 30/06/2026 e P4 16/06/2026 (era 09/10, 18/12, 30/10 e 16/10/2026). No PDCA, exemplo 2, a data da etapa 5 passa de 31/07/2026 a 07/08/2026, o fim do piloto. Os valores da matriz não mudam.

### N10

**Estudos que mudam:** Caso-Integrado

**Conflito.** Caso integrado chama de "RNC 2027-19" e "RNC 2027-22" dois registros de produto não conforme da Liberação (série PNC, como em P10).

**Decisão.** Nos passos 6 e 7 do fio da indústria, "RNC 2027-19" passa a "Registro de produto não conforme 2027-19" e "RNC 2027-22" a "Registro de produto não conforme 2027-22". Os números não mudam.

### N11

**Estudos que mudam:** SWOT

**Conflito.** SWOT, exemplo 3: responsável "Diretor industrial"; nos outros estudos, a indústria tem diretor geral e gerente industrial.

**Decisão.** O responsável da SWOT da indústria passa a "Diretor geral".

### N12

**Estudos que mudam:** Partes-Interessadas

**Conflito.** Partes interessadas, parte 3 (Direção e acionistas): "Análise crítica anual"; a análise crítica da indústria é semestral (I06).

**Decisão.** O relacionamento passa a "Análise crítica a cada semestre e reunião mensal de resultados."

### N13

**Estudos que mudam:** Partes-Interessadas, ISO-9001

**Conflito.** Partes interessadas, parte 7: "Três itens críticos têm fornecedor único"; ISO 9001 requisito a requisito: "os itens de fornecedor único". Riscos (C1), Fornecedores, Análise crítica e Caso integrado: um só fornecedor, o da resina de polietileno (F-01).

**Decisão.** O item crítico de fornecedor único é a resina de polietileno, até a homologação do F-13 em 29/03/2027. Partes interessadas, parte 7: "A resina de polietileno tem fornecedor único." ISO 9001 requisito a requisito (6.1, O que falta): "Definir ação para a resina, de fornecedor único."

### N14

**Estudos que mudam:** Objetivos

**Conflito.** Objetivos: a ação do O5 "Homologar o fornecedor de resina reciclada", com os ensaios externos de R$ 12.000, prazo 31/03/2027 e conclusão em 29/03/2027, é a decisão 9 da análise crítica (homologar o segundo fornecedor de resina, F-13, pelo risco C1), que o Caso integrado diz homologado "por outro motivo".

**Decisão.** O F-13, Resinas Atlântico, é o segundo fornecedor de resina de polietileno (risco C1) e oferece também a resina reciclada de menor custo (oportunidade O3 de Riscos). Em Objetivos, a ação passa a "Homologar o segundo fornecedor de resina, que oferece a resina reciclada."; recursos, responsável, prazo e conclusão não mudam.

### N15

**Estudos que mudam:** nenhum estudo muda

**Conflito.** Não conformidade e Processos (setembro e outubro de 2026): quatro compradores; Competências (12/03/2027): quatro compradores, um deles admitido em janeiro de 2027.

**Decisão.** Um comprador saiu no fim de 2026, e Camila foi admitida em janeiro de 2027 no lugar dele: são quatro compradores nos dois momentos. Nenhum estudo muda.

### N16

**Estudos que mudam:** Conhecimento

**Conflito.** Conhecimento, lição I-02: "Procedimento de compras PC-02"; o procedimento de compras da indústria é o PR-SUP-01, em seis estudos.

**Decisão.** Onde incorporar a lição I-02 passa a "Procedimento PR-SUP-01".

### N17

**Estudos que mudam:** nenhum estudo muda

**Conflito.** Códigos de documentos da indústria fora do padrão que Informação documentada ensina (tipo-processo-número, como PR-SUP-01): PQ-08, PE-11, PE-14, PG-05, PM-01, FM-02 e IE-12.

**Decisão.** Não aplicar nesta leva: padronizar exige trocar códigos em Conhecimento, Caso integrado, Técnica de auditoria e Projeto, e o spec não prevê. Os códigos ficam registrados como estão. Fica para a revisão do autor.

### N18

**Estudos que mudam:** Nao-Conformidade

**Conflito.** Não conformidade, exemplo 3 (injeção de tampas, desenho D-118, lotes 2607 e 2655): a organização é "Indústria de embalagens plásticas", que só faz filmes (Escopo, Certificação).

**Decisão.** O exemplo é de outra organização, que não volta na série: o campo Organização passa a "Fábrica de tampas plásticas por injeção".

### N19

**Estudos que mudam:** Calibracao

**Conflito.** Calibração (30/06/2027): "Instrumentos · 7 cadastrados"; auditoria de 2026, 5W2H e Técnica de auditoria: 25 instrumentos em uso.

**Decisão.** O exemplo mostra 7 dos 25 instrumentos, os da extrusora 3 e do laboratório. O título da tabela passa a "Instrumentos da extrusora 3 e do laboratório · 7 dos 25 cadastrados", com o resto das contagens igual.

### N20

**Estudos que mudam:** Certificacao

**Conflito.** Certificação, escopo do certificado: "Desenvolvimento e produção de filmes técnicos lisos e impressos para embalagem de alimentos"; Escopo (10/05/2027): "Projeto, fabricação e expedição de filmes plásticos técnicos, lisos e impressos, para embalagem de alimentos."

**Decisão.** Vale a declaração do Escopo, que o certificado repete: o campo Escopo de Certificação passa a "Projeto, fabricação e expedição de filmes plásticos técnicos, lisos e impressos, para embalagem de alimentos."

### N21

**Estudos que mudam:** nenhum estudo muda

**Conflito.** A declaração de escopo restringe a indústria a "embalagem de alimentos", e o Escopo diz que ela "não exclui nada que a fábrica faça", mas Satisfação e Partes interessadas têm clientes de cosméticos (18) e industriais (16).

**Decisão.** Não aplicar nesta leva: acertar exige reescrever as declarações e a figura do Escopo, o escopo de Certificação e conferir Partes interessadas e Satisfação, e o spec não prevê. Fica para a revisão do autor.

### N22

**Estudos que mudam:** Auditoria, Tecnica-Auditoria, Certificacao, Nao-Conformidade, Indicadores

**Conflito.** A pizzaria abre das 18h à meia-noite (Recursos, base das contas de disponibilidade, 180 horas no mês), mas quatro estudos citam um "turno do almoço": a equipe auditora de Auditoria ("Atendente e pizzaiolo do turno do almoço"), os auditores de Técnica de auditoria, o responsável do critério 7 de Certificação e o auditor líder do RNC 2026-05 na planilha de Não conformidade. Indicadores diz que "O turno do almoço entrega 96% no prazo", como se a loja entregasse no almoço.

**Decisão.** Vale o horário de Recursos (contas conferidas). A loja tem dois turnos: o da tarde, antes da abertura, sem atendimento a clientes (é nele que a loja recebe os insumos, às 15h, como em Técnica de auditoria), e o da noite, das 18h à meia-noite. "Turno do almoço" passa a "turno da tarde" em todos os lugares: Auditoria, exemplo 1, equipe auditora: "Atendente e pizzaiolo do turno da tarde" (aud_body.html e aud_data.py, lider e equipe); Técnica de auditoria, exemplo 1: auditor líder "Atendente do turno da tarde", equipe "Pizzaiolo do turno da tarde", e as duas colunas da tabela de avaliação dos auditores com os mesmos nomes (tec_data.py, cabeçalho e avaliação); Certificação, critério 7 da prontidão da pizzaria: responsável "Atendente do turno da tarde" (cert_data.py); Não conformidade, RNC 2026-05: "Atendente do turno da tarde, auditor líder" (nc_data.py). Indicadores, módulo da meta, linha "Uma referência": "O turno do almoço entrega 96% no prazo." passa a "As pizzarias da região entregam 96% no prazo, pelo relatório do aplicativo de delivery." (ind_body.html); o número 96 não entra em nenhuma conta e fica. Os "atendentes da noite", o "garçom do turno da noite" e o "cansaço do turno da noite" não mudam.

### N23

**Estudos que mudam:** Analise-Critica, Competencias

**Conflito.** Achado na tarefa 3 (núcleo de auditoria). Pelo item T05 do spec, a constatação 3 da auditoria 2026-03 (entregador admitido em setembro sem o treinamento na IT-EXP-01) passa de oportunidade de melhoria a não conformidade menor nº 3. Dois estudos ainda contam o resultado antigo: a análise crítica de 14/12/2026 (c4: dois registros; c6: "duas não conformidades menores e uma oportunidade de melhoria", texto que N05 mantinha) e Competências ("A integração, que a auditoria sugeriu").

**Decisão.** Vale T05 (spec, aprovado). A auditoria 2026-03 teve três não conformidades menores e nenhuma oportunidade de melhoria. Na análise crítica (ac_data.py), as frases de N05 passam a: c4 "Três registros abertos pela auditoria 2026-03. O RNC 2026-05 foi encerrado como eficaz. Os outros dois estão em verificação." (o segundo é o da temperatura, que c5 dá como registrada em todos os turnos desde outubro; o terceiro é o do treinamento, cuja eficácia saiu parcial em Competências); c6 "A auditoria 2026-03, no delivery: três não conformidades menores. O salão e as compras nunca foram auditados." Esta entrada substitui o texto de c4 e c6 dado em N05, e foi aplicada na tarefa 3. Em Competências (comp_body.html, exemplo 1, "O que observar"), "A integração, que a auditoria sugeriu, passa a ser" passa a "A integração, ação corretiva da não conformidade da auditoria, passa a ser". Nenhuma conta muda: a avaliação de c4 (Favorável) e a de c6 (Atenção) ficam.

### N24

**Estudos que mudam:** Tecnica-Auditoria, Certificacao

**Conflito.** Achado na revisão da tarefa 3. Técnica de auditoria passou a chamar de "Desvio pontual" a amostra com um desvio e de "Desvio repetido" a com dois ou mais; Certificação definia a NC maior como a que "mostra uma falha que se repete" ou "desvio que se repete", e a menor como "desvio pontual"; e Auditoria classifica 3 de 28 turnos sem registro como NC menor. Juntos, levavam a ler "repetido na amostra ⇒ maior".

**Decisão.** O grau da não conformidade segue o critério da tabela "Tipos de constatação" de Auditoria interna (maior: falha generalizada, ou que compromete o sistema ou o resultado para o cliente; menor: falha pontual ou parcial), e não a contagem de desvios na amostra. Técnica de auditoria (tec_body.html): módulo 8, linha "Desvio pontual", ação "Não conformidade; ampliar a amostra para saber se é pontual ou repetido." → "Não conformidade; ampliar a amostra para medir a extensão."; módulo 5, nota "O que fazer com um desvio", acrescentada a frase do grau pelo critério de Auditoria; exemplo 1, "O que observar": a não conformidade das comandas passa a ter o grau dito (menor, falha parcial, só nas comandas de sábado). O rótulo "Desvio pontual" (ISOL) fica. Certificação (cert_body.html): módulo 6, parágrafo "a maior põe em dúvida a capacidade do sistema de alcançar os resultados, ou mostra uma falha que se repete" → "…ou mostra uma falha generalizada, ou que volta depois de a ação corretiva ter sido dada como concluída"; tabela, NC maior, "desvio que se repete" → "falha generalizada, ou que volta depois de a ação corretiva ter sido dada como concluída"; glossário, NC maior, "ou mostra falha que se repete" → "ou mostra falha generalizada, ou que volta depois de a ação corretiva ter sido dada como concluída". "NC menor: desvio pontual, que não compromete o sistema" fica. A I-3 (4 de 11 mudanças sem autorização, 2 depois da constatação da auditoria interna) continua maior, porque a ação corretiva não funcionou; o item do questionário sobre ela fica. Auditoria não muda.

### N25

**Estudos que mudam:** Producao, Conhecimento, Caso-Integrado

**Conflito.** Achado na revisão da tarefa 4. Depois de T15, Escopo, ISO 9001 e Conhecimento (módulo das normas) dizem que atender a reclamação não é atividade pós-entrega: ela é tratada pelo 8.2.1, pelo 9.1.2 e pelo 10.2. Dois lugares ainda punham a reclamação entre as atividades pós-entrega.

**Decisão.** Pós-entrega é garantia, assistência, obrigações do contrato e serviços como o recolhimento; a reclamação é tratada pela comunicação com o cliente, pelo monitoramento da satisfação e pelo tratamento de não conformidade. Produção (prod_body.html), módulo das normas, linha 8.5.5, coluna do significado: "Garantia, assistência e atendimento a reclamações fazem parte do serviço." → "Garantia, assistência e o que o contrato prevê depois da entrega fazem parte do serviço. A reclamação segue pela comunicação com o cliente e pelo tratamento de não conformidade." Conhecimento (con_body.html), glossário, "Atividades pós-entrega": "O que a organização faz depois que o produto chega ao cliente: garantia, assistência, atendimento a reclamações, recolhimento." → "O que a organização faz depois que o produto chega ao cliente: garantia, assistência, obrigações do contrato, recolhimento. A reclamação é tratada pela comunicação com o cliente, pelo monitoramento da satisfação e pelo tratamento de não conformidade." Os outros textos de Conhecimento que tratam a reclamação junto com o pós-entrega (introdução e tabela do módulo 1) ficam para a tarefa do grupo de Apoio e avaliação decidir. Decidido na tarefa 7 (con_body.html, con_data.py): o estudo continua a tratar a reclamação junto, no mesmo registro de atendimentos (tipos, contagens e datas sem mudança), mas não a chama de pós-entrega. Introdução do módulo 1: "atende a reclamação, cumpre a garantia, presta assistência, orienta o uso. É também a melhor fonte de conhecimento novo, porque mostra o produto no uso real." → "cumpre a garantia, presta assistência, troca ou devolve, orienta o uso e faz o que o contrato prevê. As reclamações chegam pelo mesmo caminho e entram no mesmo registro de atendimentos, mas não são atividade pós-entrega: a norma as trata pela comunicação com o cliente, pelo monitoramento da satisfação e pelo tratamento de não conformidade. Os atendimentos, de um tipo ou de outro, são a melhor fonte de conhecimento novo, porque mostram o produto no uso real." Tabela do módulo 1, "Pós-entrega": "As atividades depois da entrega: reclamação, garantia, devolução, assistência, orientação." / "O laudo da reclamação técnica em 5 dias." → "As atividades depois da entrega: garantia, devolução, assistência, orientação e o que o contrato prevê. A reclamação entra no mesmo registro, mas tem requisitos próprios." / "O ajuste da seladora do cliente ao filme novo." (o atendimento N-03). Figura 1, caixa "Pós-entrega": "Reclamação, garantia, assistência, orientação de uso." → "Garantia, assistência, orientação de uso. As reclamações chegam pelo mesmo caminho." A regra N25 de PROIBIDO ganha as duas frases antigas do módulo 1. Revisão da tarefa 7: outros lugares de Conhecimento ainda punham o tratamento da reclamação no pós-entrega. Pontos de atenção do módulo 11: "No pós-entrega, pede a política de garantia, escolhe três reclamações e confere prazo, causa e o que mudou depois." → "No pós-entrega, pede a política de garantia; nas reclamações, escolhe três e confere prazo, causa e o que mudou depois." Exercício 1, item 6: "A reclamação de atraso foi resolvida com desconto, sem causa registrada.", resposta "Acertar o pós-entrega" (P), explicação "Reclamação resolvida pede a causa, ou volta." → "A reclamação de atraso foi resolvida com desconto. O caso fechou sem causa registrada, e a entrega continua igual.", resposta "Dar destino à lição" (L), explicação "Sem a causa, a reclamação não vira lição, e o atraso volta." (12 itens; C 3, L 4, P 2, O 3). Política do exemplo 2 (con_data.py), coluna "O que se faz depois da entrega", nos três produtos: "Laudo da reclamação técnica" → "Laudo técnico do defeito" (o resto da frase fica). Lição I-07 (bobina telescopada, vinda da reclamação N-05): origem "Pós-entrega" → "Reclamação". Os atendimentos, que incluem as reclamações, deixam de ser chamados de pós-entrega: tabela do módulo 2, linha "A cada atendimento", "O pós-entrega vira dado." → "O atendimento vira dado."; módulo 8, "o primeiro sinal de que o pós-entrega precisa de gente" → "o primeiro sinal de que o atendimento precisa de gente"; caixa "O custo do pós-entrega" → "O custo dos atendimentos"; tabela do módulo 10, linha da Análise crítica, "o custo do pós-entrega, como entrada" → "o custo dos atendimentos, como entrada". Propagado ao Caso integrado (caso_body.html, questionário): "O custo do pós-entrega somou R$ 13.000 em dois meses." → "O custo dos atendimentos depois da entrega somou R$ 13.000 em dois meses."; explicação do item da cantoneira, "O que se aprendeu no pós-entrega vai para o procedimento e para o treinamento." → "O que se aprendeu com a reclamação vai para o procedimento e para o treinamento." O título do estudo, a aba Pós-entrega e a política de pós-entrega (com o prazo para reclamar, que é o da garantia legal ou contratual) ficam. A regra N25 ganha "escolhe três reclamações", "Laudo da reclamação técnica" e "custo do pós-entrega".

### N26

**Estudos que mudam:** Objetivos

**Conflito.** Achado na tarefa 5. Pelo item T23 do spec, o O5 da pizzaria (dar indicador e meta aos quatro processos que não tinham, prazo 26/02/2027) passa a constar como alcançado em março, com atraso: o acompanhamento de Objetivos mostra 5, 7, 9 e 9 de janeiro a abril. Mas a única ação do O5 aparecia concluída em 24/02/2027, dentro do prazo, e a ficha dava "9 de 9 em 24/02/2027".

**Decisão.** Vale T23 (spec, aprovado) e o acompanhamento (5, 7, 9, 9), que tem as contas do quadro: a ação "Definir o indicador do salão, das compras, da manutenção e do treinamento, com os líderes" foi concluída em 10/03/2027, depois do prazo de 26/02/2027 (obj_data.py, data de conclusão, era 24/02/2027). Resultados, prazo, situação e contagens não mudam. Nenhum estudo diz quando cada indicador foi definido; a ficha escolhe, coerente com o acompanhamento (5, 7, 9) e com o O7, cuja cobertura da matriz tem resultado desde fevereiro: em fevereiro, A1 (comprar e armazenar) e A3 (treinar a equipe); em março, P4 (atender no salão) e A2 (manter equipamentos e motos), quando a ação foi concluída. O número-chave passa a "7 de 9 em fevereiro (A1 e A3) e 9 de 9 em março de 2027 (P4 e A2)". A decisão c3 da análise crítica de 14/12/2026 (prazo 26/02/2027) não muda.

### N27

**Estudos que mudam:** Processos

**Conflito.** Achado na revisão da tarefa 5. I16 mandava mudar o elemento g (avaliação) do G1 da pizzaria de "Não" para "Parcial", mas o conflito do spec é o do elemento c: o G1 tem o indicador "Objetivos alcançados no ano" e o elemento c (critérios e indicadores) dizia "Não". Com isso, a coluna c contava 5 processos sem indicador, contra "Quatro processos não têm indicador" no "O que observar" de Processos e a base 5 de 9 do O5 em Objetivos.

**Decisão.** Em Processos (proc_data.py, G1), o elemento c passa de "Não" a "Parcial", e o g volta a "Não": "SPNSSPPP" (versão da tarefa 5) → "SPPSSPNP" (era "SPNSSPNP" antes da leva). Pontos 5,0 e 63% sem mudança; coluna 4.4.1 c: 3 sim, 2 parcial, 4 não; coluna g: 2 sim, 2 parcial, 5 não. O parcial do G1 fica como o do P1, só na tabela dos elementos. A parte da pizzaria de I16 foi corrigida.

### N28

**Estudos que mudam:** SWOT

**Conflito.** Achado na revisão da tarefa 5. N08 trocou o W2 da SWOT, exemplo 2, de "Processo manual, em planilhas e e-mails" para "Cotações e aprovações por e-mail, fora do sistema de compras", e manteve as estratégias. A estratégia WO "W2 × O2" da planilha ficou falando de planilhas que o exemplo não tem mais.

**Decisão.** Na aba "Exemplo 2 - Compras" (build_swot.py), "Implantar uma plataforma de cotação eletrônica no lugar das planilhas." passa a "Implantar uma plataforma de cotação eletrônica no lugar das cotações por e-mail." O treinamento não mostra as estratégias do exemplo 2.

### N29

**Estudos que mudam:** Liberacao

**Conflito.** Achado na tarefa 6, ao aplicar P16 na indústria. O cabeçalho de autoridades do exemplo 2 de Liberação dizia só "Coordenador da Qualidade. Refugo acima de 500 kg e recolhimento no cliente: gerente industrial e gerente comercial.", mas o 2027-23 (devolução da resina) foi decidido pelo gerente de Suprimentos, o 2027-24 (retrabalho na linha) pelo líder do turno, e os recolhimentos 2027-22 e 2027-25 pelo gerente comercial sozinho e pelo coordenador da Qualidade. O exercício do estudo dá como certa a devolução da resina decidida pelo gerente de Suprimentos e como certa a autoridade do líder do turno no refile.

**Decisão.** O cabeçalho da indústria ("Quem decide a disposição", lib_data.py) passa a "Coordenador da Qualidade. Retrabalho na linha: líder do turno. Devolução de insumo ao fornecedor: gerente de Suprimentos. Refugo acima de 500 kg e recolhimento no cliente: gerente industrial e gerente comercial." O 2027-23 e o 2027-24 ficam como estão; no 2027-22 e no 2027-25 (recolher ou substituir), quem decidiu passa a "Gerente industrial e gerente comercial" (eram "Gerente comercial" e "Coordenador da Qualidade"). O lote 140 ganha quem liberou, "Analista da Qualidade", e a observação "Retido em 20/05; liberado em 21/05, com a concessão do cliente B." A decisão do lote continua "Retido" (a de 20/05), e as contagens não mudam. Não foi achada no texto atual a frase "2 fora" citada no conflito de P16: as colunas "Fora" das liberações batem com os registros.

### N30

**Estudos que mudam:** Fornecedores

**Conflito.** Achado na tarefa 6, ao aplicar T38. Fornecedores tinha a usinagem de moldes (F-12) como processo terceirizado e o transporte (F-09) e os ensaios externos (F-11) como serviço; o Escopo e a ficha dão como processos terceirizados da indústria a armazenagem e o transporte, os ensaios de migração em laboratório externo e a calibração, e como serviços críticos a manutenção (F-10) e a usinagem (F-12).

**Decisão.** No cadastro do exemplo 1 de Fornecedores (forn_data.py), F-09 (transporte de produto acabado) e F-11 (ensaios de migração e espessura) passam a "Processo terceirizado", e F-12 (usinagem de moldes) a "Serviço". No módulo 1, os exemplos de serviço ficam "Manutenção, usinagem de moldes, revisão das motos." e os de processo terceirizado "Impressão ou laminação feitas fora, ensaio em laboratório externo, entrega ao cliente por transportadora ou por aplicativo."; a nota "Processo terceirizado" do módulo 3 passa a usar a entrega ao cliente pela transportadora. Índices, classes e contagens não mudam.

### N31

**Estudos que mudam:** Producao

**Conflito.** Achado na revisão da tarefa 6. A primeira aplicação de P15 ("um registro por noite nos demais") escreveu frequências fracas no plano da pizzaria: K7 "Uma pizza por noite, no pico", também como exemplo do campo Frequência no módulo 3, que ensina que a frequência acompanha o risco; K4 "Uma vez por noite, no pico"; K6 "Uma vez por noite: a maior espera, lida no fechamento", que não sustenta as reações durante o serviço (saída priorizada em 12/03, pedidos refeitos em 13/03). O exercício dá como completos "três pedidos por hora" (K7) e "uma vez por hora" (K4), e Liberação diz que a temperatura na saída "não foi medida na última hora do pico" em 20/03. Na indústria, K2 ("A cada duas horas") e K4, K5 e K7 ("Cada bobina") tinham um registro por lote.

**Decisão.** As conferências acontecem durante a noite e no pico; o registro de cada noite (ou de cada lote, na indústria) resume essas conferências. Nenhum total muda: pizzaria 56 verificações, 6 fora, 1 sem reação; indústria 40, 5 e 1; "8 de 8" em Liberação. Pizzaria (prod_data.py): K4 "O que controlar" "Temperatura do forno" → "Temperatura do forno no pico: a pior leitura da noite", frequência "Uma vez por noite, no pico" → "A cada hora do pico; registra-se a leitura fora da faixa ou, com todas dentro, a mais afastada de 300 °C"; K5 "Uma amostra de 20 pedidos por noite, somada no fechamento" → "20 pedidos por noite, conferidos na saída durante o pico; o fechamento registra quantos tinham a rubrica"; K6 "Uma vez por noite: a maior espera, lida no fechamento" → "Acompanhada no sistema durante a noite; a maior espera é registrada no fechamento"; K7 "O que controlar" "Temperatura da pizza na saída" → "Menor temperatura da pizza na saída, na noite", frequência "Uma pizza por noite, no pico" → "Três pizzas por hora no pico; registra-se a menor temperatura da noite". Módulo 3 (exemplo do K7): "O que controlar" → "A menor temperatura da pizza na saída, na noite, na expedição"; "Frequência" → "Três pizzas por hora no pico; registra-se a menor temperatura da noite". Ficam: K1 "Duas leituras por noite" (14 registros, cada leitura registrada; o texto passa a "Duas leituras por dia, uma em cada turno" pela N36), K2 "Uma vez por noite, no lote de massa do dia" (7, um lote por dia), K3 "Uma vez por noite, na abertura" (7, uma abertura por noite). Indústria: K2 "A cada duas horas" → "A cada duas horas; a folha registra, por lote, a leitura mais afastada de 190 °C"; K4 "Cada bobina" → "Cada bobina; a folha registra, por lote, a largura mais afastada de 600 mm"; K5 "Cada bobina" → "Cada bobina; a folha registra, por lote, se todas as bobinas estão conformes"; K7 "Cada bobina" → "Cada bobina; o romaneio registra, por lote, se todas as etiquetas conferem" (5 registros cada, um por lote). Ficam: K1 "Cada lote recebido" (5), K3 "Cada bobina" (10, duas bobinas por lote), K6 "Uma amostra por lote" (5). Os exercícios ("três pedidos por hora", "uma vez por hora", "a cada bobina") e a frase de Liberação sobre a última hora do pico passam a concordar com o plano sem mudança.

### N32

**Estudos que mudam:** Competencias

**Conflito.** Achado na tarefa 7, ao aplicar P18. P18 manda valer a matriz de Suprimentos de 12/03/2027 e dá "Felipe nível 2 em S7", mas a matriz (comp_data.py, "32223100") dá nível 0 a Felipe em S7: é a lacuna que o curso de 24/02/2027 trata, com a eficácia ainda a avaliar (ação 8 do plano, "Em acompanhamento"). O questionário dava 1 ("fez o curso há uma semana e ainda não aplicou").

**Decisão.** Vale a matriz, como P18 manda: Felipe tem nível 0 em S7 (uma lacuna; 11 lacunas na indústria, sem mudança). O número "2" de P18 para Felipe foi lido errado e não é aplicado: dar 2 mudaria a matriz, as contagens e deixaria a ação 8 do plano sem lacuna. No questionário de Competências (comp_body.html), o item de Felipe passa a "Felipe fez o curso de requisitos da ISO 9001 para aquisição, mas, perguntado no posto, não soube dizer o que a norma pede de um fornecedor.", resposta 0, com a explicação "O curso não basta: ele ainda não conhece o padrão. O nível vem do que a pessoa sabe e faz no posto, e não do certificado." Luana segue P18 (nível 2 em S1, resposta 2).

### N33

**Estudos que mudam:** Recursos

**Conflito.** Achado na tarefa 7. Pelo item T50 do spec, a pizzaria de Recursos tinha 20 pizzas por hora por pizzaiolo no dimensionamento (60 pizzas por hora, 3 pizzaiolos, "Justo") e 24 pizzas por hora medidas no fator de ambiente "Pizzas por pizzaiolo no pico".

**Decisão.** Vale o dimensionamento, que tem a conta da escala: 60 ÷ 3 = 20. No fator de ambiente (rec_data.py, exemplo 1), o valor medido passa de 24 a 20 pizzas por hora, dentro do limite de 20, e a ação "Rever a escala da sexta em maio, com a demanda de abril." sai, porque não há o que rever. O ambiente da pizzaria passa de 3 a 2 fatores fora do limite; as outras contagens não mudam.

### N34

**Estudos que mudam:** Satisfacao

**Conflito.** Achado na revisão da tarefa 7. Satisfação, exemplo 3 (reclamação do cliente A de 14/09/2026, fechada na análise crítica de 18/02/2027), "O que observar": "O cliente A não reclamou de novo." Mas o mesmo cliente reclama do filme fino do lote 135 em 24/05/2027 (Liberação, Calibração, Conhecimento I-01, Caso integrado e a linha do tempo), e de cor e de odor em agosto e setembro de 2027 (Conhecimento, N-01 e N-07).

**Decisão.** Vale a linha do tempo. A frase passa a valer só até o fechamento do exemplo, como já diz a etapa "Fechada" de 18/02/2027 em sat_data.py ("Nenhuma reclamação do cliente A de outubro a fevereiro."). Satisfação (sat_body.html), exemplo 3, "O que observar": "O cliente A não reclamou de novo." → "O cliente A não reclamou de novo até fevereiro." Nenhum outro estudo dizia que o cliente A não reclamou mais.

### N35

**Estudos que mudam:** 5W2H

**Conflito.** Achado na revisão da tarefa 8. 5W2H, exemplo 1, "O que observar": "Cada causa confirmada recebeu pelo menos uma ação" e "As duas últimas linhas não atacam causas: uma mede o resultado". Mas o Ishikawa e o PDCA dão a fila do forno (C1) como confirmada e deixada para o ciclo seguinte, sem ação, e a A5 (medir por faixa de horário) é a ação de controle da causa de não detecção E1 (T61).

**Decisão.** Valem o Ishikawa e o PDCA (P22, T61). 5W2H (w5_body.html), exemplo 1, "O que observar": "Cada causa que seguiu para o plano recebeu pelo menos uma ação, e o motivo está escrito ao lado dela. A fila do forno, confirmada, ficou para o ciclo seguinte, como no Ishikawa. A A5 responde à causa de não detecção (E1): mede o tempo por faixa de horário, para que o pico não volte a se esconder na média do dia, e dá os dados da verificação. A A6 transforma o novo método em padrão. Um plano que só ataca as causas de ocorrência deixa de fora o controle, a verificação e a padronização." As ações e os números não mudam.

### N36

**Estudos que mudam:** Auditoria, Partes-Interessadas, Producao

**Conflito.** Achado na revisão final. A frequência da leitura da câmara fria se contradizia: "duas vezes por turno" em Auditoria (pergunta do checklist e critério da constatação 2 da auditoria 2026-03; tabela de como escrever a constatação), em Partes interessadas (vigilância sanitária) e na ficha (IT-PRO-01 e N02); "duas leituras por noite" em Produção (K1, P15 e N31); e a Técnica de auditoria conta 56 leituras em fevereiro de 2027, duas por dia. Com os dois turnos da pizzaria (N22), "duas vezes por turno" daria quatro leituras por dia.

**Decisão.** Uma leitura em cada turno, duas por dia (regra 4.3 do desenho: a versão dos números conferidos, em mais estudos, e a que muda menos). Valor antigo → novo: aud_data.py, checklist, "A temperatura da câmara fria é registrada duas vezes por turno?" → "A temperatura da câmara fria é registrada em cada turno?", e a evidência "3 turnos sem nenhum registro: 12/09 noite, 13/09 noite e 20/09 noite." → "3 turnos sem registro: 12/09 noite, 13/09 noite e 20/09 noite."; constatação 2, critério "Rotina de controle: a temperatura da câmara fria deve ser registrada duas vezes por turno." → "…deve ser registrada uma vez em cada turno."; aud_body.html, "A rotina IT-PRO-01 pede o registro da temperatura duas vezes por turno." → "A rotina IT-PRO-01 pede o registro da temperatura em cada turno."; pi_data.py, vigilância sanitária, "registro de temperatura, duas vezes por turno." → "registro de temperatura, uma vez em cada turno."; prod_data.py, K1, frequência "Duas leituras por noite" → "Duas leituras por dia, uma em cada turno"; prod_body.html, tabela do módulo 2, linha Registro, "A planilha de temperatura, duas vezes por noite." → "A planilha de temperatura, uma leitura em cada turno."; caixa "Controle bem escrito", "no visor, duas vezes por noite." → "no visor, uma vez em cada turno."; build_prod_html.py, figura do K1, "DUAS LEITURAS POR NOITE" → "UMA LEITURA EM CADA TURNO". Ficha: título da IT-PRO-01, N02, P15 e N31. Ficam: as 14 leituras de Produção (duas por dia, em 7 dias; a 2ª do dia 11/03 fora, às 21h40, no turno da noite), as 56 de fevereiro na Técnica de auditoria, os 28 turnos de Auditoria, a c5 da Análise crítica ("registrada em todos os turnos"), a GUT ("registrar a temperatura duas vezes por turno até o reparo", medida provisória do P3, treinamento e planilha), o item do questionário de Produção que dá "duas vezes por turno" como controle mal escrito (o erro do item é a falta do número) e Recursos ("Visor lido na abertura e no fechamento", abril de 2027: duas leituras por dia). Emenda a N02, que o autor aprovou: decisão do controlador, à espera da revisão do autor.

### N37

**Estudos que mudam:** Indicadores

**Conflito.** Achado na revisão final, ao refazer a média do P1 (P07). A coluna "Média do ano" de Indicadores sai de dois lugares: a planilha calcula a média e a mostra com uma casa, arredondando o meio para cima; o treinamento (build_ind_html.py) a escrevia com o arredondamento do Python, que leva o meio ao par. Nas médias que terminam em 5 na segunda casa, os dois divergiam: C2 30,25 (planilha 30,3, treinamento 30,2) e C3 81,25 (planilha 81,3, treinamento 81,2); com agosto em 94, o P1 dá 84,25 (planilha 84,3, treinamento 84,2).

**Decisão.** Vale a planilha, que tem a conta (e é a regra do estudo de Processos, build_proc_html.py: o meio vai para cima). O gerador do treinamento passa a arredondar a média como a planilha (build_ind_html.py, função media). Valor antigo → novo no treinamento de Indicadores: P1 84,4 → 84,3 (por P07); C2 30,2 → 30,3; C3 81,2 → 81,3. As outras médias não mudam. Ficha: média do ano do C2 30,2 → 30,3. Nenhum outro estudo cita essas médias. Decidida na correção da revisão final (seção 4.3 do desenho), à espera da revisão do autor.
