# Teste de coerência da série: lê o texto dos treinamentos e confere com _geradores/fatos.py.
#   coerencia.py                      roda tudo; sai com 1 se houver falha
#   coerencia.py --so T01,I03         só as regras de PROIBIDO com esses id
#   coerencia.py --extrair DEST       grava um .txt por HTML (raiz do repositório)
#   coerencia.py --extrair DEST --de ORIGEM   idem, com os *.html de ORIGEM
import glob, html as _html, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.dirname(AQUI))

UNIDADES = {'um': 1, 'uma': 1, 'dois': 2, 'duas': 2, 'três': 3, 'quatro': 4, 'cinco': 5, 'seis': 6,
            'sete': 7, 'oito': 8, 'nove': 9, 'dez': 10, 'onze': 11, 'doze': 12, 'treze': 13,
            'catorze': 14, 'quatorze': 14, 'quinze': 15, 'dezesseis': 16, 'dezessete': 17,
            'dezoito': 18, 'dezenove': 19}
DEZENAS = {'vinte': 20, 'trinta': 30, 'quarenta': 40, 'cinquenta': 50, 'sessenta': 60,
           'setenta': 70, 'oitenta': 80, 'noventa': 90}
_UN = '|'.join(sorted(UNIDADES, key=len, reverse=True))
_DZ = '|'.join(DEZENAS)
RE_ESTUDOS = re.compile(r'\b(?:(\d+)|((?:%s)(?: e (?:%s))?)|(%s))\s+estudos\b' % (_DZ, _UN, _UN),
                        re.IGNORECASE)


