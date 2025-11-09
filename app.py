import streamlit as st

st.set_page_config(page_title="数字人演示", layout="centered")
st.title("💬 数字人基础演示")

# 最简单的对话实现
if "chat" not in st.session_state:
    st.session_state.chat = ["助手: 你好！请提问关于数字人的问题。"]

# 显示对话
for msg in st.session_state.chat:
    st.write(msg)

# 输入
user_input = st.text_input("你的问题:")
if user_input:
    st.session_state.chat.append(f"你: {user_input}")
    st.session_state.chat.append(f"助手: 已收到: '{user_input}' - 这是实时对话演示！")
    st.rerun()
