# 状态定义： 图的全局状态、出入参定义，节点的出入参定义
from typing import Literal, Optional
from pydantic import BaseModel, Field


class GlobalState(BaseModel):
    """全局状态定义"""
    trigger_type: str = Field(default="", description="触发类型：morning（早安）/ evening（晚安）")
    city: str = Field(default="苏州", description="城市名称")
    weather_info: str = Field(default="", description="天气查询结果")
    greeting_text: str = Field(default="", description="生成的问候语文本")
    audio_url: str = Field(default="", description="生成的语音文件URL")
    send_status: str = Field(default="", description="发送状态：success/failed")


class GraphInput(BaseModel):
    """工作流的输入"""
    city: str = Field(default="苏州", description="城市名称，用于查询当地天气")
    trigger_type: str = Field(default="morning", description="触发类型：morning（早安）/ evening（晚安）")


class GraphOutput(BaseModel):
    """工作流的输出"""
    greeting_text: str = Field(..., description="生成的问候语文本")
    audio_url: str = Field(..., description="生成的语音文件URL")
    send_status: str = Field(..., description="发送状态")


class TriggerInput(BaseModel):
    """定时触发节点的输入"""
    trigger_type: str = Field(default="morning", description="触发类型：morning（早安）/ evening（晚安）")


class TriggerOutput(BaseModel):
    """定时触发节点的输出"""
    trigger_type: str = Field(..., description="触发类型：weather（天气预报）/ morning（早安问候）/ evening（晚安问候）")


class WeatherQueryInput(BaseModel):
    """天气查询节点的输入"""
    city: str = Field(default="北京", description="城市名称")


class WeatherQueryOutput(BaseModel):
    """天气查询节点的输出"""
    weather_info: str = Field(..., description="天气查询结果")


class GreetingGenerateInput(BaseModel):
    """问候语生成节点的输入"""
    trigger_type: str = Field(default="morning", description="触发类型：weather（天气预报）/ morning（早安）/ evening（晚安）")
    weather_info: str = Field(default="", description="天气查询结果")


class GreetingGenerateOutput(BaseModel):
    """问候语生成节点的输出"""
    greeting_text: str = Field(..., description="生成的问候语文本")


class TTSInput(BaseModel):
    """语音合成节点的输入"""
    greeting_text: str = Field(..., description="需要转换为语音的文本")


class TTSOutput(BaseModel):
    """语音合成节点的输出"""
    audio_url: str = Field(..., description="生成的语音文件URL")


class SendMessageInput(BaseModel):
    """消息发送节点的输入"""
    greeting_text: str = Field(..., description="问候语文本")
    audio_url: str = Field(..., description="语音文件URL")


class SendMessageOutput(BaseModel):
    """消息发送节点的输出"""
    send_status: str = Field(..., description="发送状态：success/failed")
