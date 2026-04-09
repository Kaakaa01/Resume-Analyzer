import streamlit as st
import PyPDF2
import io
import os
from groq import Groq    
# from openai import OpenAI
from dotenv import load_dotenv
import re

#Load environment variables
load_dotenv()

#Page configuration
st.set_page_config(page_title="Resume Analyzer", page_icon=":clipboard:", layout="centered")


#Custom UI Styling
st.markdown("""
<style>
.stButton button { background-color: #4CAF50; color: white; border-radius: 10px; height: 3em; width: 100%; font-size: 16px; }
.stProgress > div > div {background-color: #4CAF50;}
.score-card {padding: 10px; margin: 5px; border-radius: 10px; background-color: #f1f1f1; text-align: center;}
.high {background-color: #d4edda;}
.medium {background-color: #fff3cd;}
.low {background-color: #f8d7da;}
</style>
""", unsafe_allow_html=True)

#Title
st.title("Resume Review :clipboard:")
st.markdown("Upload your resume in PDF format, and get feedback on how to improve it!")

#API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#Upload file and job role
uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])

job_role = st.text_input("Enter the job role you are applying for (optional)")

analyze = st.button("Analyze Resume")

#Extract PDF text
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

#Extract file text
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

#Extract scores using regex
def extract_scores(text):
    score = {
        "Overall": 0,
        "Content": 0,
        "Skills": 0,
        "Experience": 0,
        "ATS": 0
    }
    patterns = {
        "Overall": r"Overall score.*?(\d+(?:\.\d+)?)",
        "Content": r"Content Quality.*?(\d+(?:\.\d+)?)",
        "Skills": r"Skills Relevance.*?(\d+(?:\.\d+)?)",
        "Experience": r"Experience Strength.*?(\d+(?:\.\d+)?)",
        "ATS": r"ATS Compatibility.*?(\d+(?:\.\d+)?)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            score[key] = float(match.group(1))
    
    return score

# Function to assign color class
def score_class(value):
    if value >= 8: return "high"
    elif value >=5: return "medium"
    else: return "low"

#Main logic
if analyze and uploaded_file:
    with st.spinner("Analyzing your resume..."):
        try:
            file_content = extract_text_from_file(uploaded_file)

            if not file_content.strip():
                st.error("File does not have any text content. Please upload a valid resume.")
                st.stop()

            prompt  = f"""
            You are an expert resume reviewer.

            Analyze the resume and provide: 

            ### Scores (out of 10)
                - Overall score
                - Content Quality
                - Skills Relevance
                - Experience Strength
                - ATS Compatibility
            ### Detailed Feedback
                1. Strengths
                2. Weakensses
                3. Missing Skills for {job_role if job_role else 'general roles'}
                4. Improvements (actionable suggestions)
            ### Bonus
            Rewrite 2 weak bullet points into strong action-based statemnts.

            Resume:
            {file_content}

            Keep the response structured and clear.
            """
            #Groq API call
            client = Groq(api_key=GROQ_API_KEY)


            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=900
            )

            result = response.choices[0].message.content
            #Extract scores
            score = extract_scores(result)
            st.success("Analysis completed!")

            #Display scores
            st.subheader("Resume Scores")

            for key, value in score.items():
                st.write(f"**{key} Score:** {value}/10")
                st.progress(value / 10)
            
            #Feedback
            st.subheader("Detailed Feedback")
            st.markdown(result)


            # Optional raw output
            if st.checkbox("Show raw AI response"):
                st.text(result)

        except Exception as e:
            st.error(f"An error occured: {str(e)}")




# if analyze and uploaded_file:
#     try:
#         file_content = extract_text_from_file(uploaded_file)

#         if not file_content.strip():
#             st.error("File does not have any text content. Please upload a valid resume.")
#             st.stop()

#         prompt  = f"""Please analyze this resume and provide constructive feedback.
#         Focus on the following aspects:
#         1. Content clarity and impact
#         2. Skills presentation
#         3. Experience descriptions
#         4. Specific improvements for {job_role if job_role else 'general job applications'}
        
#         Resume content:
#         {file_content}
        
#         Please provide your analysis in a clear, structured format with specific recommendations."""
        
#         client = OpenAI(api_key=OPENAI_API_KEY)
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.7,
#             max_tokens=1000
#         )
#         st.markdown("### Analysis Results")
#         st.markdown(response.choices[0].message.content)
    
#     except Exception as e:
#         st.error(f"An error occured: {str(e)}")