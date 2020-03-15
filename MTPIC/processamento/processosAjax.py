from django.shortcuts import render,HttpResponse
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from . import models

#Obtem pasta pardrão para referenciar
config = models.Configuracoes.objects.get(id_config = 1)

caminho = str(config.caminho_raiz_programas)
caminho = caminho.replace("\\MTPIC_Processador","")

import sys
sys.path.insert(0,caminho+"\\MTPIC_Processador\\PreprocessamentoTexto\\")

sys.path.insert(1,caminho+"\\MTPIC_Processador\\")

import operacoesBanco

import preprocess_stemming

import preprocess_lemmatization

import removalStopwords

import tokenizer

def obtemLinguagem():
    with open(caminho+"\\MTPIC\\processamento\\static\\config\\config.txt", 'r',encoding='utf8') as configuracoesLeitura:
        for linha in configuracoesLeitura.readlines():
            if(linha.startswith("Linguagem")):
                idProcesso = linha.split(":")
                idProcesso = idProcesso[1]
                linguagens = {"portugues":"pt","english":"en","español":"es"}
                configuracoesLeitura.close()
                return linguagens[idProcesso.replace('\n','')]
        configuracoesLeitura.close()
    return ""

@csrf_exempt
def processaStemming(request):
    linguagem = obtemLinguagem()
    print(linguagem)
    if request.method == 'POST' and linguagem != "":
        texto = request.POST['texto']
        print(preprocess_stemming.preProcess(texto,linguagem))
        data = {
            'texto':preprocess_stemming.preProcess(texto,linguagem)
        }
        return JsonResponse(data)
    return None

@csrf_exempt
def processaLemmatization(request):
    linguagem = obtemLinguagem()
    if request.method == 'POST' and linguagem != "":
        texto = request.POST['texto']
        print(preprocess_lemmatization.preProcess(texto))
        data = {
            'texto':preprocess_lemmatization.preProcess(texto)
        }
        return JsonResponse(data)
    return None


@csrf_exempt
def processaStopWords(request):
    linguagem = obtemLinguagem()
    if request.method == 'POST' and linguagem != "":
        texto = request.POST['texto']
        print(removalStopwords.removalStopwordsText(texto,linguagem))
        data = {
            'texto':removalStopwords.removalStopwordsText(texto,linguagem)
        }
        return JsonResponse(data)
    return None


@csrf_exempt
def processaTokenizer(request):
    if request.method == 'POST':
        texto = request.POST['texto']
        print(tokenizer.tokenizerText(texto))
        data = {
            'texto':tokenizer.tokenizerText(texto)
        }
        return JsonResponse(data)
    return None

@csrf_exempt
def processaTemaCentral(request):
    from . import obtemTexto
    obtemTemas = obtemTexto.ObtemTexto(request)

    data = {'texto':obtemTemas.obterTexto() }  
    return JsonResponse(data)   

@csrf_exempt
def processasubTema(request):
    from . import obtemTexto
    obtemTemas = obtemTexto.ObtemTexto(request)

    data = {'texto':obtemTemas.obtemSubTema() }  
    return JsonResponse(data)  

@csrf_exempt
def processaTeste(request):
    if request.method == 'POST' and request.FILES['myfile']:
        print("\n\n\nok\n\n\n")
        myfile = request.FILES['myfile']        
       
        data = {'texto':""} 
        return JsonResponse(data)  
    return None

    
@csrf_exempt
def processaTudo(request):
    from . import obtemTexto
    obtemTemas = obtemTexto.ObtemTexto(request)
    tema,subTema,grafo,erro = obtemTemas.obtemSubTema_Tema()
    data = {'tema':tema,'subTema':subTema,'grafo':grafo,'erro':erro}  
    return JsonResponse(data)  

@csrf_exempt
def obtemdadosProcessados(request):
    from . import obtemTexto
    obtemTemas = obtemTexto.ObtemTexto(request)
    tema,subTema,grafo,erro = obtemTemas.obtemSubTema_Tema_processados()
    data = {'tema':tema,'subTema':subTema,'grafo':grafo,'erro':erro}  
    return JsonResponse(data)  
    
@csrf_exempt
def iniciaServer(request):
    if request.method == 'POST':
        linguagem = request.POST.get("linguagem")

        import os
        import signal
        import subprocess      

        print("iniciando\n\n")
        print("Linguagem Selecionada = "+str(linguagem)+"\n\n")

        #Realiza leitura do arquivo para verficar se existe ao menos um processo já aberto e tenta finalizar
        with open(caminho+"\\MTPIC\\processamento\\static\\config\\config.txt", 'r',encoding='utf8') as configuracoesLeitura:
            for linha in configuracoesLeitura.readlines():
                if(linha.startswith("Processo")):
                    idProcesso = linha.split(":")
                    idProcesso = idProcesso[1]
                    if(idProcesso!=""):
                        try:
                            print("Processo a finalizar " +str(int(idProcesso)) )
                            os.kill(int(idProcesso), signal.SIGTERM)
                            print("Processo Encerrado ")
                            pass
                        except :
                            pass


        configuracoes = open(caminho+"\\MTPIC\\processamento\\static\\config\\config.txt", 'w',encoding='utf8')

        configuracoes.write("Linguagem:"+str(linguagem)+"\n")

        linguagens = {"portugues":"pt","english":"en","español":"es"}

        cmd = "python C:\\MTPIC\\ProcessadorTextos\\processadorTextos.py -l "+linguagens[str(linguagem)]

        print(cmd)
        # The os.setsid() is passed in the argument preexec_fn so
        # it's run after the fork() and before  exec() to run the shell.
        pro = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE) 
   
        print(pro.pid)





        configuracoes.write("Processo:"+str(pro.pid)+"\n")
        print("Carga Finalizada \n\n")


        data = {'texto':""} 
        return JsonResponse(data)  
    return None