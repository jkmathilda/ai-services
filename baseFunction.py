import streamlit as st 
from langchain.schema import SystemMessage, HumanMessage

def initialize_session_state():
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = None
        
    if "openai" not in st.session_state:
        st.session_state.openai = None
        
    if "llm_chatmodel" not in st.session_state:
        st.session_state.llm_chatmodel = "gpt-3.5-turbo"
        
    # CHATBOT
        
    if "ai_role" not in st.session_state:
        st.session_state.ai_role = 2 * ["You are a helpful assistant."]

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=st.session_state.ai_role[0])
        ]
    if "prompt_exists" not in st.session_state:
        st.session_state.prompt_exists = False
        
    if "temperature" not in st.session_state:
        st.session_state.temperature = [0.5, 0.5]