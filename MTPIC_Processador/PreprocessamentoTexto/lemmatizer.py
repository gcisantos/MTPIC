# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 13:47:00 2018

@author: GCISANTOS
"""
import spacy

def __main__():
    print("Iniciando Lemmatizer em português.")
    texto = input('Insira o texto para realizar o Lemmatizer: ')    
    print(lemmatizer(texto))
   

def lemmatizer(texto):
    nlp = spacy.load('pt')
    
    #Processa o texto com spacy
    doc = nlp(texto)
                
    #percorre os tokens processado para poder obter os lemas e junta no novo texto para salvar a linha
    lemmas = [token.lemma_ for token in doc]
    
    return ' '.join(lemmas)
    
    
if __name__ == "__main__":
    __main__()
