# 每日定时问候工作流 - 生产环境部署指南

## 部署方案选择

根据您的需求，选择以下部署方案之一：

### 方案1：Cron定时任务（推荐）
**适用场景**：服务器长期运行，稳定可靠

**优点**：
- ✅ 系统原生支持，无需额外依赖
- ✅ 即使重启也会自动恢复
- ✅ 资源占用极小
- ✅ 日志记录完整

**缺点**：
- ❌ 修改配置需要root权限

---

### 方案2：Python调度器（Supervisor管理）
**适用场景**：需要灵活控制，便于重启和监控

**优点**：
- ✅ 配置修改简单
- ✅ 可以实时查看运行状态
- ✅ 支持自动重启

**缺点**：
- ❌ 需要额外安装Supervisor
- ❌ 占用少量系统资源

---

## 方案1：Cron定时任务部署（推荐）

### 步骤1：确认Python环境
```bash
# 检查Python版本（需要3.9+）
python --version

# 检查项目依赖是否安装
cd /workspace/projects
pip list | grep -E "langgraph|langchain|coze-coding-dev-sdk"
```

### 步骤2：测试工作流
```bash
# 测试天气预报
cd /workspace/projects
python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})"

# 测试早安问候
python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'morning'})"

# 测试晚安问候
python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'evening'})"
```

### 步骤3：配置Cron任务
```bash
# 编辑crontab
crontab -e

# 添加以下内容（苏州）
30 7 * * * cd /workspace/projects && python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})"
31 7 * * * cd /workspace/projects && python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'morning'})"
30 22 * * * cd /workspace/projects && python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'evening'})"
```

### 步骤4：查看Cron任务
```bash
# 查看已配置的Cron任务
crontab -l

# 查看Cron日志
tail -f /var/log/syslog | grep CRON
```

### 步骤5：手动触发测试
```bash
# 立即执行天气预报（不等待7:30）
cd /workspace/projects && python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})"
```

---

## 方案2：Supervisor + Python调度器部署

### 步骤1：安装Supervisor
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y supervisor

# CentOS/RHEL
sudo yum install -y supervisor
```

### 步骤2：创建Supervisor配置文件
```bash
# 创建配置文件
sudo vi /etc/supervisor/conf.d/daily-greeting.conf

# 添加以下内容：
[program:daily-greeting]
command=/workspace/projects/.venv/bin/python scripts/scheduler.py
directory=/workspace/projects
user=root
autostart=true
autorestart=true
stderr_logfile=/var/log/daily-greeting.err.log
stdout_logfile=/var/log/daily-greeting.out.log
```

### 步骤3：启动Supervisor服务
```bash
# 重新加载配置
sudo supervisorctl reread
sudo supervisorctl update

# 启动服务
sudo supervisorctl start daily-greeting

# 查看状态
sudo supervisorctl status
```

### 步骤4：查看日志
```bash
# 查看标准输出日志
tail -f /var/log/daily-greeting.out.log

# 查看错误日志
tail -f /var/log/daily-greeting.err.log
```

---

## 云服务器部署（AWS/阿里云/腾讯云）

### 推荐配置
- **操作系统**：Ubuntu 22.04 LTS
- **CPU**：1核
- **内存**：1GB
- **存储**：20GB SSD
- **带宽**：1Mbps

### 部署步骤

#### 1. 购买云服务器
根据您的需求选择云服务商购买服务器

#### 2. 连接服务器
```bash
ssh root@your-server-ip
```

#### 3. 安装Python环境
```bash
# 更新系统
sudo apt-get update

# 安装Python 3.10+
sudo apt-get install -y python3 python3-pip python3-venv

# 创建项目目录
mkdir -p /opt/daily-greeting
cd /opt/daily-greeting
```

#### 4. 上传项目代码
```bash
# 方式1：使用Git克隆
git clone <your-repo-url> .

