"""
title: 语音合成节点
desc: 使用TTS技能将问候语文本转换为语音
integrations: audio
"""
import os
import json
import requests
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import TTSClient
from src.graphs.state import TTSInput, TTSOutput


def tts_node(state: TTSInput, config: RunnableConfig, runtime: Runtime[Context]) -> TTSOutput:
    """
    title: 语音合成
    desc: 使用文字转语音技术将问候语转换为语音文件
    integrations: audio
    """
    ctx = runtime.context

    # 初始化TTS客户端
    tts_client = TTSClient(ctx=ctx)

    try:
        # 调用TTS服务生成语音
        audio_url, audio_size = tts_client.synthesize(
            uid="daily_greeting",
            text=state.greeting_text,
            speaker="zh_female_vv_uranus_bigtts",  # 使用温柔女声Vivi
            audio_format="mp3",
            sample_rate=24000
        )

        return TTSOutput(audio_url=audio_url)

    except Exception as e:
        # TTS失败时返回空URL
        return TTSOutput(audio_url="")
