import pymupdf  # PyMuPDF

# Open the PDF file
pdf_document = "table.pdf"
doc = pymupdf.open(pdf_document)

page = doc[0]

tables = page.find_tables()

for index, table in enumerate(tables):
    for cell in table.header.cells:
        print(cell)
