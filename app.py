import io
import streamlit as st
from pypdf import PdfReader

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Syllabus & Interactive Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { border-radius: 8px; font-weight: 600; }
    .metric-card {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .notes-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #2563eb;
        height: 520px;
        overflow-y: auto;
    }
    .mcq-card {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. SESSION STATE INITIALIZATION (In-Memory Database)
# -----------------------------------------------------------------------------
if "faculty_data" not in st.session_state:
    st.session_state.faculty_data = {
        "college_name": "",
        "university_name": "",
        "raw_text": "",
        "extracted_meta": None,
        "modules": [],
        "supplementary": [],
    }

if "student_responses" not in st.session_state:
    st.session_state.student_responses = {}

if "submission_result" not in st.session_state:
    st.session_state.submission_result = None

if "rag_chat_history" not in st.session_state:
    st.session_state.rag_chat_history = []


# -----------------------------------------------------------------------------
# 3. HELPER FUNCTIONS: PDF EXTRACTION & MOCK LLM ENGINE
# -----------------------------------------------------------------------------
def extract_pdf_text(uploaded_file) -> str:
    """Extracts raw text from an uploaded PDF syllabus."""
    pdf_reader = PdfReader(uploaded_file)
    extracted = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            extracted += text + "\n"
    return extracted


def extract_syllabus_structure(raw_text: str, college: str, uni: str):
    """Parses syllabus text and establishes modules, submodules, and temporal hours."""
    # Standard mock AI extraction structure (replace with LangChain/LLM calls as needed)
    return {
        "subject_name": "Artificial Intelligence & Machine Learning",
        "subject_code": "21CS71",
        "total_modules": 3,
        "modules": [
            {
                "id": 1,
                "title": "Module 1: Foundations of Search Algorithms",
                "estimated_hours": "3 Hours 30 Mins",
                "submodules": [
                    "Uninformed Search Strategies (BFS, DFS)",
                    "Informed Heuristic Search (A*, Greedy Best-First)",
                ],
                "notes": (
                    "### 1. Uninformed Search Strategies\n"
                    "Uninformed search algorithms explore search spaces without domain-specific heuristics.\n"
                    "- **Breadth-First Search (BFS):** Expands shallowest nodes first using a FIFO queue. Complete and optimal for unit step costs.\n"
                    "- **Depth-First Search (DFS):** Explores path to maximum depth using a LIFO queue. Space complexity is linear $O(bm)$.\n\n"
                    "### 2. Informed Search Strategies\n"
                    "- **A* Search:** Combines path cost $g(n)$ and heuristic estimate $h(n)$ with evaluation function $f(n) = g(n) + h(n)$."
                ),
                "mcqs": [
                    {
                        "id": "m1_q1",
                        "question": "What is the evaluation function for A* search?",
                        "options": ["f(n) = g(n) + h(n)", "f(n) = g(n) - h(n)", "f(n) = h(n)", "f(n) = max(g(n), h(n))"],
                        "answer": "f(n) = g(n) + h(n)",
                    },
                    {
                        "id": "m1_q2",
                        "question": "Which data structure is standard for Breadth-First Search (BFS)?",
                        "options": ["FIFO Queue", "LIFO Stack", "Priority Hash", "Binary Tree"],
                        "answer": "FIFO Queue",
                    },
                ],
            },
            {
                "id": 2,
                "title": "Module 2: Knowledge Representation & Logic",
                "estimated_hours": "2 Hours 45 Mins",
                "submodules": [
                    "Propositional Logic & Inference",
                    "First-Order Predicate Calculus",
                ],
                "notes": (
                    "### 1. Propositional Logic\n"
                    "Deals with declarative propositions that hold truth values (True/False).\n\n"
                    "### 2. First-Order Logic (FOL)\n"
                    "Extends propositional logic by introducing predicates, functions, objects, and quantifiers ($\forall, \exists$)."
                ),
                "mcqs": [
                    {
                        "id": "m2_q1",
                        "question": "Which quantifier denotes 'for all' in First-Order Logic?",
                        "options": ["Universal Quantifier (∀)", "Existential Quantifier (∃)", "Negation (¬)", "Conjunction (∧)"],
                        "answer": "Universal Quantifier (∀)",
                    }
                ],
            },
            {
                "id": 3,
                "title": "Module 3: Supervised Machine Learning",
                "estimated_hours": "4 Hours 15 Mins",
                "submodules": [
                    "Linear & Logistic Regression",
                    "Decision Trees & Ensemble Methods",
                ],
                "notes": (
                    "### 1. Regression Models\n"
                    "- **Linear Regression:** Models linear relationships between independent features and continuous targets.\n"
                    "- **Logistic Regression:** Models probabilities for classification via the sigmoid function.\n\n"
                    "### 2. Ensemble Learning\n"
                    "- Combines multiple base estimators (e.g., Random Forests, Gradient Boosting) to reduce variance and bias."
                ),
                "mcqs": [
                    {
                        "id": "m3_q1",
                        "question": "What activation function does standard binary Logistic Regression employ?",
                        "options": ["Sigmoid / Logistic", "ReLU", "Tanh", "Softmax"],
                        "answer": "Sigmoid / Logistic",
                    }
                ],
            },
        ],
    }


def query_rag_engine(question: str) -> str:
    """Mock RAG retrieval across notes and supplementary materials."""
    all_context = ""
    for mod in st.session_state.faculty_data.get("modules", []):
        all_context += f"\n--- {mod['title']} ---\n" + mod["notes"]
    for sup in st.session_state.faculty_data.get("supplementary", []):
        all_context += f"\n--- Supplementary Material ({sup['type']}) ---\n" + sup["content"]

    if not all_context.strip():
        return "No syllabus content has been ingested or published yet."

    q_lower = question.lower()
    if "a*" in q_lower or "heuristic" in q_lower:
        return "**[RAG Assistant]**: A* Search balances path cost $g(n)$ and heuristic cost $h(n)$ with $f(n) = g(n) + h(n)$. It ensures optimality when $h(n)$ is admissible."
    elif "bfs" in q_lower or "dfs" in q_lower:
        return "**[RAG Assistant]**: BFS utilizes a FIFO queue expanding level by level, whereas DFS utilizes a LIFO queue/stack reaching maximum depth first."
    elif "regression" in q_lower:
        return "**[RAG Assistant]**: Linear regression models continuous targets, while Logistic regression applies a sigmoid transformation to output probabilities for classification."
    else:
        return f"**[RAG Assistant]**: Based on the faculty-approved pre-class notes and supplementary materials, your query aligns with: *'{question}'*. Please review the finalized module notes in Column 1 for complete theoretical derivations."


# -----------------------------------------------------------------------------
# 4. SIDEBAR NAVIGATION & PORTAL ROUTING
# -----------------------------------------------------------------------------
st.sidebar.title("📚 EduPlatform POC")
portal_selection = st.sidebar.radio("Navigate Portals", ["🏛️ Faculty Portal", "👨‍🎓 Student Portal"])

st.sidebar.markdown("---")
st.sidebar.subheader("System Status")
if st.session_state.faculty_data["extracted_meta"]:
    st.sidebar.success(f"Loaded: {st.session_state.faculty_data['extracted_meta']['subject_name']}")
    st.sidebar.caption(f"Code: {st.session_state.faculty_data['extracted_meta']['subject_code']}")
    st.sidebar.caption(f"Modules: {len(st.session_state.faculty_data['modules'])}")
else:
    st.sidebar.info("Awaiting syllabus ingestion in Faculty Portal.")


# -----------------------------------------------------------------------------
# 5. FACULTY PORTAL WORKFLOW
# -----------------------------------------------------------------------------
if portal_selection == "🏛️ Faculty Portal":
    st.title("Faculty Curriculum & Content Management")
    st.caption("Ingest syllabus PDFs, inspect AI-extracted metadata, manage pre-class notes, and augment materials.")

    tab1, tab2, tab3 = st.tabs(["1. Data Ingestion & Extraction", "2. Notes Management", "3. Supplementary Augmentation"])

    # TAB 1: Ingestion & Extraction
    with tab1:
        st.subheader("Step 1 & 2: Course Details & Syllabus Ingestion")
        c1, c2 = st.columns(2)
        with c1:
            college_input = st.text_input("College Name", value=st.session_state.faculty_data["college_name"] or "PES University")
            uni_input = st.text_input("University Name", value=st.session_state.faculty_data["university_name"] or "Autonomous / State Board")
        with c2:
            uploaded_pdf = st.file_uploader("Upload Syllabus Document (PDF)", type=["pdf"])

        if st.button("Extract Syllabus & Structure Modules", type="primary"):
            if uploaded_pdf is not None or college_input:
                raw_text = extract_pdf_text(uploaded_pdf) if uploaded_pdf else "Sample Syllabus Text"
                extracted = extract_syllabus_structure(raw_text, college_input, uni_input)

                st.session_state.faculty_data["college_name"] = college_input
                st.session_state.faculty_data["university_name"] = uni_input
                st.session_state.faculty_data["raw_text"] = raw_text
                st.session_state.faculty_data["extracted_meta"] = {
                    "subject_name": extracted["subject_name"],
                    "subject_code": extracted["subject_code"],
                    "total_modules": extracted["total_modules"],
                }
                st.session_state.faculty_data["modules"] = extracted["modules"]
                st.success("Syllabus processed and modules extracted successfully!")
            else:
                st.error("Please provide course details or upload a PDF file.")

        if st.session_state.faculty_data["extracted_meta"]:
            st.markdown("---")
            st.subheader("Step 3: Temporal Organization & Extracted Metadata")
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

    # TAB 2: Notes Review & Modification
    with tab2:
        st.subheader("Step 4: Auto-Generated Pre-Class Notes Review")
        if not st.session_state.faculty_data["modules"]:
            st.warning("Please ingest a syllabus in Tab 1 first.")
        else:
            selected_mod_idx = st.selectbox(
                "Select Module to Review & Edit:",
                range(len(st.session_state.faculty_data["modules"])),
                format_func=lambda i: st.session_state.faculty_data["modules"][i]["title"],
            )

            current_mod = st.session_state.faculty_data["modules"][selected_mod_idx]
            st.info(f"Editing notes for: **{current_mod['title']}** (Time budget: {current_mod['estimated_hours']})")

            edited_notes = st.text_area(
                "Module Pre-Class Notes (Markdown supported):",
                value=current_mod["notes"],
                height=300,
            )

            if st.button("Save & Finalize Notes"):
                st.session_state.faculty_data["modules"][selected_mod_idx]["notes"] = edited_notes
                st.success("Pre-class notes updated and saved to session context!")

    # TAB 3: Augmentation
    with tab3:
        st.subheader("Step 4 (Augmentation): Supplementary Materials")
        st.caption("Upload web links, extra text snippets, or supplementary references to enrich the RAG knowledge base.")

        aug_type = st.radio("Material Type", ["Web Link / URL", "Reference Text Snippet"], horizontal=True)
        if aug_type == "Web Link / URL":
            link_input = st.text_input("Enter Resource URL")
            link_desc = st.text_input("Description / Topic")
            if st.button("Add URL to Knowledge Base"):
                if link_input:
                    st.session_state.faculty_data["supplementary"].append({
                        "type": "URL",
                        "content": f"URL: {link_input} | Description: {link_desc}",
                    })
                    st.success("Web resource indexed.")
        else:
            snippet_text = st.text_area("Paste Reference Text")
            if st.button("Add Text Snippet to Knowledge Base"):
                if snippet_text:
                    st.session_state.faculty_data["supplementary"].append({
                        "type": "Snippet",
                        "content": snippet_text,
                    })
                    st.success("Text snippet indexed.")

        if st.session_state.faculty_data["supplementary"]:
            st.markdown("#### Indexed Supplementary Items")
            for idx, item in enumerate(st.session_state.faculty_data["supplementary"], start=1):
                st.write(f"{idx}. `[{item['type']}]` {item['content']}")


# -----------------------------------------------------------------------------
# 6. STUDENT PORTAL WORKFLOW
# -----------------------------------------------------------------------------
elif portal_selection == "👨‍🎓 Student Portal":
    st.title("Student Interactive Learning & Assessment Dashboard")

    if not st.session_state.faculty_data["modules"]:
        st.info("No course content available. Please switch to the Faculty Portal to ingest a syllabus.")
    else:
        active_module_idx = st.selectbox(
            "Select Course Module:",
            range(len(st.session_state.faculty_data["modules"])),
            format_func=lambda i: st.session_state.faculty_data["modules"][i]["title"],
        )
        active_module = st.session_state.faculty_data["modules"][active_module_idx]

        st.markdown("---")

        # 3-COLUMN INTERACTIVE DASHBOARD
        col1, col2, col3 = st.columns([1.5, 1.2, 1.3], gap="medium")

        # COLUMN 1: LEARNING INTERFACE
        with col1:
            st.subheader("📖 Learning Notes")
            st.caption("Faculty-approved pre-class notes")
            st.markdown(
                f'<div class="notes-box">{active_module["notes"]}</div>',
                unsafe_allow_html=True,
            )

        # COLUMN 2: ASSESSMENT GENERATION (MCQ Display)
        with col2:
            st.subheader("📝 Dynamic MCQs")
            st.caption("Generated directly from notes")
            mcqs = active_module.get("mcqs", [])
            if not mcqs:
                st.write("No assessments generated for this module.")
            else:
                for idx, mcq in enumerate(mcqs, start=1):
                    st.markdown(
                        f"""
                        <div class="mcq-card">
                            <strong>Q{idx}: {mcq['question']}</strong><br/>
                            <small>A. {mcq['options'][0]}<br/>
                            B. {mcq['options'][1]}<br/>
                            C. {mcq['options'][2]}<br/>
                            D. {mcq['options'][3]}</small>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # COLUMN 3: STUDENT RESPONSE INTERFACE
        with col3:
            st.subheader("✍️ Your Responses")
            st.caption("Select your answers and submit")

            with st.form(key=f"mcq_form_{active_module_idx}"):
                user_answers = {}
                for idx, mcq in enumerate(mcqs, start=1):
                    chosen = st.radio(
                        f"Select Answer for Q{idx}:",
                        options=mcq["options"],
                        key=f"radio_{mcq['id']}",
                        index=None,
                    )
                    user_answers[mcq["id"]] = chosen

                submit_btn = st.form_submit_button("Submit Assessment", type="primary")

                if submit_btn:
                    total = len(mcqs)
                    correct_count = 0
                    detailed_feedback = []

                    for mcq in mcqs:
                        user_ans = user_answers.get(mcq["id"])
                        correct_ans = mcq["answer"]
                        is_correct = user_ans == correct_ans
                        if is_correct:
                            correct_count += 1
                        detailed_feedback.append({
                            "question": mcq["question"],
                            "selected": user_ans,
                            "correct": correct_ans,
                            "status": is_correct,
                        })

                    st.session_state.submission_result = {
                        "score": correct_count,
                        "total": total,
                        "percentage": (correct_count / total * 100) if total > 0 else 0,
                        "feedback": detailed_feedback,
                    }

        # ROW 2, COLUMN 2 / FEEDBACK AREA: INSTANT RESULTS DISPLAY
        if st.session_state.submission_result:
            st.markdown("---")
            st.subheader("🎯 Instant Assessment Feedback & Performance")
            res = st.session_state.submission_result

            fc1, fc2, fc3 = st.columns([1, 1, 2])
            fc1.metric("Calculated Marks", f"{res['score']} / {res['total']}")
            fc2.metric("Accuracy", f"{res['percentage']:.1f}%")
            with fc3:
                if res["percentage"] >= 80:
                    st.success("Excellent grasp of pre-class concepts!")
                elif res["percentage"] >= 50:
                    st.warning("Good attempt. Review the highlighted sections in the notes.")
                else:
                    st.error("Please revisit the pre-class notes and try again.")

            with st.expander("View Question-by-Question Breakdown", expanded=True):
                for item in res["feedback"]:
                    if item["status"]:
                        st.markdown(f"✅ **{item['question']}** — Correct (`{item['selected']}`)")
                    else:
                        st.markdown(f"❌ **{item['question']}** — Your Answer: `{item['selected']}` | Correct: `{item['correct']}`")

        # -------------------------------------------------------------------------
        # 4. 24/7 INTERACTIVE AI TEACHING ASSISTANT (RAG System)
        # -------------------------------------------------------------------------
        st.markdown("---")
        st.subheader("🤖 24/7 AI Teaching Assistant (Context-Aware RAG)")
        st.caption("Ask questions strictly grounded in the approved pre-class notes and supplementary materials.")

        for msg in st.session_state.rag_chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_query = st.chat_input("Ask a conceptual question about this module...")
        if user_query:
            st.session_state.rag_chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            assistant_reply = query_rag_engine(user_query)
            st.session_state.rag_chat_history.append({"role": "assistant", "content": assistant_reply})
            with st.chat_message("assistant"):
                st.markdown(assistant_reply)
