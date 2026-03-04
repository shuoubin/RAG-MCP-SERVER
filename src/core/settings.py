"""
src/core/settings.py
配置加载与校验模块。
对应任务 A3：配置加载与校验（Settings）

公开接口：
    Settings          - 配置数据容器（dataclass）
    load_settings()   - 读取 YAML -> Settings，同时执行 fail-fast 校验
    validate_settings()- 仅校验（可独立调用）
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# -----------------------------------------------------------------------
# Settings 数据容器
# -----------------------------------------------------------------------

@dataclass
class Settings:
    """
    项目全局配置。
    字段对应 config/settings.yaml 中各顶级 key。
    所有字段默认为空 dict，load_settings 加载后赋实际值。
    """
    llm: dict[str, Any] = field(default_factory=dict)
    vision_llm: dict[str, Any] = field(default_factory=dict)
    embedding: dict[str, Any] = field(default_factory=dict)
    vector_store: dict[str, Any] = field(default_factory=dict)
    splitter: dict[str, Any] = field(default_factory=dict)
    retrieval: dict[str, Any] = field(default_factory=dict)
    rerank: dict[str, Any] = field(default_factory=dict)
    ingestion: dict[str, Any] = field(default_factory=dict)
    evaluation: dict[str, Any] = field(default_factory=dict)
    observability: dict[str, Any] = field(default_factory=dict)


# -----------------------------------------------------------------------
# 必填字段清单（字段路径使用 "." 分隔）
# -----------------------------------------------------------------------
_REQUIRED_FIELDS: list[str] = [
    "llm.provider",
    "embedding.provider",
    "vector_store.provider",
    "vector_store.persist_dir",
    "retrieval.top_k",
    "observability.log_dir",
]


# -----------------------------------------------------------------------
# 公开 API
# -----------------------------------------------------------------------

def load_settings(path: str = "config/settings.yaml") -> Settings:
    """
    从 YAML 文件加载配置，返回 Settings 对象。
    文件不存在或必填字段缺失时抛出异常（fail-fast）。

    支持的环境变量覆盖（在 YAML 值为空字符串时生效）：
        OPENAI_API_KEY  → llm.api_key  /  embedding.api_key
        AZURE_API_KEY   → llm.api_key  /  embedding.api_key（azure provider）
    """
    # 1. 读取 YAML
    resolved_path = _resolve_path(path)
    if not resolved_path.exists():
        raise FileNotFoundError(
            f"Settings file not found: {resolved_path}\n"
            f"Expected location: {resolved_path.absolute()}"
        )

    raw = _read_yaml(resolved_path)

    # 2. 构建 Settings
    settings = Settings(
        llm=raw.get("llm", {}),
        vision_llm=raw.get("vision_llm", {}),
        embedding=raw.get("embedding", {}),
        vector_store=raw.get("vector_store", {}),
        splitter=raw.get("splitter", {}),
        retrieval=raw.get("retrieval", {}),
        rerank=raw.get("rerank", {}),
        ingestion=raw.get("ingestion", {}),
        evaluation=raw.get("evaluation", {}),
        observability=raw.get("observability", {}),
    )

    # 3. 环境变量覆盖
    _apply_env_overrides(settings)

    # 4. 校验
    validate_settings(settings)

    return settings


def validate_settings(settings: Settings) -> None:
    """
    校验 Settings 必填字段。
    缺失字段时抛出 ValueError，错误信息包含字段路径，便于定位。
    """
    missing: list[str] = []
    for dot_path in _REQUIRED_FIELDS:
        if not _get_nested(settings, dot_path):
            missing.append(dot_path)

    if missing:
        formatted = "\n  - ".join(missing)
        raise ValueError(
            f"Missing required configuration fields:\n  - {formatted}\n"
            f"Please update config/settings.yaml or set the corresponding "
            f"environment variables."
        )


# -----------------------------------------------------------------------
# 内部辅助函数
# -----------------------------------------------------------------------

def _resolve_path(path: str) -> Path:
    """将相对路径解析为绝对路径（相对于调用时的工作目录）。"""
    p = Path(path)
    if not p.is_absolute():
        p = Path.cwd() / p
    return p


def _read_yaml(path: Path) -> dict[str, Any]:
    """读取 YAML 文件，返回顶层 dict。"""
    try:
        import yaml  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "PyYAML is required to load settings. Install it with: pip install pyyaml"
        ) from exc

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(
            f"Invalid settings file format: expected a YAML dict at top level, "
            f"got {type(data).__name__}"
        )
    return data


def _apply_env_overrides(settings: Settings) -> None:
    """将环境变量注入到 Settings 中（仅当 YAML 字段为空字符串时覆盖）。"""
    env_map: list[tuple[str, str, str]] = [
        # (env_var, section, key)
        ("OPENAI_API_KEY", "llm", "api_key"),
        ("OPENAI_API_KEY", "embedding", "api_key"),
        ("AZURE_OPENAI_API_KEY", "llm", "api_key"),
        ("AZURE_OPENAI_API_KEY", "embedding", "api_key"),
        ("AZURE_OPENAI_API_KEY", "vision_llm", "api_key"),
        ("OPENAI_API_BASE", "llm", "api_base"),
        ("OPENAI_API_BASE", "embedding", "api_base"),
    ]

    for env_var, section, key in env_map:
        value = os.environ.get(env_var)
        if not value:
            continue
        section_dict: dict[str, Any] = getattr(settings, section, {})
        # 仅在 YAML 中未设置（空字符串或不存在）时覆盖
        existing = section_dict.get(key, "")
        if not existing:
            section_dict[key] = value


def _get_nested(settings: Settings, dot_path: str) -> Any:
    """
    读取嵌套字段值，例如 "embedding.provider" → settings.embedding["provider"]
    若路径不存在或值为 None / 空字符串，返回 None。
    """
    parts = dot_path.split(".")
    if len(parts) < 2:
        return getattr(settings, parts[0], None)

    section_name, *rest = parts
    section: dict[str, Any] = getattr(settings, section_name, {})
    value: Any = section
    for part in rest:
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    # 空字符串视为缺失
    if value == "" or value is None:
        return None
    return value
