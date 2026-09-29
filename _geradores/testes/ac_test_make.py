"""Confere Analise-Critica-modelo.xlsx e preenche cópias com dados de teste.  Uso: ac_test_make.py <modelo.xlsx> <pasta de saída>"""
import openpyxl, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ac_data import EX1, EX2, ITENS, SITS, TIPOS, decisoes, situacao_acao
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
print('vazio:', wb['Reunião']['E41'].value, '|', wb['Ações anteriores']['E31'].value, '|', wb['Entradas']['E26'].value, '|', wb['Saídas']['E29'].value,
      '|', wb['Checklist']['D24'].value)

# exemplos: valores da planilha contra os dados
for nome, ex in (('Exemplo 1 - Pizzaria', EX1), ('Exemplo 2 - Indústria', EX2)):
    s = wb[nome]
    linhas = [r for r in range(1, s.max_row + 1) if s[f'B{r}'].value in ITENS]
    dec = [s[f'I{r}'].value for r in linhas]
    ok1 = dec == [len(decisoes(ex, i)) for i in ITENS]
    sit = [s[f'J{r}'].value for r in range(1, s.max_row + 1) if isinstance(s[f'B{r}'].value, int) and isinstance(s[f'J{r}'].value, str)]
    ok2 = sit == [situacao_acao(a, ex['head']['data']) for a in ex['anteriores']]
    res = {s[f'B{r}'].value: s[f'E{r}'].value for r in range(linhas[-1], s.max_row + 1) if isinstance(s[f'B{r}'].value, str) and s[f'C{r}'].value is None}
    e = ex['entradas']
    esperado = {'Entradas analisadas, de 12': 12,
                'Favoráveis, em atenção e críticas': '%d, %d e %d' % tuple(sum(1 for x in e if x['sit'] == t) for t in SITS),
                'Críticas sem decisão': 0, 'Decisões registradas': len(ex['saidas']),
                'De melhoria, de mudança no sistema e de recursos': '%d, %d e %d' % tuple(sum(1 for x in ex['saidas'] if x['tipo'] == t) for t in TIPOS),
                'Valor total aprovado': sum(x['valor'] or 0 for x in ex['saidas'])}
    ok3 = all(res.get(k) == v for k, v in esperado.items())
    print(nome, '| decisões por entrada', 'OK' if ok1 else 'DIFERE %s' % dec, '| situação das ações', 'OK' if ok2 else 'DIFERE %s' % sit,
          '| resumo', 'OK' if ok3 else 'DIFERE %s' % res)


def preencher(nome, ex=None, reuniao=None, acoes=(), entradas=None, saidas=(), sistema=None, check=None, extra=None):
    w = openpyxl.load_workbook(SRC)
    R, A, E, S, C = w['Reunião'], w['Ações anteriores'], w['Entradas'], w['Saídas'], w['Checklist']
    if ex:
        h = ex['head']
        reuniao = dict({'D4': h['org'], 'D5': h['data'], 'D6': h['periodo'], 'D7': h['local'], 'D8': h['conduz'], 'D9': h['secretario'], 'D10': h['anterior'],
                        'D11': h['proxima']}, **(reuniao or {}))
        for k, p in enumerate(ex['part']):
            for col, v in zip('CDEF', p):
                R[f'{col}{16 + k}'] = v
        acoes = acoes or [(a['origem'], a['acao'], a['quem'], a['prazo'], a['status'], a['feito'], a['eficaz'] or None, a['obs'] or None) for a in ex['anteriores']]
        if entradas is None:
            entradas = {e['item']: (e['quem'], e['fonte'], e['resultado'], e['tend'], e['sit'], e['conclusao']) for e in ex['entradas']}
        saidas = saidas or [(x['item'], x['tipo'], x['decisao'], x['quem'], x['prazo'], x['recurso'] or None, x['valor']) for x in ex['saidas']]
        if sistema is None:
            sistema = ex['sistema']
    for ref, v in (reuniao or {}).items():
        if v is not None:
            R[ref] = v
    for k, row in enumerate(acoes):
        for col, v in zip('CDEFGHIJ', row):
            if v is not None:
                A[f'{col}{9 + k}'] = v
    for item, row in (entradas or {}).items():
        r = 6 + ITENS.index(item)
        for col, v in zip('EFGHIJ', row):
            if v is not None:
                E[f'{col}{r}'] = v
    for k, row in enumerate(saidas):
        for col, v in zip('CEFGHIJ', row):
            if v is not None:
                S[f'{col}{7 + k}'] = v
    for k, row in enumerate(sistema or ()):
        for col, v in zip('FG', row):
            if v is not None:
                R[f'{col}{29 + k}'] = v
    for k, v in enumerate(check or ()):
        if v:
            C[f'D{5 + k}'] = v
    for (aba, ref), v in (extra or {}).items():
        w[aba][ref] = v
    w.save(OUTDIR + '/%s.xlsx' % nome)


