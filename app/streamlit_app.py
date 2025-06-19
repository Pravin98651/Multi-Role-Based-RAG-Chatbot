import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import json

# Configure the page
st.set_page_config(
    page_title="FinSolve Chatbot",
    page_icon="💬",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title and description
st.title("FinSolve Technologies Chatbot")
st.markdown("""
This chatbot provides role-based access to company information. Please log in to start chatting.
""")

# Sidebar for login
with st.sidebar:
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        try:
            response = requests.get(
                "http://localhost:8000/login",
                auth=HTTPBasicAuth(username, password)
            )
            if response.status_code == 200:
                data = response.json()
                if "username" in data and "role" in data:
                    st.session_state.user = data
                    st.success("Login successful!")
                else:
                    st.error("Login response missing username or role.")
            else:
                st.error("Invalid credentials")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Main chat interface
if "user" in st.session_state and "username" in st.session_state.user and "role" in st.session_state.user:
    st.sidebar.markdown(f"Logged in as: **{st.session_state.user['username']}**")
    st.sidebar.markdown(f"Role: **{st.session_state.user['role']}**")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from API
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                auth=HTTPBasicAuth(username, password),
                json={"message": prompt}
            )
            
            if response.status_code == 200:
                response_data = response.json()
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response_data["response"]})
                with st.chat_message("assistant"):
                    st.markdown(response_data["response"])
            else:
                st.error("Error getting response from server")
        except Exception as e:
            st.error(f"Error: {str(e)}")

else:
    st.info("Please log in to start chatting.") 