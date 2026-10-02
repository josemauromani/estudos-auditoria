# -*- coding: utf-8 -*-
"""Dados do estudo ISO 9001 requisito a requisito, usados pelo HTML e pela planilha.

Os resumos dos requisitos foram escritos com palavras próprias, a partir da estrutura da ISO 9001:2015.
Eles não reproduzem o texto da norma.
"""
from datetime import date

D = date
A, P, N = "Atende", "Atende em parte", "Não atende"
PONTOS = {A: 1.0, P: 0.5, N: 0.0}

SECOES = [
    (4, "Contexto da organização", "Onde estamos, quem depende de nós e até onde o sistema vai?"),
    (5, "Liderança", "Quem conduz, com que compromisso e com que papéis?"),
    (6, "Planejamento", "O que pode dar errado, aonde queremos chegar e como mudar?"),
    (7, "Apoio", "Que recursos, pessoas, conhecimento e documentos sustentam o trabalho?"),
    (8, "Operação", "Como o pedido do cliente vira produto ou serviço entregue?"),
    (9, "Avaliação de desempenho", "Como sabemos se está funcionando?"),
    (10, "Melhoria", "O que fazemos com o que descobrimos?"),
]
FASE = {4: "base", 5: "base", 6: "p", 7: "d", 8: "d", 9: "c", 10: "a"}

# estudos da série: chave -> (nome, caminho a partir da pasta do estudo)
ESTUDOS = {
    "swot": ("Matriz SWOT", "../SWOT/treinamento-swot.html"),
    "proc": ("Mapa de processos e tartaruga", "../Processos/treinamento-processos.html"),
    "sipoc": ("SIPOC", "../SIPOC/treinamento-sipoc.html"),
    "raci": ("Matriz RACI", "../RACI/treinamento-raci.html"),
    "riscos": ("Matriz de riscos", "../Riscos/treinamento-riscos.html"),
    "ind": ("Indicadores", "../Indicadores/treinamento-indicadores.html"),
    "pdca": ("PDCA", "../PDCA/treinamento-pdca.html"),
    "gut": ("Matriz GUT", "../GUT/treinamento-gut.html"),
    "ishikawa": ("Diagrama de Ishikawa", "../Ishikawa/treinamento-ishikawa.html"),
    "w5h2": ("5W2H", "../5W2H/treinamento-5w2h.html"),
    "auditoria": ("Auditoria interna", "../Auditoria/treinamento-auditoria.html"),
    "nc": ("Não conformidade e ação corretiva", "../Nao-Conformidade/treinamento-nao-conformidade.html"),
    "ac": ("Análise crítica pela direção", "../Analise-Critica/treinamento-analise-critica.html"),
    "doc": ("Informação documentada", "../Informacao-Documentada/treinamento-informacao-documentada.html"),
    "comp": ("Matriz de competências", "../Competencias/treinamento-competencias.html"),
    "forn": ("Avaliação de fornecedores", "../Fornecedores/treinamento-fornecedores.html"),
    "sat": ("Satisfação do cliente", "../Satisfacao/treinamento-satisfacao.html"),
    "par": ("Pareto e folha de verificação", "../Pareto/treinamento-pareto.html"),
    "pi": ("Partes interessadas", "../Partes-Interessadas/treinamento-partes-interessadas.html"),
    "obj": ("Objetivos da qualidade", "../Objetivos/treinamento-objetivos.html"),
    "prod": ("Controle de produção e de serviço", "../Producao/treinamento-producao.html"),
    "lib": ("Liberação e produto não conforme", "../Liberacao/treinamento-liberacao.html"),
    "ped": ("Requisitos do cliente e análise de pedidos", "../Pedidos/treinamento-pedidos.html"),
    "proj": ("Projeto e desenvolvimento", "../Projeto/treinamento-projeto.html"),
    "esc": ("Escopo e liderança", "../Escopo/treinamento-escopo.html"),
    "cal": ("Calibração e recursos de medição", "../Calibracao/treinamento-calibracao.html"),
    "rec": ("Recursos, infraestrutura e ambiente", "../Recursos/treinamento-recursos.html"),
    "con": ("Conhecimento organizacional e pós-entrega", "../Conhecimento/treinamento-conhecimento.html"),
}


def _req(rows):
    keys = ("num", "titulo", "pede", "pergunta", "evid", "estudos")
    out = []
    for r in rows:
        d = dict(zip(keys, r))
        d["secao"] = int(d["num"].split(".")[0])
        out.append(d)
    return out


