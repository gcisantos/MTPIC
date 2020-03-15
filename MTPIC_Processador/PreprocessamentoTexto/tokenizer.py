import nltk

def __main__():
    print("Iniciando Tokenizer")
    texto = input('Insira o texto para realizar o tokenizer: ')
    print(tokenizerText(texto))

def tokenizer(texto):
    return nltk.word_tokenize(texto)
    
def tokenizerText(texto):
    tokens =nltk.word_tokenize(texto)    
    return ','.join(['[\''+str(token)+'\']' for token in tokens])

if __name__ == "__main__":
    __main__()
