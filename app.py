import streamlit as st
import pandas as pd
import time

# ==========================================
# 1. SESSION STATE INITIALIZATION
# ==========================================
# Replacing MongoDB by storing all data in the UI session state
if "app_state" not in st.session_state:
    st.session_state.app_state = {
        "faculty_data": {
            "college_name": "",
            "university_name": "",
            "syllabus_pdf": None,
            "metadata": None,
            "temporal_plan": None,
            "pre_class_notes": "AI-generated notes will appear here...",
            "supplementary_materials": []
        },
        "student_data": {
            "mcqs": [],
            "responses": {},
            "score": None,
            "chat_history": []
        }
    }

st.set_page_config(layout="wide", page_title="AI Learning Platform POC")

# ==========================================
# 2. MOCK AI & LANGCHAIN PLACEHOLDERS
# ==========================================
def extract_syllabus_metadata(pdf_file):
    """Placeholder for PyPDF / LangChain Document Loader extraction."""
    time.sleep(1) # Simulate processing
    return {
        "subject_name": "Advanced Data Structures",
        "subject_code": "CS402",
        "total_modules": 5,
        "sub_modules_per_module": 3
    }

def generate_temporal_plan():
    """Placeholder for AI logical structuring."""
    return {
        "Module 1": {"estimated_time": "3 hours", "sub_modules": ["Sub-module 1", "Sub-module 2", "Sub-module 3"]},
        "Module 2": {"estimated_time": "2 hours 30 mins", "sub_modules": ["Sub-module 1", "Sub-module 2", "Sub-module 3"]}
    }

def generate_mcqs():
    """Placeholder for stateful MCQ generation based on notes."""
    return [
        {"id": "q1", "question": "What is the primary advantage of a Hash Table?", "options": ["A) Fast access", "B) Ordered data", "C) Memory efficiency", "D) None of the above"], "answer": "A) Fast access"},
        {"id": "q2", "question": "Which time complexity represents binary search?", "options": ["A) O(n)", "B) O(log n)", "C) O(n^2)", "D) O(1)"], "answer": "B) O(log n)"}
    ]

def invoke_rag_agent(query):
    """Placeholder for LangGraph/LangChain RAG pipeline answering student queries."""
    time.sleep(1)
    return f"Based on the pre-class notes and uploaded context, here is the answer to: '{query}'."

# ==========================================
# 3. FACULTY PORTAL
# ==========================================
def faculty_portal():
    st.header("👨‍🏫 Faculty Portal")
    st.divider()
    
    # Step 1: Data Ingestion
    st.subheader("Step 1: Data Ingestion")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.app_state["faculty_data"]["college_name"] = st.text_input("College Name", value=st.session_state.app_state["faculty_data"]["college_name"])
    with col2:
        st.session_state.app_state["faculty_data"]["university_name"] = st.text_input("University Name", value=st.session_state.app_state["faculty_data"]["university_name"])
    
    uploaded_syllabus = st.file_uploader("Upload Syllabus (PDF format)", type=["pdf"])
    if uploaded_syllabus:
        st.session_state.app_state["faculty_data"]["syllabus_pdf"] = uploaded_syllabus.name
        
        if st.button("Process Syllabus"):
            with st.spinner("AI is extracting syllabus metadata..."):
                st.session_state.app_state["faculty_data"]["metadata"] = extract_syllabus_metadata(uploaded_syllabus)
                st.session_state.app_state["faculty_data"]["temporal_plan"] = generate_temporal_plan()
            st.success("Syllabus processed successfully!")

    # Step 2 & 3: AI Syllabus Extraction & Temporal Organization
    if st.session_state.app_state["faculty_data"]["metadata"]:
        st.divider()
        st.subheader("Step 2 & 3: Extraction & Temporal Organization")
        m_data = st.session_state.app_state["faculty_data"]["metadata"]
        
        st.markdown(f"**Subject:** {m_data['subject_name']} ({m_data['subject_code']}) | **Total Modules:** {m_data['total_modules']}")
        
        t_plan = st.session_state.app_state["faculty_data"]["temporal_plan"]
        for mod, details in t_plan.items():
            with st.expander(f"{mod} (Estimated: {details['estimated_time']})"):
                for sm in details["sub_modules"]:
                    st.markdown(f"- {sm}")

    # Step 4: Content Generation & Management
    st.divider()
    st.subheader("Step 4: Content Generation & Management")
    
    st.markdown("**1. Auto-Generation & 2. Review & Modification**")
    edited_notes = st.text_area("Review and modify AI-generated pre-class notes:", 
                                value=st.session_state.app_state["faculty_data"]["pre_class_notes"], 
                                height=200)
    
    if st.button("Save Final Notes"):
        st.session_state.app_state["faculty_data"]["pre_class_notes"] = edited_notes
        st.success("Pre-class notes finalized and saved to memory!")

    st.markdown("**3. Augmentation (Supplementary Materials)**")
    supp_file = st.file_uploader("Upload Supplementary PDFs/Text", type=["pdf", "txt"], accept_multiple_files=True)
    supp_link = st.text_input("Add Web Link")
    if st.button("Add Materials"):
        if supp_file:
            for f in supp_file:
                st.session_state.app_state["faculty_data"]["supplementary_materials"].append(f.name)
        if supp_link:
            st.session_state.app_state["faculty_data"]["supplementary_materials"].append(supp_link)
        st.success("Materials appended to RAG vector knowledge base.")


