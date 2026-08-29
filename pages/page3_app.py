
# import streamlit as st
# from streamlit_pdf_viewer import pdf_viewer

# # -----------------------------------------------------------------------------
# # 1. PAGE CONFIGURATION & STYLING
# # -----------------------------------------------------------------------------
# st.set_page_config(
#     page_title="Student Learning Portal",
#     page_icon="👨‍🎓",
#     layout="wide"
# )

# st.markdown(
#     """
#     <style>
#     .main { background-color: #ffffff; color: #1f2937; }
#     .content-box {
#         background-color: #f8fafc;
#         padding: 20px;
#         border-radius: 8px;
#         border-top: 4px solid #10b981;
#         border-left: 1px solid #e2e8f0;
#         border-right: 1px solid #e2e8f0;
#         border-bottom: 1px solid #e2e8f0;
#         margin-bottom: 20px;
#     }
#     .resource-box {
#         background-color: #fffbeb;
#         padding: 20px;
#         border-radius: 8px;
#         border-top: 4px solid #f59e0b;
#         border-left: 1px solid #fde68a;
#         border-right: 1px solid #fde68a;
#         border-bottom: 1px solid #fde68a;
#         margin-bottom: 20px;
#     }
#     .mcq-box {
#         background-color: #f0fdf4;
#         padding: 20px;
#         border-radius: 8px;
#         border-left: 4px solid #22c55e;
#         margin-top: 20px;
#     }
#     .link-box {
#         background-color: #eff6ff;
#         padding: 15px;
#         border-radius: 8px;
#         border-left: 4px solid #3b82f6;
#         margin-bottom: 20px;
#     }
#     /* Style the download buttons to fit neatly next to expanders */
#     .stDownloadButton > button {
#         width: 100%;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # -----------------------------------------------------------------------------
# # 2. HELPER FUNCTIONS
# # -----------------------------------------------------------------------------
# def display_pdf(pdf_bytes):
#     """Renders the PDF using PDF.js to bypass Chrome's native iframe blocks."""
#     pdf_viewer(input=pdf_bytes, width=800, height=600)

# def render_file_list(files, title="📎 Attached Documents", key_prefix="dl"):
#     """Renders a list of files with View (if PDF) and Download buttons."""
#     if not files:
#         return
        
#     st.markdown(f"#### {title}")
#     for idx, file_data in enumerate(files):
#         c1, c2 = st.columns([4, 1])
#         with c1:
#             if file_data["type"] == "application/pdf" and "bytes" in file_data:
#                 with st.expander(f"📄 View Document: {file_data['name']}", expanded=False):
#                     display_pdf(file_data["bytes"])
#             else:
#                 st.markdown(f"📄 **{file_data['name']}** *(Preview not available for this file type)*")
#         with c2:
#             st.download_button(
#                 label="⬇️ Download",
#                 data=file_data.get("bytes", b""),
#                 file_name=file_data["name"],
#                 key=f"{key_prefix}_{idx}_{file_data['name']}"
#             )
#     st.markdown("<br/>", unsafe_allow_html=True)

# def render_mcqs(mcq_text):
#     """Parses raw AI MCQ text and hides the answers in an expander."""
#     if not mcq_text:
#         return
        
#     st.markdown('<div class="mcq-box">', unsafe_allow_html=True)
#     st.markdown("#### 🧠 Knowledge Check")
#     st.caption("Test your understanding before moving on.")
    
#     lines = mcq_text.split('\n')
#     current_q_block = []
    
#     for line in lines:
#         if "Correct Answer:" in line or "Correct Answer" in line:
#             st.write("  \n".join(current_q_block))
#             with st.expander("👀 View Answer & Explanation"):
#                 st.write(line)
#             st.markdown("---")
#             current_q_block = []
#         else:
#             if line.strip():
#                 current_q_block.append(line.strip())
                
#     if current_q_block and "".join(current_q_block).strip():
#         st.write("  \n".join(current_q_block))
        
#     st.markdown('</div>', unsafe_allow_html=True)

# def render_phase_content(phase_data, phase_name):
#     """Renders all materials mapped to a specific phase."""
#     if not phase_data or not any(phase_data.get(k) for k in ["notes", "files", "mcqs", "youtube_link", "google_form_link", "mcq_link", "class_assignment", "assignment_files"]):
#         st.info("No materials have been uploaded for this section yet.")
#         return

#     # 1. External Links & Video (YouTube, Google Forms, External MCQs)
#     yt_link = phase_data.get("youtube_link")
#     gf_link = phase_data.get("google_form_link")
#     mcq_link = phase_data.get("mcq_link")
    
#     if yt_link or gf_link or mcq_link:
#         st.markdown('<div class="link-box">', unsafe_allow_html=True)
        
