import streamlit as st
import requests
import time
import random
import base64

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
        {"role": "assistant", "content": "👋 你好！我是基于'14865'训练体系的智能数字人，支持语音对话和Gemini AI模型。"}
    ]
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "current_subject" not in st.session_state:
    st.session_state.current_subject = "会计学"
if "training_round" not in st.session_state:
    st.session_state.training_round = 1
if "auto_speech" not in st.session_state:
    st.session_state.auto_speech = True
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gemini-2.5-pro"
if "api_status" not in st.session_state:
    st.session_state.api_status = "disconnected"

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
        border: 1px solid #bbdefb;
    }
    .assistant-message {
        background: #f5f5f5;
        padding: 12px 16px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 80%;
        margin-right: auto;
        border: 1px solid #e0e0e0;
    }
    
    /* API状态指示器 */
    .status-connected {
        background: #4CAF50;
        color: white;
        padding: 8px 12px;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
    }
    .status-disconnected {
        background: #ff9800;
        color: white;
        padding: 8px 12px;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
    }
    .status-testing {
        background: #2196F3;
        color: white;
        padding: 8px 12px;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
    }
    .status-error {
        background: #f44336;
        color: white;
        padding: 8px 12px;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
    }
    
    /* 计费信息样式 */
    .billing-info {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* 模型卡片样式 */
    .model-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 8px 0;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# 学科数据
SUBJECTS_DATA = {
    "会计学": {
        "emoji": "📊", 
        "pain_points": ["准则理解", "报表分析", "成本控制", "税务筹划"],
        "color": "#667eea"
    },
    "税法": {
        "emoji": "⚖️", 
        "pain_points": ["政策更新", "税务筹划", "合规风险", "跨境税务"],
        "color": "#f093fb"
    },
    "金融学": {
        "emoji": "💹", 
        "pain_points": ["风险管理", "投资决策", "市场分析", "金融创新"],
        "color": "#4ECDC4"
    },
    "近现代史纲要": {
        "emoji": "📜", 
        "pain_points": ["历史脉络", "事件关联", "理论理解", "现实意义"],
        "color": "#FF6B6B"
    }
}

# 支持的AI模型（适配新API）
AI_MODELS = {
    "gemini-2.5-pro": {
        "name": "Gemini 2.5 Pro", 
        "description": "高性能模型，按次计费",
        "endpoint": "generateContent"
    },
    "gemini-2.0-flash": {
        "name": "Gemini 2.0 Flash", 
        "description": "快速响应模型",
        "endpoint": "generateContent"
    }
}

# 语音合成功能
def text_to_speech_html(text, rate=1.0, pitch=1.0):
    """生成语音合成的HTML代码"""
    clean_text = text.replace('"', '').replace("'", "").replace("`", "").replace("\n", " ")[:150]
    
    return f'''
    <script>
        function speakText() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance();
                utterance.text = "{clean_text}";
                utterance.lang = 'zh-CN';
                utterance.rate = {rate};
                utterance.pitch = {pitch};
                utterance.volume = 0.8;
                
                utterance.onstart = function() {{
                    console.log('语音开始');
                }};
                
                utterance.onend = function() {{
                    console.log('语音结束');
                }};
                
                setTimeout(() => {{
                    window.speechSynthesis.speak(utterance);
                }}, 500);
            }}
        }}
        speakText();
    </script>
    '''

# API测试函数
def test_api_connection(api_key, model):
    """测试API连接是否正常"""
    if not api_key:
        return False, "未提供API密钥"
    
    try:
        # 使用新的API端点格式
        url = f"https://api.qiyiguo.uk/v1beta/models/{model}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Gemini API的请求格式
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": "请简单回复'连接测试成功'"}
                    ]
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                return True, "✅ API连接成功"
            else:
                return False, "❌ API响应格式错误"
        else:
            return False, f"❌ API连接失败: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ 连接错误: {str(e)}"

# 调用Gemini API
def call_gemini_api(user_input, api_key, subject, model):
    """调用Gemini API进行智能对话"""
    
    # 如果没有API密钥，使用演示模式
    if not api_key:
        return get_demo_response(user_input, subject)
    
    try:
        # 构建API端点
        endpoint = AI_MODELS[model]["endpoint"]
        url = f"https://api.qiyiguo.uk/v1beta/models/{model}:{endpoint}"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # 14865训练体系系统提示词
        system_prompt = f"""你是{subject}专家数字人，严格遵循14865训练体系：

【14865训练体系】
1 - 人性逻辑：基于未来价值的底层决策逻辑
4 - 四大准则：可靠性、相关性、可理解性、可比性  
8 - 八项质量要求：真实性、完整性、及时性、明晰性、实质性、谨慎性、重要性、权责发生制
6 - 六大要素：资产、负债、权益、收入、费用、利润
5 - 五大计量属性：历史成本、重置成本、可变现净值、现值、公允价值

请用专业但友好的方式回答用户问题，体现深入浅出、通俗易懂的特点。"""
        
        # Gemini API的请求格式
        full_prompt = f"{system_prompt}\n\n用户问题：{user_input}"
        
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": full_prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                st.error("API响应格式异常")
                return get_demo_response(user_input, subject)
        else:
            st.error(f"API调用失败: {response.status_code}")
            return get_demo_response(user_input, subject)
            
    except Exception as e:
        st.error(f"请求出错: {str(e)}")
        return get_demo_response(user_input, subject)

