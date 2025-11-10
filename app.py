import streamlit as st
import requests
import time
import random

# 页面配置
st.set_page_config(
    page_title="14865数字人训练系统",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 你好！我是基于'14865'训练体系的智能数字人，请先在侧边栏设置API密钥开始训练。"}
    ]
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "current_subject" not in st.session_state:
    st.session_state.current_subject = "会计学"
if "training_round" not in st.session_state:
    st.session_state.training_round = 1

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .avatar-container {
        text-align: center;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .user-message {
        background: #e3f2fd;
        padding: 12px 16px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
    }
    .assistant-message {
        background: #f5f5f5;
        padding: 12px 16px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 80%;
        margin-right: auto;
    }
    .stButton button {
        width: 100%;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 学科数据
SUBJECTS_DATA = {
    "会计学": {"emoji": "📊", "pain_points": ["准则理解", "报表分析", "成本控制"]},
    "税法": {"emoji": "⚖️", "pain_points": ["政策更新", "税务筹划", "合规风险"]},
    "金融学": {"emoji": "💹", "pain_points": ["风险管理", "投资决策", "市场分析"]}
}

# DeepSeek API调用
def call_deepseek_api(user_input, api_key):
    """调用DeepSeek API"""
    if not api_key:
        return "❌ 请先在侧边栏设置API密钥"
    
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        system_prompt = f"""你是{st.session_state.current_subject}专家，基于14865训练体系：
1-人性逻辑, 4-四大准则, 8-质量要求, 6-会计要素, 5-计量属性
请用专业但易懂的方式回答。"""
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "stream": False,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API调用失败: {response.status_code}"
            
    except Exception as e:
        return f"请求出错: {str(e)}"

# 演示模式回复
def get_demo_response(user_input):
    """演示模式下的回复"""
    responses = [
        f"🧠 **基于14865体系分析**：\n\n你的问题『{user_input}』涉及会计核心逻辑。从4大准则来看，需要确保信息可靠性和相关性。",
        f"📊 **专业视角**：\n\n这个问题可以从6大要素角度分析，特别是资产和费用的管理。",
        f"💡 **深入思考**：\n\n结合14865框架，建议从人性逻辑出发，考虑未来价值决策。"
    ]
    return random.choice(responses)

# 侧边栏
def sidebar_config():
    with st.sidebar:
        st.header("⚙️ 系统配置")
        
        # API设置
        st.subheader("🔑 API设置")
        api_key = st.text_input(
            "DeepSeek API密钥",
            type="password",
            value=st.session_state.api_key,
            placeholder="输入你的API密钥"
        )
        st.session_state.api_key = api_key
        
        if api_key:
            st.success("✅ API已配置")
        else:
            st.warning("⚠️ 演示模式")
            st.info("**免费申请**: platform.deepseek.com")
        
        st.markdown("---")
        
        # 学科选择
        st.subheader("📚 学科选择")
        for subject, data in SUBJECTS_DATA.items():
            emoji = data["emoji"]
            if st.button(f"{emoji} {subject}", key=f"sub_{subject}", use_container_width=True):
                st.session_state.current_subject = subject
                st.session_state.messages = [
                    {"role": "assistant", "content": f"🔁 已切换到{subject}训练模式！"}
                ]
                st.rerun()
        
        st.markdown("---")
        
        # 训练控制
        st.subheader("🔄 训练控制")
        if st.button("🗑️ 清除对话", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "对话已清除，开始新的训练！"}
            ]
            st.rerun()
        
        if st.button("⏭️ 下一轮训练", use_container_width=True):
            st.session_state.training_round += 1
            st.session_state.messages = [
                {"role": "assistant", "content": f"🎉 第{st.session_state.training_round}轮训练开始！"}
            ]
            st.rerun()

# 主应用
def main():
    # 顶部标题
    st.markdown("""
    <div class="main-header">
        <h2>🧮 14865数字人训练系统</h2>
        <p>通过AI训练提升专业能力 · 当前学科: {}</p>
    </div>
    """.format(st.session_state.current_subject), unsafe_allow_html=True)
    
    # 布局
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 数字人形象
        st.markdown("""
        <div class="avatar-container">
            <div style='
                background: linear-gradient(135deg, #667eea, #764ba2);
                width: 180px;
                height: 250px;
                border-radius: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 60px;
                margin: 0 auto;
                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            '>
                {}
            </div>
            <h3>🤖 训练数字人</h3>
            <p>14865体系 · 第{}轮训练</p>
        </div>
        """.format(
            SUBJECTS_DATA[st.session_state.current_subject]["emoji"],
            st.session_state.training_round
        ), unsafe_allow_html=True)
        
        # 快速问题
        st.subheader("🚀 快速训练")
        pain_points = SUBJECTS_DATA[st.session_state.current_subject]["pain_points"]
        for pain_point in pain_points:
            if st.button(f"💡 {pain_point}", key=f"quick_{pain_point}", use_container_width=True):
                user_input = f"请分析{st.session_state.current_subject}中的{pain_point}问题"
                st.session_state.quick_question = user_input
                st.rerun()
    
    with col2:
        st.subheader("💬 实时对话训练")
        
        # 显示对话
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
        
        # 处理输入
        if "quick_question" in st.session_state:
            user_input = st.session_state.quick_question
            del st.session_state.quick_question
        else:
            user_input = st.chat_input(f"输入关于{st.session_state.current_subject}的问题...")
        
        if user_input:
            # 添加用户消息
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # 获取回复
            with st.spinner("🤔 思考中..."):
                if st.session_state.api_key:
                    response = call_deepseek_api(user_input, st.session_state.api_key)
                else:
                    response = get_demo_response(user_input)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
    
    # 侧边栏
    sidebar_config()

if __name__ == "__main__":
    main()
