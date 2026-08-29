# import streamlit as st

# # APP LOGO
# st.logo("my_logo.png")

# left_co, cent_co, last_co = st.columns([1, 2, 1])

# with cent_co:
#     st.image("my_logo.png", width=550)

# st.set_page_config(
#     page_title="EduPlatform POC | Home",
#     page_icon="🏫",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.markdown(
#     """
#     <style>
#     /* Light Theme Styles */
#     .main { background-color: #ffffff; color: #1f2937; }
    
#     .hero-box {
#         background-color: #f8fafc;
#         padding: 40px;
#         border-radius: 12px;
#         border-left: 6px solid #2563eb;
#         margin-bottom: 30px;
#         text-align: center;
#         color: #0f172a;
#     }
    
#     .card {
#         background-color: #ffffff;
#         padding: 25px;
#         border-radius: 10px;
#         border: 1px solid #e2e8f0;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
#         height: 100%;
#         transition: transform 0.2s, box-shadow 0.2s;
#         color: #334155;
#     }
    
#     .card:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
#         border-color: #2563eb;
#     }
    
#     .stButton>button {
#         background-color: #2563eb !important;
#         color: #ffffff !important;
#         border-radius: 8px;
#         font-weight: bold;
#         margin-top: 15px;
#         border: none;
#     }
    
#     .stButton>button:hover {
#         background-color: #1d4ed8 !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# if "extracted_data" not in st.session_state:
#     st.session_state.extracted_data = None

# if "hourly_materials" not in st.session_state:
#     st.session_state.hourly_materials = {}

# st.sidebar.title("🎓 Navigation")
# st.sidebar.page_link("app.py", label="Home", icon="🏠")
# st.sidebar.page_link("pages/page1_app.py", label="1. Extractor & Planner", icon="📋")
# st.sidebar.page_link("pages/page2_app.py", label="2. Hourly Upload", icon="🕒")
# st.sidebar.page_link("pages/page3_app.py", label="3. Student Portal", icon="👨‍🎓")

# st.sidebar.markdown("---")
# st.sidebar.subheader("Global System Status")
# if st.session_state.extracted_data:
#     meta = st.session_state.extracted_data.get("metadata", {})
#     st.sidebar.success(f"✅ Active Syllabus: {meta.get('subject_name', 'Loaded')}")
#     st.sidebar.caption(f"Modules Extracted: {meta.get('num_modules', 5)}")
# else:
#     st.sidebar.warning("⚠️ No syllabus loaded. Start at Step 1.")

# st.markdown(
#     """
#     <div class="hero-box">
#         <h1 style="margin-bottom: 10px;">AI-Powered Faculty Workspace</h1>
#         <p style="font-size: 1.2rem; color: #475569; max-width: 800px; margin: 0 auto;">
#             Automate syllabus extraction, map course outcomes, generate hourly teaching plans, 
#             and centralize your lecture materials in one unified platform.
#         </p>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# col1, col2, col3 = st.columns(3, gap="large")

# with col1:
#     st.markdown(
#         """
#         <div class="card">
#             <h2 style="color: #2563eb;">Step 1: Curriculum Extractor</h2>
#             <p style="color: #475569; font-size: 1.05rem;">
#                 Upload a PDF or Word document to instantly generate a structured teaching plan.
#             </p>
#             <ul style="color: #64748b; line-height: 1.8;">
#                 <li>Extract Subject Metadata & Outcomes</li>
#                 <li>Calculate Optimal Teaching Hours</li>
#                 <li>Generate a 5-Module Hourly Breakdown</li>
#             </ul>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#     if st.button("Launch Faculty Planner ➔", use_container_width=True, key="btn1"):
#         st.switch_page("pages/page1_app.py")

# with col2:
#     st.markdown(
#         """
#         <div class="card">
#             <h2 style="color: #059669;">Step 2: Content Ingestion</h2>
#             <p style="color: #475569; font-size: 1.05rem;">
#                 Map specific lecture notes and files to the hourly schedule generated in Step 1.
#             </p>
#             <ul style="color: #64748b; line-height: 1.8;">
#                 <li>Select Modules and Specific Teaching Hours</li>
#                 <li>Author Main, Pre-Class, and Post-Class Notes</li>
#                 <li>Attach Supporting Presentations & Code</li>
#             </ul>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#     if st.button("Launch Hourly Upload ➔", use_container_width=True, key="btn2"):
#         st.switch_page("pages/page2_app.py")

