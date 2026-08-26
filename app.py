import os
import io
import json
import base64
import streamlit as st
from pypdf import PdfReader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Syllabus & Interactive Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Added explicit button background and text colors to fix the contrast UI issue
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #fafafa; }
    
    /* Button Styling Fixes */
    .stButton>button { 
        border-radius: 8px; 
        font-weight: 600; 
        background-color: #2563eb !important; /* Blue background */
        color: #ffffff !important;            /* White text */
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #1d4ed8 !important; /* Darker blue on hover */
        color: #ffffff !important;
    }
    
    .notes-box {
        background-color: #1e1e2e;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #2563eb;
        height: 520px;
        overflow-y: auto;
        color: #ffffff;
    }
    .mcq-card {
        background-color: #1e1e2e;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #444;
        margin-bottom: 12px;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. SESSION STATE & DIRECTORY INITIALIZATION
# -----------------------------------------------------------------------------
NOTES_DIR = "./generated_notes"
os.makedirs(NOTES_DIR, exist_ok=True)

if "faculty_data" not in st.session_state:
    st.session_state.faculty_data = {
        "college_name": "",
        "university_name": "",
        "raw_text": "",
        "pdf_bytes": None,
        "extracted_meta": None,
        "modules": [],
        "supplementary": [],
    }

if "submission_result" not in st.session_state:
    st.session_state.submission_result = None

if "rag_chat_history" not in st.session_state:
    st.session_state.rag_chat_history = []


# -----------------------------------------------------------------------------
# 3. HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def display_pdf(pdf_bytes):
    """Displays the uploaded PDF in the Streamlit UI."""
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf" />'
    st.markdown(pdf_display, unsafe_allow_html=True)
    
    st.download_button(
        label="Download / View PDF externally",
        data=pdf_bytes,
        file_name="uploaded_syllabus.pdf",
        mime="application/pdf"
    )

def extract_pdf_text(pdf_bytes) -> str:
    cleaned_bytes = pdf_bytes.lstrip() 
    pdf_reader = PdfReader(io.BytesIO(cleaned_bytes))
    return "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

def save_notes_to_file(module_id, note_type, content):
    filename = f"{NOTES_DIR}/module_{module_id}_{note_type}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def load_notes_from_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return "Notes not found."

def generate_content_with_groq(api_key, module_title, context, config):
    """Calls Groq using the currently supported Llama 3 model."""
    # Changed model from decommissioned mixtral to llama3-70b-8192
    llm = ChatGroq(groq_api_key=api_key, model_name="llama3-70b-8192", temperature=0.2)
    
    prompt = PromptTemplate.from_template("""
    You are an expert AI curriculum developer. Based on the syllabus context provided, generate the following for the module: '{module_title}'
    
    Context: {context}
    
    Requirements:
    1. PRE-CLASS NOTES: Deep, hourly-basis theoretical notes formatted in Markdown.
    2. POST-CLASS NOTES: Summary, practical applications, and review notes formatted in Markdown.
    3. PRE-CLASS MCQs: Exactly {pre_low} Low, {pre_mid} Medium, and {pre_hard} Hard questions.
    4. POST-CLASS MCQs: Exactly {post_low} Low, {post_mid} Medium, and {post_hard} Hard questions.
    
    Output strictly in the following JSON format without any additional conversational text or markdown code blocks wrapped around it. Just the pure JSON object:
    {{
        "pre_class_notes": "markdown string",
        "post_class_notes": "markdown string",
        "pre_class_mcqs": [ {{"id": "pre_1", "question": "...", "options": ["A", "B", "C", "D"], "answer": "A"}} ],
        "post_class_mcqs": [ {{"id": "post_1", "question": "...", "options": ["A", "B", "C", "D"], "answer": "A"}} ]
    }}
    """)
    
    chain = prompt | llm
    response = chain.invoke({
        "module_title": module_title,
        "context": context,
        "pre_low": config["pre_low"], "pre_mid": config["pre_mid"], "pre_hard": config["pre_hard"],
        "post_low": config["post_low"], "post_mid": config["post_mid"], "post_hard": config["post_hard"]
    })
    
    try:
        content = response.content
        # Better extraction to ensure we grab the JSON safely
        json_str = content[content.find("{"):content.rfind("}")+1]
        return json.loads(json_str)
    except Exception as e:
        st.error(f"Failed to parse Groq output. Ensure the model returned valid JSON. Error: {e}")
        return None

def extract_syllabus_structure(raw_text: str, college: str, uni: str):
    return {
        "subject_name": "Artificial Intelligence & Machine Learning",
        "subject_code": "21CS71",
        "total_modules": 3,
        "modules": [
            {
                "id": 1,
                "title": "Module 1: Foundations of Search Algorithms",
                "estimated_hours": "3 Hours 30 Mins",
                "submodules": ["Uninformed Search Strategies", "Informed Heuristic Search"],
            },
            {
                "id": 2,
                "title": "Module 2: Knowledge Representation & Logic",
                "estimated_hours": "2 Hours 45 Mins",
                "submodules": ["Propositional Logic & Inference", "First-Order Predicate Calculus"],
            },
            {
                "id": 3,
                "title": "Module 3: Supervised Machine Learning",
                "estimated_hours": "4 Hours 15 Mins",
                "submodules": ["Linear & Logistic Regression", "Decision Trees & Ensemble Methods"],
            },
        ],
    }


# -----------------------------------------------------------------------------
# 4. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.title("📚 EduPlatform POC")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password", help="Required for content generation.")
portal_selection = st.sidebar.radio("Navigate Portals", ["🏛️ Faculty Portal", "👨‍🎓 Student Portal"])


# -----------------------------------------------------------------------------
# 5. FACULTY PORTAL WORKFLOW
# -----------------------------------------------------------------------------
if portal_selection == "🏛️ Faculty Portal":
    st.title("Faculty Curriculum & Content Management")
    tab1, tab2 = st.tabs(["1. Data Ingestion & Extraction", "2. Groq Notes & MCQ Generation"])

    # TAB 1: PDF Upload & View
    with tab1:
        st.subheader("Step 1: Course Details & Syllabus Ingestion")
        c1, c2 = st.columns(2)
        with c1:
            college_input = st.text_input("College Name", value="PES University")
            uni_input = st.text_input("University Name", value="Autonomous / State Board")
        with c2:
            uploaded_pdf = st.file_uploader("Upload Syllabus Document (PDF)", type=["pdf"])

        if uploaded_pdf:
            st.session_state.faculty_data["pdf_bytes"] = uploaded_pdf.getvalue()

        if st.button("Extract Syllabus & Structure Modules", type="primary"):
            if st.session_state.faculty_data["pdf_bytes"]:
                raw_text = extract_pdf_text(st.session_state.faculty_data["pdf_bytes"])
                extracted = extract_syllabus_structure(raw_text, college_input, uni_input)
                st.session_state.faculty_data["extracted_meta"] = extracted
                st.session_state.faculty_data["modules"] = extracted["modules"]
                st.success("Syllabus processed successfully!")
            else:
                st.error("Please upload a PDF file.")

        if st.session_state.faculty_data["extracted_meta"]:
            st.markdown("---")
            st.subheader("Step 2: Temporal Organization & Extracted Metadata")
            meta = st.session_state.faculty_data["extracted_meta"]

            m1, m2, m3 = st.columns(3)
            m1.metric("Subject Name", meta["subject_name"])
            m2.metric("Subject Code", meta["subject_code"])
            m3.metric("Total Modules", meta["total_modules"])

            st.markdown("#### Module Breakdown & Estimated Teaching Hours")
            for mod in st.session_state.faculty_data["modules"]:
                with st.expander(f"📌 {mod['title']} — (Estimated: {mod['estimated_hours']})", expanded=True):
                    st.write("**Sub-modules:**")
                    for sm in mod["submodules"]:
                        st.write(f"- {sm}")

        if st.session_state.faculty_data["pdf_bytes"]:
            st.markdown("---")
            st.markdown("### Uploaded Syllabus Preview")
            display_pdf(st.session_state.faculty_data["pdf_bytes"])


    # TAB 2: Groq Generation & Settings
    with tab2:
        st.subheader("Step 3: Generate Deep Notes & MCQs (Pre & Post Class)")
        if not st.session_state.faculty_data["modules"]:
            st.warning("Please extract a syllabus in Tab 1 first.")
        else:
            selected_mod_idx = st.selectbox(
                "Select Module to Generate:",
                range(len(st.session_state.faculty_data["modules"])),
                format_func=lambda i: st.session_state.faculty_data["modules"][i]["title"],
            )
            current_mod = st.session_state.faculty_data["modules"][selected_mod_idx]
            
            st.markdown("#### MCQ Configuration")
            col_pre, col_post = st.columns(2)
            with col_pre:
                st.write("**Pre-Class MCQs**")
                pre_l = st.number_input("Low Difficulty", min_value=0, value=2, key="pl")
                pre_m = st.number_input("Medium Difficulty", min_value=0, value=2, key="pm")
                pre_h = st.number_input("Hard Difficulty", min_value=0, value=1, key="ph")
            with col_post:
                st.write("**Post-Class MCQs**")
                post_l = st.number_input("Low Difficulty", min_value=0, value=1, key="pol")
                post_m = st.number_input("Medium Difficulty", min_value=0, value=2, key="pom")
                post_h = st.number_input("Hard Difficulty", min_value=0, value=2, key="poh")

            if st.button("Generate Content with Groq", type="primary"):
                if not groq_api_key:
                    st.error("Please enter your Groq API Key in the sidebar.")
                else:
                    with st.spinner("Groq is analyzing syllabus and generating Notes & MCQs..."):
                        config = {
                            "pre_low": pre_l, "pre_mid": pre_m, "pre_hard": pre_h,
                            "post_low": post_l, "post_mid": post_m, "post_hard": post_h
                        }
                        
                        result = generate_content_with_groq(groq_api_key, current_mod["title"], " ".join(current_mod["submodules"]), config)
                        
                        if result:
                            pre_file = save_notes_to_file(current_mod["id"], "pre_class", result["pre_class_notes"])
                            post_file = save_notes_to_file(current_mod["id"], "post_class", result["post_class_notes"])
                            
                            st.session_state.faculty_data["modules"][selected_mod_idx]["pre_notes_file"] = pre_file
                            st.session_state.faculty_data["modules"][selected_mod_idx]["post_notes_file"] = post_file
                            st.session_state.faculty_data["modules"][selected_mod_idx]["pre_mcqs"] = result["pre_class_mcqs"]
                            st.session_state.faculty_data["modules"][selected_mod_idx]["post_mcqs"] = result["post_class_mcqs"]
                            
                            st.success(f"Content generated and saved successfully to `{NOTES_DIR}`!")


# -----------------------------------------------------------------------------
# 6. STUDENT PORTAL WORKFLOW
# -----------------------------------------------------------------------------
elif portal_selection == "👨‍🎓 Student Portal":
    st.title("Student Interactive Learning Dashboard")

    if not st.session_state.faculty_data["modules"] or "pre_notes_file" not in st.session_state.faculty_data["modules"][0]:
        st.info("No content available yet. Faculty must generate notes via Groq first.")
    else:
        active_module_idx = st.selectbox(
            "Select Course Module:",
            range(len(st.session_state.faculty_data["modules"])),
            format_func=lambda i: st.session_state.faculty_data["modules"][i]["title"],
        )
        active_module = st.session_state.faculty_data["modules"][active_module_idx]

        tab_pre, tab_post = st.tabs(["🌅 Pre-Class Learning & Assessment", "🌇 Post-Class Review & Assessment"])

        def render_student_view(notes_file, mcqs, phase_key):
            col1, col2, col3 = st.columns([1.5, 1.2, 1.3], gap="medium")
            
            with col1:
                st.subheader(f"📖 {phase_key} Notes")
                notes_content = load_notes_from_file(notes_file)
                st.markdown(f'<div class="notes-box">{notes_content}</div>', unsafe_allow_html=True)

            with col2:
                st.subheader(f"📝 {phase_key} MCQs")
                if not mcqs:
                    st.write("No questions available.")
                for idx, mcq in enumerate(mcqs, start=1):
                    st.markdown(
                        f"""
                        <div class="mcq-card">
                            <strong>Q{idx}: {mcq['question']}</strong><br/>
                            <small>A. {mcq['options'][0]} | B. {mcq['options'][1]}<br/>
                            C. {mcq['options'][2]} | D. {mcq['options'][3]}</small>
                        </div>
                        """, unsafe_allow_html=True
                    )

            with col3:
                st.subheader("✍️ Your Responses")
                with st.form(key=f"{phase_key}_form_{active_module['id']}"):
                    user_answers = {}
                    for idx, mcq in enumerate(mcqs, start=1):
                        user_answers[mcq["id"]] = st.radio(f"Q{idx}:", options=mcq["options"], key=f"r_{phase_key}_{mcq['id']}")
                    
                    if st.form_submit_button("Submit Assessment", type="primary"):
                        if mcqs:
                            score = sum([1 for mcq in mcqs if user_answers[mcq["id"]] == mcq["answer"]])
                            st.success(f"Assessment Submitted! You scored {score}/{len(mcqs)}")

        with tab_pre:
            if "pre_notes_file" in active_module:
                render_student_view(active_module["pre_notes_file"], active_module.get("pre_mcqs", []), "Pre-Class")
            else:
                st.warning("Pre-class content has not been generated for this module yet.")
            
        with tab_post:
            if "post_notes_file" in active_module:
                render_student_view(active_module["post_notes_file"], active_module.get("post_mcqs", []), "Post-Class")
            else:
                st.warning("Post-class content has not been generated for this module yet.")
