# Leva 1: correções e ficha de fatos

Data: 03/10/2026. Situação: desenho para revisão do autor.

## 1. Contexto

O objetivo da série é levar uma pessoa que nunca auditou ISO 9001 a auditor sênior, com conhecimento profundo e prático. A meta escolhida é o caminho completo: auditor interno primeiro, até liderar o programa de auditoria, e auditor de terceira parte como etapa final.

A análise de 03/10/2026 leu os 34 estudos e concluiu que a série forma um bom implantador, mas ainda não forma um auditor. O trabalho foi dividido em quatro levas, cada uma com desenho, plano e execução próprios:

1. **Correções e ficha de fatos** (este documento).
2. Módulo "Como auditar este requisito" e exercício "você é o auditor" nos 34 estudos.
3. Estudos novos da trilha do auditor.
4. Simulado final e trilha por níveis no painel.

A leva 1 vem primeiro porque as outras três constroem sobre os exemplos: um exercício de auditoria montado sobre fatos que se contradizem ensina errado.

## 2. Objetivo e critérios de sucesso

Ao fim da leva 1:

- nenhum estudo ensina um hábito errado de auditor (seção 5);
- a pizzaria e a indústria têm uma história única, sem contradição entre estudos (seção 6);
- nenhum texto descreve a série como ela era antes (seção 7);
- existe uma ficha de fatos por organização, e um teste que falha quando um estudo a contradiz (seção 4);
- todas as planilhas abrem calculadas, e os testes de fórmulas existentes continuam passando.

## 3. Fora do escopo

- Módulos, exercícios e estudos novos (levas 2 a 4).
- Marcar, item por item, o que é norma e o que é convenção nos checklists e nas planilhas (leva 2, junto com o módulo "Como auditar").
- Defeitos plantados de propósito nos exemplos. Na leva 1 os exemplos ficam coerentes; os defeitos entram na leva 2, declarados e com gabarito.
- Ligar os arquivos `<estudo>_data.py` à ficha de fatos por importação. A ficha é referência e base do teste; os dados de cada estudo continuam onde estão.
- Mudanças de aparência, de estrutura dos módulos ou do painel, além das contagens e das frases citadas aqui.

## 4. Ficha de fatos e teste de coerência

### 4.1 `_geradores/fatos.py`

Um módulo Python só com dados, legível por quem vai escrever um estudo novo. Uma entrada por organização (`pizzaria`, `industria`, `distribuidora`), cada uma com:

- **identidade**: nome usado nos estudos, escopo, dias e horários de funcionamento, edição da norma e datas da certificação;
- **pessoas e cargos**: nome, quando houver, cargo, desde quando, o que só essa pessoa sabe;
- **processos**: código, nome e dono;
- **equipamentos e instrumentos**: código, descrição, critério, situação e datas;
- **documentos**: código, título, revisão vigente e data;
- **registros numerados**: série, número, data, assunto e estudo de origem;
- **linha do tempo**: data, evento e estudos que o citam;
- **números-chave**: metas e valores de indicadores citados em mais de um estudo.

O módulo traz também duas listas usadas pelo teste:

- `PROIBIDO`: expressões regulares que não podem voltar a aparecer, cada uma com o motivo (por exemplo, "certificado há 8 anos");
- `CONTAGENS`: as frases que citam o número de estudos da série.

### 4.2 `_geradores/testes/coerencia.py`

Lê os 34 treinamentos e o painel, tira as marcações e confere:

1. nenhuma expressão de `PROIBIDO` aparece;
2. todo código de documento, de instrumento e de registro numerado encontrado nos textos existe na ficha, na organização certa, e um mesmo código não tem dois significados;
3. os registros de cada série estão em ordem: número maior, data igual ou posterior;
4. toda frase que cita o número de estudos bate com o número de cartões do painel.

O roteiro termina com código de saída diferente de zero quando algo falha, e lista arquivo, trecho e motivo. O `README.md` de `_geradores/` ganha uma seção sobre a ficha e o teste, com a regra: ler a ficha antes de escrever um estudo, e atualizá-la no mesmo commit.

### 4.3 Regras para decidir o cânone

Quando dois estudos se contradizem, vale, nesta ordem:

1. a versão que aparece em mais estudos;
2. a versão com data e número de registro;
3. a versão que exige mudar menos arquivos, sem alterar contas já conferidas.

