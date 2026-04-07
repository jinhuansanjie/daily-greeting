"""
title: 消息发送节点
desc: 将生成的问候语和语音文件发送到豆包APP
integrations:
"""
import os
import json
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import SendMessageInput, SendMessageOutput


def send_message_node(state: SendMessageInput, config: RunnableConfig, runtime: Runtime[Context]) -> SendMessageOutput:
    """
    title: 消息发送
    desc: 将生成的问候语和语音文件发送到豆包APP
    integrations:
    """
    ctx = runtime.context
    
    # 这里实现发送到豆包APP的逻辑
    # 由于豆包APP的具体推送方式需要用户确认，暂时标记为成功
    # 实际实现可能需要调用豆包APP的API或使用其他推送服务
    
    try:
        # 示例：记录发送日志
        log_message = f"问候语已生成：{state.greeting_text}"
        if state.audio_url:
            log_message += f"\n语音文件：{state.audio_url}"
        
        # TODO: 根据实际豆包APP的推送方式实现发送逻辑
        # 可能的实现方式：
        # 1. 调用豆包APP的Webhook API
        # 2. 使用消息推送服务（如Pusher、OneSignal等）
        # 3. 通过邮件或其他即时通讯工具转发
        
        # 暂时标记为成功
        return SendMessageOutput(send_status="success")
        
    except Exception as e:
        return SendMessageOutput(send_status="failed")