# 演示模式回复
def get_demo_response(user_input, subject):
    """演示模式下的智能回复"""
    
    responses = [
        f"""🧠 **基于14865体系的{subject}分析** (演示模式)

📋 **框架应用**：
• 核心指导：4和8（四大准则和八项质量要求）
• 底层逻辑：1（人性逻辑）- 基于未来价值的决策分析

🎯 **专业洞察**：
你的问题「{user_input}」在{subject}领域中，可以从14865体系多角度分析。

💡 **提示**：设置API密钥可启用真实Gemini AI对话，获得更精准的专业分析。""",

        f"""📊 **{subject}专业分析** (演示模式)

🔍 **14865视角**：
• 1-人性逻辑：价值导向决策
• 4-四大准则：建立分析标准
• 6-六大要素：构建分析框架

🚀 **能力提升**：输入API密钥后，Gemini AI将提供深度专业分析。""",
    ]
    
    return random.choice(responses)

# 侧边栏配置
def sidebar_config():
    with st.sidebar:
        # 训练状态
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea, #764ba2); padding: 15px; border-radius: 10px; color: white;'>
            <h3>🎯 训练状态</h3>
            <p>📚 学科: {st.session_state.current_subject}</p>
            <p>🔄 轮次: 第{st.session_state.training_round}轮</p>
            <p>🤖 模型: {AI_MODELS[st.session_state.selected_model]['name']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 计费信息
        st.markdown("""
        <div class="billing-info">
            <h4>💰 计费信息</h4>
            <p><strong>计费方式</strong>: 按次计费</p>
            <p><strong>模型</strong>: Gemini 2.5 Pro</p>
            <p><strong>特点</strong>: 1000k tokens/次</p>
        </div>
        """, unsafe_allow_html=True)
        
        # API状态显示
        st.subheader("🔌 API连接状态")
        
        status_html = {
            "disconnected": '<div class="status-disconnected">🔴 未连接</div>',
            "testing": '<div class="status-testing">🟡 测试中...</div>',
            "connected": '<div class="status-connected">🟢 已连接</div>',
            "error": '<div class="status-error">🔴 连接错误</div>'
        }
        
        st.markdown(status_html[st.session_state.api_status], unsafe_allow_html=True)
        
        # API密钥输入
        api_key = st.text_input(
            "API密钥",
            type="password",
            value=st.session_state.api_key,
            placeholder="输入Gemini API密钥",
            help="从您的API服务商获取"
        )
        
        # 模型选择
        st.markdown("---")
        st.subheader("🤖 AI模型选择")
        
        for model_id, model_info in AI_MODELS.items():
            st.markdown(f"""
            <div class="model-card">
                <strong>{model_info['name']}</strong>
                <br><small>{model_info['description']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"选择 {model_info['name']}", 
                        key=f"model_{model_id}",
                        use_container_width=True,
                        type="primary" if model_id == st.session_state.selected_model else "secondary"):
                st.session_state.selected_model = model_id
                st.success(f"已切换到 {model_info['name']}")
        
        # 测试连接按钮
        st.markdown("---")
        st.subheader("🔧 连接测试")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧪 测试连接", use_container_width=True):
                if api_key:
                    st.session_state.api_status = "testing"
                    st.rerun()
                    success, message = test_api_connection(api_key, st.session_state.selected_model)
                    if success:
                        st.session_state.api_status = "connected"
                        st.session_state.api_key = api_key
                        st.success(message)
                    else:
                        st.session_state.api_status = "error"
                        st.error(message)
                else:
                    st.warning("请输入API密钥")
        
        with col2:
            if st.button("💾 保存设置", use_container_width=True):
                st.session_state.api_key = api_key
                st.success("API密钥已保存！")
        
        st.markdown("---")
        
        # 语音设置
        st.subheader("🎵 语音设置")
        auto_speech = st.checkbox("自动语音回复", value=st.session_state.auto_speech)
        st.session_state.auto_speech = auto_speech
        
        if auto_speech:
            st.success("🔊 语音功能已开启")
            
            if st.button("🎤 测试语音", use_container_width=True):
                test_script = text_to_speech_html("语音功能测试成功！欢迎使用14865训练系统。")
                st.components.v1.html(test_script, height=0)
                st.success("语音测试完成！")
        else:
            st.info("🔇 语音功能已关闭")
        
        st.markdown("---")
        
        # 学科选择
        st.subheader("📚 学科选择")
        for subject, data in SUBJECTS_DATA.items():
            emoji = data["emoji"]
            is_active = "✅" if subject == st.session_state.current_subject else "⚪"
            if st.button(f"{is_active} {emoji} {subject}", key=f"sub_{subject}", use_container_width=True):
                st.session_state.current_subject = subject
                st.session_state.messages = [
                    {"role": "assistant", "content": f"🔁 已切换到{subject}训练模式！基于14865体系进行专业分析。"}
                ]
                st.rerun()
        
        st.markdown("---")
        
        # 训练控制
        st.subheader("🔄 训练控制")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ 清除对话", use_container_width=True):
                st.session_state.messages = [
                    {"role": "assistant", "content": "🔄 对话已重置！开始新的训练会话。"}
                ]
                st.rerun()
        
        with col2:
            if st.button("⏭️ 下一轮", use_container_width=True):
                st.session_state.training_round += 1
                st.session_state.messages = [
                    {"role": "assistant", "content": f"🎉 进入第{st.session_state.training_round}轮训练！"}
                ]
                st.rerun()

# 主应用
def main():
    # 顶部标题
    st.markdown("""
    <div class="main-header">
        <h2>🧮 14865数字人训练系统</h2>
        <p>Gemini AI · 语音对话 · 按次计费 · 专业训练平台</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 计费提醒
    st.info("""
    💰 **计费说明**: 当前使用Gemini 2.5 Pro模型，按次计费（1000k tokens/次）。请确保API密钥有效且余额充足。
    """)
    
    # 14865框架展示
    st.markdown("""
    <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-around; text-align: center; font-weight: bold;">
            <div>1<br>人性逻辑</div>
            <div>4<br>四大准则</div>
            <div>8<br>质量要求</div>
            <div>6<br>会计要素</div>
            <div>5<br>计量属性</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 布局
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 数字人形象
        current_data = SUBJECTS_DATA[st.session_state.current_subject]
        st.markdown(f"""
        <div class="avatar-container">
            <div style='
                background: linear-gradient(135deg, {current_data["color"]}, #764ba2);
                width: 200px;
                height: 280px;
                border-radius: 15px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: white;
                margin: 0 auto;
                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            '>
                <div style="font-size: 70px; margin-bottom: 10px;">{current_data["emoji"]}</div>
                <div style="font-size: 16px; font-weight: bold;">Gemini AI</div>
                <div style="font-size: 12px; margin-top: 5px;">14865训练系统</div>
            </div>
            <h3>🤖 AI训练师</h3>
            <p><strong>当前学科</strong>: {st.session_state.current_subject}</p>
            <p><strong>AI模型</strong>: {AI_MODELS[st.session_state.selected_model]['name']}</p>
            <p><strong>API状态</strong>: {'🟢 已连接' if st.session_state.api_status == 'connected' else '🔴 未连接'}</p>
            <p><strong>语音状态</strong>: {'🔊 开启' if st.session_state.auto_speech else '🔇 关闭'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 快速问题
        st.subheader("🚀 快速训练")
        pain_points = SUBJECTS_DATA[st.session_state.current_subject]["pain_points"]
        for pain_point in pain_points[:3]:
            if st.button(f"💡 {pain_point}", key=f"quick_{pain_point}", use_container_width=True):
                user_input = f"请详细分析{st.session_state.current_subject}中的{pain_point}问题"
                st.session_state.quick_question = user_input
                st.rerun()
    
    with col2:
        st.subheader("💬 实时对话训练")
        
        # 语音控制按钮
        if st.session_state.auto_speech:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔊 朗读回复", use_container_width=True):
                    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
                        last_response = st.session_state.messages[-1]["content"]
                        tts_html = text_to_speech_html(last_response)
                        st.components.v1.html(tts_html, height=0)
            
            with col2:
                if st.button("⏹️ 停止语音", use_container_width=True):
                    stop_script = """
                    <script>
                        if ('speechSynthesis' in window) {
                            window.speechSynthesis.cancel();
                        }
                    </script>
                    """
                    st.components.v1.html(stop_script, height=0)
        
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
            user_input = st.chat_input(f"请输入关于{st.session_state.current_subject}的问题...")
        
        if user_input:
            # 添加用户消息
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # 获取回复
            with st.spinner("🧠 Gemini AI分析中..."):
                response = call_gemini_api(
                    user_input, 
                    st.session_state.api_key,
                    st.session_state.current_subject,
                    st.session_state.selected_model
                )
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # 语音合成
                if st.session_state.auto_speech:
                    tts_html = text_to_speech_html(response)
                    st.components.v1.html(tts_html, height=0)
            
            st.rerun()
    
    # 侧边栏
    sidebar_config()
    
    # 页脚
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.caption(f"🎯 {st.session_state.current_subject}")
    with col2:
        st.caption(f"🔄 第{st.session_state.training_round}轮")
    with col3:
        st.caption(f"🤖 {AI_MODELS[st.session_state.selected_model]['name']}")
    with col4:
        status_text = {
            "disconnected": "🔴 未连接",
            "testing": "🟡 测试中", 
            "connected": "🟢 已连接",
            "error": "🔴 错误"
        }
        st.caption(status_text[st.session_state.api_status])

if __name__ == "__main__":
    main()
