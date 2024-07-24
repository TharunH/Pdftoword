import streamlit as st
from resume_parser import extract_text_from_image, parse_resume
from file_converter import pdf_to_images, docx_to_images
import pandas as pd
import os

def save_to_excel(parsed_data, file_name='parsed_resume_data.xlsx'):
    flat_data = {
        'name': [parsed_data['name']],
        'email': [parsed_data['email']],
        'phone': [parsed_data['phone']],
        'education': ['; '.join(parsed_data['education'])],
        'experience': ['; '.join(parsed_data['experience'])],
        'skills': ['; '.join(parsed_data['skills'])],
        'description': ['; '.join(parsed_data['description'])]
    }
    
    df = pd.DataFrame(flat_data)
    df.to_excel(file_name, index=False)

st.title("Resume Parser")

uploaded_file = st.file_uploader("Choose a resume file", type=["docx", "pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Ensure the uploaded file retains its extension
    _, file_extension = os.path.splitext(uploaded_file.name)
    temp_file_path = f"temp_file{file_extension}"
    
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    output_folder = "output_images"
    os.makedirs(output_folder, exist_ok=True)

    image_paths = []
    poppler_path = r'C:\poppler\bin'  # Update this path to where Poppler is installed
    if file_extension.lower() == '.pdf':
        image_paths = pdf_to_images(temp_file_path, output_folder= output_folder)
    elif file_extension.lower() == '.docx':
        temp_pdf_path = "temp_file.pdf"
        image_paths = docx_to_images(temp_file_path, output_folder, temp_pdf_path)
    elif file_extension.lower() in ['.png', '.jpg', '.jpeg']:
        image_paths.append(temp_file_path)

    text = ""
    for image_path in image_paths:
        text += extract_text_from_image(image_path) + "\n"

    parsed_data = parse_resume(text)
    
    st.subheader("Extracted Text")
    st.text(text)

    st.subheader("Parsed Data")
    st.json(parsed_data)

    if st.button('Save to Excel'):
        save_to_excel(parsed_data)
        st.success('Parsed data saved to Excel successfully!')
