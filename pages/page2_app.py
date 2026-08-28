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
# 1. PAGE CONFIGURATION & STYLING (Light Theme)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Hourly Content Upload", page_icon="🕒", layout="wide")

st.markdown(
    """
    <style>
    .main { background-color: #ffffff; color: #1f2937; }
    .stTextArea textarea { background-color: #f9fafb !important; color: #111827 !important; border: 1px solid #d1d5db; }
    .stButton>button { background-color: #2563eb !important; color: #ffffff !important; border-radius: 8px; font-weight: bold; }
    .stButton>button:hover { background-color: #1d4ed8 !important; }
    .content-box { background-color: #f8fafc; padding: 20px; border-radius: 8px; border-top: 4px solid #10b981; margin-top: 10px; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;}
    .ai-box { background-color: #eff6ff; padding: 15px; border-radius: 8px; border: 1px dashed #3b82f6; margin-bottom: 15px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. SESSION STATE & AI HELPERS
# -----------------------------------------------------------------------------
if "hourly_materials" not in st.session_state:
    st.session_state.hourly_materials = {}

if "all_subjects_data" not in st.session_state or not st.session_state.all_subjects_data:
    st.warning("⚠️ No syllabus data found. Please go back to the Extractor page (Page 1) and process a syllabus first.")
    st.stop()

groq_api_key = st.session_state.get("groq_api_key", "")

def call_ai_generator(prompt_template, kwargs):
    """Helper function to call Groq LLM for content generation."""
    if not groq_api_key:
        st.error("Missing Groq API Key! Please enter it in the sidebar on the Home page.")
        return ""
    try:
        llm = ChatGroq(groq_api_key=groq_api_key, model_name="openai/gpt-oss-120b", temperature=0.3)
        prompt = PromptTemplate.from_template(prompt_template)
        chain = prompt | llm
        response = chain.invoke(kwargs)
        return response.content.strip()
    except Exception as e:
        st.error(f"AI Generation Failed: {e}")
        return ""

# -----------------------------------------------------------------------------
# 3. MAIN UI: SELECTION CONTROLS
# -----------------------------------------------------------------------------
st.title("🕒 AI-Powered Hourly Content Workspace")
st.caption("Select your Subject, Module, and Hour to generate notes, MCQs, and upload teaching files.")

col1, col2, col3 = st.columns(3)

with col1:
    subject_options = list(st.session_state.all_subjects_data.keys())
    selected_subject = st.selectbox("1. Select Subject", options=subject_options)
    active_data = st.session_state.all_subjects_data[selected_subject]
    modules = active_data.get("modules", [])

with col2:
    module_options = {i: f"Module {mod.get('module_num', i+1)}" for i, mod in enumerate(modules)}
    selected_mod_idx = st.selectbox("2. Select Module", options=list(module_options.keys()), format_func=lambda x: module_options[x])
    active_module = modules[selected_mod_idx]
    module_name = f"Module {active_module.get('module_num', selected_mod_idx+1)}"

with col3:
    raw_plan = active_module.get("hourly_plan", "")
    parsed_hours = [hour.strip() for hour in raw_plan.split("\n") if hour.strip()]
    if not parsed_hours: parsed_hours = ["Fallback Hour 1"]
    selected_hour = st.selectbox("3. Select Teaching Hour", options=parsed_hours)

topic_context = f"{selected_subject} - {module_name} - {selected_hour}. Key Concepts: {active_module.get('key_concepts', '')}"

# Setup nested dictionary for saving
if selected_subject not in st.session_state.hourly_materials:
    st.session_state.hourly_materials[selected_subject] = {}
if module_name not in st.session_state.hourly_materials[selected_subject]:
    st.session_state.hourly_materials[selected_subject][module_name] = {}

# Fetch existing saved data for this specific hour (if any)
saved_data = st.session_state.hourly_materials[selected_subject][module_name].get(selected_hour, {})

# -----------------------------------------------------------------------------
# 4. UPLOAD & AI GENERATION INTERFACE
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader(f"Workspace for: {selected_hour}")

with st.container():
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
    tab_pre, tab_main, tab_post = st.tabs(["🌅 Pre-Class Preparation", "🎓 Main Lecture", "🌇 Post-Class Review"])
    
    # --- TAB 1: PRE-CLASS ---
    with tab_pre:
        st.markdown("#### 📖 Pre-Class Reading & Instructions")
        c1, c2 = st.columns([1, 4])
        with c1:
            if st.button("✨ Draft Pre-Notes", key="btn_pre_notes", use_container_width=True):
                with st.spinner("AI is thinking..."):
                    prompt = "Write a concise, engaging pre-class reading instruction (max 3 paragraphs) for students on the topic: {topic}. Tell them what to focus on."
                    st.session_state[f"ui_pre_notes_{selected_hour}"] = call_ai_generator(prompt, {"topic": topic_context})
        with c2:
            pre_notes = st.text_area("Pre-Class Notes", value=st.session_state.get(f"ui_pre_notes_{selected_hour}", saved_data.get("pre", {}).get("notes", "")), height=150, key=f"ui_pre_notes_{selected_hour}", label_visibility="collapsed")
        
        pre_files = st.file_uploader("📎 Upload Pre-Class Materials (PDFs)", accept_multiple_files=True, key="pre_files")
        
        st.markdown("---")
        st.markdown("#### 🧠 Pre-Class Knowledge Check (MCQs)")
        st.markdown('<div class="ai-box">', unsafe_allow_html=True)
        mcq_col1, mcq_col2, mcq_col3 = st.columns([1,1,2])
        with mcq_col1: pre_easy = st.number_input("Easy Qs", min_value=0, max_value=5, value=2, key="pre_easy")
        with mcq_col2: pre_hard = st.number_input("Hard Qs", min_value=0, max_value=5, value=1, key="pre_hard")
        with mcq_col3:
            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button("✨ Generate Pre-Class MCQs", use_container_width=True):
                with st.spinner("Generating Quiz..."):
                    prompt = "Create {easy} easy and {hard} hard multiple-choice questions for university students to test their baseline knowledge on: {topic}. Format clearly with A,B,C,D options and provide the correct answer key at the bottom."
                    st.session_state[f"ui_pre_mcqs_{selected_hour}"] = call_ai_generator(prompt, {"topic": topic_context, "easy": pre_easy, "hard": pre_hard})
        st.markdown('</div>', unsafe_allow_html=True)
        pre_mcqs = st.text_area("Pre-Class MCQs", value=st.session_state.get(f"ui_pre_mcqs_{selected_hour}", saved_data.get("pre", {}).get("mcqs", "")), height=250, key=f"ui_pre_mcqs_{selected_hour}")

    # --- TAB 2: MAIN LECTURE ---
    with tab_main:
        st.markdown("#### 🎓 Main Lecture Script & Files")
        main_notes = st.text_area("Main Lecture Notes", value=saved_data.get("main", {}).get("notes", ""), height=200, placeholder="Type core concepts, examples, and talking points...")
        main_files = st.file_uploader("📎 Upload Main Lecture Decks (PPTs, PDFs)", accept_multiple_files=True, key="main_files")

    # --- TAB 3: POST-CLASS ---
    with tab_post:
        st.markdown("#### 🌇 Post-Class Summary & Homework")
        c1, c2 = st.columns([1, 4])
        with c1:
            if st.button("✨ Draft Post-Notes", key="btn_post_notes", use_container_width=True):
                with st.spinner("AI is thinking..."):
                    prompt = "Write a concise post-class summary and suggest one practical homework assignment for students based on the topic: {topic}."
                    st.session_state[f"ui_post_notes_{selected_hour}"] = call_ai_generator(prompt, {"topic": topic_context})
        with c2:
            post_notes = st.text_area("Post-Class Notes", value=st.session_state.get(f"ui_post_notes_{selected_hour}", saved_data.get("post", {}).get("notes", "")), height=150, key=f"ui_post_notes_{selected_hour}", label_visibility="collapsed")
        
        post_files = st.file_uploader("📎 Upload Post-Class Assignments (PDFs)", accept_multiple_files=True, key="post_files")
        
        st.markdown("---")
        st.markdown("#### 🧠 Post-Class Assessment (MCQs)")
        st.markdown('<div class="ai-box">', unsafe_allow_html=True)
        mcq_col1, mcq_col2, mcq_col3 = st.columns([1,1,2])
        with mcq_col1: post_easy = st.number_input("Easy Qs", min_value=0, max_value=5, value=2, key="post_easy")
        with mcq_col2: post_hard = st.number_input("Hard Qs", min_value=0, max_value=5, value=3, key="post_hard")
        with mcq_col3:
            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button("✨ Generate Post-Class MCQs", use_container_width=True):
                with st.spinner("Generating Quiz..."):
                    prompt = "Create {easy} easy and {hard} advanced/analytical multiple-choice questions to test if students understood the lecture on: {topic}. Format clearly with A,B,C,D options and provide the correct answer key at the bottom."
                    st.session_state[f"ui_post_mcqs_{selected_hour}"] = call_ai_generator(prompt, {"topic": topic_context, "easy": post_easy, "hard": post_hard})
        st.markdown('</div>', unsafe_allow_html=True)
        post_mcqs = st.text_area("Post-Class MCQs", value=st.session_state.get(f"ui_post_mcqs_{selected_hour}", saved_data.get("post", {}).get("mcqs", "")), height=250, key=f"ui_post_mcqs_{selected_hour}")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # --- SAVE BUTTON ---
    if st.button(f"💾 Save All Content for {selected_hour}", use_container_width=True):
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
        st.success(f"✅ Content mapped & saved for **{selected_subject} ➔ {selected_hour}**!")
        
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. REVIEW SAVED CONTENT
# -----------------------------------------------------------------------------
st.markdown("---")
with st.expander(f"Review Saved Materials for: {selected_subject}"):
    subject_materials = st.session_state.hourly_materials.get(selected_subject, {})
    if not subject_materials:
        st.info("No materials saved for this subject yet.")
    else:
        for mod_key, hours_dict in subject_materials.items():
            st.markdown(f"**{mod_key}**")
            for hr_key, content in hours_dict.items():
                total_files = len(content.get('main', {}).get('files', [])) + len(content.get('pre', {}).get('files', [])) + len(content.get('post', {}).get('files', []))
                has_mcqs = "Yes" if (content.get('pre', {}).get('mcqs') or content.get('post', {}).get('mcqs')) else "No"
                st.write(f"- **{hr_key}**: {total_files} files attached | MCQs Generated: {has_mcqs}")
