# 项目概述
- **名称**: 每日定时问候工作流
- **功能**: 每天定时发送天气预报和问候语到企业微信群，包含天气预报、早安问候和晚安问候

## 定时发送规则
- **7:30 天气预报**: 播报当天天气概况、温度范围、空气质量等
- **8:00 早安问候**: 起床问候语 + 天气提醒 + 贴心建议
- **23:00 晚安问候**: 温馨道别语 + 睡眠建议

## 工作流架构
```
定时触发 → 天气查询 → 问候语生成 → 语音合成 → 消息发送（企业微信群）
```

## 节点清单

| 节点名 | 文件位置 | 类型 | 功能描述 | 配置文件 |
|-------|---------|------|---------|---------|
| trigger | `nodes/trigger_node.py` | task | 根据时间判断触发类型 | - |
| weather_query | `nodes/weather_query_node.py` | task | 查询指定城市天气信息 | - |
| greeting_generate | `nodes/greeting_generate_node.py` | agent | 使用LLM生成内容 | `config/greeting_llm_cfg.json` |
| tts | `nodes/tts_node.py` | task | 将文字转换为语音 | - |
| send_message | `nodes/send_message_node.py` | task | 发送消息到企业微信群 | - |

**类型说明**: task(任务节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 技能使用
- **web-search**: 节点`weather_query`使用，用于查询实时天气
- **llm**: 节点`greeting_generate`使用，用于生成天气预报和问候语
- **audio/tts**: 节点`tts`使用，用于语音合成

## 配置说明
- **城市设置**: 可在GraphInput中指定，默认"北京"
- **LLM模型**: doubao-seed-2-0-lite-260215（均衡性能与成本）
- **语音合成**: 使用温柔女声（zh_female_vv_uranus_bigtts）
- **企业微信机器人**: 已配置Webhook Key

## 企业微信机器人配置
- **Webhook Key**: `5517f6eb-3f3e-4277-b05a-52c884cf0f42`
- **推送方式**: 企业微信群机器人
- **消息类型**: 文本消息（含语音链接）

## 外部定时触发配置

需要在外部配置定时任务，建议使用cron表达式：

### 方案1: 使用系统cron
```bash
# 编辑crontab
crontab -e

# 添加定时任务
30 7 * * * curl -X POST "你的工作流触发API" -d '{"city":"北京","trigger_type":"weather"}'
0 8 * * * curl -X POST "你的工作流触发API" -d '{"city":"北京","trigger_type":"morning"}'
0 23 * * * curl -X POST "你的工作流触发API" -d '{"city":"北京","trigger_type":"evening"}'
```

### 方案2: 使用Python调度器
```python
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', hour=7, minute=30)
def weather_job():
    main_graph.invoke({"city": "北京", "trigger_type": "weather"})

@scheduler.scheduled_job('cron', hour=8, minute=0)
def morning_job():
    main_graph.invoke({"city": "北京", "trigger_type": "morning"})

@scheduler.scheduled_job('cron', hour=23, minute=0)
def evening_job():
    main_graph.invoke({"city": "北京", "trigger_type": "evening"})

scheduler.start()
```

## 测试运行
```python
from src.graphs.graph import main_graph

# 测试天气预报
result = main_graph.invoke({
    "city": "北京",
    "trigger_type": "weather"
})

# 测试早安问候
result = main_graph.invoke({
    "city": "北京",
    "trigger_type": "morning"
})

# 测试晚安问候
result = main_graph.invoke({
    "city": "北京",
    "trigger_type": "evening"
})
```

## 使用说明
1. 消息会自动发送到配置的企业微信群
2. 每条消息包含温馨的问候语和语音播报链接
3. 点击语音链接即可播放语音
4. 支持自定义城市名称
