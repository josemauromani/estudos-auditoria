"""Lê os resultados dos testes de Objetivos-modelo.xlsx depois do recálculo.  Uso: obj_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from obj_data import EX1, EX2, caminho, situacao, resumo
D = sys.argv[1]
for nome, ex in (('t1', EX1), ('t2', EX2), ('t3', None)):
    w = openpyxl.load_workbook(f'{D}/{nome}.xlsx', data_only=True)
    O, P, A, Pa, K = w['Objetivos'], w['Planos'], w['Acompanhamento'], w['Painel'], w['Checklist']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:6] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    print('Objetivos ', [(O[f'O{r}'].value, O[f'P{r}'].value) for r in range(14, 26) if O[f'C{r}'].value], '| resumo', [O[f'D{r}'].value for r in range(28, 32)])
    print('Planos    ', [P[f'L{r}'].value for r in range(7, 43) if P[f'L{r}'].value], '| resumo', [P[f'E{r}'].value for r in range(45, 49)])
    got = [(A[f'T{r}'].value, A[f'U{r}'].value if not isinstance(A[f'U{r}'].value, (int, float)) else round(A[f'U{r}'].value, 4), A[f'V{r}'].value) for r in range(7, 19) if A[f'C{r}'].value]
    print('Acompanh. ', got, '| resumo', [A[f'D{r}'].value for r in range(21, 24)])
    print('Painel    ', [Pa[f'D{r}'].value for r in range(7, 15)], '| leitura', [(Pa[f'J{r}'].value, Pa[f'K{r}'].value, Pa[f'L{r}'].value) for r in range(18, 30) if Pa[f'C{r}'].value],
          '|', [Pa[f'D{r}'].value for r in (32, 33)])
    if ex:
        esp = [(ultimo, None if caminho(o) is None else round(caminho(o), 4), situacao(o, ex['head']['ref'])) for o, ultimo in ((o, [x for x in o['res'] if x is not None][-1]) for o in ex['objs'])]
        r = resumo(ex)
        print('            igual ao exemplo:', 'OK' if got == esp else 'DIFERE', '| ações atrasadas', 'OK' if Pa['D14'].value == r['atras'] else 'DIFERE %s' % Pa['D14'].value)
    print('Checklist ', [K[f'D{r}'].value for r in range(19, 25)])
