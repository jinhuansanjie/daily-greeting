#!/bin/bash
# GitHub Actions 快速部署

echo "========================================="
echo "  GitHub Actions 快速部署"
echo "========================================="
echo ""
echo "使用说明："
echo "1. 请先在GitHub创建仓库"
echo "2. 记录仓库地址（如：https://github.com/username/daily-greeting.git）"
echo "3. 按提示输入仓库地址"
echo ""
read -p "是否继续？(y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "已取消"
    exit 0
fi

echo ""
read -p "请输入GitHub仓库地址: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "错误: 仓库地址不能为空"
    exit 1
fi

# 进入项目目录
cd /workspace/projects

# 初始化Git
echo ""
echo "📦 初始化Git仓库..."
if [ -d ".git" ]; then
    echo "   Git仓库已存在"
else
    git init
    echo "   ✓ Git仓库已创建"
fi

# 配置用户信息
echo ""
echo "⚙️  配置Git用户信息..."
read -p "请输入GitHub用户名: " GIT_USERNAME
read -p "请输入GitHub邮箱: " GIT_EMAIL

git config user.name "$GIT_USERNAME"
git config user.email "$GIT_EMAIL"
echo "   ✓ Git用户信息已配置"

# 添加文件
echo ""
echo "➕ 添加文件..."
git add .
echo "   ✓ 文件已添加"

# 提交
echo ""
echo "💾 提交文件..."
git commit -m "部署到GitHub Actions - 每日定时问候工作流" 2>/dev/null || echo "   ✓ 提交完成"

# 添加远程仓库
echo ""
echo "🔗 配置远程仓库..."
if git remote get-url origin &> /dev/null; then
    git remote set-url origin "$REPO_URL"
    echo "   ✓ 远程仓库已更新"
else
    git remote add origin "$REPO_URL"
    echo "   ✓ 远程仓库已添加"
fi

# 推送
echo ""
echo "🚀 推送到GitHub..."
echo "   仓库: $REPO_URL"
echo ""

# 尝试推送
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo ""
    echo "下一步："
    echo "1. 访问您的GitHub仓库"
    echo "2. 点击 'Actions' 标签"
    echo "3. 查看并启用 '每日定时问候' 工作流"
    echo "4. 编辑 .github/workflows/daily-greeting.yml 调整时间"
    echo ""
    echo "时区说明："
    echo "- UTC 14:30 = 北京时间 22:30"
    echo "- UTC 23:30 = 北京时间 07:30（次日）"
    echo ""
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "可能原因："
    echo "1. 仓库地址错误"
    echo "2. 没有权限访问该仓库"
    echo "3. 需要配置SSH密钥或Personal Access Token"
    echo ""
    echo "解决方案："
    echo "方案A：使用SSH"
    echo "  1. 生成SSH密钥: ssh-keygen -t rsa"
    echo "  2. 添加公钥到GitHub（Settings → SSH keys）"
    echo "  3. 使用SSH地址: git@github.com:username/repo.git"
    echo ""
    echo "方案B：使用Personal Access Token"
    echo "  1. GitHub Settings → Developer settings → Personal access tokens"
    echo "  2. 生成新token（选择repo权限）"
    echo "  3. 使用: https://token@github.com/username/repo.git"
    echo ""
    exit 1
fi
