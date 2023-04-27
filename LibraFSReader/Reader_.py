import Reader.Nubank as Nubank
import Reader.BancoBrasil1 as BancoBrasil1

def Reader(type_of_statement, file_path):
    switcher = {
        'Nubank': Nubank.Read(file_path),
        'Banco Brasil 1': BancoBrasil1.Read(file_path)
    }
    return switcher.get(type_of_statement, "Invalid case")