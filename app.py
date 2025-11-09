import streamlit as st
import requests
import time

# 强制清理会话状态
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.messages = []

# 页面配置
st.set_page_config(
    page_title="实时对话数字人",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 添加安全渲染保护
def safe_render():
    """安全的渲染函数，避免DOM操作冲突"""
    try:
        # 主界面
        st.title("💬 实时对话数字人 - 课业项目")
        st.markdown("---")
        
        # 初始化消息
        if len(st.session_state.messages) == 0:
            st.session_state.messages = [
                {"role": "assistant", "content": "你好！我是你的数字人课业助手，请随时向我提问关于智能体或数字人的问题。"}
            ]
        
        # 安全渲染消息
        for i, message in enumerate(st.session_state.messages):
            try:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            except Exception as e:
                st.error(f"渲染消息时出错: {str(e)}")
                continue
        
        return True
    except Exception as e:
        st.error(f"界面渲染错误: {str(e)}")
        return False

# 渲染界面
if safe_render():
    # 用户输入
    if prompt := st.chat_input("请输入你的问题..."):
        try:
            # 添加用户消息
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # 显示用户消息
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # 生成回复（简化版，避免复杂操作）
            with st.chat_message("assistant"):
                with st.spinner("思考中..."):
                    # 模拟AI回复
                    time.sleep(0.5)  # 避免立即响应
                    responses = [
                        "这是一个关于数字人技术的很好问题！数字人包含3D建模、AI对话和语音合成等技术。",
                        "在智能体架构中，我们需要考虑感知、决策和执行三个核心模块。",
                        "实时对话系统需要处理自然语言理解、对话管理和自然语言生成。",
                        "我们的课业项目正在实践这些前沿AI技术！",
                        f"我已经收到你的问题：'{prompt}'。在完整版本中，这将由AI模型提供专业解答。"
                    ]
                    import random
                    response = random.choice(responses)
                    
                    st.markdown(response)
            
            # 添加助手回复
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # 强制重新渲染
            st.rerun()
            
        except Exception as e:
            st.error(f"处理对话时出错: {str(e)}")

# 添加调试信息
with st.sidebar:
    st.header("调试信息")
    st.write(f"消息数量: {len(st.session_state.messages)}")
    if st.button("重置对话"):
        st.session_state.messages = [
            {"role": "assistant", "content": "对话已重置！请问我关于数字人的问题。"}
        ]
        st.rerun()
    if st.button("清除缓存"):
        st.cache_data.clear()
        st.rerun()
