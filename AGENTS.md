# 项目概述
- **名称**: 每日定时问候工作流
- **功能**: 每天定时发送问候语到豆包APP，包含当地天气预报、起床问候（早安）或晚安问候（晚安）

## 工作流架构
```
定时触发 → 天气查询 → 问候语生成 → 语音合成 → 消息发送
```

## 定时发送规则
- **早安问候**: 每天早上6:00-12:00触发
- **晚安问候**: 每天晚上20:00-24:00或凌晨0:00-2:00触发

## 节点清单

| 节点名 | 文件位置 | 类型 | 功能描述 | 配置文件 |
|-------|---------|------|---------|---------|
| trigger | `nodes/trigger_node.py` | task | 判断触发类型（早安/晚安） | - |
| weather_query | `nodes/weather_query_node.py` | task | 查询指定城市天气信息 | - |
| greeting_generate | `nodes/greeting_generate_node.py` | agent | 使用LLM生成温馨问候语 | `config/greeting_llm_cfg.json` |
| tts | `nodes/tts_node.py` | task | 将文字转换为语音 | - |
| send_message | `nodes/send_message_node.py` | task | 发送消息到豆包APP | - |

**类型说明**: task(任务节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 技能使用
- **web-search**: 节点`weather_query`使用，用于查询实时天气
- **llm**: 节点`greeting_generate`使用，用于生成个性化问候语
- **audio/tts**: 节点`tts`使用，用于语音合成

## 配置说明
- **城市设置**: 可在GraphInput中指定，默认"北京"
- **LLM模型**: doubao-seed-2-0-lite-260215（均衡性能与成本）
- **语音合成**: 使用温柔女声（zh_female_xiaohe_uranus_bigtts）

## 测试运行
```python
from src.graphs.graph import main_graph

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
