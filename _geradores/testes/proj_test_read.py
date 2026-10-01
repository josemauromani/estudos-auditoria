"""Lê os resultados dos testes de Projeto-modelo.xlsx depois do recálculo.  Uso: proj_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from proj_data import EX1, EX2, entrada_conf, etapa_conf, mud_conf, por_tipo, resumo
D = sys.argv[1]
for nome, ex in (('t1', EX1), ('t2', EX2), ('t3', None)):
    w = openpyxl.load_workbook(f'{D}/{nome}.xlsx', data_only=True)
    P, E, M, Pa, K = w['Plano'], w['Entradas'], w['Mudanças'], w['Painel'], w['Checklist']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:6] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    et = [P[f'L{r}'].value for r in range(14, 34) if P[f'L{r}'].value]
    en = [E[f'K{r}'].value for r in range(7, 37) if E[f'K{r}'].value]
    mu = [M[f'I{r}'].value for r in range(7, 27) if M[f'I{r}'].value]
    print('Plano     ', et if not ex else 'linhas %d' % len(et), '| resumo', [P[f'D{r}'].value for r in range(36, 40)])
    print('Entradas  ', en if not ex else 'linhas %d' % len(en), '| resumo', [E[f'D{r}'].value for r in range(39, 43)])
    print('Mudanças  ', mu, '| resumo', [M[f'D{r}'].value for r in range(29, 32)])
    ind = [Pa[f'C{r}'].value for r in range(6, 18)]
    ctl = [(Pa[f'C{r}'].value, Pa[f'D{r}'].value, Pa[f'E{r}'].value, Pa[f'F{r}'].value) for r in range(21, 24)]
    tip = [(Pa[f'C{r}'].value, Pa[f'D{r}'].value, Pa[f'E{r}'].value, Pa[f'F{r}'].value) for r in range(27, 34)]
    print('Painel    ', ind, Pa['D17'].value, '| controles', ctl, '| aviso', Pa['C36'].value)
    print('Por tipo  ', tip)
    if ex:
        ref, es = ex['head']['ref'], ex['etps']
        r = resumo(ex)
        ok_e = et == [etapa_conf(e, ref, es) for e in es]
        ok_x = en == [entrada_conf(x) for x in ex['ents']]
        ok_m = mu == [mud_conf(m) for m in ex['muds']]
        ok_t = tip == [(x['n'], x['at'], x['nao'], x['pend']) for x in por_tipo(ex)]
        ok_i = (ind[0], ind[1], ind[2], ind[4], ind[5], ind[6], ind[7], ind[8], ind[9], ind[10]) == (r['etapas'], r['concl'], r['atras'], r['valid_ok'], r['ents'], r['at'], r['nao'],
                                                                                                   r['pend'], r['muds'], r['mud_rever'])
        print('            igual ao exemplo: etapas', 'OK' if ok_e else 'DIFERE %s' % et, '| entradas', 'OK' if ok_x else 'DIFERE %s' % en, '| mudanças', 'OK' if ok_m else 'DIFERE',
              '| por tipo', 'OK' if ok_t else 'DIFERE', '| indicadores', 'OK' if ok_i else 'DIFERE')
    print('Checklist ', [K[f'D{r}'].value for r in range(19, 25)])
