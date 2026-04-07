"""
title: 定时触发节点
desc: 根据传入的trigger_type决定发送内容类型
integrations:
"""
import os
import json
from typing import Literal
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import TriggerInput, TriggerOutput


def trigger_node(state: TriggerInput, config: RunnableConfig, runtime: Runtime[Context]) -> TriggerOutput:
    """
    title: 定时触发判断
    desc: 根据传入的trigger_type决定发送类型：
          - weather: 7:30天气预报
          - morning: 8:00早安问候
          - evening: 23:00晚安问候
    integrations:
    """
    ctx = runtime.context
    
    # 直接使用传入的trigger_type
    trigger_type = state.trigger_type
    
    # 验证trigger_type有效性
    valid_types = ["weather", "morning", "evening"]
    if trigger_type not in valid_types:
        trigger_type = "morning"
    
    return TriggerOutput(trigger_type=trigger_type)
