import streamlit as st
import requests

# IMPORTANT: Replace after backend deploy
BACKEND_URL = "https://prepai-saas-1.onrender.com"

st.set_page_config(
    page_title="PrepAI",
    page_icon="🚀",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
body {
    background-color: #0E1117;
}
.big-title {
    font-size:50px !important;
    font-weight:700;
    color:#4CAF50;
}
.card {
    padding:20px;
    border-radius:10px;
    background-color:#1E1E1E;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🚀 PrepAI</p>', unsafe_allow_html=True)
st.caption("Your Personal AI Interview Coach")

menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📝 Register", "🔐 Login", "📄 Resume Analysis"]
)

# ---------------- HOME ----------------
if menu == "🏠 Home":
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">📊 ATS Scoring</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">🤖 AI Mock Interviews</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">📈 Skill Gap Analysis</div>', unsafe_allow_html=True)

# ---------------- REGISTER ----------------
elif menu == "📝 Register":
    st.subheader("Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        response = requests.post(
            f"{BACKEND_URL}/register",
            json={"email": email, "password": password}
        )
        st.success(response.json())

# ---------------- LOGIN ----------------
elif menu == "🔐 Login":
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(
            f"{BACKEND_URL}/login",
            json={"email": email, "password": password}
        )
        st.write(response.json())

# ---------------- RESUME ----------------
elif menu == "📄 Resume Analysis":
    st.subheader("Upload Resume")

    file = st.file_uploader("Upload PDF", type=["pdf"])

    if file:
        if st.button("Analyze Resume"):
            files = {"file": file}
            response = requests.post(
                f"{BACKEND_URL}/upload_resume",
                files=files
            )
            data = response.json()

            st.metric("ATS Score", f"{data['ats_score']} / 100")
            st.success("Resume analyzed successfully!")