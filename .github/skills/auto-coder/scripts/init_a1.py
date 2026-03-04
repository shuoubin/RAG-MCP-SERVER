#!/usr/bin/env python3
"""
A1 初始化脚本：创建目录骨架与所有骨架文件
"""
import os

BASE = '/Users/ldh/project/rag/jetlloc/RAG-MCP-SERVER'

# ----------------------------------------------------------------
# 1. __init__.py 文件列表（仅包路径，不含已创建的）
# ----------------------------------------------------------------
init_files = [
    'src/mcp_server/tools/__init__.py',
    'src/core/query_engine/__init__.py',
    'src/core/response/__init__.py',
    'src/core/trace/__init__.py',
    'src/ingestion/__init__.py',
    'src/ingestion/chunking/__init__.py',
    'src/ingestion/transform/__init__.py',
    'src/ingestion/embedding/__init__.py',
    'src/ingestion/storage/__init__.py',
    'src/libs/__init__.py',
    'src/libs/loader/__init__.py',
    'src/libs/llm/__init__.py',
    'src/libs/embedding/__init__.py',
    'src/libs/splitter/__init__.py',
    'src/libs/vector_store/__init__.py',
    'src/libs/reranker/__init__.py',
    'src/libs/evaluator/__init__.py',
    'src/observability/__init__.py',
    'src/observability/dashboard/__init__.py',
    'src/observability/dashboard/pages/__init__.py',
    'src/observability/dashboard/services/__init__.py',
    'src/observability/evaluation/__init__.py',
    'tests/__init__.py',
    'tests/unit/__init__.py',
    'tests/integration/__init__.py',
    'tests/e2e/__init__.py',
]

# ----------------------------------------------------------------
# 2. 骨架源文件（只需存在即可 import，不含业务逻辑）
# ----------------------------------------------------------------
skeleton_files = [
    # mcp_server
    'src/mcp_server/server.py',
    'src/mcp_server/protocol_handler.py',
    'src/mcp_server/tools/query_knowledge_hub.py',
    'src/mcp_server/tools/list_collections.py',
    'src/mcp_server/tools/get_document_summary.py',
    # core
    'src/core/types.py',
    'src/core/settings.py',
    'src/core/query_engine/query_processor.py',
    'src/core/query_engine/hybrid_search.py',
    'src/core/query_engine/dense_retriever.py',
    'src/core/query_engine/sparse_retriever.py',
    'src/core/query_engine/fusion.py',
    'src/core/query_engine/reranker.py',
    'src/core/response/response_builder.py',
    'src/core/response/citation_generator.py',
    'src/core/response/multimodal_assembler.py',
    'src/core/trace/trace_context.py',
    'src/core/trace/trace_collector.py',
    # ingestion
    'src/ingestion/pipeline.py',
    'src/ingestion/document_manager.py',
    'src/ingestion/chunking/document_chunker.py',
    'src/ingestion/transform/base_transform.py',
    'src/ingestion/transform/chunk_refiner.py',
    'src/ingestion/transform/metadata_enricher.py',
    'src/ingestion/transform/image_captioner.py',
    'src/ingestion/embedding/dense_encoder.py',
    'src/ingestion/embedding/sparse_encoder.py',
    'src/ingestion/embedding/batch_processor.py',
    'src/ingestion/storage/vector_upserter.py',
    'src/ingestion/storage/bm25_indexer.py',
    'src/ingestion/storage/image_storage.py',
    # libs
    'src/libs/loader/base_loader.py',
    'src/libs/loader/pdf_loader.py',
    'src/libs/loader/file_integrity.py',
    'src/libs/llm/base_llm.py',
    'src/libs/llm/llm_factory.py',
    'src/libs/llm/azure_llm.py',
    'src/libs/llm/openai_llm.py',
    'src/libs/llm/ollama_llm.py',
    'src/libs/llm/deepseek_llm.py',
    'src/libs/llm/base_vision_llm.py',
    'src/libs/llm/azure_vision_llm.py',
    'src/libs/embedding/base_embedding.py',
    'src/libs/embedding/embedding_factory.py',
    'src/libs/embedding/openai_embedding.py',
    'src/libs/embedding/azure_embedding.py',
    'src/libs/embedding/ollama_embedding.py',
    'src/libs/splitter/base_splitter.py',
    'src/libs/splitter/splitter_factory.py',
    'src/libs/splitter/recursive_splitter.py',
    'src/libs/splitter/semantic_splitter.py',
    'src/libs/splitter/fixed_length_splitter.py',
    'src/libs/vector_store/base_vector_store.py',
    'src/libs/vector_store/vector_store_factory.py',
    'src/libs/vector_store/chroma_store.py',
    'src/libs/reranker/base_reranker.py',
    'src/libs/reranker/reranker_factory.py',
    'src/libs/reranker/cross_encoder_reranker.py',
    'src/libs/reranker/llm_reranker.py',
    'src/libs/evaluator/base_evaluator.py',
    'src/libs/evaluator/evaluator_factory.py',
    'src/libs/evaluator/ragas_evaluator.py',
    'src/libs/evaluator/custom_evaluator.py',
    # observability
    'src/observability/logger.py',
    'src/observability/dashboard/app.py',
    'src/observability/dashboard/pages/overview.py',
    'src/observability/dashboard/pages/data_browser.py',
    'src/observability/dashboard/pages/ingestion_manager.py',
    'src/observability/dashboard/pages/ingestion_traces.py',
    'src/observability/dashboard/pages/query_traces.py',
    'src/observability/dashboard/pages/evaluation_panel.py',
    'src/observability/dashboard/services/trace_service.py',
    'src/observability/dashboard/services/data_service.py',
    'src/observability/dashboard/services/config_service.py',
    'src/observability/evaluation/eval_runner.py',
    'src/observability/evaluation/ragas_evaluator.py',
    'src/observability/evaluation/composite_evaluator.py',
    # scripts
    'scripts/ingest.py',
    'scripts/query.py',
    'scripts/evaluate.py',
    'scripts/start_dashboard.py',
]

created = 0
for rel in init_files + skeleton_files:
    full = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if not os.path.exists(full):
        with open(full, 'w') as f:
            f.write(f'# {os.path.basename(rel)} - skeleton placeholder\n')
        created += 1

print(f'Created {created} new files (out of {len(init_files + skeleton_files)} total)')
