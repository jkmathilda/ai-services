import streamlit as st
import openai
from streamlit_extras.switch_page_button import switch_page
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.callbacks.base import BaseCallbackHandler
import baseFunction as bf
from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

def main():
    st.header('Analyze PDF 📑')
    
    pdf = st.file_uploader("Upload your PDF", type="pdf")  # Create a file uploader widget specifically for PDF files
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1: 
        cancel_button = st.button('Cancel')
    with col2: 
        show_summary = st.checkbox('Show Summary')
    
    if cancel_button:
        st.stop()
        
    user_question = st.text_input("Enter a question:")
        
    # Extract text from the PDF
    if pdf is not None:                     # Check if a PDF file has been successfully uploaded
        with col4: 
            st.write('**Upload Successful!**')
        
        pdf_reader = PdfReader(pdf)         # Initialize a PDF reader to read the uploaded file
        pdf_text = ""                           # Initialize a string to accumulate extracted text
        
        pages = 0
        for page in pdf_reader.pages:       # Loop through each page in the PDF
            pdf_text += page.extract_text()     # Append the extracted text from each page to the 'text' variable
            pages += 1
        
        # Text Split
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=50,
            length_function=len,
            separators=["\n", ".", " "] 
        )
        
        chunks = text_splitter.split_text(pdf_text)
        
        # Embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)
            
        if user_question:
            docs = knowledge_base.similarity_search(user_question)
            llm = OpenAI()
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question=user_question)
            st.info(response)
        
        if show_summary:
            summary = summarize_document(chunks)
            st.write(summary)

def summarize_document(docs, model="gpt-3.5-turbo"):
    map_prompt_template = """
        Write a summary of this chunk of text that includes the main points and any important details.
        {text}
        """

    map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])

    combine_prompt_template = """
        Write a concise summary of the following text delimited by triple backquotes.
        Return your response in bullet points which covers the key points of the text.
        ```{text}```
        SUMMARY:
        """

    combine_prompt = PromptTemplate(
        template=combine_prompt_template, input_variables=["text"]
    )

    openai_llm = ChatOpenAI(
        openai_api_key=st.session_state.openai_api_key,
        temperature=0,
        model_name=model,
        streaming=True
    )
    summary_chain = load_summarize_chain(
        llm=openai_llm,
        # retriever=vector_store.as_retriever(),
        chain_type="map_reduce",
        map_prompt=map_prompt,
        combine_prompt=combine_prompt,
        return_intermediate_steps=False,
        verbose=True,
    )
    
    output = summary_chain.run(docs)
    print(output)
    
    return output

if __name__ == "__main__":
    if "openai_api_key" not in st.session_state or st.session_state.openai_api_key == "" or not(st.session_state.openai_api_key.startswith('sk-')):
        switch_page('Home')

    main()