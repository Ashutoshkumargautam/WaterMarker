import os
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tqdm import tqdm  # Import tqdm
from reportlab.lib.colors import Color


def create_watermark(watermark_image, output_path, transparency=0.5):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    image_width = 600
    image_height = 600
    x = (width - image_width) / 2
    y = (height - image_height) / 2
    # Set the fill color with transparency
    c.setFillAlpha(transparency)  # Set the transparency level
    c.drawImage(watermark_image, x, y, width=image_width, height=image_height, mask='auto')
    c.save()

def add_watermark(input_pdf, output_pdf, watermark_pdf):
    watermark_reader = PyPDF2.PdfReader(watermark_pdf)
    watermark_page = watermark_reader.pages[0]

    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            watermark_overlay = PyPDF2.PageObject.create_blank_page(width=page.mediabox[2], height=page.mediabox[3])
            watermark_overlay.merge_page(watermark_page)
            watermark_overlay.merge_page(page)
            writer.add_page(watermark_overlay)

    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)

pdf_folder = 'Put-Your-Pdf-Init'
watermark_image = 'watermark/watermark.png'
output_folder = 'Result'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


create_watermark(watermark_image, 'watermark.pdf', transparency=0.3)  # Adjust transparency as needed

create_watermark(watermark_image, 'watermark.pdf')

pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
# Wrap the loop with tqdm for a progress bar
for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
    input_pdf_path = os.path.join(pdf_folder, pdf_file)
    output_pdf_path = os.path.join(output_folder, f"watermarked_{pdf_file}")
    add_watermark(input_pdf_path, output_pdf_path, 'watermark.pdf')
    print(f"Processed {pdf_file}")