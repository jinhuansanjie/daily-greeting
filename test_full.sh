#!/bin/bash
# 完整模拟test.yml的测试流程

set -e

echo "========================================="
echo "开始完整测试（模拟test.yml）"
echo "========================================="
echo ""

# 测试1：基础Python
echo "【测试1】基础Python"
python --version
python -c "print('Python工作正常')"
echo "✓ 测试1通过"
echo ""

# 测试2：安装langgraph
echo "【测试2】安装langgraph"
pip install langgraph 2>&1 | grep -v "already satisfied" || true
python -c "import langgraph; print('langgraph安装成功')"
echo "✓ 测试2通过"
echo ""

# 测试3：安装langchain-core
echo "【测试3】安装langchain-core"
pip install langchain-core 2>&1 | grep -v "already satisfied" || true
python -c "import langchain_core; print('langchain-core安装成功')"
echo "✓ 测试3通过"
echo ""

# 测试4：安装pydantic
echo "【测试4】安装pydantic"
pip install pydantic 2>&1 | grep -v "already satisfied" || true
python -c "import pydantic; print('pydantic安装成功')"
echo "✓ 测试4通过"
echo ""

# 测试5：安装coze-coding-dev-sdk
echo "【测试5】安装coze-coding-dev-sdk"
pip install coze-coding-dev-sdk 2>&1 | grep -v "already satisfied" || true
python -c "import coze_coding_dev_sdk; print('coze-coding-dev-sdk安装成功')"
echo "✓ 测试5通过"
echo ""

# 测试6：检查文件结构
echo "【测试6】检查文件结构"
echo "当前目录:"
pwd
echo ""
echo "文件列表（前20个）:"
find . -name "*.py" -type f | head -20
echo "✓ 测试6通过"
echo ""

# 测试7：检查src目录
echo "【测试7】检查src目录"
ls -la src/
echo ""
ls -la src/graphs/
echo ""
ls -la src/graphs/nodes/
echo "✓ 测试7通过"
echo ""

# 测试8：尝试导入main_graph（最关键的测试）
echo "【测试8】尝试导入main_graph"
echo "设置PYTHONPATH..."
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src
echo "PYTHONPATH=$PYTHONPATH"
echo ""

echo "开始导入测试..."
python -c "
import sys
import os

print('=' * 60)
print('Python环境信息')
print('=' * 60)
print('Python版本:', sys.version)
print('Python路径:', sys.path)
print('当前工作目录:', os.getcwd())
print('PYTHONPATH环境变量:', os.environ.get('PYTHONPATH', '未设置'))
print('=' * 60)
print()

# 测试1：导入state.py
print('步骤1: 导入src.graphs.state...')
try:
    from src.graphs.state import GlobalState, GraphInput, GraphOutput
    print('✓ state.py导入成功')
except Exception as e:
    print('✗ state.py导入失败:', str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试2：导入node.py
print()
print('步骤2: 导入src.graphs.nodes...')
try:
    from src.graphs.nodes.trigger_node import trigger_node
    from src.graphs.nodes.weather_query_node import weather_query_node
    from src.graphs.nodes.greeting_generate_node import greeting_generate_node
    from src.graphs.nodes.tts_node import tts_node
    from src.graphs.nodes.send_message_node import send_message_node
    print('✓ 所有节点导入成功')
except Exception as e:
    print('✗ 节点导入失败:', str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试3：导入graph.py
print()
print('步骤3: 导入src.graphs.graph...')
try:
    from src.graphs.graph import main_graph
    print('✓ graph.py导入成功')
except Exception as e:
    print('✗ graph.py导入失败:', str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试4：验证main_graph
print()
print('步骤4: 验证main_graph对象...')
try:
    print('main_graph类型:', type(main_graph))
    print('main_graph是否可调用:', callable(main_graph))
    print('✓ main_graph验证成功')
except Exception as e:
    print('✗ main_graph验证失败:', str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print('=' * 60)
print('✓ 所有导入测试通过！')
print('=' * 60)
"

EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "✓ 测试8通过"
    echo "========================================="
else
    echo ""
    echo "========================================="
    echo "✗ 测试8失败，退出码: $EXIT_CODE"
    echo "========================================="
    exit 1
fi

echo ""
echo "========================================="
echo "✓ 所有测试通过！"
echo "========================================="