D = date
# t1: indústria completa, tudo correto
preencher('t1', EX2, check=['Sim'] * 12)
# t2: pizzaria, primeira análise, sem ações anteriores e sem data da análise anterior
preencher('t2', EX1, check=['Sim'] * 6 + ['Parcial', 'Não'])
# t3: erros propositais
ent = {e['item']: (e['quem'], e['fonte'], e['resultado'], e['tend'], e['sit'], e['conclusao']) for e in EX2['entradas']}
ent['b'] = ('Diretor', 'SWOT', None, 'Estável', 'Atenção', 'Conclusão')          # falta o resultado
ent['c1'] = ('Gerente', 'Pesquisa', 'Resultado', None, 'Atenção', 'Conclusão')   # falta a tendência
ent['c4'] = ('Coordenador', 'Controle', 'Resultado', 'Piorando', None, None)     # falta a situação
ent['c5'] = ('Coordenador', 'Painel', 'Resultado', 'Estável', 'Favorável', None)  # falta a conclusão
del ent['f']                                                                     # não analisada
preencher('t3', EX2, reuniao={'D11': D(2027, 1, 10)}, entradas=ent,
          acoes=[(D(2026, 8, 13), 'Ação sem prazo', 'Gerente', None, 'Em andamento', None, None, None),
                 (D(2026, 8, 13), 'Ação sem status', 'Gerente', D(2026, 10, 30), None, None, None, None),
                 (D(2026, 8, 13), 'Ação concluída sem data', 'Gerente', D(2026, 10, 30), 'Concluída', None, 'Sim', None),
                 (D(2026, 8, 13), 'Ação concluída sem eficácia', 'Gerente', D(2026, 10, 30), 'Concluída', D(2026, 10, 1), None, None),
                 (D(2026, 8, 13), 'Ação cancelada', 'Gerente', D(2026, 10, 30), 'Cancelada', None, None, 'Mudou a prioridade'),
                 (D(2026, 8, 13), 'Ação no prazo', 'Gerente', D(2027, 5, 30), 'Em andamento', None, None, None),
                 (D(2026, 8, 13), 'Ação atrasada', 'Gerente', D(2027, 2, 17), 'Não iniciada', None, None, None),
                 (D(2026, 8, 13), 'Ação com prazo na data da reunião', 'Gerente', D(2027, 2, 18), 'Em andamento', None, None, None)],
          saidas=[('a', 'Melhoria', 'Decisão completa', 'Gerente', D(2027, 3, 1), None, None),
                  (None, 'Melhoria', 'Sem entrada', 'Gerente', D(2027, 3, 1), None, None),
                  ('b', None, 'Sem tipo', 'Gerente', D(2027, 3, 1), None, None),
                  ('c1', 'Melhoria', 'Sem responsável', None, D(2027, 3, 1), None, None),
                  ('c2', 'Melhoria', 'Sem prazo', 'Gerente', None, None, None),
                  ('c6', 'Mudança no sistema', 'Prazo anterior à reunião', 'Gerente', D(2027, 2, 1), None, None),
                  ('d', 'Recursos', 'Recurso sem descrição', 'Gerente', D(2027, 3, 1), None, None),
                  ('d', 'Recursos', 'Recurso só com valor', 'Gerente', D(2027, 3, 1), None, 5000),
                  ('z9', 'Melhoria', 'Entrada que não existe', 'Gerente', D(2027, 3, 1), None, None),
                  ('c4', 'Melhoria', None, 'Gerente', D(2027, 3, 1), None, None)],   # sem a decisão; as entradas críticas c3 e "e" ficam sem decisão
          sistema=[('Sim', 'Justificativa'), ('Parcial', None), ('Não', 'Justificativa'), (None, None)])
# t4: reunião sem a alta direção e sem avaliação do sistema; planilha sem data usa a data de hoje
preencher('t4', reuniao={'D4': 'Teste', 'D5': D(2027, 2, 18), 'D10': D(2026, 2, 18), 'C16': 'Ana', 'D16': 'Analista', 'E16': 'Não', 'F16': 'Presente',
                         'C17': 'Diretor', 'D17': 'Direção', 'E17': 'Sim', 'F17': 'Ausente'},
          entradas={i: ('Quem', 'Fonte', 'Nada a relatar', 'Estável', 'Favorável', 'Manter') for i in ITENS},
          saidas=[('f', 'Melhoria', 'Decisão', 'Gerente', D(2027, 3, 1), None, None)])
# t5: sem data da reunião (a situação das ações usa a data de hoje)
preencher('t5', acoes=[(D(2020, 1, 10), 'Ação antiga', 'Gerente', D(2020, 6, 30), 'Em andamento', None, None, None),
                       (D(2020, 1, 10), 'Ação futura', 'Gerente', D(2099, 6, 30), 'Em andamento', None, None, None)])
print('ok')
