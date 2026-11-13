"""Teste básico sem dependências adicionais, com o servidor já iniciado."""
import json
from urllib.request import urlopen

for caminho in ['/saude', '/produtos', '/movimentacoes', '/estoque', '/estoque/baixo', '/estoque/resumo']:
    with urlopen('http://127.0.0.1:8000' + caminho, timeout=5) as resposta:
        print(f'{caminho}: HTTP {resposta.status}')
        print(json.dumps(json.load(resposta), ensure_ascii=False, indent=2))
