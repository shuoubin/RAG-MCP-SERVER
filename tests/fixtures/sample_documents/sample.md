# Sample Document

This is a minimal sample document used for testing the Smart Knowledge Hub ingestion pipeline.

## Section 1: Introduction

The Smart Knowledge Hub is a modular RAG (Retrieval-Augmented Generation) system with MCP server support.

## Section 2: Key Features

- **Modular architecture**: Pluggable LLM, Embedding, and VectorStore backends
- **Hybrid search**: Dense (semantic) + Sparse (BM25) retrieval with RRF fusion
- **MCP Protocol**: Exposes knowledge retrieval as MCP tools for AI assistants

## Section 3: Example Content

This section contains example text that can be used to test chunking, embedding, and retrieval.

The document format is Markdown, which enables structured splitting with `RecursiveCharacterTextSplitter`.

### Subsection 3.1: Technical Details

- Vector dimensions: 1536 (OpenAI text-embedding-3-small)
- Chunk size: 512 tokens
- Chunk overlap: 64 tokens
- Distance metric: cosine similarity
