# Autoteste das funções de coerencia.py
import os, sys
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
svg = ('<p>Texto corrido.</p><figure><svg viewBox="0 0 9 9" role="img" aria-label="Rótulo &amp; figura">'
       '<text x="1">A proposta do</text><text x="1"><tspan>medidor</tspan> esperou</text><text>12 itens<title>lista inteira</title></text></svg></figure>')
f = C.texto_das_figuras(svg)
assert f.split('\n') == ['Rótulo & figura', 'lista inteira', 'A proposta do medidor esperou 12 itens'], f
assert '[FIGURA]' in C.extrair_texto(svg) and 'medidor' not in C.extrair_texto(svg)
so_figura = [{'id': 'F1', 'regex': r'proposta do medidor esperou', 'motivo': 'só na figura', 'pastas': None}]
assert C.achar_proibidos(C.extrair_texto(svg), so_figura, 'X') == []
assert [r[0] for r in C.achar_proibidos(C.texto_para_proibidos(svg), so_figura, 'X')] == ['F1']
print('autoteste OK')

# --so pelo caminho real de main(), com regras temporárias em fatos.PROIBIDO, restauradas no fim
import contextlib, io
import fatos as F
_original = list(F.PROIBIDO)
F.PROIBIDO.extend([{'id': 'ZZ-SIM', 'regex': r'Abrir o treinamento', 'motivo': 'teste: sempre presente no painel', 'pastas': ['index']},
                   {'id': 'ZZ-NAO', 'regex': r'(?!x)x', 'motivo': 'teste: nunca casa', 'pastas': None}])
try:
    for ids, esperado in (('ZZ-SIM', 1), ('ZZ-NAO', 0), ('ZZ-SIM,ZZ-NAO', 1), ('ZZ99', 2), ('ZZ-NAO,ZZ99', 2)):
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            r = C.main(['--so', ids])
        assert r == esperado, (ids, r, saida.getvalue()[-300:])
        if ids == 'ZZ-SIM':
            assert 'ZZ-SIM:' in saida.getvalue() and 'ZZ-NAO' not in saida.getvalue()
finally:
    F.PROIBIDO[:] = _original
assert all(not r['id'].startswith('ZZ-') for r in F.PROIBIDO)
print('--so OK')
