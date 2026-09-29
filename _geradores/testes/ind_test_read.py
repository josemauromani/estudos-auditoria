"""Lê os resultados dos testes depois do recálculo.  Uso: ind_test_read.py <pasta com t1.xlsx, t2.xlsx e t3.xlsx recalculados>"""
import openpyxl, sys
D = sys.argv[1]
def rd(v):
    return round(v, 2) if isinstance(v, float) else v
for n in ('t1', 't2', 't3'):
    wb = openpyxl.load_workbook(D + '/%s.xlsx' % n, data_only=True)
    f, m, p, a = wb['Fichas'], wb['Medições'], wb['Painel'], wb['Análise']
    print('==', n, '| fichas', [f[f'N{k}'].value for k in range(10, 14)], [f[f'E{k}'].value for k in range(24, 27)])
    print('   medições', [m[f'Q{k}'].value for k in range(7, 11)], 'seguidos', [m[f'Q{k}'].value for k in range(22, 26)], '|', m['D38'].value)
    for k in range(7, 11):
        print('   painel', [rd(p[f'{c}{k}'].value) for c in 'CGHIJKLMN'])
    print('   resumo painel', [p[f'D{k}'].value for k in range(21, 27)])
    print('   gráfico', p['D29'].value, p['E29'].value, [p[f'{c}30'].value for c in 'DEO'], [rd(p[f'{c}31'].value) for c in 'DEGO'], [p[f'{c}32'].value for c in 'DO'], [p[f'{c}33'].value for c in 'DO'])
    if n == 't1':
        for k in range(7, 10):
            print('   análise', [str(a[f'{c}{k}'].value)[:32] for c in 'DEL'])
        print('   resumo análise', [a[f'F{k}'].value for k in range(24, 30)])
