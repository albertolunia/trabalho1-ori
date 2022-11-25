# Projeto de ORI
# Alunas: Ana Cristina, Maria Gabriella e Larissa Mendes

from asyncore import write
from mimetypes import init

import re

conjunto = open("conjunto.txt", "r").read()
consulta = open("consulta.txt", "r").read()

#função que tira a pontuação do texto 
def limpaTexto(texto):
  return texto.replace(",", "").replace(".", "").replace("!", "").replace("?", "")

#função que remove as palavras desconsideradas
def removeDesconsideradas(text): 
    with open("desconsideradas.txt", "r") as textFile:
            lines = textFile.readlines()
            lines = list(map(lambda s: s.strip(), lines))

    for i in lines:
        text = re.sub(r'\s'+i+'([\s,\.])',r'\1',text) 

    return text

#função que verifica o tipo de busca
def busca(consulta):
    if(consulta.find(",") != -1):
        return "and"
    elif(consulta.find(";") != -1):
        return "or"
        

#função que retorna a resposta na formatação pedida
def resposta(conjunto, consulta):
    qtd = 0
    files = []
    tipo = busca(consulta)
    if(tipo == "and"):
        consulta = consulta.split(',')  
    elif(tipo == "or"):
        consulta = consulta.split(';')

    for linha in conjunto.splitlines():
        linha = linha.rstrip()
        arquivo = open(linha, "r")
        texto = str(arquivo.read()).strip()
        
        #print(consulta)
        textoLimpo = limpaTexto(texto)
        textoFinal = removeDesconsideradas(textoLimpo)

        achouPalavras = 0
        for palavra in consulta:
            if(palavra in textoFinal):
                achouPalavras += 1

        if(tipo == "and" and achouPalavras == len(consulta)):
            qtd += 1
            files.append(linha)
        elif(tipo == "or" and achouPalavras > 0):
            qtd += 1
            files.append(linha)
        arquivo.close()

    return str(qtd)+"\n"+"\n".join(files)

def pegarIndice(conjunto):
    dicionarios = []
    palavras = []
    for linha in conjunto.splitlines():
        linha = linha.rstrip()
        dic = {}
        arquivo = open(linha, "r")
        texto = str(arquivo.read()).strip()

        textoLimpo = limpaTexto(texto)
        textoFinal = removeDesconsideradas(textoLimpo)

        textoFinal = textoFinal.split(' ')
        
        for p in textoFinal:
            try: 
                dic[p] += 1
            except:
                dic[p] = 1
            palavras.append(p)
        
        dicionarios.append(dic)
        # print(textoFinal)
        # print(dic)
        arquivo.close()
    
    palavras = list( dict.fromkeys(palavras) )
    #print(palavras)

    indice = open("indice.txt", 'w')
    palavras = sorted(palavras)
    for p in palavras:
        frase = []
        count = 1
        frase.append(p)
        for dic in dicionarios:
            try:
                frase.append(str(count)+','+str(dic[p]))
            except:
                pass
            count += 1
        
        frase = " ".join(frase)
        indice.write(frase+'\n')

    indice.close()
    
pegarIndice(conjunto)

saída = resposta(conjunto, consulta)
r = open("resposta.txt", "w")
r.write(saída)
r.close()