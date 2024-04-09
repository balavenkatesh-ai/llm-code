from bs4 import BeautifulSoup
import pandas as pd
from weasyprint import HTML
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
import os

def convert_html_to_pdf(html_path, pdf_path):
    with open(html_path, "r") as html_file:
        html_content = html_file.read()
        HTML(string=html_content).write_pdf(pdf_path)

def attach_pdf_to_excel(pdf_path, excel_path):
    wb = load_workbook(filename=excel_path)
    ws = wb.active
    
    # Add the PDF as an image to the Excel sheet
    img = Image(pdf_path)
    ws.add_image(img, 'A1')

    # Save the Excel file
    wb.save(excel_path)

def main():
    # Provide the paths to your HTML, PDF, and Excel files
    html_path = "path/to/your/html/file.html"
    pdf_path = "output.pdf"
    excel_path = "path/to/your/excel/file.xlsx"

    # Convert HTML to PDF
    convert_html_to_pdf(html_path, pdf_path)

    # Attach PDF to Excel
    attach_pdf_to_excel(pdf_path, excel_path)

if __name__ == "__main__":
    main()
