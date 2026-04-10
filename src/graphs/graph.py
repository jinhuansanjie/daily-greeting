# 主图编排实现
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from src.graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)

# 导入节点函数
from src.graphs.nodes.trigger_node import trigger_node
from src.graphs.nodes.weather_query_node import weather_query_node
from src.graphs.nodes.greeting_generate_node import greeting_generate_node
from src.graphs.nodes.tts_node import tts_node
from src.graphs.nodes.send_message_node import send_message_node


# 创建状态图
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("trigger", trigger_node)
builder.add_node("weather_query", weather_query_node)
builder.add_node("greeting_generate", greeting_generate_node, metadata={"type": "agent", "llm_cfg": "config/greeting_llm_cfg.json"})
builder.add_node("tts", tts_node)
builder.add_node("send_message", send_message_node)

# 设置入口点
builder.set_entry_point("trigger")

# 添加边
builder.add_edge("trigger", "weather_query")
builder.add_edge("weather_query", "greeting_generate")
builder.add_edge("greeting_generate", "tts")
builder.add_edge("tts", "send_message")
builder.add_edge("send_message", END)

# 编译图
main_graph = builder.compile()