#         if yt_link:
#             st.markdown("#### Youtube vedio link:")
#             try:
#                 st.video(yt_link)
#             except Exception:
#                 st.markdown(f"[{yt_link}]({yt_link})")
#             st.write("---")
            
#         if gf_link:
#             st.markdown("#### Google form Link:")
#             st.markdown(f"[{gf_link}]({gf_link})")
#             st.write("---")
            
#         if mcq_link:
#             st.markdown("#### Mcq link:")
#             st.markdown(f"[{mcq_link}]({mcq_link})")
            
#         st.markdown('</div>', unsafe_allow_html=True)

#     # 2. Main Text Notes
#     if phase_data.get("notes"):
#         st.markdown('<div class="content-box">', unsafe_allow_html=True)
#         st.write(phase_data["notes"])
#         st.markdown('</div>', unsafe_allow_html=True)
        
#     # 3. Downloadable Lecture Documents
#     render_file_list(phase_data.get("files", []), title="📎 Lecture Documents", key_prefix=f"doc_{phase_name}")

#     # 4. Class Assignments & Homework
#     assignment_text = phase_data.get("class_assignment")
#     assignment_files = phase_data.get("assignment_files", [])
    
#     if assignment_text or assignment_files:
#         st.markdown('<div class="resource-box">', unsafe_allow_html=True)
#         st.markdown("#### 📋 Class Assignment & Activities")
#         if assignment_text:
#             st.write(assignment_text)
#         if assignment_files:
#             st.markdown("<hr style='margin:10px 0px;'>", unsafe_allow_html=True)
#             render_file_list(assignment_files, title="📎 Assignment Files", key_prefix=f"assn_{phase_name}")
#         st.markdown('</div>', unsafe_allow_html=True)

#     # 5. AI Generated MCQs
#     if phase_data.get("mcqs"):
#         render_mcqs(phase_data["mcqs"])

# # -----------------------------------------------------------------------------
# # 3. STATE CHECKS
# # -----------------------------------------------------------------------------
# if "all_subjects_data" not in st.session_state or not st.session_state.all_subjects_data:
#     st.warning("⚠️ No course data available. Faculty must process a syllabus first.")
#     st.stop()

# # -----------------------------------------------------------------------------
# # 4. MAIN UI & NAVIGATION
# # -----------------------------------------------------------------------------
# st.title("👨‍🎓 Student Interactive Portal")
# st.caption("Select your Subject, Module, and current Teaching Hour to access your full learning journey.")

# col1, col2, col3 = st.columns(3)

# with col1:
#     subject_names = list(st.session_state.all_subjects_data.keys())
#     selected_subject = st.selectbox("1. Select Subject", options=subject_names)

# active_data = st.session_state.all_subjects_data[selected_subject]
# modules = active_data.get("modules", [])
# resources = active_data.get("resources", [])

# if not modules:
#     st.error("No modules found for this subject.")
#     st.stop()

# with col2:
#     module_options = {i: f"Module {mod.get('module_num', i+1)}" for i, mod in enumerate(modules)}
#     selected_mod_idx = st.selectbox(
#         "2. Select Module", 
#         options=list(module_options.keys()), 
#         format_func=lambda x: module_options[x]
#     )

# active_module = modules[selected_mod_idx]
# module_name = f"Module {active_module.get('module_num', selected_mod_idx+1)}"

# with col3:
#     raw_plan = active_module.get("hourly_plan", "")
#     parsed_hours = [hour.strip() for hour in raw_plan.split("\n") if hour.strip()]
#     if not parsed_hours:
#         parsed_hours = ["Fallback Hour 1"]

#     selected_hour = st.selectbox("3. Select Teaching Hour", options=parsed_hours)

# st.markdown("---")

# # -----------------------------------------------------------------------------
# # 5. CONTENT DISPLAY DASHBOARD
# # -----------------------------------------------------------------------------
# faculty_uploads = st.session_state.get("hourly_materials", {}).get(selected_subject, {}).get(module_name, {}).get(selected_hour, {})

# tab_pre, tab_main, tab_post, tab_global = st.tabs([
#     "🌅 Pre-Class Preparation", 
#     "🎓 Main Lecture Materials", 
#     "🌇 Post-Class Review", 
#     "🔗 Global Resources"
# ])

# with tab_pre:
#     st.subheader(f"Prepare for: {selected_hour}")
#     render_phase_content(faculty_uploads.get("pre", {}), "pre")

# with tab_main:
#     st.subheader(f"Lecture Content: {selected_hour}")
#     render_phase_content(faculty_uploads.get("main", {}), "main")

# with tab_post:
#     st.subheader(f"Review & Assess: {selected_hour}")
#     render_phase_content(faculty_uploads.get("post", {}), "post")

