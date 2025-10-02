import streamlit as st
from google import genai
from google.genai import types
from google.genai import errors # Import the specific error class

# --- Configuration ---
MODEL_NAME = 'gemini-2.5-flash' 
DEFAULT_TEXT = """
EducationPunjab Engineering College (Deemed to be University) Aug 2023 – June 2027B.Tech in Computer Science and Engineering (Data Science Specialization), CGPA: 7.81 Chandigarh, IndiaHindu Vidyapeeth School 2022 – 2023Senior Secondary Education (PCM), 90.2% Sonipat, HaryanaSkills• Programming & Tools: Python, C++, SQL, Git, GitHub, R, HTML, CSS• Frameworks & Libraries: NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, TensorFlow, PyTorch• Data Analytics & Visualization: Excel, Tableau, Power BI• Software Engineering: Object-Oriented Design, System Design, Agile/Scrum, Software Development Life Cycle (SDLC)• Machine Learning & NLP: Supervised/Unsupervised Learning, ANN, CNN, RNN, LSTM• Human-Centered Design: User Research, Usability Testing• Academic Concepts: Operating Systems, DBMS, Data Structures & Algorithms• Soft Skills: Collaboration, Communication, Problem-Solving, Project ManagementLicenses & CertificationsSupervised Machine Learning: Regression and Classification (Coursera) Jan 2025Instructor: Andrew Ng Credential ID: 4APWRRHF7D9YAchievements• Solved 200+ Data Structures and Algorithms problems on LeetCode and GeeksforGeeks, covering Arrays, Recursion,DP, Hashing, and Graphs.ProjectsBook Recommender System (Python, Flask, ML)– Engineered a recommendation engine using collaborative filtering, cosine similarity, and ML pipelines on 2M+ ratingsdataset.– Deployed via Flask REST API with responsive UI, enabling real-time customer-facing features.– Optimized preprocessing (pandas, NumPy) to reduce latency by 25% and improve scalability.AI Chatbot with LLM Integration– Built a multi-turn GenAI workflow using LangGraph and Groq’s LLaMA-3 for real-time Q&A and agentic workflows.– Designed session persistence, API integrations, and transformer-based NLP for dialogue management.– Deployed on Streamlit with modern UI, achieving 90% response accuracy on benchmark queries.Personalized Email Automation Tool– Automated ATS-friendly email generation using Gemini Pro, LangChain, and Gmail API, reducing manual effort by80%.– Implemented structured metadata logging and pipeline monitoring, achieving 95%+ reliability in workflow execution.– Enhanced job outreach automation through prompt engineering and NLP-driven content generation, improving responserates by 50%.Positions of ResponsibilityOrganising Committee Member – Treasure Hunt, PECFEST 2024 Nov 2024Student Counselling Cell, PEC Chandigarh, India∗ Collaborated in planning and execution of the flagship Treasure Hunt event at PECFEST 2024.∗ Managed logistics and ensured engaging and inclusive participation experience.Subhead – Publicity Committee, PECFEST 2024 Feb 2025Punjab Engineering College Chandigarh, India∗ Led publicity campaigns and strategic promotions for PECFEST 2024.∗ Coordinated cross-team communication and contributed to media content for campus-wide outreach.
"""

# --- Gemini API Logic ---

def get_gemini_client():
    """Returns the initialized Gemini client or None if the key is missing."""
    if 'gemini_client' in st.session_state:
        return st.session_state.gemini_client
    
    # Check for the key in Streamlit's session state
    api_key = st.session_state.get('api_key')
    
    if api_key:
        try:
            # Attempt to create the client, which throws an error if the key is bad
            client = genai.Client(api_key=api_key)
            st.session_state.gemini_client = client
            return client
        except errors.APIError as e:
            # Catch the specific API error for invalid keys
            st.error(f"Initialization Failed: The API key provided is not valid. Please check and try again. ({e})")
            return None
        except Exception:
            # Catch other potential connection errors
            st.error("Invalid API Key or connection issue. Please check your key.")
            return None
    return None

