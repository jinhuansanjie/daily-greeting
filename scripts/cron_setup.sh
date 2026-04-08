#!/bin/bash
# 每日定时问候工作流 - Cron脚本

# 7:30 - 发送天气预报和早安问候
30 7 * * * cd /workspace/projects && python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '上海', 'trigger_type': 'weather'})"
31 7 * * * cd /workspace/projects && python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '上海', 'trigger_type': 'morning'})"

# 22:30 - 发送晚安问候
30 22 * * * cd /workspace/projects && python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '上海', 'trigger_type': 'evening'})"
