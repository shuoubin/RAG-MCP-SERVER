"""
tests/unit/test_config_loading.py
对应任务 A3：配置加载与校验（Settings）

测试内容：
1. 成功加载有效的 config/settings.yaml
2. 文件不存在时抛出 FileNotFoundError
3. 缺少必填字段时抛出 ValueError，错误信息包含字段路径
4. Settings 数据结构字段类型正确
5. validate_settings 独立调用行为
6. 环境变量覆盖（空 api_key 时）
"""
from __future__ import annotations

import os
import textwrap
import tempfile
from pathlib import Path

import pytest

from core.settings import Settings, load_settings, validate_settings


# -----------------------------------------------------------------------
# 辅助：写临时 YAML 文件
# -----------------------------------------------------------------------

def _write_yaml(content: str) -> str:
    """写入临时 YAML 并返回路径（调用方负责清除）。"""
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False, encoding="utf-8")
    tmp.write(textwrap.dedent(content))
    tmp.close()
    return tmp.name


# -----------------------------------------------------------------------
# 1. 成功加载有效配置
# -----------------------------------------------------------------------

@pytest.mark.unit
def test_load_settings_success(tmp_path: Path) -> None:
    """能够成功加载包含所有必填字段的合法配置。"""
    yaml_path = tmp_path / "settings.yaml"
    yaml_path.write_text(
        textwrap.dedent("""
            llm:
              provider: openai
              api_key: sk-test
            embedding:
              provider: openai
              api_key: sk-test
            vector_store:
              provider: chroma
              persist_dir: data/db/chroma
            retrieval:
              top_k: 10
            observability:
              log_dir: logs
        """),
        encoding="utf-8",
    )
    settings = load_settings(str(yaml_path))
    assert isinstance(settings, Settings)
    assert settings.llm["provider"] == "openai"
    assert settings.embedding["provider"] == "openai"
    assert settings.vector_store["provider"] == "chroma"
    assert settings.retrieval["top_k"] == 10


@pytest.mark.unit
def test_load_settings_returns_settings_type(tmp_path: Path) -> None:
    """load_settings 必须返回 Settings 实例。"""
    yaml_path = tmp_path / "s.yaml"
    yaml_path.write_text(
        textwrap.dedent("""
            llm:
              provider: openai
            embedding:
              provider: openai
            vector_store:
              provider: chroma
              persist_dir: data/db/chroma
            retrieval:
              top_k: 5
            observability:
              log_dir: logs
        """),
        encoding="utf-8",
    )
    result = load_settings(str(yaml_path))
    assert isinstance(result, Settings)


# -----------------------------------------------------------------------
# 2. 文件不存在
# -----------------------------------------------------------------------

@pytest.mark.unit
def test_load_settings_file_not_found() -> None:
    """配置文件不存在时应抛出 FileNotFoundError。"""
    with pytest.raises(FileNotFoundError, match="Settings file not found"):
        load_settings("/nonexistent/path/settings.yaml")


# -----------------------------------------------------------------------
# 3. 缺少必填字段
# -----------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.parametrize("missing_field, yaml_content", [
    (
        "llm.provider",
        """
        llm: {}
        embedding:
          provider: openai
        vector_store:
          provider: chroma
          persist_dir: data/db/chroma
        retrieval:
          top_k: 10
        observability:
          log_dir: logs
        """,
    ),
    (
        "embedding.provider",
        """
        llm:
          provider: openai
        embedding: {}
        vector_store:
          provider: chroma
          persist_dir: data/db/chroma
        retrieval:
          top_k: 10
        observability:
          log_dir: logs
        """,
    ),
    (
        "vector_store.persist_dir",
        """
        llm:
          provider: openai
        embedding:
          provider: openai
        vector_store:
          provider: chroma
        retrieval:
          top_k: 10
        observability:
          log_dir: logs
        """,
    ),
])
def test_load_settings_missing_required_field(
    missing_field: str, yaml_content: str, tmp_path: Path
) -> None:
    """缺少必填字段时应抛出 ValueError，且错误信息包含字段路径。"""
    yaml_path = tmp_path / "s.yaml"
    yaml_path.write_text(textwrap.dedent(yaml_content), encoding="utf-8")

    with pytest.raises(ValueError) as exc_info:
        load_settings(str(yaml_path))

    error_msg = str(exc_info.value)
    assert missing_field in error_msg, (
        f"Expected error to mention '{missing_field}', got:\n{error_msg}"
    )


# -----------------------------------------------------------------------
# 4. Settings 数据结构字段类型
# -----------------------------------------------------------------------

@pytest.mark.unit
def test_settings_default_fields_are_dicts() -> None:
    """Settings() 实例化后所有字段默认为 dict。"""
    s = Settings()
    for field_name in [
        "llm", "vision_llm", "embedding", "vector_store",
        "splitter", "retrieval", "rerank", "ingestion",
        "evaluation", "observability",
    ]:
        value = getattr(s, field_name)
        assert isinstance(value, dict), (
            f"Settings.{field_name} should be dict, got {type(value)}"
        )


# -----------------------------------------------------------------------
# 5. validate_settings 独立调用
# -----------------------------------------------------------------------

@pytest.mark.unit
def test_validate_settings_passes_with_required_fields() -> None:
    """包含所有必填字段的 Settings 应通过校验不抛出异常。"""
    s = Settings(
        llm={"provider": "openai"},
        embedding={"provider": "openai"},
        vector_store={"provider": "chroma", "persist_dir": "data/db/chroma"},
        retrieval={"top_k": 10},
        observability={"log_dir": "logs"},
    )
    validate_settings(s)  # 不应抛出


@pytest.mark.unit
def test_validate_settings_fails_with_empty_provider() -> None:
    """provider 为空字符串时应视为缺失并抛出 ValueError。"""
    s = Settings(
        llm={"provider": ""},  # 空字符串 → 缺失
        embedding={"provider": "openai"},
        vector_store={"provider": "chroma", "persist_dir": "data/db/chroma"},
        retrieval={"top_k": 10},
        observability={"log_dir": "logs"},
    )
    with pytest.raises(ValueError, match="llm.provider"):
        validate_settings(s)


# -----------------------------------------------------------------------
# 6. 环境变量覆盖
# -----------------------------------------------------------------------

@pytest.mark.unit
def test_env_override_api_key(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """OPENAI_API_KEY 环境变量应覆盖 YAML 中的空 api_key。"""
    monkeypatch.setenv("OPENAI_API_KEY", "env-sk-12345")

    yaml_path = tmp_path / "s.yaml"
    yaml_path.write_text(
        textwrap.dedent("""
            llm:
              provider: openai
              api_key: ""
            embedding:
              provider: openai
              api_key: ""
            vector_store:
              provider: chroma
              persist_dir: data/db/chroma
            retrieval:
              top_k: 10
            observability:
              log_dir: logs
        """),
        encoding="utf-8",
    )

    settings = load_settings(str(yaml_path))
    assert settings.llm.get("api_key") == "env-sk-12345"
    assert settings.embedding.get("api_key") == "env-sk-12345"
