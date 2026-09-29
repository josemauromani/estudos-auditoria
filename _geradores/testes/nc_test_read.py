import openpyxl, sys
D = sys.argv[1]
wb = openpyxl.load_workbook(D + '/t1.xlsx', data_only=True)
c = wb['Controle']
for r in range(10, 15):
    print([c[f'{x}{r}'].value for x in 'FMN'])
print('resumo controle', [c[f'G{r}'].value for r in range(32, 40)]); print('origens', [c[f'M{r}'].value for r in range(33, 40)])
g = wb['Registro']; print('registro', [g[f'D{r}'].value for r in range(41, 47)], '| eficácia:', g['F38'].value)
p = wb['Plano de ação']; print('cabeçalho plano', p['D4'].value, '|', str(p['F4'].value)[:40])
for r in range(9, 16):
    print([p[f'{x}{r}'].value for x in 'CKL'])
print('resumo plano', [p[f'E{r}'].value for r in range(23, 30)])
e = wb['Eficácia']
print('eficácia t1 H', [e[f'H{r}'].value for r in range(11, 23)]); print([e[f'E{r}'].value for r in range(25, 31)])
for n in ('t2', 't3', 't4', 't5', 't6', 't7', 't8'):
    e = openpyxl.load_workbook(D + '/%s.xlsx' % n, data_only=True)['Eficácia']
    print(n, [e[f'H{r}'].value for r in range(11, 18)], '|', e['E29'].value, '|', e['E30'].value)
