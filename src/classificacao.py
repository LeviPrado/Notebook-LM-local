import json
import re
from pathlib import Path
from typing import Dict, Any

def extracao_metadados_categoria(texto: str) -> Dict[str, Any]:

    cabecalho = texto[:1500].upper()

    pdr_categorias = {
        "RESOLUCAO" : r"\bRESOLUÇ[AÃ]O\b",
        "PORTARIA" : r"\bPORTARIA\b",
        "LEI" : r"\bLEI\b",
        "DECRETO" : r"\bDECRETO\b",
        "INSTRUCAO_NORMATIVA" : r"\bINSTRUÇ?[AÃ]O NORMATIVA\b"
    }

    categorias = "OUTROS"
    match_categoria = None

    for cat, regex in pdr_categorias.items():
        m = re.search(regex, cabecalho)
        if m:
            categorias = cat
            match_categoria = m
            break

    if match_categoria:
        janela = cabecalho[match_categoria.end():match_categoria.end() + 150]
    else:
        janela = cabecalho


    numero_encontrado = re.search(r'N?[º°\.\s]*?(\d[\d\.]+)', janela)
    numero = numero_encontrado.group(1) if numero_encontrado else None

    ano_encontrado = re.search(r'\b(19|20)\d{2}\b', janela)
    ano = ano_encontrado.group(0) if ano_encontrado else None

    orgaos = ["CFM", "MEC", "MS", "ANVISA", "STF", "STJ", "GOVERNO"]
    orgao_emissor = None

    for orgao in orgaos:
        if re.search(r'\b' + orgao + r'\b', cabecalho):
            orgao_emissor = orgao
            break

    return {
        "categoria" : categorias,
        "numero" : numero,
        "ano" : ano,
        "orgao_emissor" : orgao_emissor
    }

def classifica_base_extraida(caminho_entrada : Path, caminho_saida : Path) -> Dict[str, Any]:

    caminho_entrada = Path(caminho_entrada)
    caminho_saida = Path(caminho_saida)

    if not caminho_entrada.exists():
        raise FileNotFoundError(f"Caminho não encontrado : {caminho_entrada}")

    with open(caminho_entrada, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    for nome_arquivo, info in dados.items():
        texto = info.get("texto_completo", "")
        metadados = extracao_metadados_categoria(texto)
        info["classificacao"] = metadados

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    return dados

if __name__ == "__main__":
    pasta_base = Path(__file__).parent.parent
    caminho_entrada = pasta_base / "extracted data" / "dados_extraidos.json"
    caminho_saida = pasta_base / "extracted data" / "dados_classificados.json"

    classifica_base_extraida(caminho_entrada, caminho_saida)