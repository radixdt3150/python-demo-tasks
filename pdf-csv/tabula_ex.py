import tabula

pdf_path = "table.pdf"

dataframes = tabula.read_pdf(pdf_path)

print(dataframes)

tabula.convert_into(pdf_path, "output.csv", output_format="csv", pages="all", stream=True)