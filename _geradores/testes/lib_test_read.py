"""Lê os resultados dos testes de Liberacao-modelo.xlsx depois do recálculo.  Uso: lib_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lib_data import EX1, EX2, lib_conf, lib_leitura, pnc_conf, pnc_sit, por_det, resumo
D = sys.argv[1]
for nome, ex in (('t1', EX1), ('t2', EX2), ('t3', None)):
    w = openpyxl.load_workbook(f'{D}/{nome}.xlsx', data_only=True)
    A, L, P, Pa, K = w['Autoridades'], w['Liberação'], w['Produto não conforme'], w['Painel'], w['Checklist']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:6] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    print('Autorid.  ', [A[f'I{r}'].value for r in range(7, 15)], '|', A['E17'].value, '|', A['E18'].value)
    lib = [(L[f'I{r}'].value, L[f'O{r}'].value) for r in range(7, 67) if L[f'D{r}'].value]
    print('Liberação ', lib if not ex else 'linhas %d' % len(lib), '| resumo', [L[f'E{r}'].value for r in range(69, 73)])
    pnc = [(P[f'R{r}'].value, P[f'S{r}'].value, P[f'T{r}'].value) for r in range(7, 67) if P[f'T{r}'].value]
    print('PNC       ', pnc if not ex else 'linhas %d' % len(pnc), '| resumo', [P[f'E{r}'].value for r in range(69, 73)])
    print('Painel    ', [Pa[f'C{r}'].value for r in range(5, 17)], '| aviso', Pa['C35'].value)
    det = [(Pa[f'B{r}'].value, Pa[f'C{r}'].value, Pa[f'D{r}'].value, Pa[f'E{r}'].value) for r in range(20, 24)]
    disp = [(Pa[f'B{r}'].value, Pa[f'C{r}'].value, Pa[f'D{r}'].value) for r in range(27, 33)]
    print('Detecção  ', det)
    print('Disposição', disp)
    if ex:
        r = resumo(ex)
        ok_l = lib == [(lib_leitura(l), lib_conf(l)) for l in ex['libs']]
        ok_p = [(a, c) for a, b, c in pnc] == [(pnc_sit(p), pnc_conf(p, ex['pncs'])) for p in ex['pncs']]
        ok_d = [(b, c, round(d, 2)) for a, b, c, d in det] == [(x['n'], x['custo'], round(x['medio'] or 0, 2)) for x in por_det(ex)]
        ok_i = (Pa['C5'].value, Pa['C6'].value, Pa['C7'].value, Pa['C8'].value, Pa['C9'].value, Pa['C10'].value, Pa['C14'].value) == \
               (r['libs'], r['conf'], r['aut'], r['ret'], r['lib_rever'], r['pncs'], r['custo'])
        print('            igual ao exemplo: liberações', 'OK' if ok_l else 'DIFERE %s' % lib, '| registros', 'OK' if ok_p else 'DIFERE %s' % pnc, '| detecção', 'OK' if ok_d else 'DIFERE',
              '| indicadores', 'OK' if ok_i else 'DIFERE')
    print('Checklist ', [K[f'D{r}'].value for r in range(19, 25)])
