"""
Root conftest.py
确保 src/ 目录在所有测试中均可导入（与 pyproject.toml pythonpath = ["src"] 配合）。
"""
import sys
import os

# 将 src/ 加入 Python 路径（pytest 的 pythonpath 配置已处理，此处作为备份）
_SRC = os.path.join(os.path.dirname(__file__), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
