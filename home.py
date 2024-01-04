import streamlit as st 
import openai
import os
from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage
import baseFunction as bf

def main():
    bf.initialize_session_state()
    
    st.set_page_config(
        page_title="AI Services",
        page_icon="🪄"
    )
    
    st.title("AI Services 🪄")
    st.write("**OPENAI_API_KEY 🔑**")
    api_choice = st.radio(
        label="{API Choice}",
        options=("Your key", "My key"),
        label_visibility="collapsed",
        horizontal=True,
    )
    
    authen = False
    
    if api_choice == "Your key":
        st.session_state.openai_api_key = st.text_input(
            label="{Your OpenAI API Key}",
            type="password",
            placeholder="sk-",
            value="",
            label_visibility="collapsed",
        )
    
        if st.session_state.openai_api_key == "":
            authen = False
        elif st.session_state.openai_api_key.startswith('sk-'):
            authen = True
        else:
            authen =  False
            st.info("Please enter a valid API key 💣")
    
    else: 
        load_dotenv()
        if not load_dotenv():
            st.info("Incorrect API key or unable to load .env 💣")
            exit(1)
        else:
            st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY")
            st.info("Log-in successful!")
        
    st.session_state.openai = openai.OpenAI(
        api_key=st.session_state.openai_api_key
    )
    
    if authen == True:
        st.info("Log-in successful!")
    
if __name__ == '__main__':
    main()