REQ = _req([
    # ------------------------------------------------------------ 4
    ("4.1", "Entendendo a organização e seu contexto",
     "Determinar as questões internas e externas que afetam o propósito, a direção estratégica e os resultados do sistema. Monitorar e analisar essas questões. A emenda de 2024 pede também que a organização determine se a mudança climática é uma questão pertinente.",
     "Que fatores, de dentro e de fora, mais afetam os resultados?",
     "Matriz SWOT, plano estratégico, atas de análise crítica.", ("swot",)),
    ("4.2", "Entendendo as necessidades e expectativas de partes interessadas",
     "Determinar as partes interessadas pertinentes ao sistema e os requisitos de cada uma. Monitorar e analisar essas informações.",
     "Quem é afetado pelo sistema, e o que cada um espera?",
     "Lista de partes interessadas, com requisitos. Contratos e requisitos legais.", ("pi", "swot")),
    ("4.3", "Determinando o escopo do sistema de gestão da qualidade",
     "Definir os limites e a aplicabilidade do sistema, considerando o contexto, as partes interessadas e os produtos e serviços. Justificar todo requisito considerado não aplicável.",
     "O que está dentro do sistema, e por que algum requisito não se aplica?",
     "Declaração de escopo, com produtos, serviços, locais e justificativas.", ("esc",)),
    ("4.4", "Sistema de gestão da qualidade e seus processos",
     "Determinar os processos necessários, com entradas, saídas, sequência, interação, critérios, recursos, responsáveis, riscos e oportunidades. Avaliar os processos e melhorá-los.",
     "Quais são os processos, como se ligam e como se sabe que funcionam?",
     "Mapa de processos, SIPOC, indicadores por processo.", ("proc", "sipoc")),
    # ------------------------------------------------------------ 5
    ("5.1.1", "Liderança e comprometimento: generalidades",
     "A alta direção deve demonstrar liderança: responder pela eficácia do sistema, assegurar política e objetivos compatíveis com a estratégia, integrar os requisitos aos processos do negócio, prover recursos e promover a melhoria.",
     "Como a direção participa do sistema, além de assinar documentos?",
     "Entrevista com a direção, atas, decisões sobre recursos.", ("esc",)),
    ("5.1.2", "Foco no cliente",
     "A alta direção deve assegurar que os requisitos do cliente e os legais sejam determinados e atendidos, que os riscos para a conformidade sejam tratados e que o foco na satisfação do cliente seja mantido.",
     "Como a direção acompanha o que o cliente pede e o que ele recebe?",
     "Indicadores de satisfação e de reclamações na pauta da direção.", ("sat",)),
    ("5.2", "Política",
     "Estabelecer uma política da qualidade apropriada ao propósito e ao contexto, que sirva de base para os objetivos e inclua os compromissos de atender a requisitos e de melhorar. Comunicar a política e mantê-la disponível.",
     "O que a política diz, e como as pessoas a aplicam no trabalho?",
     "Política documentada, divulgação, entrevistas com a equipe.", ("obj",)),
    ("5.3", "Papéis, responsabilidades e autoridades organizacionais",
     "Atribuir, comunicar e fazer entender as responsabilidades e as autoridades, inclusive pela conformidade do sistema, pelo relato do desempenho e pela integridade do sistema durante as mudanças.",
     "Quem responde por quê, e quem pode decidir?",
     "Organograma, descrições de cargo, Matriz RACI.", ("raci",)),
    # ------------------------------------------------------------ 6
    ("6.1", "Ações para abordar riscos e oportunidades",
     "Determinar os riscos e as oportunidades a partir do contexto e das partes interessadas. Planejar ações para abordá-los, integrá-las aos processos e avaliar a eficácia delas. As ações devem ser proporcionais ao impacto.",
     "O que pode dar errado, o que pode ser aproveitado, e o que foi feito?",
     "Matriz de riscos, ações ligadas à SWOT, avaliação da eficácia.", ("riscos", "swot", "gut")),
    ("6.2", "Objetivos da qualidade e planejamento para alcançá-los",
     "Estabelecer objetivos mensuráveis, coerentes com a política, monitorados e comunicados. Para cada objetivo, definir o que será feito, os recursos, o responsável, o prazo e a forma de avaliar o resultado.",
     "Quais são os objetivos, e qual é o plano para cada um?",
     "Objetivos com indicador e meta. Planos de ação.", ("obj", "ind", "w5h2")),
    ("6.3", "Planejamento de mudanças",
     "Realizar as mudanças no sistema de forma planejada, considerando o propósito, as consequências, a integridade do sistema, os recursos e as responsabilidades.",
     "Como foi planejada a última mudança importante?",
     "Planos de mudança, análise de impacto, comunicações.", ("riscos", "w5h2")),
    # ------------------------------------------------------------ 7
    ("7.1.1", "Recursos: generalidades e pessoas (7.1.1 e 7.1.2)",
     "Determinar e prover os recursos necessários, considerando o que existe internamente e o que precisa vir de fora. Determinar e prover as pessoas necessárias para operar o sistema e os processos.",
     "Os recursos e as pessoas são suficientes para o que foi planejado?",
     "Orçamento, quadro de pessoal, escalas de trabalho.", ("rec",)),
    ("7.1.3", "Infraestrutura",
     "Determinar, prover e manter a infraestrutura necessária: edifícios, equipamentos, software, transporte e tecnologia da informação.",
     "Como os equipamentos e os sistemas são mantidos?",
     "Plano e registros de manutenção, cópias de segurança.", ("rec",)),
    ("7.1.4", "Ambiente para a operação dos processos",
     "Determinar, prover e manter o ambiente necessário, com os fatores físicos, sociais e psicológicos que afetam a conformidade.",
     "Que condições do ambiente afetam o produto ou o serviço?",
     "Controles de temperatura, limpeza, ruído e carga de trabalho.", ("rec",)),
    ("7.1.5", "Recursos de monitoramento e medição",
     "Assegurar que os recursos usados para medir e monitorar sejam adequados e mantidos. Quando a rastreabilidade da medição for requisito, calibrar ou verificar os instrumentos, identificá-los e protegê-los.",
     "Como se sabe que os instrumentos medem certo?",
     "Lista de instrumentos, certificados de calibração, identificação da situação.", ("cal",)),
    ("7.1.6", "Conhecimento organizacional",
     "Determinar o conhecimento necessário para operar os processos, mantê-lo e torná-lo disponível. Diante de mudanças, avaliar como obter o conhecimento que falta.",
     "O que acontece se a pessoa que sabe fazer sair da organização?",
     "Instruções, lições aprendidas, treinamento no posto de trabalho.", ("con",)),
    ("7.2", "Competência",
     "Determinar a competência necessária das pessoas que afetam o desempenho do sistema, assegurar que elas sejam competentes, agir para obter a competência que falta e avaliar a eficácia dessas ações.",
     "Que competência o cargo exige, e como se sabe que a pessoa a tem?",
     "Descrição de cargo, matriz de competências, registros de treinamento.", ("comp",)),
    ("7.3", "Conscientização",
     "Assegurar que as pessoas conheçam a política, os objetivos pertinentes, a sua contribuição para o sistema e as consequências de não atender aos requisitos.",
     "Para quem executa: como o seu trabalho afeta o cliente?",
     "Entrevistas com as pessoas, integração, comunicação interna.", ("comp",)),
    ("7.4", "Comunicação",
     "Determinar as comunicações internas e externas pertinentes ao sistema: o que comunicar, quando, a quem, como e quem comunica.",
     "Como as informações importantes chegam a quem precisa?",
     "Plano de comunicação, murais, reuniões, canais com o cliente.", ("raci",)),
    ("7.5", "Informação documentada",
     "Manter a informação documentada exigida pela norma e a que a organização considera necessária. Ao criar e atualizar, cuidar da identificação, do formato e da aprovação. Controlar a distribuição, o acesso, o armazenamento, as alterações e o descarte.",
     "Como se sabe que o documento em uso é a versão válida?",
     "Lista de documentos, controle de revisão, regras de retenção.", ("doc",)),
    # ------------------------------------------------------------ 8
    ("8.1", "Planejamento e controle operacionais",
     "Planejar, implementar e controlar os processos necessários para atender aos requisitos: determinar os requisitos, os critérios dos processos e de aceitação, os recursos e os controles. Controlar as mudanças planejadas e os processos terceirizados.",
     "Como a operação é planejada e controlada?",
     "Planos de produção, instruções, critérios de aceitação.", ("sipoc",)),
    ("8.2.1", "Comunicação com o cliente",
     "Comunicar-se com o cliente sobre produtos e serviços, consultas, contratos e pedidos, retorno e reclamações, propriedade do cliente e ações de contingência.",
     "Por onde o cliente pergunta, pede e reclama?",
     "Canais de atendimento, registros de reclamação.", ("sat", "ped")),
    ("8.2.2", "Determinação de requisitos relativos a produtos e serviços",
     "Assegurar que os requisitos dos produtos e serviços estejam definidos, inclusive os legais e os que a organização considera necessários, e que a organização possa cumprir o que oferece.",
     "Onde estão definidos os requisitos do que é oferecido?",
     "Especificações, catálogo, requisitos legais aplicáveis.", ("ped",)),
    ("8.2.3", "Análise crítica de requisitos relativos a produtos e serviços",
     "Antes de se comprometer a fornecer, analisar os requisitos declarados pelo cliente, os não declarados mas necessários, os legais e as diferenças em relação ao que foi combinado antes.",
     "Como se confirma, antes de aceitar o pedido, que é possível atendê-lo?",
     "Análise de pedidos e de propostas, confirmação do pedido.", ("ped",)),
    ("8.2.4", "Mudanças nos requisitos para produtos e serviços",
     "Quando os requisitos mudam, alterar a informação documentada pertinente e avisar as pessoas envolvidas.",
     "O que acontece quando o cliente muda o pedido?",
     "Alterações de pedido registradas e comunicadas.", ("ped",)),
    ("8.3", "Projeto e desenvolvimento de produtos e serviços",
     "Estabelecer um processo de projeto e desenvolvimento com planejamento, entradas, controles, saídas e mudanças. Os controles incluem análises críticas, verificação e validação.",
     "Como uma ideia vira produto ou serviço, e como se confirma que ele funciona?",
     "Plano de projeto, requisitos de entrada, registros de verificação e de validação.", ("proj",)),
    ("8.4.1", "Provedores externos: generalidades",
     "Assegurar que processos, produtos e serviços providos externamente atendam aos requisitos. Determinar e aplicar critérios para avaliar, selecionar, monitorar o desempenho e reavaliar os provedores externos.",
     "Como os fornecedores são escolhidos e acompanhados?",
     "Critérios de homologação, avaliações de desempenho, lista de fornecedores aprovados.", ("forn",)),
    ("8.4.2", "Provedores externos: tipo e extensão do controle",
     "Definir os controles sobre o provedor externo e sobre o que ele entrega, de acordo com o impacto na capacidade de atender ao cliente. Definir a verificação necessária para assegurar que o item recebido atende aos requisitos.",
     "O que é conferido no recebimento, e por que esse nível de controle?",
     "Inspeção de recebimento, auditorias em fornecedores.", ("forn",)),
    ("8.4.3", "Provedores externos: informação",
     "Comunicar ao provedor externo os requisitos do que será fornecido, os critérios de aprovação, a competência exigida e os controles que serão aplicados. Assegurar que os requisitos estejam adequados antes de comunicá-los.",
     "O pedido de compra diz tudo o que o fornecedor precisa saber?",
     "Pedidos de compra, contratos, especificações técnicas.", ("forn",)),
    ("8.5.1", "Controle de produção e de provisão de serviço",
     "Produzir e prestar o serviço sob condições controladas: informação sobre o que fazer e o resultado esperado, recursos de medição, monitoramento, infraestrutura, pessoas competentes, validação de processos, prevenção de erro humano e atividades de liberação e de entrega.",
     "Como quem executa sabe o que fazer, e como sabe que ficou certo?",
     "Instruções de trabalho, registros de controle do processo.", ("prod",)),
    ("8.5.2", "Identificação e rastreabilidade",
     "Identificar as saídas e a situação delas em relação às verificações. Quando a rastreabilidade for requisito, controlar a identificação única de cada saída.",
     "É possível saber de que lote veio este item e se ele já foi aprovado?",
     "Etiquetas, números de lote, registros de rastreabilidade.", ("prod",)),
    ("8.5.3", "Propriedade pertencente a clientes ou provedores externos",
     "Cuidar da propriedade de clientes e de provedores externos enquanto estiver sob controle da organização: identificar, verificar e proteger. Se for perdida ou danificada, relatar ao dono.",
     "O que do cliente está sob os cuidados da organização?",
     "Controle de materiais, ferramentas e dados do cliente.", ("prod",)),
    ("8.5.4", "Preservação",
     "Preservar as saídas durante a produção e a provisão do serviço, para assegurar a conformidade: identificação, manuseio, embalagem, armazenamento, transporte e proteção.",
     "Como o produto é protegido até chegar ao cliente?",
     "Condições de armazenagem, embalagem, validade, transporte.", ("prod",)),
    ("8.5.5", "Atividades pós-entrega",
     "Atender aos requisitos das atividades pós-entrega, considerando os requisitos legais, as consequências indesejadas, a vida útil, os requisitos do cliente e o retorno recebido.",
     "O que a organização faz depois da entrega?",
     "Garantia, assistência técnica, atendimento a reclamações.", ("con",)),
    ("8.5.6", "Controle de mudanças",
     "Analisar e controlar as mudanças na produção ou na provisão do serviço, para manter a conformidade. Registrar o resultado da análise, quem autorizou e as ações necessárias.",
     "Quem autoriza uma mudança no processo, e onde isso fica registrado?",
     "Registros de mudança de processo, autorizações.", ("prod",)),
    ("8.6", "Liberação de produtos e serviços",
     "Verificar, nas etapas planejadas, se os requisitos foram atendidos. Só liberar ao cliente depois das verificações, salvo aprovação de autoridade pertinente. Registrar a conformidade e quem autorizou a liberação.",
     "Quem libera o produto, e com base em quê?",
     "Registros de inspeção final, com a identificação de quem liberou.", ("lib",)),
    ("8.7", "Controle de saídas não conformes",
     "Identificar e controlar as saídas não conformes, para evitar o uso ou a entrega. Agir conforme a natureza da falha: corrigir, separar, devolver, informar o cliente ou obter concessão. Verificar de novo depois da correção.",
     "O que acontece com o produto reprovado?",
     "Área de segregação, registros de produto não conforme, concessões.", ("lib", "nc")),
    # ------------------------------------------------------------ 9
    ("9.1.1", "Monitoramento, medição, análise e avaliação: generalidades",
     "Determinar o que medir e monitorar, os métodos, quando medir e quando analisar os resultados. Avaliar o desempenho e a eficácia do sistema.",
     "Quais são os indicadores, e quem os analisa?",
     "Painel de indicadores, com método e frequência.", ("ind", "pdca")),
    ("9.1.2", "Satisfação do cliente",
     "Monitorar a percepção do cliente sobre o grau em que as suas necessidades e expectativas foram atendidas. Determinar os métodos para obter e usar essa informação.",
     "Como se sabe se o cliente está satisfeito?",
     "Pesquisas, reclamações, elogios, recompra, devoluções.", ("sat", "ind")),
    ("9.1.3", "Análise e avaliação",
     "Analisar os dados para avaliar a conformidade de produtos e serviços, a satisfação do cliente, o desempenho do sistema, a eficácia do planejamento e das ações sobre riscos, o desempenho de provedores externos e as necessidades de melhoria.",
     "Que decisões foram tomadas a partir dos dados?",
     "Relatórios de análise, gráficos, atas com decisões.", ("ind", "par", "gut", "ishikawa")),
    ("9.2", "Auditoria interna",
     "Conduzir auditorias internas a intervalos planejados, com programa, critérios e escopo definidos, auditores imparciais, resultados relatados à gestão e ações sem demora indevida.",
     "O programa cobre todo o sistema, e o que foi feito com as constatações?",
     "Programa, planos, relatórios de auditoria e ações.", ("auditoria",)),
    ("9.3", "Análise crítica pela direção",
     "A alta direção deve analisar o sistema a intervalos planejados, considerando as entradas definidas pela norma: ações anteriores, mudanças, desempenho, recursos, riscos e oportunidades de melhoria. As saídas são decisões sobre melhoria, mudanças e recursos.",
     "O que a direção decidiu na última análise crítica?",
     "Ata da análise crítica, com entradas, decisões e responsáveis.", ("ac",)),
    # ------------------------------------------------------------ 10
    ("10.1", "Melhoria: generalidades",
     "Determinar e selecionar oportunidades de melhoria e implementar ações para atender aos requisitos do cliente e aumentar a satisfação: melhorar produtos e serviços, corrigir e prevenir efeitos indesejados e melhorar o sistema.",
     "Que melhorias foram feitas no último ano?",
     "Projetos de melhoria, ciclos PDCA concluídos.", ("pdca",)),
    ("10.2", "Não conformidade e ação corretiva",
     "Diante de uma não conformidade, reagir, avaliar a necessidade de eliminar a causa, implementar a ação, analisar a eficácia e atualizar os riscos e o sistema, se necessário.",
     "Como uma falha é tratada, do registro à verificação da eficácia?",
     "Registros de não conformidade, análise de causa, verificação da eficácia.", ("nc", "ishikawa", "w5h2")),
    ("10.3", "Melhoria contínua",
     "Melhorar continuamente a adequação, a suficiência e a eficácia do sistema, considerando os resultados da análise e avaliação e as saídas da análise crítica pela direção.",
     "Como os resultados viram melhoria?",
     "Evolução dos indicadores, ações derivadas da análise crítica.", ("pdca",)),
])
NUMS = [r["num"] for r in REQ]
assert len(REQ) == 45 and len(set(NUMS)) == 45

