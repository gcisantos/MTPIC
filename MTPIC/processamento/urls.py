# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 22:13:29 2018

@author: GCISANTOS
"""

from django.urls import path
from . import views,processosAjax
urlpatterns = [
    #path('',views.idioma),
    #path('inicio/',views.index),
    path('',views.index),
    path('stemming/',views.stemming),
    path('lematizador/',views.lematizador),
    path('stopWords/',views.stopWords),
    path('tokenizer/',views.tokenizer),
    path('extratorSubTema/',views.extratorSubTema),
    path('mineradorCompleto/',views.mineradorCompleto),
    path('resultadoProcessamento/',views.resultadoProcessamento),
    path('teste/',views.teste),
    
    

    path('extratorTemaCentral/',views.extratorTemaCentral),
    path('processaStemming/',processosAjax.processaStemming),
    path('processaLemmatization/',processosAjax.processaLemmatization),
    path('processaStopWords/',processosAjax.processaStopWords),
    path('processaTokenizer/',processosAjax.processaTokenizer),
    path('processaTemaCentral/',processosAjax.processaTemaCentral),
    path('processaTeste/',processosAjax.processaTeste),
    path('processasubTema/',processosAjax.processasubTema),
    path('processaTudo/',processosAjax.processaTudo)    ,
    path('obtemdadosProcessados/',processosAjax.obtemdadosProcessados),
    #path('iniciaServer/',processosAjax.iniciaServer)  
    


]
