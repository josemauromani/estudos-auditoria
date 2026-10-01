# Geradores dos estudos

Esta pasta guarda os scripts que geram os treinamentos (HTML) e as planilhas (XLSX) dos estudos. Quem só lê os estudos não precisa dela: basta abrir o `index.html` da pasta principal.

## O que é gerado e o que é escrito à mão

| Arquivo | Origem |
|---|---|
| `SIPOC/` (treinamento e planilha) | Escrito à mão. Não tem gerador. |
| `PDCA/treinamento-pdca.html` | Escrito à mão. É a fonte do CSS de todos os outros treinamentos. |
| `PDCA/PDCA-modelo.xlsx` | Gerado por `build_pdca.py`. |
| Treinamentos dos outros estudos | Gerados por `build_<estudo>_html.py`, a partir de `<estudo>_body.html` e de `<estudo>_data.py`. |
| Planilhas dos outros estudos | Geradas por `build_<estudo>.py`, a partir de `<estudo>_data.py`. |
| `index.html` | Escrito à mão. |

Os nomes curtos dos estudos são:

| Nome | Estudo | Pasta |
|---|---|---|
| `pdca` | PDCA | `PDCA/` |
| `swot` | Matriz SWOT | `SWOT/` |
| `gut` | Matriz GUT | `GUT/` |
| `w5` | 5W2H | `5W2H/` |
| `ish` | Diagrama de Ishikawa | `Ishikawa/` |
| `raci` | Matriz RACI | `RACI/` |
| `aud` | Auditoria interna | `Auditoria/` |
| `nc` | Não conformidade e ação corretiva | `Nao-Conformidade/` |
| `iso` | ISO 9001 requisito a requisito | `ISO-9001/` |
| `risk` | Matriz de riscos | `Riscos/` |
| `ind` | Indicadores | `Indicadores/` |
| `proc` | Mapa de processos e diagrama de tartaruga | `Processos/` |
| `ac` | Análise crítica pela direção | `Analise-Critica/` |
| `doc` | Informação documentada | `Informacao-Documentada/` |
| `comp` | Matriz de competências e treinamento | `Competencias/` |
| `forn` | Avaliação de fornecedores | `Fornecedores/` |
| `sat` | Satisfação do cliente | `Satisfacao/` |
| `par` | Pareto e folha de verificação | `Pareto/` |
| `pi` | Partes interessadas | `Partes-Interessadas/` |
| `obj` | Objetivos da qualidade | `Objetivos/` |
| `prod` | Controle de produção e de serviço | `Producao/` |
| `lib` | Liberação e produto não conforme | `Liberacao/` |
| `ped` | Requisitos do cliente e análise de pedidos | `Pedidos/` |
| `proj` | Projeto e desenvolvimento | `Projeto/` |
| `esc` | Escopo e liderança | `Escopo/` |

## Preparação

Os scripts precisam de Python 3, da biblioteca `openpyxl` e do LibreOffice (comando `soffice`).

```bash
python3 -m venv _geradores/.venv
_geradores/.venv/bin/pip install -r _geradores/requirements.txt
```

## Como gerar

```bash
_geradores/gerar.sh risk              # gera um estudo, na pasta dele
_geradores/gerar.sh todos             # gera todos
_geradores/gerar.sh risk /tmp/teste   # gera em outra pasta, para conferir antes
```

O script usa o Python de `_geradores/.venv`, se ele existir. Para usar outro, informe a variável `PYTHON`.

## Como alterar um estudo

1. Textos e figuras fixas do treinamento: edite `<estudo>_body.html`.
2. Dados dos exemplos, que aparecem no treinamento e na planilha: edite `<estudo>_data.py`.
3. Tabelas e gráficos gerados do treinamento: edite `build_<estudo>_html.py`.
4. Planilha: edite `build_<estudo>.py`.
5. Gere em uma pasta de teste, confira, e só então gere na pasta do estudo.

O estudo de SWOT não tem arquivo de dados: os exemplos estão dentro de `build_swot.py` e de `swot_body.html`.

## Pontos de atenção

- **CSS compartilhado:** todos os geradores de HTML leem o CSS de `PDCA/treinamento-pdca.html`. Uma alteração nesse arquivo muda a aparência de todos os estudos na próxima geração.
- **Funções compartilhadas:** os geradores de planilha reaproveitam o bloco inicial de `build_pdca.py`, até a linha `STATUS = [`. Não mova nem renomeie esse arquivo.
- **Recálculo:** o `openpyxl` grava as fórmulas sem os valores. O LibreOffice abre o arquivo, calcula e grava de novo, para a planilha abrir já calculada.
- **Painel:** o `index.html` não é gerado. Ao criar um estudo, acrescente à mão o cartão, a caixa da figura, as linhas das duas tabelas e as contagens do cabeçalho.
- **Estudo da ISO 9001:** a matriz e a tabela do módulo 11 vêm do campo `estudos` de cada requisito, em `iso_data.py`. Ao criar um estudo, inclua-o ali. O estudo de Informação documentada também lê a lista `DOCS` desse arquivo, e o de Escopo e liderança, a lista `REQ`.

## Testes

A pasta `testes/` tem os roteiros usados para conferir as fórmulas de dezoito planilhas. Cada par preenche uma cópia do modelo com dados de teste, inclusive erros propositais, e lê os resultados depois do recálculo.

```bash
PY=_geradores/.venv/bin/python
$PY _geradores/testes/rk_test_make.py Riscos/Riscos-modelo.xlsx /tmp/teste
soffice --headless --convert-to 'xlsx:Calc MS Excel 2007 XML' --outdir /tmp/teste/saida /tmp/teste/t1.xlsx /tmp/teste/t2.xlsx
$PY _geradores/testes/rk_test_read.py /tmp/teste/saida
```

Os roteiros importam os arquivos de dados desta pasta. Os roteiros a partir do de indicadores já encontram a pasta sozinhos. Para rodar os outros, informe o caminho de `_geradores/` em `PYTHONPATH`.
