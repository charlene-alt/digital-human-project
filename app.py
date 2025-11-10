import streamlit as st
import requests
import json
import time
import random

# 页面配置
st.set_page_config(
    page_title="会计数字人训练系统",
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
    
    /* 学科标签 */
    .subject-tag {
        display: inline-block;
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        margin: 5px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .subject-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
    }
    
    .subject-tag.active {
        background: linear-gradient(135deg, #4CAF50, #45a049);
    }
    
    /* 汇报要求标签 */
    .requirement-badge {
        display: inline-block;
        background: rgba(102, 126, 234, 0.1);
        border: 2px solid #667eea;
        padding: 5px 12px;
        border-radius: 15px;
        margin: 2px;
        font-size: 12px;
        font-weight: bold;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# 学科数据库
SUBJECTS_DATA = {
    "会计学": {
        "pain_points": ["准则理解", "报表分析", "成本控制", "税务筹划"],
        "keywords": ["会计准则", "财务报表", "内部控制", "审计", "税务"]
    },
    "税法": {
        "pain_points": ["政策更新", "税务筹划", "合规风险", "跨境税务"],
        "keywords": ["增值税", "企业所得税", "税收优惠", "税务稽查", "国际税收"]
    },
    "近现代史纲要": {
        "pain_points": ["历史脉络", "事件关联", "理论理解", "现实意义"],
        "keywords": ["革命历程", "社会主义建设", "改革开放", "历史经验"]
    },
    "形势与政策": {
        "pain_points": ["政策解读", "国际形势", "发展趋势", "影响分析"],
        "keywords": ["国际关系", "经济政策", "社会发展", "国家安全"]
    },
    "金融学": {
        "pain_points": ["风险管理", "投资决策", "市场分析", "金融创新"],
        "keywords": ["资本市场", "风险管理", "投资银行", "金融科技"]
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

# 侧边栏配置
def sidebar_config():
    with st.sidebar:
        st.markdown('<div class="training-status">', unsafe_allow_html=True)
        st.header(f"🎯 训练轮次: 第{st.session_state.training_round}轮")
        st.write(f"当前学科: {st.session_state.current_subject}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 学科选择
        st.subheader("📚 学科选择")
        for subject in SUBJECTS_DATA.keys():
            is_active = "active" if subject == st.session_state.current_subject else ""
            if st.button(f"🎓 {subject}", key=f"subject_{subject}", use_container_width=True):
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
        
        st.markdown("---")
        
        # 语音设置
        st.subheader("🎵 语音设置")
        auto_speech = st.checkbox("自动语音回复", value=st.session_state.auto_speech)
        st.session_state.auto_speech = auto_speech
        
        # 训练控制
        st.subheader("🔄 训练控制")
        if st.button("🔄 下一训练轮次", use_container_width=True):
            st.session_state.training_round += 1
            st.session_state.messages = [
                {"role": "assistant", "content": f"🎉 进入第{st.session_state.training_round}轮训练！继续基于14865体系深化{st.session_state.current_subject}学习。"}
            ]
            st.rerun()
        
        if st.button("🗑️ 重置对话", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "🔄 对话已重置！请继续基于14865体系进行专业训练。"}
            ]
            st.rerun()

# 主应用
def main():
    # 顶部标题
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0;">🧮 14865数字人训练系统</h1>
        <p style="margin: 0; opacity: 0.9;">通过严谨的AI训练 + 跨学科实践 · 提升专业能力</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 汇报要求展示
    st.markdown("""
    <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h4 style="margin: 0; color: #333;">🎯 汇报核心要求</h4>
        <div style="margin-top: 10px;">
            <span class="requirement-badge">深入浅出</span>
            <span class="requirement-badge">通俗易懂</span>
            <span class="requirement-badge">深入思考</span>
            <span class="requirement-badge">生动活泼</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 布局
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 数字人形象
        st.markdown('<div class="avatar-container">', unsafe_allow_html=True)
        st.subheader("🤖 训练数字人")
        
        avatar_url = "https://models.readyplayer.me/691177a7de516bcc961ee065.glb"
        speaking_class = "speaking" if st.session_state.is_speaking else ""
        
        st.markdown(f'<div class="{speaking_class}">', unsafe_allow_html=True)
        st.components.v1.iframe(
            avatar_url,
            width=250,
            height=350,
            scrolling=False
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 状态显示
        if st.session_state.is_speaking:
            st.success("🔊 正在汇报...")
        else:
            st.info("🎯 等待训练指令")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 快速训练主题
        st.subheader("🚀 快速训练")
        current_subject = st.session_state.current_subject
        pain_points = SUBJECTS_DATA[current_subject]['pain_points']
        
        for pain_point in pain_points[:3]:
            if st.button(f"💡 {pain_point}问题", key=f"quick_{pain_point}", use_container_width=True):
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
