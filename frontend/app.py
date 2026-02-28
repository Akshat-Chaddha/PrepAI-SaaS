import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="PrepAI", layout="wide")

st.title("🚀 PrepAI - AI Interview Coach")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Register", "Login", "Upload Resume"]
)

if menu == "Register":
    st.subheader("Create Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Register"):
        response = requests.post(
            f"{BACKEND_URL}/register",
            json={"email": email, "password": password}
        )
        st.success(response.json())

if menu == "Login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(
            f"{BACKEND_URL}/login",
            json={"email": email, "password": password}
        )
        st.write(response.json())

if menu == "Upload Resume":
    st.subheader("Upload Resume for ATS Score")
    file = st.file_uploader("Upload PDF", type=["pdf"])

    if file:
        if st.button("Analyze Resume"):
            files = {"file": file}
            response = requests.post(
                f"{BACKEND_URL}/upload_resume",
                files=files
            )
            st.success(response.json())