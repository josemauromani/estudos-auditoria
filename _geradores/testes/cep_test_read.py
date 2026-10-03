"""Lê os resultados dos testes de Histograma-CEP-modelo.xlsx depois do recálculo.  Uso: cep_test_read.py <pasta com t1..t7.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import cep_data as R
from cep_data import (ACOMP, BASE, EX1, EX2, EXCL, LIMITE, NAOCAPAZ, SINAIS, amp, capacidade, classes, conf, fase, fora_espec, histograma, limites, media, sinal)
PASTA = sys.argv[1]

# os casos de borda vêm do roteiro de preenchimento, sem regravar as cópias
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cep_test_make.py'), encoding='utf-8').read()
_ns = {}
exec(_src[_src.index('D = date'):_src.index("preencher('t3'")], {'date': __import__('datetime').date, **vars(R)}, _ns)
exec(_src[_src.index('EX5 = '):_src.index('for nome, ex in ((')], {'EX1': EX1, 'EX2': EX2}, _ns)
PAINEL = {'Subgrupos completos': 7, 'Na base': 8, 'Excluídos': 9, 'Em acompanhamento': 10, 'Linhas a completar': 11, R.S_FORA: 13, R.S_AMP: 14, R.S_LADO: 15,
          R.S_TEND: 16, 'Sinais na base': 17, 'Sinais no acompanhamento': 18, 'Primeiro sinal no acompanhamento': 19, 'Medições': 21,
          'Medições fora da especificação': 22, 'Cp': 23, 'Cpk': 24, 'Situação da capacidade': 25}


def v(c):
    x = c.value
    return '' if x is None else (x.date() if hasattr(x, 'date') else x)


def e(x):
    return '' if x is None else x


def rnd(x):
    return round(x, 6) if isinstance(x, float) else x


def aviso(p):
    if p['Subgrupos completos'] == 0:
        return 'Lance os subgrupos na aba Dados'
    if p['Na base'] < 20:
        return 'Base com menos de 20 subgrupos: limites provisórios'
    if p['Linhas a completar'] > 0:
        return 'Há linha a completar: veja a coluna Conferência'
    if p['Sinais na base'] > 0:
        return 'Há sinal na base: procure a causa e exclua o subgrupo'
    if p['Sinais no acompanhamento'] > 0:
        return 'Há sinal no acompanhamento: procure a causa e anote a ação'
    if p['Situação da capacidade'] == NAOCAPAZ:
        return 'Processo em controle, mas não capaz: mude o processo'
    if p['Situação da capacidade'] == LIMITE:
        return 'Capacidade no limite: acompanhe de perto'
    return 'OK'


for nome, ex in (('t1', EX1), ('t2', EX2), ('t3', _ns['EX3']), ('t4', _ns['EX4']), ('t5', _ns['EX5']), ('t6', _ns['EX6']), ('t7', _ns['EX7'])):
    w = openpyxl.load_workbook(f'{PASTA}/{nome}.xlsx', data_only=True)
    Dd, G, Hs, Pa, K = w['Dados'], w['Gráficos'], w['Histograma'], w['Painel'], w['Checklist']
    print('=====', nome)
    err = [(ws.title, x.coordinate, x.value) for ws in w.worksheets[:5] if ws.title != 'Gráficos' for r in ws.iter_rows() for x in r
           if isinstance(x.value, str) and ((x.value.startswith('#') and len(x.value) > 1) or 'Err:' in x.value)]
    print('erros', err)
    subs = ex['subs']
    L = limites(ex)
    got = [tuple(rnd(v(Dd[f'{c}{13 + k}'])) for c in 'LMNOPQ') for k in range(len(subs))]
    esp = [(rnd(e(media(g['v']))), rnd(e(amp(g['v']))), fase(ex, k), fora_espec(ex, g['v']) if any(x is not None for x in g['v']) else '', sinal(ex, k, L), conf(g))
           for k, g in enumerate(subs)]
    vaz = [tuple(v(Dd[f'{c}{r}']) for c in 'LMNOPQ') for r in range(13 + len(subs), 43)]
    gl = [rnd(v(Dd[f'L{r}'])) for r in range(4, 11)]
    el = [L['n'], rnd(L['lc']), rnd(L['lsc']), rnd(L['lic']), rnd(L['rb']), rnd(L['lscr']), rnd(L['sigma'])]
    h = histograma(ex)
    gh = [v(Hs[f'E{r}']) for r in range(8, 20)] + [v(Hs['E20']), v(Hs['E21'])]
    eh = h['cont'] + [h['abaixo'], h['acima']]
    gc = [(rnd(v(Hs[f'C{r}'])), rnd(v(Hs[f'D{r}']))) for r in range(8, 20)]
    ec = [(rnd(a), rnd(b)) for a, b in classes(ex)]
    print('Linhas    ', 'OK' if got == esp else 'DIFERE\n   planilha %s\n   esperado %s' % ([x for x, y in zip(got, esp) if x != y], [y for x, y in zip(got, esp) if x != y]))
    print('Vazias    ', 'OK' if all(t == ('',) * 6 for t in vaz) else 'DIFERE %s' % vaz)
    print('Limites   ', 'OK' if gl == el else 'DIFERE %s %s' % (gl, el))
    print('Histograma', 'OK' if (gh, gc) == (eh, ec) else 'DIFERE %s %s' % (gh, gc))
    fases = [fase(ex, k) for k in range(len(subs))]
    sg = [sinal(ex, k, L) for k in range(len(subs))]
    cap = capacidade(ex, L)
    prim = next((subs[k]['data'] for k in range(len(subs)) if sg[k] and fases[k] == ACOMP), '')
    situ = '' if cap is None else ('Base com sinal: trate antes' if cap['base_sinal'] else cap['status'])
    espp = {'Subgrupos completos': sum(1 for g in subs if media(g['v']) is not None), 'Na base': fases.count(BASE), 'Excluídos': fases.count(EXCL),
            'Em acompanhamento': fases.count(ACOMP), 'Linhas a completar': sum(1 for g in subs if conf(g) not in ('', 'OK')),
            **{s: sg.count(s) for s in SINAIS}, 'Sinais na base': sum(1 for f, s in zip(fases, sg) if f == BASE and s),
            'Sinais no acompanhamento': sum(1 for f, s in zip(fases, sg) if f == ACOMP and s), 'Primeiro sinal no acompanhamento': prim,
            'Medições': h['n'], 'Medições fora da especificação': h['fora'], 'Cp': rnd(cap['cp']) if cap else '', 'Cpk': rnd(cap['cpk']) if cap else '', 'Situação da capacidade': situ}
    pa = {k: rnd(v(Pa[f'C{r}'])) for k, r in PAINEL.items()}
    dif = {k: (pa[k], x) for k, x in espp.items() if pa[k] != x}
    print('Painel    ', 'OK' if not dif else 'DIFERE %s' % dif)
    print('Aviso     ', 'OK' if v(Pa['C28']) == aviso(espp) else 'DIFERE %s esperado %s' % (v(Pa['C28']), aviso(espp)), '|', v(Pa['C28']))
    nas = sum(1 for r in range(5, 35) for c in 'CDEFGHI' if isinstance(G[f'{c}{r}'].value, str) and G[f'{c}{r}'].value.startswith('#'))
    print('Gráficos  ', 'pontos', sum(1 for r in range(5, 35) if isinstance(G[f'C{r}'].value, (int, float))), '| #N/D', nas)
    print('Resumo    ', {k: espp[k] for k in ('Na base', 'Sinais no acompanhamento', 'Cp', 'Cpk', 'Situação da capacidade')})
    print('Checklist ', [K[f'D{r}'].value for r in range(19, 25)])
