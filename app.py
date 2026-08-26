import os
import io
import json
import streamlit as st
from pypdf import PdfReader
import docx2txt
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Faculty Syllabus Extractor & Planner",
    page_icon="📋",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #fafafa; }
    .stTextArea textarea { background-color: #1e1e2e !important; color: #ffffff !important; border: 1px solid #333; }
    .stButton>button { 
        background-color: #2563eb !important; 
        color: #ffffff !important; 
        border-radius: 8px; 
        font-weight: bold; 
    }
    .stButton>button:hover { background-color: #1d4ed8 !important; }
    .header-box {
        background-color: #1e1e2e;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #2563eb;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. SESSION STATE MANAGEMENT
# -----------------------------------------------------------------------------
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None

# -----------------------------------------------------------------------------
# 3. HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def extract_text(uploaded_file) -> str:
    """Extracts text from PDF or DOCX files."""
    text = ""
    if uploaded_file.name.endswith(".pdf"):
        pdf_reader = PdfReader(io.BytesIO(uploaded_file.getvalue()))
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    elif uploaded_file.name.endswith((".docx", ".doc")):
        text = docx2txt.process(io.BytesIO(uploaded_file.getvalue()))
    return text

def process_syllabus_with_groq(api_key, text_content):
    """Uses Groq to extract syllabus metadata, outcomes, resources, and module plans in JSON."""
    
    # Change the model_name to the currently active 'llama-3.3-70b-versatile'
    llm = ChatGroq(groq_api_key=api_key, model_name="openai/gpt-oss-120b", temperature=0.1)
    
    prompt = PromptTemplate.from_template("""
    You are an expert academic planner and AI curriculum designer. Analyze the following syllabus document and extract the details.
    
    Calculate the optimal 'total_teaching_hours' required to teach this entire subject effectively. 
    Determine the 'subject_type' (e.g., Theory, Practical, Skill Enhancement).
    For the resources/textbooks mentioned, generate relevant search links or specific URL formats for notes and video tutorials.
    Extract the content and key concepts for exactly 5 modules. Then, generate an hourly teaching plan for each module based on its concepts.
    
    Syllabus Text:
    {text}
    
    Respond STRICTLY in the following JSON format. Do not include any markdown formatting blocks (like ```json) or conversational text.
    {{
        "metadata": {{
            "subject_name": "extracted name",
            "subject_code": "extracted code",
            "num_modules": 5,
            "total_teaching_hours": "calculated hours",
            "subject_type": "determined type"
        }},
        "outcomes": {{
            "co": ["CO1: ...", "CO2: ..."],
            "po": ["PO1: ...", "PO2: ..."]
        }},
        "resources": [
            {{"name": "Textbook 1 Name", "notes_link": "https://...", "video_link": "https://..."}}
        ],
        "modules": [
            {{
                "module_num": 1,
                "content": "Full extracted content of module 1...",
                "key_concepts": "Bullet points of key concepts...",
                "hourly_plan": "Hour 1: Concept A \\nHour 2: Concept B..."
            }},
            // ... repeat exactly up to module 5
        ]
    }}
    """)
    
    chain = prompt | llm
    try:
        response = chain.invoke({"text": text_content})
        content = response.content
        json_str = content[content.find("{"):content.rfind("}")+1]
        return json.loads(json_str)
    except Exception as e:
        st.error(f"Failed to parse LLM output. Error: {e}")
        return None

# -----------------------------------------------------------------------------
# 4. MAIN UI LAYOUT
# -----------------------------------------------------------------------------
st.title("📚 Intelligent Faculty Curriculum Planner")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password")

# --- STEP 1: INPUTS ---
st.header("Step 1: Course Configuration & Upload")
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        college = st.text_input("College Name")
        sem = st.text_input("Semester Name / Number")
    with col2:
        university = st.text_input("University Name")
        subject = st.text_input("Subject Name")
    with col3:
        department = st.text_input("Department Name")
        sub_code = st.text_input("Subject Code")
        
    uploaded_file = st.file_uploader("Upload Syllabus Document (PDF or Word)", type=["pdf", "docx", "doc"])

# --- STEP 2 to 5 TRIGGER ---
if st.button("Extract Sub Info", use_container_width=True):
    if not groq_api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not uploaded_file:
        st.error("Please upload a syllabus file.")
    else:
        with st.spinner("Analyzing syllabus and generating curriculum plan..."):
            raw_text = extract_text(uploaded_file)
            st.session_state.extracted_data = process_syllabus_with_groq(groq_api_key, raw_text)
            if st.session_state.extracted_data:
                # Override extracted names/codes if manually provided in Step 1
                if subject: st.session_state.extracted_data["metadata"]["subject_name"] = subject
                if sub_code: st.session_state.extracted_data["metadata"]["subject_code"] = sub_code
                st.success("Extraction Complete!")

# -----------------------------------------------------------------------------
# DYNAMIC UI RENDER (Displays only after extraction)
# -----------------------------------------------------------------------------
if st.session_state.extracted_data:
    data = st.session_state.extracted_data
    
    st.markdown("---")
    
    # --- STEP 2: METADATA ---
    st.header("Step 2: Extracted Subject Information")
    meta = data.get("metadata", {})
    st.markdown(
        f"""
        <div class="header-box">
            <strong>Subject Name:</strong> {meta.get('subject_name', 'N/A')} &nbsp;|&nbsp; 
            <strong>Subject Code:</strong> {meta.get('subject_code', 'N/A')} <br/>
            <strong>Total Modules:</strong> {meta.get('num_modules', '5')} &nbsp;|&nbsp; 
            <strong>Subject Type:</strong> {meta.get('subject_type', 'N/A')} <br/>
            <strong>Estimated Teaching Hours:</strong> {meta.get('total_teaching_hours', 'N/A')}
        </div>
        """, unsafe_allow_html=True
    )
    
    # --- STEP 3: CO & PO ---
    st.header("Step 3: Course & Program Outcomes")
    outcomes = data.get("outcomes", {})
    co_col, po_col = st.columns(2)
    with co_col:
        st.subheader("Course Outcomes (CO)")
        for co in outcomes.get("co", []):
            st.write(f"- {co}")
    with po_col:
        st.subheader("Program Outcomes (PO)")
        for po in outcomes.get("po", []):
            st.write(f"- {po}")
            
    st.markdown("---")
    
    # --- STEP 4: RESOURCES ---
    st.header("Step 4: Learning Resources")
    resources = data.get("resources", [])
    if resources:
        for res in resources:
            st.markdown(f"**📖 {res.get('name', 'Resource')}**")
            st.markdown(f"- **Notes:** [View Reference Material]({res.get('notes_link', '#')})")
            st.markdown(f"- **Videos:** [Watch Tutorials]({res.get('video_link', '#')})")
    else:
        st.info("No explicit textbooks or resources found in the syllabus.")
        
    st.markdown("---")
    
    # --- STEP 5: 3-COLUMN MODULE PLANNER ---
    st.header("Step 5: Interactive Module Content & Hourly Planner")
    st.caption("Review the extracted content. You can modify any text box below; edits will remain in your current session.")
    
    modules = data.get("modules", [])
    
    # Render exactly 5 rows (one for each module)
    for i, mod in enumerate(modules[:5]):
        st.markdown(f"### Module {i+1}")
        
        # 3-Column Layout per Row
        c1, c2, c3 = st.columns(3, gap="medium")
        
        with c1:
            st.text_area(
                "Extracted Content", 
                value=mod.get("content", ""), 
                height=300, 
                key=f"content_mod_{i}"
            )
        with c2:
            st.text_area(
                "Key Concepts", 
                value=mod.get("key_concepts", ""), 
                height=300, 
                key=f"concepts_mod_{i}"
            )
        with c3:
            st.text_area(
                "Hourly Teaching Plan", 
                value=mod.get("hourly_plan", ""), 
                height=300, 
                key=f"plan_mod_{i}"
            )
        st.divider()
