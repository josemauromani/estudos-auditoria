"""Lê os resultados dos testes de Escopo-modelo.xlsx depois do recálculo.  Uso: esc_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from esc_data import EX1, EX2, NAO, REQS, SIM, aplic_conf, aplicabilidade, escopo_conf, lider_conf, resumo
D = sys.argv[1]
# a aplicabilidade de t3, a mesma de esc_test_make.py, para conferir a coluna com a regra do Python
APLIC3 = {n: (SIM, '', '') for n, _ in REQS}
APLIC3.update({'4.3': ('', '', ''), '9.3': (NAO, 'O diretor acompanha tudo', NAO), '8.3': (NAO, '', ''), '8.5.3': (NAO, 'Nada do cliente', ''), '8.5.5': (NAO, 'Sem pós-entrega', SIM),
               '7.1.5': (NAO, 'Sem medição', NAO)})
for nome, ex in (('t1', EX1), ('t2', EX2), ('t3', None)):
    w = openpyxl.load_workbook(f'{D}/{nome}.xlsx', data_only=True)
    E, A, L, Pa, K = w['Escopo'], w['Aplicabilidade'], w['Liderança'], w['Painel'], w['Checklist']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:6] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    esc = [E[f'D{r}'].value for r in range(5, 13)]
    ap = [A[f'H{r}'].value for r in range(7, 7 + len(REQS))]
    li = [L[f'K{r}'].value for r in range(6, 16)]
    print('Escopo    ', esc, '|', [E[f'C{r}'].value for r in range(15, 18)])
    print('Aplicab.  ', {c: ap.count(c) for c in set(ap)}, '|', [A[f'D{r}'].value for r in range(54, 57)])
    print('Liderança ', li, '|', [L[f'D{r}'].value for r in range(18, 21)])
    print('Painel    ', [Pa[f'C{r}'].value for r in range(6, 16)], '| aviso', Pa['C31'].value)
    if ex:
        r = resumo(ex)
        ok_a = ap == [a['conf'] for a in aplicabilidade(ex)]
        ok_l = li == [lider_conf(c) for c in ex['lid']]
        ok_e = [x for x in esc if x not in ('OK', 'Opcional')] == escopo_conf(ex['escopo'])
        ind = [Pa[f'C{r}'].value for r in range(6, 16)]
        ok_i = (ind[3], ind[6], ind[7], ind[8], ind[9]) == (r['naoap'], r['dem'], r['parc'], r['ndem'], r['lid_rever'])
        print('            igual ao exemplo: escopo', 'OK' if ok_e else 'DIFERE', '| aplicabilidade', 'OK' if ok_a else 'DIFERE', '| liderança', 'OK' if ok_l else 'DIFERE %s' % li,
              '| indicadores', 'OK' if ok_i else 'DIFERE %s' % ind)
    if nome == 't3':
        esp = [aplic_conf(n, *APLIC3[n]) for n, _ in REQS]
        print('            t3 aplicabilidade igual à regra:', 'OK' if ap == esp else 'DIFERE %s' % [(n, g, e) for (n, _), g, e in zip(REQS, ap, esp) if g != e])
    print('Checklist ', [K[f'D{r}'].value for r in range(19, 25)])
