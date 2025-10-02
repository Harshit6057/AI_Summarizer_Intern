import os
from google import genai
from google.genai import types

# --- Configuration ---
# Use the fast, capable model for text tasks
MODEL_NAME = 'gemini-2.5-flash' 
# API Key is read from environment variable for security
API_KEY_VARIABLE = 'GEMINI_API_KEY'

def summarize_text_with_api(text_to_summarize):
    """Summarizes text using the Gemini API based on a specific prompt."""
    
    # Check for API Key first
    api_key = os.getenv(API_KEY_VARIABLE)
    if not api_key:
        return f"Error: The {API_KEY_VARIABLE} environment variable is not set."

    try:
        # Initialize the client
        client = genai.Client(api_key=api_key)

        # The core instruction for the AI: the Prompt
        prompt = (
            "You are an expert summarizer. Take the following text, which appears to be a resume, "
            "and summarize the candidate's key skills, top projects, and major achievements into "
            "exactly three clear, concise sentences. Do not add any introduction or concluding remarks."
            f"\n\n--- TEXT TO SUMMARIZE ---\n{text_to_summarize}"
        )
        
        # Send the request to the Gemini API
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1 # Keep the summary focused and less creative
            )
        )
        
        # The result is in response.text
        return response.text
        
    except Exception as e:
        return f"An API error occurred: {e}"

def main():
    """Main function to handle user interaction."""
    print("Welcome to the Gemini API Text Summarizer!")
    print("-" * 35)
    
    # A default text example (the resume content you used before)
    example_text = (
        "EducationPunjab Engineering College (Deemed to be University) Aug 2023 – June 2027B.Tech in Computer Science and Engineering (Data Science Specialization), CGPA: 7.81 Chandigarh, IndiaHindu Vidyapeeth School 2022 – 2023Senior Secondary Education (PCM), 90.2% Sonipat, HaryanaSkills• Programming & Tools: Python, C++, SQL, Git, GitHub, R, HTML, CSS• Frameworks & Libraries: NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, TensorFlow, PyTorch• Data Analytics & Visualization: Excel, Tableau, Power BI• Software Engineering: Object-Oriented Design, System Design, Agile/Scrum, Software Development Life Cycle (SDLC)• Machine Learning & NLP: Supervised/Unsupervised Learning, ANN, CNN, RNN, LSTM• Human-Centered Design: User Research, Usability Testing• Academic Concepts: Operating Systems, DBMS, Data Structures & Algorithms• Soft Skills: Collaboration, Communication, Problem-Solving, Project ManagementLicenses & CertificationsSupervised Machine Learning: Regression and Classification (Coursera) Jan 2025Instructor: Andrew Ng Credential ID: 4APWRRHF7D9YAchievements• Solved 200+ Data Structures and Algorithms problems on LeetCode and GeeksforGeeks, covering Arrays, Recursion,DP, Hashing, and Graphs.ProjectsBook Recommender System (Python, Flask, ML)– Engineered a recommendation engine using collaborative filtering, cosine similarity, and ML pipelines on 2M+ ratingsdataset.– Deployed via Flask REST API with responsive UI, enabling real-time customer-facing features.– Optimized preprocessing (pandas, NumPy) to reduce latency by 25% and improve scalability.AI Chatbot with LLM Integration– Built a multi-turn GenAI workflow using LangGraph and Groq’s LLaMA-3 for real-time Q&A and agentic workflows.– Designed session persistence, API integrations, and transformer-based NLP for dialogue management.– Deployed on Streamlit with modern UI, achieving 90% response accuracy on benchmark queries.Personalized Email Automation Tool– Automated ATS-friendly email generation using Gemini Pro, LangChain, and Gmail API, reducing manual effort by80%.– Implemented structured metadata logging and pipeline monitoring, achieving 95%+ reliability in workflow execution.– Enhanced job outreach automation through prompt engineering and NLP-driven content generation, improving responserates by 50%.Positions of ResponsibilityOrganising Committee Member – Treasure Hunt, PECFEST 2024 Nov 2024Student Counselling Cell, PEC Chandigarh, India∗ Collaborated in planning and execution of the flagship Treasure Hunt event at PECFEST 2024.∗ Managed logistics and ensured engaging and inclusive participation experience.Subhead – Publicity Committee, PECFEST 2024 Feb 2025Punjab Engineering College Chandigarh, India∗ Led publicity campaigns and strategic promotions for PECFEST 2024.∗ Coordinated cross-team communication and contributed to media content for campus-wide outreach.")
    
    # Ask the user for input
    user_input = input(
        f"Paste the text you want to summarize, or press ENTER to use the default resume example:\n\n"
    )
    
    text_to_process = user_input.strip() if user_input.strip() else example_text
    
    if not user_input.strip():
        print(f"\n--- Processing Default Resume Text ---")
    
    # Get the summary
    final_summary = summarize_text_with_api(text_to_process)

    # Output the result
    print("\n\n#################################################")
    print("** 3-SENTENCE SUMMARY (via Gemini API) **")
    print("#################################################")
    print(final_summary)
    print("#################################################")


if __name__ == "__main__":
    main()