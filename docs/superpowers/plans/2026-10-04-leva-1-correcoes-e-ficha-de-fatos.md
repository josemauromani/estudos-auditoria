# Leva 1: correções e ficha de fatos — plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Corrigir os erros técnicos, as contradições entre estudos e os textos desatualizados dos 34 estudos, e criar a ficha de fatos com o teste que impede as contradições de voltarem.

**Architecture:** Primeiro as ferramentas de conferência (extração de texto, teste de coerência, varredura das planilhas), que começam falhando nos pontos conhecidos. Depois a ficha de fatos, com uma parada para o autor rever as decisões. Depois as correções, em seis grupos de estudos, cada grupo com as correções técnicas e as de continuidade juntas. Por fim, o painel, a documentação e a geração completa.

**Tech Stack:** Python 3 com openpyxl 3.1.5 (`_geradores/.venv`), LibreOffice sem interface (`soffice`), Google Chrome sem interface para as figuras, `_geradores/gerar.sh`.

**Spec:** `docs/superpowers/specs/2026-10-03-leva-1-correcoes-e-ficha-de-fatos-design.md`. Os números T01 a T66, P01 a P23, I01 a I19 e D01 a D09 deste plano são os itens das seções 5, 6 e 7 do spec. Cada tarefa cita os itens que executa; o texto do item, com o problema e a correção, está no spec.

## Global Constraints

- Textos em português do Brasil, no tom dos estudos. Nunca reproduzir o texto das normas: só resumos com palavras próprias. A numeração dos requisitos é a da ISO 9001:2015.
- Editar a origem, nunca o arquivo gerado: `_geradores/<estudo>_body.html`, `_geradores/<estudo>_data.py`, `_geradores/build_<estudo>_html.py`, `_geradores/build_<estudo>.py`. São escritos à mão, e editados direto: `SIPOC/treinamento-sipoc.html`, `PDCA/treinamento-pdca.html` e `index.html`. A SWOT não tem arquivo de dados: os exemplos estão em `build_swot.py` e em `swot_body.html`.
- Não alterar o CSS de `PDCA/treinamento-pdca.html`: ele é lido por todos os geradores.
- Não mudar `id` de elementos, chaves de `localStorage` nem nomes de abas das planilhas: os leitores do site publicado perderiam as marcações.
- Só entram mudanças previstas no spec. Uma contradição nova, achada no caminho, segue as regras da seção 4.3 do spec e é acrescentada a `DECISOES` em `fatos.py`.
- Propagação: ao mudar um número, uma data, um código ou um nome, procurar o valor antigo em `_geradores/*.html`, `_geradores/*.py`, `SIPOC/*.html`, `PDCA/*.html` e `index.html`, e corrigir na mesma tarefa, mesmo que o estudo seja de outro grupo.
- Afirmação sobre alínea ou nota de norma: conferir numa fonte acessível antes de aplicar. Sem conferência, a redação fica no nível do resumo, sem citar a alínea.
- Frase padrão do item D08, acrescentada à caixa "Pontos de atenção" do módulo sobre as normas de cada estudo, menos no ISO 9001:2026 e no SIPOC: `Os exemplos se passam de 2026 a 2028 e usam a numeração da ISO 9001:2015, que as organizações dos exemplos seguem até a transição. O estudo <a href="../ISO-9001-2026/treinamento-iso-9001-2026.html">ISO 9001:2026: o que muda</a> mostra as diferenças.`
- Grafia única: "muçarela".
- Organização da cadeia de compras das ferramentas (item I08): `Distribuidora de materiais elétricos · Compras`.
- Commits em português, um por tarefa, terminados com `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. Não enviar ao GitHub: o envio publica o site e só é feito a pedido do autor.
- Comandos: `PY=_geradores/.venv/bin/python`. Pasta de teste: um diretório temporário fora do repositório, chamado `$T` abaixo.

## Review Focus

1. **O gerador muda algo além do previsto.** Um estudo gerado de novo sem edição deve sair idêntico ao publicado. Teste na tarefa 1, passo 6, antes de qualquer correção.
2. **Planilha com fórmula quebrada depois de mudar rótulo ou regra.** Nenhuma célula com `#REF!`, `#NAME?`, `#VALUE!`, `#DIV/0!` ou `Err:`, e nenhuma fórmula sem valor gravado. Teste: `planilhas.py`, tarefa 1, usado em todas as tarefas de correção.
3. **Valor corrigido num estudo e velho em outro.** Cada valor antigo que seja único o bastante vira regra em `PROIBIDO`, e o teste varre os 34 estudos. Teste: `coerencia.py`, tarefa 1; as regras entram em cada tarefa.
4. **Questionário com gabarito fora das opções depois de reescrever itens.** Toda resposta `a` de `ITEMS` precisa estar entre as opções do exercício. Teste: verificação de questionários em `coerencia.py`, tarefa 1.
5. **Link relativo quebrado.** A frase padrão acrescenta um link a 32 estudos, e os exemplos trocam de organização. Todo `href` relativo precisa apontar para um arquivo que existe. Teste: verificação de links em `coerencia.py`, tarefa 1.

