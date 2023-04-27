from pdfminer.high_level import extract_pages
import pdfminer
from datetime import datetime
import re
import pandas as pd

class Transaction:
    def __init__(self, date, description, value, initial_balance, final_balance):
        self.date = datetime.strptime(date, "%d %b %Y")
        self.description = description
        self.value = value
        self.initial_balance = initial_balance
        self.final_balance = final_balance

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

def ReMatchPattern(pattern, string):
    return len(re.findall(pattern,string))>0

def GetAllTransactionsPositions(all_elements):
    # O parametro x1 define o filtro de posição dos elementos
    # pode precisar ser alterado!!!
    x1 = 500
    transaction_position = {}
    for key in all_elements:
        e_pos = [e for e in all_elements[key] if e.bbox[2] > x1 and isinstance(e,pdfminer.layout.LTTextBoxHorizontal)]
        transaction_values = [e for e in e_pos if ReMatchPattern('^[0-9\\.]+,[0-9]{2}\\n$',e.get_text())]
        transaction_position[key] = [t.bbox[3] for t in transaction_values]
    return transaction_position

def GetAllDatePositions(all_elements):
    date_position = {}
    for key in all_elements:
        dates = [e for e in all_elements[key] if isinstance(e,pdfminer.layout.LTTextBoxHorizontal) and ReMatchPattern('^[0-3][0-9] [A-ZÇ]{3} 20[0-9]{2}',e.get_text())]
        date_position[key] = [d.bbox[3] for d in dates]
    return date_position

def GetAllSignPositions(all_elements):
    sign_position = {}
    for key in all_elements:
        signs = [e for e in all_elements[key] if isinstance(e,pdfminer.layout.LTTextBoxHorizontal) and ReMatchPattern('^Total de [saídentrd]+\\n$',e.get_text())]
        sign_position[key] = [s.bbox[3] for s in signs]
    return sign_position

def MashUpDicts(dict1, dict2):
    keys = set(dict1.keys()) | set(dict2.keys())
    result = {}
    for key in keys:
        values = sorted(set(dict1[key] + dict2[key]))
        result[key] = values
    return result

def GetDescriptionValue(mov):
    description = ' '.join([e.get_text() for e in mov[0:(len(mov)-1)]]).replace('\n','').strip()
    value_text = mov[len(mov)-1].get_text()
    value = float(value_text.replace('.','').replace('\n','').replace(',','.'))
    return description, value
    
def GetTransactions(file_path):
    pages = GetPagesFromFile(file_path)
    all_elements = GetAllElementsFromPages(pages)
    transaction_position = GetAllTransactionsPositions(all_elements)
    date_position = GetAllDatePositions(all_elements)
    all_positions = MashUpDicts(transaction_position,date_position)
    sign_position = GetAllSignPositions(all_elements)
    all_positions = MashUpDicts(all_positions,sign_position)
    initial_balance = 0
    final_balance = 0
    date = "01 JAN 1999"
    transactions = list()
    for key in all_positions:
        for y1 in reversed(all_positions[key]):
            mov = [e for e in all_elements[key] if int(e.bbox[3]) == int(y1)]
            if y1 in transaction_position[key]:
                if mov[0].get_text() == 'Saldo inicial\n':
                    value_text = mov[1].get_text()
                    initial_balance = float(value_text.replace('.','').replace('\n','').replace(',','.'))
                elif mov[0].get_text() == 'Saldo final do período\n':
                    value_text = mov[1].get_text()
                    final_balance = float(value_text.replace('.','').replace('\n','').replace(',','.'))
                else:
                    description, value = GetDescriptionValue(mov)
                    if sign == 'negativo':
                        value = -value
                    transactions.append(Transaction(date,description,value,initial_balance,final_balance))
            if y1 in date_position[key]:
                date = mov[0].get_text().replace('\n','')
                date = str.replace(date, 'FEV','FEB')
                date = str.replace(date, 'ABR','APR')
                date = str.replace(date, 'MAI','MAY')
                date = str.replace(date, 'AGO','AUG')
                date = str.replace(date, 'SET','SEP')
                date = str.replace(date, 'OUT','OCT')
                date = str.replace(date, 'DEZ','DEC')
            if y1 in sign_position[key]:
                if 'Total de entradas\n' in [m.get_text() for m in mov]:
                    sign = 'positivo'
                else:
                    sign = 'negativo'
    return transactions

def TransactionsToDataFrame(transactions):
    data = []
    for t in transactions:
        data.append({
            'date': t.date,
            'description': t.description,
            'value': t.value,
            'initial_balance': t.initial_balance,
            'final_balance': t.final_balance
        })
    df = pd.DataFrame(data)
    return df

def CalculateBalance(df):
    balance = [df['initial_balance'][0]]
    for i in range(0, len(df['value'])):
        balance.append(round(balance[i] + df['value'][i],2))
    df['balance'] = balance[1:]
    return df

def Read(file_path):
    transactions = GetTransactions(file_path)
    df = TransactionsToDataFrame(transactions)
    df = CalculateBalance(df)
    return df