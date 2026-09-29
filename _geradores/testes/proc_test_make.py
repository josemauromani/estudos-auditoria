"""Confere Processos-modelo.xlsx e preenche cópias com dados de teste.  Uso: proc_test_make.py <modelo.xlsx> <pasta de saída>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from proc_data import EX1, EX2, IND, IND_TIPO, INTER, ORDEM_PARTES, fornece, recebe
from datetime import date
SRC, OUTDIR = sys.argv[1], sys.argv[2]
wb = openpyxl.load_workbook(SRC, data_only=True)
wf0 = openpyxl.load_workbook(SRC)
for ws in wb.worksheets:
    f = wf0[ws.title]
    print('==', ws.title, ws.dimensions, 'dv', len(f.data_validations.dataValidation), 'cf', sum(len(v) for v in f.conditional_formatting._cf_rules.values()),
          'charts', len(f._charts), 'comments', sum(1 for r in f.iter_rows() for c in r if c.comment))
err = [(ws.title, c.coordinate, c.value) for ws in wb.worksheets for r in ws.iter_rows() for c in r
       if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
print('erros', err)
print('vazio:', wb['Processos']['E29'].value, '|', wb['Interações']['D24'].value, '|', wb['Tartaruga']['H38'].value, '|', wb['Elementos']['D27'].value,
      '|', wb['Checklist']['D24'].value)

# exemplo 1: percentuais da planilha contra os dados
s = wb['Exemplo 1 - Pizzaria']
ids = [p['id'] for p in EX1['procs']]
linhas = [k for k in range(8, 40) if s[f'B{k}'].value in ids]
for k, p in zip(linhas, EX1['procs']):
    ok = abs(s[f'P{k}'].value - p['pts']) < 1e-9 and abs(s[f'Q{k}'].value - p['pct']) < 1e-9
    print('   ', p['id'], s[f'P{k}'].value, round(100 * s[f'Q{k}'].value), 'OK' if ok else 'DIFERE de %s' % p['pts'])
k = linhas[-1] + 1
media = sum(p['pct'] for p in EX1['procs']) / len(EX1['procs'])
print('    média', s[f'Q{k}'].value, media, 'OK' if abs(s[f'Q{k}'].value - media) < 1e-9 else 'DIFERE')
print('    por elemento', [round(100 * s.cell(row=k, column=8 + j).value) for j in range(8)])
print('    resumo', [(s[f'B{r}'].value, s[f'E{r}'].value) for r in range(k + 3, k + 9)])
s = wb['Exemplo 2 - Compras']
print('Exemplo 2', [(s[f'B{r}'].value, s[f'F{r}'].value) for r in range(1, 80) if isinstance(s[f'F{r}'].value, (int, float)) and s[f'B{r}'].value],
      '| esperado', [len(EX2['tartaruga'][p]) for p in ORDEM_PARTES], len(recebe(3)), len(fornece(3)))


def preencher(nome, procs=(), inter=(), elem=(), tart=None, check=None, extra=None):
    w = openpyxl.load_workbook(SRC)
    P, I, T, E, C = w['Processos'], w['Interações'], w['Tartaruga'], w['Elementos'], w['Checklist']
    P['D4'] = 'Teste'; P['H4'] = date(2026, 10, 20)
    for k, row in enumerate(procs):
        for col, v in zip('CDEFGHIJ', row):
            if v is not None:
                P[f'{col}{10 + k}'] = v
    for a, b, t in inter:
        I.cell(row=5 + a, column=3 + b, value=t)
    for k, row in enumerate(elem):
        for j, v in enumerate(row or ()):
            if v:
                E.cell(row=5 + k, column=4 + j, value={'S': 'Sim', 'P': 'Parcial', 'N': 'Não'}[v])
    if tart:
        T['D4'] = tart['n']; T['H4'] = date(2026, 10, 20)
        pos = {'entradas': ('C', 11), 'saidas': ('G', 11), 'oque': ('C', 18), 'quem': ('G', 18), 'como': ('C', 25), 'quanto': ('G', 25), 'riscos': ('C', 32)}
        for p, itens in tart['partes'].items():
            c, r0 = pos[p]
            for j, (a, b) in enumerate(itens[:4]):
                if a is not None:
                    T[f'{c}{r0 + j}'] = a
                if b is not None:
                    T[f'{chr(ord(c) + 1)}{r0 + j}'] = b
    for k, v in enumerate(check or ()):
        if v:
            C[f'D{5 + k}'] = v
    for (aba, ref), v in (extra or {}).items():
        w[aba][ref] = v
    w.save(OUTDIR + '/%s.xlsx' % nome)


# t1: indústria completa (9 processos, 24 interações, tartaruga de compras), tudo correto
procs9 = [(n, t, 'Dono %d' % k, 'Objetivo', 'Entradas', 'Saídas', 'Cliente', 'Indicador') for k, (n, t) in enumerate(zip(IND, IND_TIPO), 1)]
preencher('t1', procs=procs9, inter=INTER, elem=['SSSSSSSS'] * 9,
          tart=dict(n=3, partes={p: EX2['tartaruga'][p] for p in ORDEM_PARTES}), check=['Sim'] * 12)
# t2: pizzaria, com os elementos do exemplo 1 (os percentuais devem ser os mesmos do treinamento)
procs_pz = [(p['nome'], p['tipo'], p['dono'], p['objetivo'], 'Entradas', 'Saídas', 'Cliente', p['indicador'] or None) for p in EX1['procs']]
preencher('t2', procs=procs_pz, elem=[''.join(x[0] for x in p['elem']) for p in EX1['procs']],
          inter=[(3, 4, 'Pedido registrado'), (4, 5, 'Pedido embalado'), (7, 4, 'Insumos')],
          tart=dict(n=5, partes={'entradas': EX1['tartaruga']['entradas'], 'saidas': [('Pedido entregue', None)], 'quanto': EX1['tartaruga']['quanto']}),
          check=['Sim'] * 6 + ['Parcial', 'Não'])
# t3: erros propositais
preencher('t3',
          procs=[('Vender', 'Principal', 'Gerente', 'Objetivo', 'E', 'S', 'Cliente', 'Ind'),
                 ('Produzir', None, 'Líder', 'Objetivo', 'E', 'S', 'Cliente', 'Ind'),          # sem tipo
                 ('Entregar', 'Principal', None, 'Objetivo', 'E', 'S', 'Cliente', 'Ind'),      # sem dono
                 ('Comprar', 'Principal', 'Comprador', 'Objetivo', 'E', None, 'Cliente', 'Ind')],  # sem saída; não há gestão nem apoio
          inter=[(1, 2, 'Pedido'), (2, 3, 'Produto'), (6, 1, 'Ligação de processo sem cadastro')],
          elem=['SSSS', None, 'PPPPPPPP', None, None, 'SSSSSSSS'],   # incompleta, não avaliado, completa, não avaliado, sem cadastro
          tart=dict(n=9, partes={'entradas': [('Pedido', 'Cliente')]}))
# t4: só processos principais completos, menos de oito; tartaruga completa do processo 2
preencher('t4', procs=[('Vender', 'Principal', 'A', 'O', 'E', 'S', 'C', 'I'), ('Dirigir', 'Gestão', 'A', 'O', 'E', 'S', 'C', 'I'),
                       ('Comprar', 'Apoio', 'A', 'O', 'E', 'S', 'C', 'I')],
          inter=[(2, 1, 'Metas'), (3, 1, 'Materiais'), (1, 2, 'Resultados')],
          tart=dict(n=2, partes={p: [('Item', 'Detalhe')] for p in ORDEM_PARTES}))
print('ok')
