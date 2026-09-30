"""Lê os resultados dos testes de Pareto-modelo.xlsx depois do recálculo.  Uso: par_test_read.py <pasta com t1..t5.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from par_data import EX1, EX3, linhas, pareto
D = sys.argv[1]
for nome in ('t1', 't2', 't3', 't4', 't5'):
    w = openpyxl.load_workbook(f'{D}/{nome}.xlsx', data_only=True)
    C, F, P, A, K = w['Coleta'], w['Folha'], w['Pareto'], w['Antes e depois'], w['Checklist']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:6] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value) and not (ws.title == 'Pareto' and c.column_letter == 'M')]
    print('erros', err)
    print('Coleta ', [C[f'F{r}'].value for r in range(14, 22) if C[f'F{r}'].value], '| resumo', [C[f'D{r}'].value for r in (25, 26)])
    print('Folha  ', [F[f'K{r}'].value for r in range(8, 18)], '| resumo', [F[f'D{r}'].value for r in range(21, 25)])
    got = [(P[f'C{r}'].value, P[f'D{r}'].value, round(P[f'E{r}'].value, 4), round(P[f'F{r}'].value, 4), P[f'G{r}'].value) for r in range(8, 17) if P[f'C{r}'].value]
    print('Pareto ', [(a, b, '%.0f%%' % (100 * c), '%.0f%%' % (100 * d), e) for a, b, c, d, e in got])
    print('         linha do gráfico', [P[f'M{r}'].value for r in range(8, 17)], '| resumo', [P[f'D{r}'].value for r in range(19, 24)])
    if nome == 't1':
        esp = [(r['nome'], r['v'], round(r['pct'], 4), round(r['acc'], 4), r['classe']) for r in pareto(linhas(EX1))]
        print('         igual ao exemplo 1:', 'OK' if got == esp else 'DIFERE')
    if nome == 't2':
        esp = [(r['nome'], r['v'], round(r['pct'], 4), round(r['acc'], 4), r['classe']) for r in pareto([(n, q * kg) for n, q, kg in EX3['defeitos']])]
        print('         igual ao exemplo 3, por quilos:', 'OK' if got == esp else 'DIFERE %s' % esp)
    print('Antes e depois', A['E7'].value, [(A[f'C{r}'].value, A[f'F{r}'].value and round(A[f'F{r}'].value, 2), A[f'G{r}'].value if A[f'G{r}'].value in ('', None) else round(A[f'G{r}'].value, 2),
                                             A[f'H{r}'].value if A[f'H{r}'].value in ('', None) else round(A[f'H{r}'].value, 2), A[f'I{r}'].value) for r in range(11, 21) if A[f'D{r}'].value not in ('', None)])
    print('         resumo', [A[f'D{r}'].value for r in range(23, 27)])
    print('Checklist', [K[f'D{r}'].value for r in range(19, 25)])
