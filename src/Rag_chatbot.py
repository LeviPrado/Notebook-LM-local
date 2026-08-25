import requests
from pathlib import Path
from busca import buscar_normas

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO_OLLAMA = "llama3.2:1b"

def formatar_contexto(resultados: list) ->str:
    blocos = []
    for i, item in enumerate(resultados, 1):
        meta = item.get("metadados", {})
        categoria = meta.get("categoria", "N/A")
        numero = meta.get("numero", "N/A")
        ano = meta.get("ano", "N/A")
        orgao = meta.get("orgao_emissor", "N/A")
        arq = meta.get("nome_arquivo", "Desconhecido")
        texto = item.get("texto", "")

        cabecalho = f"[fonte{i}]: {categoria} {numero}/{ano} ({orgao}) | Arquivo: {arq}"
        blocos.append(f"{cabecalho}\n{texto}")

    return "\n\n---------------------\n\n".join(blocos)

def consultar_ollama(pergunta: str, contexto: str) -> str:

    prompt_sistema = """Você é um assistente jurídico especializado em normas e legislações brasileiras.

Responda à pergunta do usuário utilizando ESTRITAMENTE e EXCLUSIVAMENTE as informações contidas no contexto fornecido.

REGRAS RÍGIDAS:
1. NUNCA invente números, prazos ou cargas horárias. 
2. Se a resposta exata para a pergunta NÃO estiver escrita no contexto, você é OBRIGADO a responder APENAS: "Com base nos documentos consultados, não encontrei informações sobre este assunto."
3. É expressamente PROIBIDO usar conhecimento externo. Responda apenas com o que está no texto.

Diretrizes:
1. Seja preciso, direto e cite a norma/artigo quando disponível no texto.
2. Se a resposta NÃO estiver no contexto, responda exatamente:
"Com base nos documentos consultados, não encontrei informações sobre este assunto."
3. Não invente nem adicione conhecimentos externos ao contexto fornecido.
"""

    payload = {
        "model": MODELO_OLLAMA,
        "messages": [
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content": f"""CONTEXTO DOS DOCUMENTOS:

{contexto}

PERGUNTA DO USUÁRIO:

{pergunta}

RESPOSTA:"""
            }
        ],
        "stream": False,
        "options": {
            "num_gpu": 0,
            "num_ctx": 4096,
            "temperature": 0.0
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        return response.json().get(
            "message",
            {}
        ).get(
            "content",
            "Erro: Modelo não mostrou retorno"
        )

    except requests.exceptions.ConnectionError:
        return "Erro de conexão! O Ollama não está respondendo em http://localhost:11434"

    except Exception as e:
        return f"Erro de chamada do modelo: {e}"

def executar_chat():
    pasta_base = Path(__file__).parent.parent
    pasta_vetorial = pasta_base / "extracted data" / "chroma_db"

    print("=" * 60)
    print("   NOTEBOOK LM LOCAL - (OLLAMA)")
    print("=" * 60)
    print(f"modelo: {MODELO_OLLAMA}")
    print("Digite 'q' para sair\n")

    while True:
        pergunta = input("\n sua pergunta: ").strip()

        if pergunta.lower() in ["q"]:
            break

        if not pergunta:
            continue

        print("\n Buscando contexto...")
        try:
            resultados = buscar_normas(pergunta, pasta_vetorial, n_results=12)
        except Exception as e:
            print(f"Erro na busca vetorial: {e}")
            continue

        if not resultados:
            print("Nenhum trecho interessante foi encontrado!")
            continue

        contexto = formatar_contexto(resultados)

        print("Processando contexto com Ollama...\n")

        resposta = consultar_ollama(pergunta, contexto)

        print("=" * 60)
        print("Resposta do Modelo")
        print("=" * 60)
        print(resposta)
        print("=" * 60)

        ver_contexto = input().strip().lower()
        if ver_contexto == 's':
            print(contexto)
            print("-" * 40)

if __name__ == "__main__":
    executar_chat()