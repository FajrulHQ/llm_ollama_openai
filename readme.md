# Agentic RAG System

A document processing and question-answering system that combines Retrieval-Augmented Generation (RAG) with an agent-based approach for intelligent document analysis and summarization.

## Overview

This project implements an intelligent document processing system that can:

- Process multiple document formats (PDF, DOCX, TXT)
- Generate vector embeddings for document content
- Perform semantic search across documents
- Generate document summaries
- Answer questions based on document content

## Features

- **Multi-format Document Processing**: Support for PDF, DOCX, and TXT files
- **Vector-based Document Storage**: Uses FAISS for efficient vector storage and retrieval
- **Intelligent Document Retrieval**: Semantic search capabilities using HuggingFace embeddings
- **Document Summarization**: Both single and multi-document summarization
- **Question-Answering**: Context-aware responses based on document content
- **Agent-based Interaction**: Uses LangChain agents for intelligent task handling

## Technical Stack

- **Language Models**:
  - Ollama (LLaMA 3.2)
  - HuggingFace Embeddings (sentence-transformers/all-mpnet-base-v2)
- **Vector Store**:
  - FAISS for efficient similarity search
- **Document Processing**:
  - Custom DocumentProcessor class
  - RecursiveCharacterTextSplitter for text chunking
- **Framework**:
  - LangChain for agent and chain management
  - IPython for notebook interface

## Installation

1. Clone the repository
2. Install the required dependencies:

```bash
pip install langchain langchain-community langchain-ollama faiss-cpu
pip install sentence-transformers
```

3. Ensure Ollama is installed and running with the LLaMA 3.2 model

## Project Structure

```
project/
├── data/                  # Directory for source documents
├── utils/
│   └── document_processor.py  # Document processing utilities
├── Agentic_RAG.ipynb     # Main notebook with implementation
└── README.md             # Project documentation
```

## Usage

1. **Initialize Document Processing**:

```python
docs = DocumentProcessor()
DATA_PATH = "./data"
```

2. **Process Documents and Create Vector Store**:

```python
# Documents are automatically processed and vectorized
vectorstore = FAISS.from_texts(all_texts, embedding_model, metadatas=metadata_list)
```

3. **Use Available Tools**:

- `retrieval_qa`: Answer questions based on document content
- `summarize_document`: Generate summary for a specific document
- `summarize_all_documents`: Generate summaries for all available documents

4. **Query the System**:

```python
response = agent.invoke({"input": "Summarize all documents about mental health."})
```

## Features in Detail

### Document Processing

- Automatic text extraction from multiple file formats
- Text chunking for optimal processing
- Metadata preservation for source tracking

### Vector Storage

- FAISS-based vector store for efficient similarity search
- HuggingFace embeddings for semantic representation
- Metadata-aware retrieval system

### Summarization

- Single document summarization
- Multi-document summarization
- Source-aware summary generation

### Question Answering

- Context-aware responses
- Source attribution
- Multi-document knowledge integration

## Agent Capabilities

The system uses a zero-shot agent that can:

- Understand and route queries to appropriate tools
- Combine information from multiple documents
- Generate coherent summaries and answers
- Provide source attribution for responses

## Limitations

- Currently supports only text-based documents
- Requires local installation of Ollama
- Memory usage scales with document size
- Processing time depends on document complexity
