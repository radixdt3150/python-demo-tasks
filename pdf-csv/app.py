import pymupdf  # PyMuPDF

# Open the PDF file
pdf_document = "table.pdf"
doc = pymupdf.open(pdf_document)

# Extract text from each page
for page_number in range(doc.page_count):
    page = doc.load_page(page_number)
    text = page.get_text("text")  # You can also try "blocks" or "words" for better control
    print(f"Page {page_number + 1} Text:\n{text}\n")