As decisões já tomadas estão na seção 6. O que só aparecer durante a montagem da ficha segue as mesmas regras e entra numa tabela de conflitos.

### 4.4 Ponto de revisão

A ficha é o primeiro entregável. Antes de qualquer estudo ser alterado, o autor revê a tabela de conflitos, com o valor escolhido para cada um. Só depois começam as correções.

## 5. Correções técnicas

Cada item traz a decisão. "Propagar" quer dizer levar a mudança ao treinamento, à planilha, aos testes de fórmulas e aos outros estudos que citam o trecho.

### 5.1 Núcleo de auditoria

| Nº | Estudo | Problema | Correção |
|---|---|---|---|
| T01 | Técnica de auditoria | Um desvio único, com requisito e evidência objetiva, é tratado como "oportunidade ou ponto a verificar" até a amostra ser ampliada. | Um caso com evidência objetiva já é não conformidade. A ampliação da amostra mede a extensão e ajuda a decidir o grau, não a existência. Mudam o módulo 5, a tabela do módulo 8, os dois exemplos, o questionário, o checklist, os rótulos e o painel da planilha. Propagar. |
| T02 | Técnica de auditoria | "Toda não conformidade é corroborada por duas fontes." | A não conformidade exige ao menos uma fonte objetiva: registro ou observação. Só entrevista continua fraca e pede corroboração. A segunda fonte é recomendada. As três forças da evidência ficam. |
| T03 | Técnica de auditoria, exemplo 1 | A leitura de temperatura que faltou em 14/02, 1 de 10, fica "para ampliar". | Vira não conformidade menor, pontual, com a amostra a ampliar. Contagens refeitas. |
| T04 | Técnica de auditoria, exemplo 2 | Quebra do chiller sem destino do produto, 1 de 5, vira oportunidade de melhoria. | Vira não conformidade menor contra o 8.7. A oportunidade I-6 do estudo de Certificação continua: em novembro o destino já é registrado, em outro documento. Contagens refeitas. |
| T05 | Auditoria, exemplo 1 | Constatação 3: a instrução manda treinar a equipe, 1 de 2 entregadores novos não foi treinado, e o resultado é oportunidade de melhoria. | Vira não conformidade menor nº 3. O "O que observar" explica por que não é oportunidade. A oportunidade de melhoria continua ilustrada no exemplo 2. Propagar para a planilha. O treinamento do Igor em 28/10/2026, já registrado em Competências, passa a ser citado como a correção. |
| T06 | Não conformidade | "A verificação deve ser feita por quem não executou as ações." | "Convém", com o aviso de que é convenção do material. |

### 5.2 Norma e sistema

| Nº | Estudo | Problema | Correção |
|---|---|---|---|
| T07 | Escopo | Só 7.1.5, 8.3, 8.5.3 e 8.5.5 podem ser não aplicáveis; fora deles, "não há justificativa possível". | Os quatro são os candidatos mais comuns. Fora deles, a planilha pede justificativa reforçada, em vez de proibir. Propagar. |
| T08 | Escopo, ISO 9001, Calibração | O 7.1.5 inteiro aparece como não aplicável. | Não aplicável é o 7.1.5.2, quando a rastreabilidade não é requisito. O 7.1.5.1 vale sempre que há monitoramento ou medição, e conferência de documentos é monitoramento. |
| T09 | Escopo | "A ISO 9001 não exige os dez compromissos." | Os dez são as alíneas do 5.1.1. O que a norma não exige é o formato e a classificação do material. |
| T10 | Escopo e painel | Processos terceirizados atribuídos ao 4.4. | 8.1 e 8.4. Corrigir também a linha do estudo no painel. |
| T11 | ISO 9001 | "Lista completa" das entradas da análise crítica com dez itens. | As doze, como no estudo de Análise crítica. |
| T12 | ISO 9001 | "O auditor confere a seção 5 conversando com a direção, e não lendo documentos." | "Principalmente pela entrevista, corroborada por atas e decisões." |
| T13 | ISO 9001, exemplo 1 | 5.1.1 atendido sem política e sem análise crítica. | "Em parte", com os percentuais refeitos. Propagar para os estudos que citam os percentuais do diagnóstico. |
| T14 | ISO 9001 | A nota do módulo 2 cita só parte dos requisitos agrupados. | Completar a nota. |
| T15 | Escopo, ISO 9001, Conhecimento | Atender reclamação como atividade pós-entrega. | Garantia ou assistência no exemplo. Uma frase em Conhecimento: a reclamação é tratada pelo 8.2.1, 9.1.2 e 10.2. |
| T16 | ISO 9001:2026 | A emenda de 2024 descrita como dois requisitos. | Requisito no 4.1; no 4.2, nota. |
| T17 | ISO 9001:2026 | "Alta: 4 pontos ou mais: impacto alto com lacuna…" | "Impacto alto ou médio sem atender." |
| T18 | ISO 9001:2026, exemplo 1 | M5 "atende em parte" só com evidência negativa; pontos de lacuna de ações já concluídas. | Completar a evidência do M5 e dizer que a pontuação é a do diagnóstico, e a situação, a do andamento. |
| T19 | Informação documentada | "A Produção tem o maior número de pendências, 5." | Produção e Manutenção, 5 cada. |

