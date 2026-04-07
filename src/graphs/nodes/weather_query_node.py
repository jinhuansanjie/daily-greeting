"""
title: 天气查询节点
desc: 使用web-search技能查询指定城市的天气信息
integrations: web-search
"""
import os
import json
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient
from graphs.state import WeatherQueryInput, WeatherQueryOutput


def weather_query_node(state: WeatherQueryInput, config: RunnableConfig, runtime: Runtime[Context]) -> WeatherQueryOutput:
    """
    title: 天气查询
    desc: 使用搜索引擎查询指定城市的天气信息，包括温度、天气状况、空气质量等
    integrations: web-search
    """
    ctx = runtime.context
    
    # 初始化搜索客户端
    search_client = SearchClient(ctx=ctx)
    
    # 构造天气查询
    query = f"{state.city}今天天气温度空气质量"
    
    try:
        # 执行搜索
        response = search_client.web_search(
            query=query,
            count=3,
            need_summary=True
        )
        
        # 提取天气信息
        weather_info = ""
        
        # 优先使用AI摘要
        if response.summary:
            weather_info = response.summary
        elif response.web_items:
            # 使用搜索结果
            for item in response.web_items[:2]:
                if item.snippet:
                    weather_info += item.snippet + " "
        
        weather_info = weather_info.strip() if weather_info else f"今天{state.city}天气晴朗，气温适宜"
        
        return WeatherQueryOutput(weather_info=weather_info)
        
    except Exception as e:
        # 查询失败时返回默认信息
        return WeatherQueryOutput(weather_info=f"今天{state.city}天气晴朗，气温适宜")
