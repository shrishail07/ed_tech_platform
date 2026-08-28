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

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

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
    .main { background-color: #0e1117; color: #fafafa; }
    .stTextArea textarea { background-color: #1e1e2e !important; color: #ffffff !important; border: 1px solid #4b5563; }
    .stButton>button { 
        background-color: #2563eb !important; 
        color: #ffffff !important; 
        border-radius: 8px; 
        font-weight: bold; 
    }
    .stButton>button:hover { background-color: #1d4ed8 !important; }
    .content-box {
        background-color: #1e1e2e;
        padding: 20px;
        border-radius: 8px;
        border-top: 4px solid #10b981;
        margin-top: 10px;
    }
    .ai-box {
        background-color: #1a1a24;
        padding: 15px;
        border-radius: 8px;
        border: 1px dashed #8b5cf6;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. SESSION STATE MANAGEMENT & AI FUNCTIONS
# -----------------------------------------------------------------------------
if "hourly_materials" not in st.session_state:
    st.session_state.hourly_materials = {}

if "all_subjects_data" not in st.session_state or not st.session_state.all_subjects_data:
    st.warning("⚠️ No syllabus data found. Please go back to the Extractor page (Page 1) and process a syllabus first.")
    st.stop()

def generate_ai_text(api_key, prompt_text):
    """Helper function to call Groq LLM."""
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
        return ""
    try:
        llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.3-70b-versatile", temperature=0.3)
        response = llm.invoke(prompt_text)
        return response.content
    except Exception as e:
        # Fallback if specific model fails or limits are hit
        try:
            llm = ChatGroq(groq_api_key=api_key, model_name="mixtral-8x7b-32768", temperature=0.3)
            return llm.invoke(prompt_text).content
        except Exception as fallback_e:
            st.error(f"AI Generation Failed. Check API Key or Limits. Error: {fallback_e}")
            return ""

# -----------------------------------------------------------------------------
# 3. SIDEBAR & HEADER
# -----------------------------------------------------------------------------
groq_api_key = st.sidebar.text_input("Groq API Key (For AI Generation)", type="password")

st.title("🕒 Interactive Hourly Content & AI Generator")
st.caption("Select a Subject, Module, and Hour to author materials, generate AI notes, and create MCQs.")

# --- SELECTION CONTROLS (3-Step Hierarchy) ---
col1, col2, col3 = st.columns(3)

with col1:
    subject_names = list(st.session_state.all_subjects_data.keys())
    selected_subject = st.selectbox("1. Select Subject", options=subject_names)

# Fetch the specific subject's data
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
module_concepts = active_module.get("key_concepts", "No concepts provided.")

with col3:
    raw_plan = active_module.get("hourly_plan", "")
    parsed_hours = [hour.strip() for hour in raw_plan.split("\n") if hour.strip()]
    if not parsed_hours: parsed_hours = ["Fallback Hour 1"]
    selected_hour = st.selectbox("3. Select Teaching Hour", options=parsed_hours)

# Create a unique key for tracking AI drafts in session state
state_key = f"{selected_subject}_{module_name}_{selected_hour}".replace(" ", "_")

# Initialize draft states if they don't exist
for key in ["pre_notes", "pre_mcqs", "post_notes", "post_mcqs"]:
    if f"{state_key}_{key}" not in st.session_state:
        st.session_state[f"{state_key}_{key}"] = ""

# -----------------------------------------------------------------------------
# 4. UPLOAD & GENERATION INTERFACE
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader(f"Authoring: {selected_subject} ➔ {module_name} ➔ {selected_hour}")

with st.container():
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
    tab_main, tab_pre, tab_post = st.tabs(["🎓 Main Lecture", "🌅 Pre-Class (AI & Upload)", "🌇 Post-Class (AI & Upload)"])
    
    # ==========================================
    # TAB 1: MAIN LECTURE
    # ==========================================
    with tab_main:
        main_notes = st.text_area("📝 Main Lecture Notes / Script", height=150, placeholder="Type core concepts...")
        main_files = st.file_uploader("📎 Upload Main Supporting Files (PPTs, PDFs)", accept_multiple_files=True, key="main_files")
        
    # ==========================================
    # TAB 2: PRE-CLASS (NOTES + MCQs)
    # ==========================================
    with tab_pre:
        st.markdown('<div class="ai-box">', unsafe_allow_html=True)
        if st.button("✨ Auto-Generate Pre-Class Notes", key="btn_gen_pre"):
            prompt = f"Write an engaging 100-word pre-class reading instruction for engineering students studying '{selected_subject}'. Module context: {module_concepts}. Specific hour topic: {selected_hour}. Tell them what to review before class."
            st.session_state[f"{state_key}_pre_notes"] = generate_ai_text(groq_api_key, prompt)
        
        pre_notes = st.text_area(
            "🌅 Pre-Class Instructions / Reading Notes", 
            value=st.session_state[f"{state_key}_pre_notes"],
            height=150, 
            key=f"text_pre_notes_{state_key}"
        )
        pre_files = st.file_uploader("📎 Upload Pre-Class Reading Materials (PDFs)", accept_multiple_files=True, key="pre_files")
        
        st.markdown("**🧠 Generate Pre-Class Knowledge Check (MCQs)**")
        pc1, pc2, pc3 = st.columns([1, 1, 2])
        pre_easy = pc1.number_input("Easy Qs", min_value=0, max_value=10, value=2, key="pre_easy")
        pre_hard = pc2.number_input("Hard Qs", min_value=0, max_value=10, value=1, key="pre_hard")
        
        if pc3.button("✨ Generate Pre-Class MCQs", use_container_width=True, key="btn_mcq_pre"):
            prompt = f"Generate {pre_easy} easy and {pre_hard} hard multiple-choice questions for university students to test their pre-requisite knowledge on: {selected_hour}. Context: {module_concepts}. Format cleanly with Question, A/B/C/D options, and Correct Answer."
            st.session_state[f"{state_key}_pre_mcqs"] = generate_ai_text(groq_api_key, prompt)
            
        pre_mcqs = st.text_area("Pre-Class MCQs (Edit below)", value=st.session_state[f"{state_key}_pre_mcqs"], height=200, key=f"text_pre_mcqs_{state_key}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # TAB 3: POST-CLASS (NOTES + MCQs)
    # ==========================================
    with tab_post:
        st.markdown('<div class="ai-box">', unsafe_allow_html=True)
        if st.button("✨ Auto-Generate Post-Class Summary", key="btn_gen_post"):
            prompt = f"Write a 100-word post-class summary and follow-up assignment for students who just learned '{selected_hour}' in '{selected_subject}'. Provide a real-world application to think about."
            st.session_state[f"{state_key}_post_notes"] = generate_ai_text(groq_api_key, prompt)
            
        post_notes = st.text_area(
            "🌇 Post-Class Summary / Assignments", 
            value=st.session_state[f"{state_key}_post_notes"],
            height=150, 
            key=f"text_post_notes_{state_key}"
        )
        post_files = st.file_uploader("📎 Upload Post-Class Assignments (PDFs)", accept_multiple_files=True, key="post_files")
        
        st.markdown("**🧠 Generate Post-Class Assessment (MCQs)**")
        poc1, poc2, poc3 = st.columns([1, 1, 2])
        post_easy = poc1.number_input("Easy Qs", min_value=0, max_value=10, value=3, key="post_easy")
        post_hard = poc2.number_input("Hard Qs", min_value=0, max_value=10, value=2, key="post_hard")
        
        if poc3.button("✨ Generate Post-Class MCQs", use_container_width=True, key="btn_mcq_post"):
            prompt = f"Generate {post_easy} easy and {post_hard} hard multiple-choice questions to test retention on what was taught today: {selected_hour}. Context: {module_concepts}. Format cleanly with Question, A/B/C/D options, and Correct Answer."
            st.session_state[f"{state_key}_post_mcqs"] = generate_ai_text(groq_api_key, prompt)
            
        post_mcqs = st.text_area("Post-Class MCQs (Edit below)", value=st.session_state[f"{state_key}_post_mcqs"], height=200, key=f"text_post_mcqs_{state_key}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # ==========================================
    # SAVE BUTTON
    # ==========================================
    if st.button("💾 Commit Changes for this Hour", use_container_width=True):
        if selected_subject not in st.session_state.hourly_materials:
            st.session_state.hourly_materials[selected_subject] = {}
        if module_name not in st.session_state.hourly_materials[selected_subject]:
            st.session_state.hourly_materials[selected_subject][module_name] = {}
            
        st.session_state.hourly_materials[selected_subject][module_name][selected_hour] = {
            "main": {
                "notes": main_notes,
                "files": [{"name": f.name, "type": f.type, "bytes": f.getvalue()} for f in main_files]
            },
            "pre": {
                "notes": pre_notes,
                "mcqs": pre_mcqs,
                "files": [{"name": f.name, "type": f.type, "bytes": f.getvalue()} for f in pre_files]
            },
            "post": {
                "notes": post_notes,
                "mcqs": post_mcqs,
                "files": [{"name": f.name, "type": f.type, "bytes": f.getvalue()} for f in post_files]
            }
        }
        st.success(f"✅ All content (Notes, Files, MCQs) saved successfully for '{selected_hour}'!")
        
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
                        has_mcqs = "Yes" if (content['pre'].get('mcqs') or content['post'].get('mcqs')) else "No"
                        st.write(f"- **{hr_key}**: {total_files} files attached | MCQs Generated: {has_mcqs}")
                    else:
                        st.write(f"- **{hr_key}**: Legacy data format.")
