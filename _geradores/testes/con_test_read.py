"""Lê os resultados dos testes de Conhecimento-modelo.xlsx depois do recálculo.  Uso: con_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import con_data as R
from con_data import (EX1, EX2, PRAZO_LICAO, at_conf, at_dias, at_sit, con_conf, con_sit, lic_conf, lic_dias, lic_sit, pol_conf, pontos, prazo_at, resumo)
PASTA = sys.argv[1]

# os casos de borda vêm do roteiro de preenchimento, sem regravar as cópias
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'con_test_make.py'), encoding='utf-8').read()
_ns = {}
exec(_src[_src.index('D = date'):_src.index("preencher('t3'")], {'date': __import__('datetime').date, **vars(R)}, _ns)


def mk(ref, cons, lics, pols, ats):
    z = lambda keys, rows: [dict(zip(keys, r)) for r in rows]  # noqa: E731
    return dict(head=dict(ref=ref), cons=z(("cod", "nome", "proc", "crit", "forma", "onde", "pessoas", "saida", "acao", "prazo"), cons),
                lics=z(("num", "data", "origem", "oque", "aprend", "onde", "resp", "cod", "incorp"), lics),
                pols=z(("prod", "vida", "minimo", "aceito", "ativ", "resp", "conseq"), pols),
                ats=z(("num", "abert", "cliente", "prod", "tipo", "relato", "resol", "custo", "causa", "licao"), ats))


EX3 = mk(_ns['REF3'], _ns['cons3'], _ns['lics3'], _ns['pols3'], _ns['ats3'])
PAINEL = {'Conhecimentos mapeados': 7, 'Crítico': 8, 'Em risco': 9, 'Sob controle': 10, 'Expostos sem ação de transferência': 11, 'Ações de transferência vencidas': 12,
          'Lições registradas': 14, 'Lições pendentes': 15, f'Pendentes há mais de {PRAZO_LICAO} dias': 16, 'Produtos com política': 18,
          'Prazo aceito menor que o mínimo': 19, 'Atendimentos': 20, 'Abertos': 21, 'Fora do prazo, resolvidos ou não': 22, 'Resolvidos no prazo': 23,
          'Custo dos atendimentos': 24, 'Linhas a completar': 25}


def v(c):
    """O openpyxl lê como None o texto vazio que a fórmula devolve."""
    return '' if c.value is None else c.value


def e(x):
    return '' if x is None else x


for nome, ex in (('t1', EX1), ('t2', EX2), ('t3', EX3)):
    w = openpyxl.load_workbook(f'{PASTA}/{nome}.xlsx', data_only=True)
    K, L, P, A, Pa, C = w['Conhecimento'], w['Lições'], w['Pós-entrega'], w['Atendimentos'], w['Painel'], w['Checklist']
    ref = ex['head']['ref']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:6] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    got = dict(con=[(v(K[f'M{r}']), v(K[f'N{r}']), v(K[f'O{r}'])) for r in range(8, 8 + len(ex['cons']))],
               lic=[(v(L[f'L{r}']), v(L[f'M{r}']), v(L[f'N{r}'])) for r in range(7, 7 + len(ex['lics']))],
               pol=[v(P[f'J{r}']) for r in range(7, 7 + len(ex['pols']))],
               at=[(v(A[f'M{r}']), v(A[f'N{r}']), v(A[f'O{r}']), v(A[f'P{r}'])) for r in range(7, 7 + len(ex['ats']))])
    esp = dict(con=[(e(pontos(k)), con_sit(k), con_conf(k, ref)) for k in ex['cons']],
               lic=[(lic_sit(l), e(lic_dias(l, ref)), lic_conf(l, ex['cons'], ref)) for l in ex['lics']],
               pol=[pol_conf(p) for p in ex['pols']],
               at=[(e(prazo_at(a, ex['pols'])), e(at_dias(a, ref)), at_sit(a, ex['pols'], ref), at_conf(a, ex['pols'], ex['lics'])) for a in ex['ats']])
    for k in got:
        print('%-4s' % k, 'OK' if got[k] == esp[k] else 'DIFERE\n   planilha %s\n   esperado %s' % (got[k], esp[k]))
    pa = {k: Pa[f'C{r}'].value for k, r in PAINEL.items()}
    print('Painel    ', pa)
    print('Avisos    ', [K['E52'].value, L['E71'].value, P['E30'].value, A['E91'].value, Pa['C28'].value])
    if nome != 't3':
        r = resumo(ex)
        esp_p = {'Conhecimentos mapeados': r['cons'], 'Crítico': r['sits']['Crítico'], 'Em risco': r['sits']['Em risco'], 'Sob controle': r['sits']['Sob controle'],
                 'Expostos sem ação de transferência': r['semacao'], 'Ações de transferência vencidas': r['vencidas'], 'Lições registradas': r['lics'],
                 'Lições pendentes': r['pend'], f'Pendentes há mais de {PRAZO_LICAO} dias': r['velhas'], 'Produtos com política': r['pols'],
                 'Prazo aceito menor que o mínimo': r['menor'], 'Atendimentos': r['ats'], 'Abertos': r['abertos'], 'Fora do prazo, resolvidos ou não': r['foraprazo'],
                 'Resolvidos no prazo': r['noprazo'], 'Custo dos atendimentos': r['custo'],
                 'Linhas a completar': r['con_rever'] + r['lic_rever'] + r['pol_rever'] + r['at_rever']}
        dif = {k: (pa[k], x) for k, x in esp_p.items() if (round(pa[k], 6) if isinstance(pa[k], float) else pa[k]) != (round(x, 6) if isinstance(x, float) else x)}
        print('            painel igual ao exemplo:', 'OK' if not dif else 'DIFERE %s' % dif)
    print('Checklist ', [C[f'D{r}'].value for r in range(19, 25)])
