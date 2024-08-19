import streamlit as st
import requests
from io import BytesIO
import base64
import pkg_resources 
#get version number of package
__version__ = pkg_resources.get_distribution("ragcore").version
# Constants
API_URL_UPLOAD = "http://localhost:8000/fine-tune-llm"
API_URL_QUERY = "http://localhost:8000/single-document-query"
API_URL_MULTI_QUERY = "http://localhost:8000/multiple-document-query"
AUTH_TOKEN = "Bearer askdgsdlkdafkgdlakfbnlkfdnblksewijfoijfoioivnw002898"
headers = {
                'Authorization': AUTH_TOKEN,
                'accept': 'application/json'
            }
# set page configs
st.set_page_config(page_title="DAISI", page_icon=":robot:", layout="wide")

# App state
if 'history' not in st.session_state:
    st.session_state.history = []

def reset_app():
    st.session_state.history = []

# Sidebar
st.sidebar.image("static\DAIsi-logos.jpeg")
st.sidebar.title(" ⚙️ Configs")
st.sidebar.button("Reset", on_click=reset_app)

st.markdown("<h1 style='text-align: center; color: blue;'>DAISI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Document AI for Search and Insights</h3>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; color: black;'>{__version__}</h3>", unsafe_allow_html=True)
# Column layout
col1, col2 = st.columns([0.5,0.5])

# Column 1: File upload and display

with col1:
    with st.container(border=True):
        st.header(" 📃 Upload Document")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None:
            # Display the PDF in the app
            st.subheader("Document Preview")
            base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="670" height="800" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)

            # Re-upload the file for the API
            uploaded_file.seek(0)
            files = {'file': uploaded_file}
            headers = {
                'Authorization': AUTH_TOKEN,
                'accept': 'application/json'
            }
            response = requests.post(API_URL_UPLOAD, headers=headers, files=files)

            if response.status_code == 200:
                st.success("Document uploaded successfully!")
            else:
                st.error(response.text)


with col2:
    tab1, tab2 = st.tabs(["Single Document", "Multiple Documents"])
    with tab1:
    # Column 2: Query the document

        with st.container(border=True):
            st.header(" 🗣️ Query the Document")
            if uploaded_file is not None:
                query = st.text_input("Enter your query")
                if st.button("Submit Query"):
                    if query:
                        # Perform the query
                        params = {
                            'file_name': uploaded_file.name,
                            'query': query
                        }
                        response = requests.post(API_URL_QUERY, headers=headers, params=params)

                        if response.status_code == 201:
                            result = response.json()                       

                            # Add to history
                            st.session_state.history.append({"query": query, "answer": result["content"],"page_number":result["page_number"]})
                        else:
                            st.error(f"Error querying document: {response.text}")
                    else:
                        st.warning("Please enter a query.")

            
            for item in reversed(st.session_state.history):
                
                st.write(f"**Q:** {item['query']}")
                st.write(f"**A:** {item['answer']}")
                st.write(f"**page:** {item['page_number']}")
                st.write("---")
    with tab2:
        with st.container(border=True):
            st.header(" 🗣️ Query Multiple Documents from storage")
            
            query = st.text_input("Enter your query",key="multi-query txt input")
            if st.button("Submit Query",key="multi butoon"):
                if query:
                    # Perform the query
                    params = {                        
                        'query': query
                    }
                    response = requests.post(API_URL_MULTI_QUERY, headers=headers, params=params)

                    if response.status_code == 201:
                        result = response.json()    
                        st.write(f"**source documents searched**: {result['source_document']}")                   
                
                        # Add to history
                        st.session_state.history.append({"query": query, "answer": result["content"],"page_number":result["page_number"]})
                    else:
                        st.error(f"Error querying document: {response.text}")
                else:
                    st.warning("Please enter a query.")

            
            for item in reversed(st.session_state.history):
                
                st.write(f"**Q:** {item['query']}")
                st.write(f"**A:** {item['answer']}")
                st.write(f"**page:** {item['page_number']}")     
                      
                st.write("---")
