# import streamlit as st

# # -----------------------------------------------------------------------------
# # 1. PAGE CONFIGURATION & STYLING
# # -----------------------------------------------------------------------------
# st.set_page_config(
#     page_title="Hourly Content Upload",
#     page_icon="🕒",
#     layout="wide"
# )

# st.markdown(
#     """
#     <style>
#     .main { background-color: #0e1117; color: #fafafa; }
#     .stTextArea textarea { background-color: #1e1e2e !important; color: #ffffff !important; border: 1px solid #333; }
#     .stButton>button { 
#         background-color: #2563eb !important; 
#         color: #ffffff !important; 
#         border-radius: 8px; 
#         font-weight: bold; 
#     }
#     .stButton>button:hover { background-color: #1d4ed8 !important; }
#     .content-box {
#         background-color: #1e1e2e;
#         padding: 20px;
#         border-radius: 8px;
#         border-top: 4px solid #10b981;
#         margin-top: 10px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # -----------------------------------------------------------------------------
# # 2. SESSION STATE MANAGEMENT
# # -----------------------------------------------------------------------------
# # Initialize a dictionary to store the uploaded content per module and hour
# if "hourly_materials" not in st.session_state:
#     st.session_state.hourly_materials = {}

# # Check if data exists from Page 1
# if "extracted_data" not in st.session_state or not st.session_state.extracted_data:
#     st.warning("⚠️ No syllabus data found. Please go back to the Extractor page (Page 1) and process a syllabus first.")
#     st.stop()

# # -----------------------------------------------------------------------------
# # 3. MAIN UI LAYOUT
# # -----------------------------------------------------------------------------
# st.title("🕒 Hour-by-Hour Content Upload")
# st.caption("Select a module and a specific teaching hour to upload your lecture materials, notes, and resources.")

# data = st.session_state.extracted_data
# modules = data.get("modules", [])

# if not modules:
#     st.error("No modules were found in the extracted data.")
#     st.stop()

# # --- SELECTION CONTROLS ---
# col1, col2 = st.columns(2)

# with col1:
#     # Button / Selectbox 1: Select Module
#     module_options = {i: f"Module {mod.get('module_num', i+1)}" for i, mod in enumerate(modules)}
#     selected_mod_idx = st.selectbox(
#         "1. Select Module", 
#         options=list(module_options.keys()), 
#         format_func=lambda x: module_options[x]
#     )

# active_module = modules[selected_mod_idx]
# module_name = f"Module {active_module.get('module_num', selected_mod_idx+1)}"

# with col2:
#     # Button / Selectbox 2: Select Hour
#     # We parse the 'hourly_plan' string from Page 1 into a list of individual hours by splitting newlines
#     raw_plan = active_module.get("hourly_plan", "")
#     parsed_hours = [hour.strip() for hour in raw_plan.split("\n") if hour.strip()]
    
#     if not parsed_hours:
#         parsed_hours = ["No specific hours defined. (Fallback Hour 1)"]

#     selected_hour = st.selectbox("2. Select Teaching Hour", options=parsed_hours)

# # --- UPLOAD INTERFACE ---
# st.markdown("---")
# st.subheader(f"Upload Materials for: {module_name} ➔ {selected_hour}")

# with st.container():
#     st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
#     # Text input for lecture notes or script
#     lecture_notes = st.text_area(
#         "📝 Faculty Lecture Notes / Script for this hour", 
#         height=200, 
#         placeholder="Type or paste the specific concepts, examples, and talking points you will cover during this hour..."
#     )
    
#     # File uploader for PPTs, PDFs, Code files, etc.
#     uploaded_files = st.file_uploader(
#         "📎 Upload Supporting Files (Presentations, PDFs, Code Snippets)", 
#         accept_multiple_files=True
#     )
    
#     # Save Button
#     if st.button("Save Hourly Content", use_container_width=True):
#         # Create nested dictionary structure if it doesn't exist
#         if module_name not in st.session_state.hourly_materials:
#             st.session_state.hourly_materials[module_name] = {}
            
