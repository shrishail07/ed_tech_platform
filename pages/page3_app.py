import streamlit as st
import base64
import streamlit.components.v1 as components
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
# def display_pdf(pdf_bytes):
#     """Embeds the PDF directly into the Streamlit UI."""
#     base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
#     pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf" />'
#     st.markdown(pdf_display, unsafe_allow_html=True)


def display_pdf(pdf_bytes):
    """Embeds the PDF using a secure JS Blob to bypass Chrome's iframe restrictions."""
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0; padding:0; overflow:hidden;">
        <iframe id="pdf_viewer" style="width:100%; height:600px; border:none;" src=""></iframe>
        <script>
            // Fetch the base64 string and convert it to a secure Blob URL natively
            fetch('data:application/pdf;base64,{base64_pdf}')
            .then(res => res.blob())
            .then(blob => {{
                const url = URL.createObjectURL(blob);
                document.getElementById('pdf_viewer').src = url;
            }});
        </script>
    </body>
    </html>
    """
    
    # Render the HTML component in Streamlit
    components.html(html_code, height=610)
    
def render_phase_content(phase_data):
    """Renders notes and files for a specific learning phase."""
    if not phase_data or (not phase_data.get("notes") and not phase_data.get("files")):
        st.info("No materials have been uploaded for this section yet.")
        return

    if phase_data.get("notes"):
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.write(phase_data["notes"])
        st.markdown('</div>', unsafe_allow_html=True)
        
    uploaded_files = phase_data.get("files", [])
    if uploaded_files:
        st.markdown("#### 📎 Attached Documents")
        for file_data in uploaded_files:
            if file_data["type"] == "application/pdf" and "bytes" in file_data:
                with st.expander(f"View Document: {file_data['name']}", expanded=False):
                    display_pdf(file_data["bytes"])
            else:
                st.download_button(
                    label=f"Download {file_data['name']}",
                    data=file_data.get("bytes", b""),
                    file_name=file_data["name"]
                )

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
st.caption("Select your module and current teaching hour to access your full learning journey.")

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
faculty_uploads = st.session_state.get("hourly_materials", {}).get(module_name, {}).get(selected_hour, {})

tab_pre, tab_main, tab_post, tab_global = st.tabs([
    "🌅 Pre-Class", 
    "🎓 Main Lecture", 
    "🌇 Post-Class", 
    "🔗 Global Resources"
])

with tab_pre:
    st.subheader(f"Pre-Class Preparation: {selected_hour}")
    render_phase_content(faculty_uploads.get("pre", {}))

with tab_main:
    st.subheader(f"Main Lecture Materials: {selected_hour}")
    render_phase_content(faculty_uploads.get("main", {}))

with tab_post:
    st.subheader(f"Post-Class Review: {selected_hour}")
    render_phase_content(faculty_uploads.get("post", {}))

with tab_global:
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
