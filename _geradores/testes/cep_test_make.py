"""Confere Histograma-CEP-modelo.xlsx e preenche cópias com dados de teste.  Uso: cep_test_make.py <modelo.xlsx> <pasta de saída>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from cep_data import EX1, EX2, SIM, amp, conf, fase, fora_espec, limites, media, sinal
from datetime import date
SRC, OUTDIR = sys.argv[1], sys.argv[2]
wb = openpyxl.load_workbook(SRC, data_only=True)
wf0 = openpyxl.load_workbook(SRC)
for ws in wb.worksheets:
    f = wf0[ws.title]
    print('==', ws.title, ws.dimensions, 'dv', len(f.data_validations.dataValidation), 'cf', sum(len(v) for v in f.conditional_formatting._cf_rules.values()),
          'charts', len(f._charts), 'comments', sum(1 for r in f.iter_rows() for c in r if c.comment))
err = [(ws.title, c.coordinate, c.value) for ws in wb.worksheets if ws.title != 'Gráficos' for r in ws.iter_rows() for c in r
       if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
print('erros', err)
print('vazio:', wb['Painel']['C28'].value, '|', wb['Dados']['E45'].value)


def v(c):
    """O openpyxl lê como None o texto vazio que a fórmula devolve; e as datas, como datetime."""
    x = c.value
    return '' if x is None else (x.date() if hasattr(x, 'date') else x)


def e(x):
    return '' if x is None else x


def rnd(x):
    return round(x, 6) if isinstance(x, float) else x


def linhas(s, ex, d1):
    L = limites(ex)
    got = [tuple(rnd(v(s[f'{c}{d1 + k}'])) for c in 'LMNOPQ') for k in range(len(ex['subs']))]
    esp = [(rnd(e(media(g['v']))), rnd(e(amp(g['v']))), fase(ex, k), fora_espec(ex, g['v']) if any(x is not None for x in g['v']) else '', sinal(ex, k, L), conf(g))
           for k, g in enumerate(ex['subs'])]
    return got, esp, L


for aba, ex in (('Exemplo 1 - Pizzaria', EX1), ('Exemplo 2 - Indústria', EX2)):
    s = wb[aba]
    got, esp, L = linhas(s, ex, 19)
    gl = [rnd(v(s[f'L{r}'])) for r in range(10, 17)]
    el = [L['n'], rnd(L['lc']), rnd(L['lsc']), rnd(L['lic']), rnd(L['rb']), rnd(L['lscr']), rnd(L['sigma'])]
    print(aba, '| linhas', 'OK' if got == esp else 'DIFERE\n%s\n%s' % (got, esp), '| limites', 'OK' if gl == el else 'DIFERE %s %s' % (gl, el),
          '| capacidade', s['E80'].value, s['E81'].value, s['E82'].value, '| aviso', s['E83'].value)


def preencher(nome, ex, carac='Característica', unid='u', check=None):
    w = openpyxl.load_workbook(SRC)
    Dd, K = w['Dados'], w['Checklist']
    h = ex['head']
    Dd['E4'], Dd['E5'], Dd['E6'], Dd['E7'] = carac, unid, h['lie'], h['lse']
    if h['base']:
        Dd['E8'] = h['base']
    for k, g in enumerate(ex['subs']):
        r = 13 + k
        if g['data']:
            Dd[f'C{r}'] = g['data']
        if g['id']:
            Dd[f'D{r}'] = g['id']
        for c, x in zip('EFGHI', g['v']):
            if x is not None:
                Dd[f'{c}{r}'] = x
        if g['excl']:
            Dd[f'J{r}'] = g['excl']
        if g['motivo']:
            Dd[f'K{r}'] = g['motivo']
    for k, val in enumerate(check or ()):
        if val:
            K[f'D{5 + k}'] = val
    w.save(OUTDIR + '/%s.xlsx' % nome)


preencher('t1', EX1, EX1['head']['carac'], 'g', check=['Sim'] * 12)
preencher('t2', EX2, EX2['head']['carac'], 'µm', check=['Sim'] * 6 + ['Parcial', 'Não'])

# ---- t3 e t4: casos de borda
D = date


def sub(k, vals, excl='', motivo='', data=True, ident=True):
    return dict(data=D(2028, 1, 1 + k) if data else None, id=f'S{k + 1}' if ident else '', v=list(vals), excl=excl, motivo=motivo)


base3 = []
for k in range(20):
    m = 10.02 if k % 2 == 0 else 9.98
    base3.append(sub(k, [m + 0.2, m - 0.2, m + 0.1, m - 0.1, m]))
base3[4] = sub(4, [10.6, 10.7, 10.5, 10.6, 10.6], SIM, 'Ajuste errado do operador')           # excluída da base, com sinal
acomp3 = [sub(20, [9.9, 9.9, 9.9, 10.4, 9.4]),                                             # amplitude fora
          sub(21, [10.3, 10.3, 10.2, 10.4, 10.3])]                                         # média fora
acomp3 += [sub(22 + j, [m] * 4 + [m + 0.05]) for j, m in enumerate([10.04, 10.07, 10.05, 10.09, 10.06, 10.08])]   # 7 do mesmo lado na última
acomp3 += [sub(28, [8.9, 9.0, 9.1, 9.0, 9.0]), sub(29, [10.0, 10.0, 10.0, 10.0, 10.0])]   # valores fora da especificação
EX3 = dict(head=dict(lie=9, lse=11, base=20), subs=base3 + acomp3)
subs4 = [sub(k, [m - 0.1, m + 0.1, m, m - 0.05, m + 0.05]) for k, m in enumerate([9.9, 9.92, 9.95, 9.97, 10.0, 10.03, 10.0, 9.98, 10.01, 9.99, 10.02, 9.97])]  # tendência na base
subs4 += [sub(12, [10, 10, None, None, None]),                                              # faltam medições
          dict(data=D(2028, 2, 1), id='S14', v=[None] * 5, excl='', motivo=''),             # só a data: faltam medições
          sub(14, [10, 10.1, 9.9, 10, 10], data=False),                                     # falta a data
          sub(15, [10, 10.1, 9.9, 10, 10], SIM, '')]                                        # falta o motivo
EX4 = dict(head=dict(lie=9.5, lse=10.5, base=None), subs=subs4)
preencher('t3', EX3)
preencher('t4', EX4)
EX5 = dict(EX1, head=dict(EX1['head'], lie=370, lse=430))                                # capacidade no limite
EX6 = dict(EX1, head=dict(EX1['head'], lie=360, lse=440))                                # tudo OK
EX7 = dict(EX2, head=dict(EX2['head'], base=25))                                         # sinal na base
for nome, ex in (('t5', EX5), ('t6', EX6), ('t7', EX7)):
    preencher(nome, ex)
print('ok')
