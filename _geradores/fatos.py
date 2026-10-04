# Ficha de fatos da série: o que é verdade nos exemplos de todos os estudos.
# É lida por testes/coerencia.py. Nasce com a estrutura e as regras iniciais.

def _org():
    return {'identidade': {}, 'pessoas': [], 'processos': [], 'equipamentos': [],
            'documentos': [], 'linha_do_tempo': [], 'numeros': []}

ORGS = {'pizzaria': _org(), 'industria': _org(), 'distribuidora': _org()}

# organização -> código -> significado
CODIGOS = {'pizzaria': {}, 'industria': {}, 'distribuidora': {}}

# códigos que existem de propósito em mais de uma organização
COMPARTILHADOS = set()

# prefixos de numeração corrida, que não são registrados um a um
SERIES_LIVRES = ()

# {'org', 'serie' ('RNC' ou 'PNC'), 'numero' ('aaaa-nn'), 'data' ('aaaa-mm-dd'), 'assunto', 'estudos'}
REGISTROS = []

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
DECISOES = []