# with col3:
#     st.markdown(
#         """
#         <div class="card">
#             <h2 style="color: #d97706;">Step 3: Student Portal</h2>
#             <p style="color: #475569; font-size: 1.05rem;">
#                 Access the final interactive learning materials parsed directly from the faculty.
#             </p>
#             <ul style="color: #64748b; line-height: 1.8;">
#                 <li>View Pre, Main, and Post-Class Content</li>
#                 <li>Download or View Uploaded PDFs</li>
#                 <li>Access Global Resources & Videos</li>
#             </ul>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#     if st.button("Launch Student Portal ➔", use_container_width=True, key="btn3"):
#         st.switch_page("pages/page3_app.py")
import streamlit as st

st.set_page_config(
    page_title="EduPlatform POC | Home",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# APP LOGO
st.logo("my_logo.png")

left_co, cent_co, last_co = st.columns([1, 2, 1])

with cent_co:
    st.image("my_logo.png", width=550)

st.markdown(
    """
    <style>
    /* Light Theme Styles */
    .main { background-color: #ffffff; color: #1f2937; }
    
    .hero-box {
        background-color: #f8fafc;
        padding: 40px;
        border-radius: 12px;
        border-left: 6px solid #2563eb;
        margin-bottom: 30px;
        text-align: center;
        color: #0f172a;
    }
    
    .card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        height: 100%;
        transition: transform 0.2s, box-shadow 0.2s;
        color: #334155;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #2563eb;
    }
    
    .stButton>button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 15px;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #1d4ed8 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None

if "hourly_materials" not in st.session_state:
    st.session_state.hourly_materials = {}

st.sidebar.title("🎓 Navigation")
st.sidebar.page_link("app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/page1_app.py", label="1. Extractor & Planner", icon="📋")
st.sidebar.page_link("pages/page2_app.py", label="2. Hourly Upload", icon="🕒")
st.sidebar.page_link("pages/page3_app.py", label="3. Student Portal", icon="👨‍🎓")
st.sidebar.page_link("pages/page4_app.py", label="4. AI Tutor Chatbot", icon="🤖")

st.sidebar.markdown("---")
st.sidebar.subheader("Global System Status")
if st.session_state.extracted_data:
    meta = st.session_state.extracted_data.get("metadata", {})
    st.sidebar.success(f"✅ Active Syllabus: {meta.get('subject_name', 'Loaded')}")
    st.sidebar.caption(f"Modules Extracted: {meta.get('num_modules', 5)}")
else:
    st.sidebar.warning("⚠️ No syllabus loaded. Start at Step 1.")

st.markdown(
    """
    <div class="hero-box">
        <h1 style="margin-bottom: 10px;">AI-Powered Faculty Workspace</h1>
        <p style="font-size: 1.2rem; color: #475569; max-width: 800px; margin: 0 auto;">
            Automate syllabus extraction, map course outcomes, generate hourly teaching plans, 
            and centralize your lecture materials in one unified platform.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown(
        """
        <div class="card">
            <h2 style="color: #2563eb;">Step 1: Curriculum Extractor</h2>
            <p style="color: #475569; font-size: 1.05rem;">
                Upload a PDF or Word document to instantly generate a structured teaching plan.
            </p>
            <ul style="color: #64748b; line-height: 1.8;">
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
            <h2 style="color: #059669;">Step 2: Content Ingestion</h2>
            <p style="color: #475569; font-size: 1.05rem;">
                Map specific lecture notes and files to the hourly schedule generated in Step 1.
            </p>
            <ul style="color: #64748b; line-height: 1.8;">
                <li>Select Modules and Specific Teaching Hours</li>
                <li>Author Main, Pre-Class, and Post-Class Notes</li>
                <li>Attach Supporting Presentations & Code</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Launch Hourly Upload ➔", use_container_width=True, key="btn2"):
        st.switch_page("pages/page2_app.py")

with col3:
    st.markdown(
        """
        <div class="card">
            <h2 style="color: #d97706;">Step 3: Student Portal</h2>
            <p style="color: #475569; font-size: 1.05rem;">
                Access the final interactive learning materials parsed directly from the faculty.
            </p>
            <ul style="color: #64748b; line-height: 1.8;">
                <li>View Pre, Main, and Post-Class Content</li>
                <li>Download or View Uploaded PDFs</li>
                <li>Access Global Resources & Videos</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Launch Student Portal ➔", use_container_width=True, key="btn3"):
        st.switch_page("pages/page3_app.py")

with col4:
    st.markdown(
        """
        <div class="card">
            <h2 style="color: #8b5cf6;">Step 4: AI Tutor Chatbot</h2>
            <p style="color: #475569; font-size: 1.05rem;">
                A context-aware RAG assistant that answers questions directly from your course materials.
            </p>
            <ul style="color: #64748b; line-height: 1.8;">
                <li>Query Uploaded PDFs & PPTs</li>
                <li>Phase-Specific Context</li>
                <li>Instant Doubt Resolution</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Launch AI Tutor ➔", use_container_width=True, key="btn4"):
        st.switch_page("pages/page4_app.py")
