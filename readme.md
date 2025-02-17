# Advanced RAG Implementation

This repository contains an implementation of Retrieval-Augmented Generation (RAG) using LangChain and Ollama. The system is designed to process documents, create embeddings, and generate structured summaries using Large Language Models.

## Features

- Document loading support for PDF and TXT files
- Text chunking with configurable size and overlap
- Vector storage using FAISS
- Document summarization using Llama 3.2
- Retrieval-based generation with context enhancement

## Prerequisites

- Python 3.10 or higher
- Ollama installed with Llama 3.2 model
- Required Python packages:
  - langchain-community
  - langchain-core
  - langchain
  - faiss-cpu
  - pypdf (for PDF processing)

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install langchain-community langchain-core langchain faiss-cpu pypdf
```

3. Ensure Ollama is installed and the Llama 3.2 model is available

## Usage

The main script provides several key functions:

### 1. Document Loading

```python
documents = load_document(file_path)
```

Supports:

- PDF files (.pdf)
- Text files (.txt)

### 2. Text Chunking

```python
texts = split_document(documents)
```

Features:

- Chunk size: 500 characters
- Overlap: 50 characters
- Recursive character-based splitting

### 3. Vector Store Creation

```python
vectorstore = create_vector_store(texts)
```

Uses:

- FAISS for vector storage
- Ollama embeddings (Llama 3.2)

### 4. Document Summarization

```python
summary = summarize_document(vectorstore, query)
```

Capabilities:

- Context-aware summarization
- Structured output
- Retrieves 5 most relevant chunks per query

## Example Usage

```python
# Path to your document
file_path = "your_document.pdf"

# Load and process the document
documents = load_document(file_path)
texts = split_document(documents)
vectorstore = create_vector_store(texts)

# Generate summary
query = "Buat ringkasan lengkap dan terstruktur dari dokumen ini."
summary = summarize_document(vectorstore, query)
print(summary)
```

## Configuration

Key parameters that can be modified:

- `chunk_size`: Size of text chunks (default: 500)
- `chunk_overlap`: Overlap between chunks (default: 50)
- `k`: Number of relevant chunks to retrieve (default: 5)
- `temperature`: LLM temperature setting (default: 0)

## Model Information

This implementation uses:

- LLM: Llama 3.2 (1B parameters, instruct model, FP16)
- Embeddings: Ollama embeddings with Llama 3.2
- Vector Store: FAISS (Facebook AI Similarity Search)

## Error Handling

The implementation includes error handling for:

- Unsupported file formats
- File reading errors
- Processing failures

## Notes

- The system is currently configured for Indonesian language processing
- Summarization prompts are in Indonesian
- The implementation is optimized for memory efficiency with chunk-based processing
