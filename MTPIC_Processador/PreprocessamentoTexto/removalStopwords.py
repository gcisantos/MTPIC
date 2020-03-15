from nltk.corpus import stopwords
import nltk

def __main__():
    print("Iniciando Stemming em português.")
    texto = input('Insira o texto para realizar o processo de remoção de stopWords: ')
    print(removalStopwords(nltk.word_tokenize(texto),'pt'))

def removalStopwords(tokens,linguagem):
    removeStopWords= None
    if(linguagem=='pt'):
        removeStopWords =stopwords.words("portuguese")
        removeStopWords.append('é')        
    elif(linguagem=='en'):
        removeStopWords =stopwords.words("english")        
    elif(linguagem=='es'):
        removeStopWords =stopwords.words("spanish")

    return [word for word in tokens if word.lower() not in removeStopWords]

def removalStopwordsText(texto,linguagem):
    removeStopWords= None
    if(linguagem=='pt'):
        removeStopWords =stopwords.words("portuguese")
        removeStopWords.append('é')        
    elif(linguagem=='en'):
        removeStopWords =stopwords.words("english")        
    elif(linguagem=='es'):
        removeStopWords =stopwords.words("spanish")
    
    return ' '.join([word for word in nltk.word_tokenize(texto) if word.lower() not in removeStopWords])
   

if __name__ == "__main__":
    __main__()
