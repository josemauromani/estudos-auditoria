# Autoteste das funções de coerencia.py
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coerencia as C

html = ('<style>p{}</style><p>A loja tem 29 estudos e o FR-07.</p><svg><text>x</text></svg>'
        '<p>RNC 2027-04 e registro 2027-14; lote 135.</p><script>var a=1;</script>')
t = C.extrair_texto(html)
assert 'p{}' not in t and 'var a' not in t and '[FIGURA]' in t
assert C.codigos_no_texto(t) == {'FR-07'}
assert C.registros_no_texto(t) == {'2027-04', '2027-14'}
assert C.contagens_de_estudos('Trinta e quatro estudos; os 29 estudos') == [34, 29]
regras = [{'id': 'D01', 'regex': r'\b29 estudos', 'motivo': 'a série tem 34', 'pastas': None},
          {'id': 'X', 'regex': r'FR-07', 'motivo': 'só no Escopo', 'pastas': ['Escopo']}]
assert [r[0] for r in C.achar_proibidos(t, regras, 'Caso-Integrado')] == ['D01']
q = "var KEYS = ['B','C'];\nvar ITEMS = [ { t: 'x', a: 'B', w: 'y' }, { t: 'z', a: 'Q', w: 'y' } ];"
assert C.questionarios('<script>' + q + '</script>') == ['Q']
print('autoteste OK')
import subprocess
_cli = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'coerencia.py')
r = subprocess.run([sys.executable, _cli, '--so', 'ZZ99'], capture_output=True, text=True)
assert r.returncode == 2 and 'ZZ99' in r.stdout, (r.returncode, r.stdout)
# o código de saída acompanha a contagem de falhas do id pedido, qualquer que seja o estado dos estudos
r = subprocess.run([sys.executable, _cli, '--so', 'D01'], capture_output=True, text=True)
_n = int(re.search(r'(\d+) falha', r.stdout).group(1))
assert r.returncode == (1 if _n else 0), (r.returncode, r.stdout)
print('--so OK')
