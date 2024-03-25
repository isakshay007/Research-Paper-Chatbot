import os
import streamlit as st
from PIL import Image
from lyzr import ChatBot
from utils import utils  # Assuming utils.py contains the function save_uploaded_file

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

# Create directory if it doesn't exist
data = "data"
os.makedirs(data, exist_ok=True)

# Setup Streamlit page config
st.set_page_config(
    page_title="Lyzr",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Research Paper ChatBot📝")
st.markdown("### Built using Lyzr SDK🚀")
st.markdown(
"Dive into the world of research papers effortlessly: Upload your PDF, pose your questions, and let our ChatBot illuminate your path to discovery!")

# Custom function to style the app
def style_app():
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Function to initialize ChatBot for PDF files
def initialize_chatbot(file_path):
    vector_store_params = {
        "vector_store_type": "WeaviateVectorStore",
        "url": "https://my-qa-tdacvc8s.weaviate.network",
        "api_key": "JKH1RRtpqOMRZ5cZ4L5rxcQKBMIAUhlv8A4Hj",
        "index_name": "Ronaldo"
    }
    chatbot = ChatBot.pdf_chat(input_files=[file_path], vector_store_params=vector_store_params)
    return chatbot

# Function to integrate ChatBot for PDF files
def pdf_chat_integration():

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload PDF file", type=['pdf'])
    if uploaded_file is not None:  # Check if file is uploaded
        st.success(f"File uploaded: {uploaded_file.name} (PDF)")
        st.markdown("### Pre-Prompts:")
        prompts = [
            "What are the main findings of this paper?",
            "What methodology was used in this research?",
            "Can you summarize the key points discussed in the paper?",
            "What are the implications of the research findings?"
        ]
        
        # Display pre-defined prompts as buttons
        col1, col2 = st.columns(2)
        for i, prompt in enumerate(prompts):
            if i % 2 == 0:
                button = col1.button(prompt, key=f"button_{i}")
            else:
                button = col2.button(prompt, key=f"button_{i}")

            # Check if button is clicked
            if button:
                st.text("Processing...")
                file_path = utils.save_uploaded_file(uploaded_file)  # Save uploaded file
                if file_path is not None:  # Check if file is saved successfully
                    print("File saved at:", file_path)  # Print file path for debugging
                    chatbot = initialize_chatbot(file_path)
                    if chatbot:
                        response = chatbot.chat(prompt)  # Use selected prompt
                        st.text("Answer:")
                        st.write(response.response)
                    else:
                        st.error("Failed to initialize chatbot. Please try again.")

        question = st.text_input("Ask a question about the document:")
        if st.button("Get Answer"):
            st.text("Processing...")
            file_path = utils.save_uploaded_file(uploaded_file)  # Save uploaded file
            if file_path is not None:  # Check if file is saved successfully
                print("File saved at:", file_path)  # Print file path for debugging
                chatbot = initialize_chatbot(file_path)
                if chatbot:
                    response = chatbot.chat(question)  # Corrected method call
                    st.text("Answer:")
                    st.write(response.response)
                else:
                    st.error("Failed to initialize chatbot. Please try again.")
    else:
        st.warning("Please upload a PDF file.")

if __name__ == "__main__":
    style_app()
    pdf_chat_integration()
    with st.expander("ℹ️ - About this App"):
        st.markdown("""
This app utilizes Lyzr Chatbot agent to generate analysis on data, streamlining the complexity of data analytics into a powerful, intuitive, and conversational interface. For any inquiries or issues, please contact Lyzr.
    
        """)
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)
