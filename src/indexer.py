import json
from pathlib import Path
from typing import List, Dict, Any
import chromadb

def criar_chunks_com_overlap(texto: str, chunk_size: int = 800, overlap: int = 150) -> List[str]:

    if not texto:
        return []

    chunks = []
    inicio = 0
    tamanho_texto = len(texto)

    while inicio < tamanho_texto:
        fim = inicio + chunk_size
        chunk = texto[inicio:fim]
        chunks.append(chunk)

        inicio += (chunk_size - overlap)

    return chunks

def indexar_base_com_classificacao(caminho_json: Path, pasta_chromadb: Path) -> None:
    caminho_json = Path(caminho_json)
    pasta_chromadb = Path(pasta_chromadb)

    if not caminho_json.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_json}")

    with open(caminho_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    cliente = chromadb.PersistentClient(path=str(pasta_chromadb))

    colecao = cliente.get_or_create_collection(name="normas_juridicas")

    total_indexado = 0

    for nome_arquivo, info in dados.items():
        texto_completo = info.get("texto_completo", "")
        classificacao = info.get("classificacao", {})

        chunks = criar_chunks_com_overlap(texto_completo)
        if not chunks:
            print(f"{nome_arquivo}: sem texto extraido, pulando indexação")
            continue

        ids = []
        documentos = []
        metadados = []

        for idx, chunk in enumerate(chunks):
            chunks_id = f"{nome_arquivo}_chunk_{idx}"

            ids.append(chunks_id)
            documentos.append(chunk)

            metadados.append({
                "nome_arquivo": nome_arquivo,
                "categoria": classificacao.get("categoria", "OUTROS"),
                "numero": str(classificacao.get("numero") or "N/A"),
                "ano": str(classificacao.get("ano") or "N/A"),
                "orgao_emissor": str(classificacao.get("orgao_emissor") or "N/A"),
                "chunk_index": idx
            })

        colecao.add(
            ids=ids,
            documents=documentos,
            metadatas=metadados
        )
        total_indexado += len(documentos)
        print(f"{nome_arquivo}: {len(documentos)} chunks indexados")

    print(f"\nTotal geral = {total_indexado} chunks indexados em {pasta_chromadb}")

if __name__ == "__main__":
    pasta_base =Path(__file__).parent.parent
    caminho_entrada = pasta_base / "extracted data" / "dados_classificados.json"
    pasta_vetorial = pasta_base / "extracted data" / "chroma_db"

    indexar_base_com_classificacao(caminho_entrada, pasta_vetorial)