#!/bin/bash
# 每日定时问候工作流 - 一键部署脚本

set -e

echo "========================================="
echo "  每日定时问候工作流 - 一键部署"
echo "========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查项目路径
PROJECT_PATH="/workspace/projects"
if [ ! -d "$PROJECT_PATH" ]; then
    echo -e "${RED}错误: 项目目录不存在: $PROJECT_PATH${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} 项目目录检查通过"

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo -e "${RED}错误: Python未安装${NC}"
    exit 1
fi

PYTHON_VERSION=$(python --version | awk '{print $2}')
echo -e "${GREEN}✓${NC} Python版本: $PYTHON_VERSION"

# 检查依赖
echo ""
echo "检查依赖包..."
cd "$PROJECT_PATH"

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠${NC} 虚拟环境不存在，正在创建..."
    python -m venv .venv
    echo -e "${GREEN}✓${NC} 虚拟环境创建成功"
fi

# 激活虚拟环境
source .venv/bin/activate

# 检查并安装依赖
echo "安装/检查依赖包..."
if [ -f "requirements.txt" ]; then
    pip install -q -r requirements.txt
    echo -e "${GREEN}✓${NC} 依赖包安装完成"
else
    echo -e "${YELLOW}⚠${NC} requirements.txt不存在，跳过依赖安装"
fi

# 测试工作流
echo ""
echo "测试工作流..."
python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})" &> /dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} 工作流测试通过"
else
    echo -e "${RED}✗${NC} 工作流测试失败"
    echo "请手动测试: python -c \"from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})\""
    exit 1
fi

# 配置Cron任务
echo ""
echo "配置Cron定时任务..."
CRON_JOB1="30 7 * * * cd $PROJECT_PATH && python -c \"from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})\""
CRON_JOB2="31 7 * * * cd $PROJECT_PATH && python -c \"from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'morning'})\""
CRON_JOB3="30 22 * * * cd $PROJECT_PATH && python -c \"from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'evening'})\""

# 检查是否已存在Cron任务
if crontab -l 2>/dev/null | grep -q "daily-greeting"; then
    echo -e "${YELLOW}⚠${NC} Cron任务已存在，将被覆盖"
fi

# 备份当前Cron
crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null || true

# 添加Cron任务
(crontab -l 2>/dev/null | grep -v "daily-greeting"; echo "# 每日定时问候工作流"; echo "$CRON_JOB1"; echo "$CRON_JOB2"; echo "$CRON_JOB3") | crontab -

echo -e "${GREEN}✓${NC} Cron任务配置完成"

# 显示配置信息
echo ""
echo "========================================="
echo "  部署完成！"
echo "========================================="
echo ""
echo "定时任务："
echo "  - 7:30  天气预报"
echo "  - 7:31  早安问候"
echo "  - 22:30 晚安问候"
echo ""
echo "城市设置：苏州"
echo ""
echo "查看Cron任务："
echo "  crontab -l"
echo ""
echo "查看日志："
echo "  tail -f /app/work/logs/bypass/app.log"
echo ""
echo "手动测试："
echo "  cd $PROJECT_PATH"
echo "  python -c \"from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})\""
echo ""
echo "停止定时任务："
echo "  crontab -e"
echo "  删除相关任务后保存"
echo ""
echo -e "${GREEN}✓${NC} 部署成功！工作流将在指定时间自动运行。"
echo ""
