#!/usr/bin/env bash
# Gera de novo o treinamento (HTML) e a planilha (XLSX) de um estudo.
#
#   _geradores/gerar.sh <estudo> [pasta de saída]
#   _geradores/gerar.sh todos   [pasta de saída]
#
# Estudos: pdca swot gut w5 ish raci aud nc iso risk ind proc ac doc comp forn sat par pi obj prod lib ped proj esc cal rec con caso tec cert
# Sem a pasta de saída, os arquivos são gravados na pasta do próprio estudo.
set -euo pipefail

AQUI="$(cd "$(dirname "$0")" && pwd)"
RAIZ="$(dirname "$AQUI")"
if [ -n "${PYTHON:-}" ]; then PY="$PYTHON"
elif [ -x "$AQUI/.venv/bin/python" ]; then PY="$AQUI/.venv/bin/python"
else PY="python3"; fi

# estudo | pasta | arquivo HTML | arquivo XLSX
TABELA="
pdca|PDCA||PDCA-modelo.xlsx
swot|SWOT|treinamento-swot.html|SWOT-modelo.xlsx
gut|GUT|treinamento-gut.html|GUT-modelo.xlsx
w5|5W2H|treinamento-5w2h.html|5W2H-modelo.xlsx
ish|Ishikawa|treinamento-ishikawa.html|Ishikawa-modelo.xlsx
raci|RACI|treinamento-raci.html|RACI-modelo.xlsx
aud|Auditoria|treinamento-auditoria.html|Auditoria-modelo.xlsx
nc|Nao-Conformidade|treinamento-nao-conformidade.html|RNC-modelo.xlsx
iso|ISO-9001|treinamento-iso-9001.html|ISO-9001-modelo.xlsx
risk|Riscos|treinamento-riscos.html|Riscos-modelo.xlsx
ind|Indicadores|treinamento-indicadores.html|Indicadores-modelo.xlsx
proc|Processos|treinamento-processos.html|Processos-modelo.xlsx
ac|Analise-Critica|treinamento-analise-critica.html|Analise-Critica-modelo.xlsx
doc|Informacao-Documentada|treinamento-informacao-documentada.html|Informacao-Documentada-modelo.xlsx
comp|Competencias|treinamento-competencias.html|Competencias-modelo.xlsx
forn|Fornecedores|treinamento-fornecedores.html|Fornecedores-modelo.xlsx
sat|Satisfacao|treinamento-satisfacao.html|Satisfacao-modelo.xlsx
par|Pareto|treinamento-pareto.html|Pareto-modelo.xlsx
pi|Partes-Interessadas|treinamento-partes-interessadas.html|Partes-Interessadas-modelo.xlsx
obj|Objetivos|treinamento-objetivos.html|Objetivos-modelo.xlsx
prod|Producao|treinamento-producao.html|Producao-modelo.xlsx
lib|Liberacao|treinamento-liberacao.html|Liberacao-modelo.xlsx
ped|Pedidos|treinamento-pedidos.html|Pedidos-modelo.xlsx
proj|Projeto|treinamento-projeto.html|Projeto-modelo.xlsx
esc|Escopo|treinamento-escopo.html|Escopo-modelo.xlsx
cal|Calibracao|treinamento-calibracao.html|Calibracao-modelo.xlsx
rec|Recursos|treinamento-recursos.html|Recursos-modelo.xlsx
con|Conhecimento|treinamento-conhecimento.html|Conhecimento-modelo.xlsx
caso|Caso-Integrado|treinamento-caso-integrado.html|Caso-Integrado-modelo.xlsx
tec|Tecnica-Auditoria|treinamento-tecnica-auditoria.html|Tecnica-Auditoria-modelo.xlsx
cert|Certificacao|treinamento-certificacao.html|Certificacao-modelo.xlsx
"

gerar() {
  local nome="$1" saida="${2:-}" linha pasta html xlsx destino tmp
  linha="$(printf '%s\n' "$TABELA" | grep "^$nome|" || true)"
  if [ -z "$linha" ]; then echo "Estudo desconhecido: $nome" >&2; exit 1; fi
  IFS='|' read -r _ pasta html xlsx <<< "$linha"
  destino="${saida:-$RAIZ/$pasta}"
  mkdir -p "$destino"
  tmp="$(mktemp -d)"

  if [ -n "$html" ]; then
    # o CSS de todos os estudos vem do treinamento de PDCA, que é escrito à mão
    "$PY" "$AQUI/build_${nome}_html.py" "$RAIZ/PDCA/treinamento-pdca.html" "$AQUI/${nome}_body.html" "$destino/$html" > /dev/null
    echo "ok  $destino/$html"
  fi

  "$PY" "$AQUI/build_${nome}.py" "$tmp/$xlsx" > /dev/null
  # o LibreOffice recalcula as fórmulas e grava os valores, para a planilha abrir já calculada
  soffice --headless --norestore "-env:UserInstallation=file://$tmp/perfil" \
    --convert-to 'xlsx:Calc MS Excel 2007 XML' --outdir "$tmp/saida" "$tmp/$xlsx" > /dev/null 2>&1
  if [ ! -s "$tmp/saida/$xlsx" ]; then echo "Falha ao recalcular $xlsx no LibreOffice" >&2; exit 1; fi
  cp "$tmp/saida/$xlsx" "$destino/$xlsx"
  echo "ok  $destino/$xlsx"
}

if [ $# -lt 1 ]; then sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 1; fi
if [ "$1" = "todos" ]; then
  for n in pdca swot gut w5 ish raci aud nc iso risk ind proc ac doc comp forn sat par pi obj prod lib ped proj esc cal rec con caso tec cert; do gerar "$n" "${2:-}"; done
else
  gerar "$1" "${2:-}"
fi
