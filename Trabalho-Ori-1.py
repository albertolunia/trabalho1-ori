import re

consulta = open("consulta.txt", "r").read()
conjunto = open("conjunto.txt", "r").read()


# Retorna o tipo de busca
def tipoDeBusca(consulta):
    if consulta.find(",") != -1:  # Caso as palavras estejam separar por , siginifica AND
        return "and"
    elif consulta.find(";") != -1:  # Caso as palavras estejam separar por ; siginifica OR
        return "or"


# Retira palavras desconsideradas
def removeDesconsideradas(text):
    with open("desconsideradas.txt", "r") as textFile:
        lines = textFile.readlines()
        lines = list(map(lambda s: s.strip(), lines))

    for i in lines:
        pattern = r'\b' + i + '([\s,.])'  # Retira todas as ocorrencias da palavra encontrada
        replacement = r''  # E substitui por nada
        text = re.sub(pattern, replacement, text)
    return text


# Retira todas as pontuações do texto
def removePontuacao(texto):
    return texto.replace(",", "").replace(".", "").replace("!", "").replace("?", "")


# Retorna o arquivo resposta.txt
def criaArquivoResposta(conjunto, consulta):
    qtd = 0
    files = []
    tipo = tipoDeBusca(consulta)  # Define o tipo de busca
    if tipo == "and":
        consulta = consulta.split(',')  # Caso seja and, separo as palavras por virgula
    elif tipo == "or":
        consulta = consulta.split(';')  # Caso seja or, separo as palavras por ponto e virgula

    for linha in conjunto.splitlines():  # Separando cada arquivo como um valor de linha
        linha = linha.rstrip()  # Tiro qualquer espaço que tenha no final da minha linha

        arquivo = open(linha, "r")  # Passo cada linha como um arquivo de texto pro meu arquivo
        texto = str(arquivo.read()).strip()  # Tiro qualquer espaço que tenha no começo ou no fim da linha

        textoLimpo = removePontuacao(texto)  # Retiro a pontuação
        textoFinal = removeDesconsideradas(textoLimpo)  # Retiro as palavras desconsideradas

        achouPalavras = 0
        for palavra in consulta:
            if palavra in textoFinal:  # Verifico se encontro alguma palavra buscada na minha linha
                achouPalavras += 1  # Se encontro eu aumento o numero de palavras achadas

        if tipo == "and" and achouPalavras == len(consulta):  # Verifico se achei as duas palavras consultadas
            qtd += 1
            files.append(linha)  # Se sim adiciono qual arquivo esta
        elif tipo == "or" and achouPalavras > 0:  # Verifico se achei qualquer uma das duas palavras consultadas
            qtd += 1
            files.append(linha)  # Se sim adiciono qual arquivo esta
        arquivo.close()  # Fecho o arquivo

    saida = str(qtd) + "\n" + "\n".join(files)  # Retorno a qtd e quais arquivos elas estão

    teste = open("resposta.txt", "w")
    teste.write(saida)
    teste.close()


# Retorna o arquivo indice.txt
def criaArquivoIndice(conjunto):
    dicionarios = []
    palavras = []
    for linha in conjunto.splitlines():  # Para cada arquivo do meu conjunto eu transformo os textos em uma linha
        linha = linha.rstrip()  # Retiro espaços no final da linha caso haja

        arquivo = open(linha, "r")  # Leio cada linha
        texto = str(arquivo.read()).strip()  # E retiro espaços antes e depois

        textoLimpo = removePontuacao(texto)  # Retiro pontuação
        textoFinal = removeDesconsideradas(textoLimpo)  # Retiramos palavras desconsideradas

        textoFinal = textoFinal.split()  # Separo cada palavra por espaço

        dic = {}
        for p in textoFinal:  # Adicionando cada palavra como um dicionario
            try:
                dic[p] += 1
            except:
                dic[p] = 1
            palavras.append(p)

        dicionarios.append(dic)  # Adicionando cada dicionario na lista de dicionarios
        arquivo.close()

    palavras = list(dict.fromkeys(palavras))  # Pegando somente a palavra chave do dicionario

    indice = open("indice.txt", 'w')
    palavras = sorted(palavras)  # Organizo as palavras
    for p in palavras:  # Cada palavra chave
        frase = []
        count = 1
        frase.append(p)  # Adiciono na lista de palavras
        for dic in dicionarios:  # Para cada dicionario meu na lista de dicionarios
            try:
                frase.append(str(count) + ',' + str(dic[p]))  # Esrevo quantas vezes ele apareceu e o nome dele
            except:
                pass
            count += 1  # Incremento toda vez que a palavra se repete

        frase = " ".join(frase)  # Retiro os []'' que tem no tipo de dado dicionario
        indice.write(frase + '\n')  # E escrevo no meu indice

    indice.close()


criaArquivoIndice(conjunto)
criaArquivoResposta(conjunto, consulta)
