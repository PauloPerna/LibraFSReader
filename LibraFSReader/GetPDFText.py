import PyPDF2

def GetPDFText(path):
    with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text = ""
        for i in range(num_pages):
            page = reader.pages[i]
            text += page.extract_text()
    return text