import chromadb
from pathlib import Path
from typing import List, Dict, Any, Optional

def buscar_normas(
        perguntas: str,
        pasta_chroma: Path,
        n_results: int = 3,
        categotia_filtro: Optional[str] = None
) ->List[Dict[str, Any]]:

    if not pasta_chroma.exists():
        raise FileNotFoundError(f"O banco vetorial não está em {pasta_chroma}")

    cliente = chromadb.PersistentClient(path=str(pasta_chroma))
    colecao = cliente.get_collection(name="normas_juridicas")

    wh_clause = None

    if categotia_filtro:
        wh_clause = {"categoria": categotia_filtro.upper()}

    resultados = colecao.query(
        query_texts=[perguntas],
        n_results=n_results,
        where=wh_clause
    )

    resultados_formatados = []

    if resultados and resultados.get("documents"):
        docs = resultados["documents"][0]
        metas = resultados["metadatas"][0]
        distancias = resultados["distances"][0]

        for doc, meta, dist in zip(docs, metas, distancias):
            resultados_formatados.append({
                "texto": doc,
                "metadados": meta,
                "distancia": round(dist, 4)
            })

    return resultados_formatados

if __name__ == "__main__":

    pasta_base = Path(__file__).parent.parent
    pasta_vetorial = pasta_base / "extracted data" / "chroma_db"

    while True:
        pergunta_teste = input("\nPergunta teste:").strip()

        if pergunta_teste.lower() in ["q"]:
            break

        if not pergunta_teste:
            continue

        try:
            resultados = buscar_normas(pergunta_teste, pasta_vetorial, n_results=3)

            if not resultados:
                print("sem resultados interessantes")
                continue

            for i, item in enumerate(resultados, 1):
                meta = item.get("metadados", {}) 
                
                arq = meta.get('nome_arquivo', 'Desconhecido')
                cat = meta.get('categoria', 'OUTROS')
                num = meta.get('numero', 'N/A')
                ano = meta.get('ano', 'N/A')
                
                print(f"\nResultado {i} (distancia = {item['distancia']})")
                print(f"Arquivo = {arq} | Categoria = {cat} | Norma = {num}/{ano}")
                print(f"Trecho extraido = \n\n{item['texto']}")

        except Exception as e:
            print(f"Erro na busca: {e}")