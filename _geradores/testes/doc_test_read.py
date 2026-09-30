"""Lê os resultados dos testes de Informacao-Documentada-modelo.xlsx depois do recálculo.  Uso: doc_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys
D = sys.argv[1]
for nome in ('t1', 't2', 't3'):
    w = openpyxl.load_workbook(f'{D}/{nome}.xlsx', data_only=True)
    L, R, X, A, C = w['Lista mestra'], w['Registros'], w['Externos'], w['Alterações'], w['Checklist']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:6] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    print('Lista      ', [(L[f'D{r}'].value[:14], L[f'N{r}'].value.strftime('%m/%Y') if L[f'N{r}'].value else None, L[f'P{r}'].value) for r in range(9, 39) if L[f'P{r}'].value])
    print('            resumo', [L[f'E{r}'].value for r in range(41, 47)], '| por situação', [L[f'L{r}'].value for r in range(41, 48)])
    print('Registros  ', [R[f'L{r}'].value for r in range(7, 27) if R[f'L{r}'].value], '| resumo', [R[f'E{r}'].value for r in range(29, 33)])
    print('Externos   ', [(X[f'K{r}'].value.strftime('%m/%Y') if X[f'K{r}'].value else None, X[f'L{r}'].value) for r in range(7, 22) if X[f'L{r}'].value],
          '| resumo', [X[f'E{r}'].value for r in range(24, 28)])
    print('Alterações ', [A[f'K{r}'].value for r in range(7, 27) if A[f'K{r}'].value], '| resumo', [A[f'F{r}'].value for r in range(29, 32)])
    print('Checklist  ', [C[f'D{r}'].value for r in range(19, 25)])
