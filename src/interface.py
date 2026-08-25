import streamlit as st
from pathlib import Path
from busca import buscar_normas
from Rag_chatbot import consultar_ollama, formatar_contexto

st.set_page_config(page_title="RAG Jurídico", page_icon="°", layout="centered")

st.title("Notebook LM para Consultas a Normas Jurídicas")
st.caption("Sistema RAG local rodando via CPU com ChromaDB e Ollama")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua pergunta"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):

        with st.spinner(" Buscando normas e gerando resposta..."):
            pasta_base = Path(__file__).parent.parent
            pasta_vetorial = pasta_base / "extracted data" / "chroma_db"

            try:
                resultados = buscar_normas(prompt, pasta_vetorial, n_results=10)
                
                if resultados:
                    contexto = formatar_contexto(resultados)
                    resposta = consultar_ollama(prompt, contexto)
                else:
                    contexto = None
                    resposta = "Nenhum trecho relevante foi encontrado no banco de dados."

            except Exception as e:
                resposta = f"Erro ao processar de processamento: {e}"
                contexto = None

        st.markdown(resposta)

        if contexto:
            with st.expander("Ver fontes e trechos consultados"):
                st.text(contexto)

    st.session_state.messages.append({"role": "assistant", "content": resposta})