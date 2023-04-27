from pdfminer.high_level import extract_pages
import pdfminer
from datetime import datetime
import re
import pandas as pd

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

def GetAllElementsFromPages(pages):
    all_elements = {}
    for i in range(len(pages)):
        all_elements[i] = GetElementsFromPage(pages[i])
    return all_elements

def CleanElements(all_elements):
    for key in all_elements:
        # Check if 'Informações Adicionais' exists
        cut = [m for m in all_elements[key] if isinstance(m, pdfminer.layout.LTTextBoxHorizontal)
                and ReMatchPattern('Informações Adicionais',m.get_text())]
        if len(cut) == 0:
            continue
        # Get its position
        cut = cut[0].bbox[1]
        # Exclude everthing bellow it
        all_elements[key] = [m for m in all_elements[key] if m.bbox[1] > cut]
    return all_elements

def ReMatchPattern(pattern, string):
    return len(re.findall(pattern,string))>0

def GetDates(all_elements):
    all_dates = []
    for key in all_elements:
        dates = [m.get_text() for m in all_elements[key] if isinstance(m, pdfminer.layout.LTTextBoxHorizontal) and 
                    m.bbox[0] == 30 and
                    ReMatchPattern('[0-9]{2}/[0-9]{2}/[0-9]{4}',m.get_text())]
        dates = [d.replace('Lançamentos\n','').replace('Dia\n','') for d in dates]
        dates = [e for d in dates for e in re.sub('\\n$','',d).split('\n') if e != '']
        dates = [datetime.strptime(d,'%d/%m/%Y') for d in dates]
        all_dates += dates
    return all_dates

def GetValues(all_elements):
    all_values = []
    for key in all_elements:    
        values = [m.get_text() for m in all_elements[key] if isinstance(m,pdfminer.layout.LTTextBoxHorizontal) and
                    int(m.bbox[2]+0.5)==570 and 
                    ReMatchPattern('^[0-9\.]+,[0-9]{2} *\([\+\-]\)',m.get_text())]
        values = [v.replace('Valor\n','') for v in values]
        values = [x for v in values for x in re.sub('\\n$','',v).split('\n') if x != '']
        values = [re.sub('[^0-9\+\-]','',v) for v in values]
        values = [-0.01*int(v.replace('+','').replace('-','')) if ReMatchPattern('-',v) else 0.01*int(v.replace('+','').replace('-','')) for v in values]
        values = [round(v,2) for v in values]
        all_values += values
    return all_values

def GetDescription(all_elements):
    all_description = []
    for key in all_elements:
        description = [m.get_text() for m in all_elements[key] if isinstance(m, pdfminer.layout.LTTextBoxHorizontal) and m.bbox[0] == 91]
        description = [d.replace('Histórico\n','') for d in description]
        description = [v for d in description for v in re.sub('\n([^\n]*)(\n)',' \g<1> new_line ',d).split(' new_line ') if v!= '']
        all_description += description
    return all_description

def CalculateBalance(df):
    balance = [df['value'][0]]
    mask = (df['description'] != 'S A L D O\n') & (df['description'] != 'Saldo Anterior\n')
    df = df[mask]
    df = df.reset_index(drop = True)
    for i in range(0, len(df['value'])):
        balance.append(round(balance[i] + df['value'][i],2))
    df['balance'] = balance[1:]
    return df

def ReadBancoBrasil(file_path):
    pages = GetPagesFromFile(file_path)
    all_elements = GetAllElementsFromPages(pages)
    all_elements = CleanElements(all_elements)
    dates = GetDates(all_elements)
    values = GetValues(all_elements)
    description = GetDescription(all_elements)
    df = pd.DataFrame({'date': dates, 'value': values, 'description': description})
    df = CalculateBalance(df)
    return df

# # Exemple:
# file_path = '../ExtratosFail/04/Extrato01.pdf'
# file_path = '../ExtratosFail/04/Extrato09.pdf'

# df = ReadBancoBrasil(file_path)