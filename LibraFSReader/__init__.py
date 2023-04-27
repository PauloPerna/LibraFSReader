import GetPDFText
import Identifier
from Reader_ import Reader

def ReadAll(file_path):
    text = GetPDFText.GetPDFText(file_path)
    typeExtrato = Identifier.Identifier(text=text)
    df = Reader(typeExtrato, file_path)
    return df

def IdentifierAll(text):
    return Identifier.Identifier(text=text)