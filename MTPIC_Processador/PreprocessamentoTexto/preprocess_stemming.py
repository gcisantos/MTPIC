import stemming
import tokenizer
import removalStopwords

def __main__():
    print("Iniciando Stemming em português.")
    texto = input('Insira o texto para realizar préprocessamento: ')
    print(preProcess(texto,'pt'))

def preProcess(texto,linguagem):
    return stemming.stemmer(removalStopwords.removalStopwords(tokenizer.tokenizer(texto),linguagem),linguagem)

def processaTokens(tokens,linguagem):
    return stemming.stemmer(removalStopwords.removalStopwords(tokens,linguagem),linguagem)

if __name__ == "__main__":
    __main__()

