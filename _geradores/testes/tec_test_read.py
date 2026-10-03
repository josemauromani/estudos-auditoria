"""Lê os resultados dos testes de Tecnica-Auditoria-modelo.xlsx depois do recálculo.  Uso: tec_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import tec_data as R
from tec_data import (CONF, EX1, EX2, FORMACAO, FORTE, FRACA, INCOMP, ISOL, LIDERAR, EQUIPE, NC, REPET, SEMCORR, am_conf, am_sit, aud_conf, aud_conta, aud_nivel,
                      aud_pct, ev_conf, forca, passo, resumo, tamanho)
PASTA = sys.argv[1]

# os casos de borda vêm do roteiro de preenchimento, sem regravar as cópias
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tec_test_make.py'), encoding='utf-8').read()
_ns = {}
exec(_src[_src.index('AK = '):_src.index("preencher('t3'")], vars(R).copy(), _ns)
EX3 = dict(ams=_ns['ams3'], evs=_ns['evs3'], auds=_ns['auds3'])
PAINEL = {'Amostras': 7, 'Registros verificados': 8, 'Desvios': 9, 'Conforme na amostra': 10, 'Desvio isolado': 11, 'Desvio repetido': 12, 'Amostra incompleta': 13,
          'Perguntas': 15, 'Não conformidades': 16, 'Evidências fortes': 17, 'Evidências fracas': 18, 'Não conformidades sem corroboração': 19, 'Auditores avaliados': 21,
          'Apto a liderar': 22, 'Apto a auditar em equipe': 23, 'Em formação': 24, 'Linhas a completar': 25}


def v(c):
    """O openpyxl lê como None o texto vazio que a fórmula devolve."""
    return '' if c.value is None else c.value


def e(x):
    return '' if x is None else x


def r4(x):
    return round(x, 4) if isinstance(x, float) else x


for nome, ex in (('t1', EX1), ('t2', EX2), ('t3', EX3)):
    w = openpyxl.load_workbook(f'{PASTA}/{nome}.xlsx', data_only=True)
    A, E, U, Pa, K = w['Amostras'], w['Evidências'], w['Auditores'], w['Painel'], w['Checklist']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:5] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    got_a = [(v(A[f'I{r}']), v(A[f'J{r}']), v(A[f'N{r}']), v(A[f'O{r}'])) for r in range(12, 12 + len(ex['ams']))]
    esp_a = [(e(tamanho(a)), e(passo(a)), am_sit(a), am_conf(a)) for a in ex['ams']]
    got_e = [(v(E[f'J{r}']), v(E[f'K{r}'])) for r in range(7, 7 + len(ex['evs']))]
    esp_e = [(forca(x), ev_conf(x)) for x in ex['evs']]
    got_u = [tuple(r4(v(U[f'{chr(70 + k)}{21 + j}'])) for j in range(5)) for k in range(len(ex['auds']))]
    esp_u = [(aud_conta(a['notas'])[0], aud_conta(a['notas'])[1], r4(aud_pct(a['notas'])), aud_nivel(a['notas']), aud_conf(a['nome'], a['notas'])) for a in ex['auds']]
    for rot, g, x in (('Amostras', got_a, esp_a), ('Evidências', got_e, esp_e), ('Auditores', got_u, esp_u)):
        print('%-11s' % rot, 'OK' if g == x else 'DIFERE\n   planilha %s\n   esperado %s' % (g, x))
    pa = {k: Pa[f'C{r}'].value for k, r in PAINEL.items()}
    print('Painel     ', pa)
    print('Avisos     ', [A['E46'].value, E['E71'].value, U['F30'].value, Pa['C28'].value])
    if nome != 't3':
        r = resumo(ex)
        esp = {'Amostras': r['ams'], 'Registros verificados': r['verif'], 'Desvios': r['desv'], 'Conforme na amostra': r['sits'][CONF], 'Desvio isolado': r['sits'][ISOL],
               'Desvio repetido': r['sits'][REPET], 'Amostra incompleta': r['sits'][INCOMP], 'Perguntas': r['evs'], 'Não conformidades': r['consts'][NC],
               'Evidências fortes': r['forcas'][FORTE], 'Evidências fracas': r['forcas'][FRACA], 'Não conformidades sem corroboração': r['semcorr'], 'Auditores avaliados': r['auds'],
               'Apto a liderar': r['niveis'][LIDERAR], 'Apto a auditar em equipe': r['niveis'][EQUIPE], 'Em formação': r['niveis'][FORMACAO],
               'Linhas a completar': r['am_rever'] + r['ev_rever']}
        dif = {k: (pa[k], x) for k, x in esp.items() if pa[k] != x}
        print('             painel igual ao exemplo:', 'OK' if not dif else 'DIFERE %s' % dif)
    print('Checklist  ', [K[f'D{r}'].value for r in range(19, 25)])
