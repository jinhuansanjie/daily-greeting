"""
title: 消息发送节点
desc: 将问候语和语音通过Coze API发送到豆包APP
integrations:
"""
import os
import json
import logging
from datetime import datetime
from typing import Optional
import requests
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import SendMessageInput, SendMessageOutput


logger = logging.getLogger(__name__)

# Coze API 配置
COZE_API_BASE = "https://api.coze.cn"
COZE_API_TOKEN = "pat_5qLzyX5FSrbxJXeFVW9fsWVKpq9OR0xIyaIEihOX1R9n58yx1SFciTKl64XhAWUF"
COZE_BOT_ID = "7624738708238942234"


def send_message_to_doubao(text: str, audio_url: str = "") -> dict:
    """
    通过Coze API发送消息到豆包APP
    
    Args:
        text: 文本消息内容
        audio_url: 语音文件URL（可选）
    
    Returns:
        dict: 包含success和message的响应
    """
    # Bot ID - 小暖暖
    bot_id = COZE_BOT_ID
    conversation_id = os.getenv("COZE_CONVERSATION_ID", "")
    
    if not bot_id:
        return {
            "success": False,
            "message": "未配置Bot ID，请设置环境变量 COZE_BOT_ID"
        }
    
    headers = {
        "Authorization": f"Bearer {COZE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # 构建消息内容
    content = text
    if audio_url:
        content = f"{text}\n\n🎙️ 语音播报：{audio_url}"
    
    # 消息体 - Coze API需要user_id参数
    payload = {
        "bot_id": bot_id,
        "stream": False,
        "user_id": "daily_greeting_user",
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": content,
                "content_type": "text"
            }
        ]
    }
    
    # 如果有conversation_id，添加到payload
    if conversation_id:
        payload["conversation_id"] = conversation_id
    
    try:
        # 调用Coze API发送消息
        response = requests.post(
            f"{COZE_API_BASE}/v3/chat",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        result = response.json()
        
        if response.status_code == 200 and result.get("code") == 0:
            chat_id = result.get("data", {}).get("id")
            conversation_id_from_response = result.get("data", {}).get("conversation_id")
            
            # 保存conversation_id供后续使用
            if conversation_id_from_response and not conversation_id:
                logger.info(f"创建新对话: {conversation_id_from_response}")
            
            logger.info(f"消息发送成功，chat_id: {chat_id}")
            return {
                "success": True,
                "message": "消息发送成功",
                "chat_id": chat_id
            }
        else:
            error_msg = result.get("msg", "未知错误")
            logger.error(f"消息发送失败: {error_msg}")
            return {
                "success": False,
                "message": f"发送失败: {error_msg}"
            }
            
    except requests.exceptions.Timeout:
        logger.error("请求超时")
        return {
            "success": False,
            "message": "请求超时，请稍后重试"
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"网络请求错误: {str(e)}")
        return {
            "success": False,
            "message": f"网络错误: {str(e)}"
        }
    except Exception as e:
        logger.error(f"发送消息异常: {str(e)}")
        return {
            "success": False,
            "message": f"发送异常: {str(e)}"
        }


def send_message_node(state: SendMessageInput, config: RunnableConfig, runtime: Runtime[Context]) -> SendMessageOutput:
    """
    title: 消息发送
    desc: 将问候语和语音通过Coze API发送到豆包APP"小暖暖"
    integrations:
    """
    ctx = runtime.context
    
    try:
        # 调用Coze API发送消息
        result = send_message_to_doubao(
            text=state.greeting_text,
            audio_url=state.audio_url
        )
        
        if result.get("success"):
            logger.info(f"成功发送到豆包APP: {result.get('message')}")
            return SendMessageOutput(send_status="success")
        else:
            logger.warning(f"发送到豆包APP失败: {result.get('message')}")
            return SendMessageOutput(send_status=f"failed: {result.get('message')}")
            
    except Exception as e:
        logger.error(f"消息发送节点异常: {str(e)}")
        return SendMessageOutput(send_status="failed")
