"""Lê os resultados dos testes de Producao-modelo.xlsx depois do recálculo.  Uso: prod_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from prod_data import EX1, EX2, criterio, leitura, resumo, resumo_k
D = sys.argv[1]
for nome, ex in (('t1', EX1), ('t2', EX2), ('t3', None)):
    w = openpyxl.load_workbook(f'{D}/{nome}.xlsx', data_only=True)
    P, R, T, M, Pa, K = w['Plano de controle'], w['Registros'], w['Rastreabilidade'], w['Mudanças'], w['Painel'], w['Checklist']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:7] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    crit = [(P[f'N{r}'].value, P[f'O{r}'].value) for r in range(10, 30) if P[f'D{r}'].value]
    print('Plano     ', crit if not ex else [c for c in crit if c[1] != 'OK'], '| resumo', [P[f'D{r}'].value for r in range(32, 36)])
    leit = [(R[f'L{r}'].value, R[f'O{r}'].value) for r in range(7, 157) if R[f'O{r}'].value]
    print('Registros ', leit if not ex else [l for l in leit if l[1] != 'OK'], '| resumo', [R[f'E{r}'].value for r in range(159, 164)])
    print('Rastreab. ', [T[f'H{r}'].value for r in range(7, 17) if T[f'H{r}'].value], [T[f'H{r}'].value for r in range(21, 29) if T[f'H{r}'].value], '| resumo', [T[f'D{r}'].value for r in range(31, 35)])
    print('Mudanças  ', [M[f'I{r}'].value for r in range(7, 19) if M[f'I{r}'].value], '| resumo', [M[f'E{r}'].value for r in range(21, 24)])
    tab = [(Pa[f'B{r}'].value, Pa[f'E{r}'].value, Pa[f'F{r}'].value, Pa[f'G{r}'].value, None if Pa[f'H{r}'].value in ('', None) else round(Pa[f'H{r}'].value, 4), Pa[f'I{r}'].value)
           for r in range(18, 38) if Pa[f'C{r}'].value]
    print('Painel    ', [Pa[f'D{r}'].value for r in range(7, 15)], '| aviso', Pa['D40'].value)
    if ex:
        ks = {k['id']: k for k in ex['plano']}
        r = resumo(ex)
        ok_c = [c for c, _ in crit] == [criterio(k) for k in ex['plano']]
        ok_l = [R[f'L{i}'].value for i in range(7, 7 + len(ex['regs']))] == [leitura(ks[x['k']], x) for x in ex['regs']]
        ok_t = [(t[1], t[2], t[3], t[4]) for t in tab] == [(x['n'], x['fora'], x['semr'], round(x['dentro'], 4)) for x in resumo_k(ex)]
        ok_p = (Pa['D7'].value, Pa['D8'].value, Pa['D10'].value, Pa['D11'].value) == (r['controles'], r['n'], r['fora'], r['semr'])
        print('            igual ao exemplo: critérios', 'OK' if ok_c else 'DIFERE %s' % [c for c, _ in crit], '| leituras', 'OK' if ok_l else 'DIFERE', '| tabela do painel', 'OK' if ok_t else 'DIFERE %s' % tab,
              '| indicadores', 'OK' if ok_p else 'DIFERE')
    else:
        print('            tabela', tab)
    print('Checklist ', [K[f'D{r}'].value for r in range(19, 25)])