#         st.session_state.hourly_materials[module_name][selected_hour] = {
#             "notes": lecture_notes,
#             #"files": [{"name": f.name, "type": f.type, "size": f.size} for f in uploaded_files] 
#             "files": [{"name": f.name, "type": f.type, "bytes": f.getvalue()} for f in uploaded_files]
#             # Note: In a real DB, you would save the actual file bytes/urls here. 
#             # We are storing metadata for the POC session state.
#         }
#         st.success(f"✅ Content saved successfully for '{selected_hour}' in {module_name}!")
        
#         st.markdown('</div>', unsafe_allow_html=True)
# # -----------------------------------------------------------------------------
# # 4. REVIEW SAVED CONTENT
# # -----------------------------------------------------------------------------
# st.markdown("---")
# with st.expander("Review Saved Hourly Materials (Session Overview)"):
#     if not st.session_state.hourly_materials:
#         st.info("No materials saved yet.")
#     else:
#         for mod_key, hours_dict in st.session_state.hourly_materials.items():
#             st.markdown(f"**{mod_key}**")
#             for hr_key, content in hours_dict.items():
#                 st.write(f"- **{hr_key}**: {len(content['files'])} files attached, {len(content['notes'])} characters of notes.")


# import streamlit as st

# # -----------------------------------------------------------------------------
# # 1. PAGE CONFIGURATION & STYLING
# # -----------------------------------------------------------------------------
# st.set_page_config(
#     page_title="Hourly Content Upload",
#     page_icon="🕒",
#     layout="wide"
# )

# st.markdown(
#     """
#     <style>
#     .main { background-color: #0e1117; color: #fafafa; }
#     .stTextArea textarea { background-color: #1e1e2e !important; color: #ffffff !important; border: 1px solid #333; }
#     .stButton>button { 
#         background-color: #2563eb !important; 
#         color: #ffffff !important; 
#         border-radius: 8px; 
#         font-weight: bold; 
#     }
#     .stButton>button:hover { background-color: #1d4ed8 !important; }
#     .content-box {
#         background-color: #1e1e2e;
#         padding: 20px;
#         border-radius: 8px;
#         border-top: 4px solid #10b981;
#         margin-top: 10px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # -----------------------------------------------------------------------------
# # 2. SESSION STATE MANAGEMENT
# # -----------------------------------------------------------------------------
# if "hourly_materials" not in st.session_state:
#     st.session_state.hourly_materials = {}

# if "extracted_data" not in st.session_state or not st.session_state.extracted_data:
#     st.warning("⚠️ No syllabus data found. Please go back to the Extractor page (Page 1) and process a syllabus first.")
#     st.stop()

# # -----------------------------------------------------------------------------
# # 3. MAIN UI LAYOUT
# # -----------------------------------------------------------------------------
# st.title("🕒 Hour-by-Hour Content Upload")
# st.caption("Select a module and a specific teaching hour to upload your lecture materials, notes, and resources.")

# data = st.session_state.extracted_data
# modules = data.get("modules", [])

# if not modules:
#     st.error("No modules were found in the extracted data.")
#     st.stop()

# # --- SELECTION CONTROLS ---
# col1, col2 = st.columns(2)

# with col1:
#     module_options = {i: f"Module {mod.get('module_num', i+1)}" for i, mod in enumerate(modules)}
#     selected_mod_idx = st.selectbox(
#         "1. Select Module", 
#         options=list(module_options.keys()), 
#         format_func=lambda x: module_options[x]
#     )

# active_module = modules[selected_mod_idx]
# module_name = f"Module {active_module.get('module_num', selected_mod_idx+1)}"

# with col2:
#     raw_plan = active_module.get("hourly_plan", "")
#     parsed_hours = [hour.strip() for hour in raw_plan.split("\n") if hour.strip()]
    
#     if not parsed_hours:
#         parsed_hours = ["No specific hours defined. (Fallback Hour 1)"]

#     selected_hour = st.selectbox("2. Select Teaching Hour", options=parsed_hours)

# # --- UPLOAD INTERFACE ---
# st.markdown("---")
# st.subheader(f"Upload Materials for: {module_name} ➔ {selected_hour}")

# with st.container():
#     st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
#     # Use tabs to organize Main, Pre-class, and Post-class uploads
#     tab_main, tab_pre, tab_post = st.tabs(["🎓 Main Lecture", "🌅 Pre-Class Materials", "🌇 Post-Class Materials"])
    
