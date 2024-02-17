import os
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_watermark(watermark_image, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter  # Get the dimensions of the page size
    image_width = 600
    image_height = 600
    # Calculate coordinates to center the image
    x = (width - image_width) / 1
    y = (height - image_height) / 1
    c.drawImage(watermark_image, x, y, width=image_width, height=image_height)
    c.save()


def add_watermark(input_pdf, output_pdf, watermark_pdf):
    # Open the input PDF file
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Open the watermark PDF file
        with open(watermark_pdf, 'rb') as watermark_file:
            watermark_reader = PyPDF2.PdfReader(watermark_file)
            watermark_page = watermark_reader.pages[0]

            # Merge each page of the input PDF with the watermark
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]

                # Create a new page to merge the watermark first and then the original page
                watermark_overlay = PyPDF2.PageObject.create_blank_page(width=page.mediabox[2], height=page.mediabox[3])
                watermark_overlay.merge_page(watermark_page)
                watermark_overlay.merge_page(page)

                # Add the new page with the watermark to the output writer
                writer.add_page(watermark_overlay)

        # Write the output PDF file
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)


# Directory containing the PDF file
pdf_folder = 'Put-Your-Pdf-Init'

# Get the PDF file path
pdf_file = os.path.join(pdf_folder, os.listdir(pdf_folder)[0])

# Watermark image file
watermark_image = 'watermark/watermark.png'  # Replace 'watermark.png' with your image file path

# Output PDF file with watermark
output_pdf = 'Result/output_with_watermark.pdf'

# Create a PDF containing the watermark image
create_watermark(watermark_image, 'watermark.pdf')

# Add watermark to the input PDF
add_watermark(pdf_file, output_pdf, 'watermark.pdf')


