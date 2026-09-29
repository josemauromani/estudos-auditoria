import openpyxl, sys
D = sys.argv[1]
def rd(v):
    return round(v, 2) if isinstance(v, float) else v
for n in ('t1', 't2'):
    wb = openpyxl.load_workbook(D + '/%s.xlsx' % n, data_only=True)
    r = wb['Riscos']
    print('==', n)
    for k in range(11, 28):
        if r[f'E{k}'].value:
            print('   ', [str(r[f'{c}{k}'].value)[:30] for c in 'EIJRSTUV'])
    print('   resumo riscos', [r[f'G{k}'].value for k in range(33, 39)])
    m = wb['Mapa']
    print('   cabeçalho', m['C4'].value, m['J4'].value)
    print('   inicial ', [[m[f'{c}{k}'].value for c in 'CDEFG'] for k in range(7, 12)])
    print('   residual', [[m[f'{c}{k}'].value for c in 'JKLMN'] for k in range(7, 12)])
    print('   níveis', [(m[f'B{k}'].value, m[f'E{k}'].value, m[f'F{k}'].value) for k in range(15, 19)])
    print('   resumo mapa', [rd(m[f'E{k}'].value) for k in range(21, 27)])
    o = wb['Oportunidades']
    print('   oport', [[o[f'{c}{k}'].value for c in 'GHN'] for k in range(7, 12)], [o[f'E{k}'].value for k in range(19, 24)])
