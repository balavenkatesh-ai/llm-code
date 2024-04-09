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


import pandas as pd

def create_csv_with_title(filename, title):
    # Create a DataFrame for the first table
    data1 = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    }
    df1 = pd.DataFrame(data1)

    # Create a DataFrame for the second table
    data2 = {
        'Country': ['USA', 'Canada', 'UK'],
        'Language': ['English', 'French', 'English'],
        'Population': [328, 37, 66]
    }
    df2 = pd.DataFrame(data2)

    # Write the title and DataFrames to a CSV file
    with open(filename, 'w') as f:
        f.write(title + '\n\n')  # Write the title and leave one empty row
        df1.to_csv(f, index=False)
        # Add extra row between tables
        f.write('\n')
        df2.to_csv(f, index=False)

def main():
    filename = 'example.csv'
    title = 'Table Title'

    # Create the CSV file with title and tables
    create_csv_with_title(filename, title)

if __name__ == "__main__":
    main()
