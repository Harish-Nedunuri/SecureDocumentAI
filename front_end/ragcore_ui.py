import streamlit as st
import requests
import json
from datetime import datetime, timedelta
from io import BytesIO
import base64
import pkg_resources 
# set page configs
st.set_page_config(page_title="Secure RAG", page_icon=":robot:", layout="wide")
# Backend API URL
API_URL = "http://localhost:8000"
#get version number of package
__version__ = pkg_resources.get_distribution("ragcore").version
# App state
if 'history' not in st.session_state:
    st.session_state.history = []

def reset_app():
    st.session_state.history = []
# Helper function to store token in cookies
def save_token_to_session_state(token_data):
    expires_at = datetime.now() + timedelta(minutes=token_data["access_token_expires_mins"])
    st.session_state["access_token"] = token_data["access_token"]
    st.session_state["refresh_token"] = token_data["refresh_token"]
    st.session_state["expires_at"] = expires_at.isoformat()

# Helper function to refresh token
def refresh_token():
    if "refresh_token" in st.session_state:
        response = requests.post(
            f"{API_URL}/refresh-token",
            data={"refresh_token": st.session_state["refresh_token"]},
        )
        if response.status_code == 200:
            token_data = response.json()
            save_token_to_session_state(token_data)
        else:
            st.error("Failed to refresh token. Please log in again.")

# Check if access token is still valid, if not, refresh it
def get_valid_token():
    if "expires_at" in st.session_state:
        expires_at = datetime.fromisoformat(st.session_state["expires_at"])
        if datetime.now() >= expires_at:
            refresh_token()
    return st.session_state.get("access_token", None)

# Login page
def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(
            f"{API_URL}/token",
            data={"username": username, "password": password},
        )
        if response.status_code == 200:
            token_data = response.json()
            save_token_to_session_state(token_data)
            st.success("Logged in successfully!")
            # Trigger a rerun without using experimental_rerun
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid username or password")

# Protected content page
def protected_content():
    token = get_valid_token()
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/success-endpoint", headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Sidebar
            st.sidebar.image("static/RAG.png")
            st.sidebar.title(" ⚙️ Configs")
            st.sidebar.button("Reset", on_click=reset_app)
            st.sidebar.write(data["message"])

            # Main Page Banner
            st.markdown("<h1 style='text-align: center; color: blue;'>Secure RAG</h1>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; color: black;'>A Secure RAG application to use data with Personally Identifiable Information</h3>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: black;'>{__version__}</h3>", unsafe_allow_html=True)
        else:
            st.error("Failed to access protected content.")
    else:
        st.warning("You are not logged in. Please log in to continue.")

# Main application logic
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    protected_content()
else:
    login()
