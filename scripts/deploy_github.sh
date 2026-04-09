# GitHub Actions部署脚本

echo "========================================="
echo "  GitHub Actions 部署向导"
echo "========================================="
echo ""

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo "错误: Git未安装，请先安装Git"
    exit 1
fi

echo "✓ Git已安装"
echo ""

# 输入GitHub仓库地址
read -p "请输入GitHub仓库地址（例如: https://github.com/username/daily-greeting.git）: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "错误: 仓库地址不能为空"
    exit 1
fi

echo ""
echo "仓库地址: $REPO_URL"
echo ""

# 进入项目目录
cd /workspace/projects

# 初始化Git仓库
echo "1. 初始化Git仓库..."
if [ -d ".git" ]; then
    echo "   Git仓库已存在，跳过初始化"
else
    git init
    echo "   ✓ Git仓库初始化完成"
fi

# 添加所有文件
echo "2. 添加文件到Git..."
git add .
echo "   ✓ 文件已添加"

# 提交文件
echo "3. 提交文件..."
git commit -m "部署到GitHub Actions - 每日定时问候工作流"
echo "   ✓ 文件已提交"

# 添加远程仓库
echo "4. 添加远程仓库..."
if git remote get-url origin &> /dev/null; then
    echo "   远程仓库已存在，更新地址..."
    git remote set-url origin "$REPO_URL"
else
    git remote add origin "$REPO_URL"
fi
echo "   ✓ 远程仓库配置完成"

# 推送到GitHub
echo "5. 推送到GitHub..."
echo "   正在推送..."
git push -u origin main

# 检查推送结果
if [ $? -eq 0 ]; then
    echo "   ✓ 推送成功！"
else
    echo "   ✗ 推送失败"
    echo "   可能原因："
    echo "   1. 仓库地址错误"
    echo "   2. 没有权限访问该仓库"
    echo "   3. 需要配置Git凭据"
    exit 1
fi

echo ""
echo "========================================="
echo "  部署完成！"
echo "========================================="
echo ""
echo "接下来："
echo "1. 访问您的GitHub仓库"
echo "2. 点击 'Actions' 标签"
echo "3. 查看 '每日定时问候' 工作流"
echo "4. 点击工作流查看运行状态"
echo ""
echo "工作流将在指定时间自动运行："
echo "  - 7:30 UTC (15:30 北京时间) - 天气预报"
echo "  - 7:31 UTC (15:31 北京时间) - 早安问候"
echo "  - 14:30 UTC (22:30 北京时间) - 晚安问候"
echo ""
echo "注意：如果使用北京时间，需要调整cron表达式"
echo ""
