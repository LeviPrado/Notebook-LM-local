import re
from typing import Dict, Any
from pathlib import Path
import pymupdf as fitz
import json

def limpa_texto(texto: str) -> str:
    if not texto:
        return ""

    texto = re.sub(r'(\w+)-\n(\w+)', r'\1\2', texto)

    texto = re.sub(r'(?<!\n)\n(?!\n)', ' ', texto)

    texto = re.sub(r'[ \t]+', ' ', texto)

    texto = re.sub(r'\n\s*\n', '\n\n', texto)

    return texto.strip()

def extrair_texto(pdf_path: Path) -> Dict[str, Any]:

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"arquivo não encontrado no caminho: {pdf_path}")

    paginas = []
    bloco_texto = []

    with fitz.open(pdf_path) as documentos:
        metadado = documentos.metadata or {}

        for num_pagina, pagina in enumerate(documentos, start=1):
            texto_bruto = pagina.get_text()
            texto_limpo = limpa_texto(texto_bruto)


            paginas.append({
                "numero_pagina": num_pagina,
                "conteudo": texto_limpo
            })

            if texto_limpo:
                bloco_texto.append(texto_limpo)

    texto_inteiro = "\n\n".join(bloco_texto)

    return{
        "nome_arquivo": pdf_path.name,
        "caminho": str(pdf_path),
        "total_paginas": len(paginas),
        "metadados": metadado,
        "texto_completo": texto_inteiro,
        "paginas": paginas
    }

if __name__ == "__main__":
    # Aponta para um PDF de teste na pasta data/
    caminho_teste = Path(__file__).parent.parent / "Arquivos de Dados"

    # Pega o primeiro PDF que encontrar na pasta para testar
    pdfs_encontrados = list(caminho_teste.glob("*.pdf"))

    if pdfs_encontrados:
        resultado = extrair_texto(pdfs_encontrados[0])
        print("✔ Teste concluído com sucesso!")
        print(f"Arquivo: {resultado['nome_arquivo']}")
        print(f"Total de páginas: {resultado['total_paginas']}")
        print(f"Tamanho do texto extraído: {len(resultado['texto_completo'])} caracteres")
    else:
        print("Nenhum PDF encontrado na pasta para testar.")