### 5.3 Contexto e planejamento

| Nº | Estudo | Problema | Correção |
|---|---|---|---|
| T20 | Objetivos | O resumo do 6.2.1 não traz a alínea d. | Incluir: pertinentes à conformidade de produtos e serviços e ao aumento da satisfação do cliente. |
| T21 | Objetivos | "Não alcançado e sem decisão registrada é não conformidade." | Dizer contra qual requisito, e trocar "registrada" por "sem evidência de análise e ação". |
| T22 | Objetivos | "A ação funcionou", mas o indicador caiu antes da ação. | Reescrever a conclusão: a queda começou antes, e a ação sozinha não a explica. |
| T23 | Objetivos | "Alcançado" com um único mês. | A regra da planilha fica. Aviso no módulo 7: um mês não sustenta um objetivo anual. O O5 passa a constar como alcançado em março, com atraso. |
| T24 | Objetivos | Itens do questionário com mais de uma resposta certa. | Reescrever os enunciados para resposta única. |
| T25 | Riscos | Oportunidade definida como evento incerto favorável. | Aviso: a conta de probabilidade e benefício é convenção, e a norma fala em situação favorável. |
| T26 | Riscos | "Há quatro respostas possíveis." | São uma simplificação; citar as outras opções da nota do 6.1.2. |
| T27 | Riscos, exemplo 1 | R5 classificado como compartilhar, com queda só da probabilidade. | Separar: revisão e treinamento reduzem; o seguro compartilha. |
| T28 | Riscos | Plano de contingência exigido para impacto 5, e nenhum mostrado. | Mostrar um plano no exemplo e ajustar a nota do C6. |
| T29 | SWOT, exemplo 2 | "As fraquezas pesam mais", comparando somas de 3 e de 4 fatores. | Comparar médias, no texto e na planilha. Propagar. |
| T30 | Processos | "Um projeto não é um processo"; dono único e indicador por processo no imperativo. | Tirar o projeto da lista e pôr dono único e indicador na lista "não exige". |
| T31 | Riscos, RACI | Não dizem que o 6.1 e o 5.3 não pedem informação documentada. | Dizer. |

### 5.4 Operação

| Nº | Estudo | Problema | Correção |
|---|---|---|---|
| T32 | Projeto | "Cada parte pede um registro." | Quatro das seis partes pedem registro retido, de 8.3.3 a 8.3.6. |
| T33 | Projeto | "Exclusão" do 8.3. | "Não aplicabilidade"; "exclusão" é o termo da edição de 2008. |
| T34 | Liberação | Produto sem a verificação planejada listado como saída não conforme. | É produto de situação indeterminada, retido até a verificação. |
| T35 | Fornecedores | "A norma não exige avaliação de fornecedores não críticos." | A norma permite graduar o controle; a classificação precisa de critério defensável. |
| T36 | Fornecedores | 8.6 citado para o recebimento. | 8.4.2. |
| T37 | Fornecedores | Selecionar, avaliar e reavaliar, contra os quatro verbos da norma. | Uma frase com a correspondência. |
| T38 | Fornecedores | Exemplos de processo terceirizado invertidos. | Impressão ou laminação externas e a entrega ao cliente. |
| T39 | Produção | Identificação do produto como exigência incondicional. | "Quando necessário para assegurar a conformidade." |
| T40 | Produção | 8.5.6 lido como "nenhuma mudança sem análise prévia". | Nota: a norma admite analisar depois, na extensão necessária; a análise prévia é a prática do material. |

### 5.5 Apoio e avaliação

