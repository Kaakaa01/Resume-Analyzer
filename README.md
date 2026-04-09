# AI Resume Analyzer

## Overview
**AI Resume Analyzer** is a Streamlit-based web application that allows users to upload their resumes (PDF or TXT) and receive automated feedback using AI. The tool analyzes the resume for content clarity, skills relevance, experience strength, ATS compatibility, and provides actionable recommendations for improvement.  

This project leverages **Groq AI** for natural language understanding and generates a **scored analysis** along with detailed feedback.

---

## Features
- Upload PDF or TXT resumes.
- Optional job role input for targeted feedback.
- AI-generated scores out of 10 for:
  - Overall Score
  - Content Quality
  - Skills Relevance
  - Experience Strength
  - ATS Compatibility
- Actionable feedback with rewritten bullet points.
- Optional raw AI response for transparency.
- Clean and interactive Streamlit UI.

---

## Demo
You can run the app locally using Streamlit:

```bash
streamlit run App.py
