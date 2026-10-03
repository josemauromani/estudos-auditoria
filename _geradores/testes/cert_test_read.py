"""Lê os resultados dos testes de Certificacao-modelo.xlsx depois do recálculo.  Uso: cert_test_read.py <pasta com t1..t4.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import cert_data as R
from cert_data import (ATRASADA, CRITERIOS, EVENTOS, EX1, EX2, MAIOR, PLANOATR, VENCE, VENCIDA, AGUARDA, ct_conf, ct_sit, evento_sit, limites, prazo_fech,
                       prazo_plano, pront_conf, pront_res, resumo, validade)
PASTA = sys.argv[1]

# os casos de borda vêm do roteiro de preenchimento, sem regravar as cópias
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cert_test_make.py'), encoding='utf-8').read()
_ns = {}
exec(_src[_src.index('D = date'):_src.index("preencher('t3'")], {'date': __import__('datetime').date, **vars(R)}, _ns)
EX3 = dict(pront=dict(itens=_ns['itens3']), ciclo=_ns['ciclo3'], cts=_ns['cts3'])
EX4 = dict(pront=dict(itens=_ns['itens4']), ciclo=_ns['ciclo4'], cts=[])
PAINEL = {'Percentual atendido': 8, 'Impeditivos antes da fase 1': 9, 'Impeditivos antes da fase 2': 10, 'Resultado': 11, 'Validade': 14, 'Próximo limite': 15,
          'Próximo evento': 16, 'Eventos atrasados': 17, 'Eventos que vencem em 60 dias': 18, 'Constatações': 20, 'NC maiores': 21, 'NC maiores abertas': 22,
          'Planos atrasados': 23, 'NC maiores vencidas': 24, 'Aguardando verificação': 25, 'Linhas a completar': 26}


def v(c):
    x = c.value
    return '' if x is None else (x.date() if hasattr(x, 'date') else x)


def e(x):
    return '' if x is None else x


for nome, ex in (('t1', EX1), ('t2', EX2), ('t3', EX3), ('t4', EX4)):
    w = openpyxl.load_workbook(f'{PASTA}/{nome}.xlsx', data_only=True)
    P, C, T, Pa, K = w['Prontidão'], w['Ciclo'], w['Constatações'], w['Painel'], w['Checklist']
    c = ex['ciclo']
    print('=====', nome)
    err = [(ws.title, x.coordinate, x.value) for ws in w.worksheets[:5] for r in ws.iter_rows() for x in r
           if isinstance(x.value, str) and ((x.value.startswith('#') and len(x.value) > 1) or 'Err:' in x.value)]
    print('erros', err)
    res = pront_res(ex['pront']['itens'])
    got_p = [v(P[f'L{r}']) for r in range(7, 21)] + [round(v(P['E23']), 6), v(P['E24']), v(P['E25']), v(P['E26'])]
    esp_p = [pront_conf(k, i) for k, i in zip(CRITERIOS, ex['pront']['itens'])] + [round(res['pct'], 6), res['imp1'], res['imp2'], res['res']]
    got_v = [v(C['D9'])] + [(v(C[f'D{r}']), v(C[f'F{r}'])) for r in range(13, 20)]
    esp_v = [e(validade(c))] + [(e(l), evento_sit(c, k)) for k, l in enumerate(limites(c))]
    got_c = [(v(T[f'L{r}']), v(T[f'M{r}']), v(T[f'N{r}']), v(T[f'O{r}'])) for r in range(7, 7 + len(ex['cts']))]
    esp_c = [(e(prazo_plano(x)), e(prazo_fech(x)), ct_sit(x, c['ref']), ct_conf(x)) for x in ex['cts']]
    for rot, g, x in (('Prontidão', got_p, esp_p), ('Ciclo', got_v, esp_v), ('Constatações', got_c, esp_c)):
        print('%-13s' % rot, 'OK' if g == x else 'DIFERE\n   planilha %s\n   esperado %s' % (g, x))
    pa = {k: v(Pa[f'C{r}']) for k, r in PAINEL.items()}
    print('Painel       ', pa)
    print('Avisos       ', [P['E27'].value, C['E24'].value, T['E51'].value, Pa['C29'].value])
    # próximo limite: o menor limite de um evento ainda não feito
    pend = [(l, ev) for k, (l, ev) in enumerate(zip(limites(c), EVENTOS)) if l and not c['feito'][k] and k != 2]
    prox = min(pend) if pend else ('', '')
    print('Próximo      ', 'OK' if (pa['Próximo limite'], pa['Próximo evento']) == prox else 'DIFERE %s esperado %s' % ((pa['Próximo limite'], pa['Próximo evento']), prox))
    if nome in ('t1', 't2'):
        r = resumo(ex)
        sits = [evento_sit(c, k) for k in range(len(EVENTOS))]
        cs = [ct_sit(x, c['ref']) for x in ex['cts']]
        esp = {'Impeditivos antes da fase 1': r['imp1'], 'Impeditivos antes da fase 2': r['imp2'], 'Resultado': r['res'], 'Validade': r['validade'],
               'Eventos atrasados': sits.count(ATRASADA), 'Eventos que vencem em 60 dias': sits.count(VENCE), 'Constatações': r['cts'], 'NC maiores': r['tipos'][MAIOR],
               'NC maiores abertas': r['maiores_abertas'], 'Planos atrasados': cs.count(PLANOATR), 'NC maiores vencidas': cs.count(VENCIDA),
               'Aguardando verificação': cs.count(AGUARDA), 'Linhas a completar': r['pront_rever'] + r['ct_rever']}
        dif = {k: (pa[k], x) for k, x in esp.items() if pa[k] != x}
        print('              painel igual ao exemplo:', 'OK' if not dif else 'DIFERE %s' % dif)
    print('Checklist    ', [K[f'D{r}'].value for r in range(19, 25)])