---

### Task 1: Ferramentas de conferência

**Files:**
- Create: `_geradores/fatos.py`
- Create: `_geradores/testes/coerencia.py`
- Create: `_geradores/testes/coerencia_autoteste.py`
- Create: `_geradores/testes/planilhas.py`

**Interfaces:**
- Produces, em `fatos.py` (nesta tarefa só a estrutura e as regras iniciais; a tarefa 2 preenche o resto):
  - `ORGS: dict[str, dict]` com as chaves `'pizzaria'`, `'industria'`, `'distribuidora'`; cada valor tem `identidade: dict`, `pessoas`, `processos`, `equipamentos`, `documentos`, `linha_do_tempo`, `numeros`, todos `list[dict]`.
  - `CODIGOS: dict[str, dict[str, str]]`, organização → código → significado.
  - `COMPARTILHADOS: set[str]`, códigos que existem de propósito em mais de uma organização.
  - `SERIES_LIVRES: tuple[str, ...]`, prefixos de numeração corrida que não são registrados um a um (requisições, pedidos, lotes).
  - `REGISTROS: list[dict]` com `org`, `serie` (`'RNC'` ou `'PNC'`), `numero` (`'aaaa-nn'`), `data` (`'aaaa-mm-dd'`), `assunto`, `estudos`.
  - `PROIBIDO: list[dict]` com `id`, `regex`, `motivo`, `pastas` (`None` para todos os estudos, ou lista de pastas).
  - `DECISOES: list[dict]` com `id`, `conflito`, `canone`, `estudos`.
- Produces, em `coerencia.py`:
  - `extrair_texto(html: str) -> str`: tira `<style>` e `<script>`, troca cada `<svg>` por `[FIGURA]`, quebra linha no fim de parágrafo, item, linha de tabela e título, e desfaz as entidades.
  - `achar_proibidos(texto: str, regras: list[dict], pasta: str) -> list[tuple[str, str, str]]`: devolve `(id, trecho, motivo)`.
  - `codigos_no_texto(texto: str) -> set[str]`: casa `\b[A-Z]{2,4}(?:-[A-Z0-9]{1,4})?-\d{1,4}\b`.
  - `registros_no_texto(texto: str) -> set[str]`: casa `20\d\d-\d{2}` precedido de `RNC ` ou de `registro `, sem diferenciar maiúsculas.
  - `contagens_de_estudos(texto: str) -> list[int]`: os números, em algarismos ou por extenso, que precedem a palavra "estudos".
  - `questionarios(html: str) -> list[str]`: as respostas `a` de `ITEMS` que não estão nas opções do exercício.
  - `links_quebrados(caminho_html: str) -> list[str]`.
  - Linha de comando: sem argumentos, roda tudo e sai com 1 se houver falha, listando arquivo, trecho e motivo; `--so T01,I03` roda só as regras de `PROIBIDO` com esses `id`; `--extrair DEST [--de ORIGEM]` grava um `.txt` por HTML, com o mesmo nome de base, lendo `*/treinamento-*.html` e `index.html` da raiz ou, com `--de`, os `*.html` da pasta dada.
- Produces, em `planilhas.py`: `planilhas.py <arquivo.xlsx>...` lista as células com erro e as fórmulas sem valor gravado, e sai com 1 se houver alguma.

- [ ] **Step 1: Escrever o autoteste, que falha**

