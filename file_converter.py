import os
import pythoncom
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
from docx2pdf import convert

# Function to convert PDF to images
def pdf_to_images(pdf_path, output_folder):
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i + 1}.png')
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
    return image_paths

# Function to convert Word document to images
def docx_to_images(docx_path, output_folder, temp_pdf_path):
    pythoncom.CoInitialize()  # Initialize COM library
    # Convert DOCX to PDF first
    convert(docx_path, temp_pdf_path)
    # Convert the PDF to images
    return pdf_to_images(temp_pdf_path, output_folder)

# Helper function to create an image from text
def create_image_from_text(text, width=800, height=1000, font_size=20):
    font = ImageFont.load_default()
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    margin = 40
    offset = 50
    
    for line in text.split('\n'):
        draw.text((margin, offset), line, font=font, fill='black')
        offset += font_size + 10
        if offset > height - margin:
            break
    
    return image
