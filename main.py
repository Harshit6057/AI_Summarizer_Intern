import os
import sys
from google import genai
from google.genai import types

# --- Configuration ---
MODEL_NAME = 'gemini-2.5-flash' 
API_KEY_VARIABLE = 'GEMINI_API_KEY'

def initialize_client():
    """Initializes the Gemini client and checks for the API key."""
    api_key = os.getenv(API_KEY_VARIABLE)
    if not api_key:
        print(f"FATAL ERROR: The {API_KEY_VARIABLE} environment variable is not set.")
        print("Please set your API key in the terminal before running the script.")
        sys.exit(1) # Exit the program if the key is missing
    
    return genai.Client(api_key=api_key)

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
    except Exception as e:
        return f"An API error occurred: {e}"

def summarize_text(text_to_process, client):
    """Generates a 3-sentence summary of the provided text."""
    
    # Prompt for Summarization
    prompt = (
        "You are an expert summarizer. Take the following text, which appears to be a resume, "
        "and summarize the candidate's key skills, top projects, and major achievements into "
        "exactly three clear, concise sentences. Do not add any introduction or concluding remarks."
        f"\n\n--- TEXT TO SUMMARIZE ---\n{text_to_process}"
    )
    
    print("\n--- Generating 3-Sentence Summary ---")
    return call_gemini_api(prompt, client)

def answer_question(text_to_process, question, client):
    """Answers a question based ONLY on the provided text (Question-Answering)."""

    # Prompt for Question-Answering
    prompt = (
        "You are an expert question-answering system. Based *only* on the text provided below, "
        f"answer the following question: **{question}**.\n"
        "If the answer is not present in the text, you must respond ONLY with: 'I cannot find the answer in the provided text.' "
        "Keep your answer concise and direct."
        f"\n\n--- TEXT TO CONSULT ---\n{text_to_process}"
    )

    print(f"\n--- Answering Question: '{question}' ---")
    return call_gemini_api(prompt, client)


def main():
    """Main function to handle user interaction and feature selection."""
    
    client = initialize_client()
    
    # The default text (the resume content)
    example_text = (
        "EducationPunjab Engineering College (Deemed to be University) Aug 2023 – June 2027B.Tech in Computer Science and Engineering (Data Science Specialization), CGPA: 7.81 Chandigarh, IndiaHindu Vidyapeeth School 2022 – 2023Senior Secondary Education (PCM), 90.2% Sonipat, HaryanaSkills• Programming & Tools: Python, C++, SQL, Git, GitHub, R, HTML, CSS• Frameworks & Libraries: NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, TensorFlow, PyTorch• Data Analytics & Visualization: Excel, Tableau, Power BI• Software Engineering: Object-Oriented Design, System Design, Agile/Scrum, Software Development Life Cycle (SDLC)• Machine Learning & NLP: Supervised/Unsupervised Learning, ANN, CNN, RNN, LSTM• Human-Centered Design: User Research, Usability Testing• Academic Concepts: Operating Systems, DBMS, Data Structures & Algorithms• Soft Skills: Collaboration, Communication, Problem-Solving, Project ManagementLicenses & CertificationsSupervised Machine Learning: Regression and Classification (Coursera) Jan 2025Instructor: Andrew Ng Credential ID: 4APWRRHF7D9YAchievements• Solved 200+ Data Structures and Algorithms problems on LeetCode and GeeksforGeeks, covering Arrays, Recursion,DP, Hashing, and Graphs.ProjectsBook Recommender System (Python, Flask, ML)– Engineered a recommendation engine using collaborative filtering, cosine similarity, and ML pipelines on 2M+ ratingsdataset.– Deployed via Flask REST API with responsive UI, enabling real-time customer-facing features.– Optimized preprocessing (pandas, NumPy) to reduce latency by 25% and improve scalability.AI Chatbot with LLM Integration– Built a multi-turn GenAI workflow using LangGraph and Groq’s LLaMA-3 for real-time Q&A and agentic workflows.– Designed session persistence, API integrations, and transformer-based NLP for dialogue management.– Deployed on Streamlit with modern UI, achieving 90% response accuracy on benchmark queries.Personalized Email Automation Tool– Automated ATS-friendly email generation using Gemini Pro, LangChain, and Gmail API, reducing manual effort by80%.– Implemented structured metadata logging and pipeline monitoring, achieving 95%+ reliability in workflow execution.– Enhanced job outreach automation through prompt engineering and NLP-driven content generation, improving responserates by 50%.Positions of ResponsibilityOrganising Committee Member – Treasure Hunt, PECFEST 2024 Nov 2024Student Counselling Cell, PEC Chandigarh, India∗ Collaborated in planning and execution of the flagship Treasure Hunt event at PECFEST 2024.∗ Managed logistics and ensured engaging and inclusive participation experience.Subhead – Publicity Committee, PECFEST 2024 Feb 2025Punjab Engineering College Chandigarh, India∗ Led publicity campaigns and strategic promotions for PECFEST 2024.∗ Coordinated cross-team communication and contributed to media content for campus-wide outreach.")
    
    print("\n\n#################################################")
    print("Welcome to the Gemini-Powered Resume Analyzer!")
    print("#################################################")
    
    # Get the text to process
    user_input = input(
        f"Paste the text you want to analyze, or press ENTER to use the default resume example:\n\n"
    )
    text_to_process = user_input.strip() if user_input.strip() else example_text

    if not user_input.strip():
        print(f"\n--- Processing Default Resume Text ---")

    while True:
        print("\nWhat would you like to do?")
        choice = input("Enter 'S' for Summarize, 'Q' for Ask a Question, or 'E' to Exit: ").strip().upper()
        
        if choice == 'S':
            result = summarize_text(text_to_process, client)
            print("\n\n** SUMMARY RESULT **")
            print("-" * 20)
            print(result)
            print("-" * 20)
            
        elif choice == 'Q':
            question = input("What question do you have about this text? (e.g., 'What is their graduation year?')\nQuestion: ").strip()
            if question:
                result = answer_question(text_to_process, question, client)
                print("\n\n** Q&A RESULT **")
                print("-" * 20)
                print(result)
                print("-" * 20)
            else:
                print("Question cannot be empty.")
                
        elif choice == 'E':
            print("Exiting application. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 'S', 'Q', or 'E'.")


if __name__ == "__main__":
    main()