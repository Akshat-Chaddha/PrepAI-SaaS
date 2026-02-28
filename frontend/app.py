import streamlit as st
import requests

# ===============================
# CONFIG
# ===============================
BACKEND_URL = "https://prepai-saas-1.onrender.com"

st.set_page_config(
    page_title="PrepAI - AI Interview Coach",
    page_icon="🚀",
    layout="wide"
)

# ===============================
# SIDEBAR NAVIGATION
# ===============================
menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📝 Register", "🔒 Login", "📄 Resume Analysis"]
)

# ===============================
# HOME PAGE
# ===============================
if menu == "🏠 Home":
    st.title("🚀 PrepAI")
    st.subheader("Your Personal AI Interview Coach")
    st.write(
        """
        Welcome to PrepAI!
        
        ✔ Analyze your resume  
        ✔ Get ATS Score  
        ✔ Improve your job chances  
        """
    )

# ===============================
# REGISTER PAGE
# ===============================
elif menu == "📝 Register":
    st.header("📝 Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not email or not password:
            st.warning("Please fill all fields.")
        else:
            try:
                with st.spinner("Creating account..."):
                    response = requests.post(
                        f"{BACKEND_URL}/register",
                        json={"email": email, "password": password},
                        timeout=90
                    )

                if response.status_code == 200:
                    st.success("Account created successfully! 🎉")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
                    st.write(response.text)

            except requests.exceptions.RequestException as e:
                st.error("Backend not responding. Try again in a few seconds.")
                st.write(str(e))


# ===============================
# LOGIN PAGE
# ===============================
elif menu == "🔒 Login":
    st.header("🔒 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.warning("Please fill all fields.")
        else:
            try:
                with st.spinner("Logging in..."):
                    response = requests.post(
                        f"{BACKEND_URL}/login",
                        json={"email": email, "password": password},
                        timeout=30
                    )

                if response.status_code == 200:
                    st.success("Login successful! ✅")
                    data = response.json()
                    st.session_state["token"] = data.get("access_token")
                    st.json(data)
                else:
                    st.error("Login failed.")
                    st.write(response.text)

            except requests.exceptions.RequestException as e:
                st.error("Backend not responding.")
                st.write(str(e))


# ===============================
# RESUME ANALYSIS PAGE
# ===============================
elif menu == "📄 Resume Analysis":
    st.header("📄 Resume Analysis")

    if "token" not in st.session_state:
        st.warning("Please login first.")
    else:
        uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

        if uploaded_file is not None:
            try:
                with st.spinner("Analyzing resume..."):
                    files = {"file": uploaded_file.getvalue()}

                    headers = {
                        "Authorization": f"Bearer {st.session_state['token']}"
                    }

                    response = requests.post(
                        f"{BACKEND_URL}/upload_resume",
                        files={"file": uploaded_file},
                        headers=headers,
                        timeout=60
                    )

                if response.status_code == 200:
                    st.success("Resume analyzed successfully! 🚀")
                    st.json(response.json())
                else:
                    st.error("Analysis failed.")
                    st.write(response.text)

            except requests.exceptions.RequestException as e:
                st.error("Backend not responding.")
                st.write(str(e))