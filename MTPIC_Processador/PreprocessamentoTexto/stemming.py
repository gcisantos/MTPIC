import nltk
from nltk.stem.snowball import SnowballStemmer

idiomas =	{    
    'da':'danish',
    'nl':'dutch',
    'en':'english',
    'fi':'finnish',
    'fr':'french',
    'de':'german',
    'hu':'hungarian',
    'it':'italian',
    'no':'norwegian',
    'pt':'portuguese',
    'ro':'romanian',
    'ru':'russian',
    'es':'spanish',
    'sv':'swedish'
    }

def __main__():
    print("Iniciando Stemming em português.")
    texto = input('Insira o texto para realizar o stemming: ')
    print(stemmer(nltk.word_tokenize(texto),'pt'))

def stemmer(tokens,linguagem):
        return ' '.join([SnowballStemmer(idiomas[linguagem]).stem(token) for token in tokens])
    
    
if __name__ == "__main__":
    __main__()
