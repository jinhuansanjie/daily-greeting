"""
title: 消息发送节点
desc: 将生成的问候语和语音文件发送到豆包APP
integrations:
"""
import os
import json
import logging
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import SendMessageInput, SendMessageOutput


logger = logging.getLogger(__name__)


def send_message_node(state: SendMessageInput, config: RunnableConfig, runtime: Runtime[Context]) -> SendMessageOutput:
    """
    title: 消息发送
    desc: 将生成的问候语和语音文件准备好，待配置豆包APP推送方式后发送
    integrations:
    """
    ctx = runtime.context
    
    try:
        # 构建消息内容
        message_content = {
            "timestamp": datetime.now().isoformat(),
            "text": state.greeting_text,
            "audio_url": state.audio_url,
            "status": "ready"
        }
        
        # 保存消息到消息队列文件
        queue_path = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), "queue")
        os.makedirs(queue_path, exist_ok=True)
        queue_file = os.path.join(queue_path, "pending_messages.jsonl")
        
        with open(queue_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(message_content, ensure_ascii=False) + "\n")
        
        logger.info(f"消息已准备好待发送: {message_content['timestamp']}")
        
        return SendMessageOutput(send_status="ready")
        
    except Exception as e:
        logger.error(f"消息准备失败: {str(e)}")
        return SendMessageOutput(send_status="failed")
