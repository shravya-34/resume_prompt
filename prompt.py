import os
import fitz  # PyMuPDF
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    doc.close()
    return text

pdf_path = r"D:/prompt/resume_prompt/pdf/shravya_resume.pdf"
resume_content = extract_text(pdf_path)


system_prompt = f''' 
    You are a bot and your task is to convert given Resume_Content to a structured json format. 
    The features you need to extract from Resume_Content and return in json format are - 
    name, mobile_number, email, education, experiences, skills and projects.

    Resume_Content from which you will get the information is provided below.

    Resume_Content - {resume_content}

    Ensure to return the answer in json format only and include all features by getting required content from
    Resume_Content provided. 
    If any feature is not there in Resume_Content then just add None value for that feature in json. 
'''


generation_config = {
  "temperature": 0,
  "max_output_tokens": 8192,
#   "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

response = model.generate_content(system_prompt)

print(response.text)