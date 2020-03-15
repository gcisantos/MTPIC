import sys
import preprocess_stemming

import nltk

def main():
    print("Lendo parametros...")
    saida = open(sys.argv[2],'w',encoding='utf8')

    caracteresNpermitidos = [',',';','.','-','*','%','#','!','?','¨','&',')','(','=','+']

    saidaToken = open(sys.argv[3],'w',encoding='utf8')

    listaPalavras = []
    print("Iniciando processamento...")
    with open(sys.argv[1],"r",encoding='utf8') as arquivo:
        for linha in arquivo.readlines():
            
            #Transforma em lista para processar e armazena
            linha =  nltk.word_tokenize(linha)

            [listaPalavras.append(palavra.lower()) for palavra in linha]

            linha = ' '.join([palavra.lower()  for palavra in linha if palavra not in caracteresNpermitidos])

            linha = nltk.word_tokenize(preprocess_stemming.preProcess(linha,'pt'))

            [listaPalavras.append(palavra.lower()) for palavra in linha]

            linha = ' '.join([palavra.lower()  for palavra in linha if palavra not in caracteresNpermitidos])

            saida.write(linha+"\n")

    
    print("Lista salva...")

    print(str(len(listaPalavras)) +" Tokens distintos Encontrados" )

    listaPalavras = set(listaPalavras)

    print("Salvando lista de tokens...")

    [saidaToken.write(item+'\n') for item in listaPalavras]

  
    print("Processamento Concluído...")

if __name__ == "__main__":
    main()