# ==========================================
# 4. STUDENT PORTAL
# ==========================================
def student_portal():
    st.header("🎓 Student Portal")
    st.divider()

    # Step 1: Three-Column Layout
    col_learning, col_assessment, col_response = st.columns(3)

    # Column 1: Learning Interface
    with col_learning:
        st.subheader("Column 1: Learning Materials")
        st.info("Finalized Pre-Class Notes")
        st.write(st.session_state.app_state["faculty_data"]["pre_class_notes"])
        
        if st.session_state.app_state["faculty_data"]["supplementary_materials"]:
            st.markdown("**Supplementary Materials:**")
            for mat in st.session_state.app_state["faculty_data"]["supplementary_materials"]:
                st.write(f"- {mat}")

    # Column 2: Assessment Generation
    with col_assessment:
        st.subheader("Column 2: Assessments")
        if st.button("Generate MCQs from Notes"):
            with st.spinner("LangChain generating MCQs..."):
                st.session_state.app_state["student_data"]["mcqs"] = generate_mcqs()
        
        if st.session_state.app_state["student_data"]["mcqs"]:
            st.success("MCQs generated successfully!")
            for i, q in enumerate(st.session_state.app_state["student_data"]["mcqs"]):
                st.markdown(f"**Q{i+1}: {q['question']}**")
                for opt in q['options']:
                    st.write(opt)

    # Column 3: Student Response
    with col_response:
        st.subheader("Column 3: Submit Answers")
        if st.session_state.app_state["student_data"]["mcqs"]:
            with st.form("student_assessment_form"):
                responses = {}
                for q in st.session_state.app_state["student_data"]["mcqs"]:
                    responses[q['id']] = st.radio(f"Select answer for {q['id']}:", q['options'], key=f"radio_{q['id']}")
                
                submitted = st.form_submit_button("Submit Assessment")
                if submitted:
                    st.session_state.app_state["student_data"]["responses"] = responses
                    # Calculate Marks
                    correct = 0
                    for q in st.session_state.app_state["student_data"]["mcqs"]:
                        if responses[q['id']] == q['answer']:
                            correct += 1
                    st.session_state.app_state["student_data"]["score"] = f"{correct} / {len(st.session_state.app_state['student_data']['mcqs'])}"

    # Step 2: Instant Feedback
    if st.session_state.app_state["student_data"]["score"] is not None:
        st.divider()
        st.subheader("Instant Feedback")
        st.metric(label="Your Score", value=st.session_state.app_state["student_data"]["score"])

    # 4. Interactive AI Assistant (RAG System)
    st.divider()
    st.subheader("🤖 24/7 RAG Teaching Assistant")
    st.caption("Contextually aware of pre-class notes, faculty modifications, and supplementary materials.")
    
    # Render Chat History
    for message in st.session_state.app_state["student_data"]["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask a conceptual question based on the syllabus..."):
        st.session_state.app_state["student_data"]["chat_history"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = invoke_rag_agent(prompt)
            st.markdown(response)
        st.session_state.app_state["student_data"]["chat_history"].append({"role": "assistant", "content": response})


# ==========================================
# 5. MAIN APP ROUTING
# ==========================================
def main():
    st.sidebar.title("Navigation")
    portal_selection = st.sidebar.radio("Go to:", ["Faculty Portal", "Student Portal"])
    
    st.sidebar.divider()
    st.sidebar.info("Session State Active (No Database Connected)")

    if portal_selection == "Faculty Portal":
        faculty_portal()
    elif portal_selection == "Student Portal":
        student_portal()

if __name__ == "__main__":
    main()
