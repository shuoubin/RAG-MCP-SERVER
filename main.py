#!/usr/bin/env python3
"""
Smart Knowledge Hub - MCP Server 启动入口

用法:
    python main.py                        # 以 Stdio transport 启动 MCP Server
    python main.py --config /path/to/settings.yaml
"""
import sys
import argparse
import logging
import os

# 确保 src/ 在路径中（支持直接运行 python main.py）
_SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from core.settings import load_settings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="smart-knowledge-hub",
        description="Modular RAG Knowledge Hub via MCP Protocol",
    )
    parser.add_argument(
        "--config",
        default="config/settings.yaml",
        help="Path to settings.yaml (default: config/settings.yaml)",
    )
    parser.add_argument(
        "--log-level",
        default=None,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Override log level from settings",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # --- 加载并校验配置（fail-fast）---
    try:
        settings = load_settings(args.config)
    except (FileNotFoundError, ValueError) as exc:
        print(f"[FATAL] Configuration error: {exc}", file=sys.stderr)
        sys.exit(1)

    # --- 初始化日志 ---
    from observability.logger import get_logger
    log_level = args.log_level or settings.observability.get("log_level", "INFO")
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stderr,
    )
    logger = get_logger(__name__)
    logger.info("Smart Knowledge Hub starting up (config: %s)", args.config)

    # --- 启动 MCP Server ---
    from mcp_server.server import run_server
    run_server(settings)


if __name__ == "__main__":
    main()
