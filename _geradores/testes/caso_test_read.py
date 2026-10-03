"""Lê os resultados dos testes de Caso-Integrado-modelo.xlsx depois do recálculo.  Uso: caso_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from caso_data import ATRASO, EX1, EX2, cal_conf, cal_conta, cal_sit, rastro_conf, rastro_dias, resumo
PASTA = sys.argv[1]

# os casos de borda vêm do roteiro de preenchimento, sem regravar as cópias
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'caso_test_make.py'), encoding='utf-8').read()
_ns = {}
exec(_src[_src.index('D = date'):_src.index("preencher('t3'")], {'date': __import__('datetime').date}, _ns)
EX3 = dict(head=dict(ref=_ns['REF3']), passos=[dict(zip(("data", "estudo", "oque", "reg", "saida", "prox"), p)) for p in _ns['passos3']],
           cal=[dict(zip(("ativ", "estudo", "req", "resp", "freq", "inicio"), a[:6]), feito=set(a[6])) for a in _ns['cal3']])
PAINEL = {'Passos': 7, 'Estudos diferentes': 8, 'Dias do primeiro ao último passo': 9, 'Maior intervalo entre passos': 10, 'Passos a completar': 11, 'Mês da leitura': 13,
          'Atividades': 14, 'Previstas até o mês': 15, 'Feitas': 16, 'Cumprimento': 17, 'Atrasadas': 18, 'Atividades com atraso': 19, 'Feitas fora do plano': 20,
          'Atividades a completar': 21}


def v(c):
    """O openpyxl lê como None o texto vazio que a fórmula devolve."""
    return '' if c.value is None else c.value


def e(x):
    return '' if x is None else x


for nome, ex in (('t1', EX1), ('t2', EX2), ('t3', EX3)):
    w = openpyxl.load_workbook(f'{PASTA}/{nome}.xlsx', data_only=True)
    R, C, Pa, K = w['Rastro'], w['Calendário'], w['Painel'], w['Checklist']
    ref = ex['head']['ref']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:5] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    got_r = [(v(R[f'I{r}']), v(R[f'J{r}'])) for r in range(8, 8 + len(ex['passos']))]
    esp_r = [(e(d), c) for d, c in zip(rastro_dias(ex['passos']), rastro_conf(ex['passos']))]
    got_c = [tuple(v(C[f'{c}{r}']) for c in ('U', 'V', 'W', 'X', 'Y', 'Z')) for r in range(10, 10 + len(ex['cal']))]
    esp_c = []
    for a in ex['cal']:
        k = cal_conta(a, ref)
        valido = a['estudo'] is not None and a['freq'] and a['inicio'] and 1 <= a['inicio'] <= 12
        esp_c.append((k['prev'], k['feitos'], k['atras'], k['fora']) + (cal_sit(a, ref), cal_conf(a)) if valido else ('', '', '', '', '', cal_conf(a)))
    print('Rastro    ', 'OK' if got_r == esp_r else 'DIFERE\n   planilha %s\n   esperado %s' % (got_r, esp_r))
    print('Calendário', 'OK' if got_c == esp_c else 'DIFERE\n   planilha %s\n   esperado %s' % (got_c, esp_c))
    pa = {k: Pa[f'C{r}'].value for k, r in PAINEL.items()}
    print('Painel    ', pa)
    print('Avisos    ', [R['E42'].value, C['E55'].value, Pa['C24'].value])
    if nome != 't3':
        r = resumo(ex)
        esp = {'Passos': r['passos'], 'Estudos diferentes': r['estudos'], 'Dias do primeiro ao último passo': r['total'], 'Maior intervalo entre passos': r['maior'],
               'Passos a completar': r['ras_rever'], 'Mês da leitura': ref, 'Atividades': r['ativ'], 'Previstas até o mês': r['prev'], 'Feitas': r['feitos'],
               'Cumprimento': r['cumpr'], 'Atrasadas': r['atras'], 'Atividades com atraso': r['sits'][ATRASO], 'Feitas fora do plano': r['fora'],
               'Atividades a completar': r['cal_rever']}
        dif = {k: (pa[k], x) for k, x in esp.items() if (round(pa[k], 6) if isinstance(pa[k], float) else pa[k]) != (round(x, 6) if isinstance(x, float) else x)}
        print('            painel igual ao exemplo:', 'OK' if not dif else 'DIFERE %s' % dif)
    print('Checklist ', [K[f'D{r}'].value for r in range(19, 25)])
