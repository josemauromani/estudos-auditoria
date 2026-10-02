"""Lê os resultados dos testes de Recursos-modelo.xlsx depois do recálculo.  Uso: rec_test_read.py <pasta com t1..t3.xlsx>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PASTA = sys.argv[1]
import rec_data as R
from rec_data import EX1, EX2, amb_conf, amb_sit, cap_conf, cap_sit, disp, infra_conf, necessarias, oc_conf, paradas, prev_sit, resumo

# os casos de borda vêm do roteiro de preenchimento, sem regravar as cópias
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rec_test_make.py'), encoding='utf-8').read()
_ns = {}
exec(_src[_src.index('D = date'):_src.index("preencher('t3'")], {'date': __import__('datetime').date, **vars(R)}, _ns)


def mk(caps, infra, ocs, amb, head):
    return dict(head=head, caps=R._caps(caps), infra=[dict(zip(("cod", "nome", "tipo", "local", "crit", "interv", "ultima", "cont", "prog"), r)) for r in infra],
                ocs=[dict(zip(("data", "cod", "tipo", "horas", "oque", "causa", "acao", "afetou", "trat"), r)) for r in ocs], amb=R._amb(amb))


EX3 = mk(_ns['caps3'], _ns['infra3'], _ns['ocs3'], _ns['amb3'], _ns['H3'])
PAINEL = {'Funções e períodos': 7, 'Com falta de gente': 8, 'Pessoas a menos no pico': 9, 'Sem pessoa qualificada': 10, 'Itens cadastrados': 12, 'Itens críticos': 13,
          'Atrasada': 14, 'Vence em 7 dias': 15, 'Críticos sem contingência': 16, 'Abaixo da meta de disponibilidade': 17, 'Quebras no período': 18,
          'Horas paradas no período': 19, 'Corretivas com produto afetado': 21, 'Produto afetado sem tratamento': 22, 'Fatores do ambiente fora do limite': 23,
          'Fora do limite sem ação': 24, 'Fatores sem medição': 25, 'Linhas a completar': 26}


def dd(v):
    return v.date() if hasattr(v, 'date') else v


def r4(v):
    return round(v, 4) if isinstance(v, float) else v


for nome, ex in (('t1', EX1), ('t2', EX2), ('t3', EX3)):
    w = openpyxl.load_workbook(f'{PASTA}/{nome}.xlsx', data_only=True)
    P, I, M, A, Pa, K = w['Pessoas'], w['Infraestrutura'], w['Manutenções'], w['Ambiente'], w['Painel'], w['Checklist']
    h = ex['head']
    print('=====', nome)
    err = [(ws.title, c.coordinate, c.value) for ws in w.worksheets[:6] for r in ws.iter_rows() for c in r
           if isinstance(c.value, str) and ((c.value.startswith('#') and len(c.value) > 1) or 'Err:' in c.value)]
    print('erros', err)
    # o openpyxl lê como None o texto vazio que a fórmula devolve
    got_p = [tuple('' if P[f'{c}{r}'].value is None else P[f'{c}{r}'].value for c in 'HLM') for r in range(7, 7 + len(ex['caps']))]
    esp_p = [(necessarias(c) if necessarias(c) is not None else '', cap_sit(c), cap_conf(c)) for c in ex['caps']]
    got_i = [(I[f'M{r}'].value, I[f'N{r}'].value, I[f'O{r}'].value, r4(I[f'P{r}'].value) if I[f'P{r}'].value != '' else None, I[f'Q{r}'].value)
             for r in range(10, 10 + len(ex['infra']))]
    esp_i = [(prev_sit(i, h['ref']), *paradas(i, ex['ocs'], h['ini'], h['fim']), r4(disp(i, ex['ocs'], h['ini'], h['fim'])), infra_conf(i, ex)) for i in ex['infra']]
    got_m = [M[f'M{r}'].value for r in range(7, 7 + len(ex['ocs']))]
    esp_m = ['Falta o item' if not o['cod'] else oc_conf(o, ex['infra']) for o in ex['ocs']]
    got_a = [(A[f'M{r}'].value, A[f'N{r}'].value) for r in range(7, 7 + len(ex['amb']))]
    esp_a = [(amb_sit(a), amb_conf(a)) for a in ex['amb']]
    for rot, g, e in (('Pessoas', got_p, esp_p), ('Infra', got_i, esp_i), ('Manutenções', got_m, esp_m), ('Ambiente', got_a, esp_a)):
        print('%-12s' % rot, 'OK' if g == e else 'DIFERE\n   planilha %s\n   esperado %s' % (g, e))
    pa = {k: Pa[f'C{r}'].value for k, r in PAINEL.items()}
    print('Painel    ', pa)
    print('Avisos    ', [P['E41'].value, I['E55'].value, M['E91'].value, A['E41'].value, Pa['C29'].value])
    if nome != 't3':
        r = resumo(ex)
        esp = {'Funções e períodos': r['caps'], 'Com falta de gente': r['cap_falta'], 'Pessoas a menos no pico': r['pessoas'], 'Sem pessoa qualificada': r['semqual'],
               'Itens cadastrados': r['infra'], 'Itens críticos': r['criticos'], 'Atrasada': r['sits']['Atrasada'], 'Vence em 7 dias': r['sits']['Vence em 7 dias'],
               'Críticos sem contingência': r['semcont'], 'Abaixo da meta de disponibilidade': r['abaixo'], 'Quebras no período': r['corr'], 'Horas paradas no período': r['horas'],
               'Corretivas com produto afetado': r['afetou'], 'Produto afetado sem tratamento': r['semtrat'], 'Fatores do ambiente fora do limite': r['fora'],
               'Fora do limite sem ação': sum(1 for a in ex['amb'] if amb_conf(a) == 'Fora do limite: falta a ação'), 'Fatores sem medição': r['semmed'],
               'Linhas a completar': r['cap_rever'] + r['infra_rever'] + r['oc_rever'] + r['amb_rever']}
        print('            painel igual ao exemplo:', 'OK' if pa == esp else 'DIFERE %s' % {k: (pa[k], v) for k, v in esp.items() if pa[k] != v})
    print('Checklist ', [K[f'D{r}'].value for r in range(19, 25)])
