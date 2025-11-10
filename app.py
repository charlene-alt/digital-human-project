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
        {"role": "assistant", "content": "👋 你好！我是基于'14865'训练体系的智能数字人，请开始在下方输入问题。"}
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
    .stButton button {
        width: 100%;
        border-radius: 10px;
        margin: 2px 0;
    }
    .api-status {
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
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

# 反代API调用函数
def call_proxy_api(user_input, api_key, subject):
    """调用反代API进行智能对话"""
    
    # 如果没有API密钥，使用演示模式
    if not api_key:
        return get_demo_response(user_input, subject)
    
    try:
        # 使用反代网站
        url = "https://api.qiyiguo.uk/v1/chat/completions"
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

【训练要求】
1. 当前学科：{subject}
2. 核心指令必须基于14865体系
3. 回答要深入浅出、通俗易懂、深入思考
4. 形式生动活泼，体现数字人优势
5. 注重跨学科思维融合

请用专业但友好的方式回答用户问题。"""
        
        data = {
            "model": "gpt-3.5-turbo",  # 根据反代服务支持的模型调整
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "stream": False,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            st.error(f"API调用失败: {response.status_code}")
            return get_demo_response(user_input, subject)
            
    except Exception as e:
        st.error(f"请求出错: {str(e)}")
        return get_demo_response(user_input, subject)

# 演示模式回复
def get_demo_response(user_input, subject):
    """演示模式下的智能回复"""
    
    # 14865框架回复模板
    frameworks = {
        "1": "从人性逻辑角度，这个问题涉及未来价值决策...",
        "4": "基于四大准则（可靠性、相关性、可理解性、可比性）分析...",
        "8": "考虑八项质量要求，特别是真实性和完整性的平衡...",
        "6": "从六大要素视角，这个问题与资产管理和费用控制相关...",
        "5": "运用五大计量属性进行价值评估..."
    }
    
    responses = [
        f"""🧠 **基于14865体系的{subject}分析**

📋 **框架应用**：
• 核心指导：4和8（四大准则和八项质量要求）
• 底层逻辑：1（人性逻辑）- 基于未来价值的决策分析

🎯 **专业洞察**：
你的问题「{user_input}」在{subject}领域中，可以从以下角度深入分析：
1. 确保信息的可靠性和相关性（4大准则）
2. 平衡真实性与及时性的要求（8项质量）
3. 考虑长期价值与短期利益的协调（人性逻辑）

💡 **建议**：
建议结合14865体系进行系统性思考，提升专业判断力。""",

        f"""📊 **{subject}专业分析**

🔍 **14865视角**：
• 1-人性逻辑：价值导向决策
• 4-四大准则：建立分析标准
• 6-六大要素：构建分析框架

🎯 **问题解析**：
「{user_input}」这个问题体现了{subject}的核心挑战。通过14865体系，我们可以：

1. 从人性逻辑理解行为动机
2. 用四大准则确保分析质量  
3. 通过六大要素构建完整方案

🚀 **能力提升**：这种分析方式将帮助你超越表面理解，达到专家级洞察力。""",

        f"""💡 **智能训练反馈**

🎯 **训练主题**：{subject}
📚 **应用框架**：14865体系

🔍 **分析路径**：
1️⃣ 人性逻辑 → 理解价值驱动
2️⃣ 四大准则 → 建立质量标准  
3️⃣ 六大要素 → 构建分析框架
4️⃣ 计量属性 → 进行价值评估

📝 **针对你的问题**：「{user_input}」
这是一个很好的{subject}训练案例！通过14865体系的多维度分析，可以培养系统性思维和专业判断力。

💪 **继续努力**：多轮训练将显著提升你的{subject}专业水平！"""
    ]
    
    return random.choice(responses)

# 侧边栏配置
def sidebar_config():
    with st.sidebar:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea, #764ba2); padding: 15px; border-radius: 10px; color: white;'>
            <h3>🎯 训练状态</h3>
            <p>学科: {}</p>
            <p>轮次: 第{}轮</p>
        </div>
        """.format(st.session_state.current_subject, st.session_state.training_round), unsafe_allow_html=True)
        
        # API设置
        st.markdown("---")
        st.subheader("🔑 API设置")
        
        api_key = st.text_input(
            "API密钥",
            type="password",
            value=st.session_state.api_key,
            placeholder="输入反代API密钥（可选）",
            help="如果没有密钥，系统将使用演示模式"
        )
        st.session_state.api_key = api_key
        
        # API状态显示
        if api_key:
            st.success("✅ API已配置 - 使用反代服务")
        else:
            st.info("ℹ️ 演示模式 - 功能完整")
        
        st.info("""
        **反代API信息**：
        - 端点：https://api.qiyiguo.uk/v1
        - 支持模型：GPT系列
        - 需要有效的API密钥
        """)
        
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
                    {"role": "assistant", "content": f"🎉 进入第{st.session_state.training_round}轮训练！继续深化{st.session_state.current_subject}学习。"}
                ]
                st.rerun()
        
        # 快速问题模板
        st.markdown("---")
        st.subheader("🚀 快速开始")
        current_data = SUBJECTS_DATA[st.session_state.current_subject]
        for pain_point in current_data["pain_points"][:3]:
            if st.button(f"💡 {pain_point}", key=f"quick_{pain_point}", use_container_width=True):
                user_input = f"请详细分析{st.session_state.current_subject}中的{pain_point}问题，基于14865体系给出专业解决方案"
                st.session_state.quick_question = user_input
                st.rerun()

# 主应用
def main():
    # 顶部标题
    st.markdown("""
    <div class="main-header">
        <h2>🧮 14865数字人训练系统</h2>
        <p>基于反代API · 跨学科专业训练 · 能力提升平台</p>
    </div>
    """, unsafe_allow_html=True)
    
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
                <div style="font-size: 16px; font-weight: bold;">14865</div>
                <div style="font-size: 12px; margin-top: 5px;">训练系统</div>
            </div>
            <h3>🤖 AI训练师</h3>
            <p><strong>当前学科</strong>: {st.session_state.current_subject}</p>
            <p><strong>训练轮次</strong>: 第{st.session_state.training_round}轮</p>
            <p><strong>API状态</strong>: {'✅ 已连接' if st.session_state.api_key else '🟡 演示模式'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("💬 专业训练对话")
        
        # 显示对话历史
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
            with st.spinner("🧠 14865体系分析中..."):
                response = call_proxy_api(
                    user_input, 
                    st.session_state.api_key,
                    st.session_state.current_subject
                )
                
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
    
    # 侧边栏
    sidebar_config()
    
    # 页脚
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"🎯 {st.session_state.current_subject}")
    with col2:
        st.caption(f"🔄 第{st.session_state.training_round}轮")
    with col3:
        st.caption("🌐 反代API服务")

if __name__ == "__main__":
    main()
