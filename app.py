import streamlit as st
import requests
import json
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
        {"role": "assistant", "content": "👋 你好！我是基于14865训练体系的智能数字人，请选择运行模式开始对话。"}
    ]
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "current_subject" not in st.session_state:
    st.session_state.current_subject = "会计学"
if "training_round" not in st.session_state:
    st.session_state.training_round = 1
if "auto_speech" not in st.session_state:
    st.session_state.auto_speech = False
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "demo"
if "api_status" not in st.session_state:
    st.session_state.api_status = "disconnected"
if "api_base_url" not in st.session_state:
    st.session_state.api_base_url = "https://api.qiyiguo.uk/v1"

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .status-connected { 
        background: #4CAF50; 
        color: white; 
        padding: 8px 16px; 
        border-radius: 20px; 
        font-weight: bold; 
        text-align: center;
        display: inline-block;
        margin: 5px;
    }
    .status-disconnected { 
        background: #ff9800; 
        color: white; 
        padding: 8px 16px; 
        border-radius: 20px; 
        font-weight: bold; 
        text-align: center;
        display: inline-block;
        margin: 5px;
    }
    .status-testing { 
        background: #2196F3; 
        color: white; 
        padding: 8px 16px; 
        border-radius: 20px; 
        font-weight: bold; 
        text-align: center;
        display: inline-block;
        margin: 5px;
    }
    .status-error { 
        background: #f44336; 
        color: white; 
        padding: 8px 16px; 
        border-radius: 20px; 
        font-weight: bold; 
        text-align: center;
        display: inline-block;
        margin: 5px;
    }
    .model-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .user-message {
        background: #e3f2fd;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        border: 1px solid #bbdefb;
    }
    .assistant-message {
        background: #f5f5f5;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-right: auto;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# 学科数据
SUBJECTS_DATA = {
    "会计学": {
        "emoji": "📊", 
        "pain_points": ["准则理解", "报表分析", "成本控制", "税务筹划"],
        "color": "#667eea",
        "description": "会计理论与实务应用"
    },
    "税法": {
        "emoji": "⚖️", 
        "pain_points": ["政策更新", "税务筹划", "合规风险", "跨境税务"],
        "color": "#f093fb",
        "description": "税收法律法规解析"
    },
    "金融学": {
        "emoji": "💹", 
        "pain_points": ["风险管理", "投资决策", "市场分析", "金融创新"],
        "color": "#4ECDC4",
        "description": "金融市场与投资管理"
    }
}

# AI模型配置 - 修正API端点
AI_MODELS = {
    "demo": {
        "name": "🧪 演示模式",
        "description": "本地智能回复，无需API",
        "type": "demo"
    },
    "gpt-3.5-turbo": {
        "name": "🤖 GPT-3.5 Turbo",
        "description": "快速响应，成本较低",
        "type": "openai",
        "endpoint": "/chat/completions"
    },
    "gpt-4": {
        "name": "🧠 GPT-4",
        "description": "更强的推理能力",
        "type": "openai", 
        "endpoint": "/chat/completions"
    },
    "gpt-4-turbo": {
        "name": "⚡ GPT-4 Turbo",
        "description": "平衡性能与速度",
        "type": "openai",
        "endpoint": "/chat/completions"
    }
}

# 修正的API调用函数
def call_chat_api(messages, api_key, model_name, base_url):
    """修正的API调用函数，使用正确的端点"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        model_config = AI_MODELS.get(model_name, AI_MODELS["gpt-3.5-turbo"])
        
        # 统一使用OpenAI兼容格式
        url = f"{base_url}/chat/completions"
        
        # 构建系统提示词
        system_message = None
        user_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)
        
        # 构建最终消息列表
        final_messages = []
        if system_message:
            final_messages.append({"role": "system", "content": system_message})
        final_messages.extend(user_messages)
        
        data = {
            "model": model_name,
            "messages": final_messages,
            "stream": False,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            error_msg = f"API错误 {response.status_code}"
            try:
                error_detail = response.json()
                if "error" in error_detail:
                    error_msg = f"API错误: {error_detail['error'].get('message', str(error_detail))}"
            except:
                error_msg = f"API错误 {response.status_code}: {response.text}"
            return error_msg
            
    except requests.exceptions.Timeout:
        return "请求超时，请检查网络连接或稍后重试"
    except requests.exceptions.ConnectionError:
        return "网络连接错误，请检查网络设置"
    except Exception as e:
        return f"请求失败: {str(e)}"

# 测试API连接 - 简化版本
def test_api_connection(api_key, model_name, base_url):
    """测试API连接状态"""
    if not api_key:
        return False, "请输入API密钥"
    
    try:
        # 使用简单的测试消息
        test_messages = [
            {"role": "user", "content": "请简单回复'测试成功'三个字"}
        ]
        
        response = call_chat_api(test_messages, api_key, model_name, base_url)
        
        if "测试成功" in response:
            return True, "✅ API连接测试成功"
        elif "API错误" in response or "请求失败" in response:
            return False, response
        else:
            # 只要没有错误信息就认为连接成功
            return True, f"✅ API连接正常 - 模型响应: {response[:50]}..."
            
    except Exception as e:
        return False, f"连接测试失败: {str(e)}"

# 获取可用模型列表
def get_available_models(api_key, base_url):
    """获取API支持的模型列表"""
    if not api_key:
        return []
    
    try:
        url = f"{base_url}/models"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            models_data = response.json()
            available_models = []
            if "data" in models_data:
                for model in models_data["data"]:
                    available_models.append(model["id"])
            return available_models
        return []
    except:
        return []

# 演示模式回复
def get_demo_response(user_input, subject):
    """演示模式智能回复"""
    templates = [
        f"""🧠 **基于14865体系的{subject}分析**

📋 **框架应用**：
• 核心指导：4和8（四大准则和八项质量要求）
• 底层逻辑：1（人性逻辑）- 基于未来价值的决策分析

🎯 **专业洞察**：
您的提问「{user_input}」在{subject}领域中具有重要意义。通过14865体系的多维度分析，可以得出系统性的专业见解。

💡 **建议**：切换到API模式可获得更精准的AI分析。""",

        f"""📊 **{subject}专业视角**

🔍 **14865分析框架**：
• 1-人性逻辑：理解价值驱动因素
• 4-四大准则：建立专业标准
• 6-六大要素：构建完整分析

💎 **核心价值**：
这个问题体现了{subject}专业实践的关键挑战，通过14865体系的系统性思考，能够提升专业判断力。"""
    ]
    return random.choice(templates)

# 语音功能
def text_to_speech(text):
    """文本转语音"""
    clean_text = text[:150].replace('"', '').replace("'", "").replace("\n", " ")
    return f'''
    <script>
        function speakText() {{
            if ('speechSynthesis' in window) {{
                const utterance = new SpeechSynthesisUtterance();
                utterance.text = "{clean_text}";
                utterance.lang = 'zh-CN';
                utterance.rate = 1.0;
                utterance.volume = 0.8;
                window.speechSynthesis.speak(utterance);
            }}
        }}
        setTimeout(speakText, 500);
    </script>
    '''

# 侧边栏配置
def sidebar_config():
    with st.sidebar:
        # 训练状态面板
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea, #764ba2); padding: 20px; border-radius: 12px; color: white;'>
            <h3 style='margin:0;'>🎯 训练状态</h3>
            <p style='margin:8px 0;'>📚 {st.session_state.current_subject}</p>
            <p style='margin:8px 0;'>🔄 第{st.session_state.training_round}轮</p>
            <p style='margin:8px 0;'>🤖 {AI_MODELS[st.session_state.selected_model]['name']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # API基础设置
        st.subheader("🌐 API设置")
        
        api_base_url = st.text_input(
            "API基础地址",
            value=st.session_state.api_base_url,
            placeholder="https://api.qiyiguo.uk/v1",
            help="API服务的基础URL地址"
        )
        st.session_state.api_base_url = api_base_url
        
        api_key = st.text_input(
            "API密钥",
            type="password",
            value=st.session_state.api_key,
            placeholder="输入您的API密钥",
            help="从API服务商获取"
        )
        
        st.markdown("---")
        
        # 模型选择
        st.subheader("🤖 AI模型")
        
        # 显示可用的模型
        for model_id, model_info in AI_MODELS.items():
            if model_id == "demo":
                continue  # 演示模式单独处理
                
            st.markdown(f"""
            <div class="model-card">
                <strong>{model_info['name']}</strong>
                <br><small>{model_info['description']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(
                f"选择 {model_info['name']}",
                key=f"model_{model_id}",
                use_container_width=True,
                type="primary" if model_id == st.session_state.selected_model else "secondary"
            ):
                st.session_state.selected_model = model_id
                st.session_state.api_key = api_key
                st.success(f"已切换到 {model_info['name']}")
        
        # 演示模式按钮
        st.markdown("---")
        if st.button(
            "🧪 切换到演示模式",
            key="model_demo",
            use_container_width=True,
            type="primary" if st.session_state.selected_model == "demo" else "secondary"
        ):
            st.session_state.selected_model = "demo"
            st.session_state.api_status = "connected"
            st.success("已切换到演示模式")
        
        st.markdown("---")
        
        # 连接状态和测试
        st.subheader("🔗 连接状态")
        
        status_html = {
            "disconnected": '<div class="status-disconnected">🔴 未连接</div>',
            "testing": '<div class="status-testing">🟡 测试中</div>',
            "connected": '<div class="status-connected">🟢 已连接</div>',
            "error": '<div class="status-error">🔴 连接错误</div>'
        }
        st.markdown(status_html[st.session_state.api_status], unsafe_allow_html=True)
        
        if st.session_state.selected_model != "demo":
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🧪 测试连接", use_container_width=True):
                    if api_key:
                        st.session_state.api_status = "testing"
                        st.session_state.api_key = api_key
                        
                        with st.spinner("测试API连接中..."):
                            success, message = test_api_connection(api_key, st.session_state.selected_model, api_base_url)
                        
                        if success:
                            st.session_state.api_status = "connected"
                            st.success(message)
                        else:
                            st.session_state.api_status = "error"
                            st.error(message)
                    else:
                        st.warning("请输入API密钥")
            
            with col2:
                if st.button("🔄 刷新模型", use_container_width=True):
                    if api_key:
                        with st.spinner("获取模型列表中..."):
                            available_models = get_available_models(api_key, api_base_url)
                        if available_models:
                            st.success(f"发现 {len(available_models)} 个可用模型")
                            st.write("可用模型:", ", ".join(available_models[:5]))
                        else:
                            st.info("无法获取模型列表，请检查API密钥")
        
        st.markdown("---")
        
        # 语音设置
        st.subheader("🎵 语音设置")
        auto_speech = st.checkbox("启用语音回复", value=st.session_state.auto_speech)
        st.session_state.auto_speech = auto_speech
        
        if auto_speech:
            st.success("🔊 语音功能已开启")
        else:
            st.info("🔇 语音功能已关闭")
        
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
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ 清除对话", use_container_width=True):
                st.session_state.messages = [
                    {"role": "assistant", "content": "🔄 对话已重置！开始新的训练。"}
                ]
                st.rerun()
        
        with col2:
            if st.button("⏭️ 下一轮", use_container_width=True):
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
        <h1 style="margin:0;">🧮 14865数字人训练系统</h1>
        <p style="margin:10px 0 0 0; opacity:0.9;">修正API端点 · 稳定连接 · 专业训练</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 模式状态提示
    current_model = AI_MODELS[st.session_state.selected_model]
    if st.session_state.selected_model == "demo":
        st.success(f"🎉 当前模式: {current_model['name']} - 快速响应，无需配置")
    else:
        if st.session_state.api_status == "connected":
            st.success(f"🌐 当前模型: {current_model['name']} - API已连接")
        else:
            st.warning(f"⚠️ 当前模型: {current_model['name']} - 请测试API连接")
    
    # 14865框架展示
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 12px; color: white; margin-bottom: 20px;">
        <h4 style="margin:0; text-align:center;">🎯 14865训练框架</h4>
        <div style="display: flex; justify-content: space-around; margin-top: 15px; text-align: center; font-weight: bold;">
            <div>1<br><small>人性逻辑</small></div>
            <div>4<br><small>四大准则</small></div>
            <div>8<br><small>质量要求</small></div>
            <div>6<br><small>会计要素</small></div>
            <div>5<br><small>计量属性</small></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # API使用说明
    with st.expander("📖 API使用说明"):
        st.write("""
        **正确的API端点配置**：
        - 基础地址：`https://api.qiyiguo.uk/v1`
        - 聊天端点：`/chat/completions` 
        - 模型端点：`/models`
        
        **支持的模型**：
        - GPT-3.5 Turbo
        - GPT-4
        - GPT-4 Turbo
        
        **常见问题**：
        - 404错误：检查API端点是否正确
        - 401错误：检查API密钥是否正确
        - 超时错误：检查网络连接
        """)
    
    # 布局
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 数字人形象
        current_data = SUBJECTS_DATA[st.session_state.current_subject]
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: white; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px;'>
            <div style='
                background: linear-gradient(135deg, {current_data["color"]}, #764ba2);
                width: 200px; height: 280px; border-radius: 15px;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                color: white; margin: 0 auto;
            '>
                <div style="font-size: 70px; margin-bottom: 15px;">{current_data["emoji"]}</div>
                <div style="font-size: 18px; font-weight: bold;">AI导师</div>
                <div style="font-size: 12px; margin-top: 8px;">14865系统</div>
            </div>
            <h3 style="margin:15px 0 10px 0;">🤖 智能训练师</h3>
            <p><strong>当前学科</strong>: {st.session_state.current_subject}</p>
            <p><strong>AI模型</strong>: {current_model['name']}</p>
            <p><strong>连接状态</strong>: {st.session_state.api_status}</p>
            <p><strong>语音功能</strong>: {'🔊 开启' if st.session_state.auto_speech else '🔇 关闭'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 快速训练
        st.subheader("🚀 快速训练")
        pain_points = SUBJECTS_DATA[st.session_state.current_subject]["pain_points"]
        for i, pain_point in enumerate(pain_points):
            if st.button(f"💡 {pain_point}", key=f"quick_{i}", use_container_width=True):
                user_input = f"请详细分析{st.session_state.current_subject}中的{pain_point}问题"
                st.session_state.quick_question = user_input
                st.rerun()
    
    with col2:
        st.subheader("💬 智能对话训练")
        
        # 语音控制
        if st.session_state.auto_speech:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔊 朗读回复", use_container_width=True):
                    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
                        last_response = st.session_state.messages[-1]["content"]
                        st.components.v1.html(text_to_speech(last_response), height=0)
            
            with col2:
                if st.button("⏹️ 停止语音", use_container_width=True):
                    st.components.v1.html("""
                    <script>
                        if ('speechSynthesis' in window) {
                            window.speechSynthesis.cancel();
                        }
                    </script>
                    """, height=0)
        
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
            
            # 构建消息历史（只保留最近的10条消息避免过长）
            recent_messages = st.session_state.messages[-10:] if len(st.session_state.messages) > 10 else st.session_state.messages.copy()
            
            # 添加系统提示词
            system_prompt = f"""你是{st.session_state.current_subject}专家，严格遵循14865训练体系。请用专业但易懂的方式回答用户问题。"""
            
            messages_with_system = [{"role": "system", "content": system_prompt}] + recent_messages
            
            # 获取回复
            if st.session_state.selected_model == "demo":
                # 演示模式
                response = get_demo_response(user_input, st.session_state.current_subject)
            else:
                # API模式
                with st.spinner(f"🤖 {current_model['name']} 思考中..."):
                    response = call_chat_api(
                        messages_with_system,
                        st.session_state.api_key,
                        st.session_state.selected_model,
                        st.session_state.api_base_url
                    )
            
            # 添加助手回复
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # 语音合成
            if st.session_state.auto_speech:
                st.components.v1.html(text_to_speech(response), height=0)
            
            st.rerun()
    
    # 侧边栏
    sidebar_config()
    
    # 页脚
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.caption(f"📚 {st.session_state.current_subject}")
    with col2:
        st.caption(f"🔄 第{st.session_state.training_round}轮")
    with col3:
        st.caption(f"🤖 {current_model['name']}")
    with col4:
        st.caption(f"🔗 {st.session_state.api_status}")

if __name__ == "__main__":
    main()
