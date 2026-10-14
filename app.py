import streamlit as st
import PyPDF2
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Create Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------- UI --------------------

st.title("AI Resume Screening Agent")

st.write("Welcome to the Resume Screening Agent")

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Enter Job Description"
)

analyze_button = st.button("Analyze Resume")

# -------------------- Backend --------------------

if analyze_button:

    if uploaded_file and job_description:

        # Read PDF
        reader = PyPDF2.PdfReader(uploaded_file)

        resume_text = ""

        # Extract text from every page
        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        st.success("✅ Resume uploaded successfully!")

        # Create Prompt
        prompt = f"""
You are an AI Resume Screening Assistant.

Compare the following resume with the given job description.

Job Description:
{job_description}

Resume:
{resume_text}

Provide:

1. Match Percentage
2. Skills Found
3. Missing Skills
4. Strengths
5. Weaknesses
6. Final Recommendation
"""

        # Gemini Response
        response = model.generate_content(prompt)

        # Display Result
        st.subheader("AI Resume Analysis")
        st.write(response.text)

    else:
        st.warning("⚠️ Please upload a resume and enter the job description.")