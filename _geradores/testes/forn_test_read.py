"""Lê os resultados dos testes de Fornecedores-modelo.xlsx depois do recálculo.  Uso: forn_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys
D = sys.argv[1]
for nome in ('t1', 't2', 't3'):
    w = openpyxl.load_workbook(f'{D}/{nome}.xlsx', data_only=True)
    C, H, A, O, K = w['Cadastro'], w['Homologação'], w['Avaliação'], w['Ocorrências'], w['Checklist']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:6] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    print('Cadastro   ', [(C[f'C{r}'].value, C[f'J{r}'].value.strftime('%m/%Y') if C[f'J{r}'].value else None, C[f'L{r}'].value) for r in range(9, 39) if C[f'D{r}'].value])
    print('            resumo', [C[f'E{r}'].value for r in range(41, 47)])
    print('Homolog.   ', [H[f'C{r}'].value for r in (17, 18, 19)])
    print('Avaliação  ', [(A[f'C{r}'].value, A[f'D{r}'].value, A[f'M{r}'].value, A[f'N{r}'].value, A[f'Q{r}'].value) for r in range(7, 37) if A[f'C{r}'].value])
    print('            resumo', [A[f'E{r}'].value for r in range(39, 44)])
    print('Ocorrências', [(O[f'G{r}'].value, O[f'K{r}'].value) for r in range(7, 32) if O[f'K{r}'].value], '| resumo', [O[f'E{r}'].value for r in range(34, 38)])
    print('Checklist  ', [K[f'D{r}'].value for r in range(19, 25)])