# informação documentada exigida: (requisito, tipo, o que precisa existir, exemplo)
MANTER, RETER = "Manter", "Reter"
DOCS = [
    ("4.3", MANTER, "Escopo do sistema de gestão da qualidade", "Declaração de escopo"),
    ("4.4", MANTER, "Informação para apoiar a operação dos processos, na extensão necessária", "Mapa de processos, procedimentos"),
    ("4.4", RETER, "Evidência de que os processos são realizados conforme o planejado", "Registros dos processos"),
    ("5.2", MANTER, "Política da qualidade", "Política aprovada pela direção"),
    ("6.2", MANTER, "Objetivos da qualidade", "Quadro de objetivos e metas"),
    ("7.1.5", RETER, "Evidência de que os recursos de monitoramento e medição são adequados", "Certificados de calibração"),
    ("7.1.5", RETER, "Base usada para calibrar ou verificar, quando não existe padrão de medição", "Registro do método de verificação"),
    ("7.2", RETER, "Evidência de competência", "Registros de formação e de treinamento"),
    ("7.5", MANTER, "Informação que a organização considera necessária para a eficácia do sistema", "Instruções e formulários próprios"),
    ("8.1", MANTER + " e reter", "Informação para ter confiança de que os processos foram realizados conforme o planejado e para demonstrar a conformidade", "Planos e registros de produção"),
    ("8.2.3", RETER, "Resultados da análise crítica dos requisitos e novos requisitos de produtos e serviços", "Pedido confirmado, análise de proposta"),
    ("8.3", RETER, "Planejamento, entradas, controles, saídas e mudanças de projeto e desenvolvimento", "Pasta do projeto"),
    ("8.4.1", RETER, "Avaliação, seleção, monitoramento e reavaliação de provedores externos", "Avaliação de fornecedores"),
    ("8.5.1", MANTER, "Características dos produtos e serviços, atividades a desempenhar e resultados a alcançar", "Especificações e instruções de trabalho"),
    ("8.5.2", RETER, "Identificação necessária para a rastreabilidade, quando ela for requisito", "Registro de lotes"),
    ("8.5.3", RETER, "Ocorrências com propriedade de cliente ou de provedor externo: perda, dano ou inadequação", "Comunicação ao cliente"),
    ("8.5.6", RETER, "Resultados da análise crítica de mudanças, quem autorizou e ações necessárias", "Registro de mudança de processo"),
    ("8.6", RETER, "Evidência da conformidade com os critérios de aceitação e de quem autorizou a liberação", "Registro de inspeção final"),
    ("8.7", RETER, "Não conformidade, ações tomadas, concessões e autoridade que decidiu", "Registro de produto não conforme"),
    ("9.1.1", RETER, "Resultados do monitoramento e da medição", "Indicadores e relatórios"),
    ("9.2", RETER, "Implementação do programa de auditoria e resultados das auditorias", "Programa e relatórios de auditoria"),
    ("9.3", RETER, "Resultados das análises críticas pela direção", "Ata da análise crítica"),
    ("10.2", RETER, "Natureza das não conformidades, ações tomadas e resultados das ações corretivas", "Registros de não conformidade"),
]
assert all(d[0] in NUMS for d in DOCS)

