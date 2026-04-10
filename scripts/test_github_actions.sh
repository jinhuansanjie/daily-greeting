#!/bin/bash
# 模拟GitHub Actions环境测试

echo "========================================="
echo "  模拟GitHub Actions环境测试"
echo "========================================="
echo ""

# 设置环境
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src

echo "1. 检查Python版本..."
python --version

echo ""
echo "2. 测试导入..."
python -c "from src.graphs.graph import main_graph; print('✓ 导入成功')"

echo ""
echo "3. 测试天气预报..."
python -c "from src.graphs.graph import main_graph; result = main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'}); print('✓ 发送状态:', result.get('send_status', 'N/A'))"

echo ""
echo "4. 测试早安问候..."
python -c "from src.graphs.graph import main_graph; result = main_graph.invoke({'city': '苏州', 'trigger_type': 'morning'}); print('✓ 发送状态:', result.get('send_status', 'N/A'))"

echo ""
echo "5. 测试晚安问候..."
python -c "from src.graphs.graph import main_graph; result = main_graph.invoke({'city': '苏州', 'trigger_type': 'evening'}); print('✓ 发送状态:', result.get('send_status', 'N/A'))"

echo ""
echo "========================================="
echo "  测试完成"
echo "========================================="
