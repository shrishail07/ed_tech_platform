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


import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Hourly Content Upload",
    page_icon="🕒",
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
    .content-box {
        background-color: #1e1e2e;
        padding: 20px;
        border-radius: 8px;
        border-top: 4px solid #10b981;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. SESSION STATE MANAGEMENT
# -----------------------------------------------------------------------------
if "hourly_materials" not in st.session_state:
    st.session_state.hourly_materials = {}

if "extracted_data" not in st.session_state or not st.session_state.extracted_data:
    st.warning("⚠️ No syllabus data found. Please go back to the Extractor page (Page 1) and process a syllabus first.")
    st.stop()

# -----------------------------------------------------------------------------
# 3. MAIN UI LAYOUT
# -----------------------------------------------------------------------------
st.title("🕒 Hour-by-Hour Content Upload")
st.caption("Select a module and a specific teaching hour to upload your lecture materials, notes, and resources.")

data = st.session_state.extracted_data
modules = data.get("modules", [])

if not modules:
    st.error("No modules were found in the extracted data.")
    st.stop()

# --- SELECTION CONTROLS ---
col1, col2 = st.columns(2)

with col1:
    module_options = {i: f"Module {mod.get('module_num', i+1)}" for i, mod in enumerate(modules)}
    selected_mod_idx = st.selectbox(
        "1. Select Module", 
        options=list(module_options.keys()), 
        format_func=lambda x: module_options[x]
    )

active_module = modules[selected_mod_idx]
module_name = f"Module {active_module.get('module_num', selected_mod_idx+1)}"

with col2:
    raw_plan = active_module.get("hourly_plan", "")
    parsed_hours = [hour.strip() for hour in raw_plan.split("\n") if hour.strip()]
    
    if not parsed_hours:
        parsed_hours = ["No specific hours defined. (Fallback Hour 1)"]

    selected_hour = st.selectbox("2. Select Teaching Hour", options=parsed_hours)

# --- UPLOAD INTERFACE ---
st.markdown("---")
st.subheader(f"Upload Materials for: {module_name} ➔ {selected_hour}")

with st.container():
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
    # Use tabs to organize Main, Pre-class, and Post-class uploads
    tab_main, tab_pre, tab_post = st.tabs(["🎓 Main Lecture", "🌅 Pre-Class Materials", "🌇 Post-Class Materials"])
    
    with tab_main:
        main_notes = st.text_area(
            "📝 Main Lecture Notes / Script", 
            height=150, 
            placeholder="Type core concepts, examples, and talking points..."
        )
        main_files = st.file_uploader(
            "📎 Upload Main Supporting Files (PPTs, PDFs)", 
            accept_multiple_files=True,
            key="main_files"
        )
        
    with tab_pre:
        pre_notes = st.text_area(
            "🌅 Pre-Class Instructions / Reading Notes", 
            height=150, 
            placeholder="What should students read or prepare before this hour?..."
        )
        pre_files = st.file_uploader(
            "📎 Upload Pre-Class Reading Materials (PDFs)", 
            accept_multiple_files=True,
            key="pre_files"
        )
        
    with tab_post:
        post_notes = st.text_area(
            "🌇 Post-Class Summary / Assignments", 
            height=150, 
            placeholder="Summarize the hour or provide follow-up assignment details..."
        )
        post_files = st.file_uploader(
            "📎 Upload Post-Class Assignments/Homework (PDFs)", 
            accept_multiple_files=True,
            key="post_files"
        )
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Save Button
    if st.button("Save All Content for this Hour", use_container_width=True):
        if module_name not in st.session_state.hourly_materials:
            st.session_state.hourly_materials[module_name] = {}
            
        st.session_state.hourly_materials[module_name][selected_hour] = {
            "main": {
                "notes": main_notes,
                "files": [{"name": f.name, "type": f.type, "bytes": f.getvalue()} for f in main_files]
            },
            "pre": {
                "notes": pre_notes,
                "files": [{"name": f.name, "type": f.type, "bytes": f.getvalue()} for f in pre_files]
            },
            "post": {
                "notes": post_notes,
                "files": [{"name": f.name, "type": f.type, "bytes": f.getvalue()} for f in post_files]
            }
        }
        st.success(f"✅ Main, Pre-Class, and Post-Class content saved successfully for '{selected_hour}' in {module_name}!")
        
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. REVIEW SAVED CONTENT
# -----------------------------------------------------------------------------
st.markdown("---")
with st.expander("Review Saved Hourly Materials (Session Overview)"):
    if not st.session_state.hourly_materials:
        st.info("No materials saved yet.")
    else:
        for mod_key, hours_dict in st.session_state.hourly_materials.items():
            st.markdown(f"**{mod_key}**")
            for hr_key, content in hours_dict.items():
                total_files = len(content['main']['files']) + len(content['pre']['files']) + len(content['post']['files'])
                st.write(f"- **{hr_key}**: {total_files} total files attached across all phases.")
