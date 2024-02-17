import os
from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_watermark(watermark_image, output_path, transparency=0.5):
    """
    Creates a watermark PDF from an image with specified transparency.
    """
    # Create a canvas and set its size to letter
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    # Calculate image position (centered)
    image_width, image_height = 600, 600
    x, y = (width - image_width) / 2, (height - image_height) / 2
    # Set transparency and draw the image
    c.setFillAlpha(transparency)
    c.drawImage(watermark_image, x, y, width=image_width, height=image_height, mask='auto')
    c.save()

def add_watermark(input_pdf, output_pdf, watermark_pdf):
    """
    Adds a watermark to each page of the input PDF and saves it to the output PDF.
    """
    watermark_reader = PdfReader(watermark_pdf)
    watermark_page = watermark_reader.pages[0]

    with open(input_pdf, 'rb') as file:
        reader = PdfReader(file)
        writer = PdfWriter()
        total_pages = len(reader.pages)

        for page_num in range(total_pages):
            page = reader.pages[page_num]
            watermark_overlay = PageObject.create_blank_page(width=page.mediabox[2], height=page.mediabox[3])
            watermark_overlay.merge_page(watermark_page)
            watermark_overlay.merge_page(page)
            writer.add_page(watermark_overlay)
            print(f"Watermarking {input_pdf} - Page {page_num + 1} of {total_pages}")

    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)

def process_pdfs(pdf_folder, watermark_image, output_folder, watermark_pdf='watermark.pdf'):
    """
    Processes all PDF files in the specified folder, adding watermarks.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    create_watermark(watermark_image, watermark_pdf, transparency=0.3)
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        input_pdf_path = os.path.join(pdf_folder, pdf_file)
        output_pdf_path = os.path.join(output_folder, f"watermarked_{pdf_file}")
        print(f"Processing {pdf_file}")
        add_watermark(input_pdf_path, output_pdf_path, watermark_pdf)
        print(" - Done")

    print("All PDFs processed.")

# Example usage
pdf_folder = 'Put-Your-Pdf-Folder-Here'
watermark_image = 'watermark/watermark.png'
output_folder = 'Result'
process_pdfs(pdf_folder, watermark_image, output_folder)


