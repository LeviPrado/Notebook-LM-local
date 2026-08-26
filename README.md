# Notebook LM - Sistema RAG para leitura de PDFs

Este repositório contém a solução desenvolvida para o **Estudo de Caso – Estágio em Dados e IA**. O **Ártemis** é um pipeline completo de extração, classificação, indexação e consulta inteligente a documentos normativos em PDF utilizando arquitetura RAG (*Retrieval-Augmented Generation*).

Conforme os requisitos do projeto, a aplicação roda **100% localmente via CPU**, sem dependência de GPU.

##  Objetivos Implementados

* **Extração e OCR de PDFs:** Extração nativa via `PyMuPDF` com fallback automático para `PyTesseract` (OCR) no processamento de documentos escaneados ou imagens.
* **Classificação e Metadados:** Identificação automatizada da categoria documental (Lei, Decreto, Portaria, Resolução, Instrução Normativa) e extração de número, ano e órgão emissor via expressões regulares.
* **Busca Semântica:** Fatiamento (*chunking*) estruturado com overlap e indexação no banco vetorial `ChromaDB` utilizando o modelo `paraphrase-multilingual-MiniLM-L12-v2`.
* **LLM Local Factual:** Integração com o modelo `llama3.2:1b` via `Ollama`, configurado com parâmetros de temperatura nula e regras estritas para evitar alucinações.
* **Interface Gráfica Minimalista:** Interface web em `Streamlit` inspirada no Google Gemini, com suporte a inspeção de fontes e trechos consultados.

---

## 📂 Estrutura do Repositório

```text
.
├── 📂Arquivos de Dados/           Pasta para armazenar os PDFs de entrada
├── 📂extracted data/              Dados processados e banco vetorial (gerado automaticamente)
│   ├── dados_extraidos.json
│   ├── dados_classificados.json
│   └── chroma_db/
├── 📂src/
    ├── extracao.py                  Módulo de leitura de PDF e OCR
    ├── classificacao.py             Módulo de classificação e extração de metadados
    ├── indexer.py                   Módulo de chunking e indexação no ChromaDB
    ├── busca.py                     Módulo de busca por similaridade vetorial
    ├── Rag_chatbot.py               Interface de chat via terminal (CLI)
    └── interface.py                 Interface gráfica web (Streamlit)
├── .gitignore
├── LICENSE
├── requirements.txt             Dependências do projeto
└── README.md                    Documentação do repositório
```

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.9+
* **Processamento de PDFs e OCR:** `PyMuPDF` (`fitz`), `pytesseract`, `Pillow`
* **Indexação Vetorial e Embeddings:** `chromadb`, `sentence-transformers`
* **Inferência de LLM Local:** Ollama (Modelo `llama3.2:1b` rodando em CPU)
* **Interface Web:** `streamlit`

---

##  Como Executar o Projeto

### 1. Pré-requisitos
1. Instalar o **Python 3.9+**.
2. Instalar o **Tesseract OCR** no sistema operacional.
   * *Windows:* Certifique-se de que o executável está localizado em `C:\Program Files\Tesseract-OCR\tesseract.exe` ou atualize a rota no arquivo `extracao.py`.
3. Instalar o **Ollama** ([ollama.com](https://ollama.com/)).
4. Baixar o modelo executando no terminal:
   ```bash
   ollama run llama3.2:1b

### 2. Instalação de Dependências
Clone este repositório e instale os pacotes requeridos:
```bash
git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
cd SEU-REPOSITORIO

pip install -r requirements.txt
```

### 3. Pipeline de Dados
Adicione os arquivos PDF na pasta Arquivos de Dados/ e execute a sequência de processamento:

1° Extração de Texto e OCR:

```bash
python extracao.py
```
2° Classificação e Metadados:

```bash
python classificacao.py
```
3° Indexação no Banco Vetorial:

```bash
python indexer.py
```
4° Execução da Aplicação
Interface Web (Streamlit):

```bash
streamlit run interface.py
```
Terminal
```bash
python Rag_chatbot.py
```
