import streamlit as st
from docx import Document
from PyPDF2 import PdfReader
import openai

# Set OpenAI API key
openai.api_key = "your_openai_api_key"

# Function to extract text from uploaded files
def extract_text(file):
    if file.name.endswith('.docx'):
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    elif file.name.endswith('.pdf'):
        reader = PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages])
    else:
        return "Unsupported file type"

# Function to summarize text using OpenAI
def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Summarize this:\n{text}"}]
    )
    return response['choices'][0]['message']['content']

# Streamlit app
st.title("Document Summarizer")
st.write("Upload a Word or PDF document to summarize its contents.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])

if uploaded_file is not None:
    # Extract text from the file
    text = extract_text(uploaded_file)
    if text == "Unsupported file type":
        st.error("Unsupported file type. Please upload a .docx or .pdf file.")
    else:
        st.write("### Extracted Text:")
        st.text_area("Document Text", text, height=300)

        # Summarize the text
        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(text)
                st.write("### Summary:")
                st.success(summary)