#     with tab_main:
#         main_notes = st.text_area(
#             "📝 Main Lecture Notes / Script", 
#             height=150, 
#             placeholder="Type core concepts, examples, and talking points..."
#         )
#         main_files = st.file_uploader(
#             "📎 Upload Main Supporting Files (PPTs, PDFs)", 
#             accept_multiple_files=True,
#             key="main_files"
#         )
        
#     with tab_pre:
#         pre_notes = st.text_area(
#             "🌅 Pre-Class Instructions / Reading Notes", 
#             height=150, 
#             placeholder="What should students read or prepare before this hour?..."
#         )
#         pre_files = st.file_uploader(
#             "📎 Upload Pre-Class Reading Materials (PDFs)", 
#             accept_multiple_files=True,
#             key="pre_files"
#         )
        
#     with tab_post:
#         post_notes = st.text_area(
#             "🌇 Post-Class Summary / Assignments", 
#             height=150, 
#             placeholder="Summarize the hour or provide follow-up assignment details..."
#         )
#         post_files = st.file_uploader(
#             "📎 Upload Post-Class Assignments/Homework (PDFs)", 
#             accept_multiple_files=True,
#             key="post_files"
#         )
    
#     st.markdown("<br/>", unsafe_allow_html=True)
    
#     # Save Button
#     if st.button("Save All Content for this Hour", use_container_width=True):
#         if module_name not in st.session_state.hourly_materials:
#             st.session_state.hourly_materials[module_name] = {}
            
#         st.session_state.hourly_materials[module_name][selected_hour] = {
#             "main": {
#                 "notes": main_notes,
#                 "files": [{"name": f.name, "type": f.type, "bytes": f.getvalue()} for f in main_files]
#             },
#             "pre": {
#                 "notes": pre_notes,
#                 "files": [{"name": f.name, "type": f.type, "bytes": f.getvalue()} for f in pre_files]
#             },
#             "post": {
#                 "notes": post_notes,
#                 "files": [{"name": f.name, "type": f.type, "bytes": f.getvalue()} for f in post_files]
#             }
#         }
#         st.success(f"✅ Main, Pre-Class, and Post-Class content saved successfully for '{selected_hour}' in {module_name}!")
        
#     st.markdown('</div>', unsafe_allow_html=True)

# # -----------------------------------------------------------------------------
# # 4. REVIEW SAVED CONTENT
# # -----------------------------------------------------------------------------
# # st.markdown("---")
# # with st.expander("Review Saved Hourly Materials (Session Overview)"):
# #     if not st.session_state.hourly_materials:
# #         st.info("No materials saved yet.")
# #     else:
# #         for mod_key, hours_dict in st.session_state.hourly_materials.items():
# #             st.markdown(f"**{mod_key}**")
# #             for hr_key, content in hours_dict.items():
# #                 total_files = len(content['main']['files']) + len(content['pre']['files']) + len(content['post']['files'])
# #                 st.write(f"- **{hr_key}**: {total_files} total files attached across all phases.")

# # -----------------------------------------------------------------------------
# # 4. REVIEW SAVED CONTENT
# # -----------------------------------------------------------------------------
# st.markdown("---")
# with st.expander("Review Saved Hourly Materials (Session Overview)"):
#     if not st.session_state.hourly_materials:
#         st.info("No materials saved yet.")
#     else:
#         for mod_key, hours_dict in st.session_state.hourly_materials.items():
#             st.markdown(f"**{mod_key}**")
#             for hr_key, content in hours_dict.items():
#                 # Safety check to handle old session data vs new tabbed data
#                 if "main" in content:
#                     total_files = (
#                         len(content.get('main', {}).get('files', [])) + 
#                         len(content.get('pre', {}).get('files', [])) + 
#                         len(content.get('post', {}).get('files', []))
#                     )
#                 else:
#                     # Fallback for old data structure
#                     total_files = len(content.get('files', []))
                    
#                 st.write(f"- **{hr_key}**: {total_files} total files attached.")