| Nº | Estudo | Problema | Correção |
|---|---|---|---|
| T41 | Calibração | "Erro, ou correção" como sinônimos. | Duas linhas, com o sinal de cada uma. |
| T42 | Calibração, exemplo 1 | TER-01 conferido só a 0 °C e usado a 5 °C e a 65 °C, sem comentário. | Apontar no "O que observar" como lacuna do exemplo, com a ação. |
| T43 | Recursos | Termopar de 185 °C verificado contra padrão calibrado até 20 °C. | Calibração externa depois do reparo. |
| T44 | Calibração | Calibração apresentada como sempre externa. | "Laboratório externo ou interno competente." |
| T45 | Calibração | Incertezas menores do que a resolução permite. | Incertezas coerentes com a resolução de 1 µm, mantendo o desfecho: aprovado em 10/01, reprovado em 12/06. Propagar. |
| T46 | Calibração | "Em dia" só com mais de 30 dias, incompatível com verificação mensal. | Alerta proporcional ao intervalo. Propagar. |
| T47 | Calibração | Pior caso não declarado no exemplo 3; "tolerância" em limite unilateral. | Uma frase para cada. |
| T48 | Competências | Alcance do 7.2 com a redação de 2008. | Pessoas que fazem trabalho sob o controle da organização, o que inclui terceiros e temporários. |
| T49 | Recursos | Disponibilidade do sistema de pedidos calculada sobre 180 h. | Corrigir a frase: a câmara fria fica ligada o tempo todo, e o sistema é contado nas horas de loja aberta. |
| T50 | Recursos | 20 pizzas por pizzaiolo num quadro e 24 em outro. | Unificar. |
| T51 | Recursos | "Constatações mais comuns" sem dizer o critério; item do questionário com 7.1.2 no lugar de 7.2. | Dizer contra qual critério cada uma se sustenta; corrigir o gabarito. |
| T52 | Recursos | Horas extras como fator social. | Psicológico. |
| T53 | Análise crítica | "Passou a decidir menos e a concluir mais." | Reescrever conforme a tabela: subiu o cumprimento no prazo. |
| T54 | Satisfação | Reclamação só "vira não conformidade" se grave ou repetida. | Toda reclamação procedente é não conformidade e recebe correção; a ação corretiva é avaliada caso a caso. |
| T55 | Conhecimento | "Entre empresas, quem define o prazo é o contrato." | "Em geral." |

### 5.6 Ferramentas de melhoria

| Nº | Estudo | Problema | Correção |
|---|---|---|---|
| T56 | Histograma e CEP | "Três desvios da média das médias." | Três desvios-padrão das médias, σ ÷ √n, no texto e no glossário. |
| T57 | Histograma e CEP | Cp e Cpk sem ressalvas. | Caixa "o que o Cpk não garante": normalidade, variação só dentro do subgrupo, sistema de medição, limites provisórios. |
| T58 | Histograma e CEP | Subgrupo de cinco posições fixas na largura. | Nota sobre o subgrupo racional. |
| T59 | Histograma e CEP | Coluna "Sinal": bobina 22 no limite; amplitudes das bobinas 20 e 6 acima do limite sem marcação. | A marcação segue a regra: amplitude acima do limite aparece como sinal. O limite da bobina 22 é mostrado com três casas. |
| T60 | Ishikawa | Hipóteses confirmadas com evidência do sintoma. | Registrar o resultado do teste planejado em A1, B1 e C1. |
| T61 | Ishikawa | Causa de não detecção tratada como causa de ocorrência. | Distinguir as duas e marcar E1 como não detecção. |
| T62 | Pareto | Manutenção "responde por 48%", sem o total por área. | Incluir as requisições por área e a taxa. |
| T63 | Pareto | "A causa aqui é uma só." | Hipótese que segue para o Ishikawa. |
| T64 | GUT | Prazo único de 30 dias, inclusive para produto sem identificação. | Separar o prazo da correção, imediato, do prazo da ação corretiva. |
| T65 | GUT | "Metade da lista termina com mais de 100 pontos." | "80 pontos ou mais." |
| T66 | Indicadores | "Resultado ruim sem decisão é uma não conformidade." | "Tende a ser, contra…", com o requisito. |

## 6. Correções de continuidade

### 6.1 Pizzaria

