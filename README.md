# 每日定时问候工作流

## 项目简介
每天定时向企业微信群发送天气预报和温馨问候，包含语音播报功能。

## 功能特性
- ✅ 实时天气查询（温度、湿度、风向等）
- ✅ 智能问候语生成（早安/晚安）
- ✅ 语音合成（温柔女声）
- ✅ 企业微信群推送
- ✅ 定时自动发送

## 定时发送规则
| 时间 | 内容 | 说明 |
|------|------|------|
| 7:30 | 天气预报 | 当日天气概况、温度、空气质量 |
| 7:31 | 早安问候 | 早安祝福 + 天气提醒 |
| 22:30 | 晚安问候 | 睡前问候 + 睡眠建议 |

## 快速开始

### 1. 测试工作流
```bash
# 测试天气预报
python -c "from src.graphs.graph import main_graph; print(main_graph.invoke({'city': '上海', 'trigger_type': 'weather'}))"

# 测试早安问候
python -c "from src.graphs.graph import main_graph; print(main_graph.invoke({'city': '上海', 'trigger_type': 'morning'}))"

# 测试晚安问候
python -c "from src.graphs.graph import main_graph; print(main_graph.invoke({'city': '上海', 'trigger_type': 'evening'}))"
```

### 2. 配置定时任务

#### 方式1：使用Cron（推荐）
```bash
# 编辑crontab
crontab -e

# 添加以下3行
30 7 * * * cd /workspace/projects && python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '上海', 'trigger_type': 'weather'})"
31 7 * * * cd /workspace/projects && python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '上海', 'trigger_type': 'morning'})"
30 22 * * * cd /workspace/projects && python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '上海', 'trigger_type': 'evening'})"

# 查看已配置的任务
crontab -l
```

#### 方式2：使用Python调度器
```bash
# 运行调度器
cd /workspace/projects
python scripts/scheduler.py

# 停止调度器：按 Ctrl+C
```

## 配置说明

### 修改城市
在定时命令中修改 `city` 参数，例如：
```bash
# 改为深圳
30 7 * * * cd /workspace/projects && python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '深圳', 'trigger_type': 'weather'})"
```

### 企业微信配置
已在 `src/graphs/nodes/send_message_node.py` 中配置Webhook Key。

### 语音配置
- 音色：zh_female_vv_uranus_bigtts（温柔女声Vivi）
- 格式：MP3
- 时长：自动根据文本长度调整

## 工作流架构
```
定时触发 → 天气查询 → 问候语生成 → 语音合成 → 消息发送（企业微信群）
```

## 项目结构
```
├── src/
│   ├── graphs/
│   │   ├── state.py              # 状态定义
│   │   ├── graph.py              # 主图编排
│   │   └── nodes/                # 节点实现
│   │       ├── trigger_node.py   # 触发判断
│   │       ├── weather_query_node.py    # 天气查询
│   │       ├── greeting_generate_node.py # 问候语生成
│   │       ├── tts_node.py       # 语音合成
│   │       └── send_message_node.py     # 消息发送
│   └── tools/                    # 工具定义
├── config/
│   └── greeting_llm_cfg.json     # LLM配置
├── scripts/
│   ├── cron_setup.sh             # Cron脚本
│   └── scheduler.py              # Python调度器
├── AGENTS.md                     # 项目文档
└── README.md                     # 本文件
```

## 技术栈
- Python 3.9+
- LangGraph 1.0
- LangChain 1.0
- coze-coding-dev-sdk (LLM, Search, TTS)
- Pydantic
- APScheduler (Python调度器)

## 常见问题

### Q: 如何修改发送时间？
A: 修改cron命令中的时间参数（小时和分钟），或修改 `scripts/scheduler.py` 中的 `hour` 和 `minute` 参数。

### Q: 如何更换城市？
A: 在cron命令或测试代码中修改 `city` 参数。

### Q: 消息没有发送成功？
A: 检查企业微信Webhook Key是否正确，以及网络连接是否正常。

### Q: 如何查看日志？
A: 查看系统日志文件 `/app/work/logs/bypass/app.log`。

## 许可证
MIT License

