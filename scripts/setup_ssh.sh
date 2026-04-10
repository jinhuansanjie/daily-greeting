#!/bin/bash
# SSH密钥配置脚本

echo "========================================="
echo "  GitHub SSH密钥配置"
echo "========================================="
echo ""

# 检查SSH密钥是否存在
if [ -f ~/.ssh/id_rsa.pub ]; then
    echo "✓ SSH密钥已存在"
    echo ""
    echo "公钥内容："
    cat ~/.ssh/id_rsa.pub
    echo ""
    echo "接下来："
    echo "1. 复制上面的公钥"
    echo "2. 访问 https://github.com/settings/keys"
    echo "3. 点击 'New SSH key'"
    echo "4. 粘贴公钥并保存"
    echo ""
else
    echo "正在生成SSH密钥..."
    ssh-keygen -t rsa -b 4096 -C "jinhuansanjie@example.com" -f ~/.ssh/id_rsa -N ""

    echo "✓ SSH密钥已生成"
    echo ""
    echo "公钥内容："
    cat ~/.ssh/id_rsa.pub
    echo ""
    echo "接下来："
    echo "1. 复制上面的公钥"
    echo "2. 访问 https://github.com/settings/keys"
    echo "3. 点击 'New SSH key'"
    echo "4. 粘贴公钥并保存"
    echo ""
fi

echo "完成后，按回车继续..."
read

echo ""
echo "配置远程仓库为SSH方式..."
cd /workspace/projects
git remote set-url origin git@github.com:jinhuansanjie/daily-greeting.git
echo "✓ 远程仓库已配置为SSH"

echo ""
echo "测试SSH连接..."
ssh -T git@github.com 2>&1 || echo "如果看到 'Hi jinhuansanjie! ...' 说明配置成功"

echo ""
echo "推送代码..."
git push -u origin main
