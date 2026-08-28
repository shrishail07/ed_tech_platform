import streamlit as st
import base64

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
    .main { background-color: #0e1117; color: #fafafa; }
    .content-box {
        background-color: #1e1e2e;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #10b981;
        margin-bottom: 20px;
    }
    .resource-box {
        background-color: #1e1e2e;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #f59e0b;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def display_pdf(pdf_bytes):
    """Embeds the PDF directly into the Streamlit UI."""
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf" />'
    st.markdown(pdf_display, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. STATE CHECKS
# -----------------------------------------------------------------------------
if "extracted_data" not in st.session_state or not st.session_state.extracted_data:
    st.warning("⚠️ No course data available. Faculty must process a syllabus first.")
    st.stop()

# -----------------------------------------------------------------------------
# 4. MAIN UI & NAVIGATION
# -----------------------------------------------------------------------------
st.title("👨‍🎓 Student Interactive Portal")
st.caption("Select your module and current teaching hour to access lecture materials and reference links.")

data = st.session_state.extracted_data
modules = data.get("modules", [])
resources = data.get("resources", [])

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
        parsed_hours = ["Fallback Hour 1"]

    selected_hour = st.selectbox("2. Select Teaching Hour", options=parsed_hours)

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. CONTENT DISPLAY DASHBOARD
# -----------------------------------------------------------------------------
tab1, tab2 = st.tabs(["📚 Hourly Lecture Content", "🔗 Global Course Resources (Page 1)"])

# TAB 1: Faculty Uploads from Page 2
with tab1:
    st.subheader(f"Lecture Materials: {module_name} ➔ {selected_hour}")
    
    # Safely fetch the data saved by the faculty in Page 2
    faculty_uploads = st.session_state.get("hourly_materials", {}).get(module_name, {}).get(selected_hour, None)
    
    if not faculty_uploads:
        st.info("No specific materials have been uploaded by the faculty for this hour yet.")
    else:
        # Display Faculty Notes
        if faculty_uploads.get("notes"):
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown("#### 📝 Faculty Lecture Notes")
            st.write(faculty_uploads["notes"])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display Uploaded PDFs
        uploaded_files = faculty_uploads.get("files", [])
        if uploaded_files:
            st.markdown("#### 📎 Attached Documents")
            for file_data in uploaded_files:
                if file_data["type"] == "application/pdf" and "bytes" in file_data:
                    with st.expander(f"View Document: {file_data['name']}", expanded=True):
                        display_pdf(file_data["bytes"])
                else:
                    st.download_button(
                        label=f"Download {file_data['name']}",
                        data=file_data.get("bytes", b""),
                        file_name=file_data["name"]
                    )

# TAB 2: Extracted Global Resources from Page 1
with tab2:
    st.subheader("General Course References & Video Links")
    st.caption("Extracted directly from the core syllabus.")
    
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
