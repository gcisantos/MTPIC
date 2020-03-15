try:
    from . import Prep as prep
except ImportError:
    x=0

try:
    import Prep as prep
except ModuleNotFoundError:
    x=0

#bibliotecas para ler os comandos
import sys, getopt, os

def main(argv):    
    #idiomas disponiveis
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
    


    arquivoWikipedia = ''
    pastaSaida = ''
    
    try:
        opts,args = getopt.getopt(argv,"hi:o:l:",["arquivoWikipedia=","pastaSaida=","linguagem="])
    except getopt.GetoptError:
        print('Prep.py -i <arquivoWikipedia> -o <pastaSaida> -l <linguagem> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('\n\nPara utilização devem ser inseridos os dados no seguinte formato:\n\nPrep.py -i <arquivoWikipedia> -o <pastaSaida> -l <linguagem>\n\nLinguagens aceitas:\n'+('\n'.join([a+' - '+b for a,b in idiomas.items()])))
            sys.exit()
        elif opt in ("-i", "--arquivoWikipedia"):
            arquivoWikipedia = arg
        elif opt in ("-o", "--pastaSaida"):
            pastaSaida = arg
        elif opt in ("-l", "--linguagem"):
            linguagem = arg
            if(linguagem not in idiomas):
                print(linguagem)
                print("Linguagem seleciona é inválida são aceitas somente:\n "+('\n'.join([b+' - '+a for a,b in idiomas.items()])))
                sys.exit()

    logIni = "\n*************Parametros Selecionados*************"
    logIni = logIni+'\nArquivo de Entrada '+ arquivoWikipedia
    logIni = logIni+'\nPasta de Saida '+ pastaSaida
    logIni = logIni+'\nLinguagem Selecionada '+ linguagem
    logIni = logIni+"\n*************************************************"

    


    if(arquivoWikipedia!="" and pastaSaida!="" and linguagem!=""):

        prep.Prep(arquivoWikipedia,pastaSaida,linguagem)

    else:
        print("Parâmetros informados estão são inválidos")
        sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])