# ------------------------------------------------------------ exemplo 1: diagnóstico da pizzaria
EX1 = {
    "head": dict(org="Pizzaria (loja com salão e delivery)", data=D(2026, 10, 2), por="Gerente da loja, com apoio do atendente líder",
                 escopo="Produção e entrega de pizzas, no salão e por delivery.",
                 criterio="ISO 9001:2015, seções 4 a 10.",
                 metodo="Entrevistas, observação de dois turnos e leitura dos registros de julho a setembro."),
    "itens": {
        "4.1": (P, "Matriz SWOT feita em 2026.", "Definir quando a análise será revista."),
        "4.2": (P, "Clientes e vigilância sanitária considerados na SWOT.", "Incluir entregadores e fornecedores, com o que cada um espera."),
        "4.3": (N, "Não há escopo escrito.", "Escrever o escopo: produtos, loja, canais de venda e requisitos não aplicáveis."),
        "4.4": (P, "SIPOC e indicadores do processo de delivery.", "Mapear compras, produção e atendimento no salão."),
        "5.1.1": (A, "O dono conduz a reunião semanal de indicadores e decide sobre recursos.", ""),
        "5.1.2": (A, "Reclamações e entregas no prazo são lidas toda semana pelo dono.", ""),
        "5.2": (N, "Não há política da qualidade.", "Escrever a política e apresentá-la à equipe."),
        "5.3": (A, "Matriz RACI do delivery e escala com o responsável de cada turno.", ""),
        "6.1": (P, "Ameaças e oportunidades listadas na SWOT.", "Definir ações para os riscos priorizados e avaliar o resultado."),
        "6.2": (P, "Objetivo de entregas em até 40 minutos, com meta de 95% e plano.", "Definir objetivos e planos para reclamações e desperdício."),
        "6.3": (N, "O sistema de pedidos foi trocado sem teste e sem treinamento.", "Criar uma rotina simples para planejar mudanças."),
        "7.1.1": (A, "Escala padrão, com dois entregadores extras nas noites de pico.", ""),
        "7.1.3": (A, "Forno, motos e câmara fria com manutenção programada.", ""),
        "7.1.4": (A, "Rotina de limpeza e de controle de temperatura da cozinha.", ""),
        "7.1.5": (P, "Balança verificada todo mês.", "Verificar o termômetro da câmara fria e registrar."),
        "7.1.6": (P, "Receitas e instrução da expedição escritas.", "Registrar a regulagem do forno, conhecida só pelo pizzaiolo líder."),
        "7.2": (P, "Lista de presença do treinamento de julho.", "Definir e registrar o treinamento de quem entra depois."),
        "7.3": (P, "A equipe conhece a meta de entrega.", "Apresentar a política e os objetivos, quando existirem."),
        "7.4": (A, "Reunião semanal, quadro de avisos e grupo de mensagens.", ""),
        "7.5": (P, "Instruções com número de revisão.", "Controlar também os roteiros e os formulários."),
        "8.1": (A, "Instrução IT-EXP-01, escala padrão e rotina de temperatura.", ""),
        "8.2.1": (A, "Cardápio, site, aplicativo, telefone e canal de reclamações.", ""),
        "8.2.2": (A, "Cardápio com ingredientes, alergênicos e prazo de entrega por região.", ""),
        "8.2.3": (P, "Pedido confirmado com o cliente no site e no aplicativo.", "Pedidos por telefone ficam sem o complemento do endereço (RNC 2026-05, em tratamento)."),
        "8.2.4": (A, "Alteração de pedido registrada no sistema e avisada à cozinha.", ""),
        "8.3": (P, "Sabores novos são testados com a equipe antes de entrar no cardápio.", "Registrar a receita aprovada e o resultado do teste."),
        "8.4.1": (P, "Fornecedores fixos, escolhidos por preço e prazo.", "Escrever os critérios de escolha e avaliar o desempenho."),
        "8.4.2": (A, "Conferência de validade, temperatura e quantidade no recebimento.", ""),
        "8.4.3": (A, "Pedido ao fornecedor por escrito, com marca, quantidade e data.", ""),
        "8.5.1": (A, "Receitas e instruções no posto de trabalho. Pedido conferido antes de embalar.", ""),
        "8.5.2": (A, "Etiqueta com o número do pedido. Insumos com data de validade.", ""),
        "8.5.3": (P, "Dados do cliente protegidos por senha no sistema.", "Definir o descarte das listas de entrega impressas."),
        "8.5.4": (A, "Bolsa térmica, embalagem lacrada e tempo máximo de espera.", ""),
        "8.5.5": (A, "Reclamação atendida com reposição ou desconto.", ""),
        "8.5.6": (N, "Mudanças de receita e de método não são registradas.", "Registrar a mudança, quem autorizou e o que foi conferido."),
        "8.6": (A, "Etiqueta rubricada por quem conferiu o pedido.", ""),
        "8.7": (P, "A pizza errada é refeita antes da saída.", "Registrar a ocorrência e o que foi feito."),
        "9.1.1": (A, "Indicador semanal de entregas no prazo, por faixa de horário.", ""),
        "9.1.2": (P, "Reclamações contadas por semana.", "Medir a satisfação, e não só a reclamação."),
        "9.1.3": (P, "Dados de entrega analisados na reunião semanal.", "Analisar também as reclamações e os fornecedores."),
        "9.2": (P, "Auditoria 2026-03, do processo de delivery.", "Montar o programa anual, com todos os processos."),
        "9.3": (N, "Não há análise crítica do sistema.", "Realizar a primeira análise crítica, com as entradas que a norma pede."),
        "10.1": (A, "Ciclo PDCA das entregas, concluído em 2026.", ""),
        "10.2": (P, "RNC 2026-05, com correção feita e causa analisada.", "Tratar também as reclamações com análise de causa."),
        "10.3": (A, "Entregas no prazo subiram de 82% para 95% e se mantêm.", ""),
    },
}
assert list(EX1["itens"]) == NUMS

