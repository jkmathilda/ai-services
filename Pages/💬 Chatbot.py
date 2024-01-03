import openai
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.callbacks.base import BaseCallbackHandler
import baseFunction as bf

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)
        
        
def generate_chat_with_ai(user_prompt):
    openai_llm = ChatOpenAI(
        openai_api_key=st.session_state.openai_api_key,
        model_name=st.session_state.llm_chatmodel,
        temperature=st.session_state.temperature,
        streaming=True,
        callbacks=[StreamHandler(st.empty())]
    )

    # Add the user input to the messages
    st.session_state.messages.append(HumanMessage(content=user_prompt))
    
    try:
        response = openai_llm(st.session_state.messages)
        generated_text = response.content
    except Exception as e:
        generated_text = None
        st.error(f"An error occurred: {e}", icon="🚨")

    if generated_text is not None:
        # Add the generated output to the messages
        st.session_state.messages.append(response)

    return generated_text


def enable_user_input():
    st.session_state.prompt_exists = True

        
def main():
    default_role = "You are a helpful assistant."
    english_teacher = "You are an English teacher who analyzes texts and corrects any grammatical issues if necessary."
    translator = "You are a translator who translates English into Korean and Korean into English."
                # "You are a translator who translates English into {user chosen language}"
    coding_adviser = "You are an expert in coding who provides useful advice on efficient coding styles."
    doc_analyzer = "You are an assistant analyzing the document uploaded."
    roles = (default_role, english_teacher, translator, coding_adviser, doc_analyzer)
    
    if st.session_state.ai_role[1] not in (default_role, english_teacher):
        st.session_state.ai_role[0] = default_role
        bf.reset_conversation()
        
    with st.sidebar:
        # LLM Models
        st.write("**LLM Models**")
        llm_options = st.sidebar.radio(
            label="llm models",
            options=(
                "gpt-3.5-turbo",
                "gpt-4"
            ),
            label_visibility="collapsed",
            key="llm_chatmodel"
        )
        
        # Temperature
        st.write("")
        st.write("**Temperature (Randomness)**")
        temp_options = st.slider(
            label="temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1,
            format="%.1f",
            label_visibility="collapsed",
            key="temperature"
        )
        st.write("(Consistent $\Longleftrightarrow$ Random)")
        
    # AI Messages
    st.write("")
    st.write("##### Message to AI")
    st.session_state.ai_role[0] = st.selectbox(
        label="AI's role",
        options=roles,
        index=roles.index(st.session_state.ai_role[1]),
        # on_change=commonFunc.reset_conversation,
        label_visibility="collapsed"
    )
    
    if st.session_state.ai_role[0] != st.session_state.ai_role[1]:
        bf.reset_conversation()
        
        
    st.write("")
    st.write("##### Conversation with AI")

    # Display conversations
    for human, ai in zip(st.session_state.human_msg, st.session_state.ai_resp):
        with st.chat_message("human"):
            st.write(human)
        with st.chat_message("ai"):
            st.write(ai)
    
    user_input = st.chat_input(
        placeholder="Enter your query",
        on_submit=enable_user_input,
        disabled=False
    )
    
    # Reset conversation
    st.button(label="Reset conversation", on_click=bf.reset_conversation)
    
    if user_input and st.session_state.prompt_exists:
        user_prompt = user_input.strip()
        
    if user_input and st.session_state.prompt_exists:
        user_prompt = user_input.strip()

    if st.session_state.prompt_exists:
        with st.chat_message("human"):
            st.write(user_prompt)

        with st.chat_message("ai"):
            generated_text = generate_chat_with_ai(user_prompt)

        st.session_state.prompt_exists = False
        
        if generated_text is not None:
            st.session_state.human_msg.append(user_prompt)
            st.session_state.ai_resp.append(generated_text)
            st.rerun()

if __name__ == "__main__":
    if "openai_api_key" not in st.session_state:
        switch_page('Home')

    main()