"""
src/observability/logger.py
结构化日志模块 - 提供 get_logger 的占位实现。
A3 阶段将添加 JSON Lines 格式化输出。
"""
from __future__ import annotations

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """获取命名 Logger（输出到 stderr）。"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        )
        logger.addHandler(handler)
    return logger
