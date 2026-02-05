import pdfplumber

pdf_path = "pricelist.pdf"  # put actual path

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