def call_gemini_api(prompt, client):
    """Generic function to call the Gemini API with a specific prompt."""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1 # Low temp for factual, less creative output
            )
        )
        return response.text
    except errors.APIError as e:
        # Catch API errors during content generation and present a cleaner message
        return f"API Error during generation: {e.message}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def summarize_text(text_to_process, client):
    """Generates a 3-sentence summary of the provided text."""
    prompt = (
        "You are an expert summarizer. Take the following text, which appears to be a resume, "
        "and summarize the candidate's key skills, top projects, and major achievements into "
        "exactly three clear, concise sentences. Do not add any introduction or concluding remarks."
        f"\n\n--- TEXT TO SUMMARIZE ---\n{text_to_process}"
    )
    return call_gemini_api(prompt, client)

def answer_question(text_to_process, question, client):
    """Answers a question based ONLY on the provided text (Question-Answering)."""
    prompt = (
        "You are an expert question-answering system. Based *only* on the text provided below, "
        f"answer the following question: **{question}**.\n"
        "If the answer is not present in the text, you must respond ONLY with: 'I cannot find the answer in the provided text.' "
        "Keep your answer concise and direct."
        f"\n\n--- TEXT TO CONSULT ---\n{text_to_process}"
    )
    return call_gemini_api(prompt, client)

# --- Streamlit UI ---

st.set_page_config(
    page_title="Gemini AI Document Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📄 Gemini AI Document Analyzer")
st.caption("Summarization and Question-Answering powered by `gemini-2.5-flash`")

# --- 1. Sidebar for API Key Input ---

with st.sidebar:
    st.header("1. API Key Setup")
    
    # Text input for the API Key
    api_key_input = st.text_input(
        "Enter your Gemini API Key:", 
        type="password", 
        key="api_key_input",
        placeholder="Enter your key here...",
        value=st.session_state.get('api_key', '')
    )

    if api_key_input and api_key_input != st.session_state.get('api_key'):
        st.session_state.api_key = api_key_input
        # Clear client on key change
        if 'gemini_client' in st.session_state:
            del st.session_state.gemini_client
        st.rerun() 

    if st.session_state.get('api_key'):
        client = get_gemini_client()
        if client:
            st.success("API Key successfully set and client initialized!")
        else:
            # If initialization failed, we print a warning and ask the user to re-enter
            st.warning("API Key invalid or failed to initialize. Please check and re-enter.")
    else:
        st.info("Enter your key above to enable the app.")
        client = None

# --- Main Content: Text Input ---

st.header("2. Document Input")
text_to_process = st.text_area(
    "Paste the document text here:",
    height=300,
    value=DEFAULT_TEXT,
    key="document_text"
)

# --- Main Content: Features ---

st.header("3. AI Analysis")

if not client:
    st.warning("Please set a valid Gemini API Key in the sidebar to proceed with analysis.")
else:
    tab1, tab2 = st.tabs(["⚡ Summarize Document", "❓ Ask a Question (Q&A)"])

    # --- Tab 1: Summarization ---
    with tab1:
        st.subheader("Generate a Concise 3-Sentence Summary")
        
        if st.button("Generate Summary", use_container_width=True, type="primary"):
            if not text_to_process.strip():
                st.error("Please paste text into the document input area.")
            else:
                with st.spinner("Generating summary with Gemini..."):
                    summary = summarize_text(text_to_process, client)
                
                st.markdown("### ✅ Summary Result")
                st.info(summary)

    # --- Tab 2: Question-Answering ---
    with tab2:
        st.subheader("Get Factual Answers from the Document")
        
        qa_question = st.text_input(
            "Enter your question about the document:",
            placeholder="e.g., What is the candidate's highest educational degree?",
            key="qa_question"
        )
        
        if st.button("Get Answer", use_container_width=True, type="primary"):
            if not text_to_process.strip():
                st.error("Please paste text into the document input area.")
            elif not qa_question.strip():
                st.error("Please enter a question.")
            else:
                with st.spinner(f"Searching document for the answer to '{qa_question}'..."):
                    answer = answer_question(text_to_process, qa_question, client)
                
                st.markdown("### ✅ Q&A Result")
                st.info(answer)
