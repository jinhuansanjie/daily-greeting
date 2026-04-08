#!/bin/bash
# 每日定时问候工作流 - 启动调度器

echo "========================================="
echo "  每日定时问候工作流 - 启动调度器"
echo "========================================="
echo ""
echo "定时任务："
echo "  - 7:30  天气预报"
echo "  - 7:31  早安问候"
echo "  - 22:30 晚安问候"
echo ""
echo "城市设置：苏州"
echo ""
echo "按 Ctrl+C 停止调度器"
echo "========================================="
echo ""

cd /workspace/projects
python scripts/scheduler.py