| Nº | Conflito | Cânone | Estudos a ajustar |
|---|---|---|---|
| P01 | A loja "não abre às segundas", com registros em 08, 15 e 22/03/2027, que são segundas. | A loja abre todos os dias. A encomenda para eventos é que só é atendida de terça a domingo. | Pedidos |
| P02 | Oito pessoas em Competências; equipe bem maior em Recursos; "quatro pizzaiolos" em Conhecimento. | Recursos. A matriz de Competências passa a mostrar oito pessoas dos postos-chave, e não a loja inteira. | Competências, Conhecimento |
| P03 | Bruno regula o forno sozinho em fevereiro de 2027; em maio, só o pizzaiolo líder sabe. | Conhecimento e Caso integrado. Em Competências a ação passa a "parcial: reforçar", e o risco R6 continua aberto. Resolve também a eficácia declarada antes do prazo. | Competências |
| P04 | Pizzaiolo líder "há 12 anos" e "desde 06/2021". | Desde 06/2021. | Conhecimento |
| P05 | Alarme da câmara fria com prazo em 11/2026 e ações dadas como concluídas; em 04/2027, "não havia alarme". Preventiva semestral e trimestral. | Recursos. A resposta ao R3 passa a ser só a preventiva, a cada três meses. | Riscos |
| P06 | Sistema de pedidos trocado em julho de 2026 e em abril de 2027. | A troca foi em julho de 2026. Em abril de 2027 houve uma atualização de versão. | ISO 9001:2026, Conhecimento, Recursos |
| P07 | Entregas no prazo: 88 e 94 em junho e julho de 2026, contra 80 a 84 por semana até 26/07. | A série semanal do PDCA e do Pareto. | Indicadores e quem citar os valores |
| P08 | FR-07 é relatório de auditoria e planilha de verificação; formulários da tabela de retenção fora da lista mestra; IT-05 e IT-08 fora do padrão. | FR-07 é a planilha de verificação. O relatório ganha código livre; os formulários entram na lista mestra, com as contagens refeitas; as instruções seguem o padrão IT-XXX-00. | Informação documentada, Conhecimento |
| P09 | IT-EXP-01 revisão 2 em 10/07/2026, antes do plano de 24/07. | Revisão 2 em 31/07/2026. | Informação documentada |
| P10 | "RNC" usado para duas séries; RNC 2027-04 em 03/04 e RNC 2027-07 em 22/03. | Duas séries com nomes diferentes: RNC, do 10.2, e registro de produto não conforme, do 8.7. Os números 2027-27, 29 e 30 pertencem à segunda. Na série RNC, o registro de 22/03 da Liberação passa a 2027-03, antes do 2027-04 de 03/04. | Recursos, Histograma e CEP, Liberação |
| P11 | "Pedidos refeitos" é do P1 num estudo e do P2 em outro. | Processos. | Objetivos |
| P12 | Escopo sem o processo "Atender no salão"; riscos revistos uma vez por ano, contra a revisão semestral; dono e gerente misturados. | Processos e Caso integrado. | Escopo |
| P13 | Caixas "sem avaliação formal", mas avaliadas; homologações antes da decisão de 14/12/2026; avaliação de 11/12 para o semestre inteiro; gás crítico com documentos pendentes. | Caixas fora da tabela, total da classe A refeito; homologações depois de 14/12; avaliação datada em janeiro de 2027; o gás comentado no "O que observar". | Fornecedores |
| P14 | "Quatro resolvidos" com duas recusas; "3 das 8 encomendas"; E-34 fora das 48 horas sem comentário. | Texto refeito pela tabela. | Pedidos |
| P15 | Frequências do plano de controle que não batem com o número de registros; mudança de 26/03 em registros lidos em 15/03; reação do K5 depois da saída. | Ajustar a frequência escrita, sem mudar os totais; dar à tabela de mudanças a própria data de leitura, 31/03/2027; reescrever a reação. | Produção |
| P16 | Decisões tomadas por quem não tem a autoridade escrita; lote 140 liberado sem quem liberou; "segue aberto" contra "0 abertos"; "2 fora" com três fora. | Alinhar quem decidiu com as autoridades, registrar quem liberou e corrigir as frases. | Liberação |
| P17 | Entradas E1 e E2 da pizza vegana "atendem" depois de mudanças de ingrediente e alergênico. | Nota de reverificação. | Projeto |
| P18 | Níveis da Luana e do Felipe diferentes na matriz e no questionário; Camila com lacunas sem ação; Jorge "há sete anos" e "desde 10/2020". | A matriz. | Competências |
| P19 | Meta de reclamações 2,0 e 1,5; "prazo de resposta" com dois sentidos; contingência escrita em 13/04 e incorporada em 20/04. | Objetivos; primeira resposta e solução como termos distintos; escrita em 13/04, incorporada em 20/04, dito assim. | Satisfação, Conhecimento |
| P20 | Termômetro novo da câmara fora da lista de instrumentos. | Incluir, com a contagem refeita. | Calibração |
| P21 | Desperdício e erros com valores diferentes; reunião "toda segunda" numa terça; "três melhoraram" com um estável. | Indicadores, com as datas corrigidas. | GUT, Indicadores |
| P22 | 96% e 68% de entregas no prazo não fecham com a folha do Pareto; 8 hipóteses e 3 causas no PDCA, 12 e 5 no Ishikawa; três ações contra seis; ordem entre Pareto e Ishikawa; problema ausente da lista da GUT; causa raiz sem ação. | Pareto, Ishikawa e 5W2H. | PDCA, Ishikawa, GUT, 5W2H |
| P23 | "Muçarela" e "mussarela"; "fora da meta" com dois sentidos; status e situação trocados. | "Muçarela"; dois termos distintos em Indicadores; os termos do módulo no 5W2H. | Vários |

