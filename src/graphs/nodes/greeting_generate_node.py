"""
title: 问候语生成节点
desc: 使用LLM技能根据天气和触发类型生成温馨问候语
integrations: llm
"""
import os
import json
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import SystemMessage, HumanMessage
from src.graphs.state import GreetingGenerateInput, GreetingGenerateOutput


def greeting_generate_node(state: GreetingGenerateInput, config: RunnableConfig, runtime: Runtime[Context]) -> GreetingGenerateOutput:
    """
    title: 问候语生成
    desc: 使用大语言模型根据触发类型（早安/晚安）和天气信息生成温馨的问候语
    integrations: llm
    """
    ctx = runtime.context

    # 读取LLM配置文件
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
    with open(cfg_file, 'r') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    # 渲染用户提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "trigger_type": state.trigger_type,
        "weather_info": state.weather_info
    })

    # 初始化LLM客户端
    client = LLMClient(ctx=ctx)

    try:
        # 调用大语言模型
        response = client.invoke(
            messages=[
                SystemMessage(content=sp),
                HumanMessage(content=user_prompt_content)
            ],
            model=llm_config.get("model", "doubao-seed-2-0-lite-260215"),
            temperature=llm_config.get("temperature", 0.7),
            max_completion_tokens=llm_config.get("max_completion_tokens", 1000)
        )

        # 提取生成的问候语
        greeting_text = ""
        if isinstance(response.content, str):
            greeting_text = response.content.strip()
        elif isinstance(response.content, list):
            # 处理列表格式
            greeting_text = " ".join([
                item.get("text", "") if isinstance(item, dict) else str(item)
                for item in response.content
            ]).strip()
        else:
            greeting_text = str(response.content).strip()

        return GreetingGenerateOutput(greeting_text=greeting_text)

    except Exception as e:
        # 生成失败时返回默认问候语
        if state.trigger_type == "morning":
            default_greeting = "早上好！新的一天开始了，愿你今天心情愉快！"
        else:
            default_greeting = "晚安！祝你有个好梦，明天见！"
        return GreetingGenerateOutput(greeting_text=default_greeting)
