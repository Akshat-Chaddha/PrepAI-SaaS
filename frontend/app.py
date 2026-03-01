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
# CUSTOM CSS — DARK THEME
# ===============================
st.markdown("""
<style>
    /* ===== GOOGLE FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

    /* ===== ROOT VARIABLES ===== */
    :root {
        --bg-primary: #0d1117;
        --bg-secondary: #161b22;
        --bg-card: #1c2333;
        --bg-card-hover: #222d3f;
        --accent-blue: #00d4ff;
        --accent-violet: #7c3aed;
        --accent-green: #10b981;
        --accent-pink: #f472b6;
        --accent-orange: #f59e0b;
        --text-primary: #e6edf3;
        --text-secondary: #8b949e;
        --text-muted: #6e7681;
        --border-color: #30363d;
        --glow-blue: 0 0 20px rgba(0, 212, 255, 0.3);
        --glow-violet: 0 0 20px rgba(124, 58, 237, 0.3);
        --glow-green: 0 0 20px rgba(16, 185, 129, 0.3);
    }

    /* ===== GLOBAL OVERRIDES ===== */
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 50%, #1a1040 100%) !important;
        border-right: 1px solid var(--border-color) !important;
    }

    section[data-testid="stSidebar"] .stRadio > label {
        color: var(--text-secondary) !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    section[data-testid="stSidebar"] .stRadio > div > label {
        background: transparent !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin: 4px 0 !important;
        transition: all 0.3s ease !important;
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }

    section[data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(0, 212, 255, 0.08) !important;
        color: var(--accent-blue) !important;
        transform: translateX(4px);
    }

    section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
    section[data-testid="stSidebar"] .stRadio > div [data-checked="true"] {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(124, 58, 237, 0.15)) !important;
        border-left: 3px solid var(--accent-blue) !important;
        color: var(--accent-blue) !important;
    }

    /* ===== INPUT FIELDS ===== */
    .stTextInput > div > div > input {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        padding: 14px 18px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: var(--glow-blue) !important;
        outline: none !important;
    }

    .stTextInput > label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        margin-bottom: 6px !important;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-violet)) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 32px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        letter-spacing: 0.5px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.4), 0 0 60px rgba(124, 58, 237, 0.2) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) scale(0.98) !important;
    }

    /* ===== FILE UPLOADER ===== */
    .stFileUploader {
        background: var(--bg-secondary) !important;
        border: 2px dashed var(--border-color) !important;
        border-radius: 16px !important;
        padding: 30px !important;
        transition: all 0.3s ease !important;
    }

    .stFileUploader:hover {
        border-color: var(--accent-blue) !important;
        box-shadow: var(--glow-blue) !important;
    }

    .stFileUploader label {
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ===== ALERTS / MESSAGES ===== */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 12px !important;
        color: var(--accent-green) !important;
    }

    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 12px !important;
    }

    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
    }

    /* ===== SPINNER ===== */
    .stSpinner > div > div {
        border-top-color: var(--accent-blue) !important;
    }

    /* ===== JSON DISPLAY ===== */
    .stJson {
        background: var(--bg-secondary) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border-color) !important;
    }

    /* ===== KEYFRAME ANIMATIONS ===== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    @keyframes glow-pulse {
        0%, 100% { box-shadow: 0 0 15px rgba(0, 212, 255, 0.2); }
        50% { box-shadow: 0 0 30px rgba(0, 212, 255, 0.4), 0 0 60px rgba(124, 58, 237, 0.2); }
    }

    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }
</style>
""", unsafe_allow_html=True)