import io
import streamlit as st
from pypdf import PdfReader
import docx2txt
from langchain_groq import ChatGroq

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Hourly Content Upload & AI Generator",
    page_icon="🕒",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main { background-color: #ffffff; color: #1f2937; }
    .stTextArea textarea { 
        background-color: #f9fafb !important; 
        color: #111827 !important; 
        border: 1px solid #d1d5db; 
    }
    .stButton>button { 
        background-color: #2563eb !important; 
        color: #ffffff !important; 
        border-radius: 8px; 
        font-weight: bold; 
    }
    .stButton>button:hover { background-color: #1d4ed8 !important; }
    .content-box {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 8px;
        border-top: 4px solid #10b981;
        border-left: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        margin-top: 10px;
    }
    .ai-box {
        background-color: #f5f3ff;
        padding: 15px;
        border-radius: 8px;
        border: 1px dashed #8b5cf6;
        margin-bottom: 15px;
    }
    .status-badge {
        background-color: #ecfdf5;
        border: 1px solid #10b981;
        padding: 10px;
        border-radius: 6px;
        color: #065f46;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. SESSION STATE MANAGEMENT & HELPER FUNCTIONS
# -----------------------------------------------------------------------------
if "hourly_materials" not in st.session_state:
    st.session_state.hourly_materials = {}

if "all_subjects_data" not in st.session_state or not st.session_state.all_subjects_data:
    st.warning("⚠️ No syllabus data found. Please go back to the Extractor page (Page 1) and process a syllabus first.")
    st.stop()

def extract_text_from_files(uploaded_files):
    """Extracts raw text from PDF, DOCX, and TXT files."""
    extracted_text = ""
    for f in uploaded_files:
        try:
            if f.name.endswith(".pdf"):
                reader = PdfReader(io.BytesIO(f.getvalue()))
                for page in reader.pages:
                    t = page.extract_text()
                    if t:
                        extracted_text += t + "\n"
            elif f.name.endswith((".docx", ".doc")):
                extracted_text += docx2txt.process(io.BytesIO(f.getvalue())) + "\n"
            elif f.name.endswith(".txt"):
                extracted_text += f.getvalue().decode("utf-8") + "\n"
        except Exception as e:
            st.error(f"Error reading file {f.name}: {e}")
    return extracted_text.strip()

def generate_ai_text(api_key, prompt_text):
    """Helper function to call Groq LLM using the active model."""
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
        return ""
    try:
        llm = ChatGroq(groq_api_key=api_key, model_name="openai/gpt-oss-120b", temperature=0.2)
        response = llm.invoke(prompt_text)
        return response.content.strip()
    except Exception as e:
        st.error(f"AI Generation Failed: {e}")
        return ""

# -----------------------------------------------------------------------------
# 3. SIDEBAR & NAVIGATION CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.title("⚙️ Configuration")
groq_api_key = st.sidebar.text_input(
    "Groq API Key", 
    value=st.session_state.get("groq_api_key", ""), 
    type="password"
)
st.session_state["groq_api_key"] = groq_api_key

st.title("🕒 Hour-by-Hour Content & AI Generator")
st.caption("Upload your primary lecture notes/documents. AI will generate pre-class materials, post-class summaries, and MCQs strictly from your uploaded content.")

# Selection Controls (Subject ➔ Module ➔ Hour)
col1, col2, col3 = st.columns(3)

with col1:
    subject_names = list(st.session_state.all_subjects_data.keys())
    selected_subject = st.selectbox("1. Select Subject", options=subject_names)

active_data = st.session_state.all_subjects_data[selected_subject]
modules = active_data.get("modules", [])

if not modules:
    st.error("No modules found for this subject.")
    st.stop()

with col2:
    module_options = {i: f"Module {mod.get('module_num', i+1)}" for i, mod in enumerate(modules)}
    selected_mod_idx = st.selectbox("2. Select Module", options=list(module_options.keys()), format_func=lambda x: module_options[x])

active_module = modules[selected_mod_idx]
module_name = f"Module {active_module.get('module_num', selected_mod_idx+1)}"

with col3:
    raw_plan = active_module.get("hourly_plan", "")
    parsed_hours = [hour.strip() for hour in raw_plan.split("\n") if hour.strip()]
    if not parsed_hours: 
        parsed_hours = ["Fallback Hour 1"]
    selected_hour = st.selectbox("3. Select Teaching Hour", options=parsed_hours)

# State key for preserving in-progress edits for this specific hour
state_key = f"{selected_subject}_{module_name}_{selected_hour}".replace(" ", "_")

for k in ["main_notes", "main_extracted_doc", "pre_notes", "pre_mcqs", "post_notes", "post_mcqs"]:
    if f"{state_key}_{k}" not in st.session_state:
        st.session_state[f"{state_key}_{k}"] = ""

# -----------------------------------------------------------------------------
# 4. CONTENT AUTHORING & AI TABS
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader(f"Authoring: {selected_subject} ➔ {module_name} ➔ {selected_hour}")

with st.container():
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
    tab_main, tab_pre, tab_post = st.tabs([
        "🎓 1. Main Lecture Content (Source)", 
        "🌅 2. Pre-Class Materials (AI)", 
        "🌇 3. Post-Class Materials (AI)"
    ])
    
    # =========================================================================
    # TAB 1: MAIN LECTURE (THE PRIMARY GROUNDING SOURCE)
    # =========================================================================
    with tab_main:
        st.markdown("#### Step 1: Provide Lecture Content")
        st.caption("Type notes or upload lecture files (PDF/DOCX). The AI uses this exact content to generate Pre/Post notes and MCQs.")
        
        main_notes_input = st.text_area(
            "📝 Faculty Lecture Notes / Script", 
            value=st.session_state[f"{state_key}_main_notes"],
            height=180, 
            placeholder="Type your lecture content, explanations, theorems, or talking points...",
            key=f"widget_main_notes_{state_key}"
        )
        st.session_state[f"{state_key}_main_notes"] = main_notes_input
        
        main_files = st.file_uploader(
            "📎 Upload Lecture Documents (PDF, DOCX, TXT)", 
            type=["pdf", "docx", "doc", "txt"],
            accept_multiple_files=True, 
            key=f"widget_main_files_{state_key}"
        )
        
        # Process and store uploaded text immediately in session state
        if main_files:
            extracted_doc_text = extract_text_from_files(main_files)
            st.session_state[f"{state_key}_main_extracted_doc"] = extracted_doc_text
        
        # Combine notes and uploaded text
        combined_source_text = f"{st.session_state[f'{state_key}_main_notes']}\n\n{st.session_state[f'{state_key}_main_extracted_doc']}".strip()
        
        if combined_source_text:
            st.markdown(
                f"""
                <div class="status-badge">
                    ✅ <strong>Source Material Ready:</strong> Detected {len(combined_source_text)} characters ({len(combined_source_text.split())} words) of content. 
                    You can now open Tabs 2 and 3 to generate grounded materials.
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.info("ℹ️ Upload a document or type notes above to enable document-grounded AI generation.")

    # Prepare safe context for AI prompts (truncated to avoid rate limits)
    safe_grounding_context = combined_source_text[:14000]

    # =========================================================================
    # TAB 2: PRE-CLASS (NOTES + PREREQUISITE MCQS)
    # =========================================================================
    with tab_pre:
        st.markdown('<div class="ai-box">', unsafe_allow_html=True)
        st.markdown("#### Pre-Class Reading Instructions")
        
        if st.button("✨ Generate Pre-Class Notes from Uploaded Content", key=f"btn_gen_pre_{state_key}"):
            if not safe_grounding_context:
                st.warning("⚠️ Please provide lecture notes or upload a document in Tab 1 first.")
            else:
                with st.spinner("Analyzing document and creating pre-class notes..."):
                    prompt = f"""
                    You are an expert professor. You must base your output STRICTLY on the lecture document provided below.
                    Do NOT invent external topics or use generic placeholders.

                    LECTURE DOCUMENT CONTENT:
                    \"\"\"
                    {safe_grounding_context}
                    \"\"\"

                    TASK:
                    Write a concise (120-150 words) Pre-Class Reading Guide for students before they attend the lecture on "{selected_hour}".
                    1. State the exact foundational prerequisites they must know to understand this specific document.
                    2. Highlight the key terms and formulas mentioned in this document that they should preview.
                    3. Give them 2 guiding questions to think about.
                    """
                    st.session_state[f"{state_key}_pre_notes"] = generate_ai_text(groq_api_key, prompt)
        
        pre_notes = st.text_area(
            "Pre-Class Notes (Editable)", 
            value=st.session_state[f"{state_key}_pre_notes"],
            height=160, 
            key=f"widget_pre_notes_{state_key}"
        )
        st.session_state[f"{state_key}_pre_notes"] = pre_notes
        
        pre_files = st.file_uploader("📎 Optional: Supporting Pre-Class Reading File", accept_multiple_files=True, key=f"pre_files_{state_key}")
        
        st.markdown("---")
        st.markdown("#### 🧠 Pre-Class Diagnostic MCQs")
        st.caption("Generate Multiple Choice Questions based strictly on the prerequisite concepts in the document.")
        
        pc1, pc2, pc3 = st.columns([1, 1, 2])
        pre_easy = pc1.number_input("Easy Questions", min_value=0, max_value=10, value=2, key=f"pe_{state_key}")
        pre_hard = pc2.number_input("Hard Questions", min_value=0, max_value=10, value=1, key=f"ph_{state_key}")
        
        if pc3.button("✨ Generate Pre-Class MCQs", use_container_width=True, key=f"btn_mcq_pre_{state_key}"):
            if not safe_grounding_context:
                st.warning("⚠️ Please provide lecture notes or upload a document in Tab 1 first.")
            else:
                with st.spinner("Generating MCQs based on your uploaded document..."):
                    prompt = f"""
                    You are a university examiner. Using STRICTLY the provided lecture document content below, create {pre_easy} Easy and {pre_hard} Hard Multiple Choice Questions to test students' introductory/prerequisite understanding of "{selected_hour}".

                    LECTURE DOCUMENT CONTENT:
                    \"\"\"
                    {safe_grounding_context}
                    \"\"\"

                    OUTPUT FORMAT REQUIREMENTS:
                    Format every question exactly as follows:
                    Q[Number]: [Question text based directly on the text]
                    A) [Option A]
                    B) [Option B]
                    C) [Option C]
                    D) [Option D]
                    Correct Answer: [Option Letter]
                    Explanation: [1-sentence explanation citing the content]
                    """
                    st.session_state[f"{state_key}_pre_mcqs"] = generate_ai_text(groq_api_key, prompt)
                    
        pre_mcqs = st.text_area(
            "Pre-Class MCQs (Editable)", 
            value=st.session_state[f"{state_key}_pre_mcqs"], 
            height=220, 
            key=f"widget_pre_mcqs_{state_key}"
        )
        st.session_state[f"{state_key}_pre_mcqs"] = pre_mcqs
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # TAB 3: POST-CLASS (SUMMARY + ASSESSMENT MCQS)
    # =========================================================================
    with tab_post:
        st.markdown('<div class="ai-box">', unsafe_allow_html=True)
        st.markdown("#### Post-Class Summary & Homework")
        
        if st.button("✨ Generate Post-Class Summary from Uploaded Content", key=f"btn_gen_post_{state_key}"):
            if not safe_grounding_context:
                st.warning("⚠️ Please provide lecture notes or upload a document in Tab 1 first.")
            else:
                with st.spinner("Analyzing document and creating post-class summary..."):
                    prompt = f"""
                    You are an expert professor. You must base your output STRICTLY on the lecture document provided below.

                    LECTURE DOCUMENT CONTENT:
                    \"\"\"
                    {safe_grounding_context}
                    \"\"\"

                    TASK:
                    Write a structured Post-Class Takeaway Summary for students who completed the lecture on "{selected_hour}":
                    1. Summary of Key Takeaways (3-4 bullet points extracted from the text).
                    2. Practical Application / Take-Home Problem based on the formulas or examples in the text.
                    """
                    st.session_state[f"{state_key}_post_notes"] = generate_ai_text(groq_api_key, prompt)
            
        post_notes = st.text_area(
            "Post-Class Summary / Assignments (Editable)", 
            value=st.session_state[f"{state_key}_post_notes"],
            height=160, 
            key=f"widget_post_notes_{state_key}"
        )
        st.session_state[f"{state_key}_post_notes"] = post_notes
        
        post_files = st.file_uploader("📎 Optional: Post-Class Homework File", accept_multiple_files=True, key=f"post_files_{state_key}")
        
        st.markdown("---")
        st.markdown("#### 🧠 Post-Class Mastery MCQs")
        st.caption("Generate Multiple Choice Questions testing deep retention of facts and formulas in the document.")
        
        poc1, poc2, poc3 = st.columns([1, 1, 2])
        post_easy = poc1.number_input("Easy Questions", min_value=0, max_value=10, value=3, key=f"poe_{state_key}")
        post_hard = poc2.number_input("Hard Questions", min_value=0, max_value=10, value=2, key=f"poh_{state_key}")
        
        if poc3.button("✨ Generate Post-Class MCQs", use_container_width=True, key=f"btn_mcq_post_{state_key}"):
            if not safe_grounding_context:
                st.warning("⚠️ Please provide lecture notes or upload a document in Tab 1 first.")
            else:
                with st.spinner("Generating mastery MCQs based on your uploaded document..."):
                    prompt = f"""
                    You are a university examiner. Using STRICTLY the provided lecture document content below, create {post_easy} Easy and {post_hard} Hard Multiple Choice Questions to test students' mastery of "{selected_hour}".

                    LECTURE DOCUMENT CONTENT:
                    \"\"\"
                    {safe_grounding_context}
                    \"\"\"

                    OUTPUT FORMAT REQUIREMENTS:
                    Format every question exactly as follows:
                    Q[Number]: [Question text based directly on the text]
                    A) [Option A]
                    B) [Option B]
                    C) [Option C]
                    D) [Option D]
                    Correct Answer: [Option Letter]
                    Explanation: [1-sentence explanation citing the content]
                    """
                    st.session_state[f"{state_key}_post_mcqs"] = generate_ai_text(groq_api_key, prompt)
            
        post_mcqs = st.text_area(
            "Post-Class MCQs (Editable)", 
            value=st.session_state[f"{state_key}_post_mcqs"], 
            height=220, 
            key=f"widget_post_mcqs_{state_key}"
        )
        st.session_state[f"{state_key}_post_mcqs"] = post_mcqs
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # =========================================================================
    # COMMIT CHANGES
    # =========================================================================
    if st.button("💾 Commit Changes for this Hour", use_container_width=True):
        if selected_subject not in st.session_state.hourly_materials:
            st.session_state.hourly_materials[selected_subject] = {}
        if module_name not in st.session_state.hourly_materials[selected_subject]:
            st.session_state.hourly_materials[selected_subject][module_name] = {}
            
        st.session_state.hourly_materials[selected_subject][module_name][selected_hour] = {
            "main": {
                "notes": st.session_state[f"{state_key}_main_notes"],
                "files": [{"name": f.name, "type": f.type, "bytes": f.getvalue()} for f in (main_files or [])]
            },
            "pre": {
                "notes": st.session_state[f"{state_key}_pre_notes"],
                "mcqs": st.session_state[f"{state_key}_pre_mcqs"],
                "files": [{"name": f.name, "type": f.type, "bytes": f.getvalue()} for f in (pre_files or [])]
            },
            "post": {
                "notes": st.session_state[f"{state_key}_post_notes"],
                "mcqs": st.session_state[f"{state_key}_post_mcqs"],
                "files": [{"name": f.name, "type": f.type, "bytes": f.getvalue()} for f in (post_files or [])]
            }
        }
        st.success(f"✅ All content (Notes, Files, Grounded MCQs) saved successfully for '{selected_hour}' in {selected_subject}!")
        
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. REVIEW SAVED CONTENT
# -----------------------------------------------------------------------------
st.markdown("---")
with st.expander("Review Saved Hourly Materials (Session Overview)"):
    if not st.session_state.hourly_materials:
        st.info("No materials saved yet.")
    else:
        for sub_key, sub_dict in st.session_state.hourly_materials.items():
            st.markdown(f"### 📘 {sub_key}")
            for mod_key, hours_dict in sub_dict.items():
                st.markdown(f"**{mod_key}**")
                for hr_key, content in hours_dict.items():
                    if "main" in content:
                        total_files = len(content['main']['files']) + len(content['pre']['files']) + len(content['post']['files'])
                        pre_mcq_status = "✅" if content['pre'].get('mcqs') else "❌"
                        post_mcq_status = "✅" if content['post'].get('mcqs') else "❌"
                        st.write(f"- **{hr_key}**: {total_files} files | Pre-MCQs: {pre_mcq_status} | Post-MCQs: {post_mcq_status}")
