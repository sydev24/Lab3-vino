"""Streamlit UI — Agent Hỗ trợ Tra cứu Lịch học (Claude API)"""

import streamlit as st
from agent import ScheduleAgent

st.set_page_config(page_title="Tra cứu Lịch học", page_icon="📅", layout="wide")

if "agent" not in st.session_state:
    st.session_state.agent = ScheduleAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Agent Hỗ trợ Tra cứu Lịch học")
st.caption("Hỏi tôi về lịch học theo ngày, buổi hoặc chủ đề — Tuần 01–05/06/2026")

SUGGESTIONS = [
    "Thứ Ba học gì?",
    "Sáng thứ Hai học gì?",
    "Nội dung Vector Store học vào ngày nào?",
    "LangGraph có trong buổi học nào không?",
    "Lịch học ngày 03/06/2026?",
]

st.markdown("**Câu hỏi gợi ý:**")
cols = st.columns(len(SUGGESTIONS))
for i, suggestion in enumerate(SUGGESTIONS):
    if cols[i].button(suggestion, use_container_width=True):
        st.session_state.pending_question = suggestion

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

pending = st.session_state.pop("pending_question", None)
user_input = st.chat_input("Hỏi về lịch học...") or pending

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        agent = st.session_state.agent
        answer = agent.chat(user_input)
    except Exception as e:
        answer = f"Lỗi: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
