import pdfplumber

with pdfplumber.open('invoice-simple.pdf') as pdf:
    page0 = pdf.pages[0]
    print(page0.extract_table())
