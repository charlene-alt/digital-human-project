import streamlit as st
import requests
import os

# 网络部署专用配置
st.set_page_config(
    page_title="实时对话数字人-网络版",
    page_icon="🤖",
    layout="wide"
)

# 应用主界面
st.title("💬 实时对话数字人（网络版）")
st.caption("在任何设备上打开此网址即可使用 - 课业项目演示")

# 对话功能
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "你好！我是你的网络版数字人助手，专门为智能体与数字人课业设计。请问有什么关于AI或数字人的问题吗？"}
    ]

# 显示对话历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("请输入关于数字人或AI的问题..."):
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 生成智能回复
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            # 这里可以集成AI API，现在先用模拟回复
            if "你好" in prompt or "hi" in prompt.lower():
                response = "你好！我是你的数字人课业助手，可以讨论：智能体架构、数字人技术、AI对话系统等话题。"
            elif "数字人" in prompt:
                response = "数字人技术包含3D建模、语音合成、AI对话系统等多个模块。我们的项目正在实践这些技术！"
            elif "智能体" in prompt:
                response = "智能体是具有自主性的AI系统，能够感知环境、做出决策并执行行动。"
            else:
                response = f"我已经理解你的问题：'{prompt}'。在完整版中，这将由DeepSeek AI提供专业解答！"
            
            st.markdown(response)
    
    # 添加助手回复到历史
    st.session_state.messages.append({"role": "assistant", "content": response})
