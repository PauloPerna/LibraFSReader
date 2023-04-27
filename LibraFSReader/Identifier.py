import re

def IsBancoBrasil1(text):
    # TODO: Complete function
    return False

def IsBancoBrasil2(text):
    # TODO: Complete function
    return False

def IsBancoBrasil3(text):
    # TODO: Complete function
    return False

def IsBancoBrasil4(text):
    # TODO: Complete function
    return False

def IsBancoBrasil5(text):
    # TODO: Complete function
    return False

def IsBancoBrasil6(text):
    # TODO: Complete function
    return False

def IsBancoC6(text):
    # TODO: Complete function
    return False

def IsBancoNordeste(text):
    # TODO: Complete function
    return False

def IsBancoPan(text):
    # TODO: Complete function
    return False

def IsBanrisul(text):
    # TODO: Complete function
    return False

def IsBMG(text):
    # TODO: Complete function
    return False

def IsBMG2(text):
    # TODO: Complete function
    return False

def IsBMG3(text):
    # TODO: Complete function
    return False

def IsBradescoCelular(text):
    # TODO: Complete function
    return False

def IsBradescoInternetBanking(text):
    # TODO: Complete function
    return False

def IsBradescoNetEmpresas(text):
    # TODO: Complete function
    return False

def IsBRB(text):
    # TODO: Complete function
    return False

def IsBTG(text):
    # TODO: Complete function
    return False

def IsCaixaATM(text):
    # TODO: Complete function
    return False

def IsCaixaDuasCol(text):
    # TODO: Complete function
    return False

def IsCaixaInternetBanking(text):
    # TODO: Complete function
    return False

def IsCaixaInternetBanking2(text):
    # TODO: Complete function
    return False

def IsCaixaNew(text):
    # TODO: Complete function
    return False

def IsCaixaPadrao(text):
    # TODO: Complete function
    return False

def IsCCPI(text):
    # TODO: Complete function
    return False

def IsCivia(text):
    # TODO: Complete function
    return False

def IsCora(text):
    # TODO: Complete function
    return False

def IsInter(text):
    # TODO: Complete function
    return False

def IsItau(text):
    # TODO: Complete function
    return False

def IsItauApp(text):
    # TODO: Complete function
    return False

def IsItauCarta(text):
    # TODO: Complete function
    return False

def IsItauEmpresas(text):
    # TODO: Complete function
    return False

def IsItauUniclass(text):
    # TODO: Complete function
    return False

def IsItauUniversidade(text):
    # TODO: Complete function
    return False

def IsMercantil(text):
    # TODO: Complete function
    return False

def IsMercantil2(text):
    # TODO: Complete function
    return False

def IsNubank(text):
    return len(re.findall("CNPJ: 18.236.120/0001-58",text)) > 0

def IsNeon(text):
    # TODO: Complete function
    return False

def IsNext(text):
    # TODO: Complete function
    return False

def IsPagbank(text):
    # TODO: Complete function
    return False

def IsPicpay(text):
    # TODO: Complete function
    return False

def IsOriginal(text):
    # TODO: Complete function
    return False

def IsSafra(text):
    # TODO: Complete function
    return False

def IsSafraApp(text):
    # TODO: Complete function
    return False

def IsSafraMovimentacao(text):
    # TODO: Complete function
    return False

def IsSafraRelatorio(text):
    # TODO: Complete function
    return False

def IsSantander(text):
    # TODO: Complete function
    return False

def IsSantanderDuplos(text):
    # TODO: Complete function
    return False

def IsSantanderEmpresarial(text):
    # TODO: Complete function
    return False

def IsSantanderIBEmpresas(text):
    # TODO: Complete function
    return False

def IsSantanderInternetBanking1(text):
    # TODO: Complete function
    return False

def IsSantanderInternetBanking2(text):
    # TODO: Complete function
    return False

def IsSantanderInternetBanking3(text):
    # TODO: Complete function
    return False

def IsSantanderInterno(text):
    # TODO: Complete function
    return False

def IsSantanderMaquina(text):
    # TODO: Complete function
    return False

def IsSantanderNegociosEmpresas(text):
    # TODO: Complete function
    return False

def IsSicoob(text):
    # TODO: Complete function
    return False

def IsSicoobDivicred(text):
    # TODO: Complete function
    return False

def IsSicoobEngecred(text):
    # TODO: Complete function
    return False

def IsSicoobSisbr(text):
    # TODO: Complete function
    return False

def IsSicredi(text):
    # TODO: Complete function
    return False

def IsSicredi2(text):
    # TODO: Complete function
    return False

def IsSofisa(text):
    # TODO: Complete function
    return False

def IsStone(text):
    # TODO: Complete function
    return False

def IsUnicred(text):
    # TODO: Complete function
    return False

def IsUnicred2(text):
    # TODO: Complete function
    return False

def IsUnicred3(text):
    # TODO: Complete function
    return False

def IsUniprime(text):
    # TODO: Complete function
    return False

def Identifier(text):
    funcoes = [("IsNubank","Nubank")]
    for funcao in funcoes:
        typeMatch = eval(funcao[0] + "(text)")
        if typeMatch:
            return funcao[1]
    