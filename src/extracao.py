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

def extrair_todos_pdfs(diretorio_origem: Path, diretorio_destino: Path) -> Dict[str, Any]:

    diretorio_origem = Path(diretorio_origem)
    diretorio_destino = Path(diretorio_destino)

    if not diretorio_origem.exists():
        raise FileNotFoundError(f"Diretório de origim não encontrado: {diretorio_origem}")

    diretorio_destino.mkdir(parents=True, exist_ok=True)

    resultados = {}
    arquivos_pdf = sorted(list(diretorio_origem.glob("*.pdf")))

    for pdf_path in arquivos_pdf:
        try:
            dados_extraidos = extrair_texto(pdf_path)
            resultados[pdf_path.name] = dados_extraidos
            tamanho = len(dados_extraidos['texto_completo'])

            if tamanho == 0:
                print(f"{pdf_path.name}: 0 caracteres extraídos")
            else:
                print(f"{pdf_path.name} processado")
        except Exception as e:
            print(f"Falha ao processar '{pdf_path.name}': {e}")

    caminho_json = diretorio_destino / "dados_extraidos.json"
    with open(caminho_json, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    return resultados

if __name__ == "__main__":

    pasta_base = Path(__file__).parent.parent
    pasta_dados = pasta_base / "Arquivos de Dados"
    pasta_destino = pasta_base / "extracted data"

    dados_finais = extrair_todos_pdfs(pasta_dados, pasta_destino)