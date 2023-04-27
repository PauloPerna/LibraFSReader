import re
import pandas as pd
import tabula

def LeituraInicial(file_path):
    df_list = tabula.read_pdf(file_path)
    return df_list[1]

def UnirLinhasNA1(df):
    i = len(df)-1
    while i > 0:
        if pd.isna(df[df.columns[1]][i]):
            df[df.columns[0]][i-1] = df[df.columns[0]][i-1] + ' '+ df[df.columns[0]][i]
            df.drop(i, inplace=True)
        i-=1
    df.reset_index(drop = True, inplace=True)
    return df

def ApagarLinhasPerc(df):
    df[df.columns[1]][range(2,len(df),2)] = pd.NA
    return df

def CleanStringNAN(l):
    l = re.sub(' nan$','',l)
    l = l.strip()
    return l

def UnirLinhasNA2(df):
    i = 0
    while i < len(df):
        if pd.isna(df[df.columns[1]][i]):
            df[df.columns[0]][i-1] = df[df.columns[0]][i-1] + ' ' + str(df[df.columns[0]][i])
        i+=1
    df[df.columns[0]] = [CleanStringNAN(m) if not pd.isna(m) else '' for m in df[df.columns[0]]]
    return df

def RemoverLinhasNA(df):
    df = df[df.iloc[:,1].notnull()]
    return df

def FormatacaoFinal(df):
    df_val = df.iloc[:,1].str.split(' ',expand=True)
    df = pd.concat([df.iloc[:,0],df_val],axis=1)
    df.columns = df.iloc[0]
    df = df[1:]
    return df

def ReadSCRModalData(file_path):
    df = LeituraInicial(file_path)
    df = UnirLinhasNA1(df)
    df = ApagarLinhasPerc(df)
    df = UnirLinhasNA2(df)
    df = RemoverLinhasNA(df)
    df = FormatacaoFinal(df)
    return df