def extrair_texto(html):
    """Texto corrido de um HTML: sem estilo e script, figuras viram [FIGURA], entidades desfeitas."""
    t = re.sub(r'(?is)<(style|script)\b.*?</\1>', '', html)
    t = re.sub(r'(?is)<svg\b.*?</svg>', ' [FIGURA] ', t)
    t = re.sub(r'(?i)</(p|li|tr|h[1-6]|div|figcaption|caption|dt|dd)>|<br\s*/?>', '\n', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = _html.unescape(t)
    linhas = [re.sub(r'[ \t\xa0]+', ' ', l).strip() for l in t.split('\n')]
    return '\n'.join(l for l in linhas if l)


def achar_proibidos(texto, regras, pasta):
    """Devolve (id, trecho, motivo) de cada ocorrência de regra que vale para a pasta."""
    achados = []
    for r in regras:
        if r['pastas'] is not None and pasta not in r['pastas']:
            continue
        for m in re.finditer(r['regex'], texto):
            ini, fim = max(0, m.start() - 30), min(len(texto), m.end() + 30)
            achados.append((r['id'], texto[ini:fim].replace('\n', ' '), r['motivo']))
    return achados


def codigos_no_texto(texto):
    return set(re.findall(r'\b[A-Z]{2,4}(?:-[A-Z0-9]{1,4})?-\d{1,4}\b', texto))


def registros_no_texto(texto):
    return set(re.findall(r'(?:RNC |registro )(20\d\d-\d{2})', texto, re.IGNORECASE))


def _numero_por_extenso(s):
    return sum(DEZENAS.get(p, 0) + UNIDADES.get(p, 0) for p in s.lower().split(' e '))


def contagens_de_estudos(texto):
    """Números (em algarismos ou por extenso) que precedem a palavra 'estudos', na ordem do texto."""
    saida = []
    for m in RE_ESTUDOS.finditer(texto):
        if m.group(1):
            saida.append(int(m.group(1)))
        else:
            saida.append(_numero_por_extenso(m.group(2) or m.group(3)))
    return saida


def questionarios(html):
    """Respostas 'a' de ITEMS que não estão entre as opções do exercício (KEYS ou chaves de NAMES)."""
    m = re.search(r'var ITEMS = \[(.*?)\n?\s*\];', html, re.S)
    if not m:
        return []
    k = re.search(r'var KEYS = \[(.*?)\]', html, re.S)
    if k:
        opcoes = set(re.findall(r"'([^']*)'", k.group(1)))
    else:
        n = re.search(r'var NAMES = \{(.*?)\}', html, re.S)
        opcoes = set(re.findall(r"(\w+)\s*:", n.group(1))) if n else set()
    return [a for a in re.findall(r"\ba:\s*'([^']*)'", m.group(1)) if a not in opcoes]


def links_quebrados(caminho_html):
    """Links relativos (arquivo ou âncora) que não levam a nada."""
    with open(caminho_html, encoding='utf-8') as f:
        html = f.read()
    base = os.path.dirname(os.path.abspath(caminho_html))
    ids_cache = {}

    def ids(arq):
        if arq not in ids_cache:
            with open(arq, encoding='utf-8') as g:
                ids_cache[arq] = set(re.findall(r'\bid="([^"]*)"', g.read()))
        return ids_cache[arq]

    ruins = []
    for href in re.findall(r'<a\b[^>]*?\bhref="([^"]*)"', html):
        if re.match(r'(?i)(https?:|mailto:|tel:|data:|javascript:|//)', href) or not href:
            continue
        alvo, _, ancora = href.partition('#')
        arq = os.path.normpath(os.path.join(base, alvo)) if alvo else os.path.abspath(caminho_html)
        if not os.path.isfile(arq):
            ruins.append(href)
        elif ancora and arq.endswith('.html') and ancora not in ids(arq):
            ruins.append(href)
    return ruins


def _arquivos_da_raiz():
    """(pasta, caminho) dos treinamentos e do painel."""
    lista = [(os.path.basename(os.path.dirname(c)), c)
             for c in sorted(glob.glob(os.path.join(RAIZ, '*', 'treinamento-*.html')))]
    lista.append(('index', os.path.join(RAIZ, 'index.html')))
    return lista


def _ler(caminho):
    with open(caminho, encoding='utf-8') as f:
        return f.read()


def _extrair(dest, origem):
    os.makedirs(dest, exist_ok=True)
    if origem:
        arquivos = sorted(glob.glob(os.path.join(origem, '*.html')))
    else:
        arquivos = [c for _, c in _arquivos_da_raiz()]
    for c in arquivos:
        nome = os.path.splitext(os.path.basename(c))[0] + '.txt'
        with open(os.path.join(dest, nome), 'w', encoding='utf-8') as f:
            f.write(extrair_texto(_ler(c)) + '\n')
    print('%d arquivos gravados em %s' % (len(arquivos), dest))


def _conferir_registros(F, falhas):
    por_serie = {}
    for r in F.REGISTROS:
        por_serie.setdefault((r['org'], r['serie']), []).append(r)
    for (org, serie), lista in por_serie.items():
        lista = sorted(lista, key=lambda r: r['numero'])
        for a, b in zip(lista, lista[1:]):
            if b['data'] < a['data']:
                falhas.append(('fatos.py', '%s %s e %s' % (serie, a['numero'], b['numero']),
                               'ordem das datas: %s (%s) tem número menor e data posterior a %s (%s)'
                               % (a['numero'], a['data'], b['numero'], b['data'])))


def _rodar_tudo(F):
    falhas = []
    arquivos = _arquivos_da_raiz()
    painel = _ler(os.path.join(RAIZ, 'index.html'))
    total = len(re.findall(r'Abrir o treinamento', painel))
    todos = {c for org in F.CODIGOS.values() for c in org}
    donos = {}
    for org, cods in F.CODIGOS.items():
        for c in cods:
            donos.setdefault(c, []).append(org)
    for c, orgs in donos.items():
        if len(orgs) > 1 and c not in F.COMPARTILHADOS:
            falhas.append(('fatos.py', c, 'código em mais de uma organização (%s) e fora de COMPARTILHADOS'
                           % ', '.join(orgs)))
    registrados = {r['numero'] for r in F.REGISTROS}
    for pasta, caminho in arquivos:
        nome = os.path.relpath(caminho, RAIZ)
        html = _ler(caminho)
        texto = extrair_texto(html)
        for i, trecho, motivo in achar_proibidos(texto, F.PROIBIDO, pasta):
            falhas.append((nome, trecho, '%s: %s' % (i, motivo)))
        for c in sorted(codigos_no_texto(texto)):
            if c not in todos and c.split('-')[0] not in F.SERIES_LIVRES:
                falhas.append((nome, c, 'código não registrado em CODIGOS'))
        for n in sorted(registros_no_texto(texto)):
            if n not in registrados:
                falhas.append((nome, n, 'número de registro ausente de REGISTROS'))
        if pasta in ('index', 'Caso-Integrado'):
            for n in contagens_de_estudos(texto):
                if n >= 20 and n != total:
                    falhas.append((nome, '%d estudos' % n,
                                   'o painel tem %d links "Abrir o treinamento"' % total))
        for a in questionarios(html):
            falhas.append((nome, a, 'resposta do questionário fora das opções'))
        for h in links_quebrados(caminho):
            falhas.append((nome, h, 'link quebrado'))
    _conferir_registros(F, falhas)
    return falhas


def _so(F, ids):
    regras = [r for r in F.PROIBIDO if r['id'] in ids]
    falhas = []
    for pasta, caminho in _arquivos_da_raiz():
        for i, trecho, motivo in achar_proibidos(extrair_texto(_ler(caminho)), regras, pasta):
            falhas.append((os.path.relpath(caminho, RAIZ), trecho, '%s: %s' % (i, motivo)))
    return falhas


def main(argv):
    if '--extrair' in argv:
        dest = argv[argv.index('--extrair') + 1]
        origem = argv[argv.index('--de') + 1] if '--de' in argv else None
        _extrair(dest, origem)
        return 0
    import fatos as F
    if '--so' in argv:
        ids = set(argv[argv.index('--so') + 1].split(','))
        desconhecidos = ids - {r['id'] for r in F.PROIBIDO}
        if desconhecidos:
            print('id desconhecido em PROIBIDO: %s' % ', '.join(sorted(desconhecidos)))
            return 2
        falhas = _so(F, ids)
    else:
        falhas = _rodar_tudo(F)
    for arq, trecho, motivo in falhas:
        print('%s | %s | %s' % (arq, trecho, motivo))
    print('%d falha(s)' % len(falhas))
    return 1 if falhas else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