### 6.2 Indústria

| Nº | Conflito | Cânone | Estudos a ajustar |
|---|---|---|---|
| I01 | "Certificada há 8 anos", contra a primeira certificação em 17/12/2027. | Primeira certificação em 17/12/2027. Antes disso, sistema implantado, sem certificado. | SWOT, Partes interessadas, Auditoria |
| I02 | "Extrusora 4 em operação", contra "as três extrusoras". | Quatro extrusoras desde setembro de 2026. | Recursos |
| I03 | Nove mudanças de processo até setembro de 2027; "das 9 de 2027", com duas depois de outubro. | Onze no ano, quatro sem autorização. | Certificação |
| I04 | "Gerente de Produção", contra "Gerente industrial" e "Gerente de engenharia". | Os cargos de Auditoria, Objetivos e Riscos. | Partes interessadas |
| I05 | Processos "Extrusão", "Engenharia" e "Comercial e Qualidade", que não estão entre os nove. | Os nove de Processos. | Objetivos |
| I06 | Análise crítica "de julho". | 18/02 e 19/08/2027. | Conhecimento, Recursos |
| I07 | Medidor em linha: um ou dois, atraso antes do prazo, decisão antes da reclamação que a justifica. | Dois medidores, para as extrusoras 3 e 4, com prazo em 30/06/2027 e antecipação decidida em 19/08/2027. | Escopo, Análise crítica, Caso integrado |
| I08 | Compras com duas histórias: formulário novo e devoluções de 40% para 12% em 2026, contra indicador em 30% até setembro e RNC 2026-31. | A cadeia datada, de Auditoria, Não conformidade e Indicadores, é a da indústria. A cadeia das ferramentas passa a ser de outra organização, uma distribuidora, nomeada em cada exemplo. | GUT, Pareto, Ishikawa, 5W2H, PDCA |
| I09 | Lote piloto da resina nova, contra "o lote 135 foi o primeiro"; resposta "dentro do critério", contra 37,9 µm medidos. | Um lote piloto anterior ao 135; a resposta inicial e a medição posterior contadas em ordem. | Produção, Calibração |
| I10 | Laudo de migração antes do lote de teste; ensaio com a resina B sem lote da resina B. | Datas refeitas. | Projeto |
| I11 | RNC 2026-29 em 23/09, depois do 2026-31 em 22/09. | A regra de ordem da série, conferida na ficha. | Caso integrado |
| I12 | ISO 9001:2015 "verificada" como vigente em 2027; figura 8 com números de Suprimentos diferentes do exemplo; retenção e intervalo fora da regra. | A edição de 2026 entra na lista de documentos externos; a figura segue o exemplo; as regras com a exceção dita. | Informação documentada |
| I13 | "Cinco etapas", contra oito; "O4" é oportunidade e objetivo; prazos de M5 e M6 depois do limite. | Oito etapas; a oportunidade renomeada; os prazos comentados no "O que observar". | ISO 9001:2026 |
| I14 | Refugo de 2,6% "atende em parte" com meta abaixo de 3%; contagens de quadrantes e de pendências. | Texto refeito pela tabela. | Partes interessadas |
| I15 | "Dois antes do prazo" com três; definição em 19/02 com ações anteriores; meta de 96 com base de 97, que o próprio estudo chama de erro. | Texto refeito; a meta do O3 passa a ser manter 97. | Objetivos |
| I16 | G1 com indicador e "não" no elemento; tartaruga e interações de Suprimentos diferentes. | As duas tabelas alinhadas. | Processos |
| I17 | "Sete seguem para o cruzamento", com estratégias de fatores médios e ameaça alta sem estratégia. | Estratégias refeitas a partir dos fatores de prioridade alta. | SWOT |
| I18 | Visita ao cliente A decidida depois de feita. | Decisão de uma segunda visita. | Análise crítica |
| I19 | Instrumentos vencidos: meta em 60 dias e eficácia em 90; "três quebras" na figura e "duas" no texto; chiller "parou todas" com uma extrusora a 100%. | Prazos e contagens alinhados. | GUT, Ishikawa, 5W2H, Recursos |

