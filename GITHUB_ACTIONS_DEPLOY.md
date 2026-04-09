# GitHub Actions 部署完整指南

## 📋 准备工作

### 1. 确认您有GitHub账号
如果没有，请先注册：https://github.com/signup

### 2. 准备GitHub个人访问令牌（Personal Access Token）
如果使用HTTPS方式推送，需要配置Git凭据。

---

## 🚀 部署步骤

### 第一步：创建GitHub仓库

1. **登录GitHub**
   - 访问 https://github.com

2. **创建新仓库**
   - 点击右上角 **+** 按钮
   - 选择 **New repository**
   - 填写信息：
     ```
     Repository name: daily-greeting
     Description: 每日定时问候工作流
     Public: ☑️ 选中（免费）
     ```
   - 点击 **Create repository**

3. **记录仓库地址**
   ```
   https://github.com/your-username/daily-greeting.git
   ```

---

### 第二步：推送到GitHub

#### 方式1：使用自动化脚本（推荐）

```bash
# 运行部署脚本
cd /workspace/projects
bash scripts/deploy_github.sh

# 按提示输入GitHub仓库地址
# 例如: https://github.com/your-username/daily-greeting.git
```

#### 方式2：手动推送

```bash
# 1. 进入项目目录
cd /workspace/projects

# 2. 初始化Git仓库
git init

# 3. 添加所有文件
git add .

# 4. 提交文件
git commit -m "部署到GitHub Actions - 每日定时问候工作流"

# 5. 添加远程仓库
git remote add origin https://github.com/your-username/daily-greeting.git

# 6. 推送到GitHub
git push -u origin main
```

**如果推送时需要身份验证：**
```bash
# 配置GitHub用户名和邮箱
git config user.name "your-name"
git config user.email "your-email@example.com"

# 使用SSH方式（推荐，需要配置SSH密钥）
git remote set-url origin git@github.com:your-username/daily-greeting.git

# 或使用HTTPS + Personal Access Token
git remote set-url origin https://your-token@github.com/your-username/daily-greeting.git
```

---

### 第三步：启用GitHub Actions

1. **访问仓库**
   - 打开 https://github.com/your-username/daily-greeting

2. **启用Actions**
   - 点击 **Actions** 标签
   - 点击 **I understand my workflows, go ahead and enable them**
   - （如果提示启用）

3. **查看工作流**
   - 点击左侧菜单的 **每日定时问候**
   - 可以看到定时任务配置

---

### 第四步：配置时间（重要）

默认时间使用的是UTC时间，需要调整为北京时间：

#### 打开工作流文件
1. 点击 **Code** 标签
2. 进入 `.github/workflows/` 目录
3. 点击 `daily-greeting.yml`
4. 点击 **铅笔图标** 编辑

#### 调整时间表达式

**默认（UTC时间）：**
```yaml
on:
  schedule:
    - cron: '30 0 * * *'  # 00:30 UTC = 08:30 北京时间
    - cron: '31 0 * * *'  # 00:31 UTC = 08:31 北京时间
    - cron: '30 14 * * *' # 14:30 UTC = 22:30 北京时间
```

**调整为北京时间（7:30, 7:31, 22:30）：**
```yaml
on:
  schedule:
    - cron: '30 23 * * *'  # 23:30 UTC = 07:30+1 北京时间
    - cron: '31 23 * * *'  # 23:31 UTC = 07:31+1 北京时间
    - cron: '30 14 * * *'  # 14:30 UTC = 22:30 北京时间
```

**时间计算公式：**
- 北京时间 = UTC + 8小时
- 例如：UTC 14:30 = 北京时间 22:30

5. 修改后点击 **Commit changes** 保存

---

### 第五步：手动触发测试

在调整时间后，可以手动触发测试：

1. 点击 **Actions** 标签
2. 点击 **每日定时问候**
3. 点击 **Run workflow**
4. 选择分支（main）
5. 点击 **Run workflow** 按钮

---

## ⏰ 时区对照表

| 目标时间（北京时间） | UTC时间 | Cron表达式 |
|---------------------|---------|-----------|
| 7:30 | 23:30（前一天） | `30 23 * * *` |
| 7:31 | 23:31（前一天） | `31 23 * * *` |
| 22:30 | 14:30 | `30 14 * * *` |

---

## 📊 监控运行状态

### 查看工作流运行

1. **访问Actions页面**
   - 仓库页面 → 点击 **Actions** 标签

2. **查看运行历史**
   - 左侧选择 **每日定时问候**
   - 可以看到每次运行的记录

3. **查看运行详情**
   - 点击某次运行记录
   - 可以查看：
     - 运行时间
     - 执行步骤
     - 日志输出

### 查看日志

1. 点击某次运行记录
2. 点击具体步骤（如"发送天气预报"）
3. 可以看到详细日志：
   ```
   Run python -c "from src.graphs.graph import main_graph; ..."
   ```

---

## 🔧 常见问题

### 问题1：工作流没有自动运行

**原因：**
- GitHub Actions的定时任务可能会有5-15分钟的延迟
- 时区配置不正确
- 工作流文件格式错误

**解决方法：**
1. 检查cron表达式是否正确
2. 查看Actions页面是否有运行记录
3. 手动触发测试

### 问题2：推送代码失败

**原因：**
- 没有权限访问仓库
- Git凭据未配置
- 仓库地址错误

**解决方法：**

**方案A：使用SSH**
```bash
# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"

# 查看公钥
cat ~/.ssh/id_rsa.pub

# 将公钥添加到GitHub
# Settings → SSH and GPG keys → New SSH key

# 使用SSH方式推送
git remote set-url origin git@github.com:your-username/daily-greeting.git
git push -u origin main
```

**方案B：使用Personal Access Token**
```bash
# 创建GitHub Token
# Settings → Developer settings → Personal access tokens → Generate new token
# 选择权限：repo, workflow

# 使用Token推送
git remote set-url origin https://your-token@github.com/your-username/daily-greeting.git
git push -u origin main
```

### 问题3：工作流运行失败

**原因：**
- Python依赖未安装
- 配置文件路径错误
- 环境变量缺失

**解决方法：**
1. 查看Actions日志中的错误信息
2. 检查依赖是否完整
3. 验证配置文件路径

---

## 📝 文件说明

| 文件 | 说明 |
|------|------|
| `.github/workflows/daily-greeting.yml` | GitHub Actions工作流配置 |
| `scripts/deploy_github.sh` | 自动化部署脚本 |
| `requirements.txt` | Python依赖列表 |

---

## 🎯 总结

### 完整操作流程

1. ✅ 创建GitHub仓库
2. ✅ 运行部署脚本：`bash scripts/deploy_github.sh`
3. ✅ 推送代码到GitHub
4. ✅ 启用GitHub Actions
5. ✅ 调整时间配置
6. ✅ 手动触发测试
7. ✅ 等待自动运行

### 优点

- ✅ **完全免费**：GitHub Actions对公开仓库免费
- ✅ **零运维**：无需管理服务器
- ✅ **易于监控**：GitHub提供完整的运行历史和日志
- ✅ **自动运行**：按配置的时间自动执行

### 注意事项

- ⚠️ 定时任务可能有5-15分钟延迟
- ⚠️ 每月有免费运行时长限制（公开仓库：2000分钟）
- ⚠️ 需要调整时区（UTC vs 北京时间）

---

## 📞 获取帮助

如果遇到问题：
1. 查看GitHub Actions日志
2. 检查工作流配置文件
3. 查看GitHub文档：https://docs.github.com/actions

祝您部署顺利！🎉
