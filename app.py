import streamlit as st
import requests
import json
import base64
import time

# 页面设置
st.set_page_config(
    page_title="智能数字人助手",
    page_icon="🤖",
    layout="wide"
)

# 自定义CSS - 包含数字人形象区域
st.markdown("""
<style>
    .avatar-container {
        width: 200px;
        height: 300px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .avatar-image {
        font-size: 80px;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    .speaking .avatar-image {
        animation: talk 0.5s ease-in-out infinite;
    }
    @keyframes talk {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_speaking" not in st.session_state:
    st.session_state.is_speaking = False

# DeepSeek API调用函数
def call_deepseek_api(user_input):
    """调用DeepSeek API进行实时对话"""
    try:
        # 这里使用模拟回复，你可以替换为真实的API调用
        responses = [
            f"你好！我理解你想了解：{user_input}。数字人是结合了3D建模和AI技术的虚拟助手。",
            f"关于'{user_input}'，在智能体系统中，这涉及到自然语言处理和对话管理技术。",
            f"很好的问题！{user_input}正是我们数字人技术的核心应用场景。",
            f"我收到你的问题了：{user_input}。实时对话系统需要处理语音识别、语义理解和语音合成。",
            f"{user_input}？这让我想到数字人的多个技术模块：形象生成、语音交互和AI大脑。"
        ]
        import random
        return random.choice(responses)
        
    except Exception as e:
        return f"抱歉，暂时无法处理请求。错误：{str(e)}"

# 语音合成函数（使用浏览器TTS）
def text_to_speech(text):
    """使用浏览器语音合成"""
    try:
        # 创建语音合成代码
        tts_script = f"""
        <script>
            if ('speechSynthesis' in window) {{
                var msg = new SpeechSynthesisUtterance();
                msg.text = "{text}";
                msg.lang = 'zh-CN';
                msg.rate = 1.0;
                msg.pitch = 1.0;
                window.speechSynthesis.speak(msg);
            }}
        </script>
        """
        return tts_script
    except Exception as e:
        return ""

# 主界面布局
col1, col2 = st.columns([1, 2])

with col1:
    st.header("🎭 数字人形象")
    
    # 数字人形象容器
    speaking_class = "speaking" if st.session_state.is_speaking else ""
    st.markdown(f"""
    <div class="avatar-container {speaking_class}">
        <div class="avatar-image">🤖</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 状态显示
    if st.session_state.is_speaking:
        st.success("🔊 正在说话...")
    else:
        st.info("🎯 等待提问")
    
    # 语音控制
    st.subheader("语音设置")
    auto_speech = st.checkbox("🔊 自动语音回复", value=True)
    if st.button("🔄 测试语音"):
        test_script = text_to_speech("数字人语音系统测试成功！")
        st.components.v1.html(test_script, height=0)

with col2:
    st.header("💬 实时对话")
    
    # 显示对话历史
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # 实时对话输入
    if prompt := st.chat_input("请输入问题，例如：什么是数字人？"):
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 获取AI回复
        with st.chat_message("assistant"):
            with st.spinner("🤔 思考中..."):
                # 设置说话状态
                st.session_state.is_speaking = True
                
                # 获取AI回复
                response = call_deepseek_api(prompt)
                st.markdown(response)
                
                # 添加助手回复到历史
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # 语音合成
                if auto_speech:
                    tts_script = text_to_speech(response)
                    st.components.v1.html(tts_script, height=0)
                    time.sleep(2)  # 模拟说话时间
        
        # 结束说话状态
        st.session_state.is_speaking = False
        st.rerun()

# 控制面板
with st.sidebar:
    st.header("控制面板")
    
    if st.button("🗑️ 清除对话历史"):
        st.session_state.messages = []
        st.session_state.is_speaking = False
        st.rerun()
    
    if st.button("🔧 重新加载"):
        st.rerun()
    
    st.markdown("---")
    st.subheader("使用说明")
    st.write("""
    1. 在输入框提问任何问题
    2. 数字人会实时回答
    3. 开启语音功能可听到回复
    4. 形象会随说话状态变化
    """)
    
    st.markdown("---")
    st.subheader("技术特性")
    st.write("✅ 实时对话")
    st.write("✅ 数字人形象") 
    st.write("✅ 语音合成")
    st.write("✅ 响应式设计")

# 页脚
st.markdown("---")
st.caption("智能数字人系统 | 支持实时对话与语音交互")