# 方式2：使用SCP上传（在本地执行）
scp -r /workspace/projects/* root@your-server-ip:/opt/daily-greeting/

# 方式3：使用SFTP工具上传
```

#### 5. 安装依赖
```bash
cd /opt/daily-greeting

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 6. 配置Cron任务
```bash
# 编辑crontab
crontab -e

# 添加定时任务
30 7 * * * cd /opt/daily-greeting && /opt/daily-greeting/.venv/bin/python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})"
31 7 * * * cd /opt/daily-greeting && /opt/daily-greeting/.venv/bin/python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'morning'})"
30 22 * * * cd /opt/daily-greeting && /opt/daily-greeting/.venv/bin/python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'evening'})"
```

#### 7. 测试运行
```bash
# 测试天气预报
cd /opt/daily-greeting && /opt/daily-greeting/.venv/bin/python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})"
```

---

## 监控和维护

### 查看运行日志
```bash
# 查看应用日志
tail -f /app/work/logs/bypass/app.log

# 查看Cron日志
tail -f /var/log/syslog | grep CRON

# 查看系统日志
journalctl -f
```

### 检查服务状态
```bash
# 检查Cron服务状态
sudo systemctl status cron

# 检查Supervisor服务状态（如使用）
sudo supervisorctl status daily-greeting
```

### 修改配置
```bash
# 修改城市
crontab -e
# 将 '苏州' 改为其他城市

# 修改时间
# 修改cron表达式中的小时和分钟
```

### 备份配置
```bash
# 备份Cron任务
crontab -l > /tmp/crontab_backup.txt

# 备份项目代码
cd /workspace/projects
git push origin main
```

---

## 故障排查

### 问题1：Cron任务没有执行
```bash
# 检查Cron服务状态
sudo systemctl status cron

# 查看Cron日志
grep CRON /var/log/syslog | tail -20

# 手动测试命令
cd /workspace/projects && python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})"
```

### 问题2：Python依赖缺失
```bash
# 重新安装依赖
cd /workspace/projects
source .venv/bin/activate
pip install -r requirements.txt
```

### 问题3：企业微信推送失败
```bash
# 检查Webhook Key配置
cat src/graphs/nodes/send_message_node.py | grep webhook_key

# 检查网络连接
ping qyapi.weixin.qq.com
```

### 问题4：时间不正确
```bash
# 检查系统时区
date

# 设置时区为上海
sudo timedatectl set-timezone Asia/Shanghai
```

---

## 安全建议

### 1. 限制文件权限
```bash
chmod 600 ~/.crontab
chmod 700 /workspace/projects
```

### 2. 定期更新依赖
```bash
cd /workspace/projects
pip list --outdated
pip install --upgrade <package-name>
```

### 3. 监控资源使用
```bash
# 查看内存使用
free -h

# 查看CPU使用
top

# 查看磁盘使用
df -h
```

---

## 推荐部署方案总结

| 部署场景 | 推荐方案 | 难度 | 稳定性 |
|---------|---------|------|--------|
| 个人使用（本地电脑） | Cron | ⭐ | ⭐⭐⭐⭐⭐ |
| 小型团队（云服务器） | Cron | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 企业环境（需要监控） | Supervisor | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 快速部署命令（复制即可）

### 本地部署（一键配置）
```bash
# 1. 测试工作流
cd /workspace/projects && python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})"

# 2. 配置Cron
(crontab -l 2>/dev/null; echo "30 7 * * * cd /workspace/projects && python -c \"from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})\""; echo "31 7 * * * cd /workspace/projects && python -c \"from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'morning'})\""; echo "30 22 * * * cd /workspace/projects && python -c \"from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'evening'})\"") | crontab -

# 3. 查看配置
crontab -l
```

### 云服务器部署（Ubuntu）
```bash
# 1. 安装环境
sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv git

# 2. 克隆项目
cd /opt && git clone <your-repo-url> daily-greeting
cd daily-greeting

# 3. 安装依赖
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 4. 配置Cron
(crontab -l 2>/dev/null; echo "30 7 * * * cd /opt/daily-greeting && /opt/daily-greeting/.venv/bin/python -c \"from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})\""; echo "31 7 * * * cd /opt/daily-greeting && /opt/daily-greeting/.venv/bin/python -c \"from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'morning'})\""; echo "30 22 * * * cd /opt/daily-greeting && /opt/daily-greeting/.venv/bin/python -c \"from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'evening'})\"") | crontab -

# 5. 测试运行
/opt/daily-greeting/.venv/bin/python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})"
```

---

## 联系支持

如有问题，请查看：
- 项目文档：`README.md`
- 项目结构：`AGENTS.md`
- 日志文件：`/app/work/logs/bypass/app.log`