# ------------------------------------------------------------ exemplo 2: requisitos ligados ao processo de compras
EX2 = {
    "head": dict(org="Indústria de embalagens plásticas · processo de aquisição", data=D(2026, 9, 25), por="Analista da Qualidade, com o gerente de Suprimentos",
                 escopo="Requisitos da norma ligados ao processo de adquirir materiais e serviços.",
                 criterio="ISO 9001:2015, requisito 8.4 e requisitos relacionados.",
                 metodo="Relatório da auditoria 2026-07, de 22/09/2026, e entrevista com a gerência."),
    "itens": {
        "4.4": (A, "SIPOC do processo de aquisição, com indicador de prazo de atendimento.", ""),
        "5.3": (A, "Matriz RACI e alçadas de aprovação na política de compras.", ""),
        "6.1": (P, "Risco de falta de material crítico identificado.", "Definir ação para os itens de fornecedor único."),
        "7.2": (A, "Compradores com treinamento registrado no PR-SUP-01 rev. 5.", ""),
        "7.5": (A, "PR-SUP-01 rev. 5 controlado e disponível no sistema.", ""),
        "8.4.1": (P, "Critérios de homologação aplicados nas 5 homologações de 2026.", "5 de 12 fornecedores críticos sem avaliação de desempenho em 2026 (auditoria 2026-07, constatação nº 2)."),
        "8.4.2": (A, "Itens conferidos antes da liberação, nos 10 recebimentos da amostra.", ""),
        "8.4.3": (P, "10 pedidos com especificação, quantidade, prazo e condição de aceitação.", "4 de 10 requisições chegam a Suprimentos sem especificação técnica (RNC 2026-31)."),
        "8.5.3": (A, "Paletes e embalagens retornáveis dos fornecedores com controle de saldo.", ""),
        "8.7": (A, "Item recebido com divergência é identificado, separado e devolvido.", ""),
        "9.1.3": (P, "Prazo de atendimento analisado todo mês.", "Analisar também o desempenho dos fornecedores."),
        "9.2": (A, "Auditoria 2026-07 realizada, com relatório distribuído.", ""),
        "10.2": (P, "RNC 2026-31 aberto, com a correção feita.", "Concluir a análise de causa e as ações corretivas."),
    },
}
assert all(k in NUMS for k in EX2["itens"])

