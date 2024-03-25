import os
from PIL import Image
from pathlib import Path
import streamlit as st
from utils import utils
from lyzr import DataConnector, DataAnalyzr
import pandas as pd

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]
# create directory if it doesn't exist
data = "data"
plot = 'plot'
os.makedirs(data, exist_ok=True)
os.makedirs(plot, exist_ok=True)

# Setup your config
st.set_page_config(
    page_title="Lyzr",
    layout="centered",  # or "wide" 
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("MultiFile Analyzer🗃️")
st.markdown("### Built using Lyzr🚀")
st.markdown("A comprehensive tool tailored for efficiently analyzing and deriving insights from datasets across diverse sources of files.")

# Custom function to style the app
def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Automate EDA Application
def data_uploader():
    st.subheader("Upload your files here")

    # Dictionary to map file types to their respective extensions
    file_types = {"CSV": ["csv"], "Excel": ["xlsx", "xls"], "JSON": ["json"]}

    # File type selection
    file_type = st.radio("Select file type:", list(file_types.keys()))

    # Upload file based on selection
    uploaded_file = st.file_uploader(f"Choose {file_type} file", type=file_types[file_type])

    # Process uploaded file
    if uploaded_file is not None:
        utils.save_uploaded_file(uploaded_file)
    else:
        utils.remove_existing_files(data)
        utils.remove_existing_files(plot)


def analyzr():
    # Get list of files in the data directory
    files = file_checker()

    # Check if any files are available
    if len(files) > 0:
        # Assuming the first file in the list is the desired file
        file_path = files[0]

        # Determine file extension
        file_extension = Path(file_path).suffix.lower()

        # Load data based on file type
        if file_extension == '.csv':
            dataframe = DataConnector().fetch_dataframe_from_csv(file_path=Path(file_path))
        elif file_extension in ('.xlsx', '.xls'):
            dataframe = DataConnector().fetch_dataframe_from_excel(file_path=Path(file_path))
        elif file_extension == '.json':
            dataframe = pd.read_json(file_path)  # Load JSON file using pandas
        else:
            st.error("Unsupported file format. Please upload a CSV, Excel, or JSON file.")
            return None

        # Initialize DataAnalyzr instance
        analyzr_instance = DataAnalyzr(df=dataframe, api_key=st.secrets["apikey"])
        return analyzr_instance
    else:
        st.error("Please upload a CSV, Excel, or JSON file.")
        return None

def file_checker():
    file = []
    for filename in os.listdir(data):
        file_path = os.path.join(data, filename)
        file.append(file_path)

    return file

# Function to display the dataset description
def display_description(analyzr):
    description = analyzr.dataset_description()
    if description is not None:
        st.subheader("Dataset Description:")
        st.write(description)

# Function to display queries
def display_queries(analyzr):
    queries = analyzr.ai_queries_df()
    if queries is not None:
        st.subheader("These Queries you can run on the data:")
        st.write(queries)



if __name__ == "__main__":
    style_app()
    st.sidebar.title("File Analyzer Section")
    selection = st.sidebar.radio("Go to", ["Data", "Analysis"])

    if selection == "Data":
        data_uploader()
    elif selection == "Analysis":
        file = file_checker()
        if len(file) > 0:
            analyzr = analyzr()

            # Create buttons for the options
            if st.button("Data Description"):
                display_description(analyzr)
            if st.button("Generate Queries"):
                display_queries(analyzr)        
        
        else:
            st.error("Please upload a CSV file")
                
    
    with st.expander("ℹ️ - About this App"):
        st.markdown("""
        This app uses Lyzr DataAnalyzr agent to generate analysis on data. With DataAnalyzr, you can streamline the complexity of data analytics into a powerful, intuitive, and conversational interface that lets you command data with ease. For any inquiries or issues, please contact Lyzr.
        
        """)
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)
    