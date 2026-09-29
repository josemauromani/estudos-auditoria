import openpyxl, sys
D = sys.argv[1]
for n in ('t1', 't2', 't3', 't4'):
    wb = openpyxl.load_workbook(D + '/%s.xlsx' % n, data_only=True)
    r = wb['Resumo']
    print('==', n, '| cabeçalho', r['D4'].value, r['H4'].value)
    if n in ('t1', 't2'):
        for k in range(7, 15):
            print('   ', [r[f'{c}{k}'].value if not isinstance(r[f'{c}{k}'].value, float) else round(r[f'{c}{k}'].value, 3) for c in 'BDEFGHI'])
    print('   resumo', [r[f'E{k}'].value if not isinstance(r[f'E{k}'].value, float) else round(r[f'E{k}'].value, 3) for k in range(17, 23)])
    if n == 't2':
        d = wb['Diagnóstico']
        print('   conferência', {str(d[f'B{k}'].value): d[f'J{k}'].value for k in range(9, 61) if d[f'J{k}'].value not in (None, 'Completo')})
        p = wb['Plano de ação']
        for k in range(7, 12):
            print('   plano', [str(p[f'{c}{k}'].value)[:34] for c in 'CDEK'])
        print('   resumo plano', [p[f'E{k}'].value if not isinstance(p[f'E{k}'].value, float) else round(p[f'E{k}'].value, 3) for k in range(29, 36)])
        o = wb['Documentos']; print('   docs', [o[f'F{k}'].value for k in range(31, 38)])
