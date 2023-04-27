from pdfminer.high_level import extract_pages
import pdfminer
from datetime import datetime
import re
import pandas as pd

class Transaction:
    def __init__(self, date, description, value, balance):
        self.date = date
        self.description = description
        self.value = value
        self.balance = balance

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
    # All elements is a dict {page_number: page_elements}
    all_elements = {}
    for i in range(len(pages)):
        all_elements[i] = GetElementsFromPage(pages[i])
    return all_elements

def ReMatchPattern(pattern, string):
    return len(re.findall(pattern,string))>0

def GetDateDescription(all_elements):
    date_description = []
    for key in all_elements:
        dd = [m for m in all_elements[key] if isinstance(m, pdfminer.layout.LTTextBoxHorizontal) if
                                int(m.bbox[0]) == 30 and
                                ReMatchPattern('^[0-9]{2}/[0-9]{2}/[0-9]{4}',m.get_text())]
        # ordernar por bbox[1]
        dd = sorted(dd, key=lambda m: -m.bbox[1])
        date_description += dd
    date = [re.sub('^([0-9]{2}/[0-9]{2}/[0-9]{4}).*','\g<1>',d.get_text()) for d in date_description]
    date = [datetime.strptime(d.replace('\n',''),'%d/%m/%Y') for d in date]
    description = [re.sub('^([0-9]{2}/[0-9]{2}/[0-9]{4})','',d.get_text()).strip() for d in date_description]
    return date, description

def parse_float(string):
    string = string.replace('\n','')
    string = string.replace('.', '')
    string = string.replace(',', '.')
    value = float(string)
    return value

def GetValues(all_elements):
    values = []
    for key in all_elements:
        v = [m for m in all_elements[key] if isinstance(m, pdfminer.layout.LTTextBoxHorizontal) if
                                (454 <= int(m.bbox[2]) <= 464 or 560 <= int(m.bbox[2]) <= 570) and
                                ReMatchPattern('[0-9\\.]+,[0-9]{2}',m.get_text())]
        # ordernar por bbox[1]
        v = sorted(v, key=lambda x: -x.bbox[1])
        v = [parse_float(v.get_text()) for v in v]
        values += v
    return values

def GetTransactions(file_path):
    pages = GetPagesFromFile(file_path)
    all_elements = GetAllElementsFromPages(pages)
    dates, descriptions = GetDateDescription(all_elements)
    values = GetValues(all_elements)
    balance = 0
    transactions = list()
    for i in range(0,len(values)):
        date = dates[i]
        description = descriptions[i]
        value = values[i]
        balance = 0
        if 'SALDO' in description.split(' '):
            balance = value
            value = 0
        transactions.append(Transaction(date,description,value,balance))
    return transactions

def TransactionsToDataFrame(transactions):
    data = []
    for t in transactions:
        data.append({
            'date': t.date,
            'description': t.description,
            'value': t.value,
            'balance': t.balance,
        })
    df = pd.DataFrame(data)
    return df

def SortDataFrame(df):
    df.loc[df['description'].str.contains('SALDO'), 'date'] = pd.to_datetime(df.loc[df['description'].str.contains('SALDO'), 'date']) - pd.Timedelta(seconds=1)
    df = df.sort_values(by='date').reset_index(drop=True)
    df.loc[df['description'].str.contains('SALDO'), 'date'] = pd.to_datetime(df.loc[df['description'].str.contains('SALDO'), 'date']) + pd.Timedelta(seconds=1)
    return df

def CalculateBalance(df):
    calculated_balance = [df['balance'][0]]
    for i in range(0, len(df['value'])):
        calculated_balance.append(round(calculated_balance[i] + df['value'][i],2))
    df['calculated_balance'] = calculated_balance[1:]
    return df

def ReadItau(file_path):
    transactions = GetTransactions(file_path)
    df = TransactionsToDataFrame(transactions)
    df = SortDataFrame(df)
    df = CalculateBalance(df)
    return df    

# # Para esse extrato não é esperado que os saldos batam
# file_path = '../ExtratosFail/06/Itau.pdf'
# df = ReadItau(file_path)
# df.to_csv('itau.csv')