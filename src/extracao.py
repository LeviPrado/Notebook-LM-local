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
    # Aponta para a pasta Arquivos de Dados
    caminho_teste = Path(__file__).parent.parent / "Arquivos de Dados"

    # Pega todos os PDFs
    pdfs_encontrados = list(caminho_teste.glob("*.pdf"))

    if pdfs_encontrados:
        print(f"Encontrados {len(pdfs_encontrados)} PDFs. Analisando extração de todos:\n")
        
        for pdf_path in pdfs_encontrados:
            try:
                resultado = extrair_texto(pdf_path)
                tamanho = len(resultado['texto_completo'])
                
                # Se o tamanho for 0, colocamos um alerta visual
                if tamanho == 0:
                    print(f" {resultado['nome_arquivo']}: {resultado['total_paginas']} páginas | {tamanho} caracteres")
                else:
                    print(f" {resultado['nome_arquivo']}: {resultado['total_paginas']} páginas | {tamanho} caracteres")
            except Exception as e:
                print(f"✖ Erro ao processar {pdf_path.name}: {e}")
                
    else:
        print("Nenhum PDF encontrado na pasta para testar.")