```python
# _geradores/testes/coerencia_autoteste.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coerencia as C

html = ('<style>p{}</style><p>A loja tem 29 estudos e o FR-07.</p><svg><text>x</text></svg>'
        '<p>RNC 2027-04 e registro 2027-14; lote 135.</p><script>var a=1;</script>')
t = C.extrair_texto(html)
assert 'p{}' not in t and 'var a' not in t and '[FIGURA]' in t
assert C.codigos_no_texto(t) == {'FR-07'}
assert C.registros_no_texto(t) == {'2027-04', '2027-14'}
assert C.contagens_de_estudos('Trinta e quatro estudos; os 29 estudos') == [34, 29]
regras = [{'id': 'D01', 'regex': r'\b29 estudos', 'motivo': 'a série tem 34', 'pastas': None},
          {'id': 'X', 'regex': r'FR-07', 'motivo': 'só no Escopo', 'pastas': ['Escopo']}]
assert [r[0] for r in C.achar_proibidos(t, regras, 'Caso-Integrado')] == ['D01']
q = "var KEYS = ['B','C'];\nvar ITEMS = [ { t: 'x', a: 'B', w: 'y' }, { t: 'z', a: 'Q', w: 'y' } ];"
assert C.questionarios('<script>' + q + '</script>') == ['Q']
print('autoteste OK')
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `$PY _geradores/testes/coerencia_autoteste.py`
Expected: `ModuleNotFoundError: No module named 'coerencia'`

- [ ] **Step 3: Escrever `coerencia.py` e a estrutura de `fatos.py`**

As funções e a linha de comando são as do bloco Interfaces. Nos exercícios sem `KEYS`, as opções são as chaves de `NAMES`. As verificações da execução completa: regras de `PROIBIDO`; todo código do texto registrado em `CODIGOS` de alguma organização, ou com prefixo em `SERIES_LIVRES`; código registrado em duas organizações só se estiver em `COMPARTILHADOS`; todo número de registro do texto presente em `REGISTROS`; em `REGISTROS`, dentro de cada organização e série, número maior com data igual ou posterior; toda contagem de estudos em `index.html` e no Caso integrado igual ao número de links "Abrir o treinamento" do painel; questionários; links.

`fatos.py` nasce com `ORGS`, `CODIGOS`, `COMPARTILHADOS`, `SERIES_LIVRES`, `REGISTROS` e `DECISOES` vazios, e `PROIBIDO` com estas regras:

| id | regex | pastas |
|---|---|---|
| I01 | `certificad[oa] há 8 anos` | todas |
| I01 | `com sistema de gestão certificado` | Auditoria |
| I02 | `(três\|3) extrusoras` | todas |
| I03 | `Das 9 mudanças de processo de 2027` | todas |
| P01 | `não abre às segundas` | todas |
| P04 | `há 12 anos na loja` | todas |
| P10 | `RNC 2027-(07\|27\|29\|30)` | todas |
| P23 | `mussarela` | todas |
| T02 | `corroborada por duas fontes` | todas |
| T07 | `Não há justificativa possível` | todas |
| T19 | `A Produção tem o maior número de pendências` | todas |
| T41 | `Erro, ou correção` | todas |
| T53 | `decidir menos em cada reunião` | todas |
| T54 | `nem toda vira não conformidade` | todas |
| T56 | `três desvios da média das médias\|a três desvios da linha central` | todas |
| T65 | `mais de 100 pontos` | todas |
| T66 | `Resultado ruim sem decisão é uma não conformidade` | todas |
| D01 | `\b29 estudos` | todas |
| D02 | `estava em preparação` | todas |
| D03 | `ainda não têm estudo próprio` | todas |
| D05 | `as três ferramentas trabalham` | todas |

- [ ] **Step 4: Rodar o autoteste e ver passar**

Run: `$PY _geradores/testes/coerencia_autoteste.py`
Expected: `autoteste OK`

- [ ] **Step 5: Escrever `planilhas.py` e rodar nas 34 planilhas**

Run: `$PY _geradores/testes/planilhas.py */*.xlsx`
Expected: nenhuma célula listada, saída 0. Se alguma planilha atual tiver erro, registrar o achado em `DECISOES` e corrigir na tarefa do grupo dela.

- [ ] **Step 6: Conferir que o gerador reproduz o que está publicado**

Run:
```bash
_geradores/gerar.sh todos "$T/base"
for f in */treinamento-*.html; do cmp -s "$f" "$T/base/$(basename "$f")" || echo "DIFERE $f"; done
```
Expected: exatamente duas linhas, `DIFERE PDCA/treinamento-pdca.html` e `DIFERE SIPOC/treinamento-sipoc.html`, porque esses dois não são gerados e não existem na pasta de teste. Qualquer outro `DIFERE` é investigado e resolvido antes de seguir. As planilhas não entram nesta comparação: o LibreOffice grava a data em cada arquivo, e duas gerações nunca saem iguais byte a byte.

- [ ] **Step 7: Guardar o texto de partida e ver o teste de coerência falhar**

Run: `$PY _geradores/testes/coerencia.py --extrair "$T/antes"; $PY _geradores/testes/coerencia.py; echo "saída $?"`
Expected: saída 1, com falhas para as regras da tabela e para os códigos ainda não registrados. É o ponto de partida da leva.

- [ ] **Step 8: Commit**

```bash
git add _geradores/fatos.py _geradores/testes/coerencia.py _geradores/testes/coerencia_autoteste.py _geradores/testes/planilhas.py
git commit -m "Leva 1: teste de coerência, varredura das planilhas e estrutura da ficha de fatos"
```

---

### Task 2: Ficha de fatos e revisão das decisões

**Files:**
- Modify: `_geradores/fatos.py`
- Modify: `_geradores/README.md` (seção nova "Ficha de fatos e teste de coerência", depois de "Testes")

**Interfaces:**
- Consumes: a estrutura de `fatos.py` e `coerencia.py --extrair` da tarefa 1.
- Produces: `ORGS`, `CODIGOS`, `SERIES_LIVRES`, `REGISTROS` e `DECISOES` preenchidos **com o cânone**, isto é, com os valores que os estudos terão depois das correções. As tarefas 3 a 8 leem `DECISOES` para saber o valor exato de cada item P e I.

- [ ] **Step 1: Inventariar códigos e registros**

Com as funções `codigos_no_texto` e `registros_no_texto` sobre `$T/antes`, listar cada código e cada número de registro, com os estudos em que aparece e a frase ao redor.

- [ ] **Step 2: Preencher a ficha, uma organização por vez**

Ler os exemplos de cada organização em todos os estudos (pizzaria; indústria; cadeia de compras de GUT, Pareto, Ishikawa, 5W2H e PDCA, que passa à distribuidora). Para cada organização, preencher os oito blocos da seção 4.1 do spec. Os valores em conflito recebem o cânone das seções 6.1 e 6.2 do spec. Valores que o spec deixa para a ficha:

- P08: o código novo do relatório de auditoria interna da pizzaria é o primeiro `FR-` livre da organização.
- P10: os registros 2027-27, 2027-29 e 2027-30 entram na série `'PNC'`; o RNC de 22/03/2027 da pizzaria passa a `2027-03`.
- P13: datas das homologações da pizzaria entre 15/12/2026 e 23/12/2026, na mesma ordem de hoje; avaliação do segundo semestre de 2026 datada de 11/01/2027.
- I03: onze mudanças de processo em 2027, nove até setembro e duas em outubro e novembro.
- I09: o lote piloto da resina nova recebe um número anterior ao 131 e data anterior a 14/05/2027.
- I11: a ordem de RNC 2026-29 e 2026-31 é resolvida pela data de abertura de cada um.

- [ ] **Step 3: Registrar as decisões**

`DECISOES` recebe uma entrada para cada item P01 a P23 e I01 a I19, com o valor exato escolhido, e uma para cada contradição nova achada na leitura, numerada `N01` em diante, decidida pelas regras da seção 4.3 do spec.

- [ ] **Step 4: Conferir a estrutura da ficha**

Run: `$PY _geradores/testes/coerencia.py; echo "saída $?"`
Expected: nenhuma falha de ordem em `REGISTROS` e nenhum código em duas organizações fora de `COMPARTILHADOS`. As falhas de `PROIBIDO` e as de códigos que os estudos ainda trazem com o valor antigo continuam: são o trabalho das tarefas 3 a 8.

- [ ] **Step 5: Escrever a seção do README**

Conteúdo: para que serve a ficha; a regra "ler a ficha antes de escrever um estudo e atualizá-la no mesmo commit"; os três comandos (`coerencia.py`, `coerencia.py --so`, `planilhas.py`).

- [ ] **Step 6: Commit**

```bash
git add _geradores/fatos.py _geradores/README.md
git commit -m "Leva 1: ficha de fatos da pizzaria, da indústria e da distribuidora"
```

- [ ] **Step 7: Parar para a revisão do autor**

Apresentar ao autor a tabela de `DECISOES`: item, conflito, valor escolhido e estudos afetados, com destaque para o I08 e para as entradas `N`. Nenhuma tarefa seguinte começa antes da resposta. Mudanças pedidas entram em `fatos.py`, em novo commit.

---

### Tasks 3 a 8: correções por grupo

As seis tarefas seguem o mesmo ciclo. Os passos estão descritos uma vez aqui; cada tarefa traz os arquivos, os itens e o que é próprio dela.

**Interfaces (todas):**
- Consumes: `DECISOES` e `PROIBIDO` de `fatos.py`; `coerencia.py` e `planilhas.py`; o texto de partida em `$T/antes`.
- Produces: os estudos do grupo corrigidos e gerados; regras novas em `PROIBIDO`; nenhum item do grupo falhando em `coerencia.py --so`.

**Ciclo:**

- [ ] **Step 1: Acrescentar regras e ver falhar.** Para cada item do grupo cujo valor antigo é uma expressão que não deve voltar, acrescentar a regra a `PROIBIDO`, com o `id` do item. Run: `$PY _geradores/testes/coerencia.py --so <ids do grupo>`. Expected: saída 1, com ao menos uma falha por regra.
- [ ] **Step 2: Corrigir a origem.** Um item por vez, na ordem da lista da tarefa, nos arquivos de origem. Para cada item: aplicar a correção do spec com o valor de `DECISOES`, e fazer a propagação da seção Global Constraints.
- [ ] **Step 3: Regras de planilha, quando o item muda fórmula.** Mudar primeiro a função em `<estudo>_data.py`, rodar o par de testes do estudo e ver `DIFERE`; mudar a fórmula em `build_<estudo>.py` e ver `OK`. Comandos, com o nome curto `<n>` e a planilha `<X>`:
  ```bash
  _geradores/gerar.sh <n> "$T/g"
  $PY _geradores/testes/<n>_test_make.py "$T/g/<X>-modelo.xlsx" "$T/t"
  soffice --headless --convert-to 'xlsx:Calc MS Excel 2007 XML' --outdir "$T/t/saida" "$T"/t/t*.xlsx
  $PY _geradores/testes/<n>_test_read.py "$T/t/saida"
  ```
  Expected: `erros []` e nenhuma linha `DIFERE`.
- [ ] **Step 4: Gerar na pasta de teste e comparar o texto.** Run: `for n in <nomes curtos>; do _geradores/gerar.sh $n "$T/g"; done; $PY _geradores/testes/coerencia.py --extrair "$T/depois" --de "$T/g"; for f in "$T"/depois/*.txt; do diff -u "$T/antes/$(basename "$f")" "$f"; done`. Expected: cada diferença corresponde a um item da tarefa; nenhuma outra. Os estudos escritos à mão são comparados do mesmo modo depois do passo 6, com a extração feita da raiz.
- [ ] **Step 5: Refazer as contas dos exemplos alterados.** Para cada exemplo com número mudado, um roteiro curto que importa `<estudo>_data.py` e confere somas, médias, percentuais e contagens citadas no texto. Expected: todas as contas fecham.
- [ ] **Step 6: Gerar no lugar e conferir.** Run: `for n in <nomes curtos>; do _geradores/gerar.sh $n; done; $PY _geradores/testes/planilhas.py <planilhas do grupo>; $PY _geradores/testes/coerencia.py --so <ids do grupo>`. Expected: saída 0 nos dois.
- [ ] **Step 7: Figuras alteradas.** Para cada figura mudada: `google-chrome --headless=new --screenshot="$T/fig.png" --window-size=1280,2400 "file://$PWD/<Pasta>/treinamento-<x>.html#<id do módulo>"`, e de novo com `--force-dark-mode`. Expected: texto dentro das caixas, sem sobreposição, legível nos dois temas.
- [ ] **Step 8: Commit.** `git add` dos arquivos de origem, dos gerados e de `fatos.py`; mensagem `Leva 1: <grupo> corrigido`, com a lista dos itens no corpo.

### Task 3: Núcleo de auditoria

**Files:** `_geradores/{aud,tec,cert,nc}_body.html`, `_geradores/{aud,tec,cert,nc}_data.py`, `_geradores/build_{aud,tec,cert,nc}_html.py`, `_geradores/build_{aud,tec,cert,nc}.py`, `_geradores/testes/tec_test_make.py`, `_geradores/testes/tec_test_read.py`; gerados em `Auditoria/`, `Tecnica-Auditoria/`, `Certificacao/`, `Nao-Conformidade/`.

**Itens:** T01 a T06, I01 (cabeçalho do exemplo 3 de Auditoria), I03, D08.

**Decisões próprias:**
- `tec_data.py`: `ISOL = "Desvio pontual: não conformidade, ampliar a amostra"`; `REPET` não muda; `SEMCORR = "Não conformidade sem evidência objetiva"`; em `ev_conf`, a condição passa de `forca(e) != FORTE` para `forca(e) == FRACA`. `forca` e `am_sit` não mudam de lógica.
- Técnica, exemplo 1: a amostra de leituras de temperatura gera uma décima pergunta nas evidências, requisito 7.1.4, fonte registro, constatação não conformidade. O cabeçalho passa a "10 perguntas: 3 conformes, 5 não conformidades, 1 oportunidade". A não conformidade do aviso do tempo de espera continua marcada, agora como "sem evidência objetiva".
- Técnica, exemplo 2: a pergunta do 7.1.3 passa a requisito 8.7 e a não conformidade. O cabeçalho passa a "8 perguntas: 5 conformes, 3 não conformidades".
- Técnica, módulo 8: a linha "Desvio isolado" da tabela de conclusões passa a "Desvio pontual", com "Não conformidade; ampliar a amostra para saber se é pontual ou repetido". No checklist, o item das duas fontes passa a "Toda não conformidade tem ao menos uma evidência objetiva; a que nasce de entrevista é corroborada."
- Técnica, questionário: rever os 12 itens contra a regra nova; o gabarito de um item com um desvio em registro passa a "a evidência basta".
- Auditoria, exemplo 1: a constatação 3 passa a `NC Menor`, com a declaração "Entregadores admitidos depois do treinamento inicial trabalham sem o treinamento no método exigido pela instrução." A conclusão passa a citar três ações corretivas. A lista de verificação, item 7, passa a `NC nº 3`.
- Certificação: I-3 passa a "Das 11 mudanças de processo de 2027, 4 sem autorização, 2 delas depois da constatação da auditoria interna de outubro".

**Testes de planilha:** par `tec`. As planilhas de Auditoria, Certificação e Não conformidade só mudam nos exemplos; `cert` e `nc` têm par de testes e são rodados.

### Task 4: Norma e sistema

**Files:** origem de `iso`, `ed26`, `esc`, `doc`, `caso` (os quatro arquivos de cada um); gerados em `ISO-9001/`, `ISO-9001-2026/`, `Escopo/`, `Informacao-Documentada/`, `Caso-Integrado/`. Por propagação: `cal_body.html` (T08), `con_body.html` (T15, P08), `ac_data.py` (I07).

**Itens:** T07 a T19, P06 (parte do ISO 9001:2026), P08, P09, P12, I07, I11, I12, I13, D01, D02, D08.

**Decisões próprias:**
- T07, na planilha de Escopo: a conferência "Requisito que se aplica sempre" passa a "Justificativa reforçada: requisito fora dos candidatos comuns", e deixa de contar como erro quando a justificativa está preenchida. Par de testes `esc`.
- T13: no diagnóstico da pizzaria, o 5.1.1 passa a "em parte". Recalcular o percentual da seção 5 e o total com `iso_data.py`, e propagar os percentuais novos a todo estudo que cite os antigos. Os percentuais antigos entram em `PROIBIDO`, restritos às frases do diagnóstico.
- D01: a aba "Estudos" da planilha do Caso integrado e a tabela de ordem de implantação recebem Histograma e CEP, Técnica de auditoria, Processo de certificação, ISO 9001:2026 e o próprio Caso integrado. O calendário e os números de cumprimento não mudam.
- `iso_data.py` alimenta também Informação documentada (`DOCS`) e Escopo (`REQ`): depois de mudar esse arquivo, gerar os três estudos.

**Testes de planilha:** pares `iso`, `esc`, `doc`, `caso`, `ed26`.

### Task 5: Contexto e planejamento

**Files:** origem de `pi`, `swot` (sem `swot_data.py`), `obj`, `proc`, `raci`, `risk`; `SIPOC/treinamento-sipoc.html`; gerados em `Partes-Interessadas/`, `SWOT/`, `Objetivos/`, `Processos/`, `RACI/`, `Riscos/`.

**Itens:** T20 a T31, P05, P11, I01 (SWOT e Partes interessadas), I04, I05, I14, I15, I16, I17, D03, D05, D06, D07, D08.

**Decisões próprias:**
- I01: na SWOT, a força S1 passa a "Sistema de gestão implantado há 8 anos, com auditores internos formados", com a mesma pontuação. Em Partes interessadas, o organismo de certificação passa a parte com requisito futuro: "Vai auditar o sistema na certificação de 2027", com a situação coerente com a leitura de 20/01/2027.
- T29: a postura do exemplo e da planilha passa a comparar a média de forças com a de fraquezas, e a de oportunidades com a de ameaças. Não há par de testes da SWOT: conferir, com um roteiro, que a célula da postura dos dois exemplos bate com a conta feita em Python.
- P05: no R3, a resposta passa a "Reduzir. Fazer a manutenção preventiva a cada três meses." O residual não muda.
- T28: o plano de contingência mostrado é o do R3: o que fazer se a câmara fria parar. O texto é o da contingência escrita em 13/04/2027 no estudo de Recursos, resumido.

**Testes de planilha:** pares `pi`, `obj`, `proc`, `rk`.

### Task 6: Operação

**Files:** origem de `ped`, `proj`, `prod`, `lib`, `forn`; gerados em `Pedidos/`, `Projeto/`, `Producao/`, `Liberacao/`, `Fornecedores/`. Por propagação: `cal_data.py` e `cal_body.html` (I09).

**Itens:** T32 a T40, P01, P10 (Liberação), P13, P14, P15, P16, P17, I09, I10, D08.

**Decisões próprias:**
- P01: na oferta, "de terça a domingo" fica só na linha da encomenda para eventos. A recusa da E-33 passa a "A loja não atende encomendas para eventos às segundas, e o horário de encomenda começa às 18h."
- P16: em cada registro de produto não conforme, quem decidiu passa a ser a função que o cabeçalho de autoridades indica para aquela disposição. O lote 140 ganha quem liberou e a data, coerentes com o encerramento em 21/05.
- P13: as caixas de pizza saem da tabela de desempenho; o total da classe A passa de 5 para 4.
- T37: a frase de correspondência entra no módulo 1, e o enunciado do exercício 1 a repete.

**Testes de planilha:** pares `ped`, `proj`, `prod`, `lib`, `forn`.

### Task 7: Apoio e avaliação

**Files:** origem de `comp`, `cal`, `rec`, `con`, `ac`, `sat`; gerados em `Competencias/`, `Calibracao/`, `Recursos/`, `Conhecimento/`, `Analise-Critica/`, `Satisfacao/`.

**Itens:** T41 a T55, P02, P03, P04, P06 (Conhecimento e Recursos), P10 (Recursos), P18, P19, P20, I02, I06, I07 (Análise crítica), I18, I19 (Recursos), D04, D08.

**Decisões próprias:**
- P03: em Competências, a ação 1 do plano, do Bruno, passa a "Parcial: reforçar", com a evidência "Regula a temperatura em turno normal. Não reacende nem regula a chama do lastro, e a regulagem segue sem registro. Risco R6 continua aberto." O nível do Bruno na competência não sobe.
- P04: em Conhecimento, "há 12 anos na loja" passa a "há seis anos na loja".
- P06: em Conhecimento e em Recursos, o evento de abril de 2027 passa a "atualização de versão do sistema de pedidos".
- T45: no MIC-07, com critério de ±1 µm, o registro de 10/01 passa a erro de +0,3 µm com incerteza de ±0,6 µm (0,9: aprovado), e o de 12/06, a +1,6 µm com ±0,6 µm (2,2: reprovado). A correção das medições anteriores continua em 1,6 µm, e a frase do T47 cita o erro novo de 10/01.
- T46: na planilha de Calibração, o alerta "Vence em breve" passa a valer quando faltam menos dias do que um quarto do intervalo do instrumento, com teto de 30 dias.
- I02: em Recursos, quatro extrusoras; a lista de equipamentos ganha a EXT-04, com disponibilidade coerente com a parada do chiller.

**Testes de planilha:** pares `comp`, `cal`, `rec`, `con`, `ac`, `sat`.

### Task 8: Ferramentas de melhoria

**Files:** origem de `gut`, `par`, `cep`, `ish`, `w5`, `ind`; `build_pdca.py`; `PDCA/treinamento-pdca.html` (só o conteúdo dos exemplos, nunca o CSS); gerados em `GUT/`, `Pareto/`, `Histograma-CEP/`, `Ishikawa/`, `5W2H/`, `PDCA/`, `Indicadores/`.

**Itens:** T56 a T66, P07, P10 (Histograma e CEP), P21, P22, P23, I08, I19 (GUT, Ishikawa, 5W2H), D08.

**Decisões próprias:**
- I08: em GUT, Pareto, Ishikawa, 5W2H e PDCA, o exemplo de compras ganha a linha de organização da seção Global Constraints, no cabeçalho do exemplo e no nome da aba "Exemplo 2" quando ela cita a organização. O exemplo de instrumentos vencidos continua sendo da indústria. Nenhum número da cadeia muda por causa deste item.
- P07: em Indicadores, os valores mensais de entregas no prazo de junho e julho de 2026 passam a ser as médias das semanas correspondentes da série do PDCA, e a média do ano é refeita.
- P22: no PDCA, a figura 5 e o texto passam a "Das doze hipóteses levantadas, cinco foram confirmadas", e o plano, a seis ações, como no Ishikawa e no 5W2H.
- T59: em `cep_data.py`, a função que marca o sinal passa a marcar amplitude acima do limite; a bobina excluída da base continua com o motivo da exclusão.

**Testes de planilha:** pares `par`, `cep`, `ind`. GUT, Ishikawa, 5W2H e PDCA não têm par: rodar `planilhas.py` e conferir os exemplos com roteiro.

---

### Task 9: Painel, documentação e conferência final

**Files:**
- Modify: `index.html`
- Modify: `_geradores/README.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: tudo das tarefas 1 a 8.

- [ ] **Step 1: Corrigir o painel**

T10: na tabela "Ligação com a ISO 9001:2015", a linha de Escopo e liderança passa de "4.4 Processos terceirizados" a "8.4 Processos terceirizados". Conferir, contra os estudos corrigidos, cada descrição de cartão e cada linha das duas tabelas que cite algo mudado nesta leva.

- [ ] **Step 2: Atualizar a documentação**

D09: no `README.md` de `_geradores/`, o número de planilhas com par de testes passa a ser o contado em `_geradores/testes/`. No `README.md` da raiz, nada muda além do que a leva alterou nos nomes.

- [ ] **Step 3: Gerar tudo e conferir tudo**

Run:
```bash
_geradores/gerar.sh todos "$T/tudo"
for f in */treinamento-*.html; do cmp -s "$f" "$T/tudo/$(basename "$f")" || echo "DIFERE $f"; done
$PY _geradores/testes/coerencia_autoteste.py
$PY _geradores/testes/coerencia.py; echo "coerência $?"
$PY _geradores/testes/planilhas.py */*.xlsx; echo "planilhas $?"
```
Expected: só as duas linhas `DIFERE` do PDCA e do SIPOC, como na tarefa 1: o que está nas pastas dos estudos é o que a origem gera. Depois, `autoteste OK`, `coerência 0` e `planilhas 0`. A geração é feita na pasta de teste para não regravar as planilhas sem necessidade.

- [ ] **Step 4: Conferir o texto inteiro contra o spec**

Run: `$PY _geradores/testes/coerencia.py --extrair "$T/final"; diff -ru "$T/antes" "$T/final" > "$T/leva1.diff"`
Percorrer o spec, item por item, T01 a T66, P01 a P23, I01 a I19 e D01 a D09, e achar no arquivo a diferença de cada um. Expected: todo item tem a sua diferença, e toda diferença tem o seu item ou uma entrada `N` em `DECISOES`.

- [ ] **Step 5: Commit**

```bash
git add index.html README.md _geradores/README.md
git commit -m "Leva 1: painel e documentação atualizados"
```

- [ ] **Step 6: Relatar ao autor**

Resumo do que mudou por grupo, as entradas `N` de `DECISOES`, os itens do spec que a conferência nas fontes fez redigir de outro modo, e a lembrança de que o site só é atualizado com o envio ao GitHub.
