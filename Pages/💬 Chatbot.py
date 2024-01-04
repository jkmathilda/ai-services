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
    grammar_analyzer = "You are an English teacher who analyzes texts and corrects any grammatical issues if necessary."
    translator = "You are a translator who translates English into Korean and Korean into English."
                # "You are a translator who translates English into {user chosen language}"
    psychologist = "You are an emphathetic psychologist who genuinely cares about the user and provides effective solutions along with some real life examples or an anecdote of someone."
    teacher = "You are a teacher who explains concepts clearly and easily with analogies or effective examples. "
    roles = (default_role, grammar_analyzer, translator, psychologist, teacher)
    # , coding_adviser, doc_analyzer)
    
    # if st.session_state.ai_role[1] not in (default_role, grammar_analyzer):
    #     st.session_state.ai_role[0] = default_role
    #     bf.reset_conversation()
        
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
    role_option = st.selectbox(
        label="AI role",
        options=['Assistant 💡', 'Grammar analyzer ⌨️', 'Translator 🔠', 'Psychologist 🧸', 'Teacher 📚', 'Coding advisor 💻',
                 'Language Teacher 🔡'],
        # on_change=commonFunc.reset_conversation,
        label_visibility="collapsed"
    )
    
    
    if role_option == 'Assistant 💡':
        st.session_state.ai_role[0] = "You are a helpful assistant." 
        
    elif role_option == 'Grammar analyzer ⌨️':
        st.session_state.ai_role[0] = "You are an English teacher who analyzes texts and corrects any grammatical issues if necessary."
        
    elif role_option == 'Translator 🔠':
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.lang1 = st.selectbox(
                label='Language 1:',
                options=['English', 'French', 'Spanish', 'German', 'Dutch', 'Italian', 'Hungarian', 'Latin', 
                         'Korean', 'Mandarin', 'Japanese',  'Vietnamese', 'Thai'],
                on_change=bf.reset_conversation
            )
        with col2:
            st.session_state.lang2 = st.selectbox(
                label='Language 2:',
                options=['English', 'French', 'Spanish', 'German', 'Dutch', 'Italian', 'Hungarian', 'Latin', 
                         'Korean', 'Mandarin', 'Japanese',  'Vietnamese', 'Thai'],
                on_change=bf.reset_conversation
            )
        if st.session_state.lang1 == st.session_state.lang2:
            st.session_state.ai_role[0] = "Repeat the user input. Do not say anything else. "
        else:
            st.session_state.ai_role[0] = f'''You are a translator who translates {st.session_state.lang1} into {st.session_state.lang2} 
            and {st.session_state.lang2} into {st.session_state.lang1}. Only translate. Do not say anything else. '''
                
    elif role_option == 'Psychologist 🧸':
        st.session_state.ai_role[0] = '''You are an emphathetic psychologist who genuinely cares about the user and provides effective 
        solutions along with some real life examples or an anecdote of someone.'''
        
    elif role_option == 'Teacher 📚':
        knowledge_level = st.radio(
            index=1,
            label='Knowledge level',
            options=['Elementary School', 'Secondary School', 'University'],
            on_change=bf.reset_conversation
        )
        st.session_state.ai_role[0] = f'''You are a teacher who explains concepts clearly and easily with analogies or effective examples. 
        Explain in {knowledge_level} level with {knowledge_level} level vocabularies, analogies, and examples. '''
        
    elif role_option == 'Coding advisor 💻':
        st.session_state.ai_role[0] = "You are an expert in coding who provides useful advice on efficient coding styles."
        
    elif role_option == 'Language Teacher 🔡':
        st.session_state.langtolearn = st.selectbox(
            label='Desired Language to Learn:',
            options=['English', 'French', 'Spanish', 'German', 'Dutch', 'Italian', 'Hungarian', 'Latin', 
                        'Korean', 'Mandarin', 'Japanese',  'Vietnamese', 'Thai'],
            on_change=bf.reset_conversation
        )
        st.session_state.ai_role[0] = f'''You are a language teacher who only gives responses in {st.session_state.langtolearn}. Do
        not answer in any other language other than {st.session_state.langtolearn}. '''
        
    # doc_analyzer = "You are an assistant analyzing the document uploaded."
    
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
    if "openai_api_key" not in st.session_state or st.session_state.openai_api_key == "" or not(st.session_state.openai_api_key.startswith('sk-')):
        switch_page('Home')

    main()