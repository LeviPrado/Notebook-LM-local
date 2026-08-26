# Ártemis - Sistema RAG para Consultas Jurídicas Inteligentes

Este repositório contém a solução desenvolvida para o **Estudo de Caso – Estágio em Dados e IA**[cite: 10]. O **Ártemis** é um pipeline completo de extração, classificação, indexação e consulta inteligente a documentos normativos em PDF utilizando arquitetura RAG (*Retrieval-Augmented Generation*).

Conforme os requisitos do projeto, a aplicação roda **100% localmente via CPU**, sem dependência de GPU[cite: 10].

## 🎯 Objetivos Implementados

* **Extração e OCR de PDFs:** Extração nativa via `PyMuPDF` com fallback automático para `PyTesseract` (OCR) no processamento de documentos escaneados ou imagens[cite: 6, 10].
* **Classificação e Metadados:** Identificação automatizada da categoria documental (Lei, Decreto, Portaria, Resolução, Instrução Normativa) e extração de número, ano e órgão emissor via expressões regulares[cite: 5, 10].
* **Busca Semântica:** Fatiamento (*chunking*) estruturado com overlap e indexação no banco vetorial `ChromaDB` utilizando o modelo `paraphrase-multilingual-MiniLM-L12-v2`[cite: 4, 7, 10].
* **LLM Local Factual:** Integração com o modelo `llama3.2:1b` via `Ollama`, configurado com parâmetros de temperatura nula e regras estritas para evitar alucinações[cite: 9, 10].
* **Interface Gráfica Minimalista:** Interface web em `Streamlit` inspirada no Google Gemini, com suporte a inspeção de fontes e trechos consultados.

---

## 📂 Estrutura do Repositório

```text
.
├── Arquivos de Dados/          # Pasta para armazenar os PDFs de entrada
├── extracted data/             # Dados processados e banco vetorial (gerado automaticamente)
│   ├── dados_extraidos.json
│   ├── dados_classificados.json
│   └── chroma_db/
├── extracao.py                 # Módulo de leitura de PDF e OCR
├── classificacao.py            # Módulo de classificação e extração de metadados
├── indexer.py                  # Módulo de chunking e indexação no ChromaDB
├── busca.py                    # Módulo de busca por similaridade vetorial
├── Rag_chatbot.py              # Interface de chat via terminal (CLI)
├── interface.py                # Interface gráfica web (Streamlit)
├── requirements.txt            # Dependências do projeto
└── README.md                   # Documentação do repositório
