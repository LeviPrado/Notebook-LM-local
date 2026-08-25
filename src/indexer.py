import json
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from chromadb.utils import embedding_functions

def criar_chunks_com_overlap(texto: str, chunk_size: int = 1200, overlap: int = 300) -> List[str]:

    if not texto:
        return []

    chunks = []
    inicio = 0
    tamanho_texto = len(texto)

    while inicio < tamanho_texto:
        fim = inicio + chunk_size

        if fim < tamanho_texto:
            ultimo_espaco = texto.rfind(' ', inicio, fim)
            ultima_quebra = texto.rfind('\n', inicio, fim)

            ponto_corte = max(ultimo_espaco, ultima_quebra)
            if ponto_corte != -1 and ponto_corte > inicio:
                fim = ponto_corte

        chunk = texto[inicio:fim].strip()
        if chunk:
            chunks.append(chunk)

        inicio = fim - overlap

    return chunks

ef_multilingual = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2",
    device="cpu"
)

def indexar_base_com_classificacao(caminho_json: Path, pasta_chromadb: Path) -> None:
    caminho_json = Path(caminho_json)
    pasta_chromadb = Path(pasta_chromadb)

    if not caminho_json.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_json}")

    with open(caminho_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    cliente = chromadb.PersistentClient(path=str(pasta_chromadb))

    colecao = cliente.get_or_create_collection(name="normas_juridicas", embedding_function=ef_multilingual)

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

        colecao.upsert(
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