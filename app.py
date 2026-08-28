import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EduPlatform POC | Home",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #fafafa; }
    .hero-box {
        background-color: #1e1e2e;
        padding: 40px;
        border-radius: 12px;
        border-left: 6px solid #2563eb;
        margin-bottom: 30px;
        text-align: center;
    }
    .card {
        background-color: #1e1e2e;
        padding: 25px;
        border-radius: 10px;
        border: 1px solid #2a2b3d;
        height: 100%;
        transition: transform 0.2s;
    }
    .card:hover {
        transform: translateY(-5px);
        border-color: #2563eb;
    }
    .stButton>button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 15px;
    }
    .stButton>button:hover {
        background-color: #1d4ed8 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. GLOBAL SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
# These must be initialized on the main page so they exist globally 
# when users navigate between Page 1 and Page 2.
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None

if "hourly_materials" not in st.session_state:
    st.session_state.hourly_materials = {}

# -----------------------------------------------------------------------------
# 3. SIDEBAR SYSTEM STATUS
# -----------------------------------------------------------------------------
st.sidebar.title("🎓 Navigation")
st.sidebar.page_link("app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/page1_app.py", label="1. Extractor & Planner", icon="📋")
st.sidebar.page_link("pages/page2_app.py", label="2. Hourly Upload", icon="🕒")

st.sidebar.markdown("---")
st.sidebar.subheader("Global System Status")
if st.session_state.extracted_data:
    meta = st.session_state.extracted_data.get("metadata", {})
    st.sidebar.success(f"✅ Active Syllabus: {meta.get('subject_name', 'Loaded')}")
    st.sidebar.caption(f"Modules Extracted: {meta.get('num_modules', 5)}")
else:
    st.sidebar.warning("⚠️ No syllabus loaded. Start at Step 1.")

# -----------------------------------------------------------------------------
# 4. LANDING PAGE UI
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-box">
        <h1 style="margin-bottom: 10px;">AI-Powered Faculty Workspace</h1>
        <p style="font-size: 1.2rem; color: #94a3b8; max-width: 800px; margin: 0 auto;">
            Automate syllabus extraction, map course outcomes, generate hourly teaching plans, 
            and centralize your lecture materials in one unified platform.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        """
        <div class="card">
            <h2 style="color: #60a5fa;">Step 1: Curriculum Extractor</h2>
            <p style="color: #cbd5e1; font-size: 1.05rem;">
                Upload a PDF or Word document to instantly generate a structured teaching plan.
            </p>
            <ul style="color: #94a3b8; line-height: 1.8;">
                <li>Extract Subject Metadata & Outcomes</li>
                <li>Calculate Optimal Teaching Hours</li>
                <li>Generate a 5-Module Hourly Breakdown</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Launch Faculty Planner ➔", use_container_width=True, key="btn1"):
        st.switch_page("pages/page1_app.py")

with col2:
    st.markdown(
        """
        <div class="card">
            <h2 style="color: #34d399;">Step 2: Content Ingestion</h2>
            <p style="color: #cbd5e1; font-size: 1.05rem;">
                Map specific lecture notes and files to the hourly schedule generated in Step 1.
            </p>
            <ul style="color: #94a3b8; line-height: 1.8;">
                <li>Select Modules and Specific Teaching Hours</li>
                <li>Author Direct Lecture Scripts</li>
                <li>Attach Supporting Presentations & Code</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Launch Hourly Upload ➔", use_container_width=True, key="btn2"):
        st.switch_page("pages/page2_app.py")