# ===============================
# SIDEBAR LOGO & NAVIGATION
# ===============================
st.sidebar.markdown("""
<div style="text-align: center; padding: 20px 0 30px 0;">
    <div style="
        font-family: 'Outfit', sans-serif;
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #00d4ff, #7c3aed, #f472b6);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shift 4s ease infinite;
        letter-spacing: -0.5px;
    ">🚀 PrepAI</div>
    <div style="
        color: #8b949e;
        font-size: 12px;
        font-family: 'Inter', sans-serif;
        margin-top: 4px;
        letter-spacing: 2px;
        text-transform: uppercase;
    ">AI Interview Coach</div>
    <div style="
        width: 60%;
        height: 1px;
        background: linear-gradient(90deg, transparent, #30363d, transparent);
        margin: 20px auto 0 auto;
    "></div>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📝 Register", "🔒 Login", "📄 Resume Analysis"]
)

# Sidebar footer
st.sidebar.markdown("""
<div style="
    position: fixed;
    bottom: 20px;
    padding: 16px;
    text-align: center;
    width: inherit;
">
    <div style="
        color: #6e7681;
        font-size: 11px;
        font-family: 'Inter', sans-serif;
        letter-spacing: 1px;
    ">POWERED BY AI ✨</div>
</div>
""", unsafe_allow_html=True)


# ===============================
# HOME PAGE
# ===============================
if menu == "🏠 Home":

    # --- Hero Section ---
    st.markdown("""
    <div style="
        text-align: center;
        padding: 60px 20px 40px 20px;
        animation: fadeInUp 0.8s ease;
    ">
        <div style="
            font-family: 'Outfit', sans-serif;
            font-size: 64px;
            font-weight: 900;
            background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 50%, #f472b6 100%);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient-shift 5s ease infinite;
            line-height: 1.1;
            margin-bottom: 16px;
            letter-spacing: -2px;
        ">Ace Every Interview</div>
        <div style="
            font-family: 'Outfit', sans-serif;
            font-size: 40px;
            font-weight: 700;
            color: #e6edf3;
            margin-bottom: 20px;
            letter-spacing: -1px;
        ">With Your AI Coach 🤖</div>
        <div style="
            color: #8b949e;
            font-size: 18px;
            font-family: 'Inter', sans-serif;
            max-width: 600px;
            margin: 0 auto 30px auto;
            line-height: 1.7;
            font-weight: 400;
        ">
            Upload your resume, get instant AI-powered feedback, improve your ATS score,
            and practice with mock interviews — all in one platform.
        </div>
        <div style="
            display: inline-block;
            padding: 12px 36px;
            background: linear-gradient(135deg, #00d4ff, #7c3aed);
            border-radius: 50px;
            color: white;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 1px;
            text-transform: uppercase;
            box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
        ">✨ Get Started — It's Free</div>
    </div>
    """, unsafe_allow_html=True)

    # --- Animated GIF Section ---
    st.markdown("""
    <div style="
        display: flex;
        justify-content: center;
        gap: 30px;
        flex-wrap: wrap;
        padding: 10px 20px 50px 20px;
        animation: fadeInUp 1s ease;
    ">
        <div style="
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid #30363d;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            animation: float 4s ease-in-out infinite;
            max-width: 360px;
        ">
            <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjZ4c2E2d3Q0NWRiNHZhbmd3MWR5OXQ5b3YxdXhsZjA2eXA4NHZzYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/qgQUggAC3Pfv687qPC/giphy.gif"
                 style="width: 100%; display: block;" alt="AI Coding">
        </div>
        <div style="
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid #30363d;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            animation: float 4s ease-in-out infinite 1s;
            max-width: 360px;
        ">
            <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXlrNjVjM2w2b2Z0Mnd0b2MxdW5zN201OGFzZzl6eGplOHJncXR0NiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/LaVp0AyqR5bGsC5Cbm/giphy.gif"
                 style="width: 100%; display: block;" alt="Interview Prep">
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Feature Cards Section ---
    st.markdown("""
    <div style="
        text-align: center;
        margin-bottom: 40px;
        animation: fadeInUp 0.6s ease;
    ">
        <div style="
            color: #00d4ff;
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 12px;
        ">FEATURES</div>
        <div style="
            font-family: 'Outfit', sans-serif;
            font-size: 36px;
            font-weight: 700;
            color: #e6edf3;
            letter-spacing: -1px;
        ">Everything You Need to Succeed</div>
    </div>
    """, unsafe_allow_html=True)

    # Inject CSS for hover card effects (pure CSS, no JS needed)
    st.markdown("""
    <style>
        .feature-card {
            background: linear-gradient(145deg, #1c2333, #222d3f);
            border: 1px solid #30363d;
            border-radius: 20px;
            padding: 36px 28px;
            width: 300px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .feature-card .card-extra {
            max-height: 0;
            opacity: 0;
            overflow: hidden;
            transition: all 0.4s ease;
            font-size: 13px;
            font-family: 'Inter', sans-serif;
            line-height: 1.5;
            margin-top: 0;
            padding-top: 0;
        }
        .feature-card:hover .card-extra {
            max-height: 120px;
            opacity: 1;
            margin-top: 16px;
            padding-top: 12px;
        }

        .card-blue:hover {
            transform: translateY(-12px) scale(1.03);
            border-color: #00d4ff !important;
            box-shadow: 0 20px 60px rgba(0, 212, 255, 0.25), 0 0 40px rgba(0, 212, 255, 0.1);
        }
        .card-blue .card-extra {
            color: #00d4ff;
            border-top: 1px solid rgba(0, 212, 255, 0.2);
        }

        .card-violet:hover {
            transform: translateY(-12px) scale(1.03);
            border-color: #7c3aed !important;
            box-shadow: 0 20px 60px rgba(124, 58, 237, 0.25), 0 0 40px rgba(124, 58, 237, 0.1);
        }
        .card-violet .card-extra {
            color: #7c3aed;
            border-top: 1px solid rgba(124, 58, 237, 0.2);
        }

        .card-green:hover {
            transform: translateY(-12px) scale(1.03);
            border-color: #10b981 !important;
            box-shadow: 0 20px 60px rgba(16, 185, 129, 0.25), 0 0 40px rgba(16, 185, 129, 0.1);
        }
        .card-green .card-extra {
            color: #10b981;
            border-top: 1px solid rgba(16, 185, 129, 0.2);
        }
    </style>

    <div style="display: flex; justify-content: center; gap: 24px; flex-wrap: wrap; padding: 0 20px 60px 20px; animation: fadeInUp 0.8s ease;">
        <div class="feature-card card-blue">
            <div style="font-size: 48px; margin-bottom: 16px;">�</div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 22px; font-weight: 700; color: #e6edf3; margin-bottom: 10px;">Resume Analysis</div>
            <div style="color: #8b949e; font-size: 14px; line-height: 1.6; font-family: 'Inter', sans-serif;">Upload your resume and get instant AI-powered feedback on structure, keywords, and impact.</div>
            <div class="card-extra">🔍 Our AI scans your resume against 100+ best practices and provides actionable suggestions to boost your profile.</div>
        </div>
        <div class="feature-card card-violet">
            <div style="font-size: 48px; margin-bottom: 16px;">📊</div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 22px; font-weight: 700; color: #e6edf3; margin-bottom: 10px;">ATS Score</div>
            <div style="color: #8b949e; font-size: 14px; line-height: 1.6; font-family: 'Inter', sans-serif;">Check how well your resume passes through Applicant Tracking Systems used by top companies.</div>
            <div class="card-extra">📈 Get a compatibility score, keyword match analysis, and formatting recommendations to beat the ATS filters.</div>
        </div>
        <div class="feature-card card-green">
            <div style="font-size: 48px; margin-bottom: 16px;">🎯</div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 22px; font-weight: 700; color: #e6edf3; margin-bottom: 10px;">AI Mock Interview</div>
            <div style="color: #8b949e; font-size: 14px; line-height: 1.6; font-family: 'Inter', sans-serif;">Practice with our AI interviewer that simulates real interview questions tailored to your role.</div>
            <div class="card-extra">🎙️ Get real-time feedback on your answers, body language tips, and confidence scoring after each session.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- How It Works Section ---
    st.markdown("""
    <div style="
        text-align: center;
        margin-bottom: 40px;
        animation: fadeInUp 0.6s ease;
    ">
        <div style="
            color: #7c3aed;
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 12px;
        ">HOW IT WORKS</div>
        <div style="
            font-family: 'Outfit', sans-serif;
            font-size: 36px;
            font-weight: 700;
            color: #e6edf3;
            letter-spacing: -1px;
        ">Three Simple Steps</div>
    </div>
    """, unsafe_allow_html=True)

    # Step cards CSS
    st.markdown("""
    <style>
        .step-icon {
            width: 72px; height: 72px;
            border-radius: 20px;
            display: flex; align-items: center; justify-content: center;
            margin: 0 auto 20px auto;
            font-size: 32px;
        }
        .step-icon-blue {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(0, 212, 255, 0.05));
            border: 1px solid rgba(0, 212, 255, 0.3);
            animation: float 3s ease-in-out infinite;
        }
        .step-icon-violet {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.15), rgba(124, 58, 237, 0.05));
            border: 1px solid rgba(124, 58, 237, 0.3);
            animation: float 3s ease-in-out infinite 0.5s;
        }
        .step-icon-green {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));
            border: 1px solid rgba(16, 185, 129, 0.3);
            animation: float 3s ease-in-out infinite 1s;
        }
        .step-label { font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 2px; margin-bottom: 8px; }
        .step-title { font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 600; color: #e6edf3; margin-bottom: 8px; }
        .step-desc { color: #8b949e; font-size: 14px; font-family: 'Inter', sans-serif; line-height: 1.6; }
    </style>

    <div style="display: flex; justify-content: center; gap: 40px; flex-wrap: wrap; padding: 0 20px 60px 20px; animation: fadeInUp 1s ease;">
        <div style="text-align: center; max-width: 250px;">
            <div class="step-icon step-icon-blue">📤</div>
            <div class="step-label" style="color: #00d4ff;">STEP 01</div>
            <div class="step-title">Upload Resume</div>
            <div class="step-desc">Simply upload your PDF resume and let our AI do the rest.</div>
        </div>
        <div style="text-align: center; max-width: 250px;">
            <div class="step-icon step-icon-violet">🤖</div>
            <div class="step-label" style="color: #7c3aed;">STEP 02</div>
            <div class="step-title">AI Analysis</div>
            <div class="step-desc">Our AI evaluates content, keywords, formatting, and ATS compatibility.</div>
        </div>
        <div style="text-align: center; max-width: 250px;">
            <div class="step-icon step-icon-green">🚀</div>
            <div class="step-label" style="color: #10b981;">STEP 03</div>
            <div class="step-title">Get Hired</div>
            <div class="step-desc">Apply the insights, improve your resume, and land your dream job.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats CSS + HTML
    st.markdown("""
    <style>
        .stats-container {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.05), rgba(124, 58, 237, 0.05));
            border: 1px solid #30363d;
            border-radius: 24px;
            padding: 50px 30px;
            margin: 0 auto 60px auto;
            max-width: 900px;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
            animation: fadeInUp 1.2s ease;
        }
        .stat-number {
            font-family: 'Outfit', sans-serif;
            font-size: 42px; font-weight: 800;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stat-label { color: #8b949e; font-size: 14px; font-family: 'Inter', sans-serif; margin-top: 4px; }
        .stat-divider { width: 1px; background: #30363d; }
    </style>

    <div class="stats-container">
        <div style="text-align: center; min-width: 150px;">
            <div class="stat-number" style="background: linear-gradient(135deg, #00d4ff, #7c3aed);">10K+</div>
            <div class="stat-label">Resumes Analyzed</div>
        </div>
        <div class="stat-divider"></div>
        <div style="text-align: center; min-width: 150px;">
            <div class="stat-number" style="background: linear-gradient(135deg, #7c3aed, #f472b6);">95%</div>
            <div class="stat-label">Success Rate</div>
        </div>
        <div class="stat-divider"></div>
        <div style="text-align: center; min-width: 150px;">
            <div class="stat-number" style="background: linear-gradient(135deg, #10b981, #00d4ff);">50+</div>
            <div class="stat-label">Industries Covered</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Contact Section ---
    st.markdown("""
    <style>
        .contact-section {
            border-top: 1px solid #30363d;
            margin-top: 40px;
            padding: 60px 20px 40px 20px;
            text-align: center;
            animation: fadeInUp 0.8s ease;
        }
        .contact-heading-label {
            color: #f472b6;
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        .contact-heading-title {
            font-family: 'Outfit', sans-serif;
            font-size: 36px;
            font-weight: 700;
            color: #e6edf3;
            letter-spacing: -1px;
            margin-bottom: 40px;
        }
        .contact-card {
            background: linear-gradient(145deg, #1c2333, #222d3f);
            border: 1px solid #30363d;
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            margin: 0 auto;
            text-align: center;
        }
        .contact-name {
            font-family: 'Outfit', sans-serif;
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #00d4ff, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 24px;
        }
        .contact-items { display: flex; flex-direction: column; gap: 16px; align-items: center; }
        .contact-item {
            display: flex;
            align-items: center;
            gap: 12px;
            color: #8b949e;
            font-family: 'Inter', sans-serif;
            font-size: 15px;
            transition: all 0.3s ease;
        }
        .contact-item:hover { color: #e6edf3; }
        .contact-item a {
            color: #00d4ff;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .contact-item a:hover { color: #7c3aed; text-decoration: underline; }
        .contact-icon {
            width: 40px;
            height: 40px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
        }
        .icon-mail { background: rgba(0, 212, 255, 0.1); border: 1px solid rgba(0, 212, 255, 0.2); }
        .icon-phone { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); }
        .icon-linkedin { background: rgba(124, 58, 237, 0.1); border: 1px solid rgba(124, 58, 237, 0.2); }
        .footer-section {
            text-align: center;
            padding: 40px 20px;
            border-top: 1px solid #30363d;
            margin-top: 40px;
        }
        .footer-brand {
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 600;
            background: linear-gradient(135deg, #00d4ff, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        .footer-copy { color: #6e7681; font-size: 13px; font-family: 'Inter', sans-serif; }
    </style>

    <div class="contact-section">
        <div class="contact-heading-label">GET IN TOUCH</div>
        <div class="contact-heading-title">Contact Me</div>
        <div class="contact-card">
            <div class="contact-name">Akshat Chaddha</div>
            <div class="contact-items">
                <div class="contact-item">
                    <div class="contact-icon icon-mail">📧</div>
                    <a href="mailto:23ad10ak9@mitsgwl.ac.in">23ad10ak9@mitsgwl.ac.in</a>
                </div>
                <div class="contact-item">
                    <div class="contact-icon icon-phone">📱</div>
                    <a href="tel:+918871772139">+91 8871772139</a>
                </div>
                <div class="contact-item">
                    <div class="contact-icon icon-linkedin">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="#7c3aed">
                            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                        </svg>
                    </div>
                    <a href="https://www.linkedin.com/in/akshat-chaddha-343188354/" target="_blank">LinkedIn — Akshat Chaddha</a>
                </div>
            </div>
        </div>
    </div>

    <div class="footer-section">
        <div class="footer-brand">PrepAI</div>
        <div class="footer-copy">© 2026 PrepAI. Built with ❤️ by Akshat Chaddha.</div>
    </div>
    """, unsafe_allow_html=True)


# ===============================
# REGISTER PAGE
# ===============================
elif menu == "📝 Register":

    st.markdown("""
    <div style="
        text-align: center;
        padding: 40px 0 10px 0;
        animation: fadeInUp 0.6s ease;
    ">
        <div style="font-size: 56px; margin-bottom: 12px;">✨</div>
        <div style="
            font-family: 'Outfit', sans-serif;
            font-size: 36px;
            font-weight: 800;
            color: #e6edf3;
            letter-spacing: -1px;
            margin-bottom: 8px;
        ">Create Your Account</div>
        <div style="
            color: #8b949e;
            font-size: 16px;
            font-family: 'Inter', sans-serif;
        ">Join thousands of job seekers leveling up with AI</div>
    </div>
    """, unsafe_allow_html=True)

    # Centered form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, #1c2333, #222d3f);
            border: 1px solid #30363d;
            border-radius: 20px;
            padding: 40px;
            margin-top: 20px;
            animation: fadeInUp 0.8s ease;
        ">
        """, unsafe_allow_html=True)

        email = st.text_input("📧 Email Address", placeholder="you@example.com")
        password = st.text_input("🔑 Password", type="password", placeholder="Create a strong password")

        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)

        if st.button("🚀 Create Account", use_container_width=True):
            if not email or not password:
                st.warning("⚠️ Please fill in all fields.")
            else:
                try:
                    with st.spinner("Creating your account..."):
                        response = requests.post(
                            f"{BACKEND_URL}/register",
                            json={"email": email, "password": password},
                            timeout=90
                        )

                    if response.status_code == 200:
                        st.success("🎉 Account created successfully! Head to Login to get started.")
                        st.json(response.json())
                    else:
                        st.error(f"❌ Error: {response.status_code}")
                        st.write(response.text)

                except requests.exceptions.RequestException as e:
                    st.error("⚠️ Backend not responding. Please try again in a few seconds.")
                    st.write(str(e))

        st.markdown("</div>", unsafe_allow_html=True)


# ===============================
# LOGIN PAGE
# ===============================
elif menu == "🔒 Login":

    st.markdown("""
    <div style="
        text-align: center;
        padding: 40px 0 10px 0;
        animation: fadeInUp 0.6s ease;
    ">
        <div style="font-size: 56px; margin-bottom: 12px;">🔐</div>
        <div style="
            font-family: 'Outfit', sans-serif;
            font-size: 36px;
            font-weight: 800;
            color: #e6edf3;
            letter-spacing: -1px;
            margin-bottom: 8px;
        ">Welcome Back</div>
        <div style="
            color: #8b949e;
            font-size: 16px;
            font-family: 'Inter', sans-serif;
        ">Log in to continue your interview prep journey</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, #1c2333, #222d3f);
            border: 1px solid #30363d;
            border-radius: 20px;
            padding: 40px;
            margin-top: 20px;
            animation: fadeInUp 0.8s ease;
        ">
        """, unsafe_allow_html=True)

        email = st.text_input("📧 Email Address", placeholder="you@example.com")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")

        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)

        if st.button("🔓 Login", use_container_width=True):
            if not email or not password:
                st.warning("⚠️ Please fill in all fields.")
            else:
                try:
                    with st.spinner("Logging in..."):
                        response = requests.post(
                            f"{BACKEND_URL}/login",
                            json={"email": email, "password": password},
                            timeout=30
                        )

                    if response.status_code == 200:
                        st.success("✅ Login successful! Welcome back.")
                        data = response.json()
                        st.session_state["token"] = data.get("access_token")
                        st.json(data)
                    else:
                        st.error("❌ Login failed. Please check your credentials.")
                        st.write(response.text)

                except requests.exceptions.RequestException as e:
                    st.error("⚠️ Backend not responding.")
                    st.write(str(e))

        st.markdown("</div>", unsafe_allow_html=True)


# ===============================
# RESUME ANALYSIS PAGE
# ===============================
elif menu == "📄 Resume Analysis":

    st.markdown("""
    <div style="
        text-align: center;
        padding: 40px 0 10px 0;
        animation: fadeInUp 0.6s ease;
    ">
        <div style="font-size: 56px; margin-bottom: 12px;">📄</div>
        <div style="
            font-family: 'Outfit', sans-serif;
            font-size: 36px;
            font-weight: 800;
            color: #e6edf3;
            letter-spacing: -1px;
            margin-bottom: 8px;
        ">Resume Analysis</div>
        <div style="
            color: #8b949e;
            font-size: 16px;
            font-family: 'Inter', sans-serif;
        ">Upload your resume and let AI supercharge it</div>
    </div>
    """, unsafe_allow_html=True)

    if "token" not in st.session_state:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 40px;
            animation: fadeInUp 0.8s ease;
        ">
            <div style="
                background: linear-gradient(145deg, #1c2333, #222d3f);
                border: 1px solid rgba(245, 158, 11, 0.3);
                border-radius: 20px;
                padding: 40px;
                max-width: 500px;
                margin: 0 auto;
            ">
                <div style="font-size: 48px; margin-bottom: 16px;">🔒</div>
                <div style="
                    font-family: 'Outfit', sans-serif;
                    font-size: 22px;
                    font-weight: 600;
                    color: #f59e0b;
                    margin-bottom: 10px;
                ">Login Required</div>
                <div style="
                    color: #8b949e;
                    font-size: 14px;
                    font-family: 'Inter', sans-serif;
                    line-height: 1.6;
                ">Please log in from the sidebar to access the Resume Analysis feature. Your data stays secure & private.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="
                background: linear-gradient(145deg, #1c2333, #222d3f);
                border: 1px solid #30363d;
                border-radius: 20px;
                padding: 40px;
                margin-top: 20px;
                text-align: center;
                animation: fadeInUp 0.8s ease;
            ">
                <div style="font-size: 36px; margin-bottom: 10px;">☁️</div>
                <div style="
                    color: #8b949e;
                    font-size: 14px;
                    font-family: 'Inter', sans-serif;
                    margin-bottom: 20px;
                ">Drag & drop your PDF resume below or click to browse</div>
            </div>
            """, unsafe_allow_html=True)

            uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], label_visibility="collapsed")

            if uploaded_file is not None:
                try:
                    with st.spinner("🤖 Analyzing your resume with AI..."):
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
                        st.markdown("""
                        <div style="
                            text-align: center;
                            margin: 20px 0;
                            animation: fadeInUp 0.6s ease;
                        ">
                            <div style="font-size: 48px; margin-bottom: 8px;">🎉</div>
                            <div style="
                                font-family: 'Outfit', sans-serif;
                                font-size: 22px;
                                font-weight: 600;
                                color: #10b981;
                            ">Analysis Complete!</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.json(response.json())
                    else:
                        st.error("❌ Analysis failed.")
                        st.write(response.text)

                except requests.exceptions.RequestException as e:
                    st.error("⚠️ Backend not responding.")
                    st.write(str(e))