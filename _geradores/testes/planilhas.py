# Varredura de planilhas: lista células com erro e fórmulas sem valor gravado.
# Uso: planilhas.py <arquivo.xlsx>...   (sai com 1 se achar algo)
# Ficam de fora: #N/A de fórmula com NA() (de propósito, para os gráficos pularem o ponto)
# e fórmula que devolve texto vazio (o LibreOffice grava como texto, sem conteúdo).
import re, sys, zipfile
import openpyxl

ERROS = ('#DIV/0!', '#N/A', '#NAME?', '#NULL!', '#NUM!', '#REF!', '#VALUE!', 'Err:')
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'


def _arquivos_das_abas(z):
    """Nome da aba -> caminho do XML dela, pelo workbook.xml e pelas relações."""
    import xml.etree.ElementTree as ET
    rel_ns = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
    pkg = '{http://schemas.openxmlformats.org/package/2006/relationships}'
    alvos = {r.get('Id'): r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels')).iter(pkg + 'Relationship')}
    abas = {}
    for s in ET.fromstring(z.read('xl/workbook.xml')).iter(NS + 'sheet'):
        alvo = alvos[s.get(rel_ns + 'id')]
        abas[s.get('name')] = alvo.lstrip('/') if alvo.startswith('/') else 'xl/' + alvo
    return abas


def _sem_valor(caminho):
    """(aba, célula) com fórmula e sem tipo de resultado gravado (arquivo que ninguém recalculou)."""
    import xml.etree.ElementTree as ET
    achados = set()
    with zipfile.ZipFile(caminho) as z:
        for aba, arq in _arquivos_das_abas(z).items():
            for c in ET.fromstring(z.read(arq)).iter(NS + 'c'):
                v = c.find(NS + 'v')
                if c.find(NS + 'f') is not None and c.get('t') != 'str' and (v is None or not (v.text or '').strip()):
                    achados.add((aba, c.get('r')))
    return achados


def varrer(caminho):
    achados = []
    f = openpyxl.load_workbook(caminho)
    v = openpyxl.load_workbook(caminho, data_only=True)
    sem_valor = _sem_valor(caminho)
    for ws in f.worksheets:
        wv = v[ws.title]
        for linha in ws.iter_rows():
            for c in linha:
                val = wv[c.coordinate].value
                formula = c.value if isinstance(c.value, str) and c.value.startswith('=') else ''
                if isinstance(val, str) and val.startswith(ERROS):
                    if val == '#N/A' and 'NA()' in formula:
                        continue
                    achados.append((ws.title, c.coordinate, 'erro %s' % val))
                elif formula and val is None and (ws.title, c.coordinate) in sem_valor:
                    achados.append((ws.title, c.coordinate, 'fórmula sem valor gravado'))
    return achados


def main(argv):
    total = 0
    for caminho in argv:
        for aba, cel, msg in varrer(caminho):
            print('%s | %s!%s | %s' % (caminho, aba, cel, msg))
            total += 1
    print('%d célula(s) com problema em %d planilha(s)' % (total, len(argv)))
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
