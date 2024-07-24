import pytesseract
from PIL import Image
import spacy
import re

# Configure Tesseract path 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

# Load SpaCy model
nlp = spacy.load('en_core_web_lg')


# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Function to parse extracted text
def parse_resume(text):
    doc = nlp(text)
    data = {
        'name': None,
        'email': None,
        'phone': None,
        'linkedin':None,
        'education': [],
        'experience': [],
        'skills': [],
        'description': []
    }

    # Extract name
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            data['name'] = ent.text
            break

    # Extract Email
    email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+')
    email_matches = email_pattern.findall(text)
    if email_matches:
        data['email'] = email_matches[0]

    # Extract phone number
    phone_pattern = re.compile(r"^\s*\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$")
    phone_matches = phone_pattern.findall(text)
    if phone_matches:
        data['phone'] = ''.join(phone_matches[0])
    

     # Extract linked data
    linkedin_pattern = re.compile(r'(linkedin\.com/in/[A-Za-z0-9-]+)')
    linkedin_matches = linkedin_pattern.findall(text)
    if linkedin_matches:
        data['linkedin'] = ''.join(linkedin_matches[0])
    

    # Extract education and experience
    education_keywords = ['university', 'college', 'institute', 'school', 'degree', 'bachelor', 'master', 'b.sc', 'm.sc', 'ph.d','diploma','certification']
    experience_keywords = ['experience','work experience' 'responsibilities', 'role', 'position', 'job', 'employment', 'profesional experience','profesional expertise','work history']
    skills_keywords = ['skills', 'competencies','additional skills','technical skills']
    
    education_pattern = re.compile(r'|'.join(education_keywords), re.IGNORECASE)
    experience_pattern = re.compile(r'|'.join(experience_keywords), re.IGNORECASE)
    skills_pattern = re.compile(r'|'.join(skills_keywords), re.IGNORECASE)
    date_pattern = re.compile(r'\b(?:\d{4}|\d{1,2}/\d{1,2}/\d{4})\b') 

    lines = text.split('\n')
    for line in lines:
        if education_pattern.search(line):
            data['education'].append(line)
        elif experience_pattern.search(line):
            data['experience'].append(line)
        elif skills_pattern.search(line):
            data['skills'].append(line)

    # Additional extraction logic based on dates and contextual keywords
    for i, line in enumerate(lines):
        if education_pattern.search(line):
            data['education'].append(line)
            # Check the next few lines for more details
            for j in range(1, 3):
                if i + j < len(lines):
                    if date_pattern.search(lines[i + j]) or education_pattern.search(lines[i + j]):
                        data['education'][-1] += ' ' + lines[i + j]
        elif experience_pattern.search(line):
            data['experience'].append(line)
            # Check the next few lines for more details
            for j in range(1, 3):
                if i + j < len(lines):
                    if date_pattern.search(lines[i + j]) or experience_pattern.search(lines[i + j]):
                        data['experience'][-1] += ' ' + lines[i + j]
        elif skills_pattern.search(line.lower()):
            data['skills'].append(line)
            # Check the next few lines for more details
            for j in range(1, 3):
                if i + j < len(lines):
                    if skills_pattern.search(lines[i + j]):
                        data['skills'][-1] += ' ' + lines[i + j]

    # Extract descriptions (following experience sections)
    for i, line in enumerate(lines):
        if experience_pattern.search(line):
            description = []
            # Collect subsequent lines as description until a new section starts
            for j in range(i + 1, len(lines)):
                if experience_pattern.search(lines[j]) or education_pattern.search(lines[j]) or skills_pattern.search(lines[j]):
                    break
                description.append(lines[j])
            data['description'].append(' '.join(description).strip())

    return data
