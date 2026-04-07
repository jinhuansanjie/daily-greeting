"""
title: 定时触发节点
desc: 判断当前是早安还是晚安触发
integrations:
"""
import os
import json
from typing import Literal
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import TriggerInput, TriggerOutput


def trigger_node(state: TriggerInput, config: RunnableConfig, runtime: Runtime[Context]) -> TriggerOutput:
    """
    title: 定时触发判断
    desc: 判断当前是早安还是晚安触发，用于决定发送哪种类型的问候语
    integrations:
    """
    ctx = runtime.context
    
    # 获取当前时间
    current_hour = datetime.now().hour
    
    # 判断是早安还是晚安
    if 6 <= current_hour < 12:
        trigger_type = "morning"
    elif 20 <= current_hour < 24 or 0 <= current_hour < 2:
        trigger_type = "evening"
    else:
        # 默认早安
        trigger_type = "morning"
    
    return TriggerOutput(trigger_type=trigger_type)
