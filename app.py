import streamlit as st
import spacy
import PyPDF2
from io import BytesIO
from docx import Document

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

# Function to anonymize medical data
def anonymize_text(text):
    doc = nlp(text)
    anonymized_text = ""
    
    for ent in doc.ents:
        # Replace PERSON entity with [REDACTED]
        if ent.label_ == "PERSON":
            anonymized_text += "[REDACTED]"
        else:
            anonymized_text += ent.text
        anonymized_text += " "

    return anonymized_text

# Convert text to DOCX
def convert_text_to_docx(text):
    doc = Document()
    doc.add_paragraph(text)
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream

# Streamlit App
st.title("Medical Record Anonymizer")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    # Extract and display text from the PDF
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted Text", pdf_text, height=200)

    # Button to anonymize the text
    if st.button("Anonymize"):
        anonymized_text = anonymize_text(pdf_text)
        st.text_area("Anonymized Text", anonymized_text, height=200)

        # Convert to DOCX and allow download
        docx_file = convert_text_to_docx(anonymized_text)
        st.download_button(label="Download Anonymized Record as DOCX", data=docx_file, file_name="anonymized_record.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
