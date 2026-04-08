"""
title: 消息发送节点
desc: 将问候语和语音通过企业微信机器人发送到微信群
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

# 企业微信机器人配置
WECHAT_WEBHOOK_KEY = "24855d96d8c319ac5eab4178313a893cc2"
WECHAT_WEBHOOK_URL = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={WECHAT_WEBHOOK_KEY}"


def send_message_to_wechat(text: str, audio_url: str = "") -> dict:
    """
    通过企业微信机器人发送消息到微信群
    
    Args:
        text: 文本消息内容
        audio_url: 语音文件URL（可选）
    
    Returns:
        dict: 包含success和message的响应
    """
    # 构建消息内容
    content = text
    if audio_url:
        content = f"{text}\n\n🎙️ 语音播报：{audio_url}"
    
    # 消息体
    payload = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    
    try:
        # 调用企业微信机器人API发送消息
        response = requests.post(
            WECHAT_WEBHOOK_URL,
            json=payload,
            timeout=30
        )
        
        result = response.json()
        
        if response.status_code == 200 and result.get("errcode") == 0:
            logger.info(f"消息发送成功到微信群")
            return {
                "success": True,
                "message": "消息发送成功"
            }
        else:
            error_msg = result.get("errmsg", "未知错误")
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
    desc: 将问候语和语音通过企业微信机器人发送到微信群
    integrations:
    """
    ctx = runtime.context
    
    try:
        # 调用企业微信机器人发送消息
        result = send_message_to_wechat(
            text=state.greeting_text,
            audio_url=state.audio_url
        )
        
        if result.get("success"):
            logger.info(f"成功发送到微信群: {result.get('message')}")
            return SendMessageOutput(send_status="success")
        else:
            logger.warning(f"发送到微信群失败: {result.get('message')}")
            return SendMessageOutput(send_status=f"failed: {result.get('message')}")
            
    except Exception as e:
        logger.error(f"消息发送节点异常: {str(e)}")
        return SendMessageOutput(send_status="failed")
