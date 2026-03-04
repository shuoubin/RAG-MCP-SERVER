"""
src/mcp_server/server.py
MCP Server 入口（Stdio Transport）。
A1阶段：仅骨架，run_server 存根待 E 阶段实现。
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.settings import Settings


def run_server(settings: "Settings") -> None:
    """启动 MCP Server（Stdio Transport）。E1 阶段实现。"""
    raise NotImplementedError("MCP Server not yet implemented (target: E1)")
