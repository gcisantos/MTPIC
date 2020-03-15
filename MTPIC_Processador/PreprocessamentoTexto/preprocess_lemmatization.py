import lemmatizer
import tokenizer
import removalStopwords

def __main__():
    print("Iniciando Lemmatizer em português.")
    texto = input('Insira o texto para realizar préprocessamento: ')
    print(preProcess(texto))

def preProcess(texto):
    return lemmatizer.lemmatizer(' '.join(removalStopwords.removalStopwords(tokenizer.tokenizer(texto))))

def processaTokens(tokens):
    return lemmatizer.lemmatizer(' '.join(removalStopwords.removalStopwords(tokens)))

if __name__ == "__main__":
    __main__()

