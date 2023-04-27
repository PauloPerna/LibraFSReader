import re
import pandas as pd
from pdfminer.high_level import extract_pages
import pdfminer

file_path = ["/home/perna/Desktop/99.Paulo Perna/CLINICA ANA BARTMANN LTDA/MODALIDADE X DATA BASE.pdf",
             "/home/perna/Desktop/99.Paulo Perna/ANA KARINA BARl'MANN/MODALIDADE X DATA BASE.pdf",
             "/home/perna/Desktop/99.Paulo Perna/LUIZ MARIO PEREIRA LOPES LABADESSA/MODALIDADE X DATA BASE.pdf"]
file_path = file_path[1]

def GetPagesFromFile(file_path):
    pages = []
    for page in extract_pages(file_path):
        pages.append(page)
    return pages

def GetElementsFromPage(page):
    elements = []
    for element in page:
        elements.append(element)
    return elements

def ReMatchPattern(pattern, string):
    return len(re.findall(pattern,string))>0

# Get pages and elements
page = GetPagesFromFile(file_path)[0]
elements = GetElementsFromPage(page)

# filter to text elements
elements = [m for m in elements if isinstance(m,pdfminer.layout.LTTextBoxHorizontal)]
elements

# get table area
modalidade = [m for m in elements if isinstance(m,pdfminer.layout.LTTextBoxHorizontal) and m.get_text()=='Modalidade\n']
threshold = int(modalidade[0].bbox[3]+1)

# Get table
table = [m for m in elements if m.bbox[3] < threshold]

# Get LTRects
LTRects = [m for m in table if isinstance(m,pdfminer.layout.LTRect)]
pos = [m.bbox[0] for m in LTRects]

for i in range(0,len(LTRects)):
    print('----------------------------------------------------------------')
    LTRect = LTRects[i]
    # Get LTRects content
    content = [m for m in table if m.bbox[0] > LTRect.bbox[0] and
                                m.bbox[1] > LTRect.bbox[1] and
                                m.bbox[2] < LTRect.bbox[2] and
                                m.bbox[3] < LTRect.bbox[3]]
    print(content)