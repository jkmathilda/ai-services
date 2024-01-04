import streamlit as st
import openai
from streamlit_extras.switch_page_button import switch_page
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.callbacks.base import BaseCallbackHandler
import baseFunction as bf


def main():
    pass


if __name__ == "__main__":
    if "openai_api_key" not in st.session_state or st.session_state.openai_api_key == "" or not(st.session_state.openai_api_key.startswith('sk-')):
        switch_page('Home')

    main()