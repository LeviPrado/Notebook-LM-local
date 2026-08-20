import json
import re
from pathlib import Path
from typing import Dict, Any

def extracao_metadados_categoria(texto: str) -> Dict[str, Any]:

    cabecalho = texto[:1500].upper

    pdr_categorias = {
        "RESOLUCAO" : r"\bRESOLUÇ[AÃ]O\b",
        "PORTARIA" : r"\bPORTARIA\b",
        "LEI" : r"\bLEI\b",
        "DECRETO" : r"\bDECRETO\b",
        "INSTITUICAO_NORMATIVA" : r"\bINSTITUIÇ[AÃ]O NORMATIVA\b"
    }

    categorias = "OUTROS"

    for cat, regex in pdr_categorias.items():
        if re.search(regex, cabecalho):
            categorias = cat
            break


    numero_encontrado = re.search(r'N[º°\.\s]*([\d\.]+)', cabecalho)
    numero = numero_encontrado.group(1) if numero_encontrado else None

    ano_encontrado = re.search(r'\b(19,20)\d{2}\b', cabecalho)
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