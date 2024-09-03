"""
The following example extracts the textual content and tabular content distinctively
It also groups the ouput content based on the above categories i.e text and table data
However the data is not grouped in an ordered manner
"""
import pdfplumber

def is_within_table(word, table_bbox):
    """Check if a word is within the bounds of a table."""
    x0, y0, x1, y1 = word["x0"], word["top"], word["x1"], word["bottom"]
    table_x0, table_y0, table_x1, table_y1 = table_bbox
    
    return (x0 >= table_x0 and x1 <= table_x1 and y0 >= table_y0 and y1 <= table_y1)

def extract_table_bboxes(page):
    """Extract bounding boxes for all tables on the page."""
    table_bboxes = []
    for table in page.find_tables():
        table_bboxes.append(table.bbox)
    return table_bboxes

def merge_words(words, x_tolerance=5):
    """Merge words that are close together along the same line."""
    if not words:
        return []

    merged_words = []
    current_word = words[0]["text"]
    current_x1 = words[0]["x1"]
    
    for i in range(1, len(words)):
        word = words[i]
        if word["x0"] - current_x1 <= x_tolerance:
            # If the next word is close enough, merge it with the current word
            current_word += " " + word["text"]
            current_x1 = word["x1"]
        else:
            # Otherwise, finalize the current word and start a new one
            merged_words.append(current_word)
            current_word = word["text"]
            current_x1 = word["x1"]
    
    # Don't forget to add the last word
    merged_words.append(current_word)
    
    return merged_words

def process_page(page):
    """Extract and separate text and tables from a single page."""
    # Extract words with positional data
    words = page.extract_words()

    # Extract table bounding boxes
    table_bboxes = extract_table_bboxes(page)

    # Separate words into those inside tables and those outside
    text_outside_tables = []
    text_inside_tables = []

    for word in words:
        inside_table = False
        for bbox in table_bboxes:
            if is_within_table(word, bbox):
                text_inside_tables.append(word)
                inside_table = True
                break
        if not inside_table:
            text_outside_tables.append(word)

    # Merge words in each list
    merged_text_outside = merge_words(text_outside_tables)
    merged_text_inside = merge_words(text_inside_tables)

    # Combine the merged text outside of tables
    text_data = " ".join(merged_text_outside)

    return text_data, merged_text_inside, table_bboxes

def process_pdf(pdf_document):
    """Process each page of the PDF and extract text and tables."""
    with pdfplumber.open(pdf_document) as pdf:
        all_text_outside_tables = []
        all_text_inside_tables = []
        all_tables = []

        for i, page in enumerate(pdf.pages):
            print(f"\nProcessing Page {i + 1}...\n")
            text_outside, text_inside, table_bboxes = process_page(page)

            all_text_outside_tables.append(text_outside)
            all_text_inside_tables.append(text_inside)
            all_tables.append(page.extract_tables())

        return all_text_outside_tables, all_text_inside_tables, all_tables

def printTables(tables):
    for table in tables:
        print("Table: ")
        for row in table:
            print(row)

        print("\n")
# Usage
pdf_document = "adobe.pdf"
text_outside_tables, text_inside_tables, tables = process_pdf(pdf_document)

# Example: Print results for each page
for i, (text_outside, text_inside, table) in enumerate(zip(text_outside_tables, text_inside_tables, tables)):
    print(f"Page {i + 1} - Text Outside Tables:\n{text_outside}")
    #print(f"Page {i + 1} - Text Inside Tables:\n{text_inside}")
    printTables(table)
    print("\n")

