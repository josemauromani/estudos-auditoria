"""Lê os resultados dos testes de Pedidos-modelo.xlsx depois do recálculo.  Uso: ped_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ped_data import EX1, EX2, conf, leitura, mud_conf, nao_por_pergunta, oferta_conf, resumo
D = sys.argv[1]
for nome, ex in (('t1', EX1), ('t2', EX2), ('t3', None)):
    w = openpyxl.load_workbook(f'{D}/{nome}.xlsx', data_only=True)
    O, P, M, Pa, K = w['Oferta'], w['Pedidos'], w['Mudanças'], w['Painel'], w['Checklist']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:6] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    of = [O[f'I{r}'].value for r in range(6, 18) if O[f'I{r}'].value]
    pe = [(P[f'Q{r}'].value, P[f'R{r}'].value, P[f'X{r}'].value) for r in range(7, 67) if P[f'X{r}'].value]
    mu = [M[f'J{r}'].value for r in range(7, 37) if M[f'J{r}'].value]
    print('Oferta    ', of, '|', O['D21'].value)
    print('Pedidos   ', pe if not ex else 'linhas %d' % len(pe), '| resumo', [P[f'E{r}'].value for r in range(69, 73)])
    print('Mudanças  ', mu, '| resumo', [M[f'E{r}'].value for r in range(39, 42)])
    ind = [Pa[f'C{r}'].value for r in range(5, 18)]
    nao = [Pa[f'D{r}'].value for r in range(21, 28)]
    print('Painel    ', ind, '| não por pergunta', nao, '| aviso', Pa['C30'].value)
    if ex:
        r = resumo(ex)
        ok_p = [(a, c) for a, b, c in pe] == [(leitura(p), conf(p)) for p in ex['peds']]
        ok_o = of == [oferta_conf(o) for o in ex['ofertas']]
        ok_m = mu == [mud_conf(m) for m in ex['muds']]
        ok_n = nao == nao_por_pergunta(ex)
        ok_i = (ind[2], ind[3], ind[4], ind[5], ind[6], ind[7], ind[8], ind[11], ind[12]) == (r['peds'], r['dec']['Aceito'], r['dec']['Aceito com alteração'], r['dec']['Recusado'],
                                                                                              r['dec']['Em análise'], r['com_pend'], r['rever'], r['muds'], r['mud_rever'])
        print('            igual ao exemplo: pedidos', 'OK' if ok_p else 'DIFERE %s' % pe, '| oferta', 'OK' if ok_o else 'DIFERE', '| mudanças', 'OK' if ok_m else 'DIFERE',
              '| não por pergunta', 'OK' if ok_n else 'DIFERE', '| indicadores', 'OK' if ok_i else 'DIFERE')
    print('Checklist ', [K[f'D{r}'].value for r in range(19, 25)])