CHECK = [
    "O escopo está escrito, com os limites do sistema e as não aplicabilidades justificadas.",
    "As questões internas e externas e as partes interessadas foram levantadas.",
    "Os processos estão identificados, com entradas, saídas, responsáveis e indicadores.",
    "A política e os objetivos da qualidade estão escritos e são conhecidos pela equipe.",
    "Os riscos e as oportunidades têm ações definidas.",
    "As competências necessárias estão definidas, e há evidência de que as pessoas as têm.",
    "Os documentos e os registros exigidos existem e estão controlados.",
    "Os requisitos do cliente são analisados antes do compromisso de fornecer.",
    "Os fornecedores são avaliados com critérios definidos.",
    "Os produtos e os serviços só são liberados depois das verificações planejadas.",
    "A auditoria interna cobriu todos os requisitos aplicáveis.",
    "A direção analisou criticamente o sistema, e as não conformidades têm ação corretiva.",
]


def resumo(itens):
    """Contagem por seção: {seção: [total, atende, em parte, não atende, percentual]}"""
    out = {}
    for s, _, _ in SECOES:
        v = [itens[r["num"]][0] for r in REQ if r["secao"] == s and r["num"] in itens]
        if v:
            pts = sum(PONTOS[x] for x in v)
            out[s] = [len(v), v.count(A), v.count(P), v.count(N), pts / len(v)]
    return out


def geral(itens):
    v = [x[0] for x in itens.values()]
    return len(v), v.count(A), v.count(P), v.count(N), sum(PONTOS[x] for x in v) / len(v)


if __name__ == "__main__":
    print("requisitos por seção:", {s: sum(1 for r in REQ if r["secao"] == s) for s, _, _ in SECOES})
    print("maior resumo:", max(len(r["pede"]) for r in REQ), "| documentos:", len(DOCS),
          {t: sum(1 for d in DOCS if d[1] == t) for t in sorted({d[1] for d in DOCS})})
    for nome, ex in (("EX1", EX1), ("EX2", EX2)):
        print(nome, geral(ex["itens"]), {k: (v[0], v[1], v[2], v[3], round(v[4] * 100)) for k, v in resumo(ex["itens"]).items()})
    print("lista de requisitos:", len(",".join(NUMS)), "caracteres")
