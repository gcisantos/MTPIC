

class Prep:
    #****************IMPORTS****************
    import warnings
    warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
    warnings.filterwarnings(action='ignore', category=UserWarning, module='numpy')

    #importa modulos desenvolvidos por mim
    #wiki é a reimplementação do que eu preciso para poder extrair tbm os titulos

    import reimplementado_make_wikicorupus as wiki

    import nltk
    from nltk import word_tokenize
    #stopwords
    from nltk.corpus import stopwords
    #stem
    from nltk.stem.snowball import SnowballStemmer    
    #gensim
    import gensim
    from gensim.models.doc2vec import Doc2Vec, TaggedDocument

    #biblioteca do sistema 
    import os
    import multiprocessing
    #biblioteca utilizada para medir o tempo de processamento
    import time
    import datetime
    #Biblioteca para trabalhar com dados compactados e economizar espaço
    import gzip
    #biblioteca utilizada para gerar arquivo de configuração
    import json

    #***************************************

    #****************VARIÁVEIS****************
    caminhoBase = ""

    #Armazena o caminho onde está o dump do wikipedia que será lido
    caminhoDumpWiki =""
    
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

    #idioma selecionado
    idioma =""
    linguagem = ""
    #***************************************

    #*****************Váriaveis caminhos de arquivos**********************
    pastaAnalisadores = ""
    cm_textosWikipedia = ""
    cm_titulosWikipedia = ""
    cm_textosWikipedia_stemming = ""
    cm_dicionario = ""
    cm_doc2Bow = ""
    cm_tfidf = ""
    cm_similaridades = ""
    cm_doc2vec = ""


    #variaveis do log e tempo inicial
    start_time = 0
    logSaida = None

    #define classe main para chamar o método principal

    def __init__(self,arquivoEntrada,pastaSaida,idiomaSelecionado):
        #Inicializa Variaveis
        self.idioma = self.idiomas[idiomaSelecionado]
        self.caminhoDumpWiki = arquivoEntrada
        self.caminhoBase = pastaSaida
        self.linguagem = idiomaSelecionado
        
        #Cria estruturas de pasta        
        pastaBase = self.caminhoBase+"\\"+self.idioma+"\\Arquivos_Gerados\\"        
        if not self.os.path.exists(pastaBase):
            self.os.makedirs(pastaBase)
        
        pastaStemming = pastaBase+"Stemming\\"                    
        if not self.os.path.exists(pastaStemming):
            self.os.makedirs(pastaStemming)

        self.pastaAnalisadores = pastaBase+"Analisadores\\"                    
        if not self.os.path.exists(self.pastaAnalisadores):
            self.os.makedirs(self.pastaAnalisadores)
            
        pastaDoc2Vec = pastaBase+"Doc2Vec\\"        
        if not self.os.path.exists(pastaDoc2Vec):
            self.os.makedirs(pastaDoc2Vec)

        #Preenche variaves com os caminhos dos arquivos
        self.cm_textosWikipedia = pastaBase+"TextosWikipedia_"+self.linguagem+".gz"
        self.cm_titulosWikipedia = pastaBase+"TitulosWikipedia_"+self.linguagem+".gz"
        self.cm_textosWikipedia_stemming = pastaStemming+"BaseWikipedia_"+self.linguagem+"_Stemizado.gz"
        self.cm_dicionario = self.pastaAnalisadores+"dicionario_"+self.linguagem+".dict"
        self.cm_doc2Bow = self.pastaAnalisadores+"dicionarioDoc2Bow_"+self.linguagem+".dict"
        self.cm_tfidf = self.pastaAnalisadores+"tf_idf_"+self.linguagem+".tfidf_model"
        self.cm_similaridades = self.pastaAnalisadores+"similaridades_"+self.linguagem+".sims"
        self.cm_doc2vec = pastaDoc2Vec+"dv2_"+self.linguagem+".model"
                    
        logIni = "\n*****************Parametros Selecionados****************\n"
        logIni = logIni+'\n   Arquivo de Entrada: '+ arquivoEntrada
        logIni = logIni+'\n       Pasta de Saida: '+ pastaSaida
        logIni = logIni+'\nLinguagem Selecionada: '+ self.linguagem+' - '+self.idioma 
        logIni = logIni+"\n\n********************************************************\n\n"

        #Gera arquivo de configuração
        config ={
            "linguagem":self.linguagem,
            "idioma":self.idioma,
            "caminhoBase":pastaBase
        }
        
        with open(self.caminhoBase+"\\config_"+self.idioma+".ini",'w') as arquivo:
            self.json.dump(config,arquivo)
            
        print(logIni)
        
        #Inicia Processo
        self.IniciaLog()
        
        print("*************Iniciando preparação dos dados*************")
        print("********************************************************")
        print()     
        self.ExtrairTextos()
        self.Stemming()
        self.GeraAnalisadores()
        self.processaDoc2Vec()
        print()
        print("********************************************************")
        print("*************Preparação dos dados Finalizada************")
        
        self.FinalizaLog()

    

    def IniciaLog(self):    
        self.start_time = self.time.time()
        self.logSaida = open(self.caminhoBase+"\\"+self.idioma+"\\log"+self.datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".txt", 'w',encoding='utf8')        

    def EscreveLog(self,texto):    
        texto = self.datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] - ")+str(round((self.time.time() - self.start_time),2))+" - "+texto
        self.logSaida.write(texto)
        print(texto) 
        
    def FinalizaLog(self):
        self.logSaida.close()

    #Esse método realiza todo o processo de extrair os textos do corpus
    def ExtrairTextos(self):    
        

        #Obtem o dump do wikipedia para realizar a leitura
        textos = self.wiki.WikiCorpus(self.caminhoDumpWiki, lemmatize=False, dictionary={})
        
        #Inicia o arquivo para gravar os titulos
        corpusTitles = self.gzip.open(self.cm_titulosWikipedia, 'wb')
        
        self.EscreveLog("Iniciando processamento dos titulos")       

        #variavel para contagem de documentos lidos
        i = 0     
        
        #Percorre pelos titulos obtidos do dump do wikipedia    
        for text in textos.get_titles():
            #Aqui é aplicado uma euristica para remover os espaços que foram criados em todas as letras
            
            #Primeiro substitui espaços duplos pelo meu separador #|@|# dessa forma consigo recuperar os espaços entre as palavras depois
            removeEspacoDuplo = (" ".join(map(lambda x:x, text))).replace("  ","#|@|#")
                                
            #Remove os espaços entre as letras
            removeEspacoSimples= removeEspacoDuplo.replace(" ","")
            
            #Coloca o espaço entre as palavras
            colocaEspaco = removeEspacoSimples.replace("#|@|#","_")
                                                    
            #Escreve titulo no arquivo
            corpusTitles.write((colocaEspaco + '\n').encode('utf8'))
            
            #Exibe o processamento de 1000 em 1000
            i = i + 1

        self.EscreveLog("Total de %s titulos processados" % str(i))  

        self.EscreveLog("Iniciando processamento dos documentos")

        #Zera Contador
        i=0

        #Inicia o arquivo para gravar o corpus
        corpus = self.gzip.open(self.cm_textosWikipedia, 'wb')
        
        #percorre os textos obtidos do dump do wikipedia sem tratar
        for text in textos.get_texts():    

            #Escreve texto no documento
            corpus.write((" ".join(map(lambda x:x,text))+'\n').encode('utf8'))
            
            #Exibe o processamento de 1000 em 1000
            i = i + 1
        
        corpusTitles.close()
        corpus.close()

        self.EscreveLog("Total de %s textos processados" % str(i))  

        self.EscreveLog("Processamento de textos finalizados") 

    #Esse método realiza todo o processo de stemming nos textos processados
    def Stemming(self):
        #cria método responsável por gravar os arquivos    
        corpusStemm = self.gzip.open(self.cm_textosWikipedia_stemming, 'wb')    

        self.EscreveLog("Iniciando processamento método Stemming")     

        removeStopWords =self.stopwords.words(self.idioma)
        
        with self.gzip.open(self.cm_textosWikipedia,"rb") as arquivo:
            #realiza leitura linha a linha do corpus
            for linha in arquivo.readlines():
                #realiza aa remoção de stop words
                linha = [word for word in self.nltk.word_tokenize(linha.decode('utf8')) if word.lower() not in removeStopWords]            
                    
                corpusStemm.write((' '.join([self.SnowballStemmer(self.idioma).stem(token) for token in linha])+'\n').encode('utf8'))         
        arquivo.close()
        corpusStemm.close()

        self.EscreveLog("Textos processados pelo método Stemming")

    #Esse método realiza o processo de gerar as similaridades entre os documentos
    def GeraAnalisadores(self):
        lista = []

        self.EscreveLog("Iniciando processamento do dicionário")
        self.EscreveLog("Lendo arquivos gerados do wikipédia")

        with self.gzip.open(self.cm_textosWikipedia_stemming,"rb") as arquivo:
            for linha in arquivo:
                lista.append(linha.decode('utf8').split(" "))      
        arquivo.close()
        
        #Cria dicionario dos documentos
        self.EscreveLog("Criando dicionário")
        dictionary = self.gensim.corpora.Dictionary(lista)
        
        #Salva Dicionário para ser usado depois
        self.EscreveLog("Salvando dicionário")
        dictionary.save(self.cm_dicionario)
        
        #Gera Corpus
        self.EscreveLog("Gerando Corpus")
        corpus = []
        while(len(lista)>0):
            corpus.append(dictionary.doc2bow(lista[0]))
            lista.remove(lista[0])

        
        #salva o doc2Bow em um arquivo
        self.EscreveLog("Salvando corpus")
        self.gensim.corpora.MmCorpus.serialize(self.cm_doc2Bow, corpus)

        #cria modelo tf-idf
        self.EscreveLog("Gerando TF-IDF")
        tf_idf = self.gensim.models.TfidfModel(corpus)    
            
        #salva o tf_idf em arquivo
        self.EscreveLog("Salvando TF-IDF")
        tf_idf.save(self.cm_tfidf)

        self.EscreveLog("Gerando Similaridades")                
        sims = self.gensim.similarities.Similarity(self.pastaAnalisadores,tf_idf[corpus],
                                            num_features=len(dictionary))

        self.EscreveLog("Salvando Similaridades")  
        sims.save(self.cm_similaridades)

        self.EscreveLog("Analisadores Gerados") 
    
    #Esse método é responsável por gerar os arquivos doc2vec, distancia entre todos os documentos
    def processaDoc2Vec(self):
        self.EscreveLog("Iniciando processamento do Doc2Vec")
        contador = 0
        #Carrega documentos para memória
        """
        tagged_data = []
        with self.gzip.open(self.cm_textosWikipedia_stemming,"rb") as arquivo:
            for linha in arquivo:
                palavras = [word.lower()  for word in self.word_tokenize((linha.decode('utf8')))]
                tagged_data.append(self.TaggedDocument(words=palavras, tags=[str(contador)]))
                contador = contador+1
                if(contador%1000==0):
                    self.EscreveLog(" % linhas processadas no Doc2Vec " % contador)
        arquivo.close()
        """

        
        #Carrega documentos para memória
        documentos = []
        with self.gzip.open(self.cm_textosWikipedia_stemming,"rb") as arquivo:
            for linha in arquivo.readlines():
                documentos.append([word for word in self.nltk.word_tokenize(linha.decode('utf8'))])
        arquivo.close()

        tagged_data = [self.TaggedDocument(words=_d, tags=[str(i)]) for i, _d in enumerate(documentos)]

        cores = self.multiprocessing.cpu_count()
        
        self.EscreveLog("Criando modelo para treinamento")

        model = self.Doc2Vec( 
                        min_alpha=0.00025,
                        dbow_words=1, 
                        size=350, 
                        window=8, 
                        min_count=15,
                        workers=cores,
                        dm =0)

        model.build_vocab(tagged_data)

        self.EscreveLog("Iniciando treinamento doc2vec")
        model.train(tagged_data,total_examples=model.corpus_count,epochs=30)		

        """max_epochs = 10

        for epoch in range(max_epochs):
            self.EscreveLog('Interação loop {0}'.format(epoch))
            model.train(tagged_data,
                        total_examples=model.corpus_count,
                        epochs=model.iter)
            # decrease the learning rate
            model.alpha -= 0.0002
            # fix the learning rate, no decay
            model.min_alpha = model.alpha"""
        
        self.EscreveLog("Salvando modelo treinado")
        model.save(self.cm_doc2vec)
        self.EscreveLog("Processo Doc2Vec concluído!")
    