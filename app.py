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
        {"role": "assistant", "content": "👋 你好！我是基于'14865'训练体系的智能数字人，专注于通过跨学科训练提升会计专业能力。请选择你的训练主题！"}
    ]
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "is_speaking" not in st.session_state:
    st.session_state.is_speaking = False
if "auto_speech" not in st.session_state:
    st.session_state.auto_speech = True
if "current_subject" not in st.session_state:
    st.session_state.current_subject = "会计学"
if "training_round" not in st.session_state:
    st.session_state.training_round = 1
if "avatar_style" not in st.session_state:
    st.session_state.avatar_style = "professional"

# 自定义CSS样式
st.markdown("""
<style>
    /* 主容器样式 */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 25px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* 训练状态指示器 */
    .training-status {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        padding: 15px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
        text-align: center;
    }
    
    /* 数字人容器 */
    .avatar-container {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        text-align: center;
        border: 3px solid #4CAF50;
        margin-bottom: 20px;
    }
    
    /* 说话动画 */
    .speaking {
        animation: pulse 1.5s ease-in-out infinite;
        border-color: #FF6B6B !important;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.7); }
        50% { transform: scale(1.02); box-shadow: 0 0 0 10px rgba(255, 107, 107, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 107, 107, 0); }
    }
    
    /* 消息样式 */
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        max-width: 80%;
        margin-right: auto;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
    }
    
    /* 按钮样式 */
    .stButton button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* 侧边栏样式 */
    .sidebar-content {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    
    /* 会计思维标签 */
    .accounting-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 5px 12px;
        border-radius: 20px;
        margin: 2px;
        font-size: 12px;
        font-weight: bold;
    }
    
    /* 数字人形象样式 */
    .avatar-professional {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    .avatar-creative {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    }
    
    .avatar-technical {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%) !important;
    }
    
    .avatar-academic {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

# 学科数据库
SUBJECTS_DATA = {
    "会计学": {
        "pain_points": ["准则理解", "报表分析", "成本控制", "税务筹划"],
        "keywords": ["会计准则", "财务报表", "内部控制", "审计", "税务"],
        "avatar_emoji": "📊"
    },
    "税法": {
        "pain_points": ["政策更新", "税务筹划", "合规风险", "跨境税务"],
        "keywords": ["增值税", "企业所得税", "税收优惠", "税务稽查", "国际税收"],
        "avatar_emoji": "⚖️"
    },
    "近现代史纲要": {
        "pain_points": ["历史脉络", "事件关联", "理论理解", "现实意义"],
        "keywords": ["革命历程", "社会主义建设", "改革开放", "历史经验"],
        "avatar_emoji": "📜"
    },
    "形势与政策": {
        "pain_points": ["政策解读", "国际形势", "发展趋势", "影响分析"],
        "keywords": ["国际关系", "经济政策", "社会发展", "国家安全"],
        "avatar_emoji": "🌍"
    },
    "金融学": {
        "pain_points": ["风险管理", "投资决策", "市场分析", "金融创新"],
        "keywords": ["资本市场", "风险管理", "投资银行", "金融科技"],
        "avatar_emoji": "💹"
    }
}

# 14865训练体系核心逻辑
def get_14865_framework(subject, user_input):
    """根据14865体系生成专业回复"""
    
    framework = {
        "1": {
            "name": "人性逻辑",
            "description": "基于未来价值决策的底层逻辑",
            "application": "分析行为动机和价值判断"
        },
        "4": {
            "name": "四大准则", 
            "description": "可靠性、相关性、可理解性、可比性",
            "application": "建立分析的基本标准"
        },
        "8": {
            "name": "八项质量要求",
            "description": "真实性、完整性、及时性、明晰性、实质性、谨慎性、重要性、权责发生制",
            "application": "确保输出质量的核心要求"
        },
        "6": {
            "name": "六大要素",
            "description": "资产、负债、权益、收入、费用、利润",
            "application": "构建分析框架的基本元素"
        },
        "5": {
            "name": "五大计量属性",
            "description": "历史成本、重置成本、可变现净值、现值、公允价值", 
            "application": "价值评估和决策依据"
        }
    }
    
    # 根据学科特点调整框架应用
    if subject == "会计学":
        core_elements = "6和5"  # 六大要素和五大计量属性为核心
    elif subject == "税法":
        core_elements = "4和8"  # 准则和质量要求为核心
    else:
        core_elements = "1和4"  # 人性逻辑和准则为核心
    
    response = f"""
🧠 **基于14865训练体系的{subject}分析**

📋 **框架应用**：
• **核心指导**：{core_elements} ({framework[core_elements[0]]['name']}和{framework[core_elements[1]]['name']})
• **底层逻辑**：1 ({framework['1']['name']}) - {framework['1']['application']}

🎯 **学科痛点解决**：
{random.choice(SUBJECTS_DATA[subject]['pain_points'])} → 通过{core_elements}提供具体解决方案

💡 **专业洞察**：
基于14865体系，你的问题「{user_input}」可以从以下角度深入分析：
1. {framework[core_elements[0]]['application']}
2. {framework[core_elements[1]]['application']} 
3. {framework['1']['application']}

🚀 **能力提升**：本次训练将强化你在{subject}领域的专业判断力和AI应用能力。
"""
    
    return response

# DeepSeek API调用函数
def call_deepseek_api(user_input, subject, api_key=None):
    """调用DeepSeek API进行智能对话"""
    try:
        if not api_key:
            # 使用14865训练体系生成回复
            return get_14865_framework(subject, user_input)
        
        # 真实API调用
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # 14865训练体系系统提示词
        system_prompt = f'''你是专业数字人训练助手，严格遵循14865训练体系：

【14865训练体系】
1 - 人性逻辑：基于未来价值的底层决策逻辑
4 - 四大准则：可靠性、相关性、可理解性、可比性  
8 - 八项质量要求：真实性、完整性、及时性、明晰性、实质性、谨慎性、重要性、权责发生制
6 - 六大要素：资产、负债、权益、收入、费用、利润
5 - 五大计量属性：历史成本、重置成本、可变现净值、现值、公允价值

【训练要求】
1. 当前学科：{subject}，学科痛点：{", ".join(SUBJECTS_DATA[subject]['pain_points'])}
2. 核心指令必须基于14865体系，错字零容忍
3. 回答要深入浅出、通俗易懂、深入思考
4. 形式生动活泼，体现数字人优势
5. 注重跨学科思维融合

【汇报目标】
通过多轮训练，让学生对{subject}问题的理解超越普通同学甚至一般专家，打造强大的AI应用能力。'''
        
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
            return get_14865_framework(subject, user_input)
            
    except Exception as e:
        return get_14865_framework(subject, user_input)

# 语音合成功能
def text_to_speech_html(text, rate=1.0, pitch=1.0):
    """生成语音合成的HTML代码"""
    simple_text = text[:100].replace('"', '').replace("'", "").replace("`", "")
    
    return f'''
    <script>
        function speakText() {{
            if ('speechSynthesis' in window) {{
                const utterance = new SpeechSynthesisUtterance();
                utterance.text = "{simple_text}";
                utterance.lang = 'zh-CN';
                utterance.rate = {rate};
                utterance.pitch = {pitch};
                
                utterance.onstart = function() {{
                    console.log('开始说话');
                }};
                
                utterance.onend = function() {{
                    console.log('结束说话');
                }};
                
                window.speechSynthesis.speak(utterance);
            }}
        }}
        setTimeout(speakText, 1000);
    </script>
    '''

# 数字人形象显示函数 - 方案三：CSS创建动态形象
def show_digital_human():
    with st.container():
        st.markdown('<div class="avatar-container">', unsafe_allow_html=True)
        
        st.subheader("🤖 14865训练数字人")
        
        # 获取当前学科的emoji
        current_emoji = SUBJECTS_DATA[st.session_state.current_subject]["avatar_emoji"]
        
        # 根据风格选择CSS类
        style_class = f"avatar-{st.session_state.avatar_style}"
        
        # 创建动态数字人形象
        avatar_html = f"""
        <div style="text-align: center;">
            <div id="digitalHuman" class="{style_class}" style="
                width: 220px; 
                height: 320px; 
                border-radius: 20px;
                margin: 0 auto;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: white;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                border: 3px solid #4CAF50;
                position: relative;
                overflow: hidden;
            ">
                <div style="font-size: 80px; margin-bottom: 15px;">{current_emoji}</div>
                <div style="font-size: 16px; font-weight: bold; text-align: center; margin-bottom: 10px;">
                    14865训练系统
                </div>
                <div style="font-size: 12px; text-align: center; opacity: 0.9;">
                    {st.session_state.current_subject}
                </div>
                <div style="
                    position: absolute;
                    bottom: 10px;
                    font-size: 11px;
                    opacity: 0.7;
                ">
                    第{st.session_state.training_round}轮训练
                </div>
            </div>
        </div>
        """
        
        speaking_class = "speaking" if st.session_state.is_speaking else ""
        st.markdown(f'<div class="{speaking_class}">{avatar_html}</div>', unsafe_allow_html=True)
        
        # 形象控制按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 更新形象", use_container_width=True):
                styles = ["professional", "creative", "technical", "academic"]
                current_index = styles.index(st.session_state.avatar_style)
                new_index = (current_index + 1) % len(styles)
                st.session_state.avatar_style = styles[new_index]
                st.success(f"已切换到{styles[new_index]}风格！")
                st.rerun()
        
        with col2:
            if st.button("🎯 训练状态", use_container_width=True):
                st.info(f"当前训练轮次: {st.session_state.training_round}\n当前学科: {st.session_state.current_subject}")
        
        # 状态显示
        if st.session_state.is_speaking:
            st.success("🔊 数字人正在汇报中...")
        else:
            st.info("🎯 等待训练指令 - 准备就绪")
            
        st.markdown('</div>', unsafe_allow_html=True)

# 侧边栏配置
def sidebar_config():
    with st.sidebar:
        st.markdown('<div class="training-status">', unsafe_allow_html=True)
        st.header(f"🎯 训练轮次: 第{st.session_state.training_round}轮")
        st.write(f"当前学科: {st.session_state.current_subject}")
        st.write(f"形象风格: {st.session_state.avatar_style}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 学科选择
        st.subheader("📚 学科选择")
        st.write("点击切换训练学科：")
        
        for subject, data in SUBJECTS_DATA.items():
            emoji = data["avatar_emoji"]
            is_active = "✅" if subject == st.session_state.current_subject else "⚪"
            if st.button(f"{is_active} {emoji} {subject}", key=f"subject_{subject}", use_container_width=True):
                st.session_state.current_subject = subject
                st.session_state.messages = [
                    {"role": "assistant", "content": f"🔁 已切换到{subject}训练模式！请提出关于{subject}的问题，我将基于14865体系进行专业分析。"}
                ]
                st.rerun()
        
        st.markdown("---")
        
        # API密钥设置
        st.subheader("🔑 API设置")
        api_key = st.text_input(
            "DeepSeek API密钥",
            type="password",
            help="输入密钥启用真实AI对话，留空使用演示模式",
            value=st.session_state.get("api_key", "")
        )
        st.session_state.api_key = api_key
        
        if api_key:
            st.success("✅ API已配置 - 真实AI对话")
        else:
            st.warning("⚠️ 演示模式运行中")
        
        st.markdown("---")
        
        # 语音设置
        st.subheader("🎵 语音设置")
        auto_speech = st.checkbox("自动语音回复", value=st.session_state.auto_speech)
        st.session_state.auto_speech = auto_speech
        
        if auto_speech:
            st.success("🔊 语音功能已开启")
        else:
            st.info("🔇 语音功能已关闭")
        
        # 测试语音按钮
        if st.button("🎤 测试语音功能", use_container_width=True):
            test_script = text_to_speech_html("数字人语音系统测试成功！欢迎使用14865训练系统。")
            st.components.v1.html(test_script, height=0)
            st.success("语音测试完成！")
        
        st.markdown("---")
        
        # 训练控制
        st.subheader("🔄 训练控制")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏭️ 下一轮", use_container_width=True):
                st.session_state.training_round += 1
                st.session_state.messages = [
                    {"role": "assistant", "content": f"🎉 进入第{st.session_state.training_round}轮训练！继续基于14865体系深化{st.session_state.current_subject}学习。"}
                ]
                st.rerun()
        
        with col2:
            if st.button("🔄 重置", use_container_width=True):
                st.session_state.messages = [
                    {"role": "assistant", "content": "🔄 对话已重置！请继续基于14865体系进行专业训练。"}
                ]
                st.rerun()
        
        # 训练统计
        st.markdown("---")
        st.subheader("📈 训练统计")
        st.write(f"• 训练轮次: {st.session_state.training_round}")
        st.write(f"• 对话消息: {len(st.session_state.messages)}")
        st.write(f"• 当前学科: {st.session_state.current_subject}")
        st.write(f"• 系统状态: ✅ 运行正常")

# 主应用
def main():
    # 顶部标题
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0;">🧮 14865数字人训练系统</h1>
        <p style="margin: 0; opacity: 0.9;">通过严谨的AI训练 + 跨学科实践 · 提升专业能力</p>
        <p style="margin: 10px 0 0 0; font-size: 14px; opacity: 0.8;">
            深入浅出 · 通俗易懂 · 深入思考 · 生动活泼
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 14865框架展示
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px;">
        <h4 style="margin: 0; text-align: center;">🎯 14865训练框架</h4>
        <div style="display: flex; justify-content: space-between; margin-top: 15px; text-align: center;">
            <div><strong>1</strong><br>人性逻辑</div>
            <div><strong>4</strong><br>四大准则</div>
            <div><strong>8</strong><br>质量要求</div>
            <div><strong>6</strong><br>会计要素</div>
            <div><strong>5</strong><br>计量属性</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 布局
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 显示数字人形象
        show_digital_human()
        
        # 快速训练主题
        st.subheader("🚀 快速训练")
        current_subject = st.session_state.current_subject
        pain_points = SUBJECTS_DATA[current_subject]['pain_points']
        
        st.write("点击快速开始训练：")
        for i, pain_point in enumerate(pain_points[:4]):
            if st.button(f"💡 {pain_point}", key=f"quick_{i}", use_container_width=True):
                user_input = f"请分析{current_subject}中的{pain_point}问题，基于14865体系给出专业解决方案"
                st.session_state.quick_question = user_input
                st.rerun()
    
    with col2:
        st.subheader("💬 专业训练对话")
        
        # 显示对话历史
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
        
        # 处理快速提问
        if "quick_question" in st.session_state:
            user_input = st.session_state.quick_question
            del st.session_state.quick_question
        else:
            user_input = st.chat_input(f"请输入关于{st.session_state.current_subject}的问题...")
        
        # 处理用户输入
        if user_input:
            # 添加用户消息
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # 获取AI回复
            with st.spinner(f"🔍 14865体系分析中..."):
                st.session_state.is_speaking = True
                
                # 调用API
                response = call_deepseek_api(
                    user_input, 
                    st.session_state.current_subject, 
                    st.session_state.api_key
                )
                
                # 添加助手回复
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # 语音合成
                if st.session_state.auto_speech:
                    tts_html = text_to_speech_html(response)
                    st.components.v1.html(tts_html, height=0)
                    time.sleep(len(response) * 0.03)
                
                st.session_state.is_speaking = False
            
            st.rerun()
    
    # 侧边栏
    sidebar_config()
    
    # 页脚信息
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"🎯 当前学科: {st.session_state.current_subject}")
    with col2:
        st.caption(f"🔄 训练轮次: {st.session_state.training_round}")
    with col3:
        st.caption("🧠 14865训练体系")

if __name__ == "__main__":
    main()
