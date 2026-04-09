# 每日定时问候工作流 - Docker版本
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . /app/

# 安装Python依赖
RUN pip install -r requirements.txt

# 设置Python路径
ENV PYTHONPATH=/app/src:/app

# 复制Cron配置
COPY scripts/cron_docker /etc/cron.d/daily-greeting

# 设置Cron权限
RUN chmod 0644 /etc/cron.d/daily-greeting
RUN crontab /etc/cron.d/daily-greeting

# 创建日志目录
RUN mkdir -p /app/logs

# 启动Cron并保持容器运行
CMD cron && tail -f /var/log/syslog
