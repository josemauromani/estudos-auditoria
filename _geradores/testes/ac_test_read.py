"""Lê os resultados dos testes de Analise-Critica-modelo.xlsx depois do recálculo.  Uso: ac_test_read.py <pasta com t1..t5.xlsx>"""
import openpyxl, sys
D = sys.argv[1]
for nome in ('t1', 't2', 't3', 't4', 't5'):
    w = openpyxl.load_workbook(f'{D}/{nome}.xlsx', data_only=True)
    R, A, E, S, C = w['Reunião'], w['Ações anteriores'], w['Entradas'], w['Saídas'], w['Checklist']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:6] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    print('Reunião   ', [R[f'E{r}'].value for r in range(35, 42)])
    print('Ações     ', [A[f'K{r}'].value for r in range(9, 24) if A[f'K{r}'].value])
    print('           resumo', [A[f'E{r}'].value for r in range(26, 32)], '| por situação', [A[f'K{r}'].value for r in range(26, 31)])
    print('Entradas   decisões', [E[f'K{r}'].value for r in range(6, 18)])
    print('           conferência', [E[f'L{r}'].value for r in range(6, 18)])
    print('           resumo', [E[f'E{r}'].value for r in range(20, 27)])
    print('Saídas    ', [(S[f'D{r}'].value, S[f'K{r}'].value) for r in range(7, 22) if S[f'K{r}'].value])
    print('           resumo', [S[f'E{r}'].value for r in range(24, 30)])
    print('Checklist ', [C[f'D{r}'].value for r in range(19, 25)])
