# AI Summarizer and Analyzer

## Project Overview

This project is a command-line application designed to process long text (like a resume or document) and provide two core AI services:

1.  **Text Summarization:** Generates a concise, fixed-length summary.
2.  **Question-Answering (Stretch Goal):** Answers specific queries based _only_ on the provided text, demonstrating Retrieval-Augmented Generation (RAG) principles.

### Final Technology Stack

- **Language:** Python 3.10+
- **Core AI Service:** Gemini API (`google-genai` SDK)
- **Environment:** Python Virtual Environment (`venv`)

---

## 🚀 Setup and Installation

Follow these steps to set up the project locally and run the application.

### 1. Prerequisites

You must have a Gemini API Key. You can obtain one from the Google AI Studio documentation.

### 2. Create and Activate Virtual Environment

Navigate to the project root directory and execute these commands:

```bash
# 1. Create the virtual environment
python -m venv .venv

# 2. Activate the environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Your prompt should now start with '(.venv)'
```
