import streamlit as st

def main():
    st.set_page_config(
        page_title="会计思维数字人", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # 自定义样式
    st.markdown("""
    <style>
    .avatar-container {
        border: 3px solid #4CAF50;
        border-radius: 15px;
        padding: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🧮 会计思维数字人系统")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="avatar-container">', unsafe_allow_html=True)
        st.subheader("🤖 数字人形象")
        
        # 你的数字人URL
        avatar_url = "https://models.readyplayer.me/691177a7de516bcc961ee065.glb"
        
        # 显示3D模型
        st.components.v1.iframe(
            avatar_url,
            width=260,
            height=360,
            scrolling=False
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 形象信息
        st.info("""
        **形象信息**
        - ID: 691177a7de516bcc961ee065
        - 平台: Ready Player Me
        - 状态: ✅ 已加载
        """)
    
    with col2:
        st.header("💬 实时对话")
        st.caption("基于48651会计思维的智能对话")
        
        # 初始化对话
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "你好！我是基于48651会计思维的数字人助手，请问有什么会计或技术问题？"}
            ]
        
        # 显示对话历史
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # 用户输入
        if prompt := st.chat_input("输入关于会计或数字人的问题..."):
            # 添加用户消息
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            
            # 显示用户消息
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # AI回复（集成48651思维）
            with st.chat_message("assistant"):
                with st.spinner("🔍 应用会计思维分析中..."):
                    # 这里可以集成真实的AI API
                    response = f"""
**基于48651会计思维分析你的问题：**

📊 **问题分析**："{prompt}"

🎯 **4大准则视角**：
- 可靠性：确保信息准确可靠
- 相关性：紧密围绕你的需求

💡 **建议回答**：
这个问题很好的结合了会计思维与数字人技术！
"""
                    st.markdown(response)
            
            # 添加到历史
            st.session_state.chat_messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
