
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

import time

from . import processosAjax
#from . import extratorTema


# Create your views here.
def idioma(request):
    return render(request,"idioma.html")

def index(request):
        return render(request,"index.html")
"""if(validaIdioma(request)):
        return render(request,"idioma.html")
    else:
        idioma = processosAjax.obtemLinguagem()
        if(idioma == 'pt'):
                return render(request,"index.html")
        elif (idioma == 'en'):
                return render(request,"index_en.html")
        elif (idioma == 'es'):
                return render(request,"index_es.html")"""


def stemming(request):
        return render(request,"modulos/stemming.html")
"""if(validaIdioma(request)):
        return render(request,"idioma.html")
    else:
        idioma = processosAjax.obtemLinguagem()
        if(idioma == 'pt'):
                return render(request,"modulos/stemming.html")
        elif (idioma == 'en'):
                return render(request,"modulos/stemming_en.html")
        elif (idioma == 'es'):
                return render(request,"modulos/stemming_es.html")"""
        
       

def lematizador(request):
        return render(request,"lematizador.html")
"""if(validaIdioma(request)):
        return render(request,"idioma.html")
    else:
        idioma = processosAjax.obtemLinguagem()
        if(idioma == 'pt'):
                return render(request,"modulos/lematizador.html")
        elif (idioma == 'en'):
                return render(request,"modulos/lematizador_en.html")
        elif (idioma == 'es'):
                return render(request,"modulos/lematizador_es.html")"""
        

def stopWords(request):
        return render(request,"modulos/stopWords.html")
"""if(validaIdioma(request)):
        return render(request,"idioma.html")
    else:
        idioma = processosAjax.obtemLinguagem()
        if(idioma == 'pt'):
                return render(request,"modulos/stopWords.html")
        elif (idioma == 'en'):
                return render(request,"modulos/stopWords_en.html")
        elif (idioma == 'es'):
                return render(request,"modulos/stopWords_es.html")"""
        
    
def tokenizer(request):
        return render(request,"modulos/tokenizer.html")
"""if(validaIdioma(request)):
        return render(request,"idioma.html")
    else:
        idioma = processosAjax.obtemLinguagem()
        if(idioma == 'pt'):
                return render(request,"modulos/tokenizer.html")
        elif (idioma == 'en'):
                return render(request,"modulos/tokenizer_en.html")
        elif (idioma == 'es'):
                return render(request,"modulos/tokenizer_es.html")"""
        

def teste(request):
    validaIdioma(request)
    return render(request,"modulos/teste.html")

def extratorTemaCentral(request):
        return render(request,"modulos/extratorTemaCentral.html")
        """
    if(validaIdioma(request)):
        return render(request,"idioma.html")
    else:
        idioma = processosAjax.obtemLinguagem()
        if(idioma == 'pt'):
                return render(request,"modulos/extratorTemaCentral.html")
        elif (idioma == 'en'):
                return render(request,"modulos/extratorTemaCentral_en.html")
        elif (idioma == 'es'):
                return render(request,"modulos/extratorTemaCentral_es.html")  
                """
        

def extratorSubTema(request):
        return render(request,"modulos/extratorSubTema.html")
        """
    if(validaIdioma(request)):
        return render(request,"idioma.html")
    else:
        idioma = processosAjax.obtemLinguagem()
        if(idioma == 'pt'):
                return render(request,"modulos/extratorSubTema.html")
        elif (idioma == 'en'):
                return render(request,"modulos/extratorSubTema_en.html")
        elif (idioma == 'es'):
                return render(request,"modulos/extratorSubTema_es.html")"""  
        

def mineradorCompleto(request):
        return render(request,"modulos/mineradorCompleto.html")
        """
    if(validaIdioma(request)):
        return render(request,"idioma.html")
    else:
        idioma = processosAjax.obtemLinguagem()
        if(idioma == 'pt'):
                return render(request,"modulos/mineradorCompleto.html")
        elif (idioma == 'en'):
                return render(request,"modulos/mineradorCompleto_en.html")
        elif (idioma == 'es'):
                return render(request,"modulos/mineradorCompleto_es.html")  """
        

def resultadoProcessamento(request):
        return render(request,"modulos/resultadoProcessamento.html")
        """
    if(validaIdioma(request)):
        return render(request,"idioma.html")
    else:
        idioma = processosAjax.obtemLinguagem()
        if(idioma == 'pt'):
                return render(request,"modulos/resultadoProcessamento.html")
        elif (idioma == 'en'):
                return render(request,"modulos/resultadoProcessamento_en.html")
        elif (idioma == 'es'):
                return render(request,"modulos/resultadoProcessamento_es.html") """



def validaIdioma(request):
    with open("C:\\MTPIC\\MTPIC\\processamento\\static\\config\\config.txt", 'r',encoding='utf8') as configuracoesLeitura:        
        tamanho =len(configuracoesLeitura.readlines()) 
        configuracoesLeitura.close()
        return tamanho<=0
        
            