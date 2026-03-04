"""
tests/unit/test_smoke_imports.py
冒烟测试：验证所有顶层包和关键子模块可被成功导入。
对应任务 A2：引入 pytest 并建立测试目录约定
"""
import importlib
import pytest


# ----------------------------------------------------------------
# 顶层包
# ----------------------------------------------------------------
TOP_LEVEL_PACKAGES = [
    "mcp_server",
    "core",
    "ingestion",
    "libs",
    "observability",
]

# ----------------------------------------------------------------
# 关键子模块
# ----------------------------------------------------------------
KEY_SUBMODULES = [
    # mcp_server
    "mcp_server.server",
    "mcp_server.protocol_handler",
    "mcp_server.tools",
    # core
    "core.settings",
    "core.types",
    "core.query_engine",
    "core.query_engine.query_processor",
    "core.query_engine.hybrid_search",
    "core.query_engine.dense_retriever",
    "core.query_engine.sparse_retriever",
    "core.query_engine.fusion",
    "core.query_engine.reranker",
    "core.response",
    "core.response.response_builder",
    "core.response.citation_generator",
    "core.response.multimodal_assembler",
    "core.trace",
    "core.trace.trace_context",
    "core.trace.trace_collector",
    # ingestion
    "ingestion.pipeline",
    "ingestion.document_manager",
    "ingestion.chunking",
    "ingestion.transform",
    "ingestion.embedding",
    "ingestion.storage",
    # libs
    "libs.loader",
    "libs.llm",
    "libs.llm.base_llm",
    "libs.llm.llm_factory",
    "libs.embedding",
    "libs.embedding.base_embedding",
    "libs.embedding.embedding_factory",
    "libs.splitter",
    "libs.splitter.base_splitter",
    "libs.splitter.splitter_factory",
    "libs.vector_store",
    "libs.vector_store.base_vector_store",
    "libs.vector_store.vector_store_factory",
    "libs.reranker",
    "libs.reranker.base_reranker",
    "libs.reranker.reranker_factory",
    "libs.evaluator",
    "libs.evaluator.base_evaluator",
    "libs.evaluator.evaluator_factory",
    # observability
    "observability.logger",
    "observability.dashboard",
    "observability.evaluation",
]


@pytest.mark.unit
@pytest.mark.parametrize("package", TOP_LEVEL_PACKAGES)
def test_top_level_package_importable(package: str) -> None:
    """顶层包必须可导入。"""
    mod = importlib.import_module(package)
    assert mod is not None, f"Failed to import top-level package: {package}"


@pytest.mark.unit
@pytest.mark.parametrize("module", KEY_SUBMODULES)
def test_key_submodule_importable(module: str) -> None:
    """关键子模块必须可导入。"""
    mod = importlib.import_module(module)
    assert mod is not None, f"Failed to import submodule: {module}"


@pytest.mark.unit
def test_logger_get_logger() -> None:
    """observability.logger.get_logger 应返回 Logger 实例。"""
    import logging
    from observability.logger import get_logger

    logger = get_logger("test")
    assert isinstance(logger, logging.Logger)


@pytest.mark.unit
def test_settings_class_importable() -> None:
    """core.settings.Settings 数据类应可实例化（无参数默认值）。"""
    from core.settings import Settings

    s = Settings()
    assert isinstance(s, Settings)
    assert isinstance(s.llm, dict)
    assert isinstance(s.embedding, dict)
