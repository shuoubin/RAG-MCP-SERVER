"""
src/core/settings.py
配置加载与校验模块。
A1阶段：骨架占位，Settings 数据结构与 load_settings/validate_settings 将在 A3 实现。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Settings:
    """项目配置数据容器（A3 阶段实现完整校验逻辑）。"""
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


def load_settings(path: str = "config/settings.yaml") -> Settings:
    """读取 YAML 配置文件并返回 Settings 对象。A3 阶段完整实现。"""
    raise NotImplementedError("load_settings not yet implemented (target: A3)")


def validate_settings(settings: Settings) -> None:
    """校验 Settings 必填字段。A3 阶段完整实现。"""
    raise NotImplementedError("validate_settings not yet implemented (target: A3)")
