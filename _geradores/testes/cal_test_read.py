"""Lê os resultados dos testes de Calibracao-modelo.xlsx depois do recálculo.  Uso: cal_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from cal_data import EX1, EX2, SITS, cal_conf, inst_conf, proxima, resultado, resumo, situacao
D = sys.argv[1]
for nome, ex in (('t1', EX1), ('t2', EX2), ('t3', None)):
    w = openpyxl.load_workbook(f'{D}/{nome}.xlsx', data_only=True)
    I, C, Pa, K = w['Instrumentos'], w['Calibrações'], w['Painel'], w['Checklist']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:5] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    ins = [(I[f'O{r}'].value, I[f'P{r}'].value, I[f'Q{r}'].value, I[f'R{r}'].value) for r in range(8, 48) if I[f'C{r}'].value]
    cal = [(C[f'K{r}'].value, C[f'L{r}'].value, C[f'O{r}'].value) for r in range(7, 87) if C[f'O{r}'].value]
    print('Instrum.  ', [(a.date() if hasattr(a, 'date') else a, b, c, d) for a, b, c, d in ins] if not ex else 'linhas %d' % len(ins), '|', [I[f'E{r}'].value for r in range(50, 54)])
    print('Calibr.   ', cal if not ex else 'linhas %d' % len(cal), '|', [C[f'E{r}'].value for r in range(89, 92)])
    print('Painel    ', [Pa[f'C{r}'].value for r in range(6, 17)], '| aviso', Pa['C19'].value)
    if ex:
        ref, r = ex['head']['ref'], resumo(ex)
        ok_i = [(a.date() if a else None, b, c or '', d) for a, b, c, d in ins] == [(proxima(i), situacao(i, ref), __import__('cal_data').adequacao(i), inst_conf(i, ref)) for i in ex['insts']]
        ok_c = [(b, c) for a, b, c in cal] == [(resultado(c, ex['insts']), cal_conf(c, ex['insts'])) for c in ex['cals']]
        ind = [Pa[f'C{r}'].value for r in range(6, 17)]
        ok_p = ind[:7] == [r['insts']] + [r['sits'][s] for s in SITS] + [r['grossa']] and ind[8] == r['reprov']
        print('            igual ao exemplo: instrumentos', 'OK' if ok_i else 'DIFERE %s' % ins, '| calibrações', 'OK' if ok_c else 'DIFERE %s' % cal, '| painel', 'OK' if ok_p else 'DIFERE %s' % ind)
    print('Checklist ', [K[f'D{r}'].value for r in range(19, 25)])