# with tab_global:
#     st.subheader("General Course References & Video Links")
#     st.caption(f"Extracted directly from the core syllabus for {selected_subject}.")
    
#     if not resources:
#         st.write("No general resources were found in the syllabus.")
#     else:
#         st.markdown('<div class="resource-box">', unsafe_allow_html=True)
#         for res in resources:
#             st.markdown(f"**📖 {res.get('name', 'Resource')}**")
#             st.markdown(f"- 📄 **Notes Link:** [{res.get('notes_link', 'Not Available')}]({res.get('notes_link', '#')})")
#             st.markdown(f"- 🎥 **Video Link:** [{res.get('video_link', 'Not Available')}]({res.get('video_link', '#')})")
#             st.write("---")
#         st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Student Learning Portal",
    page_icon="👨‍🎓",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main { background-color: #ffffff; color: #1f2937; }
    .content-box {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 8px;
        border-top: 4px solid #10b981;
        border-left: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    .resource-box {
        background-color: #fffbeb;
        padding: 20px;
        border-radius: 8px;
        border-top: 4px solid #f59e0b;
        border-left: 1px solid #fde68a;
        border-right: 1px solid #fde68a;
        border-bottom: 1px solid #fde68a;
        margin-bottom: 20px;
    }
    .mcq-box {
        background-color: #f0fdf4;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #22c55e;
        margin-top: 20px;
    }
    .link-box {
        background-color: #eff6ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 20px;
    }
    /* Style the download buttons to fit neatly next to expanders */
    .stDownloadButton > button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def display_pdf(pdf_bytes):
    """Renders the PDF using PDF.js to bypass Chrome's native iframe blocks."""
    pdf_viewer(input=pdf_bytes, width=800, height=600)

def render_file_list(files, title="📎 Attached Documents", key_prefix="dl"):
    """Renders a list of files with View (if PDF) and Download buttons."""
    if not files:
        return
        
    st.markdown(f"#### {title}")
    for idx, file_data in enumerate(files):
        c1, c2 = st.columns([4, 1])
        with c1:
            if file_data["type"] == "application/pdf" and "bytes" in file_data:
                with st.expander(f"📄 View Document: {file_data['name']}", expanded=False):
                    display_pdf(file_data["bytes"])
            else:
                st.markdown(f"📄 **{file_data['name']}** *(Preview not available for this file type)*")
        with c2:
            st.download_button(
                label="⬇️ Download",
                data=file_data.get("bytes", b""),
                file_name=file_data["name"],
                key=f"{key_prefix}_{idx}_{file_data['name']}"
            )
    st.markdown("<br/>", unsafe_allow_html=True)

def render_mcqs(mcq_text):
    """Parses raw AI MCQ text and hides the answers in an expander."""
    if not mcq_text:
        return
        
    st.markdown('<div class="mcq-box">', unsafe_allow_html=True)
    st.markdown("#### 🧠 Knowledge Check")
    st.caption("Test your understanding before moving on.")
    
    lines = mcq_text.split('\n')
    current_q_block = []
    
    for line in lines:
        if "Correct Answer:" in line or "Correct Answer" in line:
            st.write("  \n".join(current_q_block))
            with st.expander("👀 View Answer & Explanation"):
                st.write(line)
            st.markdown("---")
            current_q_block = []
        else:
            if line.strip():
                current_q_block.append(line.strip())
                
    if current_q_block and "".join(current_q_block).strip():
        st.write("  \n".join(current_q_block))
        
    st.markdown('</div>', unsafe_allow_html=True)

def render_phase_content(phase_data, phase_name):
    """Renders all materials mapped to a specific phase."""
    if not phase_data or not any(phase_data.get(k) for k in ["notes", "files", "mcqs", "youtube_link", "google_form_link", "mcq_link", "class_assignment", "assignment_files"]):
        st.info("No materials have been uploaded for this section yet.")
        return

    # 1. External Links & Video (YouTube, Google Forms, External MCQs)
    yt_link = phase_data.get("youtube_link")
    gf_link = phase_data.get("google_form_link")
    mcq_link = phase_data.get("mcq_link")
    
    if yt_link or gf_link or mcq_link:
        st.markdown('<div class="link-box">', unsafe_allow_html=True)
        
        if yt_link:
            st.markdown("#### Youtube vedio link:")
            try:
                st.video(yt_link)
            except Exception:
                st.markdown(f"[{yt_link}]({yt_link})")
            st.write("---")
            
        if gf_link:
            st.markdown("#### Google form Link:")
            st.markdown(f"[{gf_link}]({gf_link})")
            st.write("---")
            
        if mcq_link:
            st.markdown("#### Mcq link:")
            st.markdown(f"[{mcq_link}]({mcq_link})")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. Main Text Notes
    if phase_data.get("notes"):
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.write(phase_data["notes"])
        st.markdown('</div>', unsafe_allow_html=True)
        
    # 3. Downloadable Documents (Applies dynamically to Pre, Main, and Post files)
    file_title = "📎 Lecture Documents" if phase_name == "main" else "📎 Attached Documents"
    render_file_list(phase_data.get("files", []), title=file_title, key_prefix=f"doc_{phase_name}")

    # 4. Class Assignments & Homework
    assignment_text = phase_data.get("class_assignment")
    assignment_files = phase_data.get("assignment_files", [])
    
    if assignment_text or assignment_files:
        st.markdown('<div class="resource-box">', unsafe_allow_html=True)
        st.markdown("#### 📋 Class Assignment & Activities")
        if assignment_text:
            st.write(assignment_text)
        if assignment_files:
            st.markdown("<hr style='margin:10px 0px;'>", unsafe_allow_html=True)
            render_file_list(assignment_files, title="📎 Assignment Files", key_prefix=f"assn_{phase_name}")
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. AI Generated MCQs
    if phase_data.get("mcqs"):
        render_mcqs(phase_data["mcqs"])

# -----------------------------------------------------------------------------
# 3. STATE CHECKS
# -----------------------------------------------------------------------------
if "all_subjects_data" not in st.session_state or not st.session_state.all_subjects_data:
    st.warning("⚠️ No course data available. Faculty must process a syllabus first.")
    st.stop()

# -----------------------------------------------------------------------------
# 4. MAIN UI & NAVIGATION
# -----------------------------------------------------------------------------
st.title("👨‍🎓 Student Interactive Portal")
st.caption("Select your Subject, Module, and current Teaching Hour to access your full learning journey.")

col1, col2, col3 = st.columns(3)

with col1:
    subject_names = list(st.session_state.all_subjects_data.keys())
    selected_subject = st.selectbox("1. Select Subject", options=subject_names)

active_data = st.session_state.all_subjects_data[selected_subject]
modules = active_data.get("modules", [])
resources = active_data.get("resources", [])

if not modules:
    st.error("No modules found for this subject.")
    st.stop()

with col2:
    module_options = {i: f"Module {mod.get('module_num', i+1)}" for i, mod in enumerate(modules)}
    selected_mod_idx = st.selectbox(
        "2. Select Module", 
        options=list(module_options.keys()), 
        format_func=lambda x: module_options[x]
    )

active_module = modules[selected_mod_idx]
module_name = f"Module {active_module.get('module_num', selected_mod_idx+1)}"

with col3:
    raw_plan = active_module.get("hourly_plan", "")
    parsed_hours = [hour.strip() for hour in raw_plan.split("\n") if hour.strip()]
    if not parsed_hours:
        parsed_hours = ["Fallback Hour 1"]

    selected_hour = st.selectbox("3. Select Teaching Hour", options=parsed_hours)

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. CONTENT DISPLAY DASHBOARD
# -----------------------------------------------------------------------------
faculty_uploads = st.session_state.get("hourly_materials", {}).get(selected_subject, {}).get(module_name, {}).get(selected_hour, {})

tab_pre, tab_main, tab_post, tab_global = st.tabs([
    "🌅 Pre-Class Preparation", 
    "🎓 Main Lecture Materials", 
    "🌇 Post-Class Review", 
    "🔗 Global Resources"
])

# Renders the exact same structured content boxes for all 3 phases
with tab_pre:
    st.subheader(f"Prepare for: {selected_hour}")
    render_phase_content(faculty_uploads.get("pre", {}), "pre")

with tab_main:
    st.subheader(f"Lecture Content: {selected_hour}")
    render_phase_content(faculty_uploads.get("main", {}), "main")

with tab_post:
    st.subheader(f"Review & Assess: {selected_hour}")
    render_phase_content(faculty_uploads.get("post", {}), "post")

with tab_global:
    st.subheader("General Course References & Video Links")
    st.caption(f"Extracted directly from the core syllabus for {selected_subject}.")
    
    if not resources:
        st.write("No general resources were found in the syllabus.")
    else:
        st.markdown('<div class="resource-box">', unsafe_allow_html=True)
        for res in resources:
            st.markdown(f"**📖 {res.get('name', 'Resource')}**")
            st.markdown(f"- 📄 **Notes Link:** [{res.get('notes_link', 'Not Available')}]({res.get('notes_link', '#')})")
            st.markdown(f"- 🎥 **Video Link:** [{res.get('video_link', 'Not Available')}]({res.get('video_link', '#')})")
            st.write("---")
        st.markdown('</div>', unsafe_allow_html=True)
