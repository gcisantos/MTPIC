import extratorTema,operacoesBanco

from time import sleep

from os.path import dirname

import sys, getopt,json,os,os.path

extrator = None
banco = None

def __main__(argv):
    global extrator
    global banco
    
    linguagem = ''
    idioma = ''
    caminhoBase = ''
    
    arquivoConfig = ''
    
    try:
        opts,args = getopt.getopt(argv,"hi:",["arquivoConfiguracao="])
    except getopt.GetoptError:
        print('processadorTextos.py -i <arquivoConfiguracao> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('\n\nPara utilização devem ser inseridos os dados no seguinte formato:\n\nprocessadorTextos.py -i <arquivoConfiguracao> ')
            sys.exit()
        elif opt in ("-i", "--arquivoConfiguracao"):
            arquivoConfig = arg
    
    with open(arquivoConfig) as json_file:
        data = json.load(json_file)
        linguagem =data['linguagem']
        idioma =data['idioma']
        caminhoBase =data['caminhoBase']
        
        
    extrator = extratorTema.ExtratorTema(linguagem,caminhoBase)
    banco = operacoesBanco.OperacoesBanco(str(dirname(os.path.abspath(os.path.join(os.getcwd(), os.pardir))))+"\\MTPIC\\MTPIC\\db.sqlite3",(1,idioma,linguagem,os.getcwd(),caminhoBase))
    inicia_verificador()

   
def inicia_verificador():
    global extrator
    global banco
    while(True):
        sleep(0.1)
        #obtem os itens pendentes
        itensPendentes = banco.itens_pendentes()
        #verifica se existe  itens pendentes
        
        if(len(itensPendentes) > 0):
            #caso existe realiza atualização processando os dados
            for ids,texto,taxaAceitacao,euristicaProcessamento,tipoBusca in itensPendentes:
                retornoTexto,qtdTer,termos,data = ("","","","")
                if(tipoBusca==1):
                    retornoTexto,qtdTer,termos,data = extrator.retornaTemaCentral(texto,taxaAceitacao,euristicaProcessamento)
                    banco.processa_item((retornoTexto,data,ids))
                elif(tipoBusca==2):
                    retornoTexto,qtdTer,termos,data = extrator.retornaSubtemas(texto)
                    banco.processa_item_sub((retornoTexto,data,ids))
                elif(tipoBusca==3):
                    temas,subtemas,grafo,data =extrator.retornaTema_subTema(texto,taxaAceitacao,euristicaProcessamento)
                    banco.processa_item_sub_Tema((temas,subtemas,grafo,data,ids))        
            
            print("\n\n******* Processador Textos ******* ")
            print("\nForam processados: "+str(len(itensPendentes) ))
            itensPendentes = None

if __name__ == "__main__":
    __main__(sys.argv[1:])