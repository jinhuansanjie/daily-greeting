#!/bin/bash
# 模拟test.yml的测试步骤

set -e

echo "========================================="
echo "开始测试"
echo "========================================="
echo ""

# 测试1：基础Python
echo "测试1：基础Python"
python --version
python -c "print('Python工作正常')"
echo "✓ 测试1通过"
echo ""

# 测试2：安装langgraph
echo "测试2：安装langgraph"
pip install langgraph 2>&1 | grep -v "already satisfied" || true
python -c "import langgraph; print('langgraph安装成功')"
echo "✓ 测试2通过"
echo ""

# 测试3：安装langchain-core
echo "测试3：安装langchain-core"
pip install langchain-core 2>&1 | grep -v "already satisfied" || true
python -c "import langchain_core; print('langchain-core安装成功')"
echo "✓ 测试3通过"
echo ""

# 测试4：安装pydantic
echo "测试4：安装pydantic"
pip install pydantic 2>&1 | grep -v "already satisfied" || true
python -c "import pydantic; print('pydantic安装成功')"
echo "✓ 测试4通过"
echo ""

# 测试5：安装coze-coding-dev-sdk
echo "测试5：安装coze-coding-dev-sdk"
pip install coze-coding-dev-sdk 2>&1 | grep -v "already satisfied" || true
python -c "import coze_coding_dev_sdk; print('coze-coding-dev-sdk安装成功')"
echo "✓ 测试5通过"
echo ""

# 测试6：检查文件结构
echo "测试6：检查文件结构"
echo "当前目录:"
pwd
echo ""
echo "文件列表:"
find . -name "*.py" -type f | head -20
echo "✓ 测试6通过"
echo ""

# 测试7：检查src目录
echo "测试7：检查src目录"
ls -la src/
ls -la src/graphs/
ls -la src/graphs/nodes/
echo "✓ 测试7通过"
echo ""

# 测试8：尝试导入main_graph
echo "测试8：尝试导入main_graph"
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src
python -c "
import sys
import os
print('Python路径:', sys.path)
print('当前目录:', os.getcwd())
print('PYTHONPATH:', os.environ.get('PYTHONPATH'))
print('')
try:
    from src.graphs.graph import main_graph
    print('✓ main_graph导入成功')
except Exception as e:
    print('✗ 导入失败:', str(e))
    import traceback
    traceback.print_exc()
"
echo ""
echo "========================================="
echo "测试完成"
echo "========================================="
