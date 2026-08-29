EduPlatform: AI-Powered Faculty & Student Workspace
EduPlatform is an end-to-end educational operating system built with Streamlit, LangChain, and Groq. It automates the entire academic lifecycle: from parsing raw syllabus documents into structured JSON data, to dynamically generating RAG-backed lecture materials, and finally serving those materials to students via an interactive portal and an AI chatbot tutor.

System Architecture
The application operates on a centralized session-state memory, flowing sequentially through four primary modules.

1. Curriculum Extractor & Planner (pages/page1_app.py)
Role: The foundational ingestion engine.

Mechanism: Accepts raw unstructured syllabus files (PDF, DOCX) and pushes the text through a strict LLM Prompt Template using Groq (openai/gpt-oss-120b).

Output: Forces the LLM to output a heavily structured JSON schema containing course metadata, Course/Program Outcomes (CO/PO), resource links, and a strict 5-module, hour-by-hour teaching plan.

2. Hourly Content & RAG Generator (pages/page2_app.py)
Role: The Faculty Authoring Environment.

Mechanism: Utilizes a 3-tier hierarchy (Subject ➔ Module ➔ Hour). Faculty can upload specific lecture presentations (.pptx), notes (.pdf, .docx), and external links (YouTube, Google Forms, external MCQs).

AI Integration: Implements an advanced RAG pipeline. It cleans uploaded documents, splits them using RecursiveCharacterTextSplitter, embeds them using HuggingFace (all-MiniLM-L6-v2), and stores them in a local FAISS Vector Database. The Groq LLM then queries this FAISS index to auto-generate deep lecture notes, pre-class reading guides, post-class summaries, and diagnostic MCQs perfectly grounded in the uploaded files.

3. Student Interactive Portal (pages/page3_app.py)
Role: The Student Consumption Dashboard.

Mechanism: Reads the nested dictionary created in Page 2. It dynamically renders native PDF viewers using streamlit-pdf-viewer, embedded YouTube video players, hyperlinked assignments, and downloadable files.

UI/UX: Hides MCQ answers inside toggleable expanders for self-assessment and structures the data strictly by Pre-Class, Main Lecture, and Post-Class phases.

4. AI Tutor Chatbot (pages/page4_app.py)
Role: Context-Isolated Student Assistant.

Mechanism: A conversational interface that forces memory isolation. Students select the exact hour and phase they are studying. The system compiles only the notes, assignments, and PDFs mapped to that specific hour, builds a highly localized FAISS vector store on the fly, and constrains the LLM to answer questions strictly based on that bounded context.

Technology Stack
Frontend & State Management: Streamlit (streamlit, streamlit-pdf-viewer)

LLM Orchestration: LangChain (langchain, langchain-core, langchain-groq)

RAG Pipeline:

Vector Store: FAISS (faiss-cpu, langchain-community)

Embeddings: HuggingFace (sentence-transformers)

Text Processing: langchain-text-splitters

Inference Engine: Groq API (Model: openai/gpt-oss-120b)

Document Parsing: pypdf, docx2txt, python-pptx

Installation & Setup
1. Clone the repository and navigate to the directory:

Bash
git clone <repository_url>
cd eduplatform
2. Install dependencies:

Bash
pip install -r requirements.txt
(Ensure faiss-cpu, langchain-text-splitters, and python-pptx are explicitly included in your requirements file).

3. Launch the application:

Bash
streamlit run app.py
Usage Flow
Launch App: Navigate to app.py to view the global system status.

Step 1 (Faculty): Open the Extractor, input your Groq API key, upload a raw syllabus, and click "Extract Sub Info". Review the generated JSON UI. Click "Commit Changes".

Step 2 (Faculty): Navigate to the Hourly Upload page. Select an hour, upload a PPT or PDF, and click "Auto-Generate Deep Lecture Notes". Review the AI-generated MCQs and summaries across the Pre/Main/Post tabs. Click "Commit Changes".

Step 3 (Student): Open the Student Portal to view the formatted PDFs, watch embedded videos, and take the hidden-answer MCQs.

Step 4 (Student): Open the AI Tutor, select the exact hour you are studying, click "Load Tutor Database" to vectorize the specific documents, and chat with the course material.
