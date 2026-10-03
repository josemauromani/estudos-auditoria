"""Lê os resultados dos testes de ISO-9001-2026-modelo.xlsx depois do recálculo.  Uso: ed26_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import ed26_data as R
from ed26_data import (ATRAS, CONCL, EX1, EX2, IMPACTOS, LACUNA, MUDANCAS, NOPRAZO, P_ALTA, P_ATRAS, P_MEDIA, P_VENCE, PASSOS, acao_sit, diag_conf, limite_passo,
                       passo_sit)
PASTA = sys.argv[1]

# os casos de borda vêm do roteiro de preenchimento, sem regravar as cópias
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ed26_test_make.py'), encoding='utf-8').read()
_ns = {}
exec(_src[_src.index('D = date'):_src.index("preencher('t3'")], {'date': __import__('datetime').date, **vars(R)}, _ns)
DEPOIS = "A auditoria está depois do fim da transição"
PAINEL = {'Atende': 7, 'Atende em parte': 8, 'Não atende': 9, 'Prioridade alta': 10, 'Prioridade média': 11, 'Pontos de lacuna': 12, 'Ações': 13, 'Ações concluídas': 14,
          'Ações atrasadas': 15, 'Linhas a completar': 16, 'Data da auditoria': 18, 'Alerta de prazo': 19, 'Etapas atrasadas': 20, 'Etapas que vencem em 30 dias': 21,
          'Próximo limite': 22, 'Próxima etapa': 23}


def v(c):
    x = c.value
    return '' if x is None else (x.date() if hasattr(x, 'date') else x)


def e(x):
    return '' if x is None else x


def linhas(nome):
    """As mudanças de cada teste, com o impacto de cada linha (fixo nas nove, digitado nas livres)."""
    if nome == 't1':
        return [(m, d) for m, d in zip(MUDANCAS, EX1['diag'])], EX1['head']['ref'], EX1['plano'], 'Sem certificado'
    if nome == 't2':
        return [(m, d) for m, d in zip(MUDANCAS, EX2['diag'])], EX2['head']['ref'], EX2['plano'], 'Certificado pela edição de 2015'
    rows = [(m, d) for m, d in zip(MUDANCAS, _ns['diag3'])] + [(d['m'][:4] + (d['m'][4],), d) for d in _ns['livres3']]
    return rows, _ns['REF3'], _ns['plano3'], 'Certificado pela edição de 2015'


def pts(m, sit):
    if not sit or not m[4]:
        return ''
    return IMPACTOS[m[4]] * LACUNA[sit]


def pri(m, sit):
    p = pts(m, sit)
    return '' if p == '' else (P_ALTA if p >= 4 else P_MEDIA if p >= 2 else R.P_BAIXA if p >= 1 else R.P_SEM)


for nome in ('t1', 't2', 't3'):
    w = openpyxl.load_workbook(f'{PASTA}/{nome}.xlsx', data_only=True)
    M, P, Pa, K = w['Mudanças'], w['Plano'], w['Painel'], w['Checklist']
    rows, ref, pl, cert = linhas(nome)
    print('=====', nome)
    err = [(ws.title, x.coordinate, x.value) for ws in w.worksheets[:5] for r in ws.iter_rows() for x in r
           if isinstance(x.value, str) and ((x.value.startswith('#') and len(x.value) > 1) or 'Err:' in x.value)]
    print('erros', err)
    got_d = [(v(M[f'O{8 + k}']), v(M[f'P{8 + k}']), v(M[f'Q{8 + k}']), v(M[f'R{8 + k}'])) for k in range(len(rows))]
    esp_d = [(pts(m, d['sit']), pri(m, d['sit']), acao_sit(d, ref), diag_conf(d)) for m, d in rows]
    got_p = [(v(P[f'E{r}']), v(P[f'G{r}']), v(P[f'I{r}'])) for r in range(12, 12 + len(PASSOS))]
    esp_p = [(limite_passo(pl['audit'], k), passo_sit(pl, k), e(None if pl['feito'][k] else limite_passo(pl['audit'], k))) for k in range(len(PASSOS))]
    vazias = [(v(M[f'O{r}']), v(M[f'Q{r}']), v(M[f'R{r}'])) for r in range(8 + len(rows), 23)]
    for rot, g, x in (('Mudanças', got_d, esp_d), ('Plano', got_p, esp_p)):
        print('%-10s' % rot, 'OK' if g == x else 'DIFERE\n   planilha %s\n   esperado %s' % (g, x))
    print('Vazias    ', 'OK' if all(t == ('', '', '') for t in vazias) else 'DIFERE %s' % vazias)
    alerta = DEPOIS if cert.startswith('Certificado') and pl['audit'] > pl['fim'] else 'OK'
    print('Alerta    ', 'OK' if v(P['D9']) == alerta else 'DIFERE %s esperado %s' % (v(P['D9']), alerta))
    pa = {k: v(Pa[f'C{r}']) for k, r in PAINEL.items()}
    sits = [d['sit'] for m, d in rows]
    pris = [x[1] for x in esp_d]
    acs = [x[2] for x in esp_d]
    ps = [x[1] for x in esp_p]
    pend = [(l, PASSOS[k][0]) for k, (l, _, p) in enumerate(esp_p) if p != '']
    prox = min(pend) if pend else ('', '')
    esp = {'Atende': sits.count(R.ATENDE), 'Atende em parte': sits.count(R.PARCIAL), 'Não atende': sits.count(R.NAOATENDE), 'Prioridade alta': pris.count(P_ALTA),
           'Prioridade média': pris.count(P_MEDIA), 'Pontos de lacuna': sum(x[0] for x in esp_d if x[0] != ''),
           'Ações': sum(1 for a in acs if a in (CONCL, NOPRAZO, ATRAS)), 'Ações concluídas': acs.count(CONCL), 'Ações atrasadas': acs.count(ATRAS),
           'Linhas a completar': sum(1 for x in esp_d if x[3] != 'OK'), 'Data da auditoria': pl['audit'], 'Alerta de prazo': alerta,
           'Etapas atrasadas': ps.count(P_ATRAS), 'Etapas que vencem em 30 dias': ps.count(P_VENCE), 'Próximo limite': prox[0], 'Próxima etapa': prox[1]}
    dif = {k: (pa[k], x) for k, x in esp.items() if pa[k] != x}
    print('Painel    ', 'OK' if not dif else 'DIFERE %s' % dif)
    if nome in ('t1', 't2'):
        r = R.resumo(EX1 if nome == 't1' else EX2)
        ok = (r['pts'], r['atras'], r['diag_rever']) == (esp['Pontos de lacuna'], esp['Ações atrasadas'], esp['Linhas a completar'])
        print('Resumo    ', 'OK' if ok else 'DIFERE %s' % r)
    print('Avisos    ', [M['E27'].value, P['E23'].value, Pa['C26'].value])
    print('Checklist ', [K[f'D{r}'].value for r in range(19, 25)])