### 6.3 Não aplicar

- Formatos diferentes de número de lote e de certificado: variação plausível entre registros.
- Registros em sábado e domingo no Caso integrado: as duas organizações trabalham nesses dias.
- Indústria certificada pela edição de 2015 quinze meses depois da nova: o estudo de Certificação já explica.
- Códigos P1 a P7 para fornecedores e para processos, e números iguais de registro nas duas organizações: a ficha separa por organização e por série.

## 7. Textos desatualizados e regra da edição

| Nº | Onde | Correção |
|---|---|---|
| D01 | Caso integrado: "os 29 estudos", lista de estudos e ordem de implantação | 34 estudos, com os cinco que faltam. O calendário não ganha atividades novas, e os números de cumprimento ficam. |
| D02 | ISO 9001: "uma nova edição estava em preparação" | A edição de 2026 foi publicada em 16/09/2026; remeter ao estudo dela. |
| D03 | Processos, figura 8: partes "sem estudo próprio na série" | Apontar Recursos, Calibração e Informação documentada. |
| D04 | Análise crítica, figura 3 e tabela do módulo 9 | Apontar Satisfação, Fornecedores e Recursos; tabela com os estudos atuais. |
| D05 | SWOT: "as três ferramentas" | Frase refeita. |
| D06 | SIPOC: "1 exercício" | 2 exercícios. |
| D07 | Objetivos, figura 7: "C1 a C4" | Três compromissos. |
| D08 | Todos os módulos sobre as normas | Uma frase padrão: os exemplos se passam de 2026 a 2028 e usam a numeração de 2015, que as organizações seguem até a transição; o estudo ISO 9001:2026 mostra o que muda. |
| D09 | `_geradores/README.md`: número de planilhas com teste | Conferir e atualizar. |

## 8. Como o trabalho é feito

1. **Ficha.** Montar `fatos.py` relendo os estudos por organização. Entregar a tabela de conflitos para revisão (seção 4.4).
2. **Correções, por grupo de estudos.** Os grupos são os das seções 5.1 a 5.6. Em cada estudo, as correções técnicas e as de continuidade entram juntas, nos arquivos de origem: `<estudo>_body.html`, `<estudo>_data.py` e os dois geradores. SIPOC, o treinamento de PDCA e o painel são editados à mão.
3. **Geração.** Cada estudo é gerado primeiro numa pasta de teste e comparado com o atual. Só mudanças previstas neste documento podem aparecer na comparação.
4. **Teste de coerência.** Escrito junto com a ficha, roda depois de cada grupo.
5. **Commits.** Um commit para a ficha e o teste, e um por grupo de estudos. O envio ao GitHub, que publica na Vercel, só a pedido.

## 9. Verificação

- **Texto:** comparação, estudo por estudo, entre o texto extraído antes e depois. Cada diferença corresponde a um item deste documento.
- **Contas:** todo exemplo com número alterado é refeito por roteiro, a partir do arquivo de dados.
- **Planilhas:** os testes de `_geradores/testes/` de todo estudo com fórmula alterada passam depois do recálculo no LibreOffice. Já estão previstos Técnica de auditoria, Escopo, Calibração e SWOT. As planilhas dos exemplos abrem sem erro e sem aviso novo.
- **Figuras:** as alteradas são renderizadas no Chrome sem interface e conferidas nos temas claro e escuro.
- **Coerência:** `coerencia.py` termina sem falhas.
- **Painel:** contagens do cabeçalho e das tabelas conferidas contra os cartões.

