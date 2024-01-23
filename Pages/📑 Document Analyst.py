import streamlit as st
import openai
from streamlit_extras.switch_page_button import switch_page
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.callbacks.base import BaseCallbackHandler
import baseFunction as bf
from PyPDF2 import PdfReader


def main():
    st.header('Analyze PDF 📑')
    
    pdf = st.file_uploader("Upload your PDF", type="pdf")  # Create a file uploader widget specifically for PDF files
    cancel_button = st.button('Cancel')
    if cancel_button:
        st.stop()
        
    # Extract text from the PDF
    if pdf is not None:                     # Check if a PDF file has been successfully uploaded
        pdf_reader = PdfReader(pdf)         # Initialize a PDF reader to read the uploaded file
        pdf_text = ""                           # Initialize a string to accumulate extracted text
        for page in pdf_reader.pages:       # Loop through each page in the PDF
            pdf_text += page.extract_text()     # Append the extracted text from each page to the 'text' variable


if __name__ == "__main__":
    if "openai_api_key" not in st.session_state or st.session_state.openai_api_key == "" or not(st.session_state.openai_api_key.startswith('sk-')):
        switch_page('Home')

    main()