## 10. Riscos

- **Propagação incompleta.** Um número corrigido num estudo continua antigo em outro. O teste de coerência cobre códigos e expressões proibidas, mas não todo número; por isso a ficha registra os números-chave e os estudos que os citam.
- **Correção que cria erro novo.** As afirmações sobre o texto das normas vêm de memória. Antes de aplicar um item das seções 5.2 a 5.5 que cite alínea ou nota, conferir numa fonte acessível; se não der para conferir, a redação fica no nível do resumo, sem citar a alínea.
- **Decisão de história.** O item I08 muda de quem é um exemplo usado em cinco estudos. É a decisão mais visível da leva e pode ser revista na revisão da ficha.

## Anexo: insumos para as levas 2 a 4

O que cada estudo já tem para o auditor e o que falta, segundo a análise de 03/10/2026.

| Estudo | Já tem | Falta |
|---|---|---|
| ISO 9001 | Pergunta e evidências por requisito | Não conformidades típicas, redação, grau; separar autodiagnóstico de auditoria |
| ISO 9001:2026 | Pergunta de diagnóstico por mudança | Auditar cultura e ética com evidência objetiva |
| Escopo | Constatações comuns, entrevista com a direção | A entrevista pelo lado do auditor; contestar uma não aplicabilidade |
| Informação documentada | Comparar o documento do posto com a lista mestra | Amostragem, registro eletrônico, o erro de exigir documento que a norma não pede |
| Caso integrado | Seguir o fio | Extrair e classificar constatações dos fios |
| Partes interessadas, SWOT | Evidências, sinais de análise de gaveta | Auditar sem documento, perguntas à direção |
| Objetivos | Constatações comuns, entrevista no posto | Amostragem e redação |
| Processos | A tartaruga na auditoria | Lista de verificação derivada, trilha de um pedido |
| SIPOC | Nada, nem módulo de normas | Módulo de normas e uso na preparação |
| RACI | Evidências e duas perguntas | As responsabilidades do 5.3; cruzar assinaturas com a matriz |
| Riscos | Evidências, exige e não exige | Auditar sem registro de riscos; não conformidades típicas |
| Pedidos, Projeto, Fornecedores | Trilha e constatações típicas | Redação, grau, perguntas no posto; 8.4.3 alínea por alínea |
| Produção | Ronda, teste de rastreabilidade | Validação de processos, frequência do plano contra os registros |
| Liberação | Área de segregação, lotes 139 e 142 | Testar a autoridade de quem decidiu; candidatos a maior |
| Competências | Amostra de pessoas, perguntas do 7.3 | Terceiros; competência por experiência sem registro |
| Calibração | Trilha da etiqueta ao resultado anterior | Checklist do certificado, acreditação, amostragem de instrumentos |
| Recursos, Conhecimento | Perguntas de campo | Auditar requisito sem documento sem inventar requisito |
| Análise crítica | Evidências | Conduzir a entrevista; rastrear uma decisão da ata ao processo |
| Satisfação | Três perguntas | Validade estatística; o termo NPS |
| GUT, Pareto, 5W2H, PDCA, Indicadores | Sinais de uso de fachada, em parte | Como testar; recalcular um indicador da fonte |
| Ishikawa | Causas que não passam na auditoria | Julgar análises defeituosas |
| Histograma e CEP | Só o ponto de vista de quem usa | Trilha do plano de controle ao sinal anotado |
| Auditoria, Técnica, Certificação, Não conformidade | Programa, plano, amostra, evidência, ciclo do certificado, tratamento | Relatório, casos-limite de grau, o lado de quem audita na terceira parte, avaliação do plano de ação pelo auditor |

Achados gerais para as próximas levas:

- Quase todos os questionários pedem um rótulo por frase. Faltam exercícios de julgar evidência defeituosa, citar o requisito, classificar e redigir.
- Os exemplos são sempre bem-feitos. O auditor aprende com contraexemplos.
- Convenções do material aparecem no imperativo, e um iniciante tende a auditar contra o método, e não contra a norma. Faltam itens cuja resposta certa é "não é não conformidade".
- Temas sem estudo: relatório de auditoria, auditoria remota, situações difíceis, auditoria de segunda parte, o trabalho do auditor de terceira parte, liderança de equipe, carreira e qualificação.
- O painel se apresenta como "Ferramentas da qualidade na prática", com entrada por necessidade de quem implanta.
